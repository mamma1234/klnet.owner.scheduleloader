from threading import Thread
from queue import Queue
import time

in_queue = Queue(1)

def run():
    print('get waiting')
    work = in_queue.get()
    print('get working')

    print('get done')
    in_queue.task_done()

thread = Thread(target=run).start()

in_queue.put(object())
print('put waiting')
in_queue.join()
print('put done')