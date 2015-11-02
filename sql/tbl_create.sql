
drop table if exists Contain;
drop table if exists Photo;
drop table if exists Album;
drop table if exists User;

CREATE TABLE User
(
  username VARCHAR(20) NOT NULL,
  firstname VARCHAR(20) NOT NULL,
  lastname VARCHAR(20) NOT NULL,
  password VARCHAR(20),
  email VARCHAR(40) NOT NULL,
  PRIMARY KEY (username)
);

CREATE TABLE Album
(
  albumid INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(50) NOT NULL,
  created datetime NOT NULL DEFAULT NOW(),
  lastupdated datetime NOT NULL DEFAULT NOW(),
  username VARCHAR(20) NOT NULL,
  access VARCHAR(10) NOT NULL,
  PRIMARY KEY (albumid),
  FOREIGN KEY (username) REFERENCES User(username)
);


CREATE TABLE Photo
(
  picid VARCHAR(40) NOT NULL,
  url VARCHAR(255),
  format VARCHAR(3),
  date datetime NOT NULL DEFAULT NOW(),
  PRIMARY KEY (picid)
);

CREATE TABLE Contain
(
  albumid INT NOT NULL,
  picid VARCHAR(40) NOT NULL,
  caption VARCHAR(255),
  sequencenum INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (albumid, picid),
  FOREIGN KEY (albumid) REFERENCES Album(albumid),
  FOREIGN KEY (picid) REFERENCES Photo(picid),
  UNIQUE (sequencenum)
);

CREATE TABLE AlbumAccess
(
  albumid INT NOT NULL,
  username VARCHAR(20) NOT NULL,
  PRIMARY KEY (albumid, username),
  FOREIGN KEY (albumid) REFERENCES Album(albumid),
  FOREIGN KEY (username) REFERENCES User(username)
);