from calibrate_camera import load_camera_calibration
import cv2
import pickle

class Distortion:
    def __init__(self, calibration_data_filepath):
        self.load_camera_calibration(calibration_data_filepath)

    def load_camera_calibration(self, filepath):
        self.mtx, self.dist = load_camera_calibration(filepath)

    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
