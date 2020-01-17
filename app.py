import uuid
import sqlite3

from flask import Flask

app = Flask(__name__)
db = sqlite3.connect(':memory:')

def create_database():

    """Member table
    This table contains all of the information we store on members.
    """
    db.execute(
        """
        CREATE TABLE member
        (
            id            VARCHAR(10)  NOT NULL,
            name          VARCHAR(64)  NOT NULL,
            email         VARCHAR(64)  NOT NULL,
            joined        TIME         NOT NULL,
            renewed       TIME         NOT NULL,
            receive_info  BOOLEAN      NOT NULL,
            PRIMARY KEY (id)
        )
        """
    )

    """Action table
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

    actions = [("SHOW",), ("RENEW",), ("DELETE",)]
    db.executemany("INSERT INTO action VALUES (?)", actions)

    """Link table
    This table spcifies the active links which can be accessed by a member.
    The type specifies what a link should do:
        0 - Removes the member associated with member_id from the database.
        1 - Sets the active status of the member associated with member_id to 1.
    """
    db.execute(
        """
        CREATE TABLE link
        (
            member_id  VARCHAR(10)  NOT NULL,
            action_id  VARCHAR(10)  NOT NULL,
            url        VARCHAR(64)  NOT NULL,
            PRIMARY KEY (member_id, action_id),
            FOREIGN KEY (member_id) REFERENCES member(id),
            FOREIGN KEY (action_id) REFERENCES action(id)
        )
        """
    )


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

    liuid = liuid.to_lower()

    assert is_id(liuid), "Invalid id"

    db.execute("INSERT INTO member VALUES\
            (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?)",
        (liuid, name, email, True))

# Experimental
def add_link(member_id):
    db.execute("INSERT INTO link VALUES (?, ?, ?)",
        (uuid.uuid4().bytes, 0, member_id))

# Experimental
def delete_member(member_id):
    db.execute("DELETE FROM member WHERE id = ?", (member_id,))

@app.route("/<link>")
def handle_link(link):
    return link
