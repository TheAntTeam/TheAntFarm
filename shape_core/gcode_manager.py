
import os
import re
import time
import numpy as np
from collections import OrderedDict as od
from datetime import datetime
#import matplotlib.pyplot as plt
import scipy.interpolate as spi
from shapely.geometry import LineString


class GCoder:
    # questa classe potrebbe essere la classe principale
    # che poi verra' utilizzata per diversificare i
    # gcode in base al controller che dovra' interpretarlo
    # naturalmente questa sara' basata su The Ant
    # quindi nativamente supportera' la mod di grbl che
    # utilizziamo come firmware.

    DIGITS = 4
    STEPS = 3
    SAFE_ABSOLUTE_Z_PROBE = -1.0
    CHANGE_TOOL_POS = (-41.2, -120.88, -1.0)
    PROBE_TOOL_POS = (-1.0, -1.0, -11.0)
    TAG = '@'

    def __init__(self, tag, machining_type='gerber', parent=None, units='ms'):

        self.parent = parent
        self.tag = tag

        self.mill = True

        self.change_tool_pos = self.CHANGE_TOOL_POS  # todo: vanno parametrizzati
        self.probe_tool_pos = self.PROBE_TOOL_POS  # todo: vanno parametrizzati
        self.safe_absolute_z_probe = self.SAFE_ABSOLUTE_Z_PROBE # todo: vanno parametrizzati

        # units:
        # ms -> metric system
        # is -> imperial system
        self.units = units

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
        else:
            self.cfg = {}
        self.type = machining_type
        self.path = None
        self.gcode = []

    def load_cfg(self, cfg):
        self.cfg = cfg

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
        # computa il gcode relativo alla
        # generazione dei fori

        self.gcode = []
        self.create_header()
        self.add_job_info()
        self.add_init()

        self.go_travel()
        self.spindle_on(True)

        for d in self.path:
            path = d[1]
            self.compute_drill_paths(path)

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

        #self.write(self.get_file_name())

    def compute_gerber(self):
        # essenzialmente si tratta di seguire i punti indicati dai paths
        # unendoli con movimenti veloci.
        # il formato del gcode, le info contenute e il tipo di file
        # potranno essere scelti nei settings
        # per ora creo il gcode con le sole info utili

        self.gcode = []
        self.create_header()
        self.add_job_info()
        self.add_init()

        # todo: aggiungere user head and foot

        self.go_travel()
        self.spindle_on(True)

        # ora per ogni path disponibile
        # raggiungo il punto iniziale
        # vado in modalita' mill
        # seguo il path ed infine mi rimetto
        # in modalita' travel

        for d in self.path:
            paths = d[1]
            self.compute_gerber_paths(paths)

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

        #self.write(self.get_file_name())

    def compute_pocketing(self):
        # essenzialmente si tratta di seguire i punti indicati dai paths
        # unendoli con movimenti veloci.
        # in aggiunta nel caso ci fosse un cfg valido di multipassaggio
        # eseguo le n passate necessarie
        # il formato del gcode, le info contenute e il tipo di file
        # potranno essere scelti nei settings
        # per ora creo il gcode con le sole info utili

        self.gcode = []
        self.create_header()
        self.add_job_info()
        self.add_init()

        # todo: aggiungere user header and footer

        self.go_travel()
        self.spindle_on(True)

        # ora per ogni path disponibile
        # raggiungo il punto iniziale
        # vado in modalita' mill
        # seguo il path ed infine mi rimetto
        # in modalita' travel

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
                # print("cut " + str(cut))
                # print("dpp " + str(dpp))
                # print("N " + str(n))
                pass_list = [sign * dpp * x for x in range(1, n)] + [cut]
                pass_list.sort(reverse=True)
                # print("Pass List: " + str(pass_list))
                self.compute_pocketing_paths(paths, pass_list)
            else:
                self.compute_gerber_paths(paths)

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

        #self.write(self.get_file_name())

    def compute_drill_paths(self, paths):
        # imposto la velocita' di lavoro
        # per z
        zf = self.cfg['z_feedrate']
        zf_str = self.format_float(zf)
        self.gcode.append("G01 F" + zf_str + "\n")
        tool_change = False
        for p in paths:
            cs = list(p.coords)
            for c in cs:
                self.go_to(c)
                self.make_drill()
                self.go_travel()
            if tool_change:
                self.go_tool_change()
            tool_change = True

    def compute_gerber_paths(self, paths):
        # print(paths)
        for p in paths:
            cs = list(p.coords)
            self.go_to(cs.pop(0))
            self.go_mill()
            for c in cs:
                self.go_to(c)
            self.go_travel()

    def compute_pocketing_paths(self, paths, pass_list):
        # print(paths)
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
                # cs.pop(0)
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

    def get_tool_change_string(self):
        zero_str = self.format_float(0.0)
        z_m_one = self.format_float(self.safe_absolute_z_probe)

        x_ct_str = self.format_float(self.change_tool_pos[0])
        y_ct_str = self.format_float(self.change_tool_pos[1])
        z_ct_str = self.format_float(self.change_tool_pos[2])

        x_str = self.format_float(self.probe_tool_pos[0])
        y_str = self.format_float(self.probe_tool_pos[1])
        z_str = self.format_float(self.probe_tool_pos[2])

        gc = ""
        gc += self.gcode_comment("The Ant Tool Change")

        # super safe Z position
        gc += "F60\n"
        gc += "G54\n"
        gc += "G53 G00 Z" + z_m_one + " F60\n"
        # go to probe position and performe a probe (G54 WORK SYSTEM COORD)
        gc += "G00 X" + x_str + " Y" + y_str + "\n"
        gc += "G01 F10\n"
        gc += "G38.2 Z" + z_str + "\n"
        gc += "G01 F60\n"
        # move to change tool position (MACHINE SYSTEM COORD)
        gc += "G53 G00 Z" + z_ct_str + "\n"
        gc += "G53 G00 X" + x_ct_str + "\n"
        gc += "G53 G00 Y" + y_ct_str + "\n"
        # wait for the change tool
        gc += "M0\n"
        # go to probe position and performe a probe (G54 WORK SYSTEM COORD)
        gc += "G53 G01 Z" + z_m_one + "\n"
        gc += "G54\n"
        gc += "G00 X" + x_str + " Y" + y_str + "\n"
        gc += "G01 F10\n"
        gc += "G38.2 Z" + z_str + "\n"
        gc += "G01 F60\n"
        # add tool offset
        pre_z_probe_tag = self.get_pre_z_probe_tag()
        gc += "G10 P2 L20 Z" + pre_z_probe_tag + "\n"
        # return to WP Zero
        gc += "G53 G01 Z" + z_m_one + " F60\n"
        gc += "G00 X" + zero_str + " Y" + zero_str + "\n"
        return gc

    def get_pre_z_probe_tag(self):
        return "@pre_z_probe".upper()

    def check_tag_in_string(self, gc_str):
        return self.get_pre_z_probe_tag() in gc_str

    def compute_tag(self, gc_str, status, probe_data):
        ret_str = gc_str
        tag = self.get_pre_z_probe_tag()
        print("-> Check TAG")
        print("--> TAG: " + str(tag))
        print("--> GCode: " + str(gc_str))
        if self.check_tag_in_string(gc_str):
            print("--> TAG in GCode Line")
            pre_probe = self.format_float(probe_data[1][2])
            print("--> Pre Probe " + str(pre_probe))
            ret_str = gc_str.replace(tag, pre_probe)
            print("--> Ret " + str(ret_str))
        return ret_str

    def go_tool_change(self):
        gc = self.get_tool_change_string()
        self.gcode.append(gc)

    def make_drill(self):
        steps = self.STEPS
        gc = ""

        # eseguo il foro in n steps
        # forando e tornando a zero per
        # scaricare la punta

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

    def get_autobed_leveling_code(self, xy_c_l, travel_z, probe_z_max, probe_feed_rate):
        abl_cmd_ls = []
        abl_cmd_s = ""
        abl_cmd_s += "G01 F" + str(probe_feed_rate) + "\n"  # Set probe feed rate

        prb_num_todo = 0
        for coord in xy_c_l:
            prb_num_todo += 1
            abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # Get to safety Z Travel
            abl_cmd_s += "G00 X" + str(coord[0]) + "Y" + str(coord[1]) + "\n"  # Go to XY coordinate
            abl_cmd_s += "G38.2 Z" + str(probe_z_max) + "F" + str(probe_feed_rate) + "\n"  # Set probe command
            abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # Get to safety Z Travel
            abl_cmd_ls.append(abl_cmd_s)
            abl_cmd_s = ""

        abl_cmd_s = ""
        abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # Get to safety Z Travel
        abl_cmd_s += "G00 X" + str((xy_c_l[0][0] + xy_c_l[-1][0]) / 2.0) + "Y" + \
                          str((xy_c_l[0][1] + xy_c_l[-1][1]) / 2.0) + "\n"
        abl_cmd_s += "G38.2 Z" + str(probe_z_max) + "F" + str(probe_feed_rate) + "\n"  # Set probe command
        prb_num_todo += 1
        abl_cmd_s += "G10 P1 L20 Z0\n"  # Set Z zero
        abl_cmd_s += "G00 Z" + str(travel_z) + "\n"  # Get to safety Z Travel
        abl_cmd_s += "G00 X" + str(xy_c_l[0][0]) + "Y" + str(xy_c_l[0][1]) + "\n"  # Go 1st XY coordinate
        abl_cmd_ls.append(abl_cmd_s)

        return abl_cmd_ls, prb_num_todo

    def get_tool_change_code(self, to_comment=""):
        s = ""
        if to_comment != "":
            s += self.gcode_comment(to_comment)
        s += self.get_tool_change_string()
        return s

    def get_file_name(self):
        return self.tag.lower() + "_" + self.type.lower() + ".gcode"

    def write(self, file_path):
        print("Writing gcode file:")
        print("\t " + str(os.path.abspath(file_path)))
        with open(file_path, 'w') as f:
            f.write("".join(self.gcode))
        print("Done")


class GcodeLine:
    def __init__(self):
        self.command = []
        self.params = od({})
        self.comment = ""

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
        s += " X" + str(self.coords[0])
        s += " Y" + str(self.coords[1])
        s += " Z" + str(self.coords[2])
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
                print("Lines")
                print(lines)
                if lines:
                    # ha caricato il file gcode
                    # come primo step va tipizzata ogni linea
                    self.gc = GCode(lines)
                    self.pre_parsing()
        else:
            print("Invalid GCode File Path")

    def pre_parsing(self):
        gcode_commander = GCoder("dummy", "commander")
        if self.gc is not None:
            # per ora individua i cambio tools e li espande
            # con la corretta procedura
            ls = self.gc.original_lines
            print("LS")
            print(ls)
            print("----")
            for l in ls:
                print(l)
                gl = self.interp(single_line=l)
                nls = []
                for g in gl:
                    print("G " + str(g))
                    cmd_l = g.command
                    print(" --> CMD: " + str(cmd_l))
                    if cmd_l:
                        for cmd in cmd_l:
                            if cmd[0] == self.CHANGE_TOOL_COMMAND[0] and self.CHANGE_TOOL_COMMAND[1] in cmd[1]:
                                tool_change_gc = gcode_commander.get_tool_change_code()
                                d = "\n"
                                nls = [e + d for e in tool_change_gc.split(d) if e]
                if not nls:
                    nls = [l]
                else:
                    print("Tool Change Detected!")
                    print(nls)
                self.gc.modified_lines += nls

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
                    # salvo l'eventuale commento
                    gcl.comment = comment.strip()
                    # decodifico l'eventuale comando
                    if data:
                        data = data.lower()
                        splitted = re.findall(r'[a-z][-]*[\d.]+', data)

                        # detect tags (remember, tags cannot be used in motion commands)
                        tags = re.findall(r'[a-z][@]*[a-z_]+', data)

                        cmd = splitted.pop(0)
                        ct = cmd[0]
                        cd = [int(x) for x in cmd[1::].split(".")]
                        gcl.command = [(ct, tuple(cd))]
                        # print("GCL CMD: " + str(gcl.command))

                        if splitted:
                            if splitted[0].upper().startswith("G"):
                                # second command
                                cmd = splitted.pop(0)
                                ct = cmd[0]
                                cd = [int(x) for x in cmd[1::].split(".")]
                                gcl.command += [(ct, tuple(cd))]

                        # print(gcl.command)

                        par = splitted
                        params = od({})
                        for p in par:
                            params[p[0]] = float(p[1::])
                        for t in tags:
                            params[t[0]] = t[1::]
                        gcl.params = params
                    # print(gcl)
                    gcll.append(gcl)
            if single_line is None:
                self.gc.gcll = gcll
        return gcll

    def recode_gcode(self):
        gcls = []
        if self.gc.modified_vectors:
            gcv = self.gc.modified_vectors
        else:
            gcv = self.gc.original_vectors
        if gcv:
            gcv_len = len(gcv)
            # in base alla lista delle righe
            gcl = self.gc.gcll
            #vl = gcv[1].line
            # parto da uno perche' il primo punto e' 0.0 di default
            vi = 1
            for l in range(len(gcl)):
                if gcv[vi].line == l:
                    cl_flag = True
                    # print the gcode vector line
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
                    ci = last_cmd[1][0]
                    if cn == 'g' and ci < 2 and not machine_pos:
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
            #vec = (np.array((x_min, yc)), np.array((x_max, yc)))
            #vectors.append(vec)
            vectors.append(LineString(((x_min, yc), (x_max, yc))))
        for xc in x:
            #vec = (np.array((xc, y_min)), np.array((xc, y_max)))
            #vectors.append(vec)
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
                #cs = plt.contourf(X, Y, Z, cmap="bone")
                #cbar = plt.colorbar(cs)
                #plt.title('Grid Example')
                #plt.show()
                return X, Y, Z

    def get_grid_data(self, probe_results, steps, last_probe, wco_offset=(0, 0, 0)):
        x, y, z = zip(*probe_results)
        X = np.array(x).reshape(steps[0], steps[1]) - wco_offset[0]
        Y = np.array(y).reshape(steps[0], steps[1]) - wco_offset[1]
        Z = np.array(z).reshape(steps[0], steps[1]) - last_probe[2]
        return X, Y, Z

    def interp_grid_data(self):
        if self.grid_data is not None:
            print("Grid Data Interpolation...")
            X, Y, Z = self.grid_data
            self.ig = spi.interp2d(X, Y, Z, kind='cubic')
            print("Done")

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

    def apply_advanced(self):
        # Rispetto a quello semplice che applica le info di ABL
        # solo ai vettori originali
        # questa routine mette in campo strategie per adattare l'intero
        # gcode alla superficie definita dall'ABL
        # in questo caso quindi vengono analizzati anche i segmenti del
        # gcode e non solo i suoi punti. Analizzando quindi l'andamento della
        # superficie di ABL sotto ogni segmento, nel caso in cui non abbia
        # un andamento lineare, il segmento viene suddiviso in sub-segmenti
        # in cui la variazione ABL puo' essere considerata lineare.
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
            print("Duration ", tb-ta)
            return True
        else:
            return False

    def get_grid_intersection(self, a1, a2):
        i_l = []
        line1 = LineString([a1, a2])
        for s in self.grid_lines:
            line2 = s  # LineString([s[0], s[1]])
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
    #abl.apply_advanced()
