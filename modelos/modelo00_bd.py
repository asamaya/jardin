#Programa: modelo00_DB.py
#Objetivo: 
#   A.- Declarar la base de datos a usar, en este caso: BDRetardados
#   B.- Construir la cadena de conexión para la BD
#Autor: Sergio Capacho / Sábado 24/Oct/2026 11:00 Pm


#1.- IMPORTAR  LIBRERIAS
#En este caso se importa desde la librería psycopg del paquete connect
#el cual permite establecer la conección con la Base de Datos PostGreSQL
from psycopg import connect



#2.- CREAR LA CADENA DE CONEXIÓN
def cadenaConexion():
    conexion = connect(host = "localhost",    # localhost o http://127.0.0.1
                port = 5432, 
                dbname = "bdretardados",             
                user = "postgres",
                password = "Lizzicat09.") 
    return conexion

