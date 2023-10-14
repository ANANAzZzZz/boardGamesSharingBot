PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Boardgame;
DROP TABLE IF EXISTS Courier;
DROP TABLE IF EXISTS Owner;
DROP TABLE IF EXISTS Renter;
DROP TABLE IF EXISTS Order_info;
DROP TABLE IF EXISTS Boardgame_in_circulation;

CREATE TABLE Boardgame( 
"ID" INTEGER PRIMARY KEY,
"Status" VARCHAR(30),
"Name" VARCHAR(30),
"Description" VARCHAR(30),
"Middle_game_time" TIME,
"Min_players" INTEGER,
"Max_players" INTEGER,
"Age" INTEGER,
"Rools" VARCHAR(30),
"Image" VARCHAR(30),
"Rating" FLOAT,
"Price_per_day" MONEY,
"Base_cost" MONEY,
"Complexity" FLOAT,
"Category" VARCHAR(30));

CREATE TABLE Renter(
"FIO" VARCHAR(30),
"ID" INTEGER PRIMARY KEY,
"Rating" FLOAT);

CREATE TABLE Owner(
"FIO" VARCHAR(30),
"ID" INTEGER PRIMARY KEY,
"Rating" FLOAT);

CREATE TABLE Boardgame_in_circulation(
"ID_Renter" INTEGER REFERENCES Renter("ID") ON DELETE CASCADE ON UPDATE CASCADE,
"ID_boardgame" INTEGER REFERENCES Boardgame("ID") ON DELETE CASCADE ON UPDATE CASCADE,
"ID_Owner" INTEGER REFERENCES Owner("ID")ON DELETE CASCADE ON UPDATE CASCADE,
"Status_boardgame" VARCHAR(30),
"Boardgame_state" VARCHAR(30),
PRIMARY KEY("ID_renter","ID_boardgame","ID_Owner"));

CREATE TABLE Order_info(
"ID" INTEGER PRIMARY KEY,
"Status" VARCHAR(30),
"Order_time" Time,
"Addres_recive" VARCHAR(30),
"Addres_send"VARCHAR(30),
"ID_renter" INTEGER, 
"ID_boardgame" INTEGER, 
"ID_owner" INTEGER,
"ID_courier" INTEGER REFERENCES Courier("ID")ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY("ID_renter", "ID_boardgame", "ID_owner") REFERENCES Boardgame_in_circulation("ID_Renter", "ID_boardgame", "ID_Owner") ON DELETE CASCADE ON UPDATE CASCADE);

CREATE TABLE Courier(
"FIO" VARCHAR(30),
"ID" INTEGER PRIMARY KEY,
"Rating" FLOAT);

INSERT INTO Courier("FIO", "ID","Rating") VALUES 
('ГУАП',1,2.2),
('ИТМО',2,3.3);
