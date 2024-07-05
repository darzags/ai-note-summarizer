import whisper
import ssl
import time

# Fix SSL context issue
ssl._create_default_https_context = ssl._create_unverified_context

# Load Whisper model
print("Loading Whisper model...")
model = whisper.load_model("medium")
print("Model loaded successfully.")

# Transcribe the audio file
print("Transcribing the audio file...")
start_time = time.time()

# Show progress (sort of)
print("Progress: 0%")
result = model.transcribe("test.mp3", verbose=True)
end_time = time.time()

# Show progress completion (sort of)
print("Progress: 100%")
print(f"Transcription completed in {end_time - start_time:.2f} seconds.")

# Get the segments for SRT
segments = result["segments"]

# Split long lines
def split_long_lines(text, max_length=42):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > max_length:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    lines.append(current_line)
    return lines

# Format time
def format_time(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds)) + f",{int((seconds % 1) * 1000):03d}"

# Save
print("Saving the transcribed text to an SRT file...")
with open("test.srt", "w") as file:
    index = 1
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        duration = (end_time - start_time) / len(split_long_lines(segment['text']))
        
        lines = split_long_lines(segment['text'])
        for i, line in enumerate(lines):
            start = format_time(start_time + i * duration)
            end = format_time(start_time + (i + 1) * duration)
            file.write(f"{index}\n{start} --> {end}\n{line}\n\n")
            index += 1

print("Transcription saved to test.srt")