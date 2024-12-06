CREATE TABLE timetables(
    day_type TEXT NOT NULL,
    direction TEXT NOT NULL,
    line_code TEXT,
    route_code TEXT NOT NULL,
    time TEXT NOT NULL
);

CREATE TABLE stops(
    coordinate_x REAL NOT NULL,
    coordinate_y REAL NOT NULL,
    direction TEXT NOT NULL,
    stop_code INT NOT NULL,
    stop_id INT NOT NULL,
    stop_name TEXT
);

CREATE TABLE line_stops(
    line_code TEXT NOT NULL,
    route_code TEXT NOT NULL,
    route_direction TEXT NOT NULL,
    route_order INT NOT NULL,
    stop_code INT NOT NULL
);

CREATE TABLE routes(
    line_code TEXT NOT NULL,
    line_description TEXT,
    line_id INT NOT NULL,
    line_name TEXT NOT NULL,
    route_code TEXT NOT NULL,
    route_description TEXT,
    route_direction TEXT NOT NULL,
    route_id INT NOT NULL,
    route_name TEXT NOT NULL
);

CREATE TABLE lines(
    line_code TEXT NOT NULL,
    line_id INT NOT NULL,
    line_name TEXT NOT NULL
);