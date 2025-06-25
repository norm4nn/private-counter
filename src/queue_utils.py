from redis import Redis
from rq import Queue
from workers import process_file

redis_conn = Redis(host='localhost', port=6379, db=0)
q = Queue('image_processing', connection=redis_conn)
QUEUED_SET = "queued_files"

def is_file_queued(file_path: str) -> bool:
    return redis_conn.sismember(QUEUED_SET, file_path)

def mark_file_as_queued(file_path: str):
    redis_conn.sadd(QUEUED_SET, file_path)

