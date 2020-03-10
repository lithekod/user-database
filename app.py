import uuid
import datetime
import sqlite3

from os import urandom
from os import environ

from threading import Thread

from functools import wraps

from flask import Flask
from flask import jsonify
from flask import request

from emailer import send_mail

from queries import *
from config import *
from util import *
from db import *

ACTIONS = ["SHOW", "RENEW", "DELETE", "UNSUBSCRIBE"]

app = Flask(__name__)

def admin_only(f):
    """
    Wraps endpoint so that it will require SECRET_KEY.
    """
    @wraps(f)
    def decorated_fn(*args, **kwargs):
        auth = request.authorization
        if auth is None or auth["password"] != SECRET_KEY:
            return "Unauthorized"

        return f(*args, **kwargs)

    return decorated_fn


def add_member(liuid, name, email, joined, receive_email):
    """
    Add a member to the database.
    All arguments has to be provided and properly formatted.
    Return a tuple with a boolean and a string (success, message).
    """
    def err_msg(msg):
        """ Return a informative error message. """
        return False, f"Failed to add user with id: {liuid} - {msg}."

    liuid = liuid.lower()

    if not is_id(liuid):
        return err_msg("Invalid id")

    if not is_email(email):
        return err_msg("Invalid email")

    if not is_date(joined):
        return err_msg("Invalid date (%Y-%m-%d required)")

    joined = datetime.datetime.strptime(joined, "%Y-%m-%d")

    if not is_bool(receive_email):
        return err_msg("Invalid receive_email (0 or 1 required)")

    try:
        modify_db(INSERT_NEW_MEMBER, (liuid, name, email, joined, receive_email))
    except sqlite3.Error as e:
        return err_msg(e.args[0])

    return True, f"Successfully added user with id: {liuid}."


def add_link(member_id, action):
    """
    Add a link to the database that when accessed,
    performs action on the member with corresponding member_id.

    :param member_id str: id which the link should be linked with.
    :param action str: The action the link should perform.
    """
    if action not in ACTIONS:
        return "Invalid action"

    url_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    url = "{}_".format(action)

    while len(url) < 32:
        char_index = ord(urandom(1))
        if char_index < len(url_chars):
            url += url_chars[char_index]

    modify_db(INSERT_NEW_LINK, (member_id, action, url))

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
    table = {}
    for liuid, link in query_db(SELECT_LINK_MEMBERID_LINK):
        if liuid not in table:
            table[liuid] = {}
        table[liuid][link[:link.find("_")]] = link

    return table


def regenerate_links():
    """
    Remove old links and generate new links for all users.
    Every user gets one link for each ACTION.
    """
    modify_db(DELETE_LINK)

    for (liuid,) in query_db(SELECT_MEMBER_ID):
        for action in ACTIONS:
            add_link(liuid, action)

    return get_links()


@app.route("/<link>")
def handle_link(link):
    """
    Handle a link and perform action related to the link.
    Possible actions can be found in ACTIONS.
    """
    link = query_db(SELECT_LINK_WITH_URL, (link,), True)

    if link is None:
        return "Invalid link. It might have been used up.."

    member_id, action_id, url, created  = link

    member = query_db(SELECT_MEMBER_WITH_ID, (member_id,), True)
    liuid, name, email, joined, renewed, receive_email = member

    ret = "Unknown link"

    if action_id == "SHOW":
        ret = jsonify(member_to_dict(member))

    elif action_id == "RENEW":
        modify_db(UPDATE_MEMBER_RENEW, (liuid,))
        modify_db(DELETE_LINK_WITH_IDS, (liuid, action_id))
        ret = "Your membership has been renewed!"

    elif action_id == "DELETE":
        modify_db(DELETE_LINK_WITH_MEMBER_ID, (liuid,))
        modify_db(DELETE_MEMBER_WITH_ID, (liuid,))
        ret = "You have now left LiTHe kod. We hope you enjoyed your stay!"

    elif action_id == "UNSUBSCRIBE":
        modify_db(UPDATE_MEMBER_UNSUBSCRIBE, (liuid,))
        ret = "You are no longer subscribed to emails from LiTHe kod."

    return ret


@app.route("/add_member/")
@admin_only
def handle_add_member():
    """
    Handle adding new members to the database.
    Not all arguments has to be specified in order for a user to be added.
    """
    args = request.args

    required_arguments = ["id", "name"]
    optional_arguments = ["email", "joined", "receive_email"]
    optional_default = ["{}@student.liu.se".format(args["id"]),
            datetime.date.today().isoformat(), "1"]

    member_args = []

    for required_argument in required_arguments:
        if required_argument not in args:
            return f"No '{required_argument}' specifed"
        else:
            member_args.append(args[required_argument])

    for optional_argument, default in zip(optional_arguments, optional_default):
        if optional_argument not in args:
            member_args.append(default)
        else:
            member_args.append(args[optional_argument])

    success, message = add_member(*member_args)

    # If the member is successfully added, send them an email.
    if success:

        for action in ACTIONS:
            add_link(args["id"], action)

        with open("templates/welcome.html") as f:
            html = f.read()

        send_mail(
            get_mailing_list(args["id"]),
            "Welcome to LiTHe kod!",
            html,
            get_links()
        )

    return message


@app.route("/metrics/")
@admin_only
def get_metrics():
    """
    Return information about the database.
    Shows amount of members and active members for now.
    """
    members = query_db(SELECT_MEMBER)
    active_members = len(query_db(SELECT_MEMBER_ACTIVE))

    return jsonify({
        "member_count": len(members),
        "active_members": active_members,
        "members": [member_to_dict(member) for member in members]
    })


def get_mailing_list(receivers):
    """
    Create a mailing list for the spcified receivers.
    receivers can be any of the following values:
        default - All members that wants to receive emails.
        all - All members.
        inactive - All inactive members.
        liuid - Only the member with the specified liuid.
    """
    mailing_list = []
    if receivers == "default":
        mailing_list = query_db(SELECT_MEMBER_SUBSCRIBED)
    elif receivers == "all":
        mailing_list = query_db(SELECT_MEMBER)
    elif receivers == "inactive":
        mailing_list = query_db(SELECT_MEMBER_INACTIVE)
    else:
        for liu_id in receivers.split():
            mailing_list += query_db(SELECT_MEMBER_WITH_ID, (liu_id,))

    return mailing_list


@app.route("/email_members/")
@admin_only
def email_members():
    """
    Send emails to all members.
    Specify subject and html file as arguments.
    """
    args = request.args
    if "receivers" not in args:
        return "No receivers spcified."
    receivers = args["receivers"]

    if "subject" not in args:
        return "No subject specified."
    subject = args["subject"]

    if "template" not in args:
        return "No template spcified."
    template = args["template"]

    with open("templates/{}.html".format(template)) as f:
        html = f.read()

    Thread(target=send_mail, args=(get_mailing_list(receivers), subject, html,
        get_links())).run()

    return "Emails are being sent!"


@app.teardown_appcontext
def close_connection(e):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
