from moviepy.editor import VideoFileClip
from pipeline import Pipeline
import numpy as np

clip1 = VideoFileClip('project_video.mp4')
video_output = './output_videos/project_video.mp4'

def process_video_pipeline(clip1):
    white_clip = clip1.fl_image(pipeline.process_image_pipeline).subclip(0,5) #NOTE: this function expects color images!!
    # white_clip = clip1.fl_image(pipeline.process_image_pipeline)
    white_clip.write_videofile(video_output, audio=False)


if __name__ == "__main__":
    np.seterr(all='ignore')
    pipeline = Pipeline()

    white_clip = clip1.fl_image(pipeline.process_image_pipeline).subclip(0,5) #NOTE: this function expects color images!!
    # white_clip = clip1.fl_image(pipeline.process_image_pipeline)
    white_clip.write_videofile(video_output, audio=False)
