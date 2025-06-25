import time
from pathlib import Path
from redis import Redis

redis_conn = Redis(host='localhost', port=6379, db=0)
QUEUED_SET = "queued_files"

def process_file(file_path: str):
    print(f"[WORKER] Processing: {file_path}")
    time.sleep(2)  # simulate processing
    Path(file_path + ".done").touch()
    redis_conn.srem(QUEUED_SET, file_path)
    print(f"[WORKER] Done: {file_path}")

