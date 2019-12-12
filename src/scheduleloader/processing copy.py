import config
import time
from scheduleloader.parser import distributing
import datasource
import shutil
import os
# from scheduleloader.parser.feo import feo_excelread
# from pgwrap import db as pgwrap


# def connection():
#     conn = pgwrap.connection(url='postgres://dev:dev@172.19.1.22:5432/dev')
#     print(conn)

def work():

    # pool = datasource.simpleconnectionpool()
    filepath = ""
    while True:

        try:

            print("size:", config._queue.qsize())
            # for i in range(5):
            filepath = config._queue.get()
            # print(obj)
            print('----------------------------------------------------------')
            print("filepath:",filepath)
            userclass = distributing.inspection(filepath)
            print("class:",userclass)
            if userclass is not None:
                obj = userclass(filepath)
                data = obj.parsing()
                
                # print(data)

                param = obj.migration(data)

                print("param:", param)

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

                sql = """insert into own_vsl_sch_route(line_code, vsl_name, voyage, route_seq, route_code, eta, ts_yn) 
                            values (trim(%(line_code)s),trim(%(vessel)s),trim(%(voy)s),%(seq)s,
                                    (select iso_port_code from own_vsl_sch_iso_port_code 
                                        where line_code = trim(%(line_code)s) and port_name = trim(%(port)s)),
                                    trim(%(date)s), 'N')
                        on conflict(line_code, vsl_name, voyage, route_seq)
                        do update set route_code = (select iso_port_code from own_vsl_sch_iso_port_code 
                                                        where line_code = trim(%(line_code)s) and port_name = trim(%(port)s))
                                        , eta = trim(%(date)s)"""

                conn = datasource.connect()
                cur = conn.cursor()
                cur.executemany(sql, param)
                conn.commit()
                
                # success(filepath)


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
            # fail(filepath)
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