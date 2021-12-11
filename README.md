# User database

This is LiTHe kod's user database.

## Quickstart

```sh
git clone git@github.com:lithekod/user-database.git
cd user-database
make
```

## Using the database

Most of the functionality is available at [the
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

| Parameters   | Description                  | Required |
| ------------ | ---------------------------- | :------: |
| `id`         | Liu-id                       |   yes    |
| `name`       | Full name                    |   yes    |
| `email`      | Email                        |    no    |
| `joined`     | ISO-Date (YYYY-mm-dd)        |    no    |
| `subscribed` | Subscription status (0 or 1) |    no    |

#### Example

```sh
$ curl -u :SECRECT_KEY "https://lithekod.lysator.liu.se/add_member/?id=liuid123&name=Lius+Idus"
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
$ curl -u :SECRECT_KEY "https://lithekod.lysator.liu.se/modify/?id=liuid123&field=name&new=Blargh"
Successfully set 'name' to 'Blargh' for 'liuid123'
```

### `/email_members/`

Send emails to members. Receivers is one of `default`, `all`, `inactive` or a
space separated list of liu-ids.

| Parameters  | Description       | Required |
| ----------- | ----------------- | :------: |
| `receivers` | Receivers         |   yes    |
| `subject`   | Email subject     |   yes    |
| `template`  | The email to send |   yes    |

#### Example

```sh
$ curl -u :SECRECT_KEY "https://lithekod.lysator.liu.se/email_members/?receivers=liuid123&subject=test&template=general/welcome.tpl"
Emails are being sent!
```

### `/email_list/`

Get an email list. Receivers are the same as for `/email_members/`.

| Parameters  | Description | Required |
| ----------- | ----------- | :------: |
| `receivers` | Receivers   |   yes    |

#### Example

```sh
$ curl -u :SECRECT_KEY "https://lithekod.lysator.liu.se/email_list/?receivers=all"
[...] # A JSON list of the users, the format is unspecified.
```

### `/members/`

Get all or individual members. Basically a dump of the database.

| Parameters | Description | Required |
| ---------- | ----------- | :------: |
| `id`       | Liu-id      |    no    |

#### Example

```sh
$ curl -u :SECRECT_KEY "https://lithekod.lysator.liu.se/members/"
[...] # A JSON list of the users and the links
```

### `/member_count/`

Get number of total and active members. Does not require authentication.

#### Example

```sh
$ curl "https://lithekod.lysator.liu.se/member_count/"
{"active_members":25,"total_members":110}
```
