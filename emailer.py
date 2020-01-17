import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "dev@mail.com"
password = "dev"

def send_mail(receivers, html):
    for liu_id, name, receiver_email, joined, renewed, receive_info in receivers:
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        html = html.format(liu_id=liu_id, name=name, email=receiver_email, joined=joined, renewed=renewed, receive_info=receive_info)

        part2 = MIMEText(html, "html")
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
