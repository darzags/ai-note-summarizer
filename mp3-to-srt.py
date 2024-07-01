import whisper
import ssl
import datetime
import time

# Fix SSL context issue
ssl._create_default_https_context = ssl._create_unverified_context

def format_timestamp(seconds):
    td = datetime.timedelta(seconds=seconds)
    return str(td)[:-3].replace('.', ',')

def split_text(text, max_length=40):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

def transcribe_to_srt(mp3_file, srt_file):
    start_time = time.time()
    model = whisper.load_model("base")
    result = model.transcribe(mp3_file)

    total_segments = len(result["segments"])
    print(f"Total segments to process: {total_segments}")

    with open(srt_file, "w") as file:
        for i, segment in enumerate(result["segments"]):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            lines = split_text(text)

            # We only want two lines per timestamp
            if len(lines) > 2:
                lines = lines[:2]

            file.write(f"{i + 1}\n")
            file.write(f"{start} --> {end}\n")
            file.write("\n".join(lines) + "\n\n")

            # Print progress
            progress = (i + 1) / total_segments * 100
            print(f"Progress: {progress:.2f}% - Processing segment {i + 1}/{total_segments}")

    elapsed_time = time.time() - start_time
    print(f"Transcription saved to {srt_file}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Example usage
if __name__ == "__main__":
    mp3_file = "test.mp3"
    srt_file = "test.srt"
    transcribe_to_srt(mp3_file, srt_file)