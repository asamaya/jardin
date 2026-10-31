# app.py ---> Archivo para iniciar la aplicación
# Autor: Sergio Capacho

# 01.- IMPORTACIÓN DE LIBRERÍAS

# Importación de la librería OS
import os

# Importación de Flask
from flask import Flask

# Se usa para trabajar rutas y archivos estáticos
from flask import url_for

# Permite renderizar las páginas HTML
from flask import render_template

# Permite establecer la conexión con PostgreSQL
from psycopg import connect

# Permite trabajar con variables de sesión
from flask import session

# Permite redireccionar entre vistas
from flask import redirect

# Permite recibir datos enviados desde formularios
from flask import request

from blueprints.bp03_tmstatus import obj_tmstatus

from blueprints.bp04_tmcargos import obj_tmcargos

from blueprints.bp05_tmusuarios import obj_tmusuarios

# 03.- CREACIÓN DE LA APLICACIÓN
mi_app = Flask(__name__)


# 04.- CREACIÓN DE LA LLAVE SECRETA
mi_app.secret_key = "practica"


# 05.- CREACIÓN DE LAS RUTAS

# Ruta: /hola
@mi_app.route('/hola')
def hola():
    return render_template('m01_sitio/p00_hola.html')


# Ruta: /xinicio
@mi_app.route('/xinicio')
def xinicio():
    return render_template('m01_sitio/p00_xinicio.html')


# 05.01.- RUTA RAIZ ----> /
@mi_app.route('/')
@mi_app.route('/inicio')
@mi_app.route('/index')
def inicio():
    session["xlogin"] = False
    return render_template('m01_sitio/p01_inicio.html')


# 05.02.- RUTA PRODUCTOS ----> /productos
@mi_app.route('/productos')
def productos():
    session["xlogin"] = False
    return render_template('m01_sitio/p02_productos.html')


# 05.03.- RUTA CURSOS ----> /cursos
@mi_app.route('/cursos')
def cursos():
    session["xlogin"] = False
    return render_template('m01_sitio/p03_cursos.html')


# 05.04.- RUTA GALERIA ----> /galeria
@mi_app.route('/galeria')
def galeria():
    session["xlogin"] = False
    return render_template('m01_sitio/p04_galeria.html')


# 05.05.- RUTA FORMULARIO ----> /formulario
@mi_app.route('/formulario')
def formulario():
    session["xlogin"] = False
    return render_template('m01_sitio/p05_formulario.html')

# INICIO DE LA DECLARACIÓN DE LAS RUTAS ASOCIADAS AL LOGIN (BACKEND)
# -----------------------------------------
# ------------------------------------------------------

# 05.05.A.- RUTA LOGIN
@mi_app.route('/login/entrar')
def login_formulario():
    session["xlogin"] = False
    xmensaje = " "
    return render_template(
        'm02_login/paso01_login.html',
        ymensaje=xmensaje
    )


# 05.05.B.- RUTA LOGIN
@mi_app.route('/login/entrar', methods=['POST', 'GET'])
def login_validar():
    session["xlogin"] = False

    # INICIO DE PASOS (MUY IMPORTANTE)
    # ***********************************************

    # PASO 1.- RECIBIR LOS DATOS DEL FORMULARIO
    xemail = request.form['txt_email'].strip().upper()
    # La clave NO se convierte a mayúsculas: debe compararse tal como se escribió
    xclave = request.form['txt_clave']

    # print("Datos llegados del formulario........................................")
    # print("Email ---> " + str(xemail))
    # print("Clave -----> " + str(xclave))

    # PASO 2 ---> Establecer la conexión con la base de datos localhost
    conexion = connect(
        host="127.0.0.1",
        port=5432,
        dbname="bdretardados",
        user="postgres",
        password="Lizzicat09."
    )
    cursor = conexion.cursor()

    # PASO 3 ---> Construir la consulta SQL usando el modelo00_bd (TMUsuarios)
    sql = """
        SELECT *
        FROM TMUSUARIOS
        WHERE (UPPER(email_u) = %s) AND (clave_u = %s);
    """
    datos = (xemail, xclave)

    # PASO 4 ---> Ejecutar la consulta SQL
    # Preparación para la acción (Insert, Update, Delete, Select...)
    cursor.execute(sql, datos)

    # Ejecuta la transacción; es decir, guarda cambios de forma permanente
    conexion.commit()

    # PASO 5 ---> Recuperar los datos
    # fetchone() ---> Retorna un solo registro / fetchall() ---> Varios
    resultado = cursor.fetchone()

    # PASO 6 ---> Cerrar la conexión con la base de datos
    cursor.close()
    conexion.close()

    # PASO 7 ---> Retornar resultados
    # FIN DE PASOS (MUY IMPORTANTES)
    # ***********************************************
    # ************************************************************

    # VALIDACIÓN SI LLEGARON DATOS
    if bool(resultado):
        # ASIGNACIÓN DE VALORES A VARIABLES DE SESIÓN
        session["xlogin"] = True
        session["xnombre_usuario"] = resultado[3]
        session["xemail"] = resultado[1]
        session["xnivel"] = resultado[5]
        session["xstatus"] = resultado[6]
        xmensaje = " "

        return render_template('m02_login/paso02_login.html')
    else:
        xmensaje = "¡¡¡ Acceso Denegado !!!"
        return render_template(
            'm02_login/paso01_login.html',
            ymensaje=xmensaje
        )


# 05.05.C.- RUTA LOGIN ---> /login/admin
@mi_app.route('/login/admin')
def admin():
    if session['xlogin'] and not (session['xnivel'] == 0):
        return render_template('m02_login/paso03_admin.html')
    else:
        return redirect('/inicio')


# 05.05.D.- RUTA LOGIN ---> /login/salir
@mi_app.route('/login/salir')
def login_salir():
    # Cerrando y limpiar las variables de session
    session.clear()
    return redirect('/')


# FIN RUTA LOGIN PARA TRABAJAR CON EL BACKEND
# -----------------------------------------
# ------------------------------------------------------

mi_app.register_blueprint(obj_tmstatus, url_prefix='/tmstatus')
mi_app.register_blueprint(obj_tmcargos, url_prefix='/tmcargos')
mi_app.register_blueprint(obj_tmusuarios, url_prefix='/tmusuarios')

# 06.- EJECUCIÓN DEL APLICATIVO
if __name__ == '__main__':
    mi_app.run(host="127.0.0.1", port=5000, debug=True)