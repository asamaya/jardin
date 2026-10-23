/* Función JavaScript para generar la fecha y hora */

//UN LISTENER (ESCUCHADOR - DISPARADOR)
//DEFINICIÓN: En JavaScript es una función que espera pacientemente 
//a que ocurra un evento específico en un elemento del documento web 
//(como un botón, una imagen, o la ventana del navegador). 
//Cuando ese evento sucede, el listener ejecuta el código que tiene asociado.
//OJO OJO: No esperar a que se carguen completamente recursos externos como imágenes 
// (<img>), hojas de estilo o sub-marcos.


//CREAR UN LISTENER: El cual tiene como función esperar que el DOM
//    se carge completo en la memoría, para luego cargar la función
//    que va ha ejecutar el reloj en la pagina web.
//    Es decir, el listener (ESCUCHADOR - DISPARADOR) que espera a que el DOM 
//    esté completamente cargado y luego carga la función startTime(); 


//    document.addEventListener(): 
//    Es el método que se usa para registrar la función y el evento  
//    ha escuchar en el DOM.

//    'DOMContentLoaded': Es el evento que se está escuchando todo el DOM. 
//     El evento DOMContentLoaded verifica (escucha) si documento HTML ha sido completamente cargado 
//     y está listo para ser manipulado por JavaScript.

//En resumen, actúa como un "semáforo" que da luz verde 
//a la ejecución del código de manipulación del DOM

/*document.addEventListener('DOMContentLoaded', function() {
    startTime(); 
});*/



function startTime() {
    // AQUI revisa que el ID que buscas sea correcto y exista en tu HTML
    //document.getElementById("clockdate").innerHTML = "Funciona!";

    var today = new Date();
    var hr = today.getHours();
    var min = today.getMinutes();
    var sec = today.getSeconds();
    ap = (hr < 12) ? "<span>AM</span>" : "<span>PM</span>";
    hr = (hr == 0) ? 12 : hr;
    hr = (hr > 12) ? hr - 12 : hr;
    //Add a zero in front of numbers<10
    hr = checkTime(hr);
    min = checkTime(min);
    sec = checkTime(sec);
    document.getElementById("clock").innerHTML = hr + ":" + min + ":" + sec + " " + ap;
    
    var months = ['Ene', 'Feb', 'Mar', 'Abril', 'May', 'Jun', 'Jul', 'Agost', 'Sept', 'Oct', 'Nov', 'Dic'];
    var days = ['Dom', 'Lun', 'Mar', 'Miér', 'Jue', 'Vie', 'Sáb'];
    var curWeekDay = days[today.getDay()];
    var curDay = today.getDate();
    var curMonth = months[today.getMonth()];
    var curYear = today.getFullYear();
    var date = curWeekDay+", " + curMonth + " " + curDay + "<br/><br/>" +curYear;
    document.getElementById("date").innerHTML = date;
    
    var time = setTimeout(function(){ startTime() }, 500);
}
function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}