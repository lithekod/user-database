import uuid
import sqlite3
import datetime

from os import urandom
from os import environ

from flask import Flask
from flask import jsonify
from flask import request

from emailer import send_mail

ACTIONS = ["SHOW", "RENEW", "DELETE"]

DATABASE_PATH = environ.get("DATABASE_PATH")
if not DATABASE_PATH:
    raise ValueError("No DATABASE_PATH set in env")

SECRET_KEY = environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in env")

app = Flask(__name__)

def create_database():
    """
    Construct the tables in the database.
    Call this function once when setting up the server.
    """
    db = sqlite3.connect(DATABASE_PATH)

    """Member table
    This table contains all of the information we store on members.
    """
    db.execute(
        """
        CREATE TABLE member
        (
            id             VARCHAR(10)  PRIMARY KEY,
            name           VARCHAR(64)  NOT NULL,
            email          VARCHAR(64)  NOT NULL,
            joined         TIME         NOT NULL,
            renewed        TIME         NOT NULL,
            receive_email  BOOLEAN      NOT NULL
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
            id  VARCHAR(10) PRIMARY KEY
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
    db.close()


def is_int(string):
    """ Test if a string can be interpreted as an int. """
    try:
        int(string)
        return True
    except:
        return False


def is_pnr(l):
    """
    Test if a sequence l is a valid swedish personal number.
    TDDE23 labb 2 <3
    """
    if len(l) != 10 or not is_int(id): return False
    l = [int(i) for i in l]
    ctrl = l.pop()
    for i in range(0, len(l), 2): l[i] *= 2
    s = sum([sum([int(j) for j in str(i)]) for i in l])
    return (s + ctrl) % 10 == 0


def is_liuid(liuid):
    """ Test if a string is a liuid. """
    return len(liuid) <= 8 and liuid[:-3].islower() and is_int(liuid[-3:])


def is_id(id):
    """ Test if id is either a liuid or a swedish personal number. """
    return is_liuid(id) or is_pnr(l)


def add_member(liuid, name, email, joined, receive_email):
    """
    Add a member to the database.
    All arguments has to be provided and properly formatted.
    """
    liuid = liuid.lower()

    if not is_id(liuid):
        return "Invalid id"

    if "@" not in email:
        return "Invalid email address"

    try:
        joined = datetime.datetime.strptime(joined, "%Y-%m-%d")
    except ValueError:
        return "joined has to be in the form %Y-%m-%d"

    if receive_email not in ["0", "1", 0, 1]:
        return "receive_email has to be 0 or 1"

    db = sqlite3.connect(DATABASE_PATH)
    db.execute("INSERT INTO member VALUES\
            (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
        (liuid, name, email, joined, receive_email))
    db.commit()
    db.close()

    return f"Successfully added user with id: {liuid}"


def add_link(member_id, action):
    """
    Add a link to the database that when accessed,
    performs action on the member with corresponding member_id.
    """
    if action not in ACTIONS:
        return "Invalid action"

    url_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    url = "{}_".format(action)

    while len(url) < 32:
        char_index = ord(urandom(1))
        if char_index < len(url_chars):
            url += url_chars[char_index]

    db = sqlite3.connect(DATABASE_PATH)
    db.execute("INSERT INTO link VALUES \
            (?, ?, ?, CURRENT_TIMESTAMP)", (member_id, action, url))
    db.commit()
    db.close()

    return f"Successfully added {action} link to id: {member_id}"


def get_links():
    """
    Get a dict with all of the links currently in the database.
    The dict is formatted in the following way:
    {
        "liuid123": {
            "ACTION": "ACTION_tehxrkAOEuhrc9238"
                .
                .
        }
        .
        .
    }
    """
    db = sqlite3.connect(DATABASE_PATH)
    table = {}
    for liuid, link in db.execute("SELECT member_id, url FROM link").fetchall():
        if liuid not in table:
            table[liuid] = {}
        table[liuid][link[:link.find("_")]] = link
    db.close()

    return table


def generate_links():
    """
    Remove old links and generate new links for all users.
    Every user gets one link for each ACTION.
    """
    db = sqlite3.connect(DATABASE_PATH)
    db.execute("DELETE FROM link")
    ids = db.execute("SELECT id from member").fetchall()
    db.commit()
    db.close()

    for (liuid,) in ids:
        for action in ACTIONS:
            add_link(liuid, action)

    return get_links()


@app.route("/<link>")
def handle_link(link):
    """
    Handle a link and perform action related to the link.
    Possible actions can be found in ACTIONS.
    """
    db = sqlite3.connect(DATABASE_PATH)
    link = db.execute("SELECT * FROM link WHERE url=?", (link,)).fetchone()

    if link is None:
        return "404"

    member_id, action_id, url, created  = link

    member = db.execute("SELECT * FROM member WHERE id=?", (member_id,)).fetchone()
    liuid, name, email, joined, renewed, receive_email = member

    ret = "Unknown link"

    if action_id == "SHOW":
        ret = jsonify({
            "id": liuid,
            "name": name,
            "email": email,
            "joined": joined,
            "renewed": renewed,
            "receive_email": receive_email
        })

    elif action_id == "RENEW":
        db.execute("UPDATE member SET renewed=CURRENT_TIMESTAMP WHERE id=?",
                (liuid,))
        db.execute("DELETE FROM link WHERE member_id=? AND action_id=?",
                (liuid, action_id))
        db.commit()
        ret = "Your membership has been renewed!"

    elif action_id == "DELETE":
        db.execute("DELETE FROM link WHERE member_id=?", (liuid,))
        db.execute("DELETE FROM member WHERE id=?", (liuid,))
        db.commit()
        ret = "You have now left LiTHe kod. We hope you enjoyed your stay!"

    db.close()

    return ret


@app.route("/add_member/")
def handle_add_member():
    """
    Handle adding new members to the database.
    Not all arguments has to be specified in order for a user to be added.
    """
    if request.authorization["password"] != SECRET_KEY:
        return "Unauthorized"

    required_arguments = ["id", "name"]
    optional_arguments = ["email", "joined", "receive_email"]

    args = request.args
    member_args = []

    for required_argument in required_arguments:
        if required_argument not in args:
            return f"No '{required_argument}' specifed"
        else:
            member_args.append(args[required_argument])

    optional_default = ["{}@student.liu.se".format(args["id"]),
            datetime.date.today().isoformat(), "1"]
    for optional_argument, default in zip(optional_arguments, optional_default):
        if optional_argument not in args:
            member_args.append(default)
        else:
            member_args.append(args[optional_argument])

    return add_member(*member_args)


@app.route("/metrics/")
def get_metrics():
    """
    Return information about the database.
    Shows amount of members and active members for now.
    """
    if request.authorization["password"] != SECRET_KEY:
        return "Unauthorized"

    db = sqlite3.connect(DATABASE_PATH)
    members = db.execute("SELECT count(*) FROM member").fetchone()[0]
    active_members = db.execute("SELECT count(*) FROM member\
            WHERE strftime('%s', CURRENT_TIMESTAMP)\
            - strftime('%s', renewed) < 180*24*3600").fetchone()[0]
    db.close()

    return f"members: {members}\nactive_members: {active_members}"


def get_mailing_list(receivers):
    """
    Create a mailing list for the spcified receivers.
    receivers can be any of the following values:
        default - All members that wants to receive emails.
        all - All members.
        inactive - All inactive members.
        liuid - Only the member with the specified liuid.
    """
    db = sqlite3.connect(DATABASE_PATH)

    mailing_list = []
    if receivers == "default":
        mailing_list = db.execute(
                "SELECT * FROM member WHERE receive_email=1").fetchall()
    elif receivers == "all":
        mailing_list = db.execute("SELECT * FROM member").fetchall()
    elif receivers == "inactive":
        mailing_list = db.execute("SELECT * FROM member\
            WHERE strftime('%s', CURRENT_TIMESTAMP)\
            - strftime('%s', renewed) < 180*24*3600").fetchall()
    else:
        mailing_list = db.execute("SELECT * FROM member WHERE id=?",
                (receivers,)).fetchall()
    db.close()

    return mailing_list


@app.route("/email_members/")
def email_members():
    """
    Send emails to all members.
    Specify subject and html file as arguments.
    """
    if request.authorization["password"] != SECRET_KEY:
        return "Unauthorized"

    if "receivers" not in args:
        return "No receivers spcified."
    receivers = args["receivers"]

    args = request.args
    if "subject" not in args:
        return "No subject specified."
    subject = args["subject"]

    if "htmlfile" not in args:
        return "No htmlfile spcified."
    htmlfile = args["htmlfile"]

    with open(htmlfile) as f:
        html = f.read()

    send_mail(get_mailing_list(receivers), subject, html, get_links())

    return "Mails sent!"


# Test
def test_database():
    create_database()
    add_member("erima882", "Erik Mattfolk", "erima882@student.liu.se")
    add_link("erima882", "SHOW")
