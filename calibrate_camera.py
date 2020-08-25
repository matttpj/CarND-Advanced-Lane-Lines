from image_helper import rgb_image, rgb_to_gray
import cv2
import glob
import numpy as np
import pickle
import matplotlib.pyplot as plt


# List of images to be used for calibration
images_glob = sorted(glob.glob("./camera_cal/calibration*.jpg"))

# Shape of the calibration images
image_shape = rgb_image(images_glob[0]).shape[1::-1]

# Number of columns and rows for the chessboard
chessboard_shape = (9, 6)

# Where to save the calibration data
output_file = "./camera_cal/wide_dist_pickle.p"

objpoints = []
imgpoints = []

def calibrate_camera():

    for i, filepath in enumerate(images_glob):
        # Load image
        img = rgb_image(filepath)

        # Convert image to grayscale
        gray = rgb_to_gray(img)

        # Find chessboard corners for image
        ret, corners = cv2.findChessboardCorners(gray, chessboard_shape, None)

        # Create an object points array
        cols, rows = chessboard_shape
        objp = np.zeros((cols * rows, 3), np.float32)
        objp[:,:2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)

        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

        corners_img = cv2.drawChessboardCorners(img, (9,6), corners, ret)
        plt.imsave("./camera_cal/corners{:02d}.jpg" .format(i+1), corners_img)
        #plt.pause(0.5)

    # Use the object points and image points to calibrate a camera
    _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, image_shape, None, None)

    # Save the calibration data for use later
    save_camera_calibration(output_file, mtx, dist)

def load_camera_calibration(filepath):
    with open(filepath, "rb") as f:
        data = pickle.load(f)
        mtx, dist = data["mtx"], data["dist"]
        return mtx, dist

def save_camera_calibration(filepath, mtx, dist):
    with open(filepath, "wb") as f:
        data = {}
        data["mtx"] = mtx
        data["dist"] = dist
        pickle.dump(data, f)

if __name__ == "__main__":
    calibrate_camera()
