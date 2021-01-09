import sqlite3

from config import ACTIONS

from flask import g, current_app

def get_db():
    """
    Return a database connection.
    Database path is specified in the config file.
    """
    db = getattr(g, "_database", None)
    if db is None:
        g._database = sqlite3.connect(current_app.config["DATABASE_PATH"])
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
    conn = get_db()
    conn.execute(query, args)
    conn.commit()


def init_db(app):
    """
    Construct the tables in the database.
    Call this function once when setting up the server.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())

        db.executemany("INSERT INTO action VALUES (?)", [(i,) for i in ACTIONS])
        db.commit()
