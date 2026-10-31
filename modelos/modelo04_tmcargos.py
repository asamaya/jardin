# Programa: modelo04_tmcargos.py
# Objetivo: Manejar las funciones para las operaciones con la TMCARGOS
# Autor: Sergio Capacho / Domingo 25/Oct/2026 - 11:00 Pm

# 1.- IMPORTAR DE LIBRERIAS
# 1.1.- La librería para gestionar la conexión
from psycopg import connect

# 1.2.- La cadena de conexión con la BD
from modelos.modelo00_bd import cadenaConexion

# ....................................................................................................................................


# 3.- OPERACIONES SQL PARA LA TMCARGOS
# ........................................................................................
# ..................................................................................................................................
# 3.1.- Obtener todos los registros de la Vista TMCargos
def get_all_vtmcargos():
    # PASO 1 ---> Establecer la conexión con la BD
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = " select * from vtmcargos order by pkcodcar::BIGINT;"

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(
            sql,
        )  # Ejecuta
        conexion.commit()  # Confirma

        # PASO 4 ---> Recuperar los resultados
        xresultados = cursor.fetchall()  # fetchone() Un / fetchall() Varios
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultados
        xresultados = 0
        xfilas = 0

    # print("Total de Filas afectadas -----------> " + str(xfilas))
    # print("Datos recuperados de la TMCargos ---> " + str(xresultados))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultados
    return xresultados


# 3.2.- Agregar un cargo Nuevo a la TMCargos
def add_tmcargo(xdcargo, xsueldo):
    # PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = "INSERT INTO tmcargos(dcargo, sueldo, fkcods) VALUES (%s, %s, %s);"
    datos = (xdcargo, xsueldo, 1)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecutar
        conexion.commit()  # Confirmar

        # PASO #4 ---> Recuperar los resultados
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultados
        xfilas = 0

    # print("Total de Filas Afectadas ---->" + str(xfilas))

    # PASO 5 ---> Cerrar la conexión
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultado
    return xfilas


# 3.3.- Buscar (Obtener) los datos del cargo usando el código del cargo
def get_cargo_by_pkcodcar(xcodcar):
    # print("Código del Cargo a buscar en TMCargos ---> " + str(xcodcar))
    # PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = "SELECT * FROM tmcargos WHERE pkcodcar = %s "
    datos = (xcodcar,)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecutar
        conexion.commit()  # Confirmar

        # PASO 4 ---> Recuperar resultados
        xresultados = cursor.fetchone()  # fetchone() Uno / #fetchall() Varios
        xfilas = cursor.rowcount  # ---> Total de filas afectadas
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar resultados
        xresultados = 0
        xfilas = 0

    # print("Total de Filas afectadas -----------> " + str(xfilas))
    # print("Datos recuperados de la TMCargos ---> " + str(xresultados))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar el resultado
    return xresultados


# 3.4.- Modificar (Fijar) los datos del cargo
def set_modificar_tmcargo(xcodcar, xdcargo, xsueldo, xfkcods):
    # PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Constuir la consulta SQL
    sql = "UPDATE tmcargos SET dcargo = %s, sueldo = %s, fkcods = %s WHERE pkcodcar = %s ;"
    datos = (xdcargo, xsueldo, xfkcods, xcodcar)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecutar
        conexion.commit()  # Confirmar

        # PASO #4 ---> Recuperar Resultados
        xfilas = cursor.rowcount  # ---> Total de filas afectadas en la operación
    except Exception as e:
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar resultado
        xfilas = 0

    # print("Total de Filas Afectadas --->" + str(xfilas))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar resultado
    return xfilas


# 3.5.- Eliminar (Fijar) lógicamente un cargo
def set_delete_tmcargo(xcodcar):
    # PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    # PASO 2 ---> Construir la consulta SQL
    sql = "UPDATE tmcargos SET fkcods = %s WHERE pkcodcar = %s ;"
    datos = ("0", xcodcar)

    try:
        # PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  # Ejecutar
        conexion.commit()  # Confirmar

        # PASO #4 ---> Recuperar los resultados
        xfilas = cursor.rowcount  # ---> te dice cuántas filas fueron afectadas
    except Exception as e:
        conexion.rollback()  # Si falla, deshace el cambio
        print(f"Este fue el Error: {e}")
        # PASO 4 ---> Recuperar los resultado
        xfilas = 0

    # print("Filas Afectadas---->" + str(xfilas))

    # PASO 5 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 6 ---> Retornar los resultado
    return xfilas


# ........................................................
# ................................................................................
