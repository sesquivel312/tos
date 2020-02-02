# todo are transactions being committed?

import logging
from pathlib import Path
import sqlite3 as sql

from flask import Flask, request, redirect, render_template, g
from flask_bootstrap import Bootstrap

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

            dbfile = Path(__file__)
            dbfile = dbfile.parent
            dbfile = dbfile.joinpath('crud.sqlite')

        else:

            dbfile = Path(dbfile)

        db = g._database = sql.connect(dbfile)  # so db = a sqlite3 connection

    return db


def db_add_book(cur, title):
    """
    add book having title to DB

    #todo handle attempts to add dups

    :param cur:
    :param title:
    :return:
    """

    try:
        q = "insert into books ('title') values ('{}')".format(title)
        cur.execute(q)
    except sql.IntegrityError:
        pass  # todo report dup attempt to user


def db_list_books(cur):

    q = "select * from books"

    cur.execute(q)

    r = cur.fetchall()  # list of tuples - of one value each

    return [e[0] for e in r]  # extract the book titles from tuples and return as list


def db_update_book(cur, current_title, new_title):

    q = "update books set title = '{new}' where title = '{curr}'"\
        .format(new=new_title, curr=current_title)

    cur.execute(q)


def db_delete_book(cur, title):

    q = "delete from books where title = '{}'".format(title)

    cur.execute(q)


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


@app.route('/', methods=['GET', 'POST'])
def root():

    db = get_db()
    cur = db.cursor()

    if request.form:

        t = request.form.get('title')
        db_add_book(cur, t)

        db.commit()

    books = db_list_books(cur)

    return render_template('home.html', books=books)


@app.route('/update', methods=['POST', ])
def update():

    current_title = request.form.get('current_title')
    new_title = request.form.get('new_title')

    app.logger.debug('@@@ update cur: {}, new: {}'.format(current_title, new_title))

    db = get_db()
    cur = db.cursor()

    db_update_book(cur, current_title, new_title)

    db.commit()

    return redirect('/')


@app.route('/delete', methods=['POST', ])
def delete():

    title = request.form.get('title')

    db = get_db()
    cur = db.cursor()

    db_delete_book(cur, title)

    db.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)