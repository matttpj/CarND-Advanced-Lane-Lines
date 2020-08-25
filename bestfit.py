from distortion import Distortion
from image_helper import rgb_image
from birdseye import BirdsEyeView
from lane import Lane
from lanes import Lanes
import cv2
import numpy as np
import combined_thresholds
import matplotlib.pyplot as plt

def best_fit_lines(lanes, image):

    # Paint lane pixels
    lanes_image = np.zeros_like(image).astype(np.uint8)
    lanes_image[lanes.left.ys, lanes.left.xs] = [255,0,0] # red
    lanes_image[lanes.right.ys, lanes.right.xs] = [0,0,255] # blue

    # Left lane best fit polynomial
    left_p = np.poly1d(lanes.left.pixels.fit)
    left_ys = np.linspace(0, 720, 100)
    left_xs = left_p(left_ys)

    # Right lane best fit polynomial
    right_p = np.poly1d(lanes.right.pixels.fit)
    right_ys = np.linspace(0, 720, 100)
    right_xs = right_p(right_ys)

    # Create new blank image
    pts_image = np.zeros_like(image).astype(np.uint8)

    # Create arrays to hold best fit points
    pts_left = np.array([np.transpose(np.vstack([left_xs, left_ys]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_xs, right_ys])))])
    pts = np.hstack((pts_left, pts_right))

    # Overlay best fit lines
    pts_image = cv2.polylines(pts_image, np.int_([pts_left]), isClosed=False, color=[255,255,0], thickness=12)
    pts_image = cv2.polylines(pts_image, np.int_([pts_right]), isClosed=False, color=[255,255,0], thickness=12)
    out_image = cv2.addWeighted(lanes_image, 1, pts_image, 1, 0, dtype=-1)

    return out_image
