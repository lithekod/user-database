INSERT_NEW_MEMBER = "INSERT INTO member VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)"
INSERT_NEW_LINK = "INSERT INTO link VALUES (?, ?, ?, CURRENT_TIMESTAMP)"
INSERT_NEW_TOKEN = "INSERT INTO token VALUES (?, ?, CURRENT_TIMESTAMP)"

SELECT_MEMBER = "SELECT * FROM member"
SELECT_MEMBER_ID = "SELECT id FROM member"
SELECT_LINK_WITH_URL = "SELECT * FROM link WHERE url=?"
SELECT_LINK_MEMBERID_LINK = "SELECT member_id, url FROM link"
SELECT_MEMBER_WITH_ID = "SELECT * FROM member WHERE id=?"
SELECT_MEMBER_ACTIVE = " ".join([
    "SELECT * FROM member",
    "WHERE strftime('%Y', renewed) = strftime('%Y', CURRENT_TIMESTAMP)",
])
SELECT_MEMBER_INACTIVE = SELECT_MEMBER_ACTIVE.replace("=", "!=")
SELECT_MEMBER_SUBSCRIBED = "SELECT * FROM member WHERE subscribed=1"
SELECT_TOKEN_WITH_ID = "SELECT * FROM token WHERE id=?"

UPDATE_MEMBER_RENEW = "UPDATE member SET renewed=CURRENT_TIMESTAMP WHERE id=?"
UPDATE_MEMBER_UNSUBSCRIBE = "UPDATE member SET subscribed=0 WHERE id=?"
UPDATE_MEMBER_FIELD = "UPDATE member SET {}=? WHERE id=?"

DELETE_LINK = "DELETE FROM link"
DELETE_LINK_WITH_IDS = "DELETE FROM link WHERE member_id=? AND action_id=?"
DELETE_LINK_WITH_MEMBER_ID = "DELETE FROM link WHERE member_id=?"
DELETE_MEMBER_WITH_ID = "DELETE FROM member WHERE id=?"
