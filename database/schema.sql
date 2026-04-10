


-- sqlite schema for the home database


PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS floors;
DROP TABLE IF EXISTS houses;
DROP TABLE IF EXISTS users;
-- create users table to store user information
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	full_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE
);
-- create houses table to store house information
CREATE TABLE houses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	address TEXT,
	FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
-- create floors table to store floor information for each house
CREATE TABLE floors (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	house_id INTEGER NOT NULL,
	level_number INTEGER NOT NULL,
	name TEXT NOT NULL,
	FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
	UNIQUE(house_id, level_number)
);
--create rooms table to store room information for each floor
CREATE TABLE rooms (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	floor_id INTEGER NOT NULL,
	name TEXT NOT NULL,
	room_type TEXT NOT NULL,
	FOREIGN KEY (floor_id) REFERENCES floors(id) ON DELETE CASCADE,
	UNIQUE (floor_id, name)
);
-- create devices table to store information about smart devices in each room
CREATE TABLE devices (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	room_id INTEGER NOT NULL,
	name TEXT NOT NULL UNIQUE,
	device_type TEXT NOT NULL,
	status TEXT NOT NULL DEFAULT 'off' CHECK (status IN ('on', 'off')),
	power_watts INTEGER,
	last_seen TEXT,
	FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);
-- insert some sample data to test the database and queries
INSERT INTO users (full_name, email)
-- example --> i just put my name
VALUES ('Melinda Tran', 'melinda@gmail.com');
INSERT INTO houses (user_id, name, address)
VALUES (1,'Main Home', '1 Smart St');
-- add floors to the house
INSERT INTO floors (house_id, level_number, name)
VALUES
	(1,0,'Ground Floor'),
	(1,1,'Upper Floor');
--add rooms to the floors
INSERT INTO rooms (floor_id, name, room_type)
VALUES
	(1,'Living Room','living'),
	(1,'Kitchen','kitchen'),
	(2, 'Bedroom','bedroom');
