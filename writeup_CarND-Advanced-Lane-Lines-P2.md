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
|<img src="./output_images/lanes_07.jpg"> |<img src="./output_images/curvature_07.jpg"> |
|7. Lane boundaries, curvature and vehicle offset overlayed |8. Project video processed |
|<img src="./output_images/final_07.jpg"> |<img src="./output_videos/ALL_project_video.jpg"> |



## [Rubric Points](https://review.udacity.com/#!/rubrics/571/view)

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup 


### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first section of the IPython notebook __P2.ipynb__ and __calibrate_camera.py__ and __distortion.py__. 

Camera calibration is done by loading the calibration images at __camera_cal/calibrate*.jpg__ and running grayscale versions through _cv2.findChessboardCorners()_. Corners are drawn on these images using _cv2.drawChessboardCorners()_ and saved as output to __camera_cal/corners*.jpg__.  *objpoints* and *imgpoints* arrays are passed to _cv2.calibrateCamera()_ which returns the distortion coefficients and matrix needed to undistort the image.  Distortion matrix and coefficients are stored in a pickle file so that they can be re-used throughout the project to undistort images. This is done by instantiating a __Distortion__ object from the the pickle file and calling __undistort()__ which uses _cv2.undistort()_ to undistort the image. An example camera calibration chessboard image that have been undistorted by loading the Distortion object and calling __undistort()__ is shown below. 
<br/>
<img src="./camera_cal/undistort20.jpg" width=40% height=40%>
<br/>
*A full set of undistorted camera calibration images are available here:* **./camera_cal/undistort\*.jpg**
<br/>


### Pipeline (single images)

#### 2. Provide an example of a distortion-corrected image.

The code for this step is in the second section of the IPython notebook __P2.ipynb__, __calibrate_camera.py__ and __distortion.py__.

Here is an example of __test_images/straight_lines1.jpg__ undistorted by loading the Distortion class object and calling __undistort()__ method. Distortion class loads the camera calibration matrix and distortion coefficients from the pickle file as explained above.
<br/>
<img src="./test_images/straight_lines1.jpg" width=40% height=40%>
<img src="./output_images/undistort_00.jpg" width=40% height=40%>
<br/>
*A full set of undistorted test_images are available here:* **./output_images/undistort_\*.jpg**
<br/>

#### 3. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

The code for this step is in the third section of the IPython notebook __P2.ipynb__ and __combined_thresholds.py__.
This code applies multiple gradient and thresholding transformations to the test_images.   

__Sobel gradient thesholding in X and Y directions__  
Sobel gradient thresholding was used to detect changes in pixel density in the horizontal and vertical directions. 

__Sobel gradient magnitude thresholding__  
This was not used in the submitted version as it did not offer any additional clarity over X and Y gradient thresholding.

__Sobel gradient direction thresholding__  
This was not used in the submitted version as it seemed to add a lot of additional noise in the image background.

__HLS - Saturation channel thresholding__  
After converting the RGB image to the HLS colorspace, the Saturation channel is good at detecting yellow lines.  

__RGB - Red channel thresholding__  
The red channel of the RGB image in BGR channel order is good at detecting white lines.  

After experimenting with values and different combinations, the thresholding techniques were combined using OR operators on __Grad-X, Grad-Y, Saturation__ and __Red channel__ transforms. Example results are shown below.
<br/>
<img src="./output_images/threshold_00.jpg" width=40% height=40%>
<img src="./output_images/threshold_01.jpg" width=40% height=40%>
<img src="./output_images/threshold_06.jpg" width=40% height=40%>
<img src="./output_images/threshold_07.jpg" width=40% height=40%>
<br/>
*A full set of threshold transformed test_images are available here:* **./output_images/threshold_\*.jpg**
<br/>

#### 4. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for this step is in the fourth section of the IPython notebook __P2.ipynb__ and __birdseye.py__. 

This code instantiates a BirdsEyeView object with methods **transform_to_birdseye()** and **transform_from_birdseye()** that transform the perspective of any image to or from birds-eye view by using _cv2.warpPerspective()_.  These perspective transforms use **transform_matrix()** and **inverse_transform_matrix()** methods created from a manually-defined set of source and destination polygon points and then using _cv2.getPerspectiveTransform()_ to define the actual tranformation in each direction. The source and destination points were defined by visually inspecting the initial straight line view of the road __./test_images/straight_lines1.jpg__ (which has a known perspective) and seeking to find source and destination points that transform it to a top-down view with nearly straight parallel lines. The results below show test_images transformed to birds-eye view using **birdseye.py** and then transformed using **combined_thresholds.py**.

The following source and destination points were used to feed the transform methods.
<br/>
| Source        | Destination   | 
|:-------------:|:-------------:| 
| 600, 450      | 200, 0        | 
| 700, 450      | 1000, 0       |
| 1020, 660     | 1020, 660     |
| 210, 720      | 210, 720      |
<br/>
<img src="./test_images/straight_lines1.jpg" width=40% height=40%>
<img src="./output_images/birdseye_threshold_00.jpg" width=40% height=40%>
<br/>
*A full set of birds-eye perspective and threshold transformed images are available here:* **./output_images/birdseye_threshold_\*.jpg**
<br/>

#### 5. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

The code for this step is in the fifth section of the IPython notebook __P2.ipynb__ and __detect.py__ ,__lanes.py__, __lane.py__ , __bestfit.py__. 
This step begins with an image that has already been undistorted and transformed using combined threshold and birds-eye perspective functions.

In **detect.py** lower half of the image is selected and a histogram analysis is performed on the  left to right view to find peaks of active (white) pixel destiny. Mid-points of the left and right sides of the image are marked as starting points then a series of small windows are drawn from bottom to top of image with a boundary line. For every window, active (white) pixels are identified and added to the lists of left-side and right-side pixels and then the next window is scanned for pixels. If the length of the left-side and right-side pixel arrays are above a minimum then the window is re-centered on their current positions. And then the active pixels are added to the left-side and right-side lists. The lists of left-side and right-side pixels are used to instantiate left-side and right-side Lane objects (and a Lanes object) which are cached for subsequent usage. 

Then in **bestfit.py** for each lanes_image, wih PixelCalculation objects of the left and right Lane objects call functions *np.polyfit()*, *np.poly1d()* and *np.polyder()* in turn to find the best fit polynomial line which is then plotted on top of the left and right lane lines and colored yellow using *np.linspace()*, *cv2.polylines()* and *cv2.addWeighted()*.
<br/>
<img src="./output_images/windows_00.jpg" width=40% height=40%>
<img src="./output_images/lanes_00.jpg" width=40% height=40%>
<br/>
*A full set of images with lane pixels identifed and best-fit line are shown in the P2.ipynb notebook and are also available here:* **./output_images/lanes_\*.jpg**
<br/>

#### 6. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

The code for this step is in the sixth section of the IPython notebook __P2.ipynb__ and __detect.py__, __lanes.py__, __lane.py__, __lanes_average.py__. 
__Lane curvature__  
Lane curvature is determined using the following curvature formula: 

fit = np.polyfit(xs, ys) # using the xs and ys found during detection  
p   = np.poly1d(fit)     # polynomial helper function  
p1  = np.polyder(p)      # first derivative of our polynomial  
p2  = np.polyder(p, 2)   # second derivative of our polynomial  

y is the point at which you'd like to find the curvature   
__((1 + (p1(y)*2))*1.5) / np.absolute(p2(y))__  
These calculations are performed inside lane.py.  

__Vehicle offset position__  
Assuming the camera is mounted in the center of the car, the vehicle offset position can be calculated by measuring the distance from the center of the lane to the center of the image.

Left lane curvature, right lane curvature and vehicle offset position from center were calculated. Examples for two test_images are shown here.
<br/>
| Test image: | ./test_images/straight_lines1.jpg |
|---|---|
|Left curvature:  4103.6516 m |
|Right curvature:  1287.9599 m |
|Vehicle offset:  -0.1752 m |
<br/> 
| Test image: | ./test_images/test6.jpg |
|---|---|
| Left curvature: | 578.3859 m |
| Right curvature: | 700.0287 m |
| Vehicle offset: | 0.1307 m |
<br/> 
*A full set of lane curvature and vehicle offset calculations are shown in the P2.ipynb notebook.

#### 7. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The code for this step is in the seventh section of the IPython notebook __P2.ipynb__ and __pipeline.py__, __overlay.py__. 

**pipeline.py** combines all the steps described above and then calls **overlay.py** to overlay a polygon marking the lane and to overlay text which shows the left and right lane curvatures and vehicle offset from the centre of the lane.

Here is an example of my results on test_images *straight_lines1.jpg* and *test6.jpg*:
<br/>
<img src="./output_images/final_00.jpg" width=40% height=40%>
<img src="./output_images/final_07.jpg" width=40% height=40%>
<br/>
*A full set of test_images with lane overlays plus left and right lane curvature and vehicle offset are shown in P2.ipynb notebook and are also available here:* **./output_images/final_\*.jpg**
<br/>

---

### Pipeline (video)

#### 8. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

The code for this step is in the eighth section of the IPython notebook "P2.ipynb". 
Here's a link to my video result. (./output_videos/ALL_project_video.mp4)

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


