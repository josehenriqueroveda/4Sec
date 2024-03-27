import psutil
import time

TASKS_TO_KILL = set(["obs-ffmpeg-mux.exe", "obs64.exe"])

while True:
    for task in TASKS_TO_KILL:
        # Check if the task is running
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] == task:
                # Kill the task
                psutil.Process(proc.pid).kill()
                break

    time.sleep(0.5)
