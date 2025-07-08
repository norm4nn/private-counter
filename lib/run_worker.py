from rq import Worker, Queue
from redis import Redis
from workers import process_file

redis_conn = Redis(host='localhost', port=6379)
queue = Queue('image_processing', connection=redis_conn)
worker = Worker(queues=[queue], connection=redis_conn)
worker.work()