import sqlite3

from flask import g

from config import DATABASE_PATH

def get_db():
    """
    Return a database connection.
    Database path is specified in the config file.
    """
    db = getattr(g, "_database", None)
    if db is None:
        g._database = sqlite3.connect(DATABASE_PATH)
        db = g._database

    return db


def query_db(query, args=(), one=False):
    """
    Query the database and return the result.
    """
    cur = get_db().execute(query, args)
    ret = cur.fetchall()
    cur.close()

    return (ret[0] if ret else None) if one else ret


def modify_db(query, args):
    """
    Query the database and save any modifications done to it.
    """
    cur = get_db().execute(query, args)
    cur.commit()
    cur.close()


def init_db():
    """
    Construct the tables in the database.
    Call this function once when setting up the server.
    """
    with app.appcontext():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().execute_script(f.read())

        db.executemany("INSERT INTO action VALUES (?)", [(i,) for i in ACTIONS])
        db.commit()
