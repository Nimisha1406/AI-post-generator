import redis
from rq import Queue

redis_connection = redis.Redis(host="localhost", port=6379, db=0)


otp_queue = Queue("otp", connection=redis_connection)
