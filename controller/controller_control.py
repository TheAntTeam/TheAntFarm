from PySide2.QtCore import QObject
import re
import logging
import traceback
import string
import random
import numpy as np
from collections import OrderedDict, deque
from shape_core.gcode_manager import GCoder, GCodeParser, GCodeLeveler

logger = logging.getLogger(__name__)


class ControlController(QObject):
    STATUSPAT = re.compile(
        r"^<(\w*?),MPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),"
        r"([+\-]?\d*\.\d*),WPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),"
        r"([+\-]?\d*\.\d*),?(.*)>$")
    POSPAT = re.compile(
        r"^\[(...):([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),"
        r"([+\-]?\d*\.\d*):?(\d*)\]$")
    TLOPAT = re.compile(r"^\[(...):([+\-]?\d*\.\d*)\]$")
    DOLLARPAT = re.compile(r"^\[G\d* .*\]$")
    SPLITPAT = re.compile(r"[:,]")
    VARPAT = re.compile(r"^\$(\d+)=(\d*\.?\d*) *\(?.*")

    def __init__(self, settings):
        super(ControlController, self).__init__()
        self.settings = settings

        self.status = []
        self.mpos_a = np.array([0, 0, 0])
        self.wco_a = np.array([0, 0, 0])
        self.wpos_a = np.array([0, 0, 0])
        self.dro_status_updated = False
        self.prb_activated = False
        self.abl_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.prb_val = deque([[-1.0, -1.0, -1.0], [-1.0, -1.0, -1.0]], maxlen=2)
        self.abl_val = []
        self.abl_steps = ()
        self.abl_cmd_ls = []
        self.prb_num_todo = 0
        self.prb_num_done = 0
        self.prb_reps_todo = 1
        self.prb_reps_done = 0

        self.status_report_od = OrderedDict({})
        self.workspace_params_od = OrderedDict({})

        self.gcodes_od = OrderedDict({})

    def get_probe_value(self):
        return self.prb_val[0]

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
            # logging.warning("Not a probe, nor an ABL.")
            other_cmd_flag = True

        return [ack_prb_flag, ack_abl_flag, send_next, other_cmd_flag]

    def parse_bracket_angle(self, line):
        line_stripped = line.strip()
        fields = line_stripped[1:-1].split("|")
        self.status = fields[0]
        self.status_report_od["state"] = fields[0]

        for field in fields[1:]:
            word = self.SPLITPAT.split(field.strip())
            if word[0] == "MPos":
                try:
                    self.mpos_a = np.array([float(word[1]), float(word[2]), float(word[3])])
                    self.status_report_od["mpos"] = np.array([float(word[1]), float(word[2]), float(word[3])])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "F":
                try:
                    self.status_report_od["curfeed"] = float(word[1])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "FS":
                try:
                    self.status_report_od["curfeed"] = float(word[1])
                    self.status_report_od["curspindle"] = float(word[2])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "Bf":
                try:
                    self.status_report_od["planner"] = int(word[1])
                    self.status_report_od["rxbytes"] = int(word[2])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "Ov":
                try:
                    self.status_report_od["OvFeed"] = int(word[1])
                    self.status_report_od["OvRapid"] = int(word[2])
                    self.status_report_od["OvSpindle"] = int(word[3])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "WCO":
                try:
                    self.wco_a = np.array([float(word[1]), float(word[2]), float(word[3])])
                    self.status_report_od["wco"] = np.array([float(word[1]), float(word[2]), float(word[3])])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "Pn":
                try:
                    self.status_report_od["pins"] = word[1]
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except Exception as e:
                    logger.error("Uncaught exception: %s", traceback.format_exc())

        self.wpos_a = self.mpos_a - self.wco_a
        self.status_report_od["wpos"] = self.wpos_a
        return [self.status, self.mpos_a, self.wpos_a]

    def parse_bracket_square(self, line):
        word = self.SPLITPAT.split(line.rstrip()[1:-1])

        if word[0] == "PRB":
            try:
                self.prb_val.appendleft([float(word[1]), float(word[2]), float(word[3])])
                self.prb_updated = True
            except (ValueError, IndexError) as e:
                logging.error(e, exc_info=True)
            except Exception as e:
                logger.error("Uncaught exception: %s", traceback.format_exc())
        elif word[0] == "G54":
            self.workspace_params_od["G54"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G55":
            self.workspace_params_od["G55"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G56":
            self.workspace_params_od["G56"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G57":
            self.workspace_params_od["G57"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G58":
            self.workspace_params_od["G58"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G59":
            self.workspace_params_od["G59"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G28":
            self.workspace_params_od["G28"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G30":
            self.workspace_params_od["G30"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "G92":
            self.workspace_params_od["G92"] = np.array([float(word[1]), float(word[2]), float(word[3])])
        elif word[0] == "TLO":
            self.workspace_params_od["TLO"] = float(word[1])

        return self.prb_val[0]

    def cmd_probe(self, probe_z_max, probe_feed_rate):
        probe_cmd_s = ""
        probe_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # Set probe feed rate
        probe_cmd_s += "G38.2 Z" + str(probe_z_max) + "\n"  # Set probe command

        self.prb_updated = False
        self.prb_activated = True
        self.prb_num_todo = 1
        self.prb_reps_todo = 1

        return probe_cmd_s

    def cmd_auto_bed_levelling(self, bbox_t, steps_t):
        xy_coord_list = self.get_grid_coords(bbox_t, steps_t)
        travel_z = bbox_t[5]
        probe_z_max = bbox_t[2]
        probe_feed_rate = 30
        logger.debug(xy_coord_list)

        [self.abl_cmd_ls, self.prb_num_todo] = self.make_cmd_auto_bed_levelling(xy_coord_list, travel_z,
                                                                                probe_z_max, probe_feed_rate)
        self.abl_val = []
        self.abl_steps = (steps_t[0], steps_t[1])
        self.prb_num_done = 0
        self.prb_activated = False
        self.prb_updated = False
        self.abl_updated = False
        self.abl_activated = True

        return [self.abl_cmd_ls, self.prb_num_todo]

    @staticmethod
    def get_grid_coords(bbox_t, steps_t):
        xmin = bbox_t[0]
        ymin = bbox_t[1]
        xmax = bbox_t[3]
        ymax = bbox_t[4]
        x_step = steps_t[0]  # + 1
        y_step = steps_t[1]  # + 1
        xc = np.linspace(xmin, xmax, x_step)
        yc = np.linspace(ymin, ymax, y_step)
        xi, yi = np.meshgrid(xc, yc)
        return list(zip(xi.ravel().tolist(), yi.ravel().tolist()))

    @staticmethod
    def make_cmd_auto_bed_levelling(xy_c_l, travel_z, probe_z_max, probe_feed_rate):

        gcr = GCoder("dummy", "commander")
        abl_cmd_ls, prb_num_todo = gcr.get_autobed_leveling_code(xy_c_l, travel_z, probe_z_max, probe_feed_rate)

        logger.debug("ABL routine: " + str(abl_cmd_ls))
        logger.debug("ABL points to do: " + str(prb_num_todo))

        return [abl_cmd_ls, prb_num_todo]

    def update_abl(self):
        ack_flag = False
        send_next = False
        if self.prb_updated:
            self.prb_updated = False
            self.prb_num_done += 1
            self.abl_val.append(self.prb_val[0])
            # self.prb_val = []  # doesn't need anymore
            if self.prb_num_done == self.prb_num_todo:
                ack_flag = True
                self.abl_activated = False
            elif self.prb_num_done < self.prb_num_todo:
                send_next = True
            else:
                logging.error("ABL: Number of probe done exceeded the number of probe to do.")

        return [ack_flag, send_next]

    # GCode Related
    @staticmethod
    def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_new_tag(self):
        tag_l = [self.gcodes_od[k]["tag"] for k in self.gcodes_od.keys()]
        new_tag = self.id_generator(4)
        while new_tag in tag_l:
            new_tag = self.id_generator(4)
        return new_tag

    def load_gcode_file(self, cfg, gcode_path):
        gcp = GCodeParser(cfg)
        gcp.load_gcode_file(gcode_path)
        gcp.interp()
        gcp.vectorize()
        # ov = gcp.get_gcode_original_vectors()
        tag = self.get_new_tag()
        if gcp is not None:
            self.gcodes_od[gcode_path] = {"gcode": gcp, "tag": tag}

    def get_gcode_tag_and_v(self, gcode_path):
        v = self.gcodes_od[gcode_path]["gcode"].get_gcode_vectors()
        tag = self.gcodes_od[gcode_path]["tag"]
        return tag, v

    def apply_abl(self, gcode_path):
        print("Apply ABL")
        gcp = self.get_gcode_gcp(gcode_path)
        abl = GCodeLeveler(gcp.gc)
        abl_val = self.abl_val.copy()
        last_probe = abl_val.pop()
        abl.get_grid_data(abl_val, self.abl_steps, last_probe, self.wco_a)
        abl.interp_grid_data()
        abl.apply_abl()
        # print("Leveled")
        # print(gcp.gc.modified_vectors)

    def remove_abl(self, gcode_path):
        print("Remove ABL")
        gcp = self.get_gcode_gcp(gcode_path)
        if gcp.gc.modified_vectors:
            gcp.gc.modified_vectors = []
            return True
        else:
            return False

    def get_gcode_gcp(self, gcode_path):
        return self.gcodes_od[gcode_path]["gcode"]

    def get_gcode_lines(self, gcode_path):
        return self.gcodes_od[gcode_path]["gcode"].recode_gcode()

    def get_change_tool_lines(self):
        gcp = GCodeParser(None)
        return gcp.get_change_tool_gcode()

    def get_boundary_box(self, gcode_path):
        logger.debug(gcode_path)
        return self.gcodes_od[gcode_path]["gcode"].get_bbox()
