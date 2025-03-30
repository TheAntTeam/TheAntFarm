from PySide6 import QtMultimedia
import cv2
import numpy as np


class DoubleSideManager:

    def __init__(self):
        self.detected_holes = []
        self.cap = None
        self.holes_detector = self.init_holes_detector()

    @staticmethod
    def list_cameras_indexes():
        index = 0
        arr = []
        info = QtMultimedia.QMediaDevices.videoInputs()
        for cameraDevice in info:
            arr.append(cameraDevice.description())
            print(cameraDevice.description())

        return arr

    @staticmethod
    def rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    def update_camera(self, index):
        if index >= 0:
            self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        else:
            if isinstance(self.cap, cv2.VideoCapture):
                self.cap.release()

    def get_webcam_frame(self):
        frame = None
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # TODO: add rotation angle in the align settings
                frame = self.rotate_image(frame, 180)
        return frame

    @staticmethod
    def detect_holes(frame_in, thr1=125, zoom_f=2):

        width = frame_in.shape[1]
        height = frame_in.shape[0]

        width_z = width/zoom_f
        height_z = height/zoom_f

        crop_x = int((width - width_z)/2)
        crop_y = int((height - height_z)/2)
        cropped = frame_in[crop_y:height-crop_y, crop_x:width-crop_x]
        frame = cv2.resize(cropped, None, fx=zoom_f, fy=zoom_f)
        # frame[:, :, 0] = 0
        # frame[:, :, 2] = 0

        image_gray = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2GRAY)
        image_gray[np.where(image_gray > thr1)] = 255


        # image = cv2.GaussianBlur(image_gray, (15, 15), 0)
        # image = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        # image = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 2)
        # _, image = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY)


        ret, image = cv2.threshold(image_gray, thr1, 255, cv2.THRESH_BINARY)

        # imagebn = image.copy()

        # image = cv2.Canny(image, 50, 120)

        # frame = cv2.cvtColor(imagebn, cv2.COLOR_GRAY2RGB)

        # circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 22, minDist=1, maxRadius=50)
        # x = circles[0, :, 0]
        # y = circles[0, :, 1]

        # print(x)
        # print(y)

        # for i in range(len(x)):
        # 	hx = x[i]
        # 	hy = y[i]
        # 	cv2.circle(frame, (hx, hy), 3, (255, 255, 255), -1)
        # image = image_gray
        frame_out = frame

        if True:
            black_holes = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0,
                                    maxRadius=0)

            black_holes = None
            if black_holes is not None:
                black_circles = np.round(black_holes[0, :]).astype("int")
                for (x, y, r) in black_circles:
                    cv2.circle(frame_out, (x, y), r, (255, 0, 255), 2)

            cnts, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # loop over the contours
            for c in cnts:
                # compute the center of the contour
                M = cv2.moments(c)
                (cx, cy), radius = cv2.minEnclosingCircle(c)
                if M["m00"] != 0.0 and radius < 10 and radius > 3:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # draw the contour and center of the shape on the image
                    cv2.drawContours(frame_out, [c], -1, (255, 255, 255), 1)
                    cv2.circle(frame_out, (cX, cY), 3, (255, 0, 0), -1)

        # Green color in BGR
        color = (0, 0, 255)

        # Line thickness of 9 px
        thickness = 1

        height, width, channels = frame.shape
        hhalf = int(height/2)
        whalf = int(width/2)
        start_point = (whalf, 0)
        end_point = (whalf, height)

        frame_out = cv2.line(frame_out, start_point, end_point, color, thickness)
        start_point = (0, hhalf)
        end_point = (width, hhalf)
        frame_out = cv2.line(frame_out, start_point, end_point, color, thickness)

        return frame_out

    def detect_holes_test(self, frame_in, thr1=125):

        zoom_f = 2
        width = frame_in.shape[1]
        height = frame_in.shape[0]
        crop_x = int(width / (2 * zoom_f))
        crop_y = int(height / (2 * zoom_f))
        cropped = frame_in[crop_y:3*crop_y, crop_x:3*crop_x]
        frame = cv2.resize(cropped, None, fx=zoom_f, fy=zoom_f)

        overlay = frame.copy()
        keypoints = self.holes_detector.detect(frame)
        for k in keypoints:
            cv2.circle(overlay, (int(k.pt[0]), int(k.pt[1])), int(k.size / 2), (0, 0, 255), -1)
            cv2.line(overlay, (int(k.pt[0]) - 20, int(k.pt[1])), (int(k.pt[0]) + 20, int(k.pt[1])), (0, 0, 0), 3)
            cv2.line(overlay, (int(k.pt[0]), int(k.pt[1]) - 20), (int(k.pt[0]), int(k.pt[1]) + 20), (0, 0, 0), 3)

        opacity = 0.5
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        # Uncomment to resize to fit output window if needed

        # cv2.imshow("Output", frame)

        return frame

    @staticmethod
    def init_holes_detector():

        # Setup BlobDetector
        detector = cv2.SimpleBlobDetector_create()
        params = cv2.SimpleBlobDetector_Params()

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 2
        params.maxArea = 200

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.3

        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.87

        # Filter by Inertia
        params.filterByInertia = True
        params.minInertiaRatio = 0.8

        # Distance Between Blobs
        params.minDistBetweenBlobs = 3

        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        return detector

