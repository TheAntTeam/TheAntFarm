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

        self.double_side_manager = DoubleSideManager()

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
        self.threshold_value = 0

        self.pcb = PcbObj()

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

    def on_poll_timeout(self):
        self.serial_send_s.emit("?\n")

    def on_camera_timeout(self):
        if self.align_active:
            frame = self.double_side_manager.get_webcam_frame()
            logger.debug(str(self.threshold_value))
            frame = self.double_side_manager.detect_holes(frame, self.threshold_value)
            image = qimage2ndarray.array2qimage(frame)
            self.update_camera_image_s.emit(QPixmap.fromImage(image))

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
        # print("sq_word    = ")
        # print(word)
        # print("sq_word[0] = " + word[0])
        if word[0] == "PRB":
            try:
                self.prb_val = [float(word[1]), float(word[2]), float(word[3])]
                self.prb_updated = True
            except (ValueError, IndexError) as e:
                logging.error(e, exc_info=True)
            except:
                logger.error("Uncaught exception: %s", traceback.format_exc())

        return self.prb_val

    @Slot(str, str, str)
    def load_new_layer(self, layer, layer_path):
        try:
            grb_tags = self.pcb.GBR_KEYS
            exc_tags = self.pcb.EXN_KEYS
            if layer in grb_tags:
                self.pcb.load_gerber(layer_path, layer)
                self.pcb.get_gerber(layer)
                loaded_layer = self.pcb.get_gerber_layer(layer)
                self.update_layer_s.emit(loaded_layer, layer, layer_path, False)
            if layer in exc_tags:
                self.pcb.load_excellon(layer_path, layer)
                self.pcb.get_excellon(layer)
                loaded_layer = self.pcb.get_excellon_layer(layer)
                self.update_layer_s.emit(loaded_layer, layer, layer_path, True)
        except (AttributeError, ValueError, ZeroDivisionError, IndexError) as e:
            logging.error(e, exc_info=True)
        except:
            logger.error("Uncaught exception: %s", traceback.format_exc())

    @Slot(str, Od)
    def generate_new_path(self, tag, cfg):
        gerb_lay = self.pcb.get_gerber_layer(tag)
        path = MachinePath(tag, machining_type="gerber")
        path.load_geom(gerb_lay[0])
        path.load_cfg(cfg)
        path.execute()
        p = path.get_path()
        self.update_path_s.emit(tag, p)

    @Slot(bool)
    def set_align_is_active(self, align_is_active):
        self.align_active = align_is_active

    @Slot(int)
    def update_threshold_value(self, new_threshold):
        self.threshold_value = new_threshold

    @Slot()
    def parse_rx_queue(self):
        if not self.serialRxQueue.empty():
            try:
                element = self.serialRxQueue.get(block=False)
                if element:
                    logging.debug("Element received: " + element)
                    if re.match("^<.*>\s*$\s", element):
                        self.update_status_s.emit(self.parse_bracket_angle(element))
                    elif re.match("^\[.*\]\s*$\s", element):
                        self.parse_bracket_square(element)
                        logging.debug("self.prb_activated: " + str(self.prb_activated))
                        logging.debug("self.prb_updated: " + str(self.prb_updated))
                        if self.prb_activated and self.prb_updated:
                            self.prb_activated = False
                            self.prb_updated = False
                            self.ack_probe()
                        elif self.abl_activated:
                            if self.prb_updated:
                                self.prb_updated = False
                                self.prb_num_done += 1
                                self.abl_val.append(self.prb_val)
                                self.prb_val = []
                                if self.prb_num_done == self.prb_num_todo:
                                    self.ack_auto_bed_levelling()
                                elif self.prb_num_done < self.prb_num_todo:
                                    logging.info(self.abl_cmd_ls[self.prb_num_done])
                                    self.serial_send_s.emit(self.abl_cmd_ls[self.prb_num_done])  # Execute next Probe of Auto-Bed-Levelling
                                else:
                                    logging.error("ABL: Number of probe done exceeded the number of probe to do.")
                        else:
                            logging.error("Wrong square bracket element: " + element)
                    elif re.match("ok\s*$\s", element):
                        pass
                    else:
                        self.update_console_text_s.emit(element)
            except BlockingIOError as e:
                logging.error(e, exc_info=True)
            except:
                logger.error("Uncaught exception: %s", traceback.format_exc())

    def execute_gcode_cmd(self, cmd_str):
        logging.debug(cmd_str)  # todo: debug to be removed?
        self.serial_send_s.emit(cmd_str)

    def cmd_probe(self, probe_z_max, probe_feed_rate):
        probe_cmd_s = ""
        probe_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # Set probe feed rate
        probe_cmd_s += "G38.2 Z" + str(probe_z_max) + "\n"  # Set probe command

        self.prb_val = []
        self.prb_updated = False
        self.prb_activated = True
        self.prb_num_todo = 1
        self.prb_reps_todo = 1
        logging.info(probe_cmd_s)
        self.serial_send_s.emit(probe_cmd_s)  # Execute probe

    def update_probe(self):
        self.prb_activated = False
        if self.prb_updated:
            self.prb_updated = False
            self.ack_probe()

    def ack_probe(self):
        logging.info("Probe: " + str(self.prb_val))
        self.update_probe_s.emit(self.prb_val)

    def cmd_auto_bed_levelling(self, xy_coord_list, travel_z, probe_z_max, probe_feed_rate):
        self.abl_cmd_ls = []
        abl_cmd_s = ""
        abl_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # Set probe feed rate

        self.prb_num_done = 0
        self.prb_num_todo = 0
        for coord in xy_coord_list:
            self.prb_num_todo += 1
            abl_cmd_s += "G00 Z" + str(travel_z) + " F100\n"  # Get to safety Z Travel
            abl_cmd_s += "G00 X" + str(coord[0]) + "Y" + str(coord[1]) + " F100\n"  # Go to XY coordinate
            abl_cmd_s += "G38.2 Z" + str(probe_z_max) + "\n"  # Set probe command
            abl_cmd_s += "G00 Z" + str(travel_z) + " F100\n"  # Get to safety Z Travel
            self.abl_cmd_ls.append(abl_cmd_s)
            abl_cmd_s = ""

        self.abl_cmd_ls[-1] += "G00 Z" + str(travel_z) + " F100\n"  # Get to safety Z Travel

        self.prb_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.abl_activated = True

        logging.info(self.abl_cmd_ls[0])
        self.serial_send_s.emit(self.abl_cmd_ls[0])  # Execute First Probe of Auto-Bed-Levelling

    def update_abl(self):
        if self.prb_updated:
            self.prb_updated = False
            self.prb_num_done += 1
            self.abl_val.append(self.prb_val)
            self.prb_val = []
            if self.prb_num_done == self.prb_num_todo:
                self.ack_auto_bed_levelling()
            elif self.prb_num_done < self.prb_num_todo:
                self.serial_send_s.emit(self.abl_cmd_ls[self.prb_num_done])  # Execute next Probe of ABL
            else:
                logging.error("ABL: Number of probe done exceeded the number of probe to do.")

    def ack_auto_bed_levelling(self):
        logging.info("ABL values: " + str(self.abl_val))
        self.update_abl_s.emit(self.abl_val)
