"""The camera frames of the Align tab: the holes are marked without a slow circle search."""

from unittest.mock import patch

import cv2
import numpy as np
import pytest

from TheAntFarm.double_side_manager import DoubleSideManager

HOLE_CENTRE = (200, 150)
BOARD = (40, 40, 40)
HOLE_MARK = (255, 0, 0)


@pytest.fixture
def frame():
    image = np.full((480, 640, 3), BOARD, np.uint8)
    cv2.circle(image, HOLE_CENTRE, 6, (240, 240, 240), -1)
    return image


class TestDetectHoles:
    def test_no_circle_search_is_made(self, frame):
        with patch("TheAntFarm.double_side_manager.cv2.HoughCircles") as hough:
            DoubleSideManager.detect_holes(frame, thr1=125, zoom_f=1)

        hough.assert_not_called()

    def test_a_hole_is_marked_at_its_centre(self, frame):
        out = DoubleSideManager.detect_holes(frame, thr1=125, zoom_f=1)

        x, y = HOLE_CENTRE
        assert tuple(out[y, x]) == HOLE_MARK

    def test_the_frame_keeps_its_size(self, frame):
        out = DoubleSideManager.detect_holes(frame, thr1=125, zoom_f=2)

        assert out.shape == frame.shape
