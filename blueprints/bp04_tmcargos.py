# Programa: bp04_tmcargos.py
# Objetivo: Controlar las operaciones con la TMCARGOS
# Autor: Sergio Capacho / Domingo 25/Oct/2026 11:00 Pm

# 1.- IMPORTAR LAS LIBRERIAS DE TRABAJO
from flask import Blueprint, render_template, redirect, request, Flask
from flask import session

# ........................................................

# 2.- IMPORTAR LOS MODELOS
# 2.1.- Para las operaciones con la TMCARGOS
from modelos.modelo04_tmcargos import get_all_vtmcargos  # Traer todos los registros
from modelos.modelo04_tmcargos import add_tmcargo  # Agregar un registro
from modelos.modelo04_tmcargos import get_cargo_by_pkcodcar  # Buscar el cargo
from modelos.modelo04_tmcargos import set_modificar_tmcargo  # Modifica los datos
from modelos.modelo04_tmcargos import set_delete_tmcargo  # Eliminación lógica

# 2.2.- Para las operaciones con la TMSTATUS
from modelos.modelo03_tmstatus import get_all_status  # Traer la TMStatus

# ........................................................


# 3.- CREAR EL OBJETO TMCARGOS
obj_tmcargos = Blueprint("tmcargos", __name__)
# ........................................................
# ................................................................................


# 4.- REGISTRAR LAS RUTAS DEL OBJETO TMCARGOS
# 4.1.- RUTA ---> /tmcargos/menu_crud
@obj_tmcargos.route("/menu_crud")
def menu_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        return render_template("m04_tmcargos/tmcargos01_base.html")
    else:
        return redirect("/login/entrar")


# 4.2.- RUTA ---> /tmcargos/reporte_crud
@obj_tmcargos.route("/reporte_crud")
def reporte_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmen = " "
        xdatos = get_all_vtmcargos()
        return render_template(
            "m04_tmcargos/tmcargos02_reporte.html", ydatos=xdatos, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


# 4.3.- RUTA ---> /tmcargos/agregar_crud
@obj_tmcargos.route("/agregar_crud")
def agregar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmen = " "
        return render_template("m04_tmcargos/tmcargos03_agregar.html", ymensaje=xmen)
    else:
        return redirect("/login/entrar")


@obj_tmcargos.route("/agregar_crud", methods=["GET", "POST"])
def agregar02_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        if request.method == "POST":
            xdcargo = request.form["txt_descripcion"].upper()
            xsueldo = request.form["txt_sueldo"]
            xresultado = add_tmcargo(xdcargo, xsueldo)
            xmen = " "
            if xresultado == 1:
                xmen = "¡¡¡ El " + xdcargo + " fue Registrado con Éxito !!!"
            else:
                xmen = "¡¡¡ Error al insertar el " + xdcargo + ", este ya existe !!!"

            xdatos = get_all_vtmcargos()
            return render_template(
                "m04_tmcargos/tmcargos02_reporte.html",
                ydatos=xdatos,
                ymensaje=xmen,
            )
    else:
        return redirect("/login/entrar")


# 4.4.- RUTA ---> /tmcargos/consultar_crud
@obj_tmcargos.route("/consultar_crud")
def consultar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xcargo = None
        xmen = " "
        return render_template(
            "m04_tmcargos/tmcargos04_cm.html", ycargo=xcargo, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


@obj_tmcargos.route("/consultar_crud", methods=["GET", "POST"])
def consultar02_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        if request.method == "POST":
            xcodcar = request.form["txt_codcar"]
            # print("Código del Cargo - Controlador TMCargos ---> " + str(xcodcar))
            xcargo = get_cargo_by_pkcodcar(xcodcar)
            xtmstatus = get_all_status()
            xmen = " "
            if xcargo:
                xmen = "!!! El Código " + str(xcodcar) + " Existe ¡¡¡"
            else:
                xmen = "!!! El Código " + str(xcodcar) + " No Existe ¡¡¡"

            return render_template(
                "m04_tmcargos/tmcargos04_cm.html",
                ycargo=xcargo,
                ytmstatus=xtmstatus,
                ymensaje=xmen,
            )
    else:
        return redirect("/login/entrar")


# 4.5.- RUTA ---> /tmcargos/modificar_crud
@obj_tmcargos.route("/modificar_crud")
def modificar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xcargo = None
        xmen = " "
        return render_template(
            "m04_tmcargos/tmcargos01_base.html", ycargo=xcargo, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


@obj_tmcargos.route("/modificar_crud", methods=["GET", "POST"])
def modificar02_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xmensaje = " "
        if request.method == "POST":
            xcodcar = request.form["txt_codcar"]
            xdcargo = request.form["txt_descripcion"].upper()
            xsueldo = request.form["txt_sueldo"]
            xfkcods = request.form["txt_fkcods"]

            # Enviando datos al modelo para la modificación
            xresultado = set_modificar_tmcargo(xcodcar, xdcargo, xsueldo, xfkcods)

            if xresultado == 1:
                xmen = "¡¡¡ El " + xdcargo + " fue Modificado con Éxito !!!"
            else:
                xmen = "¡¡¡ Error al modificar el " + xdcargo + " !!!"

            xdatos = get_all_vtmcargos()
            return render_template(
                "m04_tmcargos/tmcargos02_reporte.html",
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
@obj_tmcargos.route("/eliminar_crud")
def eliminar01_crud():
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        xcargo = None
        xmen = " "
        return render_template(
            "m04_tmcargos/tmcargos01_base.html", ycargo=xcargo, ymensaje=xmen
        )
    else:
        return redirect("/login/entrar")


@obj_tmcargos.route("/eliminar_crud/<int:xcodcar>")
def eliminar02_crud(xcodcar=None):
    if session["xlogin"] == True and session["xnivel"] in (1, 4):
        set_delete_tmcargo(xcodcar)
        return redirect("/tmcargos/reporte_crud")
    else:
        return redirect("/login/entrar")


# ........................................................
# ................................................................................
