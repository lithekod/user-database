# User database
This is the software that runs the LiTHe kod user database.

## API

| Endpoint       | Description             | Example                             |
|----------------|-------------------------|-------------------------------------|
| `/<link>`      | Access generated links  | `/DELETE_fjU7y5LNwS9Ewn08AjUTWjWip` |
| `/add_member/` | Add members to database | `curl -u :ADMIN_PASSWORD 'localhost:5000/add_member/?id=liuid123&name=Per%20Encode&email=id%40liu.se'` |
