INSERT INTO own_vsl_sch(line_code, vsl_code, voyage, inb_voyage, eta, eta_time, etd, etd_time, ts_yn, insert_date, insert_user, update_date, update_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

INSERT INTO own_vsl_sch_route(line_code, vsl_code, voyage, route_seq, route_code, eta, eta_time, etd, etd_time, ts_yn, insert_date, insert_user, update_date, update_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

INSERT INTO own_vsl_sch_vessel_name(line_code, vessel_name, vessel_code) VALUES (?, ?, ?);

INSERT INTO own_vsl_sch_iso_port_code(line_code, port_name, iso_port_code)	VALUES (?, ?, ?);