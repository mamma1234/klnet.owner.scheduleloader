import config
import time
from scheduleloader.parser import distributing
import datasource
import shutil
import os
import logging
import logging.handlers
# from scheduleloader.parser.feo import feo_excelread
# from pgwrap import db as pgwrap


# def connection():
#     conn = pgwrap.connection(url='postgres://dev:dev@172.19.1.22:5432/dev')
#     print(conn)


# logging.basicConfig(filename ='./log/test.log', level=logging.DEBUG)


def work():

    logger = logging.getLogger("processing")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s[%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fileHandler = logging.FileHandler(f"{config._path_log}{os.path.sep}log.log")
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)


    # pool = datasource.simpleconnectionpool()
    filepath = ""
    filename = ""
    while True:

        try:

            print("size:", config._queue.qsize())
            # for i in range(5):
            filepath = config._queue.get()
            filename = os.path.basename(filepath)
            # print(obj)
            print('----------------------------------------------------------')
            logger.debug("filepath>>" + filepath)
            userclass = distributing.inspection(filepath)
            print("class:",userclass)
            # if userclass == []:
            #     print("class:",userclass)
            if userclass is not None:
                obj = userclass(filepath)
                data = obj.parsing()
                
                # print(data)

                param = obj.migration(data)

                logger.debug(param)

                # sql = """insert into own_vsl_sch_route(line_code, vsl_name, voyage, route_seq, route_code, eta) 
                #             values (%(line_code)s,%(vessel)s,%(voy)s,%(seq)s,
                #                     (select iso_port_code from own_vsl_sch_iso_port_code 
                #                         where line_code = %(line_code)s and port_name = %(port)s),
                #                     %(date)s)"""

                # sql = """with upd as (update own_vsl_sch_route 
                #                     set route_code = (select iso_port_code from own_vsl_sch_iso_port_code 
                #                                         where line_code = %(line_code)s and port_name = %(port)s)
                #                         , eta = %(date)s
                #                     where  line_code = %(line_code)s and vsl_name = %(vessel)s and  voyage = %(voy)s and route_seq = %(seq)s
                #                     returning line_code, vsl_name, voyage, route_seq),
                #                     ins as (select where not exists (select * from upd))
                #                     insert into own_vsl_sch_route (line_code, vsl_name, voyage, route_seq, route_code, eta) select * from ins
                # """

                # sql = """insert into own_vsl_sch_route(line_code, vsl_name, voyage, route_seq, route_code, eta, ts_yn) 
                #             values (trim(%(line_code)s),trim(%(vessel)s),trim(%(voy)s),%(seq)s,
                #                     (select iso_port_code from own_vsl_sch_iso_port_code 
                #                         where line_code = trim(%(line_code)s) and port_name = trim(%(port)s)),
                #                     trim(%(date)s), 'N')
                #         on conflict(line_code, vsl_name, voyage, route_seq)
                #         do update set route_code = (select iso_port_code from own_vsl_sch_iso_port_code 
                #                                         where line_code = trim(%(line_code)s) and port_name = trim(%(port)s))
                #                         , eta = trim(%(date)s)"""

                

                # sql = f"""insert into own_vsl_sch_route_list(line_code, vsl_name, voyage, route_date, route_code, route_name, ts_yn, insert_user) 
                #             values (trim(%(line_code)s),trim(%(vessel)s),trim(%(voy)s),trim(%(date)s),
                #                     COALESCE((select iso_port_code from own_vsl_sch_iso_port_code 
                #                                 where line_code = trim(%(line_code)s) and port_name = trim(%(port)s)),'None'),
                #                     trim(%(port)s), 'N', trim('{filename}'))
                #         on conflict(line_code, vsl_name, voyage, route_date, route_code)
                #         do update set route_name = trim(%(port)s)
                #                       , insert_user = trim('{filename}')"""

                sql = f"""insert into own_vsl_sch_route_list(line_code, vsl_name, voyage, 
                            start_route_date, start_route_code, start_route_name, 
                            end_route_date, end_route_code, end_route_name, 
                            ts_yn, insert_user, svc) 
                            values (trim(%(line_code)s),trim(%(vessel)s),trim(%(voy)s),
                                    trim(%(start_route_date)s),
                                    COALESCE((select iso_port_code from own_vsl_sch_iso_port_code 
                                                where line_code = trim(%(line_code)s) and port_name = trim(%(start_route_name)s)),'None'),
                                    trim(%(start_route_name)s), 
                                    trim(%(end_route_date)s),
                                    COALESCE((select iso_port_code from own_vsl_sch_iso_port_code 
                                                where line_code = trim(%(line_code)s) and port_name = trim(%(end_route_name)s)),'None'),
                                    trim(%(end_route_name)s), 
                                    'N', trim('{filename}'), trim(%(svc)s))
                        on conflict(line_code, vsl_name, voyage, start_route_date, start_route_code, end_route_date, end_route_code)
                        do update set start_route_name = trim(%(start_route_name)s)
                                    , end_route_name = trim(%(end_route_name)s)
                                    , insert_user = trim('{filename}')"""



                conn = datasource.connect()
                cur = conn.cursor()
                cur.executemany(sql, param)
                conn.commit()
                
                success(filepath)


                print('success')
                # datasource.executemany(pool, sql, param)

                # conn1 = database.poolconnect(pool)
                # cur = conn1.cursor()
                # cur.executemany(sql, param)
                
                # sql = """insert into own_vsl_sch_route(line_code, vsl_name, voyage, route_seq, route_code, eta)
                #     SELECT unnest(ARRAY '%(line_code)s'), unnest(ARRAY '%(vessel)s'), unnest(ARRAY '%(voy)s'),
                #             unnest(ARRAY '%(seq)s'), unnest(ARRAY '%(port)s'), unnest(ARRAY '%(date)s')
                #     """
                # line_code = [r['line_code'] for r in param]
                # vessel = [r['vessel'] for r in param]
                # voy = [r['voy'] for r in param]
                # seq = [r['seq'] for r in param]
                # port = [r['port'] for r in param]
                # date = [r['date'] for r in param]
                # database.execute(sql, locals())


            # parser = feo_excelread.parser(obj)
            # print(parser.parsing())
            # print('==========================================================')
            # if(conn):
            #     conn.insert('own_vsl_sch', {'line_code':'tes3', 'vsl_code': 'vsl_code', 'in_voyage':'1234'})


        except Exception as identifier:
            fail(filepath)
            print("Processing Exception:", identifier)
            pass
        

        time.sleep(1)


def success(filepath):
    # print(">>>>>>>", os.path.basename(filepath))
    # print(">>>>>>>", os.path.dirname(filepath))
    filename = os.path.basename(filepath)
    frompath = os.path.dirname(filepath)
    topath = frompath.replace(config._path, config._path_success)
    # shutil.move(filepath, topath)
    try:
        os.mkdir(topath)
    except Exception as identifier:
        pass
    shutil.move(filepath, f"{topath}{os.path.sep}{filename}")

    
def fail(filepath):
    # print(">>>>>>>", os.path.basename(filepath))
    # print(">>>>>>>", os.path.dirname(filepath))
    filename = os.path.basename(filepath)
    frompath = os.path.dirname(filepath)
    topath = frompath.replace(config._path, config._path_fail)
    # shutil.move(filepath, topath)
    try:
        os.mkdir(topath)
    except Exception as identifier:
        pass
    shutil.move(filepath, f"{topath}{os.path.sep}{filename}")

    print("excel parsing exception:", filepath)