from moviepy.editor import VideoFileClip

# Path to the video file
video_path = "inputvideo.mp4"
output_path = "trimmed_video.mp4"

# Load the video
video = VideoFileClip(video_path)

# Define start and end time for trimming (in seconds)
start_time = 10  # Start trimming at 10 seconds
end_time = 30    # End trimming at 30 seconds

# Trim the video using subclip(start_time, end_time)
trimmed_video = video.subclip(start_time, end_time)

# Write the trimmed video to a new file
trimmed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Close the video files
video.close()
trimmed_video.close()
