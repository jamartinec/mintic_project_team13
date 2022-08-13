import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con=sqlite3.connect('baseDatos.db')
        return con
    except Error:
        print(Error)


def connect_execute(strsql):
    con = sql_connection()
    cursor_Obj = con.cursor()

    cursor_Obj.execute(strsql)
    last_row_id= cursor_Obj.lastrowid
    con.commit()
    con.close()
    return last_row_id

def sql_insert_user(user_name: str, fecha_creacion: str, nombre: str,
                    mail: str, numero_documento: str, telefono: str):

    strsql= ("INSERT INTO usuarios (user_name, fecha_creacion, nombre, mail, numero_documento,telefono) VALUES (?,?,?,?,?,?)",
             (user_name, fecha_creacion, nombre, mail, numero_documento, telefono)
             )

    last_row_id = connect_execute(strsql)
    return last_row_id

def sql_insert_habitacion(numero_habitacion: str, numero_huespedes: int, numero_camas: int, calificacion: float):

    strsql = ("INSERT INTO habitaciones (numero_habitacion, numero_huespedes, numero_camas, calificacion) VALUES (?,?,?,?)",
              (numero_habitacion, numero_huespedes, numero_camas, calificacion)
              )
    connect_execute(strsql)

def sql_insert_tipo_usuario(user_id: int, ind_usuario_final: int, ind_admon: int, ind_superadmon: int):
    strsql = ("INSERT INTO tipo_usuario (user_id, ind_usuario_final, ind_admon, ind_superadmon) VALUES (?,?)",
              (user_id, ind_usuario_final, ind_admon, ind_superadmon)
              )
    connect_execute(strsql)

def sql_insert_reserva(room_id: int, fecha_inicio_reserva: str, fecha_fin_reserva: str, tomador_reserva_id: int):
    strsql = ("INSERT INTO reservas (room_id, fecha_inicio_reserva, fecha_fin_reserva, tomador_reserva_id) VALUES (?,?,?,?)",
              (room_id, fecha_inicio_reserva, fecha_fin_reserva, tomador_reserva_id)
              )
    last_row_id = connect_execute(strsql)
    return last_row_id


def sql_insert_huesped(reserva_id: int, numero_documento: str, nombre: str, mail: str):
    strsql = (
        "INSERT INTO reservas (reserva_id, numero_documento, nombre, mail) VALUES (?,?,?,?)",
        (reserva_id, numero_documento, nombre, mail)
    )
    connect_execute(strsql)

def sql_insert_calificaciones(reserva_id: int, room_id: int, fecha_calificacion: str, comentario: str, calificacion: float):
    strsql = (
        "INSERT INTO reservas (reserva_id, room_id, fecha_calificacion, comentario, calificacion) VALUES (?,?,?,?,?)",
        (reserva_id, room_id, fecha_calificacion, comentario, calificacion)
    )
    connect_execute(strsql)

def sql_insert_contrasena(user_id: int, password: str):
    strsql = (
        "INSERT INTO reservas (user_id, password) VALUES (?,?)",
        (user_id, password)
    )
    connect_execute(strsql)

#-------------------------------------------------------------------------------------
# Crear una cuenta.
# El usuario suministra un user_name, password, confirmación de password y un código
# de creación (?)

# después de dar click en el botón registrar:
# 1. Consultar la tabla de usuarios.
def sql_existe_usuario(user_name: str, mail: str):
    strsql = (
        "EXISTS(SELECT * FROM usuarios where user_name = ? or mail = ?)", (user_name, mail)
    )
    with sql_connection()() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        flag = cursor_Obj.fetchone()
        #con.commit()
    return flag

#2. Si el user_name existe o el email existe, se muestra un error. De lo contrario
# se ejecuta sql_insert_user el cual retorna  last_row_id. A continuación se actualiza la tabla
# de contraseñas. # MIRAR MÉTODO PARA GUARDAR USUARIO/CONTRASEÑA. DEBERÍA SER AL REVÉS?

#-----------------------------------------------------------------------------------------------------------

# Para generar o editar una reserva el usuario debe suministrar una fecha y nosotros devolvemos
# las habitaciones que estén disponibles

def sql_select_available_rooms(fecha_izq: str, fecha_der: str):
    strsql = (
        "SELECT DISTINCT * FROM habitaciones INNER JOIN reservas ON (reservas.room_id = habitaciones.room_id) WHERE (reservas.fecha_fin_reserva <= ?  OR reservas.fecha_inicio_reserva >= ? )",
        (fecha_izq, fecha_der)
    )
    with sql_connection()() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        list_rows_rooms = cursor_Obj.fetchall()
        #con.commit()
    return list_rows_rooms


def sql_update_reserva(reserva_id: int, room_id: int, fecha_inicio_reserva: str, fecha_fin_reserva: str):
    strsql = (
        "UPDATE reserva SET room_id = ?, fecha_inicio_reserva= ?, fecha_fin_reserva= ? WHERE reserva_id=?",
        (room_id, fecha_inicio_reserva, fecha_fin_reserva, reserva_id)
    )
    with sql_connection()() as con:
        cur = con.cursor()
        cur.execute(strsql)
        con.commit()


def sql_insert_calificacion(reserva_id, room_id, fecha_calificacion, comentario, calificacion):
    strsql = (
        "INSERT INTO calificaciones (reserva_id, room_id, fecha_calificacion, comentario, calificacion) VALUES (?,?, ?, ?,?)",
        (reserva_id, room_id, fecha_calificacion, comentario, calificacion)
    )
    connect_execute(strsql)

def count_number_calif_room(room_id: int):
    strsql = ("SELECT COUNT(reserva_id) FROM calificaciones WHERE room_id = ? ", room_id)
    with sql_connection()() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        conteo = cursor_Obj.fetchone()
        #con.commit()
    return conteo



def update_room_score(room_id: int, new_calificacion: float):
    # traer calificacion actual
    strsql = ("SELECT calificacion FROM calificaciones WHERE room_id = ? ", room_id)
    with sql_connection()() as con:
        cursor_Obj = con.cursor()
        cursor_Obj.execute(strsql)
        calificacion_prom = cursor_Obj.fetchone()
    conteo = count_number_calif_room(room_id)
    new_calif_prom = (conteo/(conteo+1))*calificacion_prom + (new_calificacion / (conteo + 1))
    strsql = ("UPDATE habitacion SET calificacion = ? WHERE room_id=?",
              (new_calif_prom, room_id)
              )
    with sql_connection()() as con:
        cur = con.cursor()
        cur.execute(strsql)
        con.commit()
    
