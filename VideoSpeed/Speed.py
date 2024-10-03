from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import speedx
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management with flash

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Set max file size limit (100 MB in this case)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

# Main route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')  # Renders the upload form

# Route to process the uploaded video and adjust its speed
@app.route('/process_video', methods=['POST'])
def process_video():
    try:
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part in the request')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))

        # Save the uploaded file to the server
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_path)

        # Get the speed factor from the form (default is 1.0 if not provided)
        speed_factor = float(request.form.get('speed_factor', 1.0))

        # Load and process the video using MoviePy
        video = VideoFileClip(video_path)
        adjusted_video = speedx(video, factor=speed_factor)

        # Save the processed video with a modified filename
        output_filename = f'adjusted_{file.filename}'
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        adjusted_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Close the video objects
        video.close()
        adjusted_video.close()

        # Flash success message
        flash(f'Success! The video has been processed and saved as: {output_filename}')
        return redirect(url_for('index'))

    except Exception as e:
        # Return the error message if any exception occurs
        flash(f"Error occurred: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
