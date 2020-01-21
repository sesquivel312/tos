# todo randomize user and category IDs

from datetime import datetime

etime = int(datetime.now().timestamp())
e = (5, etime, 3)

c.execute('insert into events (user, ts, category) values ({},{},{})'.format(*e))
cn.commit()
cn.close()
