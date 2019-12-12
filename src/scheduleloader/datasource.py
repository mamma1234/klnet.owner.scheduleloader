import psycopg2

# conn = pgwrap.connection(url='postgres://dev:dev@172.19.1.22:5432/dev')

def simpleconnectionpool():
    pool = psycopg2.pool.SimpleConnectionPool(1, 10, user="dev", password="dev", host="172.19.1.22", port="5432", database="dev")

    return pool

def poolconnect(pool):
    if(pool):
        connection = pool.getconn()
        return connection
    return None

def executemany(pool, sql, params=[]):
    with poolconnect(pool) as connection:
        with connection.cursor() as cursor:
            print(params)
            cursor.executemany(sql, params)
        


def connect():
    # connection = psycopg2.connect(host='172.19.1.22:5432', dbname='dev', user='dev', password='dev')
    connection = psycopg2.connect(host='172.19.1.22', port='5432', dbname='dev', user='dev', password='dev')
    # connection = psycopg2.connect("host=172.19.1.22 port=5432 dbname=dev user=dev password=dev")
    # connection = psycopg2.connect(url='postgres://dev:dev@172.19.1.22:5432/dev')
    # psycopg2.extras.register_hstore(connection)
    
    return connection



def execute(sql, params=[]):
    with connect() as connection:
        with connection.cursor() as cursor:
            print(params)
            cursor.execute(sql, params)


class insert_own_vsl_sch_route:
    def insert(self):
        sql = '''inset into own_vsl_sch_route(line_code, vsl_name, voyage, route_seq, route_code, eta)
            SELECT unnest(ARRAY '%(line_code)s'), unnest(ARRAY '%(vessel)s'), unnest(ARRAY '%(voy)s'),
                    unnest(ARRAY '%(seq)s'), unnest(ARRAY '%(port)s'), unnest(ARRAY '%(date)s')
            '''
