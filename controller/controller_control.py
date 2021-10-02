from PySide2.QtCore import QObject
import re
import logging
import traceback
import string
import random
import numpy as np
from collections import OrderedDict
from shape_core.gcode_manager import GCodeParser

logger = logging.getLogger(__name__)


class ControlController(QObject):
    STATUSPAT = re.compile(
        r"^<(\w*?),MPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),WPos:([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),?(.*)>$")
    POSPAT = re.compile(
        r"^\[(...):([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*),([+\-]?\d*\.\d*):?(\d*)\]$")
    TLOPAT = re.compile(r"^\[(...):([+\-]?\d*\.\d*)\]$")
    DOLLARPAT = re.compile(r"^\[G\d* .*\]$")
    SPLITPAT = re.compile(r"[:,]")
    VARPAT = re.compile(r"^\$(\d+)=(\d*\.?\d*) *\(?.*")

    def __init__(self, settings):
        super(ControlController, self).__init__()
        self.settings = settings

        self.status_l = []
        self.mpos_a = np.array([0, 0, 0])
        self.wpos_a = np.array([0, 0, 0])
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

        self.gcodes_od = OrderedDict({})

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
            # logging.warning("Not a probe, nor an ABL.")
            other_cmd_flag = True

        return [ack_prb_flag, ack_abl_flag, send_next, other_cmd_flag]

    def parse_bracket_angle(self, line):
        fields = line[1:-1].split("|")
        status = fields[0]
        wco_a = np.array([])

        for field in fields[1:]:
            word = self.SPLITPAT.split(field)
            if word[0] == "MPos":
                try:
                    self.mpos_a = np.array([float(word[1]), float(word[2]), float(word[3])])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except:
                    logger.error("Uncaught exception: %s", traceback.format_exc())
            elif word[0] == "WCO":
                try:
                    wco_a = np.array([float(word[1]), float(word[2]), float(word[3])])
                except (ValueError, IndexError) as e:
                    logging.error(e, exc_info=True)
                except:
                    logger.error("Uncaught exception: %s", traceback.format_exc())

        self.wpos_a = self.mpos_a + wco_a
        return [status, self.mpos_a, self.wpos_a]

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
        self.abl_val = []
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

    def get_gcode_tag_and_ov(self, gcode_path):
        ov = self.gcodes_od[gcode_path]["gcode"].get_gcode_original_vectors()
        tag = self.gcodes_od[gcode_path]["tag"]
        return tag, ov

    def get_gcode_gcp(self, gcode_path):
        return self.gcodes_od[gcode_path]["gcode"]

    def get_gcode_lines(self, gcode_path):
        return self.gcodes_od[gcode_path]["gcode"].recode_gcode()
