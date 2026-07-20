from rq import SimpleWorker
from redis_queue import otp_queue, redis_connection

worker = SimpleWorker([otp_queue], connection=redis_connection)


print("OTP worker running...")

worker.work()
