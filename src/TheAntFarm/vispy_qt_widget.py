
import vispy.app as vapp
vapp.use_app('PySide6')
from vispy.app.qt import QtSceneCanvas
from vispy.scene import visuals
from vispy.scene.cameras import TurntableCamera
import numpy as np


class VispyCanvas(QtSceneCanvas):
    def __init__(self, parent):
        super(VispyCanvas, self).__init__(
            keys='interactive', size=(800, 600)
        )

        self.unfreeze()
        self.view = self.central_widget.add_view()
        self.view.bgcolor = '#444444'   #'#ffffff'
        self.view.camera = TurntableCamera(
            fov=0.0, distance=0.0, up='+z', center=(0.0, 0.0, 0.0), azimuth=0, elevation=90)
        self.last_pos = [0, 0, 0]
        self.pos_markers = visuals.Markers()
        self.meas_markers = visuals.Markers()
        self.pos_data = np.array([0, 0, 0], ndmin=2)
        self.meas_data = np.array([0, 0, 0], ndmin=2)
        self.pos_markers.set_data(self.pos_data)
        self.meas_markers.set_data(self.meas_data)
        self.lines = []

        self.view.add(self.pos_markers)
        self.view.add(self.meas_markers)

        self.freeze()

        visuals.XYZAxis(parent=self.view.scene)

