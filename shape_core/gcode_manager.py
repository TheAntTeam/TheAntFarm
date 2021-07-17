
import os
import re
import numpy as np
from collections import OrderedDict as od
from datetime import datetime
# import matplotlib.pyplot as plt
import scipy.interpolate as spi


class GCoder:
    # questa classe potrebbe essere la classe principale
    # che poi verra' utilizzata per diversificare i
    # gcode in base al controller che dovra' interpretarlo
    # naturalmente questa sara' basata su The Ant
    # quindi nativamente supportera' la mod di grbl che
    # utilizziamo come firmware.

    DIGITS = 4
    STEPS = 3
    SAFE_Z_PROBE = -1.0
    CHANGE_TOOL_POS = (6.0, 8.0, 9.0)
    PROBE_TOOL_POS = (6.0, 8.0, 9.0)

    def __init__(self, tag, machining_type='gerber', parent=None, units='ms'):

        self.parent = parent
        self.tag = tag

        self.mill = True

        self.change_tool_pos = self.CHANGE_TOOL_POS  # todo: vanno parametrizzati
        self.probe_tool_pos = self.PROBE_TOOL_POS  # todo: vanno parametrizzati
        self.safe_z_probe = self.SAFE_Z_PROBE

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

        # todo: aggiungere user head and foot

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
        print(paths)
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

    def go_tool_change(self):

        zero_str = self.format_float(0.0)
        z_m_one = self.format_float(self.SAFE_Z_PROBE)
        x_str = self.format_float(self.probe_tool_pos[0])
        y_str = self.format_float(self.probe_tool_pos[1])
        z_str = self.format_float(self.probe_tool_pos[2])

        gc = ""
        gc += self.gcode_comment("The Ant Tool Change")
        gc += "G90\n"
        gc += "G01 Z" + z_m_one + "\n"
        gc += "G00 X" + x_str + " Y" + y_str + "\n"
        gc += "G91\n"
        gc += "G38.2 Z" + z_str + "\n"
        gc += "G55\n"
        gc += "G10 P2 L20 Z" + zero_str + "\n"
        gc += "T01\n"
        gc += "M06\n"
        gc += "G90\n"
        gc += "G01 Z" + z_m_one + "\n"
        gc += "G00 X" + x_str + " Y" + y_str + "\n"
        gc += "G91\n"
        gc += "G38.2 Z" + z_str + "\n"
        gc += "G92 Z" + zero_str + "\n"
        gc += "G54\n"
        gc += "G90\n"
        gc += "G01 Z" + z_m_one + "\n"
        gc += "G91\n"
        gc += "G00 X" + zero_str + " Y" + zero_str + "\n"

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
            gc += "P" + one_str + "\n"  # just a little pause
            spindle_speed = self.cfg['spindle']
            spindle_speed_str = self.format_float(spindle_speed)
            gc += "M3 S" + spindle_speed_str + "\n"  # spindle at the full speed
            gc += "\n"
        else:
            zero_str = self.format_float(0.0)
            gc += "M3 S" + zero_str + "\n"  # set speed to 0
            one_str = self.format_float(1.0)
            gc += "P" + one_str + "\n"  # just a little pause
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
        self.command = ()
        self.params = od({})
        self.comment = ""

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
    def __init__(self):
        self.coords = np.zeros((3,))
        self.line = -1
        self.sub_line = 0
        self.type = "w"  # w working t travel

    def __repr__(self):
        s = "GcodeVector (\n"
        s += " coords = " + str(self.coords) + "," + "\n"
        s += " type  = " + str("working" if self.type == "w" else "travel") + "\n"
        s += " line  = " + str(self.line) + "\n"
        if self.sub_line > 0:
            s += " sub_line  = " + str(self.sub_line) + "\n"
        s += ")\n"
        return s

    def copy(self):
        np = GcodePoint()
        np.coords = self.coords.copy()
        np.line = self.line
        np.sub_line = self.sub_line
        np.type = self.type
        return np


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

    def __init__(self, cfg):
        self.gcode_path = ""
        self.cfg = cfg
        self.gc = None

    def load_gcode_file(self, gcode_path):
        lines = []
        if os.path.isfile(gcode_path):
            self.gcode_path = gcode_path
            with open(self.gcode_path) as f:
                lines = f.readlines()
            if lines:
                # ha caricato il file gcode
                # come primo step va tipizzata ogni linea
                self.gc = GCode(lines)
        else:
            print("Invalid GCode File Path")

    def interp(self):
        if self.gc is not None:
            ls = self.gc.original_lines
            gcll = []
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

                        cmd = splitted.pop(0)
                        ct = cmd[0]
                        cd = [int(x) for x in cmd[1::].split(".")]
                        gcl.command = (ct, cd)

                        par = splitted
                        params = od({})
                        for p in par:
                            params[p[0]] = float(p[1::])
                        gcl.params = params
                    gcll.append(gcl)
            self.gc.gcll = gcll

    def vectorize(self):
        if self.gc.gcll:
            p0 = GcodePoint()
            last_coord = p0.coords.copy()
            vl = [p0]
            bb_max = [-1e6, -1e6, -1e6]
            bb_min = [1e6, 1e6, 1e6]
            for i, gcl in enumerate(self.gc.gcll):
                if gcl.command:
                    # print(gcl)
                    cn = gcl.command[0]
                    ci = gcl.command[1][0]
                    if cn == 'g' and ci < 2:
                        # e' un comando di movimento vado ad aggiornare la lista
                        # dei vettori
                        a = set(gcl.params.keys())
                        b = set(self.COORD_TAG)
                        c = b.intersection(a)
                        if c:
                            for e in c:
                                last_coord[self.COORD_TAG.index(e)] = gcl.params[e]
                                bb_max[self.COORD_TAG.index(e)] = max(bb_max[self.COORD_TAG.index(e)], gcl.params[e])
                                bb_min[self.COORD_TAG.index(e)] = min(bb_min[self.COORD_TAG.index(e)], gcl.params[e])
                            p = last_coord.copy()
                            px = GcodePoint()
                            px.coords = p
                            px.type = 't' if ci == 0 else 'w'
                            px.line = i
                            #print(gcl)
                            #print(px)
                            vl.append(px)
            if len(vl) > 1:
                self.gc.original_vectors = vl
                self.gc.bb = tuple(bb_min + bb_max)

    def get_gcode(self):
        return self.gc

    def get_bbox(self):
        return self.gc.bb


class GCodeLeveler:

    def __init__(self, gc, grid_data=None):
        self.gc = gc
        if grid_data is not None:
            self.grid_data = grid_data
        else:
            self.grid_data = self.get_dummy_grid_data()
        self.ig = None

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
                np = p.copy()
                delta = self.ig(np.coords[0], np.coords[1])
                np.coords[2] += delta
                mvl.append(np)
        print("Auto Bed Leveler Stop")


if __name__ == "__main__":

    gcode_path = "C:\\Users\\Mattia\\Documents\\PythonPrj\\TheAntLord\\gcode_tmp\\top_gerber.gcode"
    cfg = {}

    gcp = GCodeParser(cfg)
    gcp.load_gcode_file(gcode_path)
    gcp.interp()
    gcp.vectorize()
    abl = GCodeLeveler(gcp.gc)
    abl.get_dummy_grid_data()
    abl.interp_grid_data()
    abl.apply()
