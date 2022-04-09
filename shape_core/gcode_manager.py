
import os
import re
import time
import numpy as np
from collections import OrderedDict as od
from datetime import datetime
import scipy.interpolate as spi
from shapely.geometry import LineString
from .macros_manager import Macros


class GCoder:
    """ This class could be the parent class
        which will then be used to diversify the
        gcode based on the controller that will have to interpret it
        of course this will be based on The Ant
        so it will natively support the grbl mod that
        we use as firmware. """

    DIGITS = 4
    STEPS = 3
    CHANGE_TOOL_COMMAND = "M6"

    def __init__(self, tag, machining_type='gerber', parent=None, units='ms'):

        self.parent = parent
        self.tag = tag

        self.mill = True

        # units:
        # ms -> metric system
        # is -> imperial system
        # todo: check the functionalities of unit conversion

        self.units = units
        self.macro = None

        self.geom_list = []
        if machining_type == 'gerber':
            self.cfg = {
                'cut': -0.07,
                'travel': 0.7,
                'xy_feedrate': 250.0,
                'z_feedrate': 40.0,
                'spindle': 1000.0
            }
        elif machining_type == 'profile':
            self.cfg = {
                'cut': -1.8,
                'travel': 0.7,
                'xy_feedrate': 250.0,
                'z_feedrate': 40.0,
                'spindle': 1000.0,
                'multi_depth': True,
                'depth_per_pass': 0.6
            }
        elif machining_type == 'pocketing':
            self.cfg = {
                'cut': -0.07,
                'travel': 0.7,
                'xy_feedrate': 250.0,
                'z_feedrate': 40.0,
                'spindle': 1000.0
            }
        elif machining_type == 'drill':
            self.cfg = {
                'cut': -2.1,
                'travel': 0.7,
                'xy_feedrate': 250.0,
                'z_feedrate': 40.0,
                'spindle': 1000.0
            }
        elif machining_type == 'commander':
            self.cfg = {
                'tool_probe_pos': (-1.0, -1.0, -11.0),
                'tool_probe_working': True,  # False: machine pos or True: working pos
                'tool_probe_min': -11.0,
                'tool_change_pos': (-41.2, -120.88, -1.0),
                'tool_probe_feedrate': (50.0, 80.0, 300.0) # SLOW FAST XY
            }
            self.macro = Macros(self.cfg, digits=self.DIGITS, parent=self)
        else:
            self.cfg = {}
        self.type = machining_type
        self.path = None
        self.gcode = []

    def load_cfg(self, cfg):
        self.cfg = cfg
        if self.macro is not None:
            self.macro.load_cfg(self.cfg)

    def format_float(self, f):
        ff = round(f, self.DIGITS)
        fs = "{:." + str(self.DIGITS) + "f}"
        f_str = fs.format(ff)
        return f_str

    def load_path(self, path):
        self.path = path

    def compute(self):
        if self.type == 'gerber':
            self.compute_gerber()
        elif self.type == 'profile':
            self.compute_pocketing()
        elif self.type == 'drill':
            self.compute_drill()
        elif self.type == 'pocketing':
            self.compute_pocketing()
        elif self.type == 'commander':
            print("Nothing to do!")
        else:
            print("Machining Type not supported")
            return False
        return True

    def compute_drill(self):
        # compute GCode from a drill path

        self.gcode = []
        self.create_header()
        self.add_job_info()
        self.add_init()

        self.go_travel()
        self.spindle_on(True)

        print("Compute Drill:")
        tool_change = -1
        for d in self.path:
            data = d[0]
            path = d[1]
            if data[1] == 'pocketing':
                print(" - Pocketing, bit diameter " + str(data[0]))
                self.insert_comment("Pocketing Section in Drill Procedure")
                self.insert_comment("Tool Diameter: " + str(data[0]))
                cut = self.cfg['cut']
                sign = cut / abs(cut)
                dpp = data[0]
                n = int(abs(cut) // dpp) + 1
                dpp = abs(cut)/n
                pass_list = [sign * dpp * x for x in range(1, n)] + [cut]
                pass_list.sort(reverse=True)
                self.compute_pocketing_paths(path, pass_list)
            else:
                print(" - Drilling, bit diameter " + str(data[0]))
                self.insert_comment("Drill Section in Drill Procedure")
                self.insert_comment("Tool Diameter: " + str(data[0]))
                self.compute_drill_paths(path, tool_change=tool_change)
            tool_change += 1

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

    def compute_gerber(self):
        # essentially it's about following the points indicated by the paths
        # joining them with fast movements.
        # the format of the gcode, the info contained and the file type
        # can be chosen in the settings

        self.gcode = []
        self.create_header()
        self.add_job_info()
        self.add_init()

        # todo: add user head and foot

        self.go_travel()
        self.spindle_on(True)

        # for each available path
        # reach the starting point
        # go into mill mode
        # follow the path and finally
        # return in travel mode

        for d in self.path:
            paths = d[1]
            self.compute_gerber_paths(paths)

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

    def compute_pocketing(self):
        # same concept of the milling method
        # in addition, in case there is a valid multipass cfg
        # execute the n necessary passes
        # the format of the gcode, the info contained and the file type
        # can be chosen in the settings

        self.gcode = []
        self.create_header()
        self.add_job_info()
        self.add_init()

        # todo: add user header and footer

        self.go_travel()
        self.spindle_on(True)

        # for each available path
        # reach the starting point
        # go into mill mode
        # follow the path and finally
        # return in travel mode

        multi_pass = False
        if self.cfg['multi_depth']:
            multi_pass = self.cfg['depth_per_pass'] > 0.0

        for d in self.path:
            paths = d[1]
            if multi_pass:
                cut = self.cfg['cut']
                sign = cut/abs(cut)
                dpp = self.cfg['depth_per_pass']
                n = int(abs(cut)//dpp)
                pass_list = [sign * dpp * x for x in range(1, n)] + [cut]
                pass_list.sort(reverse=True)
                self.compute_pocketing_paths(paths, pass_list)
            else:
                self.compute_gerber_paths(paths)

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

    def compute_drill_paths(self, paths, tool_change=-1):

        # set the working feed rate
        # of the Z axis
        zf = self.cfg['z_feedrate']
        zf_str = self.format_float(zf)
        self.gcode.append("G01 F" + zf_str + "\n")

        # insert tool change command if needed
        if tool_change >= 0:
            self.go_tool_change(tool_id=tool_change)

        for p in paths:
            cs = list(p.coords)
            for c in cs:
                self.go_to(c)
                self.make_drill()
                self.go_travel()

    def compute_gerber_paths(self, paths):
        for p in paths:
            cs = list(p.coords)
            self.go_to(cs.pop(0))
            self.go_mill()
            for c in cs:
                self.go_to(c)
            self.go_travel()

    def compute_pocketing_paths(self, paths, pass_list):
        for p in paths:
            rev = True
            orig_cs = list(p.coords)
            cs = orig_cs.copy()
            self.go_to(cs.pop(0))
            for cp in pass_list:
                self.go_mill(cp)
                for c in cs:
                    self.go_to(c)
                cs = orig_cs.copy()
                if rev:
                    cs.reverse()
                rev = not rev
            self.go_travel()

    def go_to(self, p):
        gc = ""
        x, y = p
        x_str = self.format_float(x)
        y_str = self.format_float(y)
        if self.mill:
            gc += "G01 X" + x_str + " Y" + y_str + "\n"
        else:
            gc += "G00 X" + x_str + " Y" + y_str + "\n"
        self.gcode.append(gc)

    def compute_tag(self, gc_str, wsp, probe_data, dro):
        replaced = gc_str
        if self.macro is not None:
            replaced = self.macro.compute_tag(gc_str, wsp, probe_data, dro)
        return replaced

    def go_tool_change(self, tool_id=0):
        gc = "T" + str(int(tool_id)) + "\n"
        gc += self.CHANGE_TOOL_COMMAND + "\n"
        self.gcode.append(gc)

    def make_drill(self):
        steps = self.STEPS
        gc = ""

        # drill the hole in n steps
        # drilling and returning to zero for
        # unload the tip

        z_zero_str = self.format_float(0.0)
        z_drill = self.cfg['cut']
        delta_z = z_drill/(steps * 1.0)
        z = 0.0

        for i in range(steps):
            z += delta_z
            zt_str = self.format_float(z)
            gc += "G01 Z" + zt_str + "\n"
            gc += "G00 Z" + z_zero_str + "\n"
        self.gcode.append(gc)

    def go_travel(self):
        zt = self.cfg['travel']
        zt_str = self.format_float(zt)
        self.gcode.append("G00 Z" + zt_str + "\n")
        self.mill = False

    def go_mill(self, z=None):
        gc = ""
        zf = self.cfg['z_feedrate']
        if z is None:
            zt = self.cfg['cut']
        else:
            zt = z
        zf_str = self.format_float(zf)
        gc += "G01 F" + zf_str + "\n"
        zt_str = self.format_float(zt)
        gc += "G01 Z" + zt_str + "\n"
        xyf = self.cfg['xy_feedrate']
        xyf_str = self.format_float(xyf)
        gc += "G01 F" + xyf_str + "\n"
        self.gcode.append(gc)
        self.mill = True

    def spindle_on(self, on=True):
        gc = ""
        if on:
            ten_str = self.format_float(10.0)
            gc += "M3 S" + ten_str + "\n"  # activate splindle
            one_str = self.format_float(1.0)
            gc += "G4 P" + one_str + "\n"  # just a little pause
            spindle_speed = self.cfg['spindle']
            spindle_speed_str = self.format_float(spindle_speed)
            gc += "M3 S" + spindle_speed_str + "\n"  # spindle at the full speed
            gc += "\n"
        else:
            zero_str = self.format_float(0.0)
            gc += "M3 S" + zero_str + "\n"  # set speed to 0
            one_str = self.format_float(1.0)
            gc += "G4 P" + one_str + "\n"  # just a little pause
            gc += "M5\n"  # just a little pause
            gc += "\n"
        self.gcode.append(gc)

    def add_init(self):
        gc = ""
        # units
        if self.units == 'ms':
            gc += "G21\n"
        else:
            gc += "G20\n"

        # absolute positioning
        gc += "G90\n"

        # plane section xy
        gc += "G17\n"

        # feed rate mode as units per minutes
        gc += "G94\n"

        gc += "\n"
        self.gcode.append(gc)

    def create_header(self):
        gc = self.gcode_comment("GCode generated by The Ant Controller")
        if self.parent is not None:
            cv = self.parent.get_core_version()
            gv = self.parent.get_gui_version()
            gc += self.gcode_comment("Core version: " + cv)
            gc += self.gcode_comment("GUI version: " + gv)
        fn = self.get_file_name()
        gc += "\n"
        gc += self.gcode_comment("File name: " + fn)
        gc += self.gcode_comment("Machining type: " + self.type.lower())
        gc += "\n"

        # date
        now = datetime.now()
        d = now.today().strftime('%A')
        D = now.today().strftime("%d %B, %Y at %H:%M:%S")

        gc += self.gcode_comment("Create on " + d + ", " + D)
        gc += "\n"

        self.gcode.append(gc)

    def add_job_info(self):
        gc = self.gcode_comment("Job Info:")
        for k in self.cfg.keys():
            gc += self.gcode_comment(k + ": " + str(self.cfg[k]))
        gc += "\n"
        self.gcode.append(gc)

    def gcode_comment(self, txt):
        c = ""
        lines = txt.split('\n')
        for l in lines:
            c += "(" + l + ")\n"
        return c

    def insert_comment(self, txt):
        self.gcode.append(self.gcode_comment(txt))

    def get_autobed_leveling_code(self, xy_c_l, travel_z, probe_z_min, probe_feed_rate):
        # todo: change this part using methods to create the GCode
        abl_cmd_ls = []
        abl_cmd_s = ""
        abl_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # set probe feed rate

        prb_num_todo = 0
        for coord in xy_c_l:
            prb_num_todo += 1
            abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # get to safety Z Travel
            abl_cmd_s += "G00 X" + str(coord[0]) + "Y" + str(coord[1]) + "\n"  # go to XY coordinate
            abl_cmd_s += "G38.2 Z" + str(probe_z_min) + "F" + str(probe_feed_rate) + "\n"  # set probe command
            abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # get to safety Z Travel
            abl_cmd_ls.append(abl_cmd_s)
            abl_cmd_s = ""

        abl_cmd_s = ""
        abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # get to safety Z Travel
        abl_cmd_s += "G00 X" + str((xy_c_l[0][0] + xy_c_l[-1][0]) / 2.0) + "Y" + \
                          str((xy_c_l[0][1] + xy_c_l[-1][1]) / 2.0) + "\n"
        abl_cmd_s += "G38.2 Z" + str(probe_z_min) + "F" + str(probe_feed_rate) + "\n"  # set probe command
        prb_num_todo += 1
        abl_cmd_s += "G10 P1 L20 Z0\n"  # set Z zero
        abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # get to safety Z Travel
        abl_cmd_s += "G00 X" + str(xy_c_l[0][0]) + "Y" + str(xy_c_l[0][1]) + "\n"  # go 1st XY coordinate
        abl_cmd_ls.append(abl_cmd_s)

        return abl_cmd_ls, prb_num_todo

    def get_macro_code(self, macro_type="M6", to_comment=""):
        print("Get Macro Code")
        print(macro_type)
        s = ""
        if to_comment != "":
            s += self.gcode_comment(to_comment)
        if self.macro is not None:
            s += self.macro.get_macro_string(macro_type)
        return s

    def get_file_name(self):
        return self.tag.lower() + "_" + self.type.lower() + ".gcode"

    def write(self, file_path):
        print("Writing gcode file:")
        print("\t " + str(os.path.abspath(file_path)))
        with open(file_path, 'w') as f:
            f.write("".join(self.gcode))
        print("Done")

    # macro section

    def is_macro(self, cmd):
        print("Is Macro")
        print(cmd)
        if self.macro is not None:
            return self.macro.is_macro(cmd)
        else:
            return False


class GCodeMacro:

    def __init__(self, freezed_dro, macro_type="M6", gcr=None):
        self.id = 0
        self.freezed_dro = freezed_dro
        if gcr is None:
            self.gcc = GCoder("dummy", machining_type="commander")
        else:
            self.gcc = gcr
        self.macro_lines = self.gcc.get_macro_code(macro_type).split("\n")

    def get_next_line(self, wsp, probe_data):
        if self.id < len(self.macro_lines):
            line = self.macro_lines[self.id] + "\n"
            parsered_line = self.gcc.compute_tag(line, wsp, probe_data, self.freezed_dro)
            self.id += 1
            return parsered_line
        else:
            return None


class GcodeLine:
    def __init__(self):
        self.command = []
        self.params = od({})
        self.comment = ""
        self.tag = False

    def get_string(self):
        s = ""
        if self.command:
            sep = ""
            for cmd in self.command:
                s += sep
                s += cmd[0]
                s += ".".join([str(x) for x in cmd[1]])
                sep = " "

        if self.params:
            for k in self.params.keys():
                s += " " + k + str(self.params[k])
        s = s.upper()
        if self.comment:
            s += " ;" + self.comment
        s += "\n"
        return s

    def __repr__(self):
        s = "GcodeLine (\n"
        s += " command = " + str(self.command) + "\n"
        t = []
        for k in self.params:
            t.append(str(k) + ": " + str(self.params[k]))
        s += " params  = {" + ", ".join(t) + "}\n"
        s += " comment = " + str(self.comment) + "\n"
        s += ")\n"
        return s


class GcodePoint:

    TRAVEL = "t"
    WORKING = "w"
    WORKING_POS = "wp"
    MACHINE_POS = "mp"

    def __init__(self):
        self.coords = np.zeros((3,))
        self.line = -1
        self.sub_line = 0
        self.type = self.WORKING  # w working t travel
        self.pos = self.WORKING_POS  # wp working mp machine
        self.params = od({})

    def __repr__(self):
        s = "GcodeVector (\n"
        s += " coords = " + str(self.coords) + "," + "\n"
        s += " type  = " + str("working" if self.type == self.WORKING else "travel") + "\n"
        s += " line  = " + str(self.line) + "\n"
        if self.sub_line > 0:
            s += " sub_line  = " + str(self.sub_line) + "\n"
        if self.params.keys():
            s += " params = "
            pl = []
            for k in self.params.keys():
                pl.append(str(k) + ":" + str(self.params[k]))
            s += ", ".join(pl) + "\n"
        s += ")\n"
        return s

    def copy(self):
        cnp = GcodePoint()
        cnp.coords = self.coords.copy()
        cnp.line = self.line
        cnp.sub_line = self.sub_line
        cnp.type = self.type
        cnp.pos = self.pos
        cnp.params = self.params.copy()
        return cnp

    def get_string(self):
        s = ""
        if self.pos == self.MACHINE_POS:
            s += "G53 "

        if self.type == self.TRAVEL:
            s += "G0"
        else:
            s += "G1"
        s += " X" + "{:.3f}".format(self.coords[0])
        s += " Y" + "{:.3f}".format(self.coords[1])
        if len(self.coords) > 2:
            s += " Z" + "{:.3f}".format(self.coords[2])
        for k in self.params.keys():
            s += " " + str(k).upper() + str(self.params[k])
        s += "\n"
        return s


class GCode:

    def __init__(self, lines):
        self.original_lines = lines
        self.modified_lines = []
        self.gcll = []
        self.original_vectors = []
        self.modified_vectors = []
        self.bb = None


class GCodeParser:

    COORD_TAG = ['x', 'y', 'z']
    PARAM_TAG = ['f', 'p']
    CHANGE_TOOL_COMMAND = ('m', 6)
    MACHINE_POS_COMMAND = ('g', 53)

    def __init__(self, cfg):
        self.gcode_path = ""
        self.cfg = cfg
        self.gc = None

    def load_gcode_file(self, gcode_path):
        print("GCoder Loading GCode File:")
        print(gcode_path)
        if os.path.isfile(gcode_path):
            self.gcode_path = gcode_path
            with open(self.gcode_path) as f:
                lines = f.readlines()
                if lines:
                    # GCode file loaded
                    self.gc = GCode(lines)
        else:
            print("Invalid GCode File Path")

    def interp(self, single_line=None):
        gcll = []
        if self.gc is not None or single_line is not None:
            if single_line is not None:
                ls = [single_line]
            else:
                if self.gc.modified_lines:
                    ls = self.gc.modified_lines
                else:
                    ls = self.gc.original_lines
            for l in ls:
                d = l.strip()
                d = d.replace("(", ";")
                d = d.replace(")", "")
                d += ";"
                tmp = d.split(";")
                data, comment = tmp[0:2]
                if data or comment:
                    gcl = GcodeLine()
                    # store the comment if needed
                    gcl.comment = comment.strip()
                    # decode the commands
                    if data:
                        data = data.lower()
                        if "$#" in data:
                            gcl.command = [("$#", tuple())]
                        else:
                            splitted = re.findall(r'[a-z][-]*[\d.]+', data)

                            # detect tags (remember, tags cannot be used in motion commands)
                            tags = re.findall(r'[a-z][@]*[a-z_]+[@]*', data)

                            cmd = splitted.pop(0)
                            ct = cmd[0]
                            cd = [int(x) for x in cmd[1::].split(".")]
                            gcl.command = [(ct, tuple(cd))]

                            if splitted:
                                if splitted[0].upper().startswith("G"):
                                    # second command
                                    cmd = splitted.pop(0)
                                    ct = cmd[0]
                                    cd = [int(x) for x in cmd[1::].split(".")]
                                    gcl.command += [(ct, tuple(cd))]

                            par = splitted
                            params = od({})
                            for p in par:
                                params[p[0]] = float(p[1::])
                            for t in tags:
                                params[t[0]] = t[1::]
                                gcl.tag = True
                            gcl.params = params
                    gcll.append(gcl)
            if single_line is None:
                self.gc.gcll = gcll
        return gcll

    def recode_gcode(self):
        # Recode Gcode
        gcls = []
        if self.gc.modified_vectors:
            # - Modified Loaded
            gcv = self.gc.modified_vectors
        else:
            # - Original Loaded
            gcv = self.gc.original_vectors
        gcl = self.gc.gcll
        if gcv or gcl:
            gcv_len = len(gcv)
            # start from one because the first initial point
            # is always in origin of the working coords system
            vi = 1
            for l in range(len(gcl)):
                if vi < len(gcv):
                    nl = gcv[vi].line
                else:
                    nl = -1
                if nl == l:
                    cl_flag = True
                    gcls.append(gcv[vi].get_string())
                    while cl_flag and vi < gcv_len - 1:
                        vi += 1
                        cl_flag = gcv[vi].line == l
                        if cl_flag:
                            gcls.append(gcv[vi].get_string())
                else:
                    if gcl[l].command:
                        gcls.append(gcl[l].get_string())
        return gcls

    def get_change_tool_gcode(self):
        ctc = self.CHANGE_TOOL_COMMAND
        ctc_str = ctc[0].upper() + str(ctc[1]) + "\n"
        return ["T0\n", ctc_str]

    def vectorize(self):
        if self.gc.gcll:
            p0 = GcodePoint()
            last_coord = p0.coords.copy()
            vl = [p0]
            bb_max = [-1e6, -1e6, -1e6]
            bb_min = [1e6, 1e6, 1e6]
            for i, gcl in enumerate(self.gc.gcll):
                if gcl.command:
                    first_cmd = gcl.command[0]
                    last_cmd = gcl.command[-1]

                    # check for position command
                    machine_pos = False
                    if first_cmd != last_cmd:
                        if first_cmd[0] == self.MACHINE_POS_COMMAND[0] and self.MACHINE_POS_COMMAND[1] in first_cmd[1]:
                            machine_pos = True

                    cn = last_cmd[0]
                    if len(last_cmd[1]) > 0:
                        ci = last_cmd[1][0]
                    else:
                        ci = -1
                    if cn == 'g' and ci < 2 and not machine_pos and not gcl.tag:
                        # it is a valid position command in working position system
                        # let's vectorize it
                        a = set(gcl.params.keys())
                        b = set(self.COORD_TAG)
                        c = b.intersection(a)
                        d = set(self.PARAM_TAG)
                        f = a.intersection(d)
                        if c:
                            for e in c:
                                last_coord[self.COORD_TAG.index(e)] = gcl.params[e]
                                bb_max[self.COORD_TAG.index(e)] = max(bb_max[self.COORD_TAG.index(e)], gcl.params[e])
                                bb_min[self.COORD_TAG.index(e)] = min(bb_min[self.COORD_TAG.index(e)], gcl.params[e])
                            p = last_coord.copy()
                            px = GcodePoint()
                            px.coords = p
                            px.type = px.TRAVEL if ci == 0 else px.WORKING
                            px.pos = px.MACHINE_POS if machine_pos else px.WORKING_POS
                            px.line = i
                            if f:
                                for g in f:
                                    px.params[g] = gcl.params[g]
                            vl.append(px)

            if len(vl) > 1:
                self.gc.original_vectors = vl
                self.gc.bb = tuple(bb_min + bb_max)

    def get_gcode(self):
        return self.gc

    def get_gcode_original_vectors(self):
        return self.gc.original_vectors

    def get_gcode_vectors(self):
        if self.gc.modified_vectors:
            return self.gc.modified_vectors
        else:
            return self.gc.original_vectors

    def get_bbox(self):
        return self.gc.bb


class GCodeLeveler:

    def __init__(self, gc, grid_data=None):
        self.gc = gc
        if grid_data is not None:
            self.grid_data = grid_data
        else:
            self.grid_data = self.get_dummy_grid_data()
        self.grid_lines, self.grid_step = self.get_grid_lines()
        self.ig = None

    def get_grid_lines(self):
        x = list(set(self.grid_data[0].ravel().tolist()))
        x.sort()
        y = list(set(self.grid_data[1].ravel().tolist()))
        y.sort()
        x_step = abs(x[1] - x[0])
        y_step = abs(y[1] - y[0])
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        vectors = []
        for yc in y:
            vectors.append(LineString(((x_min, yc), (x_max, yc))))
        for xc in x:
            vectors.append(LineString(((xc, y_min), (xc, y_max))))
        return vectors, (x_step, y_step)

    def get_dummy_grid_data(self):
        grid_steps = 10
        if self.gc is not None:
            bb = self.gc.bb
            if bb is not None:
                x_min = bb[0]
                y_min = bb[1]
                delta_x = bb[3]-bb[0]
                delta_y = bb[4]-bb[1]
                delta_i = np.sqrt(delta_x*delta_x + delta_y*delta_y)
                delta_z = 0.2
                delta_z0 = -0.1
                xi = np.linspace(0.0, delta_x, grid_steps)
                yi = np.linspace(0.0, delta_y, grid_steps)
                X, Y = np.meshgrid(xi, yi)
                Z = np.sqrt(np.square(X) + np.square(Y))/delta_i * delta_z + delta_z0
                X += x_min
                Y += y_min
                return X, Y, Z

    def get_grid_data(self, probe_results, steps, last_probe, wco_offset=(0, 0, 0)):
        x, y, z = zip(*probe_results)
        X = np.array(x).reshape(steps[0], steps[1]) - wco_offset[0]
        Y = np.array(y).reshape(steps[0], steps[1]) - wco_offset[1]
        Z = np.array(z).reshape(steps[0], steps[1]) - last_probe[2]
        return X, Y, Z

    def interp_grid_data(self):
        if self.grid_data is not None:
            X, Y, Z = self.grid_data
            self.ig = spi.interp2d(X, Y, Z, kind='cubic')

    def apply(self):
        print("Auto Bed Leveler Start")
        if self.gc is not None and self.ig is not None:
            mvl = []
            for p in self.gc.original_vectors:
                cnp = p.copy()
                delta = self.ig(cnp.coords[0], cnp.coords[1])
                cnp.coords[2] += delta
                mvl.append(cnp)
        print("Auto Bed Leveler Stop")

    def apply_abl(self):
        # this routine puts in place strategies to fit the whole
        # GCode to the surface defined by the ABL
        # analyzing the segments of the gcode and not just its points.
        # following the trend of surface of ABL under each segment,
        # in case it has not a linear trend, the segment is divided
        # into sub-segments in which the ABL variation can be considered linear.

        if self.gc is not None and self.ig is not None:
            ta = time.time()
            print("Advanced Auto Bed Leveler Start")
            mvl = []
            pre_pc = None
            min_step = min(self.grid_step)
            print("Min Step ", min_step)
            for p in self.gc.original_vectors:
                np_l = []
                nwp = p.copy()
                delta = self.ig(nwp.coords[0], nwp.coords[1])
                nwp.coords[2] += delta
                if pre_pc is not None:
                    pc = np.array(nwp.coords[:2])
                    seg_len = np.linalg.norm(pc - pre_pc)
                    sub_line = 0
                    if seg_len <= min_step and seg_len > 0.1:
                        i_l = self.get_grid_intersection(pc, pre_pc)
                        if i_l:
                            for i in i_l:
                                x = i.xy[0][0]
                                y = i.xy[1][0]
                                # if intersection differ from segment vertex
                                if (x != pc[0] and y != pc[1]) or (x != pre_pc[0] and y != pre_pc[1]):
                                    nip = nwp.copy()
                                    nip.coords[0] = x
                                    nip.coords[1] = y
                                    delta = self.ig(nip.coords[0], nip.coords[1])
                                    nip.coords[2] += delta
                                    nip.sub_line = sub_line
                                    np_l.append(nip)
                                    sub_line += 1
                    nwp.sub_line = sub_line
                    np_l.append(nwp)
                else:
                    np_l = [nwp]
                mvl += np_l
                pre_pc = np.array(p.coords[:2])
            self.gc.modified_vectors = mvl
            print("Advanced Auto Bed Leveler Stop")
            tb = time.time()
            print("Done in " + "{:.3f}".format(tb-ta) + " sec")
            return True
        else:
            return False

    def get_grid_intersection(self, a1, a2):
        i_l = []
        line1 = LineString([a1, a2])
        for s in self.grid_lines:
            line2 = s
            i = line1.intersection(line2)
            if i:
                i_l.append(i)
        return i_l


if __name__ == "__main__":

    gcode_path = "C:\\Users\\Mattia\\Documents\\PythonPrj\\TheAntLord\\gcode_tmp\\top_gerber.gcode"
    cfg = {}

    gcp = GCodeParser(cfg)
    gcp.load_gcode_file(gcode_path)
    gcp.interp()
    gcp.vectorize()
    lines = gcp.recode_gcode()

    #abl = GCodeLeveler(gcp.gc)
    #abl.get_dummy_grid_data()
    #abl.interp_grid_data()
    #abl.apply_abl()
