import sys
import time
import argparse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

from datetime import datetime

from html2text import html2text

from config import *

def try_construct_link(liu_id, action, links):
    """
    Try to create a link to action for the member with liu_id.
    If a link does not exist a placeholder link is returned instead.

    :param liu_id str: Member to construct link for.
    :param action str: Action of link to construct.
    :param links dict: Links to actions for users.
    """
    if liu_id in links and action in links[liu_id]:
        return "http://{}/{}".format(SERVER_URL, links[liu_id][action])
    return "http://{}/404".format(SERVER_URL)


def send_mail(receivers, subject, html, links={}, interactive=False):
    """
    Send emails to receivers.

    :param receivers list: List of members to receive emails.
    :param subject str: Subject of emails.
    :param html str: HTML template to be rendered.
    :param links dict: Links to actions for users.
    :param interactive bool: Enables retrying of sending emails. (requires input)
    """
    TIME_BETWEEN_EMAILS = 5 if len(receivers) > 1 else 0
    if interactive:
        LOG_FILE = sys.stdout
    else:
        current_time = datetime.now().strftime("%Y-%m-%dat%H:%M:%S")
        LOG_FILE = open("logs/emaillog_{}".format(current_time), "w")


    timestamp = datetime.now().timestamp()
    deadline = datetime.fromtimestamp(timestamp + 365 / 2 * 24 * 3600).strftime("%Y-%m-%d")

    plain = html2text(html)
    for liu_id, name, receiver_email, joined, renewed, receive_info in receivers:
        delete_link = try_construct_link(liu_id, "DELETE", links)
        renew_link = try_construct_link(liu_id, "RENEW", links)
        show_link = try_construct_link(liu_id, "SHOW", links)
        unsubscribe_link = try_construct_link(liu_id, "UNSUBSCRIBE", links)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = formataddr((str(Header('LiTHe kod', 'utf-8')), SENDER_EMAIL))
        message["To"] = receiver_email

        kwargs = {
            "deadline": deadline,
            "liu_id": liu_id,
            "name": name,
            "email": receiver_email,
            "joined": joined,
            "renewed": renewed,
            "receive_info": receive_info,
            "delete_link": delete_link,
            "renew_link": renew_link,
            "show_link": show_link,
            "unsubscribe_link": unsubscribe_link
        }

        formatted_plain = plain.format(**kwargs)
        formatted_html = html.format(**kwargs)

        part1 = MIMEText(formatted_plain, "plain")
        part2 = MIMEText(formatted_html, "html")
        message.attach(part1)
        message.attach(part2)

        retry = True
        while retry:
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(
                        SENDER_EMAIL, receiver_email, message.as_string()
                    )

                print("Sent email to: {}".format(liu_id), file=LOG_FILE, flush=True)

                retry = False
                time.sleep(TIME_BETWEEN_EMAILS)
            except Exception as e:
                print(e, file=LOG_FILE, flush=True)
                if interactive:
                    retry_message = "{}\nFailed sending mail to {} - retry? (Y/n/skip): "\
                                    .format(e, liu_id)
                    ans = input(retry_message).lower()

                    if ans == "n":
                        return

                    retry = ans != "skip"
                else:
                    retry = False

    if not interactive:
        LOG_FILE.close()


def run_as_server():
    """
    Wait for pickled files of email instructions, and then send the emails.
    """
    import pickle
    from os import listdir, remove

    PICKLE_NAME = "emailpickle"

    try:
        while True:
            if PICKLE_NAME in listdir("."):
                with open(PICKLE_NAME, "br") as f:
                    send_mail(*pickle.load(f))
                remove(PICKLE_NAME)
            time.sleep(10)
    except Exception:
        return



if __name__ == "__main__":

    if "server" in sys.argv:
        run_as_server()
        exit()

    parser = argparse.ArgumentParser(description="Send emails to members")

    parser.add_argument("-r", "--receivers",
                        nargs=1,
                        required=True,
                        help="Either one of the values: 'default', 'all',\
                              'inactive' or a space-separated list of liuids.")

    parser.add_argument("-s", "--subject",
                        nargs=1,
                        required=True,
                        help="Email subject")

    parser.add_argument("-t", "--template",
                        nargs=1,
                        required=True,
                        help="Email template")

    args = parser.parse_args()

    import app

    with app.app.app_context():
        receivers = app.get_mailing_list(args.receivers[0])
        links = app.get_links()
    subject = args.subject[0]
    template = open(args.template[0]).read()

    send_mail(receivers, subject, template, links, interactive=True)
