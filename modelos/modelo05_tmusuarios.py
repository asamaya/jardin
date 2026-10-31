from psycopg import connect

# 1.2.- La cadena de conexión con la BD
from modelos.modelo00_bd import cadenaConexion

def get_all_tmniveles():
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    sql = "SELECT pknivel, dnivel FROM tmniveles ORDER BY pknivel;"

    try:
        cursor.execute(sql)
        xresultados = cursor.fetchall()
    except Exception as e:
        print(f"Error al consultar los niveles: {e}")
        xresultados = []

    cursor.close()
    conexion.close()

    return xresultados if isinstance(xresultados, (list, tuple)) else []


def get_all_tmusuarios():
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    sql = """
        SELECT
            u.pknu,
            u.nom_u,
            u.email_u,
            u.foto_u,
            u.nivel_u,
            u.fkcods,
            COALESCE(s.dstatus, 'SIN ESTATUS') AS estatus
        FROM tmusuarios u
        LEFT JOIN tmstatus s ON s.pkcods = u.fkcods
        ORDER BY u.pknu;
    """

    try:
        cursor.execute(sql)
        xresultados = cursor.fetchall()
    except Exception as e:
        print(f"Error al consultar usuarios: {e}")
        xresultados = []

    cursor.close()
    conexion.close()

    # Garantizar que siempre se retorne una lista iterable
    return xresultados if isinstance(xresultados, (list, tuple)) else []


#añadir un usuario a la tabla tmusuarios
def add_tmusuario(xnombre, xemail, xclave, xfoto, xnivel):
    # PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = "INSERT INTO tmusuarios(nom_u, email_u, clave_u, foto_u, nivel_u) VALUES (%s, %s, %s, %s, %s);"
    datos = (xnombre, xemail, xclave, xfoto, xnivel)
    
    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecutar
        conexion.commit()  # Confirma

        # PASO 4 ---> Recuperar los resultados
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultados
        xfilas = 0

    # print("Total de Filas afectadas -----------> " + str(xfilas))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultados
    return xfilas

#buscar un usurio por su nombre
def get_usuario_by_nombre(xnombre):
    # PASO 1 ---> Establecer la conexión con la BD
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = """
        SELECT pknu, nom_u, email_u, foto_u, nivel_u
        FROM tmusuarios
        WHERE nom_u = %s;
    """
    datos = (xnombre,)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecuta
        conexion.commit()  # Confirma

        # PASO 4 ---> Recuperar los resultados
        xresultado = cursor.fetchone()  # fetchone() Un / fetchall() Varios
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultados
        xresultado = None
        xfilas = 0

    # print("Total de Filas afectadas -----------> " + str(xfilas))
    # print("Datos recuperados de la TMUsuarios ---> " + str(xresultado))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultados
    return xresultado 

#modificar un usuario por su pknu
def set_modificar_usuario(xpknu, xnombre, xemail, xclave, xfoto, xnivel):
    # PASO 1 ---> Establecer la conexión con la BD
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = """
        UPDATE tmusuarios
        SET nom_u = %s,
            email_u = %s,
            clave_u = COALESCE(NULLIF(%s, ''), clave_u),
            foto_u = COALESCE(%s, foto_u),
            nivel_u = %s
        WHERE pknu = %s;
    """
    datos = (xnombre, xemail, xclave, xfoto, xnivel, xpknu)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecuta
        conexion.commit()  # Confirma

        # PASO 4 ---> Recuperar los resultados
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultados
        xfilas = 0

    # print("Total de Filas afectadas -----------> " + str(xfilas))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultados
    return xfilas   

#eliminar usuario por pk
def set_eliminar_usuario(xpknu):
    # PASO 1 ---> Establecer la conexión con la BD
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL (eliminación lógica)
    sql = "UPDATE tmusuarios SET fkcods = 0 WHERE pknu = %s;"
    datos = (xpknu,)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecuta
        conexion.commit()  # Confirma

        # PASO 4 ---> Recuperar los resultados
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultados
        xfilas = 0

    # print("Total de Filas afectadas -----------> " + str(xfilas))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultados
    return xfilas

def get_foto_usuario(xpknu):
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    sql = """
        SELECT foto_u
        FROM tmusuarios
        WHERE pknu = %s;
    """

    try:
        cursor.execute(sql, (xpknu,))
        xresultado = cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar la foto: {e}")
        xresultado = None

    cursor.close()
    conexion.close()

    return xresultado