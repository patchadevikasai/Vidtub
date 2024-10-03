import os
import moviepy.editor as mp
import requests
import time
import srt

ASSEMBLYAI_API_KEY = 'd59fe0428f694b6e934d2189870e3232'  # Replace with your AssemblyAI API key

def extract_audio_from_video(video_path, audio_path):
    """Extracts audio from the given video file."""
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio_to_srt(audio_path, srt_path):
    """Transcribes audio to SRT format using AssemblyAI."""
    # Upload audio file to AssemblyAI
    with open(audio_path, 'rb') as audio_file:
        upload_response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers={'authorization': ASSEMBLYAI_API_KEY},
            data=audio_file
        )
    
    audio_url = upload_response.json()['upload_url']
    print("Audio uploaded. URL:", audio_url)

    # Request transcription
    transcription_request = {
        'audio_url': audio_url
    }
    transcription_response = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        json=transcription_request,
        headers={'authorization': ASSEMBLYAI_API_KEY}
    )
    
    transcript_id = transcription_response.json()['id']
    print("Transcription requested. ID:", transcript_id)

    # Poll for transcription completion
    while True:
        response = requests.get(
            f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
            headers={'authorization': ASSEMBLYAI_API_KEY}
        )
        status = response.json()['status']
        if status == 'completed':
            full_text = response.json()['text']
            print("Transcription completed.")
            break
        elif status == 'failed':
            print("Transcription failed.")
            return
        time.sleep(5)  # Wait before polling again

    # Debugging: Print the full response to understand its structure
    print("Transcription response:", response.json())

    # Create SRT subtitles based on the transcription
    subtitles = []
    words_info = response.json().get('words', [])  # Use .get() to avoid KeyError

    for index, word_info in enumerate(words_info):
        # Check if 'text' key exists in word_info instead of 'word'
        if 'text' in word_info:
            start_time = word_info['start'] / 1000  # Convert ms to seconds
            end_time = word_info['end'] / 1000  # Convert ms to seconds
            subtitles.append(
                srt.Subtitle(
                    index=index + 1,
                    start=srt.timedelta(seconds=start_time),
                    end=srt.timedelta(seconds=end_time),
                    content=word_info['text']  # Use 'text' instead of 'word'
                )
            )
        else:
            print(f"Warning: 'text' key not found in word_info: {word_info}")

    # Write subtitles to SRT file
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))
    print(f"SRT file saved as {srt_path}")
def add_subtitles_to_video(video_path, srt_path, output_path):
    """Adds subtitles from an SRT file to the video, with even-indexed subtitles having a background color."""
    video = mp.VideoFileClip(video_path)
    subtitles = []

    # Read and parse the SRT file
    with open(srt_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()
        for subtitle in srt.parse(srt_content):
            subtitles.append((subtitle.start.total_seconds(), subtitle.end.total_seconds(), subtitle.content))

    # Create subtitle clips
    text_clips = []
    for index, (start, end, content) in enumerate(subtitles):
        duration = end - start  # Calculate the duration of the subtitle

        # Alternate background color based on even or odd index
        if index % 2 == 0:
            # Even-indexed subtitles with background color
            text_clip = (mp.TextClip(content, fontsize=60, font='Teko', color='black', bg_color='yellow', stroke_color="black", stroke_width=2)
                         .set_start(start)
                         .set_duration(duration)  # Correct duration is set here
                         .set_position(('center', 'bottom')))
        else:
            # Odd-indexed subtitles without background color
            text_clip = (mp.TextClip(content, fontsize=60, font='Impact', color='white')
                         .set_start(start)
                         .set_duration(duration)  # Correct duration is set here
                         .set_position(('center', 'bottom')))
        text_clips.append(text_clip)

    # Overlay subtitles on the video
    final_video = mp.CompositeVideoClip([video] + text_clips)

    # Write the final video with subtitles
    final_video.write_videofile(output_path, codec='libx264', fps=video.fps, preset='medium')


def main(video_file):
    audio_file = "extracted_audio.wav"
    srt_file = "subtitles.srt"
    output_video_file = "output.mp4"

    extract_audio_from_video(video_file, audio_file)
    transcribe_audio_to_srt(audio_file, srt_file)
    add_subtitles_to_video(video_file, srt_file, output_video_file)

    # Cleanup: Commenting out the deletion of SRT file
    if os.path.exists(audio_file):
        os.remove(audio_file)
    # The following line is commented out to keep the SRT file
    # if os.path.exists(srt_file):
    #     os.remove(srt_file)

# Example usage
video_file = 'video.mp4'
main(video_file)
