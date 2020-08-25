from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from detect import detect_lane_lines
from distortion import Distortion
from image_helper import rgb_image
from birdseye import BirdsEyeView
from lane import Lane
import cv2
import glob
import numpy as np
import combined_thresholds
import matplotlib.pyplot as plt

def overlay_text(image, text, pos=(0, 0), color=(255, 255, 255)):
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("./fonts/LucidaBrightRegular.ttf", 64)
    draw.text(pos, text, color, font=font)
    image = np.asarray(image)

    return image

def overlay_lane(image, left_fit, right_fit, birdseye):
    left_ys = np.linspace(0, 100, num=101) * 7.2
    left_xs = left_fit[0]*left_ys**2 + left_fit[1]*left_ys + left_fit[2]

    right_ys = np.linspace(0, 100, num=101) * 7.2
    right_xs = right_fit[0]*right_ys**2 + right_fit[1]*right_ys + right_fit[2]

    color_warp = np.zeros_like(image).astype(np.uint8)

    pts_left = np.array([np.transpose(np.vstack([left_xs, left_ys]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_xs, right_ys])))])
    pts = np.hstack((pts_left, pts_right))

    cv2.fillPoly(color_warp, np.int_([pts]), (0, 0, 255))
    newwarp = cv2.warpPerspective(color_warp, birdseye.inverse_transform_matrix(), (image.shape[1], image.shape[0]))
    newwarp = birdseye.transform_from_birdseye(color_warp, image)

    return cv2.addWeighted(image, 1, newwarp, 0.3, 0)

def overlay_detected_lane_data(image, lanes, birdseye):
    height, width, _ = image.shape

    image = overlay_lane(image, lanes.left.pixels.fit, lanes.right.pixels.fit, birdseye)
    image = overlay_text(image, "Left curvature: {0:.2f}m".format(lanes.left.meters.curvature(height)), pos=(10, 10))
    image = overlay_text(image, "Right curvature: {0:.2f}m".format(lanes.right.meters.curvature(height)), pos=(10, 90))
    image = overlay_text(image, "Vehicle offset: {0:.2f}m".format(lanes.distance_from_center((width/2, height))), pos=(10, 170))

    return image

class OverlayDetectedLaneData:
    def __init__(self, birdseye):
        self.birdseye = birdseye

    def draw_overlays(self, image, lanes):
        return overlay_detected_lane_data(
                image=image,
                lanes=lanes,
                birdseye=self.birdseye)

if __name__ == "__main__":
    np.seterr(all='ignore')

    birdseye = BirdsEyeView()
    distortion = Distortion(calibration_data_filepath="./camera_cal/wide_dist_pickle.p")
    overlay = OverlayDetectedLaneData(birdseye=birdseye)

    images_glob = glob.glob("./test_images/test1.jpg")

    for filepath in images_glob:
        image = rgb_image(filepath)
        bin_image = distortion.undistort(image)
        bin_image = birdseye.transform_to_birdseye(bin_image)
        bin_image, gb = combined_thresholds.pipeline(bin_image)

        lanes, _ = detect_lane_lines(bin_image)
        output_image = overlay.draw_overlays(image, lanes)

        plt.imshow(output_image)
        plt.show()
