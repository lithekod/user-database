import unittest
import base64
import json
import os

from db import *
from util import *
from config import SECRET_KEY, DATABASE_PATH
from app import app

# Only run tests in a debug environment.
# We don't want to delete the production database.
if SECRET_KEY != "dev":
    exit()

def reset_db():
    """ Reset the database. """
    try:
        os.remove(DATABASE_PATH)
    except OSError:
        pass

    init_db(app)


def app_get(path, get_data=False):
    """
    Return the result of getting an endpoint from app.
    """
    with app.test_client() as t:
        cred = base64.b64encode(f":{SECRET_KEY}".encode()).decode()
        resp = t.get(path, headers={"Authorization": "Basic {}".format(cred)})
        return resp.data.decode() if get_data else resp.status_code


class TestIntegration(unittest.TestCase):
    """ Test using the database. """

    def test_add_member(self):
        """ Test adding members to the database. """
        reset_db()
        url = "/add_member/?name=Erik+Mattfolk&testing=yes&"

        self.assertEqual(app_get(f"{url}id=erima882"), 200)
        self.assertEqual(app_get(f"{url}id=erima882"), 400)
        self.assertEqual(app_get(f"{url}id=erima82"), 400)

        self.assertEqual(app_get(f"{url}id=erima883&email=yeet&"), 400)
        self.assertEqual(app_get(f"{url}id=erima883&email=yeet@os.net&"), 200)

        self.assertEqual(app_get(f"{url}id=erima884&joined=20-5-1&"), 400)
        self.assertEqual(app_get(f"{url}id=erima884&joined=2020-5-1&"), 200)

        self.assertEqual(app_get(f"{url}id=erima885&receive_email=yes&"), 400)
        self.assertEqual(app_get(f"{url}id=erima885&receive_email=1&"), 200)


    def test_metrics(self):
        """ Test getting metrics about the database. """
        reset_db()
        url = "/metrics/"

        resp = json.loads(app_get(url, get_data=True))
        self.assertEqual(resp["active_members"], 0)
        self.assertEqual(resp["member_count"], 0)
        self.assertEqual(resp["members"], [])

        app_get("/add_member/?id=erima882&name=Erik+Mattfolk&testing=yes")

        resp = json.loads(app_get(url, get_data=True))
        self.assertEqual(resp["active_members"], 1)
        self.assertEqual(resp["member_count"], 1)
        self.assertEqual(len(resp["members"]), 1)

        app_get("/modify/?id=erima882&field=renewed&new=2019-01-01")

        resp = json.loads(app_get(url, get_data=True))
        self.assertEqual(resp["active_members"], 0)
        self.assertEqual(resp["member_count"], 1)
        self.assertEqual(len(resp["members"]), 1)


class TestValidation(unittest.TestCase):
    """ Test various utility used for input validation """

    def test_is_int(self):
        """ Test int validation """
        self.assertTrue(is_int("123"))
        self.assertTrue(is_int("9"))
        self.assertFalse(is_int("abc"))
        self.assertFalse(is_int("5.69"))


    def test_is_pnr(self):
        """ Test personal number validation """
        self.assertTrue(is_pnr("7402174820"))
        self.assertFalse(is_pnr("a"))
        self.assertFalse(is_pnr("123123123"))
        self.assertFalse(is_pnr("7402174821"))


    def test_is_liuid(self):
        """ Test liuid validation """
        self.assertTrue(is_liuid("yeeto420"))
        self.assertTrue(is_liuid("liud123"))
        self.assertFalse(is_liuid("a"))
        self.assertFalse(is_liuid("12345"))
        self.assertFalse(is_liuid("justastring"))


    def test_is_id(self):
        """ Test id validation """
        self.assertTrue(is_id("7402174820"))
        self.assertTrue(is_id("yeeto420"))
        self.assertFalse(is_id("7402174821"))
        self.assertFalse(is_id("justastring"))


    def test_is_email(self):
        """ Test email validation """
        self.assertTrue(is_email("generic.email@emails.com"))
        self.assertFalse(is_email("notemail"))


    def test_is_date(self):
        """ Test date validation """
        self.assertTrue(is_date("2020-03-01"))
        self.assertTrue(is_date("2019-12-31"))
        self.assertFalse(is_date("19-12-31"))
        self.assertFalse(is_date("2019/12/31"))
        self.assertFalse(is_date("100"))


    def test_is_bool(self):
        """ Test sqlite3 bool validation """
        self.assertTrue(is_bool(0))
        self.assertTrue(is_bool(1))
        self.assertTrue(is_bool("0"))
        self.assertTrue(is_bool("1"))
        self.assertFalse(is_bool(2))
        self.assertFalse(is_bool("2"))


    def test_member_to_dict(self):
        """ Test member to dict/JSON """
        member = ("liuid123", "Liu Id", "liu@liu.se", "1990-01-01", "2020-02-31", "1")
        self.assertEqual(
            member_to_dict(member),
            {
                "id": "liuid123",
                "name": "Liu Id",
                "email": "liu@liu.se",
                "joined": "1990-01-01",
                "renewed": "2020-02-31",
                "receive_email": "1"
            }
        )


if __name__ == "__main__":
    unittest.main()
