import psutil
import time

def check_system_health(cpu_threshold=80, memory_threshold=80, disk_threshold=90):
    """
    Monitors CPU, Memory, and Disk usage and prints alerts if thresholds are exceeded.
    Parameters:
        cpu_threshold (int): CPU usage percentage that triggers alert.
        memory_threshold (int): Memory usage percentage that triggers alert.
        disk_threshold (int): Disk usage percentage that triggers alert.
    """
    
    # CPU Usage
    current_cpu = psutil.cpu_percent(interval=1)
    print(f"Current CPU Usage: {current_cpu}%")
    if current_cpu > cpu_threshold:
        print("CPU Alert: Usage is above threshold!")
    else:
        print("CPU is under threshold.")

    # Memory Usage
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    print(f"Current Memory Usage: {memory_percent}%")
    if memory_percent > memory_threshold:
        print("Memory Alert: Usage is above threshold!")
    else:
        print("Memory is under threshold.")

    # Disk Usage (Root / partition)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    print(f"Current Disk Usage: {disk_percent}%")
    if disk_percent > disk_threshold:
        print("Disk Alert: Usage is above threshold!")
    else:
        print("Disk is under threshold.")


if __name__ == "__main__":
    while True:
        check_system_health(cpu_threshold=80, memory_threshold=80, disk_threshold=90)
        print("-" * 50)
        time.sleep(10)  # check every 10 seconds
