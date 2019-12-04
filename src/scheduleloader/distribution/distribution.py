from scheduleloader.distribution import filequeue
import time

def work():
    while True:
        print("size:", filequeue._queue.qsize())
        # for i in range(5):
        obj = filequeue._queue.get()
        print(obj)
        time.sleep(5)