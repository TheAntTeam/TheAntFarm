
import vispy.app as vapp
vapp.use_app('pyside2')
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
        self.view.bgcolor = '#ffffff'
        self.view.camera = TurntableCamera(
            fov=0.0, distance=30.0, up='+z', center=(0.0, 0.0, 0.0))
        self.last_pos = [0, 0, 0]
        self.pos_markers = visuals.Markers()
        self.meas_markers = visuals.Markers()
        self.pos_data = np.array([0, 0, 0], ndmin=2)
        self.meas_data = np.array([0, 0, 0], ndmin=2)
        self.lines = []

        self.view.add(self.pos_markers)
        self.view.add(self.meas_markers)

        self.freeze()

        visuals.XYZAxis(parent=self.view.scene)

