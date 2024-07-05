import psutil

def print_cpu_threads():
    cpu_count = psutil.cpu_count(logical=True)
    print(f"Total CPU Threads: {cpu_count}")
