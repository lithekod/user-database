import sys
import subprocess

from urllib import parse

if len(sys.argv) != 4:
    print("Usage: python upload_members.py members.txt URL ADMIN_PASSWORD")
    exit()

URL = sys.argv[2]
ADMIN_PASSWORD = sys.argv[3]

with open(sys.argv[1], "r") as f:
    for line in f:
        line = line.rstrip()
        id, name, email, joined, receive_email = (parse.quote_plus(arg) for arg in line.split(","))
        out = subprocess.check_output([f"curl -s -u :{ADMIN_PASSWORD} '{URL}/add_member/?id={id}&name={name}&email={email}&joined={joined}&receive_email={receive_email}'"],
                shell=True)
        print(out)
