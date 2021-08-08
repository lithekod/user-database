# This script updates the database to the latest version.
# It assumes the database has been initialized.
from app import app
from db import get_db

def v1(db):
    """ Update the database from v0 to v1 """
    db.execute("ALTER TABLE member RENAME COLUMN receive_email TO subscribed")
    return 1

def v2(db):
    """ Update the database from v1 to v2 """
    db.execute("DROP TABLE token")
    return 2

# Dict of functions that migrate the database.
# The functions return the resulting version number, allowing us to reach the
# latest version by chaining upgrades together.
migrations = {
    0: v1,
    1: v2,
}

if __name__ == "__main__":
    with app.app_context():
        db = get_db()

        version = db.execute("SELECT version FROM version").fetchone()[0]
        while version != app.config["DATABASE_VERSION"]:
            version = migrations[version](db)

        db.execute("UPDATE version SET version=?", (version,))
        db.commit()
