CREATE INDEX timetables_line_code ON timetables(line_code);
CREATE INDEX timetables_route_code ON timetables(route_code);

CREATE INDEX line_stops_line_code ON line_stops(line_code);
CREATE INDEX line_stops_route_code ON line_stops(route_code);

CREATE INDEX routes_line_code ON routes(line_code);
CREATE INDEX routes_route_code ON routes(route_code);

CREATE UNIQUE INDEX stops_stop_code ON stops(stop_code);

CREATE UNIQUE INDEX lines_line_code ON lines(line_code);
