import logging

from PySide6.QtCore import QObject
from app.services.align_service import AlignService

logger = logging.getLogger(__name__)


class AlignController(QObject):

    EXCELLON_LAYER_TAGS = ("drill",)

    def __init__(self, settings):
        super(AlignController, self).__init__()
        self.settings = settings

        self._service = AlignService(
            camera_rotation=settings.app_settings.camera_rotation_angle,
            flip_h=settings.app_settings.camera_flip_h,
            flip_v=settings.app_settings.camera_flip_v,
        )

    @property
    def flipping_view(self):
        return self._service.flipping_view

    @property
    def align_data(self):
        return self._service.align_data

    @align_data.setter
    def align_data(self, value):
        self._service.align_data = value

    @property
    def threshold_value(self):
        return self._service.threshold_value

    def load_new_align_layer(self, layer, layer_path):
        result = self._service.load_align_layer(layer, layer_path)
        if result.ok and result.layer_data is not None:
            return [result.layer_data, True]
        if layer in self.EXCELLON_LAYER_TAGS:
            return [None, True]
        return [None, None]

    def remove_align_points(self, selected_rows):
        return self._service.remove_align_points(selected_rows)

    def flip_align_layer_horizontally(self, flipped):
        self._service.flip_horizontally(flipped)

    def flip_align_layer_vertically(self, flipped):
        self._service.flip_vertically(flipped)

    def update_threshold_value(self, new_threshold):
        self._service.set_threshold(new_threshold)

    def set_camera_rotation(self, angle: float) -> None:
        """Set camera rotation angle."""
        self._service.set_camera_rotation(angle)

    def set_camera_flip_h(self, flip_h: bool) -> None:
        """Set camera horizontal flip."""
        self._service.set_camera_flip_h(flip_h)

    def set_camera_flip_v(self, flip_v: bool) -> None:
        """Set camera vertical flip."""
        self._service.set_camera_flip_v(flip_v)

    def get_camera_list(self):
        return self._service.get_camera_list()

    def update_camera_selected(self, index):
        return self._service.update_camera(index)

    def camera_new_frame(self, zoom=1):
        return self._service.get_camera_frame(zoom)

    def add_new_align_point(self, geom_point, working_position_point):
        return self._service.add_align_point(geom_point, working_position_point)
