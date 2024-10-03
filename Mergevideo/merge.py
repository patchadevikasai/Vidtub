from moviepy.editor import VideoFileClip, concatenate_videoclips

# Function to merge videos
def merge_videos(video_paths, output_path):
    try:
        # Load video clips from the provided file paths
        video_clips = [VideoFileClip(path) for path in video_paths]
        
        # Concatenate the video clips
        final_clip = concatenate_videoclips(video_clips)
        
        # Write the output video file
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"Videos merged successfully! Output saved at: {output_path}")
    except Exception as e:
        print(f"Error while merging videos: {e}")

# Function to get video file paths from the user
def get_video_paths():
    video_paths = []
    num_videos = int(input("How many videos do you want to merge? "))
    
    for i in range(num_videos):
        path = input(f"Enter the path for video {i+1}: ")
        video_paths.append(path)
    
    return video_paths

# Main function to execute the merging process
if __name__ == "__main__":
    # Get input video paths from the user
    video_paths = get_video_paths()
    
    # Get the output file path
    output_path = input("Enter the output file path (e.g., 'output.mp4'): ")
    
    # Call the merge function
    merge_videos(video_paths, output_path)
