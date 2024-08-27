INSERT INTO pts.lines SELECT * FROM ptd.lines;
INSERT INTO pts.timetables SELECT * FROM ptd.timetables;
INSERT INTO pts.stops SELECT coordinates.x, coordinates.y, direction, stop_code, stop_id, stop_name FROM ptd.stops;
INSERT INTO pts.routes SELECT * FROM ptd.routes;
INSERT INTO pts.line_stops 
    SELECT coordinates.x, 
    coordinates.y, 
    direction,
    line_code,
    line_id,
    route_code,
    route_direction,
    route_order,
    stop_code, 
    stop_name FROM ptd.line_stops;