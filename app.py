import uuid
import sqlite3

from os import urandom

from flask import Flask, jsonify

DATABASE_PATH = "/tmp/test.db"

app = Flask(__name__)
db = sqlite3.connect(DATABASE_PATH)

ACTIONS = ["SHOW", "RENEW", "DELETE"]

def create_database():

    """Member table
    This table contains all of the information we store on members.
    """
    db.execute(
        """
        CREATE TABLE member
        (
            id             VARCHAR(10)  NOT NULL,
            name           VARCHAR(64)  NOT NULL,
            email          VARCHAR(64)  NOT NULL,
            joined         TIME         NOT NULL,
            renewed        TIME         NOT NULL,
            receive_email  BOOLEAN      NOT NULL,
            PRIMARY KEY (id)
        )
        """
    )

    """Action table
    The id specifies what a action should do:
        DELETE - Removes a member from the database.
        RENEW - Sets the renewed status of the member to the current date.
        SHOW - Provides a json string with one of the members information.
    """
    db.execute(
        """
        CREATE TABLE action
        (
            id  VARCHAR(10),
            PRIMARY KEY (id)
        )
        """
    )

    db.executemany("INSERT INTO action VALUES (?)", [(i,) for i in ACTIONS])

    """Link table
    This table spcifies the active links which can be accessed by a member.
    """
    db.execute(
        """
        CREATE TABLE link
        (
            member_id  VARCHAR(10)  NOT NULL,
            action_id  VARCHAR(10)  NOT NULL,
            url        VARCHAR(32)  UNIQUE NOT NULL,
            created    TIME         NOT NULL,
            PRIMARY KEY (member_id, action_id),
            FOREIGN KEY (member_id) REFERENCES member(id),
            FOREIGN KEY (action_id) REFERENCES action(id)
        )
        """
    )

    db.commit()


def check_pnr(l):
    l = [int(i) for i in l]
    ctrl = l.pop()
    for i in range(0, len(l), 2): l[i] *= 2
    s = sum([sum([int(j) for j in str(i)]) for i in l])
    return (s + ctrl) % 10 == 0


def is_int(string):
    try:
        int(string)
        return True
    except:
        return False


def is_id(liuid):
    return (len(liuid) <= 8 and liuid[:-3].islower() and is_int(liuid[-3:])) or \
            (len(liuid) == 10 and is_int(liuid) and check_pnr(l))


def add_member(liuid, name, email):

    liuid = liuid.lower()

    if not is_id(liuid):
        return "Invalid id"

    db.execute("INSERT INTO member VALUES\
            (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)",
        (liuid, name, email, True))
    db.commit()

    return "Success"


def add_link(member_id, action):

    if action not in ACTIONS:
        return "Invalid action"

    url_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    url = "{}_".format(action)

    while len(url) < 32:
        char_index = ord(urandom(1))
        if char_index < len(url_chars):
            url += url_chars[char_index]

    db.execute("INSERT INTO link VALUES \
            (?, ?, ?, CURRENT_TIMESTAMP)", (member_id, action, url))
    db.commit()

    return "Success"


# Experimental
def delete_member(member_id):
    db.execute("DELETE FROM member WHERE id=?", (member_id,))
    db.commit()

@app.route("/<link>")
def handle_link(link):

    db = sqlite3.connect(DATABASE_PATH)
    link = db.execute("SELECT * FROM link WHERE url=?", (link,)).fetchone()

    if link is None:
        return "404"

    member_id, action_id, url, created  = link

    if action_id == "SHOW":
        member = db.execute("SELECT * FROM member WHERE id=?", (member_id,)).fetchone()
        id, name, email, joined, renewed, receive_email = member
        return jsonify({
            "id": id,
            "name": name,
            "email": email,
            "joined": joined,
            "renewed": renewed,
            "receive_email": receive_email
        })

    return action_id

# Test
def test_database():
    add_member("erima882", "Erik Mattfolk", "erima882@student.liu.se")
    add_link("erima882", "SHOW")

