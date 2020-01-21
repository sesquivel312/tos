import pathlib

import tos.lib as lib

data_path = pathlib.Path('data')
db = data_path.joinpath('db.sqlite')

cn = lib.get_sqlite_conn(db)

holder = lib.get_holder(cn)[0]


print('{} has the token for {}'.format(holder[0], holder[2]))

