import code,sys
from pgwrap import db as pgwrap


if __name__ == '__main__':
    print("aa")
    print(pgwrap)
    db = pgwrap.connection(url='postgres://dev:dev@172.19.1.22:5432/dev')
    # code.interact(local=locals())

    db.insert('own_vsl_sch', {'line_code':'tes0', 'vsl_code': 'vsl_code', 'in_voyage':'1234'})
    db.insert('own_vsl_sch', {'line_code':'tes1', 'vsl_code': 'vsl_code', 'in_voyage':'1234'})
    db.insert('own_vsl_sch', {'line_code':'tes2', 'vsl_code': 'vsl_code', 'in_voyage':'1234'})

