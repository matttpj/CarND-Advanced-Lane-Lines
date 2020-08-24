# Advanced Lane Lines

## Writeup by Matthew Jones

### Project: CarND-Advanced-Lane-Lines-P2
---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

  1. Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
  2. Apply a distortion correction to raw images.
  3. Use color transforms, gradients, etc., to create a thresholded binary image.
  4. Apply a perspective transform to rectify binary image ("birds-eye view").
  5. Detect lane pixels and fit to find the lane boundary.
  6. Determine the curvature of the lane and vehicle position with respect to center.
  7. Warp the detected lane boundaries back onto the original image and show estimate of lane curvature and vehicle position.
  8. Run project videos of a car driving down the freeway through the image processing pipeline.
  9. Discuss challenging aspects of the project.

## Image References

|1. Chessboard corners identified |2. Curved road undistorted |
|:---:|:---:|
|<img src="./camera_cal/corners06.jpg"> |<img src="./output_images/undistort_07.jpg"> |
|3. Combined thresholds transformed |4. Perspective transformed to birds-eye view |
|<img src="./output_images/threshold_07.jpg"> |<img src=./output_images/birdseye_threshold_07.jpg> |
|5. Lane pixels and line of best fit identified |6. Lane curvature and vehicle offset calculated |
|<img src="./output_images/bestfit_lanes_07.jpg"> |<img src="./output_images/overlay_07.jpg"> |
|7. Lane boundaries, curvature and vehicle offset overlayed |8. Project video processed |
|<img src="./output_images/final_00.jpg"> |<img src="./output_videos/ALL_project_video.jpg"> |



## [Rubric Points](https://review.udacity.com/#!/rubrics/571/view)

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup 


### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first section of the IPython notebook __P2.ipynb__ and __calibrate_camera.py__ and __distortion.py__ python files. 

__Object Points__ are the (x, y, z) coordinates of the chessboard corners and assumes the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image. `objp` is a replicated array of coordinates and `objpoints` is appended every time all chessboard corners are detected in a test image.  __Image Points__ will be appended with the (x, y) pixel position of each of the corners in the image plane for each successful chessboard detection.  

Output `objpoints` and `imgpoints` are used to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  The Distortion class which includes `cv2.undistort()` as a class method was applied to one of the camera calibration images with the below result.
<br/>
<img src="./camera_cal/undistort20.jpg" width=40% height=40%>
<br/>
*A full set of undistorted camera calibration images are available here:* __./camera_cal/undistort*.jpg__
<br/>


### Pipeline (single images)

#### 2. Provide an example of a distortion-corrected image.

The code for this step is in the second section of the IPython notebook __P2.ipynb__, __calibrate_camera.py__ and __distortion.py__ python file.

The matrix and distortion coefficients calculated in step 1 (camera calibration using chessboard images) are stored in a pickle file __./camera_cal/wide_dist_pickle.p__. The Distortion class includes "cv2.undistort()" as a class method and when instantiated and applied to images in folder __test_images__ obtained the following results.
<br/>
<img src="./test_images/straight_lines1.jpg" width=40% height=40%>
<img src="./output_images/undistort_00.jpg" width=40% height=40%>
<br/>
*A full set of undistorted __test_images__ are available here:*  
__./output_images/undistort_*.jpg__  
<br/>

#### 3. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

The code for this step is in the third section of the IPython notebook __P2.ipynb__ and __combined_thresholds.py__ python file.
A combination of gradient threshold and color threshold functions were applied to generate a binary image in which lines could be more easily identified. A combination of transforms were made using absolute Sobel gradient threshold on the X and Y gradients, Saturation threshold on the S channel of HLS colorspace and  Red threshold on the R channel or RGB colorspace. Through experimentation Magnitude and Direction gradient threshold transforms were found to be ineffective. Here are some examples of my output from this step. 
<br/>
<img src="./output_images/threshold_00.jpg" width=40% height=40%>
<img src="./output_images/threshold_01.jpg" width=40% height=40%>
<img src="./output_images/threshold_06.jpg" width=40% height=40%>
<img src="./output_images/threshold_07.jpg" width=40% height=40%>
<br/>
*A full set of threshold transformed __test_images__ are available here:* 
__./output_images/threshold_*.jpg__  
<br/>

#### 4. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for this step is in the fourth section of the IPython notebook __P2.ipynb__ and __birdseye.py__. 

My perspective transform uses a hard coded points from a straight line view of the road __./test_images/straight-line1.jpg__ to a top-down perspective birds-eye view which were then verified by outputting the resulting to screen and adjusted according.

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 600, 450      | 200, 0        | 
| 700, 450      | 1000, 0       |
| 1020, 660     | 1020, 660     |
| 210, 720      | 210, 720      |
<br/>
<img src="./output_images/birdseye_threshold_00.jpg" width=40% height=40%>
<img src="./output_images/birdseye_threshold_07.jpg" width=40% height=40%>
<br/>
*A full set of birds-eye perspective transforms are available here:* 
__./output_images/birdseye_threshold_*.jpg__  
<br/>

#### 5. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

The code for this step is in the fifth section of the IPython notebook "P2.ipynb". 
Starting with the warped images that have been undistorted and perspective transformed to top-down view in grayscale.
The lower half of the image is selected and a histogram analysis of left to right view of the image to find peaks of active (white) pixel destiny.
Mid-points of left and right side of the image are marked as starting points then a series of small windows are drawn from bottom to top of image with a boundary line. Then active (white) pixels within the window are identified and added to list of left-side and right-side pixels. Then the next window is scanned for pixels and if is above a minimum then the window is re-centered on the current position and the active pixels added to the left-side and right-side lists.
The lists of left-side and right-side pixels are then passed to the polyfit() function to identify best fit polynomial function.
Then left-side pixels are painted red and right-side painted blue and best-fit polynomial line is drawn across the images.

<img src="./output_images/warped+lanes_00.jpg.jpg" width=40% height=40%>
<img src="./output_images/warped+lanes_01.jpg" width=40% height=40%>

#### 6. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

The code for this step is in the sixth section of the IPython notebook "P2.ipynb". 
The warped images are passed to function measure_curvature_real() which in turn calls fit_polynomial() and returns the lists of left-side and right-side pixels which are used to calculate the curvature in metres and the vehicle bias.

output_images/warped_00.jpg
Left:  9072.60 m   Right:  13933.05 m
Vehicle Bias:  0.0370 

<img src="./output_images/warped+lanes_00.jpg" width=40% height=40%>
<img src="./output_images/warped+lanes_01.jpg" width=40% height=40%>

#### 7. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The code for this step is in the seventh section of the IPython notebook "P2.ipynb". 

Function overlay() takes the lists of pixels that fit the left-side and right-side curvature lines, plots them back on the undistorted images and prints the curvatures and vehicle bias. Here is an example of my results on a test image:
<img src="./output_images/overlay_00.jpg.jpg" width=40% height=40%>
<img src="./output_images/overlay_01.jpg" width=40% height=40%>

---

### Pipeline (video)

#### 8. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

The code for this step is in the eighth section of the IPython notebook "P2.ipynb". 
Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 9. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Quite a few!!! Here's where I got stuck.
(3) Combining gradient and color transforms to show respective pixels on blue and green channels on the same image
(5) Getting the pixels to show red and blue and then drawing the line of best fit on top
(7) Getting the curvatures and overlays to display on the correct test_images; I had a number of isssues with lists getting out of order. Getting the pipeline function to run through all the main functions top to bottom in order.
(8) Processing the video; does not seem to work on my local Jupyter/Conda install

After 4 or 5 days trying to get my own code running, I reference/re-used a lot of the code here:

https://github.com/waterwheel31/SD_advanced_lane_finding/blob/master/Advanced_Lane_Line_Detection.ipynb


