import filequeue
import time
from scheduleloader.parser import distributing
# from scheduleloader.parser.feo import feo_excelread
# from pgwrap import db as pgwrap


# def connection():
#     conn = pgwrap.connection(url='postgres://dev:dev@172.19.1.22:5432/dev')
#     print(conn)

def work(conn):
    while True:
        print("size:", filequeue._queue.qsize())
        # for i in range(5):
        filename = filequeue._queue.get()
        # print(obj)
        print('----------------------------------------------------------')
        print(filename)
        userclass = distributing.inspection(filename)
        print(userclass)
        if userclass is not None:
            obj = userclass(filename)
            data = obj.parsing()
            # print(data)
        # parser = feo_excelread.parser(obj)
        # print(parser.parsing())
        print('==========================================================')
        # if(conn):
        #     conn.insert('own_vsl_sch', {'line_code':'tes3', 'vsl_code': 'vsl_code', 'in_voyage':'1234'})


        time.sleep(5)

