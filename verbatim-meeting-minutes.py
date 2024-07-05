import re

# Parse SRT file
def parse_srt(srt_file):
    with open(srt_file, 'r') as file:
        content = file.read()
    
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(content)
    
    srt_data = []
    for match in matches:
        index, start, end, text = match
        srt_data.append({
            'start': start,
            'end': end,
            'text': text.replace('\n', ' ')
        })
    
    return srt_data

# Parse VTT file
def parse_vtt(vtt_file):
    with open(vtt_file, 'r') as file:
        content = file.read()
    
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n<v (.*?)>(.*?)</v>', re.DOTALL)
    matches = pattern.findall(content)
    
    vtt_data = []
    for match in matches:
        start, end, speaker, text = match
        vtt_data.append({
            'start': start.replace('.', ','),
            'end': end.replace('.', ','),
            'speaker': speaker,
            'text': text.replace('\n', ' ')
        })
    
    return vtt_data

# Match SRT and VTT data
def match_transcripts(srt_data, vtt_data):
    combined_transcript = []
    
    for vtt_entry in vtt_data:
        for srt_entry in srt_data:
            if vtt_entry['start'] <= srt_entry['start'] <= vtt_entry['end']:
                combined_transcript.append({
                    'speaker': vtt_entry['speaker'],
                    'start': vtt_entry['start'],
                    'text': srt_entry['text']
                })
                break
    
    return combined_transcript

# Group group consecutive entries
def group_by_speaker(transcript):
    grouped_transcript = []
    if not transcript:
        return grouped_transcript

    current_speaker = transcript[0]['speaker']
    current_start = transcript[0]['start']
    current_text = transcript[0]['text']

    for entry in transcript[1:]:
        if entry['speaker'] == current_speaker:
            current_text += ' ' + entry['text']
        else:
            grouped_transcript.append({
                'speaker': current_speaker,
                'start': current_start,
                'text': current_text
            })
            current_speaker = entry['speaker']
            current_start = entry['start']
            current_text = entry['text']
    
    # Append the last grouped entry
    grouped_transcript.append({
        'speaker': current_speaker,
        'start': current_start,
        'text': current_text
    })

    return grouped_transcript

# Save
def save_combined_transcript(combined_transcript, output_file):
    with open(output_file, 'w') as file:
        for entry in combined_transcript:
            file.write(f"{entry['speaker']} ({entry['start']}): {entry['text']}\n\n")  # Add an extra newline for separation

def main():
    srt_file = 'test.srt'  # Replace with your SRT file name
    vtt_file = 'test.vtt'  # Replace with your VTT file name
    output_file = 'combined_transcript.txt'
    
    srt_data = parse_srt(srt_file)
    vtt_data = parse_vtt(vtt_file)
    
    # Debugging: Print parsed SRT and VTT data
    print("Parsed SRT Data:")
    for entry in srt_data:
        print(entry)
    
    print("\nParsed VTT Data:")
    for entry in vtt_data:
        print(entry)
    
    combined_transcript = match_transcripts(srt_data, vtt_data)
    
    # Group by speaker
    grouped_transcript = group_by_speaker(combined_transcript)
    
    # Debugging: Print combined transcript data
    print("\nGrouped Transcript Data:")
    for entry in grouped_transcript:
        print(entry)
    
    save_combined_transcript(grouped_transcript, output_file)
    print(f"Combined transcript saved to {output_file}")

if __name__ == "__main__":
    main()