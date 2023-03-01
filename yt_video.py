from pytube import YouTube
from dataclasses import dataclass
from time_utils import seconds_to_time
import config


@dataclass
class VideoMetadata:
    ''' Data class for storing video metadata. '''
    title: str
    id: int
    author: str
    author_url: str
    thumbnail_url: str
    upload_date: str
    view_count: int
    options: list
    audio: list
    length: tuple


class YtVideo:
    ''' Wrapper class for retrieving video streams and downloading'''

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.url = f'www.youtube.com/watch?v={video_id}'
        self.yt = YouTube(self.url)
        self.video_options = []
        self.streams = self.yt.streams.filter(
            file_extension='mp4', adaptive=True)
        self.title = self.yt.title

    def get_options(self) -> VideoMetadata:
        ''' Returns all possible video and audio options and other metadata'''

        resolutions = set()
        framerates = set()

        # Loop for adding just the unique streams (without repeating the resolution or framerate)
        for stream in self.streams:
            if stream.mime_type == "video/mp4" and (stream.resolution not in resolutions or stream.fps not in framerates):
                self.video_options.append({
                    "resolution": stream.resolution,
                    "itag": stream.itag,
                    "fps": str(stream.fps) + 'fps',
                    "size": round(stream.filesize / 1000000, 1)
                })
                resolutions.add(stream.resolution)
                framerates.add(stream.fps)

        audio_options = self.yt.streams.filter(mime_type="audio/mp4")

        # Replacing the SD thumbnail with HD
        thumbnail_url = self.yt.thumbnail_url.replace('sddefault', 'mqdefault')

        data = VideoMetadata(id=self.video_id,
                             title=self.yt.title,
                             author=self.yt.author,
                             thumbnail_url=thumbnail_url,
                             upload_date=self.yt.publish_date.strftime(
                                 "%m.%d.%Y"),
                             view_count=self.yt.views,
                             options=self.video_options,
                             audio=audio_options,
                             author_url=self.yt.channel_url,
                             length=seconds_to_time(self.yt.length))
        return data

    def download_video_and_audio(self, itag: int) -> None:
        ''' Downloads video with provided itag and the best quality audio. '''

        filename = self.video_id + '.mp4'

        video = self.yt.streams.get_by_itag(itag)
        audio = self.yt.streams.get_audio_only()

        print('Downloading video..')
        video.download(config.VIDEO_PATH, filename=filename)
        print('Downloading audio..')
        audio.download(config.AUDIO_PATH, filename=filename)
