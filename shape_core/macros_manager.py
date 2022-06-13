
import os
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class Macros:

    TAG = '@'
    TAGS = {
        "tlo": "TLO",
        "position": "POSITION"
    }
    AXIS = ("X", "Y", "Z")

    def __init__(self, parent=None):

        self.parent = parent

        self.cfg = None
        self.load_cfg()

        self.macros_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../macros"))

        self.macros_dict = {
            "M6": "tool_change_wcs.gcode"
        }

        self.tags = [
            "PROBE_FEED_FAST",
            "PROBE_FEED_SLOW",
            "PROBE_TYPE_POS",
            "PROBE_POS_X",
            "PROBE_POS_Y",
            "PROBE_POS_Z",
            "PROBE_POS_MIN",
            "PROBE_VALUE_PREX",
            "PROBE_VALUE_PREY",
            "PROBE_VALUE_PREZ",
            "PROBE_VALUE_ACTX",
            "PROBE_VALUE_ACTY",
            "PROBE_VALUE_ACTZ",
            "CHANGE_POS_X",
            "CHANGE_POS_Y",
            "CHANGE_POS_Z",
            "SAFE_POS_Z",
            "PRE_POS_X"
            "PRE_POS_Y",
            "PRE_POS_Z",
            "TLO_TYPE_A",
        ]

    def load_cfg(self, cfg=None):
        if cfg is not None:
            self.cfg = cfg
        else:
            self.cfg = {
                'tool_probe_pos': (-1.0, -1.0, -11.0),
                'tool_probe_working': True,  # False: machine pos or True: working pos
                'tool_probe_min': -11.0,
                'tool_change_pos': (-41.2, -120.88, -1.0),
                'tool_probe_feedrate': (300.0, 80.0, 50.0),
                'tool_probe_hold': False,
                'tool_probe_zero': False,
            }
        self.cfg["safe_pos"] = (-1.0, -1.0, -1.0)
        # print("Macros CFG")
        # print(self.cfg)

    def is_macro(self, cmd):
        # splitted = re.findall(r'[a-zA-Z][-]*[\d.]+', cmd.strip().upper())
        # if self.CHANGE_TOOL_COMMAND in splitted:
        #    return True
        print("Is Macro New: " + str(cmd))
        macros_list = list(self.macros_dict.keys())
        print(cmd.strip().upper() in macros_list)
        return cmd.strip().upper() in macros_list

    def get_macro_string(self, macro):
        lines = []
        if self.is_macro(macro):
            macro_path = os.path.join(self.macros_path, self.macros_dict[macro])
            if os.path.isfile(macro_path):
                with open(macro_path) as f:
                    lines = f.readlines()
            else:
                logger.error("Macro File: " + str(macro_path) + " not found")
        else:
            logger.error("Command: " + str(macro) + " isn't a valid macro command")
        lines = "".join(lines)
        print(lines)
        return lines

    def compute_tag(self, gc_str, wsp, probe_data, dro):
        splitted_str = gc_str.strip().split(self.TAG)
        replaces_l = splitted_str.copy()
        tags_family = self.get_tags_family()
        for i, tag in enumerate(splitted_str):
            stag = tag.upper().split("_")
            head = stag[0]
            if head == "PROBE":
                replaces_l[i] = self.compute_probe_tag(stag, dro, probe_data)
            elif head == "CHANGE":
                replaces_l[i] = self.compute_change_tag(stag)
            elif head == "SAFE":
                replaces_l[i] = self.compute_safe_tag(stag)
            elif head == "TLO":
                replaces_l[i] = self.compute_tlo_tag(stag, wsp, probe_data)
            elif head == "PRE":
                replaces_l[i] = self.compute_pre_tag(stag, dro)
        replaced = "".join(replaces_l) + "\n"
        if gc_str != "\n":
            print("--------------------")
            print(gc_str.strip())
            print(replaced.strip())
        return replaced

    def get_tags_family(self):
        splitted_tags = [x.split("_") for x in self.tags]
        return list(set([x[0] for x in splitted_tags]))

    def format_float(self, f):
        return self.parent.format_float(f)

    def check_tag_in_string(self, gc_str):
        return self.TAG in str(gc_str)

    def compute_probe_tag(self, stag, dro, probe_data):
        tag_type = stag[1]
        tag_str = ""
        if tag_type == "POS":
            ax = stag[2]
            if ax != "MIN":
                pos = self.cfg["tool_probe_pos"][self.AXIS.index(ax)]
            else:
                pos = self.cfg["tool_probe_min"]
            tag_str = self.format_float(pos)
        elif tag_type == "VALUE":
            ax = stag[2][-1]
            ax_type = stag[2][0:3]
            wpo = dro["WPO"]
            mpo = dro["MPO"]
            delta = mpo - wpo
            if ax_type == "PRE":
                prev = probe_data[1][self.AXIS.index(ax)]
                ax_delta = delta[self.AXIS.index(ax)]
                tag_str = self.format_float(prev - ax_delta)
            elif ax_type == "ACT":
                last = probe_data[0][self.AXIS.index(ax)]
                ax_delta = delta[self.AXIS.index(ax)]
                tag_str = self.format_float(last - ax_delta)
            else:
                logger.error("INVALID MACRO TAG: " + str("_".join(stag)))
        elif tag_type == "TYPE":
            if stag[2] == "POS":
                tag_str = "G54" if self.cfg["tool_probe_working"] else "G53"
        elif tag_type == "FEED":
            if stag[2] == "SLOW":
                tag_str = self.format_float(self.cfg["tool_probe_feedrate"][2])
            elif stag[2] == "FAST":
                tag_str = self.format_float(self.cfg["tool_probe_feedrate"][1])
            elif stag[2] == "XY":
                tag_str = self.format_float(self.cfg["tool_probe_feedrate"][0])
        elif tag_type == "HOLD":
            if self.cfg["tool_probe_hold"]:
                tag_str = "M0"
            else:
                tag_str = "(NO HOLD)"
        return tag_str

    def compute_change_tag(self, stag):
        tag_type = stag[1]
        tag_str = ""
        if tag_type == "POS":
            ax = stag[2]
            pos = self.cfg["tool_change_pos"][self.AXIS.index(ax)]
            tag_str = self.format_float(pos)
        elif tag_type == "TYPE":
            if stag[2] == "POS":
                tag_str = "G54" if self.cfg["tool_change_working"] else "G53"
        elif tag_type == "FEED":
            if stag[2] == "SLOW":
                tag_str = self.format_float(self.cfg["tool_change_feedrate"][0])
            elif stag[2] == "FAST":
                tag_str = self.format_float(self.cfg["tool_change_feedrate"][1])
        return tag_str

    def compute_safe_tag(self, stag):
        tag_type = stag[1]
        tag_str = ""
        if tag_type == "POS":
            ax = stag[2]
            pos = self.cfg["safe_pos"][self.AXIS.index(ax)]
            tag_str = self.format_float(pos)
        return tag_str

    def compute_tlo_tag(self, stag, wsp, probe_data):
        tag_type = stag[1]
        tag_str = ""
        if tag_type == "TYPE":
            id = stag[2]
            tag_str = ""
            last = probe_data[0][2]
            prev = probe_data[1][2]
            difference = last - prev
            if id == "N":
                # replace TLO
                tag_str = self.format_float(difference)
            if id == "A":
                # add to actual TLO
                tag_str = self.format_float(wsp["TLO"] + difference)
        return tag_str

    def compute_pre_tag(self, stag, dro):
        tag_type = stag[1]
        tag_str = ""
        if tag_type == "POS":
            ax = stag[2]
            wpo = dro["WPO"]
            tag_str = self.format_float(wpo[self.AXIS.index(ax)])
        return tag_str
