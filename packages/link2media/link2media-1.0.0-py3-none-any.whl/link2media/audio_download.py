import os
from pytube import YouTube
from concurrent.futures import ThreadPoolExecutor

def download_audio(file_path, output_folder="LAION Debate", num_threads=16):
    with open(file_path, 'r') as file:
        links = file.readlines()

    total_links = len(links)
    print(f"TOTAL LINKS: {total_links}")
    downloaded_count = 0

    os.makedirs(output_folder, exist_ok=True)

    def process_link(link):
        try:
            yt = YouTube(link.strip())
            # Filter the streams to find the one with the desired audio
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                out_file = audio_stream.download(output_path=output_folder)  # Download the audio file
                # Convert to MP3
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                return True, None
            else:
                return False, f"No suitable stream found for link {link.strip()}"

        except Exception as e:
            return False, f"Error processing link {link.strip()}: {e}"
    
    print(f"NUM THREADS: {num_threads}")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for success, message in executor.map(process_link, links):
            if success:
                downloaded_count += 1
            else:
                print(message)

    print(f"DOWNLOADED VIDEOS: {downloaded_count}")
    print("All the audio files are downloaded!")


download_audio("02-05-2024-CAM.txt")
