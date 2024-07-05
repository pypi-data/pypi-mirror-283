import psutil

def cpu_threads():
    cpu_count = psutil.cpu_count(logical=True)
    print(f"Total CPU Threads: {cpu_count}")
