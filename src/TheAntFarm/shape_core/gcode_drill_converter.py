
import os
import math
import numpy as np

from .gcode_manager import GCodeParser
from gerber.excellon import ExcellonFile, ExcellonStatement
from .geometry_manager import Geom, merge_polygons


class DrillGcodeConverter:
    def __init__(self, cfg):

        self.gcode_path = ""
        self.cfg = cfg
        self.parser = GCodeParser(None)

    def load_gcode(self, gcode_path):
        self.gcode_path = gcode_path

    def convert(self):

        if self.gcode_path:
            if os.path.isfile(self.gcode_path):
                self.parser.load_gcode_file(self.gcode_path)
                self.parser.interp()
                self.parser.vectorize()
            else:
                print("Invalid GCode Path")

    def get_drill_layer(self):

        layer = None
        if self.parser is not None:
            if self.parser.gc is not None:
                if self.parser.gc.original_vectors is not None:
                    ov = self.parser.gc.original_vectors
                    coords = np.array([v.coords for v in ov if v.type == v.WORKING])
                    z_min = np.min(coords, axis=0)[2]
                    drill_coords = coords[np.where(np.isclose(coords[:, 2], z_min))[0], :]

                    mp = []
                    for i in range(drill_coords.shape[0]):
                        dd = self.cfg["default_gcode_drill_size"]
                        center_coords = drill_coords[i, :].tolist()
                        circle_coords = self.get_all_circle_coords(center_coords,
                                                                   radius=dd,
                                                                   n_points=40)
                        gd = {
                            "points": circle_coords,
                            "closed": True,
                            "polarity": "dark",
                            "complex": False
                        }

                        g = Geom(gd)
                        if g.closed:
                            mp.append(g)

                    layer = merge_polygons(mp)
                    print(layer)

                else:
                    print("No Vectorized GCode")
            else:
                print("No Loaded GCode")
        else:
            print("No Active GCode Parser")

        return layer

    # https://gis.stackexchange.com/questions/394955/generating-approximate-polygon-for-circle-with-given-radius-and-centre-without
    @staticmethod
    # This function gets just one pair of coordinates based on the angle theta
    def get_circle_coord(theta, x_center, y_center, z_center, radius):
        x = radius * math.cos(theta) + x_center
        y = radius * math.sin(theta) + y_center
        return x, y, z_center

    # This function gets all the pairs of coordinates
    def get_all_circle_coords(self, center_coords, radius, n_points):
        x_center, y_center, z_center = center_coords
        thetas = [i/n_points * math.tau for i in range(n_points)]
        circle_coords = [self.get_circle_coord(theta, x_center, y_center, z_center, radius) for theta in thetas]
        return circle_coords








