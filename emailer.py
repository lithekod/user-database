import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server_url = "lithekod.lysator.liu.se"
sender_email = "dev@mail.com"
password = "dev"


def try_construct_link(liu_id, links, action):
    if liu_id in links and action in links[liu_id]:
        return "{}/{}".format(server_url, links[liu_id][action])
    return "{}/404".format(server_url)


def send_mail(receivers, links, subject, html):
    for liu_id, name, receiver_email, joined, renewed, receive_info in receivers:
        delete_link = try_construct_link(liu_id, links, "DELETE")
        renew_link = try_construct_link(liu_id, links, "RENEW")
        show_link = try_construct_link(liu_id, links, "SHOW")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        html = html.format(liu_id=liu_id, name=name, email=receiver_email,
                joined=joined, renewed=renewed, receive_info=receive_info,
                delete_link=delete_link, renew_link=renew_link,
                show_link=show_link)

        part2 = MIMEText(html, "html")
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
