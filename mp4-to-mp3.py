import sys
from moviepy.editor import VideoFileClip

def convert_mp4_to_mp3(input_file, output_file):
    try:
        # Load the video file
        video = VideoFileClip(input_file)
        # Extract the audio and save it as an MP3 file
        video.audio.write_audiofile(output_file, codec='mp3')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        video.close()

# Example usage
if __name__ == "__main__":
    input_file = "test.mp4"
    output_file = "test.mp3"
    convert_mp4_to_mp3(input_file, output_file)
