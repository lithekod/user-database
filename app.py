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
            id     BLOB     UNIQUE PRIMARY KEY,
            liu_id TEXT     NOT NULL,
            email  TEXT     NOT NULL,
            active BOOLEAN  NOT NULL
        )
        """
    )

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
            id         BLOB  UNIQUE PRIMARY KEY,
            type       INT   NOT NULL,
            member_id  BLOB  NOT NULL,
            FOREIGN KEY(member_id) REFERENCES member(id)
        )
        """
    )

# Experimental
def add_member(liuid, email):
    db.execute("INSERT INTO member VALUES (?, ?, ?, ?)",
        (uuid.uuid4().bytes, liuid, email, 0))

# Experimental
def add_link(member_id):
    db.execute("INSERT INTO link VALUES (?, ?, ?)",
        (uuid.uuid4().bytes, 0, member_id))

# Experimental
def delete_member(member_id):
    db.execute("DELETE FROM member WHERE id = ?", (member_id,))

