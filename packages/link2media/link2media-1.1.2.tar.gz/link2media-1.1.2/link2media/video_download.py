import os
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor

def download_videos(file_path, output_folder="LAION Debate", num_threads=16):
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

    print(f"DOWNLOADED VIDEOS: {downloaded_count}")
    print("All videos downloaded successfully!")


