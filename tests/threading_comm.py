import threading
from queue import Queue
import sys
def creator(data, q):
    """
    생산자 : 쓰레드간 데이터 전송 예제
    """
    print('Creating data and putting it on the queue')
    print('\n')
    for item in data:
        evt = threading.Event()
        q.put((item, evt))
        print('Waiting for data to be doubled')
        evt.wait()


def consumer(q):
    """
    소비자 : 쓰레드간 데이터 전송 예제
    """
    while True:
        data, evt = q.get()
        print('Receive Original Data : {}'.format(data))
        processed = data * 5
        print('Receive Processed Data : {}'.format(processed))
        print('\n')
        evt.set()
        q.task_done()


if __name__ == '__main__':

    try:
        print("start")
        q = Queue()
        data = [7, 14, 39, 59, 77, 1, 109, 99, 167, 920, 1035]
        thread_one = threading.Thread(target=creator, args=(data, q))
        thread_two = threading.Thread(target=consumer, args=(q,))
        # thread_one.daemon = True
        # thread_two.daemon = True
        thread_one.start()
        thread_two.start()
        q.join()
    except KeyboardInterrupt:
        # thread_one._stop()
        # thread_two._stop()
        print("KeyboardInterrupt")
        # Ctrl+C 입력시 예외 발생
        #sys.exit() #종료
