import time
from pathlib import Path
from redis import Redis
from rq import Queue
from workers import process_file

# Configuration
WATCH_DIR = Path("/mnt/ncdata/admin/files/Photos")
CHECK_INTERVAL = 5  # seconds between scans
QUEUED_SET = "queued_files"

# Redis connection and queue setup
redis_conn = Redis(host='localhost', port=6379, db=0)
q = Queue('image_processing', connection=redis_conn)

def is_file_queued(file_path: str) -> bool:
    return redis_conn.sismember(QUEUED_SET, file_path)

def mark_file_as_queued(file_path: str):
    redis_conn.sadd(QUEUED_SET, file_path)

def process_directory():
    for file in WATCH_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            done_marker = file.with_name(file.name + ".done")

            if done_marker.exists():
                continue  # already processed

            if is_file_queued(str(file)):
                continue  # already queued

            # Enqueue file
            job = q.enqueue(process_file, str(file))
            mark_file_as_queued(str(file))
            print(f"[QUEUE] Enqueued: {file.name} as job {job.id}", flush=True)

if __name__ == "__main__":
    print(f"[WATCHER] Watching folder: {WATCH_DIR.resolve()}", flush=True)
    while True:
        try:
            process_directory()
        except Exception as e:
            print(f"[ERROR] Exception during directory scan: {e}", flush=True)
        time.sleep(CHECK_INTERVAL)

