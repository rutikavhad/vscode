-- Metro Simulation Schema

CREATE TABLE IF NOT EXISTS stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    color TEXT NOT NULL DEFAULT '#FF0000'
);

CREATE TABLE IF NOT EXISTS line_stations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_id INTEGER NOT NULL,
    station_id INTEGER NOT NULL,
    sequence INTEGER NOT NULL,
    FOREIGN KEY (line_id) REFERENCES lines(id),
    FOREIGN KEY (station_id) REFERENCES stations(id)
);

CREATE TABLE IF NOT EXISTS station_intervals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_station_id INTEGER NOT NULL,
    to_station_id INTEGER NOT NULL,
    travel_time_minutes REAL NOT NULL,
    FOREIGN KEY (from_station_id) REFERENCES stations(id),
    FOREIGN KEY (to_station_id) REFERENCES stations(id)
);

CREATE TABLE IF NOT EXISTS line_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    line_id INTEGER NOT NULL UNIQUE,
    start_time TEXT NOT NULL DEFAULT '05:00',
    end_time TEXT NOT NULL DEFAULT '23:00',
    frequency_minutes REAL NOT NULL DEFAULT 6,
    turnaround_minutes REAL NOT NULL DEFAULT 8,
    FOREIGN KEY (line_id) REFERENCES lines(id)
);
