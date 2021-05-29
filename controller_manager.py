from PySide2.QtCore import QRunnable, Slot, QFile, QTextStream, QObject, Signal, QTimer
from PySide2.QtGui import QPixmap
import re
import qimage2ndarray
from double_side_manager import DoubleSideManager
from shape_core.pcb_manager import PcbObj
from shape_core.path_manager import MachinePath
from collections import OrderedDict as Od
import logging
import traceback

logger = logging.getLogger(__name__)


class ControllerWorker(QObject):
    update_layer_s = Signal(Od, str, str, bool)  # Signal to update layer visualization
    update_path_s = Signal(str, list)            # Signal to update path visualization
    update_camera_image_s = Signal(QPixmap)      # Signal to update Camera Image
    update_status_s = Signal(list)               # Signal to update controller status
    update_console_text_s = Signal(str)          # Signal to send text to the console textEdit
    serial_send_s = Signal(str)                  # Signal to send text to the serial

    update_probe_s = Signal(list)                # Signal to update probe value
    update_abl_s = Signal(list)                  # Signal to update Auto-Bed-Levelling value

    STATUSPAT = re.compile(
        r"^<(\w*?),MPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),WPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),?(.*)>$")
    POSPAT = re.compile(
        r"^\[(...):([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*):?(\d*)\]$")
    TLOPAT = re.compile(r"^\[(...):([+\-]?\d*\.\d*)\]$")
    DOLLARPAT = re.compile(r"^\[G\d* .*\]$")
    SPLITPAT = re.compile(r"[:,]")
    VARPAT = re.compile(r"^\$(\d+)=(\d*\.?\d*) *\(?.*")

    def __init__(self, serial_rx_queue):
        super(ControllerWorker, self).__init__()

        self.view_controller = ViewController()
        self.control_controller = ControlController()
        self.align_controller = AlignController()

        self.serialRxQueue = serial_rx_queue

        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.on_poll_timeout)
        self.poll_timer.setInterval(120)
        self.poll_timer.start()

        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.on_camera_timeout)
        self.camera_timer.setInterval(120)
        self.camera_timer.start()

        self.status_l = []

        self.align_active = False

        self.dro_status_updated = False
        self.prb_activated = False
        self.abl_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.prb_val = []
        self.abl_val = []
        self.abl_cmd_ls = []
        self.prb_num_todo = 0
        self.prb_num_done = 0
        self.prb_reps_todo = 1
        self.prb_reps_done = 0

    # ***************** VIEW related functions. ***************** #

    @Slot(str, str)
    def load_new_layer(self, layer, layer_path):
        [loaded_layer, exc_flag] = self.view_controller.load_new_layer(layer, layer_path)
        if loaded_layer is not None:
            self.update_layer_s.emit(loaded_layer, layer, layer_path, exc_flag)

    @Slot(str, Od, str)
    def generate_new_path(self, tag, cfg, machining_type):
        new_paths = self.view_controller.generate_new_path(tag, cfg, machining_type)
        self.update_path_s.emit(tag, new_paths)

    # ***************** CONTROL related functions. ***************** #

    def on_poll_timeout(self):
        self.serial_send_s.emit(str("?\n"))  # "?\n")

    @Slot()
    def parse_rx_queue(self):
        if not self.serialRxQueue.empty():
            try:
                element = self.serialRxQueue.get(block=False)
                if element:
                    logging.debug("Element received: " + element)
                    if re.match("^<.*>\s*$\s", element):
                        self.update_status_s.emit(self.control_controller.parse_bracket_angle(element))
                    elif re.match("^\[.*\]\s*$\s", element):
                        self.control_controller.parse_bracket_square(element)
                        [ack_prb_flag, ack_abl_flag, send_next, other_cmd_flag] = \
                            self.control_controller.process_probe_and_abl()
                        if ack_prb_flag:
                            self.ack_probe()
                        if ack_abl_flag:
                            self.ack_auto_bed_levelling()
                        if send_next:
                            self.send_next_abl()
                        if other_cmd_flag:
                            self.update_console_text_s.emit(element)
                    elif re.match("ok\s*$\s", element):
                        pass
                    else:
                        self.update_console_text_s.emit(element)
            except BlockingIOError as e:
                logging.error(e, exc_info=True)
            except:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    def execute_gcode_cmd(self, cmd_str):
        """ Send generic G-CODE command coming from elsewhere. """
        logging.debug(cmd_str)
        self.serial_send_s.emit(cmd_str)

    def cmd_probe(self, probe_z_max, probe_feed_rate):
        probe_cmd_s = self.control_controller.cmd_probe(probe_z_max, probe_feed_rate)
        logging.info(probe_cmd_s)
        self.serial_send_s.emit(probe_cmd_s)  # Execute probe

    def ack_probe(self):
        prb_val = self.control_controller.get_probe_value()
        logging.info("Probe: " + str(prb_val))
        self.update_probe_s.emit(prb_val)

    def cmd_auto_bed_levelling(self, xy_coord_list, travel_z, probe_z_max, probe_feed_rate):
        self.control_controller.cmd_auto_bed_levelling(xy_coord_list, travel_z, probe_z_max, probe_feed_rate)
        self.send_next_abl()  # Send first probe command.

    def send_next_abl(self):
        next_abl_cmd = self.control_controller.get_next_abl_cmd()
        logging.info(next_abl_cmd)
        self.serial_send_s.emit(next_abl_cmd)  # Execute next Probe of Auto-Bed-Levelling

    def ack_auto_bed_levelling(self):
        abl_values = self.control_controller.get_abl_value()
        logging.info("ABL values: " + str(abl_values))
        self.update_abl_s.emit(abl_values)

# ***************** ALIGN related functions. ***************** #

    def on_camera_timeout(self):
        if self.align_active:
            image = self.align_controller.camera_new_frame()
            self.update_camera_image_s.emit(QPixmap.fromImage(image))

    @Slot(bool)
    def set_align_is_active(self, align_is_active):
        self.align_active = align_is_active

    @Slot(int)
    def update_threshold_value(self, new_threshold):
        self.align_controller.update_threshold_value(new_threshold)


class ViewController(QObject):
    def __init__(self):
        super(ViewController, self).__init__()
        self.pcb = PcbObj()

    def load_new_layer(self, layer, layer_path):
        try:
            grb_tags = self.pcb.GBR_KEYS
            exc_tags = self.pcb.EXN_KEYS
            if layer in grb_tags:
                self.pcb.load_gerber(layer_path, layer)
                self.pcb.get_gerber(layer)
                loaded_layer = self.pcb.get_gerber_layer(layer)
                return [loaded_layer, False]
            if layer in exc_tags:
                self.pcb.load_excellon(layer_path, layer)
                self.pcb.get_excellon(layer)
                loaded_layer = self.pcb.get_excellon_layer(layer)
                return [loaded_layer, True]
        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logging.error(e, exc_info=True)
        except:
            logger.error("Uncaught exception: %s", traceback.format_exc())
        return [None, None]

    def generate_new_path(self, tag, cfg, machining_type):
        if machining_type == "gerber" or machining_type == "profile":
            machining_layer = self.pcb.get_gerber_layer(tag)
        elif machining_type == "drill":
            machining_layer = self.pcb.get_excellon_layer(tag)
        else:
            logger.error("Wrong machining type")
        path = MachinePath(tag, machining_type)
        path.load_geom(machining_layer[0])
        path.load_cfg(cfg)
        path.execute()
        new_paths = path.get_path()
        return new_paths


class ControlController(QObject):
    STATUSPAT = re.compile(
        r"^<(\w*?),MPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),WPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),?(.*)>$")
    POSPAT = re.compile(
        r"^\[(...):([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*):?(\d*)\]$")
    TLOPAT = re.compile(r"^\[(...):([+\-]?\d*\.\d*)\]$")
    DOLLARPAT = re.compile(r"^\[G\d* .*\]$")
    SPLITPAT = re.compile(r"[:,]")
    VARPAT = re.compile(r"^\$(\d+)=(\d*\.?\d*) *\(?.*")

    def __init__(self):
        super(ControlController, self).__init__()
        self.status_l = []
        self.dro_status_updated = False
        self.prb_activated = False
        self.abl_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.prb_val = []
        self.abl_val = []
        self.abl_cmd_ls = []
        self.prb_num_todo = 0
        self.prb_num_done = 0
        self.prb_reps_todo = 1
        self.prb_reps_done = 0

    def get_probe_value(self):
        return self.prb_val

    def get_abl_value(self):
        return self.abl_val

    def get_next_abl_cmd(self):
        return self.abl_cmd_ls[self.prb_num_done]

    def process_probe_and_abl(self):
        ack_prb_flag = False
        ack_abl_flag = False
        send_next = False
        other_cmd_flag = False
        logging.debug("self.prb_activated: " + str(self.prb_activated))
        logging.debug("self.prb_updated: " + str(self.prb_updated))
        if self.prb_activated and self.prb_updated:
            self.prb_activated = False
            self.prb_updated = False
            ack_prb_flag = True
        elif self.abl_activated:
            [ack_abl_flag, send_next] = self.update_abl()
        else:
            logging.warning("Not a probe, nor an ABL.")
            other_cmd_flag = True

        return [ack_prb_flag, ack_abl_flag, send_next, other_cmd_flag]

    def parse_bracket_angle(self, line):
        fields = line[1:-1].split("|")
        status = fields[0]
        mpos_l = []

        for field in fields[1:]:
            word = self.SPLITPAT.split(field)
            if word[0] == "MPos":
                try:
                    mpos_l = [word[1], word[2], word[3]]
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except:
                    logger.error("Uncaught exception: %s", traceback.format_exc())

        return [status, mpos_l]

    def parse_bracket_square(self, line):
        word = self.SPLITPAT.split(line[1:-1])

        if word[0] == "PRB":
            try:
                self.prb_val = [float(word[1]), float(word[2]), float(word[3])]
                self.prb_updated = True
            except (ValueError, IndexError) as e:
                logging.error(e, exc_info=True)
            except:
                logger.error("Uncaught exception: %s", traceback.format_exc())

        return self.prb_val

    def cmd_probe(self, probe_z_max, probe_feed_rate):
        probe_cmd_s = ""
        probe_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # Set probe feed rate
        probe_cmd_s += "G38.2 Z" + str(probe_z_max) + "\n"  # Set probe command

        self.prb_val = []
        self.prb_updated = False
        self.prb_activated = True
        self.prb_num_todo = 1
        self.prb_reps_todo = 1

        return probe_cmd_s

    def cmd_auto_bed_levelling(self, xy_coord_list, travel_z, probe_z_max, probe_feed_rate):
        [self.abl_cmd_ls, self.prb_num_todo] = self.make_cmd_auto_bed_levelling(xy_coord_list, travel_z,
                                                                                probe_z_max, probe_feed_rate)
        self.prb_num_done = 0
        self.prb_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.abl_activated = True

        return [self.abl_cmd_ls, self.prb_num_todo]

    def make_cmd_auto_bed_levelling(self, xy_coord_list, travel_z, probe_z_max, probe_feed_rate):
        abl_cmd_ls = []
        abl_cmd_s = ""
        abl_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # Set probe feed rate

        prb_num_todo = 0
        for coord in xy_coord_list:
            prb_num_todo += 1
            abl_cmd_s += "G00 Z" + str(travel_z) + " F10\n"  # Get to safety Z Travel
            abl_cmd_s += "G00 X" + str(coord[0]) + "Y" + str(coord[1]) + " F10\n"  # Go to XY coordinate
            abl_cmd_s += "G38.2 Z" + str(probe_z_max) + "\n"  # Set probe command
            abl_cmd_s += "G00 Z" + str(travel_z) + " F10\n"  # Get to safety Z Travel
            abl_cmd_ls.append(abl_cmd_s)
            abl_cmd_s = ""

        abl_cmd_ls[-1] += "G00 Z" + str(travel_z) + " F10\n"  # Get to safety Z Travel

        return [abl_cmd_ls, prb_num_todo]

    def update_abl(self):
        ack_flag = False
        send_next = False
        if self.prb_updated:
            self.prb_updated = False
            self.prb_num_done += 1
            self.abl_val.append(self.prb_val)
            self.prb_val = []
            if self.prb_num_done == self.prb_num_todo:
                ack_flag = True
            elif self.prb_num_done < self.prb_num_todo:
                send_next = True
            else:
                logging.error("ABL: Number of probe done exceeded the number of probe to do.")

        return [ack_flag, send_next]


class AlignController(QObject):
    def __init__(self):
        super(AlignController, self).__init__()
        self.double_side_manager = DoubleSideManager()
        self.threshold_value = 0

    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    def camera_new_frame(self):
        frame = self.double_side_manager.get_webcam_frame()
        logger.debug(str(self.threshold_value))
        frame = self.double_side_manager.detect_holes(frame, self.threshold_value)
        image = qimage2ndarray.array2qimage(frame)
        return image
