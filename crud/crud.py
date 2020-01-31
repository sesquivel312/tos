# todo are transactions being committed?

import logging
from pathlib import Path
import sqlite3 as sql

from flask import Flask, request, render_template, g

logging.basicConfig(filename=__file__ + '.log', level=logging.DEBUG)

app = Flask(__name__)


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

            dbfile = Path(__file__)
            dbfile = dbfile.parent
            dbfile = dbfile.joinpath('crud.sqlite')

        else:

            dbfile = Path(dbfile)

        db = g._database = sql.connect(dbfile)  # so db = a sqlite3 connection

    return db


@app.teardown_appcontext
def close_connection(execpt):
    """
    no idea what this is for yet - got it from the tutorial, specifically, what is
    teardown_appcontext decorator?  my guess right now is that it marks a method as
    one that will be executed w/the flask app goes out of scope or something like
    that?

    :param execpt:
    :return:
    """

    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


def db_add_book(cur, title):
    """
    add book having title to DB

    #todo handle attempts to add dups

    :param cur:
    :param title:
    :return:
    """

    q = "insert into books ('title') values ('{}')".format(title)

    cur.execute(q)


@app.route('/', methods=['GET', 'POST'])
def root():

    if request.form:

        db = get_db()
        cur = db.cursor()

        t = request.form.get('title')
        db_add_book(cur, t)

        db.commit()

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)