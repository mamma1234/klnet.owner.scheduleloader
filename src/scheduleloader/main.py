from threading import Thread
import sys
import time
import mailling
import polling
import processing
# from pgwrap import db as pgwrap


if __name__ == '__main__':
    # path = "C:\\KLNET\\SCH"
    
    # main_start = True

    try:
    # polling.monitoring(path)

    
        mailling_work = Thread(target=mailling.work)
        mailling_work.daemon=True
        mailling_work.start()
 
    
        polling_work = Thread(target=polling.work)
        polling_work.daemon=True
        polling_work.start()
 
        # conn = pgwrap.connection(url='postgres://dev:dev@172.19.1.22:5432/dev')

        # process_work = Thread(target=processing.work, args=(conn,))
        process_work = Thread(target=processing.work)
        process_work.daemon=True
        process_work.start()
        while True:
            # print("size:", filequeue._queue.qsize())
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("stop process")
