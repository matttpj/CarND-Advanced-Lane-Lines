import cv2
import numpy as np

default_src_points = np.float32([[600, 450],
                                 [700, 450],
                                 [1020, 660],
                                 [210, 720]])

default_dst_points  = np.float32([[200, 0],
                                  [1000, 0],
                                  [1020, 660],
                                  [210, 720]])

class BirdsEyeView:
    def __init__(self, src_points=default_src_points, dst_points=default_dst_points):
        self.src_points = src_points
        self.dst_points = dst_points

    def transform_matrix(self):
        return cv2.getPerspectiveTransform(self.src_points, self.dst_points)

    def inverse_transform_matrix(self):
        return cv2.getPerspectiveTransform(self.dst_points, self.src_points)

    def transform_to_birdseye(self, img):
        return cv2.warpPerspective(img, self.transform_matrix(), img.shape[1::-1])

    def transform_from_birdseye(self, img, size_img):
        return cv2.warpPerspective(img, self.inverse_transform_matrix(), size_img.shape[1::-1])
