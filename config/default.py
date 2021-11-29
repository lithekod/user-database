import os

SECRET_KEY = "dev"

EMAIL_ADDRESS = "no-reply@lithekod.se"
EMAIL_PASSWORD = "dev"
EMAILER_PID = os.environ.get("EMAILER_PID")
if EMAILER_PID is not None:
    EMAILER_PID = int(EMAILER_PID)

SERVER_URL = "localhost:5000"

DATABASE_PATH = "/tmp/temp.db"
DATABASE_VERSION = 2
ACTIONS = ["SHOW", "RENEW", "DELETE", "UNSUBSCRIBE"]

AOC_SESSION = ""
STANDINGS_PATH = "aoc/aoc_standings.json"
INVALID_CONTESTANTS = set()
