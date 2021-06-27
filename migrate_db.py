# This script updates the database to the latest version.
# It assumes the database has been initialized.
from app import app
from db import get_db

# List of functions that migrate the database.
# They return the resulting version number.
migrations = []

if __name__ == "__main__":
    with app.app_context():
        db = get_db()

        version = db.execute("SELECT version FROM version").fetchone()[0]
        while version != app.config["DATABASE_VERSION"]:
            version = migrations[version](db)

        db.execute("UPDATE version SET version=?", (version,))
        db.commit()
