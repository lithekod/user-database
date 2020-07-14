import datetime

def random_string(length):
    """
    Return a random cryptographically safe string of given length.
    There are 62 possible characters, so there are 62^n possible strings of
    length n.
    """
    s = ""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    while len(s) < length:
        char_index = ord(urandom(1))
        if char_index < len(chars):
            s += chars[char_index]

    return s


def is_int(string):
    """ Test if a string can be interpreted as an int. """
    try:
        int(string)
        return True
    except:
        return False


def is_pnr(l):
    """
    Test if a sequence l is a valid swedish personal number.
    TDDE23 labb 2 <3
    """
    if len(l) != 10 or not is_int(l): return False
    l = [int(i) for i in l]
    ctrl = l.pop()
    for i in range(0, len(l), 2): l[i] *= 2
    s = sum([sum([int(j) for j in str(i)]) for i in l])
    return (s + ctrl) % 10 == 0


def is_liuid(liuid):
    """ Test if a string is a liuid. """
    return len(liuid) <= 8 and liuid[:-3].islower() and is_int(liuid[-3:])


def is_id(id):
    """ Test if id is either a liuid or a swedish personal number. """
    return is_liuid(id) or is_pnr(id)


def is_email(email):
    """ Test (not very thoroughly) if email is a valid email. """
    return "@" in email


def is_date(date):
    """ Test if date is a properly formatted date. """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_bool(b):
    """ Test if b can be interpreted as a bool by sqlite3. """
    return b in ["0", "1", 0, 1]


def member_to_dict(member):
    liuid, name, email, joined, renewed, receive_email = member
    return {
        "id": liuid,
        "name": name,
        "email": email,
        "joined": joined,
        "renewed": renewed,
        "receive_email": receive_email
    }


