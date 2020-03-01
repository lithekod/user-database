import unittest

from util import *

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
