import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from moviepy import VideoFileClip, AudioFileClip

# Image file paths
img_not_converted = "C:/Users/Cess/Desktop/File Converter/Photos/Image converter"
img_converted = "C:/Users/Cess/Desktop/File Converter/Photos/jpeg result"

# Video file paths
vid_not_converted = "C:/Users/Cess/Desktop/File Converter/Videos/Vid converter"
vid_converted = "C:/Users/Cess/Desktop/File Converter/Videos/MP4 result"

# Audio file paths
aud_not_converted = "C:/Users/Cess/Desktop/File Converter/Audios/Aud converter"
aud_converted = "C:/Users/Cess/Desktop/File Converter/Audios/MP3 result"

class FileHandler(FileSystemEventHandler):
    def file_detected(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        name, file_type = os.path.splitext(file_name)
        file_type = file_type.lower()

        if file_type in [".png", ".webp", ".bmp", ".svg", ".cr2", ".nef", ".dng", ".heic", ".heif", ".tif", ".tiff", ".cr3", ".nef", ".arw", ".avif", ".gif"]:
            self.image_convert(file_path, file_name)

        elif file_type in [".mov", ".gif", ".avi", ".mkv", ".wmv", ".m4v", ".mpg", ".mpeg", ".mts", ".m2ts", ".webm", ".flv", ".mxf"]:
            self.vid_convert(file_path, file_name)

        elif file_type in [".wav", ".flac", ".ogg", ".m4a", ".aiff", ".alac", ".aac", ""]:
            self.aud_convert(file_path, file_name)

    def image_convert(self, file_path, file_name):

    def vid_convert(self, file_path, file_name):

    def aud_convert(self, file_path, file_name):