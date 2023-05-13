
class CommandManager:
    """
    A CommandManager Object manages requests of gcode translation for a set of known commands.
    ...

    Supported Commands
    ------------------
    - soft_reset
    - unlock
    - homing
    - goto
    - jog
    - set_wps
    - probe
    - hold

    Methods
    -------
    load_cfg(cfg=None)
        Load the object relative configuration

    get_command_str(command, values)
        return the GCODE sting of the requested command.
        values, if needed, contain X Y and Z coordinates.
    """

    AXIS = ("X", "Y", "Z")
    CMDS = {
        "soft_reset": b'\x18',
        "unlock": "$X",
        "homing": "$H",
        "goto": "G90 G00",
        "jog": "$J=G91",
        "set_wps": "G10 P1 L20",
        "probe": "G38.2",
        "hold": "M0",
    }

    def __init__(self, parent):
        """
        Return a CommandManager Object.

            Parameters:
                parent (object): Usually a GCoder object o derivatives

            Returns:
                 CommandManager Object (object)
        """
        self.parent = parent
        self.cfg = None
        self.load_cfg()

    def load_cfg(self, cfg=None):
        """
        Return a CommandManager Object.

            Parameters:
                cfg (dict): if None a default set of configuration parameters loaded

            Returns:
                 None

            cfg parameters:
                - tool_probe_pos (tuple): Probe position coordinates (X, Y, Z) [default (-1.0, -1.0, -11.0)]
                - tool_probe_working (bool) If False: tool_probe_pos is intended in machine pos,
                                            if True: working pos [default True]
                - tool_probe_min (float): Probe Z limit [default -11.0]
                - tool_change_pos (tuple): Tool change position in machine pos. [default (-41.2, -120.88, -1.0)]
                - tool_probe_feedrate (tuple): Feedrate for Jogging XY,
                                               Jogging Z and Probe approaching respectively
                                               [default (300.0, 80.0, 50.0)]
                - tool_probe_hold (bool): Force and HOLD before the probe command [default False]
                - tool_probe_zero (bool): Force zeroing Z axis after probing [default False]
                - safe_pos (tuple): Unused
        """
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

    def get_command_str(self, command, values):
        str_l = []
        xy_check = [q is not None for q in values[0:2]]
        z_check = values[2] is not None
        if command == "soft_reset":
            str_l.append(self.CMDS[command])
        elif command == "unlock":
            str_l.append(self.CMDS[command] + "\n")
        elif command == "homing":
            str_l.append(self.CMDS[command] + "\n")
        elif command == "jog" or command == "goto":
            feedrate = self.cfg['tool_probe_feedrate']
            xy = values[0:2]
            z = values[2]
            if z_check:
                zstr = self.parent.format_float(z)
                zfrstr = self.parent.format_float(feedrate[1])
                cmd = self.CMDS[command] + " " + self.AXIS[2] + zstr
                if command == "jog":
                    cmd += " F" + zfrstr
                cmd += "\n"
                str_l.append(cmd)
            if any(xy_check):
                cmd = self.CMDS[command]
                for i, v in enumerate(xy):
                    if v is not None:
                        cmd += " " + self.AXIS[i] + self.parent.format_float(v)
                if command == "jog" or command == "goto":
                    cmd += " F" + self.parent.format_float(feedrate[0])
                cmd += "\n"
                str_l.append(cmd)

        elif command == "set_wps":
            cmd = self.CMDS[command]
            for i, v in enumerate(values):
                if v is not None:
                    cmd += " " + self.AXIS[i] + self.parent.format_float(v)
            cmd += "\n"
            str_l.append(cmd)
        elif command == "probe":
            if self.cfg["tool_probe_hold"]:
                cmd = self.CMDS["hold"] + "\n"
                str_l.append(cmd)
            fr = self.cfg['tool_probe_feedrate'][2]
            frstr = self.parent.format_float(fr)
            cmd = self.CMDS[command] + " F" + frstr
            for i, v in enumerate(values):
                if v is not None:
                    cmd += " " + self.AXIS[i] + self.parent.format_float(v)
            cmd += "\n"
            str_l.append(cmd)
            if self.cfg["tool_probe_zero"]:
                str_l += self.get_command_str("set_wps", (None, None, 0.0))
        return str_l
