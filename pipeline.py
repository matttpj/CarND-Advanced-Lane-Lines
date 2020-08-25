from detect import detect_lane_lines
from distortion import Distortion
from image_helper import rgb_image
from overlay import OverlayDetectedLaneData
from birdseye import BirdsEyeView
from lanes_average import LanesAverage
import cv2
import glob
import numpy as np
import combined_thresholds
import matplotlib.pyplot as plt

class Pipeline:
    def __init__(self):
        self.birdseye = BirdsEyeView()
        self.distortion = Distortion(calibration_data_filepath="./camera_cal/wide_dist_pickle.p")
        self.overlay = OverlayDetectedLaneData(birdseye=self.birdseye)
        self.last_lanes = None
        self.lanes_average = LanesAverage()

    # @profile
    def process_image_pipeline(self, image):
        image_height, image_width, _ = image.shape

        bin_image = self.distortion.undistort(image)
        bin_image = self.birdseye.transform_to_birdseye(bin_image)
        bin_image, gb = combined_thresholds.pipeline(bin_image)

        lanes, _ = detect_lane_lines(bin_image, self.last_lanes)
        self.lanes_average.update(lanes)

        if self.last_lanes is None:
            self.last_lanes = lanes

        if lanes.lanes_parallel(image_height) and lanes.distance_from_center((image_width/2, image_height)) < 4.0:
            self.last_lanes = lanes

        return self.overlay.draw_overlays(
                image=image,
                lanes=self.lanes_average)

if __name__ == "__main__":
    np.seterr(all='ignore')
    pipeline = Pipeline()

    # images_glob = glob.glob("./test_images/test/*.jpg")
    images_glob = glob.glob("./test_images/test3.jpg")

    for filepath in images_glob:
        image = rgb_image(filepath)
        result = pipeline.process_image_pipeline(image)

        plt.imshow(result)
        plt.show()
