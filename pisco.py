#!/usr/bin/python3
# -*- coding: UTF-8

import os
import time
import requests
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict
from colorama import Fore, init
from urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
init()

#colores
verde = Fore.GREEN
lverde = Fore.LIGHTGREEN_EX
rojo = Fore.RED
lrojo = Fore.LIGHTRED_EX
amarillo = Fore.YELLOW
blanco = Fore.WHITE
cyan = Fore.CYAN
violeta = Fore.MAGENTA
azul = Fore.BLUE
lazul = Fore.LIGHTBLUE_EX

################### FUNCIONES DE LA HERRAMIENTA
# sistema de numeros de dni
def consulta_dni():
    dni = input("[+] Escribe el dni: ")
    def datos_del_doc():
        url = f"https://api.reniec.online/dni/{dni}"
        data1 = requests.get(url, verify=False)
        resp = data1.json()
        print(f"{azul}DNI : {blanco}"+resp['dni'])
        print(f"{azul}NOMBRES : {blanco}"+resp['nombres'])
        print(f"{azul}APELLIDO PATERNO : {blanco}"+resp['apellido_paterno'])
        print(f"{azul}APELLIDO MATERNO : {blanco}"+resp['apellido_materno'])
        #print(f"{azul}CODIGO VERIFICACIÓN : {blanco}"+resp['cui'])

    def verificar_documento():
        url2 = f"https://api.reniec.online/dni/{dni}"
        data2 = requests.get(url2, verify=False)
        respuesta = data2.json()
        # verificar la validez del documento introducido
        # en caso que exista los datos seran devueltos sean +18 o -18
        # si el dni no existe = [error:NO_DATA]
        try:
            respuesta['dni']
            datos_del_doc()
        except KeyError:
            print(f"{rojo}ERROR NO DATA")
    
    verificar_documento()
    
#sistema de verificacion de ruc
def consultaruc():
    token = '?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImdyYWR5Mzl1X24yOTFpQG5hZnhvLmNvbSJ9.cl5KQzsXaRuLuwEUWNJDLX_Zh2R_HkBsn9_YEP4keio'
    rucki = input("[+] RUC >> ")
    response = requests.get("https://dniruc.apisperu.com/api/v1/ruc/" +rucki +token)
    for key, value in response.json().items():
        print("[-] %s: %s" % (key, value))

# sistema de busqueda de direccion de casa
def direccion_casa():
    data_dni = input("[+] ESCRIBE EL DNI: ")
    url_base = f"https://sistemas.oefa.gob.pe/sirte-backend/comun/combo/SSOfindPersonaPorDni/{data_dni}"
    respuesta = requests.get(url_base)
    informacion_json = respuesta.json()
    # recopilacion de los datos
    # si es valido = esValido:true
    # si no es valido = esValido:false
    # si es de un menor = esValido:false
    validar_doc = informacion_json['esValido']
    if validar_doc == "false":
        print(f"{rojo}EL DOCUMENTO PARECE SER INCORRECTO O DE UN MENOR DE EDAD")
    elif validar_doc == "true":
        inf_casa = informacion_json['direccion']
        inf_ap_p = informacion_json['apellidoPaterno']
        inf_ap_m = informacion_json['apellidoMaterno']
        inf_fecha = informacion_json['fechaNacimiento']
        info_t_d = informacion_json['tipoDocumento']
        inf_names = informacion_json['nombres']
        inf_name_c = informacion_json['nombreCompleto']
        #### imprimir la información
        print(f"""
{verde}NOMBRES {cyan}: {blanco}{inf_names}
{verde}APELLIDO PATERNO {cyan}: {blanco}{inf_ap_p}
{verde}APELLIDO MATERNO {cyan}: {blanco}{inf_ap_m}
{verde}NOMBRES COMPLETOS {cyan}: {blanco}{inf_name_c}
{verde}DIRECCIÓN DE CASA {cyan}: {blanco}{inf_casa}
{verde}FECHA DE NACIMIENTO {cyan}: {blanco}{inf_fecha}         
        """)

# sistema de busqueda de números telefónicos
def consultaindividual():
    numerotelefonico = input("[+] ESCRIBE EL NÚMERO TELEFÓNICO: ")
    url1 = f"http://apilayer.net/api/validate?access_key=a34d97f03e51e991d6699b9de0b8694c&number={numerotelefonico}&country_code&format=1"
    url2 = f"https://phonevalidation.abstractapi.com/v1/?api_key=49f4fe982a1b4f5cacdde03608161cdd&phone={numerotelefonico}"

    data1 = requests.get(f"{url1}")
    data2 = requests.get(f"{url2}")

    dataJson1 = data1.json()
    dataJson2 = data2.json()

    existeono = dataJson1['local_format']

        # datos url numero 1
    validar = dataJson1['valid']
    prefijo = dataJson1['country_prefix']
    codigo = dataJson1['country_code']
    codigo_pais = dataJson1['country_name']
    localizacion = dataJson1['location']
        #datos url numero 2
    formato_local_pais = dataJson2['format']['local']
    carril = dataJson2['carrier']
    if existeono == '':
        print(f"{lrojo}NO EXISTE ")
    elif existeono is None:
        print(f"{lrojo}NO EXISTE ")
    else:
        print(f"{cyan}ES VALIDO ? :{blanco} {validar}\n{cyan}PREFIJO :{blanco} {prefijo}\n{cyan}FORMATO LOCAL :{blanco} {formato_local_pais}\n{cyan}CODIGO DEL PAIS :{blanco} {codigo}\n{cyan}PAIS :{blanco} {codigo_pais}\n{cyan}LOCALIZACIÓN :{blanco} {localizacion}\n{cyan}COMPAÑIA :{blanco} {carril}\n")

# consulta de nombres y apellidos por dni
def consulta_por_nombres():
    name = input("ESCRIBE EL NOMBRE: ")
    apellidop = input("ESCRIBE EL APELLIDO PATERNO: ")
    apellidom = input("ESCRIBE EL APELLIDO MATERNO: ")
    url = "https://buscardni.xyz/buscador/ejemplo_ajax_proceso.php"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = f"APE_PAT={apellidop}&APE_MAT={apellidom}&NOMBRES={name}"
    resp = requests.post(url, headers=headers, data=data)
    text = resp.text
    soup = BeautifulSoup(text, "lxml")
    text2 = soup.get_text()
    new_b = text2[131:]
    characters = "ver"
    string = ''.join( x for x in new_b if x not in characters)
    print(string)


def portada():
    print(f"""{violeta}       .       .        .    .       .     . 
 ██████╗ ██╗███████╗ ██████╗ ██████╗ .  .   .   .  .   . .   .
 ██╔══██╗██║██╔════╝██╔════╝██╔═████╗  ▄▀▀▀▀▀▄{violeta}.  .  .  
 ██████╔╝██║███████╗██║     ██║██╔██║ ▐░▄░░░▄░▌{violeta}.  .   . 
 ██╔═══╝ ██║╚════██║██║     ████╔╝██║ ▐░▀▀░▀▀░▌{violeta}  .   .   . 
 ██║     ██║███████║╚██████╗╚██████╔╝  ▀▄░═░▄▀{violeta} .   .     
 ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═════╝ . ▐░▀▄▀░▌ {violeta}    . .   
 {verde}PROGRAMADO POR D4VID.0                  {cyan}Versión 2.1 .   .
 {lverde}═══════════════════════════════════════════════════════
 {lrojo}INSTAGRAM: {blanco}d4vid.0day
 {blanco}GITHUB:{blanco} https://github.com/Monkey-hk4
 {azul}TELEGRAM:{blanco} mhk4_0
 {lazul}DONACIONES:{blanco} https://www.paypal.com/paypalme/davidhk4
 {lverde}═══════════════════════════════════════════════════════
    """)
    time.sleep(0.5)

def menu_ayuda():
    print(f"""
 {verde}MENÚ DE OPCIONES - PROYECTO PISC0
 {lverde}ÚLTIMA ACTUALIZACIÓN 05/12/2021 
 
  {blanco}COMANDO                  INFORMACIÓN {verde}
- [ dni ]          MOSTRAR NOMBRES Y APELLIDOS DE UNA PERSONA CON SU NÚMERO
                   DE DNI => ACTUALIZACIÓN PERMITE CONSULTAR PARA -18 & +18

- [ ruc ]          CONSULTA UNA RUC

- [ casa ]         CONSULTA LA DIRECCIÓN DE CASA DE UNA PERSONA CON SU NÚMERO
                   DE DNI => ACTUALIZACIÓN: Nombres,Apellidos,Fecha Nacimiento
                   y dirección de casa

- [ numero ]       Permite consultar datos basicos de un número telefónico
                   Ejemplo=> +51999888777

- [ buscar ]       Buscar a una persona con nombres y apellidos y obtener su 
                   Número de DNI => Solo personas mayores de edad.

 El script se va a actualizar todos los meses y se va a añadir más opciones.

 {azul}[clear] limpiar terminal - linux
 {azul}[cls] limpiar terminal windows
 {rojo}[exit] Salir de la herramienta.
    """)                                    

def eleccion():
    print(f"{verde}")
    opc = input(f"[pisco@root]>> ")
    if opc == "dni":
        consulta_dni()
        eleccion()
    elif opc == "help":
        menu_ayuda()
        eleccion()
    elif opc == "ayuda":
        menu_ayuda()
        eleccion()
    elif opc == "?":
        menu_ayuda()
        eleccion()
    elif opc == "casa":
        direccion_casa()
        eleccion()
    elif opc == "ruc":
        consultaruc()
        eleccion()
    elif opc == "numero":
        consultaindividual()
        eleccion()
    elif opc == "buscar":
        consulta_por_nombres()
        eleccion()
    elif opc == "clear":
        os.system("clear")
        portada()
        eleccion()
    elif opc == "cls":
        os.system("cls")
        portada()
        eleccion() 
    elif opc == "exit":
        exit()   
    else:
        print(f"""{rojo}
    ERROR 404 OPCIÓN INCORRECTA x_x 
        {verde}""")
        eleccion()
    
# inicio de tool
if __name__ == "__main__":
    portada()
    eleccion()