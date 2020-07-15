/*
Member table
This table contains all of the information we store on members.
*/
CREATE TABLE member
(
    id             VARCHAR(10)  PRIMARY KEY,
    name           VARCHAR(64)  NOT NULL,
    email          VARCHAR(64)  NOT NULL,
    joined         TIME         NOT NULL,
    renewed        TIME         NOT NULL,
    receive_email  BOOLEAN      NOT NULL
);

/*
Action table
The id specifies what a action should do:
    DELETE - Removes a member from the database.
    RENEW - Sets the renewed status of the member to the current date.
    SHOW - Provides a json string with one of the members information.
    UNSUBSCRIBE - Sets the receive_email status to false.
*/
CREATE TABLE action
(
    id  VARCHAR(10) PRIMARY KEY
);

/*
Link table
Spcifies the active links which can be accessed by a member.
*/
CREATE TABLE link
(
    member_id  VARCHAR(10)  NOT NULL,
    action_id  VARCHAR(10)  NOT NULL,
    url        VARCHAR(32)  UNIQUE NOT NULL,
    created    TIME         NOT NULL,
    PRIMARY KEY (member_id, action_id),
    FOREIGN KEY (member_id) REFERENCES member(id),
    FOREIGN KEY (action_id) REFERENCES action(id)
);

/*
Token table
These are tokens used for authentication with the server.
*/
CREATE TABLE token
(
    id        VARCHAR(32)  PRIMARY KEY,
    owner     VARCHAR(64)  NOT NULL,
    issued    TIME         NOT NULL
);
