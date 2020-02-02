"""
General comments

    SQL(ite) stuff
        results are returned as rows, which are represented as tuples.  If multiple
        rows are returned then a list of tuples is returned, a single tuple is otherwise


todo p1 complete db operation function
todo p1 update db functions to consume/return human readable strings instead of IDs
todo P2 test with uwsgi, then nginx
todo p3 fix the log file name - possibly move it
todo p3 bootstrap integration
todo p3 add static image file to templates
todo p3 can I use one conn/cursor - will need to pass around
todo p3 secure db operations (inserts, etc.)
todo p3 when/where close conn - this is tied up w/flask
"""

from datetime import datetime as dt
import logging
from pathlib import Path
import sqlite3 as sql
import sys

from flask import Flask, request, redirect, render_template, g
from flask_bootstrap import Bootstrap
import pytz

logging.basicConfig(filename=__file__ + '.log', level=logging.DEBUG)

app = Flask(__name__)
bs4 = Bootstrap(app)


# setup DB connection & cursor
def get_db(dbfile=None):
    """
    connect to the DB & return conn, cur, both?

    :return:
    """

    # g is some global object in Flask that can hold - stuff
    # likely some of that stuff is built in, and you can
    # create your own.  I'm not sure yet which is the case for
    # _database (likely the latter).  I'm not sure if any of
    # this is really needed, i.e. could I just create the db
    # connection in the route methods and skip storing it
    # in flask anywhere?  Maybe it's good to put it there
    # b/c flask maintains access to g when I would need it?
    # i'm not sure what I'm saying yet

    db = getattr(g, '_database', None)  # ? _database exists, then get value

    if db is None:

        if dbfile is None:
            dbfile = Path('data/tos.sqlite')

        else:
            dbfile = Path(dbfile)

        db = g._database = sql.connect(dbfile)  # so db = a sqlite3 connection

    return db


@app.teardown_appcontext
def close_connection(exception):
    """
    no idea what this is for yet - got it from the tutorial, specifically, what is
    teardown_appcontext decorator?  my guess right now is that it marks a method as
    one that will be executed w/the flask app goes out of scope or something like
    that?

    :param exception:
    :return:
    """

    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


def strtime_to_unixts(timestring, tz='Etc/UTC', tformat='%Y-%m-%d', keep_sec=False):
    """
    convert a time string to unix timestamp, optionally including seconds, etc.

    The keep_sec param is a bool flag determining if the returned timestamp includes
    seconds (and smaller fractions of time).  Default is to remove seconds, etc.

    todo p1 how to handle tz's - tests are failing

    :param tz: timezone name, from pytz, UTC is default
    :type tz: str
    :param tformat: strftime time format string
    :type tformat: str
    :param timestring: date and/or time string
    :type timestring: str
    :param keep_sec: flag determines if seconds and smaller are kept
    :type keep_sec: bool
    :return: unix timestamp
    :rtype: float | int
    """

    tz = pytz.timezone(tz)

    t = datetime.strptime(timestring, tformat)  # convert to naive datetime obj
    t = t.replace(tzinfo=tz)  # use the dt object replace method to set tz attribute

    if tz is not pytz.utc:  # convert to UTC if not already
        t = t.astimezone(pytz.utc)

    t = t.timestamp()  # convert to unix timestamp w/o seconds, etc.

    if not keep_sec:

        t = int(t)  # drop seconds, etc.

    return t


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


def db_add_user(cur, name):
    """
    add users to users db

    Note:
        to insert multiple records, the insert statement looks like this:

            insert into users (name) values ('name1'), ('name2'), ... ('namen')

    todo checks and return something sensible
    todo check # of records to insert
    :param cur: python dbapi connection object
    :param name: user name
    :type name: list
    :return: name added or None if fail
    :rtype: str | None
    """

    q = "insert into users (name) values ('{}')".format(name)
    cur.execute(q)


def db_delete_user(cur, user):
    """
    delete the user


    :param cur:
    :param user:
    :return:
    """

    q = "delete from users where name = '{}'".format(user)

    cur.execute(q)


def db_get_users(cur):
    """
    get the current list of user names

    """
    q = "select ROWID, name from users"

    cur.execute(q)

    return cur.fetchall()


def db_get_user_by_id(cur, id=None):
    """
    get user given an ID

    todo p2 handle no id & errors
    :param id:

    """
    q = "select name from users where ROWID = {}".format(id)

    cur.execute(q)

    return cur.fetchone()


def db_get_categories(cur):
    """
    get the current list of categories

    """
    q = "select ROWID, category from categories"

    cur.execute(q)

    return cur.fetchall()


def db_add_event(cur, event):
    """
    add a token event to the events db

    :param event: tuple representing row to insert
    :type event: tuple
    :param cur: python dbapi connection object
    :return: todo return what
    """

    ts = int(dt.utcnow().timestamp())  # only need date part

    q = "insert into events (timestamp, nominee, reporter, category) values ({}, {}, {}, {})"\
        .format(ts, *event)

    cur.execute(q)


def db_delete_event(cur, event):
    """
    event is currently a string like: (1580640716, 4, 6, 3), delete the row w/the timestamp, given by the first
    element of the tuple - but have to conver it to an int first.


    :param cur:
    :param event:
    :return:
    """

    event = event.split(',')  # split the tuple components - gives list
    event = event[0].lstrip('(')  # remove paren
    event = int(event)  # cast to int

    q = "delete from events where timestamp = {}".format(event)

    cur.execute(q)


def db_get_events(cur, limit=5):
    """
    get the ts of the latest $limit events in the events table

    If limit is None then get all the events

    :param limit: number of events to get
    :type limit: int
    :param cur: python dbapi connection object
    :return: event rows matching query
    :rtype: list
    """

    # todo get latest events only - e.g. last 10
    q = """
select events.timestamp, nominee.name, reporter.name, categories.category
from events 
join users nominee on events.nominee == nominee.ROWID
join users reporter on events.reporter == reporter.ROWID
join categories on events.category == categories.ROWID
order by timestamp desc limit {}
""".format(limit)  # get all the events

    cur.execute(q)
    events = cur.fetchall()

    for i, event in enumerate(events):
        # convert the unix timestamps to a human friendly format
        # need to recreate the tuples b/c immutable, then replace
        # each tuple in the events list

        ts, nom, rep, cat = event  # extract the tuple elements

        ts = dt.fromtimestamp(ts)  # make ts human friendly
        ts = dt.strftime(ts, '%m-%d-%Y')

        events[i] = (ts, nom, rep, cat) # reconstitute the tuple & replace in events list

    return events


def db_get_holder(cur):
    """
    get the current token holder

    :param cur:
    :return:
    """

    q = """
select users.name
from events
join users on events.nominee = users.ROWID
where events.timestamp = (
    select max(events.timestamp)
    from events
    )"""

    cur.execute(q)

    return cur.fetchone()[0]


@app.route('/', methods=['GET', 'POST', ])
def root():
    """
    handle the home page, which:

        * displays the current holder
        * provides form to award to new holder
        * displays the last 5 awards

    :return: rendered home page template
    :rtype: text
    """

    db = get_db()
    cur = db.cursor()

    # need all this info in order to populate the page template
    holder = db_get_holder(cur)
    users = db_get_users(cur)
    categories = db_get_categories(cur)
    events = db_get_events(cur)

    if request.form:
        # award token, i.e. add event to events table

        reporter = request.form.get('reporter')
        nominee = request.form.get('nominee')
        categeory = request.form.get('category')

        db_add_event(cur, (nominee, reporter, categeory))
        db.commit()

        # get new holder & recent events
        holder = db_get_holder(cur)
        events = db_get_events(cur)

    return render_template('home.html',
                           holder=holder,
                           users=users,
                           categories=categories,
                           events=events)


@app.route('/user/add', methods=['GET', 'POST', ])
def user_add():
    """
    add a user to the DB

    todo P1 must be authenticated
    todo P2 handle attempt to add duplicate
    :return:
    """

    if request.form:

        db = get_db()
        cur = db.cursor()

        name = request.form.get('name')

        db_add_user(cur, name)
        db.commit()

    return render_template('add_user.html')


@app.route('/user/delete', methods=['GET', 'POST', ])
def user_delete():
    """
    remove a user from the DB

    todo P1 must be authenticated
    todo P2 handle attempt to add duplicate
    :return:
    """

    if request.form:

        db = get_db()
        cur = db.cursor()

        name = request.form.get('name')

        db_delete_user(cur, name)
        db.commit()

    return render_template('delete_user.html')


if __name__ == '__main__':
    # this bit should only be used by the dev server

    app.run(debug=True)
