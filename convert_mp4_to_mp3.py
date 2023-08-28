from moviepy.editor import VideoFileClip
import os

videos_path = r"D:\Github\DownloadResources\vids"
mp3_path = r"D:\Github\DownloadResources\music"

for file in os.listdir(videos_path):
    if file.endswith("mp4"):
        video = VideoFileClip(os.path.join(videos_path, file))
        video.audio.write_audiofile(os.path.join(mp3_path, file.replace("mp4", "mp3")))
