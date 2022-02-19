
import cv2
import numpy as np


class DoubleSideManager:

	def __init__(self):

		self.detected_holes = []
		# grab webcam
		self.cap = cv2.VideoCapture(4, cv2.CAP_DSHOW)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	@staticmethod
	def rotate_image(image, angle):
		image_center = tuple(np.array(image.shape[1::-1]) / 2)
		rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
		result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
		return result

	def get_webcam_frame(self):
		ret, frame = self.cap.read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		# frame = self.rotate_image(frame, 0)
		return frame

	@staticmethod
	def detect_holes(frame, thr1=125):
		image = cv2.cvtColor(frame.copy(), cv2.COLOR_RGB2GRAY)
		image = cv2.GaussianBlur(image, (15, 15), 0)
		#image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
		#image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 2)
		#_, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
		_, image = cv2.threshold(image, thr1, 255, cv2.THRESH_BINARY)
		imagebn = image.copy()
		image = cv2.Canny(image, 50, 120)
		#frame = cv2.cvtColor(imagebn, cv2.COLOR_GRAY2RGB)

		# circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 22, minDist=1, maxRadius=50)
		# x = circles[0, :, 0]
		# y = circles[0, :, 1]

		# print(x)
		# print(y)

		# for i in range(len(x)):
		# 	hx = x[i]
		# 	hy = y[i]
		# 	cv2.circle(frame, (hx, hy), 3, (255, 255, 255), -1)

		if True:
			cnts, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

			# loop over the contours
			for c in cnts:
				# compute the center of the contour
				M = cv2.moments(c)
				(cx, cy), radius = cv2.minEnclosingCircle(c)
				if M["m00"] != 0.0 and radius < 10:
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])

					# draw the contour and center of the shape on the image
					cv2.drawContours(frame, [c], -1, (255, 255, 255), 1)
					cv2.circle(frame, (cX, cY), 3, (255, 0, 0), -1)

		# Green color in BGR
		color = (0, 0, 255)

		# Line thickness of 9 px
		thickness = 1

		height, width, channels = frame.shape
		hhalf = int(height/2)
		whalf = int(width/2)
		start_point = (whalf, 0)
		end_point = (whalf, height)
		frame = cv2.line(frame, start_point, end_point, color, thickness)
		start_point = (0, hhalf)
		end_point = (width, hhalf)
		frame = cv2.line(frame, start_point, end_point, color, thickness)

		return frame
