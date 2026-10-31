#bp03_tmstatus.py
#Objetivo: Controlar las operaciones con la TMSTATUS
#Autor: Sergio Capacho / Sábdo 24/Oct/2026 11:00 Pm


#1.- IMPORTAR LAS LIBRERIAS DE TRABAJO
from flask import  Blueprint, session, render_template, redirect, request


#2.- IMPORTAR LOS MODELOS para las operaciones con la TMSTATUS - Funciones
from modelos.modelo03_tmstatus import get_all_status        #Traer todos los registros
from modelos.modelo03_tmstatus import add_status            #Agregar un registro
from modelos.modelo03_tmstatus import get_status_by_pkcods  #Buscar los datos de un Status X
from modelos.modelo03_tmstatus import set_modificar_status  #Modifica los datos del Status
#.............................................................
#................................................................................



#3.- CREAR EL OBJETO TMSTATUS 
obj_tmstatus = Blueprint('tmstatus', __name__)
#........................................................
#................................................................................


#4.- DEFINIR LAS RUTAS DEL OBJETO TMSTATUS
#4.1.- RUTA ---> /tmstatus/menu_crud
@obj_tmstatus.route('/menu_crud')
def menu_crud():
    if (session["xlogin"] == True and  session["xnivel"] in (1,4)  ):
        return render_template('m03_tmstatus/tmstatus01_base.html')
    else:
        return redirect('/login/entrar')




#4.2.- RUTA ---> /tmstatus/reporte_crud
@obj_tmstatus.route('/reporte_crud')
def reporte_crud():
    if (session["xlogin"] == True and ( session["xnivel"] in (1, 4) ) ):
        xmen = " "
        xdatos = get_all_status()
        return render_template('m03_tmstatus/tmstatus02_reporte.html', ydatos = xdatos, ymensaje = xmen)
    else:
        return redirect('/login/entrar')




#4.3.- RUTA ---> /tmstatus/agregar_crud
@obj_tmstatus.route('/agregar_crud')
def agregar01_crud():
    if (session["xlogin"] == True and ( session["xnivel"] in (1, 4) )):
        xmen = " "
        return render_template('m03_tmstatus/tmstatus03_agregar.html', ymensaje = xmen)
    else:
        return redirect('/login/entrar')


@obj_tmstatus.route('/agregar_crud', methods=['GET', 'POST'])
def agregar02_crud():
    if (session["xlogin"] == True  and   session["xnivel"] in (1, 4)  ):
        if request.method == 'POST':
            xdstatus = request.form['txt_descripcion'].upper()
            xresultado = add_status(xdstatus)
            xmen = " "
            if xresultado == 1 :
                xmen = "¡¡¡ El  " + xdstatus + " fue Registrado con Éxito !!!"
            else:
                xmen = "¡¡¡ Error al insertar el  " + xdstatus + ". Este dato ya existe  !!!"
        
        xdatos = get_all_status()
        return render_template('m03_tmstatus/tmstatus02_reporte.html', ydatos = xdatos, ymensaje = xmen)
    else:
        return redirect('/login/entrar')




#4.4.- RUTA ---> /tmstatus/consultar_crud
@obj_tmstatus.route('/consultar_crud')
def consultar01_crud():
    if (session["xlogin"] == True and   session["xnivel"] in (1, 4)  ):
        xdato = None
        xmen = " "
        return render_template('m03_tmstatus/tmstatus04_cm.html', ydato = xdato, ymensaje = xmen)
    else:
        return redirect('/login/entrar')


@obj_tmstatus.route('/consultar_crud', methods=['GET', 'POST'])
def consultar02_crud():
    if (session["xlogin"] == True and  session["xnivel"] in (1, 4) ):
        if request.method == 'POST':
            xmen = " "
            xpkcods = request.form['txt_pkcods'] 
            xresultados = get_status_by_pkcods(xpkcods) 

            if xresultados :
                xmen = "!!! El Código " + str(xpkcods) + " fue Encontrado ¡¡¡"
            else:
                xmen = "!!! El Código " + str(xpkcods) + " No Existe ¡¡¡"
                
        return render_template('m03_tmstatus/tmstatus04_cm.html', ydato = xresultados, ymensaje = xmen)
    else:
        return redirect('/login/entrar')




#4.5.- RUTA ---> /tmstatus/modificar_crud
@obj_tmstatus.route('/modificar_crud')
def modificar01_crud():
    if (session["xlogin"] == True and   session["xnivel"] in (1, 4)  ):
        xdato = None
        xmen = " "
        return render_template('m03_tmstatus/tmstatus04_cm.html', ydato = xdato, ymensaje = xmen)
    else:
        return redirect('/login/entrar')


@obj_tmstatus.route('/modificar_crud', methods=['GET', 'POST'])
def modificar02_crud():
    if (session["xlogin"] == True  and  session["xnivel"] in (1, 4) ):
        if request.method == 'POST':
            xmensaje = " "
            xpkcods  = request.form['txt_pkcods']
            xdstatus = request.form['txt_descripcion'].upper()

            #print("Código --->"  + xpkcods)
            #print("Status --->"  + xdstatus)

            xresultados = set_modificar_status(xpkcods, xdstatus)

            if xresultados == 1 :
                xmen = "¡¡¡ El  " + xdstatus + " fue Modificado con Éxito !!!"
            else:
                xmen = "¡¡¡ Error al modificar el " + xdstatus + "  !!!"

            xdatos = get_all_status()
            return render_template('m03_tmstatus/tmstatus02_reporte.html', ydatos = xdatos, ymensaje = xmen)

            #return redirect("/tmstatus/reporte")
    else:
        return redirect('/login/entrar')



#........................................................
#................................................................................