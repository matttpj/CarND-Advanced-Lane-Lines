import cv2
import matplotlib.image as mpimg

def rgb_image(filepath):
    """Load an image as RGB"""
    return mpimg.imread(filepath)

def rgb_to_gray(img):
    """Convert an RGB image to Grayscale"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def rgb_to_bgr(img):
    """Convert an RGB image to BGR"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def bgr_to_rgb(img):
    """Convert an BGR image to RGB"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def rgb_to_hls(img):
    """Convert an RGB image to HLS"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)

def sorter(item):
    """Get an item from the list (one-by-one) and return a score for that item."""
    return item[1]
