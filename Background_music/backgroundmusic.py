from moviepy.editor import VideoFileClip, AudioFileClip

# Paths to the input video and audio files
video_path = "src/inputvideo.mp4"
audio_path = "background_music.mp3"
output_path = "video_with_background_music.mp4"

# Load the video
video = VideoFileClip(video_path)
print("Video Duration:", video.duration)  # Print video duration

# Load the audio (background music)
background_audio = AudioFileClip(audio_path)

# Ensure the audio does not exceed the video duration
if background_audio.duration > video.duration:
    background_audio = background_audio.subclip(0, video.duration)

# Set the audio to the video
video_with_music = video.set_audio(background_audio)

# Write the output video file with background music
video_with_music.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video.fps)

# Close the video and audio files
video.close()
background_audio.close()
