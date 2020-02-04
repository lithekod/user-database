# User database
This is the software that runs the LiTHe kod user database.

## API

| Endpoint       | Description             | Example                                |
|----------------|-------------------------|----------------------------------------|
| `/<link>`      | Access generated links  | `URL/DELETE_fjU7y5LNwS9Ewn08AjUTWjWip` |
| `/add_member/` | Add members to database | `curl -u :SECRET_KEY 'URL/add_member/?id=liuid123&name=Per%20Encode&email=id%40liu.se&joined=2020-01-01&receive_email=1'` |
| `/metrics/`    | Get database metrics    | `curl -u :SECRET_KEY URL/metrics/` |
| `/email_members/` | Send emails to members | `curl -u :SECRET_KEY 'URL/email_members/?subject=Hello+There&htmlfile=template.txt&receivers=default'` |
