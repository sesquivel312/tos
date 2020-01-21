# todo can I use one conn/cursor - will need to pass around
# todo secure db operations (inserts, etc.)
# todo when/where close conn

from datetime import datetime
import logging
import sqlite3 as sql
import sys

logging.basicConfig(format='%(asctime)s %(message)s', filename='tos.log', level=logging.DEBUG)
log = logging.getLogger('tos')


def strtime_to_unixts(timestring, tformat='%Y-%m-%d', keep_sec=False):
    """
    convert a time string to unix timestamp, optionally including seconds, etc.

    The keep_sec param is a bool flag determining if the returned timestamp includes
    seconds (and smaller fractions of time).  Default is to remove seconds, etc.

    :param tformat: strftime time format string
    :type tformat: str
    :param timestring: date and/or time string
    :type timestring: str
    :param keep_sec: flag determines if seconds and smaller are kept
    :type keep_sec: bool
    :return: unix timestamp
    :rtype: float | int
    """

    t = datetime.strptime(timestring, '%Y-%m-%d')  # convert to datetime obj

    t = t.timestamp()  # convert to unix timestamp w/o seconds, etc.

    if not keep_sec:

        t = int(t)  # drop seconds, etc.

    return t


def get_sqlite_conn(fname='db.sqlite'):
    """
    return a python dbapi connection to sqlite db file

    by default it will try to connect to 'db.sqlite' in the current directory

    todo correct rtype as needed

    :param fname: name of sqlite db file
    :type fname: str | Path
    :return: python dbapi connection object
    :rtype: connection
    """

    return sql.connect(fname)


def db_query(conn, query=None):
    """
    run a query against a database

    :param conn: python dbapi connection object
    :param query: query to execute
    :type query: str
    :return: query results
    :rtype: list
    """

    c = conn.cursor()

    c.execute(query)

    return c.fetchall()


def add_users(names, conn):
    """
    add users to users db

    Note:
        to insert multiple records, the insert statement looks like this:

            insert into users (name) values ('name1'), ('name2'), ... ('namen')

    todo checks and return something sensible
    todo check # of records to insert
    :param conn: python dbapi connection object
    :param names: user name
    :type names: list
    :return: name added or None if fail
    :rtype: str | None
    """

    values = ''
    for name in names:
        values += "('{}'),".format(name)
    values = values.rstrip(',')  # remove the trailing comma

    q = 'insert into users (name) values {}'.format(values)
    c = conn.cursor()

    try:
        c.execute(q)
        conn.commit()
    except:
        log.warning(str(sys.exc_info()))


def add_event(event, conn):
    """
    add a token event to the events db

    :param event: tuple representing row to insert
    :type event: tuple
    :param conn: python dbapi connection object
    :return: todo return what
    """

    q = 'insert into events (user, ts, category) values ({}, {}, {})'.format(*event)
    c = conn.cursor()

    try:
        c.execute(q)
        conn.commit()
    except:
        log.warning(str(sys.exc_info()))


def get_latest_event_ts(conn):
    """
    get the ts of the latest event in the events table

    :param conn: python dbapi connection object
    :return: todo return what?
    """

    # get the latest event

    q = 'select max(events.ts) from events'

    try:
        c = conn.cursor()
        c.execute(q)
        r = c.fetchall()
    except:
        log.warning(sys.exc_info())

    return r[0][0]  # list of tuples - need first and only element


def get_holder(conn):
    """
    get current token holder

    :param conn:
    :return: todo what to return?
    """

    try:
        ts = get_latest_event_ts(conn)
    except:
        log.warning(sys.exc_info())

    q = """
select users.name, events.ts, categories.category
from events
join users on events.user = users.ROWID
join categories on events.category = categories.ROWID
where events.ts = {}
""".format(ts)

    try:
        c = conn.cursor()
        c.execute(q)

        r = c.fetchall()
        return r

    except:
        log.warning(sys.exc_info())