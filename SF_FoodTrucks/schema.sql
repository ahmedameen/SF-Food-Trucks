DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);
