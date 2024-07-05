import os
import logging
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor
import ffmpeg

def high_quality_audio(file_path, output_folder="LAION Debate", num_threads=None):
    with open(file_path, 'r') as file:
        links = file.readlines()

    total_links = len(links)
    print(f"TOTAL LINKS: {total_links}")
    downloaded_count = 0

    os.makedirs(output_folder, exist_ok=True)

    def process_link(link):
        try:
            yt = YouTube(link.strip())
            video_stream = yt.streams.filter(file_extension='mp4').first()
            if video_stream:
                video_stream.download(output_path=output_folder)  # Set output folder for video

                video_file_path = os.path.join(output_folder, video_stream.default_filename)
                audio_file_path = os.path.join(output_folder, video_stream.default_filename[:-4] + ".mp3")  # Adjust audio file path

                # Use ffmpeg to extract audio and save it as an MP3 file
                ffmpeg.input(video_file_path).output(audio_file_path, acodec='mp3').run()

                os.remove(video_file_path)

                return True, None
            else:
                return False, f"No suitable stream found for link {link.strip()}"

        except Exception as e:
            return False, f"Error processing link {link.strip()}: {e}"
    
    if num_threads is None:
        num_threads = os.cpu_count()
    
    print(f"NUM THREADS: {num_threads}")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for success, message in executor.map(process_link, links):
            if success:
                downloaded_count += 1
            else:
                print(message)

    print(f"DOWNLOADED AUDIO {downloaded_count}")
    print("All videos downloaded and converted successfully!")
