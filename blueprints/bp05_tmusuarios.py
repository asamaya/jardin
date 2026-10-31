# Programa: bp04_tmcargos.py
# Objetivo: Controlar las operaciones con la TMCARGOS
# Autor: Sergio Capacho / Domingo 25/Oct/2026 11:00 Pm

from pathlib import Path

# 1.- IMPORTAR LAS LIBRERIAS DE TRABAJO
from flask import Blueprint, render_template, redirect, request
from flask import session, send_from_directory
from werkzeug.utils import secure_filename



RUTA_FOTOS = Path(__file__).resolve().parent.parent / "static" / "img" / "fotos"


def guardar_foto(archivo):
    if archivo is None or not archivo.filename:
        return None

    nombre_foto = secure_filename(archivo.filename)
    if not nombre_foto:
        return None

    RUTA_FOTOS.mkdir(parents=True, exist_ok=True)
    archivo.save(RUTA_FOTOS / nombre_foto)
    return nombre_foto

# ........................................................

# 2.- IMPORTAR LOS MODELOS
# 2.1.- Para las operaciones con la TMCARGOS
from modelos.modelo05_tmusuarios import get_all_tmusuarios  # Traer todos los registros
from modelos.modelo05_tmusuarios import get_all_tmniveles  # Traer los niveles
from modelos.modelo05_tmusuarios import add_tmusuario  # Agregar un registro
from modelos.modelo05_tmusuarios import get_usuario_by_nombre  # Buscar el cargo
from modelos.modelo05_tmusuarios import set_modificar_usuario  # Modifica los datos
from modelos.modelo05_tmusuarios import set_eliminar_usuario  # Eliminación lógica
from modelos.modelo05_tmusuarios import get_foto_usuario  # Obtener la foto


# ........................................................


# 3.- CREAR EL OBJETO TMCARGOS
obj_tmusuarios = Blueprint("tmusuarios", __name__)
# ........................................................
# ................................................................................


# 4.- REGISTRAR LAS RUTAS DEL OBJETO TMUSUARIOS
# 4.1.- RUTA ---> /tmusuarios/menu_crud
@obj_tmusuarios.route("/menu_crud")
def menu_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        return render_template("m05_tmusuarios/tmusuarios01_base.html")
    else:
        return redirect("/login/entrar")


@obj_tmusuarios.route("/mostrar_foto/<int:xpknu>")
def mostrar_foto(xpknu):
    xfoto = get_foto_usuario(xpknu)
    if xfoto and xfoto[0] and (RUTA_FOTOS / xfoto[0]).is_file():
        return send_from_directory(RUTA_FOTOS, xfoto[0])
    return send_from_directory(RUTA_FOTOS, "foto_perfil.png")


# 4.2.- RUTA ---> /tmusuarios/reporte_crud
@obj_tmusuarios.route("/reporte_crud")
def reporte_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmen = " "
        xdatos = get_all_tmusuarios()
        return render_template(
            "m05_tmusuarios/tmusuarios02_reporte.html", ydatos=xdatos, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


# 4.3.- RUTA ---> /tmusuarios/agregar_crud
@obj_tmusuarios.route("/agregar_crud")
def agregar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmen = " "
        xniveles = get_all_tmniveles()
        return render_template(
            "m05_tmusuarios/tmusuarios03_agregar.html",
            ymensaje=xmen,
            yniveles=xniveles,
        )
    else:
        return redirect("/login/entrar")


@obj_tmusuarios.route("/agregar_crud", methods=["GET", "POST"])
def agregar02_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        if request.method == "POST":
            xnombre = request.form["txt_nombre_usuario"].strip().upper()
            xemail = request.form["txt_correo"].strip().upper()
            xclave = request.form["txt_clave"]
            xfoto = guardar_foto(request.files.get("txt_foto"))
            xnivel = request.form["txt_nivel"]
            xresultado = add_tmusuario(xnombre, xemail, xclave, xfoto, xnivel)
            xmen = " "
            if xresultado == 1:
                xmen = "¡¡¡ El " + xnombre + " fue Registrado con Éxito !!!"
            else:
                xmen = "¡¡¡ Error al insertar el " + xnombre + ", este ya existe !!!"

            xdatos = get_all_tmusuarios()
            return render_template(
                "m05_tmusuarios/tmusuarios02_reporte.html",
                ydatos=xdatos,
                ymensaje=xmen,
            )
    else:
        return redirect("/login/entrar")

# 4.4.- RUTA ---> /tmusuarios/consultar_crud
@obj_tmusuarios.route("/consultar_crud")
def consultar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmen = " "
        return render_template(
            "m05_tmusuarios/tmusuarios04_cm.html", yusuario=None, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


@obj_tmusuarios.route("/consultar_crud", methods=["GET", "POST"])
def consultar02_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        if request.method == "POST":
            xnombre = request.form["txt_nombre_usuario"].strip().upper()
            xusuario = get_usuario_by_nombre(xnombre)
            xmen = " "
            if xusuario:
                xmen = "!!! El Usuario " + str(xnombre) + " Existe ¡¡¡"
            else:
                xmen = "!!! El Usuario " + str(xnombre) + " No Existe ¡¡¡"

            return render_template(
                "m05_tmusuarios/tmusuarios04_cm.html",
                yusuario=xusuario,
                ymensaje=xmen,
            )
    else:
        return redirect("/login/entrar")

# 4.5.- RUTA ---> /tmusuarios/modificar_crud
@obj_tmusuarios.route("/modificar_crud")
def modificar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmen = " "
        return render_template(
            "m05_tmusuarios/tmusuarios04_cm.html", yusuario=None, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


@obj_tmusuarios.route("/modificar_crud", methods=["GET", "POST"])
def modificar02_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmensaje = " "
        if request.method == "POST":
            xpknu = request.form["txt_codusu"]
            xnombre = request.form["txt_nombre_usuario"].strip().upper()
            xemail = request.form["txt_correo"].strip().upper()
            xclave = request.form.get("txt_clave", "")
            xfoto = guardar_foto(request.files.get("txt_foto"))
            xnivel = request.form["txt_nivel"]

            # Enviando datos al modelo para la modificación
            xresultado = set_modificar_usuario(
                xpknu, xnombre, xemail, xclave, xfoto, xnivel
            )

            if xresultado == 1:
                xmen = "¡¡¡ El " + xnombre + " fue Modificado con Éxito !!!"
            else:
                xmen = "¡¡¡ Error al modificar el " + xnombre + " !!!"

            xdatos = get_all_tmusuarios()
            return render_template(
                "m05_tmusuarios/tmusuarios02_reporte.html",
                ydatos=xdatos,
                ymensaje=xmen,
            )
    else:
        return redirect("/login/entrar")


# 4.6.- RUTA ---> /tmcargos/eliminar
# Nota: los datos se reciben de dos formas:
# Opcion 1: xcodcar = request.form['txt_codcar']
# Opción 2: Mencionar directamente la función
# <a href="url_for('tmcargos.eliminar02', xcodcar = cargo[0])">...</a>
# donde el tipo pude: int(Entero) / string (String) / float (real) / path (Ruta)
@obj_tmusuarios.route("/eliminar_crud")
def eliminar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xnombre = None
        xmen = " "
        return render_template(
            "m05_tmusuarios/tmusuarios01_base.html", yusuario=xnombre, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")

    
@obj_tmusuarios.route("/eliminar_crud/<int:xpknu>")
def eliminar02_crud(xpknu=None):
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        set_eliminar_usuario(xpknu)
        return redirect("/tmusuarios/reporte_crud")
    else:
        return redirect("/login/entrar")


# ........................................................
# ................................................................................