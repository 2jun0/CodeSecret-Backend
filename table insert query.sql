DROP TABLE `code_secret`.`account`, `code_secret`.`file`, `code_secret`.`repository`, `code_secret`.`secret_key`;

create table account (
  id varchar(12) NOT NULL,
  password varchar(100) NOT NULL,
  githubUsername varchar(100) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE repository (
  fullname varchar(512) NOT NULL,
  name varchar(100) NOT NULL,
  lastCommitDate datetime DEFAULT NULL,
  lastCommitSha varchar(50) DEFAULT NULL,
  owner varchar(12) NOT NULL,
  PRIMARY KEY (fullname),
  FOREIGN KEY (owner) REFERENCES account (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE file (
  fullname varchar(512) NOT NULL,
  name varchar(100) NOT NULL,
  repoFullname varchar(512) NOT NULL,
  lastCommitSha varchar(50) DEFAULT NULL,
  PRIMARY KEY (fullname),
  FOREIGN KEY (repoFullname) REFERENCES repository (fullname) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE secret_key (
  y int NOT NULL,
  x int NOT NULL,
  fileFullname varchar(512) NOT NULL,
  content varchar(100) NOT NULL,
  PRIMARY KEY (x, y, fileFullname)
);