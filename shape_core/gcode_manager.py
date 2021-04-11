
import os
from datetime import datetime


class GCoder:
    # questa classe potrebbe essere la classe principale
    # che poi verra' utilizzata per diversificare i
    # gcode in base al controller che dovra' interpretarlo
    # naturalmente questa sara' basata su The Ant
    # quindi nativamente supportera' la mod di grbl che
    # utilizziamo come firmware.

    DIGITS = 4
    STEPS = 3

    def __init__(self, tag, machining_type='gerber', parent=None, units='ms'):

        self.parent = parent
        self.tag = tag

        self.mill = True

        self.change_tool_pos = (6.0, 8.0, 9.0)
        self.probe_tool_pos = (6.0, 8.0, 9.0)

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

    def format_float(self, f):
        ff = round(f, self.DIGITS)
        fs = "{:." + str(self.DIGITS) + "f}"
        f_str = fs.format(ff)
        return f_str

    def load_path(self, path):
        self.path = path

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
            print("D")
            print(d)
            path = d[1]
            self.compute_drill_paths([path])

        self.spindle_on(False)
        self.go_to((0.0, 0.0))

        self.write(self.get_file_name())

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

        self.write(self.get_file_name())

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
        gc = ""
        # mi muovo a probe pos
        # faccio una prima probe
        # Porto lo z a 0 macchina
        gc += self.gcode_comment("Dummy Tool Change")

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

    def go_mill(self):
        gc = ""
        zf = self.cfg['z_feedrate']
        zf_str = self.format_float(zf)
        gc += "G01 F" + zf_str + "\n"
        zt = self.cfg['cut']
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
