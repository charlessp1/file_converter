import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from moviepy import VideoFileClip, AudioFileClip
from constants import FILE_EXTENSIONS, DIRECTORIES_TO_CLEAN

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
    def on_created(self, event):
        time.sleep(5)
        if event.is_directory:
            return
        file_path = event.src_path.replace("\\", "/")
        file_name = os.path.basename(file_path)
        name, file_type = os.path.splitext(file_name)
        file_type = file_type.lower()

        if file_type in FILE_EXTENSIONS["Images"] and img_not_converted in file_path:
            if file_type == ".jpg" or file_type == ".jpeg":
                print("File is already in JPEG format")
                return
            self.image_convert(file_path, f"converted_{name}")

        elif file_type in FILE_EXTENSIONS["Videos"] and vid_not_converted in file_path:
            if file_type == ".mp4":
                print("File is already in MP4 format")
                return
            self.vid_convert(file_path, f"converted_{name}")

        elif file_type in FILE_EXTENSIONS["Audios"] and aud_not_converted in file_path:
            if file_type == ".mp3":
                print("File is already in MP3 format")
                return
            self.aud_convert(file_path, f"converted_{name}")

        else:
            print(f"Unsupported file type: {file_type}")

    def image_convert(self, file_path, name):
        time.sleep(1)
        converted_jpeg = os.path.join(img_converted, f"{name}.jpg")
        with Image.open(file_path) as photo:
            photo.convert("RGB").save(converted_jpeg)
        print(f"Successfully converted {name} to JPEG!")

    def vid_convert(self, file_path, name):
        time.sleep(1)
        converted_mp4 = os.path.join(vid_converted, f"{name}.mp4")
        with VideoFileClip(file_path) as clip:
            width, height = clip.size
            if width % 2 !=0 or  height % 2 != 0:
                print(f"Fixing video dimensions of {name}")
                width = width - (width % 2)
                height = height - (height % 2)
                new_clip = clip.resize(size=(width, height))
                new_clip.write_videofile(converted_mp4, codec="libx264", audio_codec="aac", fps=clip.fps, remove_temp=False)
                new_clip.close()

            else:
                clip.write_videofile(converted_mp4, codec="libx264", audio_codec="aac", fps=clip.fps, remove_temp=False)
                
        print(f"Successfully converted {name} to MP4!")

    def aud_convert(self, file_path, name):
        time.sleep(1)
        converted_mp3 = os.path.join(aud_converted, f"{name}.mp3")
        with AudioFileClip(file_path) as audio:
            audio.write_audiofile(converted_mp3)
        print(f"Successfully converted {name} to MP3!")

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, img_not_converted, recursive=False)
    observer.schedule(event_handler, vid_not_converted, recursive=False)
    observer.schedule(event_handler, aud_not_converted, recursive=False)
    print("Initializing clean up for TEMP FILES...")
    for directory in DIRECTORIES_TO_CLEAN:
        for filename in os.listdir(directory):
            if "TEMP_MPY" in filename:
                full_path = os.path.join(directory, filename)
                os.remove(full_path)
                print(f"Cleaned up {filename}")
    print("Clean up complete!")
    observer.start()                       # watches the folders and looks for files to be converted
    print("Starting file converter")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ask_delete = input("Would you like to delete the previous leftover file/s? (y/n): ")
        if ask_delete.lower() == "y":
            ask_which = input("Which files would you like to delete? (images/videos/audios/all): ")
            if ask_which.lower() == "images":
                for images in os.listdir(img_not_converted):
                    os.remove(os.path.join(img_not_converted, images))

            elif ask_which.lower() == "videos":
                for videos in os.listdir(vid_not_converted):
                    os.remove(os.path.join(vid_not_converted, videos))

            elif ask_which.lower() == "audios":
                for audios in os.listdir(aud_not_converted):
                    os.remove(os.path.join(aud_not_converted, audios))

            elif ask_which.lower() == "all":
                for images in os.listdir(img_not_converted):
                    os.remove(os.path.join(img_not_converted, images))
                for videos in os.listdir(vid_not_converted):
                    os.remove(os.path.join(vid_not_converted, videos))
                for audios in os.listdir(aud_not_converted):
                    os.remove(os.path.join(aud_not_converted, audios))

            else:
                print("Please enter a valid input: img/vid/aud/all.")
                
        observer.stop()
        print("Shutting down file converter...")
    observer.join()
    print("File converter shut down")