DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
user_name TEXT,
fecha_creacion TEXT,
nombre TEXT,
mail TEXT,
numero_documento TEXT,
telefono TEXT,
type_id INTEGER
);

DROP TABLE IF EXISTS reservas;
CREATE TABLE reservas (
reserva_id INTEGER PRIMARY KEY AUTOINCREMENT,
room_id INTEGER,
fecha_inicio_reserva TEXT,
fecha_fin_reserva TEXT,
tomador_reserva_id INTEGER,
numero_huespedes INTEGER,
FOREIGN KEY (room_id) REFERENCES habitaciones(room_id),
FOREIGN KEY (tomador_reserva_id) REFERENCES usuarios (user_id)

);
DROP TABLE IF EXISTS habitaciones;
CREATE TABLE habitaciones (
room_id INTEGER PRIMARY KEY AUTOINCREMENT,
numero_habitacion TEXT,
numero_huespedes INTEGER,
numero_camas INTEGER,
calificacion REAL
);

DROP TABLE IF EXISTS huespedes;
CREATE TABLE huespedes (
reserva_id INTEGER PRIMARY KEY,
numero_documento TEXT,
nombre TEXT,
mail TEXT,
FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id)
);

DROP TABLE IF EXISTS contrasenas;
CREATE TABLE contrasenas(
user_id INTEGER PRIMARY KEY,
user_name TEXT,
password_hash TEXT,
password_salt TEXT,
FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
);

DROP TABLE IF EXISTS tipo_usuario;
CREATE TABLE tipo_usuario(
type_id INTEGER PRIMARY KEY,
type_name TEXT
);


DROP TABLE IF EXISTS calificaciones;
CREATE TABLE calificaciones(
reserva_id INTEGER PRIMARY KEY,
room_id INTEGER,
fecha_calificacion TEXT,
comentario TEXT,
calificacion REAL
);
