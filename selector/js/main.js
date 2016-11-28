$(document).ready(main);
URL_BASE="http://localhost:8000/gestionbd"
URL_LISTA_CICLOS    = URL_BASE + "/get_json_ciclos"
URL_LISTA_MODULOS   =URL_BASE + "/get_json_modulos/"
URL_LISTA_RAS       = URL_BASE + "/get_json_ras/"   
OPCION_VACIA        =   -1



function cargar_datos_ras(){
    html=""
    for (pos in datos_ras){
        modelo=datos_ras[pos]
        clave=modelo.pk
        if ( typeof modelo.fields.letra=== "undefined" ){
            prefijo=modelo.fields.numero
        } else {
            prefijo=modelo.fields.letra
        }
        nombre=prefijo+ ") " + modelo.fields.texto
        html+="<option value='"+clave+"'>" + nombre + "</option>"
    }
    $("#ras").html(html)
}
function modulo_cambiado(){
    id_modulo=$("#modulo").val()
    if (id_modulo == OPCION_VACIA ) return 
    alert(id_modulo)
    var jqXHR=$.getScript(URL_LISTA_RAS+id_modulo, cargar_datos_ras)
}
function cargar_datos_modulos(){
    html="<option value='" + OPCION_VACIA + "'>Elija un módulo</option>"
    for (pos in datos_modulos){
        modelo=datos_modulos[pos]
        clave=modelo.pk
        nombre=modelo.fields.nombre
        html+="<option value='"+clave+"'>" + nombre + "</option>"
    }
    $("#modulo").html(html)
}
function ciclo_cambiado(){
    codigo_ciclo=$("#ciclo").val()
    if (codigo_ciclo==OPCION_VACIA){
        return 
    }
    var jqXHR=$.getScript(URL_LISTA_MODULOS+codigo_ciclo, cargar_datos_modulos)
}

function marcar_ras(){
    $("#ras>option").attr("selected", "selected")
}

function desmarcar_ras(){
    $("#ras>option").removeAttr("selected")
}
function instalar_controladores_eventos(){
    $("#ciclo").change(ciclo_cambiado);
    $("#modulo").change(modulo_cambiado);
    $("#marcar_todos_ras").click(marcar_ras)
    $("#desmarcar_todos_ras").click(desmarcar_ras)
}

function cargar_datos_iniciales(){
    html="<option value='"+OPCION_VACIA+"'>Elija un ciclo</option>"
    for (pos in datos_ciclos){
        modelo=datos_ciclos[pos]
        clave=modelo.pk
        nombre=modelo.fields.nombre
        html+="<option value='"+clave+"'>" + nombre + "</option>"
    }
    $("#ciclo").html(html)
}

//Poner aquí el codigo de inicio del programa JS
function main(){
    
    var jqXHR=$.getScript(URL_LISTA_CICLOS, cargar_datos_iniciales)
    instalar_controladores_eventos()
}