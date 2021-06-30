# User database

This is LiTHe kod's user database.

## Getting started

```sh
git clone git@github.com:lithekod/user-database.git
cd user-database
git clone git@github.com:lithekod/emails.git
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Using the database

All of the functionality is available at [the
website](https://lithekod.lysator.liu.se). To add new email templates, simply
push them to the [emails](https://github.com/lithekod/emails) repo and they
will show up on the website.

## API

If, for some reason, you want to access the database from the commandline, you
can use the API. This table only provides the endpoints, not the arguments
required. See [#22](https://github.com/lithekod/user-database/issues/22).

| Endpoint          | Description                            |
|-------------------|----------------------------------------|
| `/<link>`         | Access generated links                 |
| `/add_member/`    | Add member to database                 |
| `/modify/`        | Modify member data                     |
| `/email_members/` | Send emails to members                 |
| `/email_list/`    | Get an email list                      |
| `/members/`       | Get all or individual members          |
| `/member_count/`  | Get number of total and active members |
