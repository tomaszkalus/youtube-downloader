import subprocess
import os
import config
from time_utils import querystring_to_time

def merge(filename, start=None, end=None):
    ''' Merges audio with video, trims it (if time marks are provided) and returns the path for the output file'''

    video_path = os.path.join(config.VIDEO_PATH, filename)
    audio_path = os.path.join(config.AUDIO_PATH, filename)
    output_path = os.path.join(config.OUTPUT_PATH, filename)

    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        return False
    
    if not (start and end):
        call = ['ffmpeg', '-y', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', output_path]
    else:
        start_time = querystring_to_time(start)
        end_time = querystring_to_time(end)
        call = ['ffmpeg','-y', '-i', video_path, '-ss', start_time, '-to', end_time, '-i', audio_path, '-ss', start_time, '-to', end_time, '-c:v', 'copy', '-c:a', 'aac', output_path]

    subprocess.call(call, shell=False)
    os.remove(video_path)
    os.remove(audio_path)

    return output_path
