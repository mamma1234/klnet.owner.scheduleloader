from scheduleloader.polling import polling
from scheduleloader.distribution import distribution
from threading import Thread
import sys
import time



if __name__ == '__main__':
    path = "C:\\KLNET\\SCH"
    # main_start = True

    try:
    # polling.monitoring(path)
        thread_polling = Thread(target=polling.monitoring, args=(path, ))
        thread_polling.daemon=True
        thread_polling.start()
        thread_distribution = Thread(target=distribution.work)
        thread_distribution.daemon=True
        thread_distribution.start()
        while True:
            # print("size:", filequeue._queue.qsize())
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("stop process")
