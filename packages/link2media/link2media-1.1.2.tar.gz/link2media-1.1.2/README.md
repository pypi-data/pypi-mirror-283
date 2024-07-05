### Introduction
link2Media is a library specifically designed to download the LAION Debate dataset. It helps researchers to download the entire LAION Debate dataset through one-line of code. Including options what format the dataset researchers want to download (.mp3, mp4) and quality of the dataset as well. 

#### Usage
You can use the library through below code
from link2media import download_audio, download_videos, high_quality_audio, cpu_threads

```Python
download_videos(file_path, output_folder="LAION Debate", num_threads=16)
high_quality_audio(file_path, output_folder="LAION Debate", num_threads=16)
print_cpu_threads()
download_audio(file_path, output_folder="LAION Debate", num_threads=16)
```

<pre>
@misc{link2Media,
  author = {tawsif ahmed},
  title = {link2Media: A Library for Downloading the LAION Debate Dataset},
  year = {2024},
  published = {\url{https://pypi.org/project/link2media/}},
  note = {Version 1.1.2}
}

</pre>