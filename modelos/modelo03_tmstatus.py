#Programa: modelo03_tmstatus.py
#Objetivo: Manejar las funciones para las operaciones con la TMSTATUS
#Autor: Sergio Capacho / Sábado 24/Oct/2026  -  11:00 Pm


#1.- IMPORTAR DE LIBRERIAS
from psycopg import connect
#........................................................
#................................................................................


#2.- IMPORTAR EL MODELO DE LA BD CON SU LA CONEXIÓN
from modelos.modelo00_bd import cadenaConexion
#........................................................
#................................................................................



#3.- OPERACIONES SQL DE LA TMSTATUS
#........................................................
#................................................................................

#3.1.- Obtener todos los registros de la TMSTATUS
def get_all_status():
    #PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    #PASO 2 ---> Construir la consulta SQL
    sql = "SELECT * FROM  tmstatus ORDER BY pkcods::BIGINT;"
    
    try:
        #PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql,  )  #Ejecute
        conexion.commit()       #Confirma

        #PASO 4 ---> Recuperar resultados
        xresultados = cursor.fetchall()     #fetchone() ---> Un solo registro
                                            #fetchall() ---> Varios registros
        #print("Datos recuperados de la TMStatus ---> " + str(xresultado))
        xfilas = cursor.rowcount            #cursor.rowcount ---> Total de filas afectadas en la operación
    except Exception as e:
        print( f"Este fue el Error: {e}")
        #PASO 4 ---> Recuperar resultados
        xresultados = 0
        xfilas = 0

    print("Filas afectadas ---->" + str(xfilas))

    #PASO 5 ---> Cerrar la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 6 ---> Retornar resultados
    return xresultados


#3.2.- Agregar un Nuevo Status a la TMSTATUS
def add_status(xdstatus):
    #PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    #PASO 2 ---> Construir la consulta SQL
    sql = "insert into tmstatus(dstatus) values (%s);"
    datos = (xdstatus, )

    try:
        #PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  #Ejecutar
        conexion.commit()           #Confirmar

        #PASO #4 ---> Recuperar Resultados
        xfilas = cursor.rowcount    #cursor.rowcount ---> Total de filas afectadas en la operación 
    except Exception as e:
        print( f"Este fue el Error: {e}")
        #(PASO #4 ---> Recuperar resultados
        xfilas = 0                

    print("Filas afectadas ---->" + str(xfilas))

    #PASO 5 ---> Cerrar la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 6 ---> Retornar resultados
    return xfilas


#3.3.- Consultar (Obtener) los datos del Status por medio del código del Status
def get_status_by_pkcods(xpkcods):
    #print("Código del Status a buscar ---> " + str(xpkcods))
    #PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    #PASO 2 ---> Construir la consulta SQL
    sql = "SELECT * FROM tmstatus  WHERE pkcods = %s "
    datos = (xpkcods, )

    try:
        #PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  #Ejecurar
        conexion.commit()           #Confirmar

        #PASO 4 ---> Recuperar resultados
        xresultados = cursor.fetchone() #fetchone() ---> Un solo registro
                                        #fetchall() ---> Varios registro
        #print("Datos recuperados de la TMStatus ---> " + str(xresultado))
        xfilas = cursor.rowcount  #cursor.rowcount ---> Total de filas afectadas en la operación
    except Exception as e:
        print( f"Este fue el Error: {e}")
        #(PASO #4 ---> Recuperar resultados
        xresuktados = 0 
        xfilas = 0                 
   
    print("Filas afectadas ---->" + str(xfilas))     

    #PASO 5 ---> Cerrar la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 6 ---> Retornar resultado
    return xresultados


#3.4.- Modificar (Fijar/Asignar) los datos en la TMStatus
def set_modificar_status(xpkcods, xdstatus):
    #PASO 1 ---> Establecer la conexión con la base de datos
    conexion = cadenaConexion()
    cursor = conexion.cursor()

    #PASO 2 ---> Constuir la consulta SQL
    sql = "UPDATE tmstatus SET  dstatus = %s  WHERE pkcods = %s ;"
    datos = (xdstatus, xpkcods )

    try:
        #PASO 3 ---> Ejecutar la consulta SQL
        cursor.execute(sql, datos)  #Ejecutar
        conexion.commit()           #Confirmar

        #PASO 4 ---> Recuperar Resultados
        xfilas = cursor.rowcount    #cursor.rowcount ---> te dice cuántas filas fueron afectadas
    except Exception as e:   
        print( f"Este fue el Error: {e}")
        #(PASO #4 ---> Recuperar resultados
        xfilas = 0                    

    print(f"Filas afectadas: {cursor.rowcount}")

    #PASO 5 ---> Cerrar la conexión con la base de datos 
    cursor.close()
    conexion.close()

    #PASO 6 ---> Retornar resultado
    return xfilas

#........................................................
#................................................................................

