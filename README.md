# User database

This is LiTHe kod's user database.

## Quickstart

```sh
git clone git@github.com:lithekod/user-database.git
cd user-database
make
```

## Using the database

All of the functionality is available at [the
website](https://lithekod.lysator.liu.se). To add new email templates, simply
push them to the [emails](https://github.com/lithekod/emails) repo and they
will show up on the website.

## API

If you want to access the database from the commandline or do development, you
have to use the API.

### Overview

| Endpoint          | Description                            |
| ----------------- | -------------------------------------- |
| `/<link>`         | Access generated links                 |
| `/add_member/`    | Add member to database                 |
| `/modify/`        | Modify member data                     |
| `/email_members/` | Send emails to members                 |
| `/email_list/`    | Get an email list                      |
| `/members/`       | Get all or individual members          |
| `/member_count/`  | Get number of total and active members |

### `/<link>`

Access generated links. They look something like `SHOW_hahu928bo` and are best
opened in the browser.

#### Example

```
https://lithekod.lysator.liu.se/SHOW_hahu928bo
```

### `/add_member/`

Add a member to to database.

| Parameters   | Description         | Required |
| ------------ | ------------------- | :------: |
| `id`         | Liu-id              |   yes    |
| `name`       | Full name           |   yes    |
| `email`      | Email               |    no    |
| `joined`     | ISO-Date            |    no    |
| `subscribed` | Subscription status |    no    |

#### Example

```sh
$ curl -u :SECRECT_KEY https://lithekod.lysator.liu.se/add_member/?id=liuid123&name=Lius+Idus
Successfully added user with id: liuid123.
```

### `/modify/`

Modify member data. The modifiable fields are the parameters to `/add_member/`.

| Parameters | Description     | Required |
| ---------- | --------------- | :------: |
| `id`       | Liu-id          |   yes    |
| `field`    | Field to modify |   yes    |
| `new`      | New value       |   yes    |

#### Example

```sh
$ curl -u :SECRECT_KEY https://lithekod.lysator.liu.se/modify/?id=liuid123&field=name&new=Blargh
Successfully set 'name' to 'Blargh' for 'liuid123'
```
