import code,sys
from pgwrap import db as pgwrap


if __name__ == '__main__':
    print("aa")
    print(pgwrap)
    db = pgwrap.connection()
    code.interact(local=locals())
