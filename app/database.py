import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        con = sqlite3.connect('app/mydatabase.db')
        return con
    except Error:
        print(Error)


def connect_execute(strsql, values):
    con = sql_connection()
    cursor_Obj = con.cursor()
    cursor_Obj.execute(strsql, values)
    last_row_id = cursor_Obj.lastrowid
    con.commit()
    con.close()
    return last_row_id


def sql_insert_user(user_name: str, fecha_creacion: str, nombre: str, mail: str, numero_documento: str, telefono: str, type_id: int):
    strsql, value = "INSERT INTO usuarios (user_name, fecha_creacion, nombre, mail, numero_documento, telefono, type_id) VALUES (?,?,?,?,?,?,?)", (user_name, fecha_creacion, nombre, mail, numero_documento, telefono, type_id)
    last_row_id = connect_execute(strsql, value)
    return last_row_id


def sql_insert_habitacion(numero_habitacion: str, numero_huespedes: int, numero_camas: int, calificacion: float):
    strsql, value = "INSERT INTO habitaciones (numero_habitacion, numero_huespedes, numero_camas, calificacion) VALUES (?,?,?,?)", (numero_habitacion, numero_huespedes, numero_camas, calificacion)
    connect_execute(strsql, value)


def sql_insert_tipo_usuario(user_id: int, ind_usuario_final: int, ind_admon: int, ind_superadmon: int):
    strsql, value = "INSERT INTO tipo_usuario (user_id, ind_usuario_final, ind_admon, ind_superadmon) VALUES (?,?)",
    (user_id, ind_usuario_final, ind_admon, ind_superadmon)

    connect_execute(strsql, value)


def sql_insert_reserva(room_id: int, fecha_inicio_reserva: str, fecha_fin_reserva: str, tomador_reserva_id: int):
    strsql, value = "INSERT INTO reservas (room_id, fecha_inicio_reserva, fecha_fin_reserva, tomador_reserva_id) VALUES (?,?,?,?)",
    (room_id, fecha_inicio_reserva, fecha_fin_reserva, tomador_reserva_id)

    last_row_id = connect_execute(strsql, value)
    return last_row_id


def sql_select_reserva():
    strsql = "SELECT * FROM reservas;"
    con = sql_connection()
    cursor_Obj = con.cursor()
    cursor_Obj.execute(strsql)
    reservas = cursor_Obj.fetchall()
    con.close()
    return reservas


def sql_insert_huesped(reserva_id: int, numero_documento: str, nombre: str, mail: str):
    strsql, value = "INSERT INTO reservas (reserva_id, numero_documento, nombre, mail) VALUES (?,?,?,?)",
    (reserva_id, numero_documento, nombre, mail)

    connect_execute(strsql, value)


def sql_insert_calificaciones(reserva_id: int, room_id: int, fecha_calificacion: str, comentario: str, calificacion: float):
    strsql, value = "INSERT INTO reservas (reserva_id, room_id, fecha_calificacion, comentario, calificacion) VALUES (?,?,?,?,?)",
    (reserva_id, room_id, fecha_calificacion, comentario, calificacion)

    connect_execute(strsql, value)


def sql_insert_contrasena(user_id: int, user_name: str, password_hash: str):
    strsql, value = "INSERT INTO contrasenas (user_id, user_name, password_hash) VALUES (?,?,?)", (user_id, user_name, password_hash)
    connect_execute(strsql, value)

# -------------------------------------------------------------------------------------
# Crear una cuenta.
# El usuario suministra un user_name, password, confirmaci??n de password y un c??digo
# de creaci??n (?)

# despu??s de dar click en el bot??n registrar:
# 1. Consultar la tabla de usuarios.


def sql_existe_usuario(user_name: str, mail: str):
    strsql, value = "SELECT COUNT(*) FROM usuarios where user_name = ? or mail = ?;", (user_name, mail)

    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql, value)
        flag = cursor_Obj.fetchone()
        # con.commit()
    return flag[0]

# 2. Si el user_name existe o el email existe, se muestra un error. De lo contrario
# se ejecuta sql_insert_user el cual retorna  last_row_id. A continuaci??n se actualiza la tabla
# de contrase??as. # MIRAR M??TODO PARA GUARDAR USUARIO/CONTRASE??A. DEBER??A SER AL REV??S?

# -----------------------------------------------------------------------------------------------------------

# Para generar o editar una reserva el usuario debe suministrar una fecha y nosotros devolvemos
# las habitaciones que est??n disponibles

def sql_consultar_usuario(user_name: str):
    strsql, value = "SELECT * FROM contrasenas where user_name = ?", (user_name,)
    
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql, value)
        flag = cursor_Obj.fetchone()
        # con.commit()
    return flag

def sql_consultar_usuario_name(user_name: str):
    strsql, value = "SELECT * FROM usuarios where user_name = ?", (user_name,)
    
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql, value)
        flag = cursor_Obj.fetchone()
        # con.commit()
    return flag

def sql_consultar_usuarios():
    strsql = "SELECT * FROM usuarios"
    
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        flag = cursor_Obj.fetchall()
        # con.commit()
    return flag

def sql_consultar_type_usuarios():
    strsql = "SELECT * FROM tipo_usuario"
    
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        flag = cursor_Obj.fetchall()
        # con.commit()
    return flag

def sql_consultar_habitaciones():
    strsql = "SELECT * FROM habitaciones"
    
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        flag = cursor_Obj.fetchall()
        # con.commit()
    return flag

def sql_select_available_rooms(fecha_izq: str, fecha_der: str):
    strsql, value = "SELECT DISTINCT * FROM habitaciones INNER JOIN reservas ON (reservas.room_id = habitaciones.room_id) WHERE (reservas.fecha_fin_reserva <= ? AND reservas.fecha_inicio_reserva >= ?);",
    (fecha_izq, fecha_der)

    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql, value)
        list_rows_rooms = cursor_Obj.fetchall()
        # con.commit()
    return list_rows_rooms


def sql_update_reserva(reserva_id: int, room_id: int, fecha_inicio_reserva: str, fecha_fin_reserva: str):
    strsql, value = "UPDATE reserva SET room_id = ?, fecha_inicio_reserva= ?, fecha_fin_reserva= ? WHERE reserva_id=?",
    (room_id, fecha_inicio_reserva, fecha_fin_reserva, reserva_id)

    with sql_connection() as con:
        cur = con.cursor()
        cur.execute(strsql, value)
        con.commit()


def sql_insert_calificacion(reserva_id, room_id, fecha_calificacion, comentario, calificacion):
    strsql, value = "INSERT INTO calificaciones (reserva_id, room_id, fecha_calificacion, comentario, calificacion) VALUES (?,?, ?, ?,?)",
    (reserva_id, room_id, fecha_calificacion, comentario, calificacion)

    connect_execute(strsql)


def count_number_calif_room(room_id: int):
    strsql, value = "SELECT COUNT(reserva_id) FROM calificaciones WHERE room_id = ? ", room_id
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql, value)
        conteo = cursor_Obj.fetchone()
        # con.commit()
    return conteo


def update_room_score(room_id: int, new_calificacion: float):
    # traer calificacion actual
    strsql, value = "SELECT calificacion FROM calificaciones WHERE room_id = ? ", room_id
    with sql_connection() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql, value)
        calificacion_prom = cursor_Obj.fetchone()
    conteo = count_number_calif_room(room_id)
    new_calif_prom = (conteo/(conteo+1))*calificacion_prom + \
        (new_calificacion / (conteo + 1))
    strsql, value = "UPDATE habitacion SET calificacion = ? WHERE room_id=?",
    (new_calif_prom, room_id)

    with sql_connection() as con:
        cur = con.cursor()
        cur.execute(strsql, value)
        con.commit()
