from flask import Flask, request
from xml.etree import ElementTree as ET
from Diccionario import Diccionario
from Empresas import Empresas
from Mensaje import Mensaje
from Respuesta import Alias_servicio, Empresa_con_Servicio, Respuesta

from Sentimiento import Sentimientos
from Servicios import Servicios
import re



def enviar():
    #para el boton enviar
    pass

app = Flask(__name__)


@app.route('/ConsultarDatos', methods=['GET'])  #tipo get

def ConsultarDatos():
    Datos = Diccionario()
#todo esto serivara para el boton enviar, aun asi tambien sirve
#para consultar fechas, la diferencia es que en enviar
#habra una lista unica para la funcion. Cada que entre a la funcio, inicializo una lista.
    binary_xml = request.get_data()
    xml = binary_xml.decode('utf-8')
    
    raiz = ET.XML(xml)
    
    mensaje_de_todo = ""

    
    for elem in raiz:
        if elem.tag == "diccionario":
            S = Sentimientos()
            
            Emp = Empresas()
            
            for subelem in elem:
                
                if subelem.tag == "sentimientos_positivos":
                    
                    lista_postivos = []
                    
                    for subsubelem in subelem:
                        sentimiento_positivo = subsubelem.text.lower()
                        sentimiento_positivo_sin_tildes = sentimiento_positivo.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                        
                        lista_postivos.append(sentimiento_positivo_sin_tildes) #se agrega sentiminetos en lista

                       
                    S.crear_diccionario("Positivo", lista_postivos)

                elif subelem.tag == "sentimientos_negativos":
                    
                    lista_negativos = []

                    for subsubelem in subelem:
                        sentimiento_negativo = subsubelem.text.lower()
                        sentimiento_negativo_sin_tildes = sentimiento_negativo.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")


                        lista_negativos.append(sentimiento_negativo_sin_tildes)   #se agregan sentiminetos en lista
                        
                        
                    S.crear_diccionario("Negativo", lista_negativos)

                elif subelem.tag == "empresas_analizar":
                    
                    
                    
                    for subsubelem in subelem:
                        Se = Servicios()
                        if subsubelem.tag == "empresa":

                            for sub_empresa in subsubelem:
                                if sub_empresa.tag == "nombre":
                                    nombre_empresa = sub_empresa.text.lower()
                                    nombre_empresa_sin_tildes = nombre_empresa.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                                    

                                elif sub_empresa.tag == "servicio":
                                    lista_servicios = []
                                    nombre_servicio = sub_empresa.get("nombre").lower()
                                    servicio_sin_espacios = nombre_servicio.strip(" ")
                                    nombre_servicio_sin_tildes = servicio_sin_espacios.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")

                                    
                                   

                                    cont = 0
                                    for sub_servicio in sub_empresa:
                                        cont+=1

                                    if cont == 0:
                                        Se.crear_servicio(nombre_servicio_sin_tildes, None)  #se crea la lista de servicios

                                    else:
                                        for sub_servicio in sub_empresa:
                                            sub_servicio_minuscula = sub_servicio.text.lower()
                                            sub_servicio_sin_tildes = sub_servicio_minuscula.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                                            sub_servicio_sin_espacios = sub_servicio_sin_tildes.strip(" ")
                                            lista_servicios.append(sub_servicio_sin_espacios)

                                        Se.crear_servicio(nombre_servicio_sin_tildes, lista_servicios)
                            dic_ser = Se.get_servicio()
                            Emp.crear_empresa(nombre_empresa_sin_tildes, dic_ser)  #se agrega la lista de servicios con su nombre

            #crear lista de diccionarios
            dic_emp = Emp.get_dic_empresas()
            dic_sen = S.get_dic_sentimientos()
            Datos.crear_lista_diccionarios(dic_sen, dic_emp)  #diccionario con sentimientos y empresas


    print("Datos del xml")
    mensaje_de_todo+="Datos del xml"
    mensaje_de_todo+="\n\n"
    datos = Datos.get_lista()
    for c in datos:
        print(c.dic_emp)
        print("")
        print(c.dic_sen)
        print("")
        msg1 = str(c.dic_emp)
        mensaje_de_todo+= msg1 + "\n" + "\n"
        msg2 = str(c.dic_sen)
        mensaje_de_todo+= msg2 + "\n" + "\n"

    print("")
    print("DATOS DE LOS MENSAJES")

    mensajes =[]  #lista con datos del mensaje incluido el mensaje

    #guarda el lugar, fecha, usuario, red social y msg del mensaje
    for elem in raiz:
        if elem.tag == "lista_mensajes":
            for subelem in elem:
                mensaje = subelem.text
                
                

                correcto = True
                variable = ""

                Fecha = ""
                Usuario = ""
                Red_Social = ""
                Lugar = ""
                msg = ""


                get_lugar = True
                get_fecha = False
                get_usuario = False
                get_red_social = False
                get_mensaje = False
                 

                i = 0
                while i < len(mensaje) and correcto == True:

                    caracter = mensaje[i]
                    
                

                    if caracter == ":" and get_lugar == True:
                        for posicion in range(len(mensaje)):
                            posicion = i+1
                            caracter_pre = mensaje[posicion]
                            
                            

                            if re.search(r'[a-zA-Z]', caracter_pre):
                                variable+=caracter_pre

                            elif caracter_pre == " ":
                                pass
                    
                            elif not re.search(r'[a-zA-Z]', caracter_pre):
                                Lugar = variable
                                #lugar = lugar_con_espacios.strip(" ")
                                
                                variable = ""
                                get_lugar = False
                                get_fecha = True
                                break

                            i+=1

                    elif re.search(r'[0-9]', caracter) and get_fecha == True:
                        for posicion in range(len(mensaje)):
                            posicion = i
                            caracter_pre = mensaje[posicion]

                            if caracter_pre != "U" or caracter_pre != "u":
                                variable+=caracter_pre

                            if re.search(r'[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]\ [0-9][0-9]\:[0-9][0-9]', variable):
                                Fecha = variable
                                
                                variable = ""
                                get_fecha = False
                                get_usuario = True
                                break

                            elif caracter_pre == "u" or caracter_pre == "U":
                                print("error con fecha")
                                correcto = False
                                break

                            i+=1

                    elif caracter == ":" and get_usuario == True:
                        for posicion in range(len(mensaje)):
                            posicion = i+2
                            
                            caracter_pre = mensaje[posicion]
                            

                            if caracter_pre != "\n" or caracter_pre != "\t" or caracter_pre != " ":
                                
                                
                                variable+=caracter_pre
                                sin_espacio = variable.strip(" ")
                                

                            if caracter_pre == "\n" or caracter_pre == "\t" or caracter_pre == " ":
                                


                                if re.search(r'([a-zA-Z]|[0-9])+\@?(([+A-zA-Z]|[0-9])+\.?)+', sin_espacio):
                                    Usuario = sin_espacio
                                    
                                    variable = ""
                                    get_usuario = False
                                    get_red_social = True
                                    break

                                else:
                                   
                                    break

                            i+=1
                 
                    elif caracter == ":" and get_red_social == True:
                        posicion = i+2
                        

                        while posicion < len(mensaje):
                            
                            
                            
                            caracter_pre = mensaje[posicion]
                            
                            

                            if re.search(r'[a-zA-Z]', caracter_pre):
                                
                                variable+=caracter_pre

                                

                            elif not re.search(r'[a-zA-Z]', caracter_pre):
                               
                                Red_Social = variable
                                
                                
                                variable = ""
                                get_red_social = False
                                get_mensaje = True
                                i = posicion
                                break

                           
                            posicion+=1
                            
                            
                    elif get_mensaje == True:
                        posicion = i
                        
                        while posicion < len(mensaje):
                            
                            caracter_pre = mensaje[posicion]
                            msg+=caracter_pre  

                            posicion+=1         

                        i = posicion
                        msg_conespacios = msg
                        msg = msg_conespacios.strip(" ")


                    i+=1

                if correcto == True:
                    Nuevo_mensaje = Mensaje(Lugar, Fecha, Usuario, Red_Social, msg)

                    mensajes.append(Nuevo_mensaje)

                    
    print("")

    mensaje_de_todo+="Datos del mensaje del xml" + "\n"
    for c in mensajes:
        place = str(c.lugar)
        print(place)
        mensaje_de_todo+= place + "\n" + "\n"
        hour = str(c.lugar)
        print(hour)
        mensaje_de_todo+= hour + "\n" + "\n"
        user = str(c.usuario)
        print(user)
        mensaje_de_todo+= user + "\n" + "\n"
        mensaje_de_todo+= str(c.red_social) + "\n" + "\n"
        print(c.red_social)
        mensaje_de_todo+= str(c.msg) + "\n" + "\n"
        print(c.msg)
        print("")
 
    
    list_respuestas = []
    for dato in mensajes:
        calificacion_alias =""
        calificacion_empresa = ""
        calificacion_mensaje = ""
        calificacion_servicio = ""

        palabras = []  #palabras del mensaje en minuscula y sin tildes
        positivos = 0
        negativos = 0
        hora_y_fecha = dato.fecha.split(" ")
        fecha_mensaje = hora_y_fecha[0].strip(" ")

        #print("Fecha:", fecha_mensaje)  #fecha del mensaje sin hora
        
        calificacion_mensaje = ""
        mensaje_sin_signos = dato.msg.replace(".","").replace(",","")  #lista de palabras del mensaje

        palabras_del_mensaje = mensaje_sin_signos.split(" ")
       

        for word in palabras_del_mensaje:
            palabra_minuscula = word.lower()
            palabra_sin_tildes = palabra_minuscula.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
            palabra_sin_espacio = palabra_sin_tildes.strip(" ")
            palabras.append(palabra_sin_espacio)

        for c in datos:
            palabras_positivas = c.dic_sen.get("Positivo")

            for p in palabras_positivas:
                if p.strip(" ") in palabras:
                    positivos+=1

            
        for c in datos:
            palabras_negativas = c.dic_sen.get("Negativo")

            for p in palabras_negativas:
                if p.strip(" ") in palabras:
                    negativos+=1

        

        if positivos == negativos:
            calificacion_mensaje = "neutro"
        
        elif positivos > negativos:
            calificacion_mensaje = "positivo"

        elif positivos < negativos:
            calificacion_mensaje = "negativo"

        #print("Calificacion_mensaje:", calificacion_mensaje)  #calificación del mensaje
        
        for c in datos:
            lista_empresas_archivo = c.dic_emp.keys()
            
        
       
            
        #empieza a ver todas las empresas
        list_empresas = []
        for c in lista_empresas_archivo:

            #verifico que exista la empresa en el msg
            if c.strip(" ") in palabras:
               
                
                empresa_del_mensaje = c.strip(" ")
                calificacion_empresa = calificacion_mensaje

                #print("Empresa:", empresa_del_mensaje) #nombre de la empresa
                #print("Calificacion_empresa:", calificacion_empresa) #calificacion de la empresa
                
                #creo las oraciones

                oracion_sin_punto_final = dato.msg.strip(".")
                oraciones_en_minuscula = oracion_sin_punto_final.lower()
                oraciones_sin_tildes = oraciones_en_minuscula.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                oraciones = oraciones_sin_tildes.split(",")  #lista de oraciones del msg
                positivos_oracion = 0
                negativos_oracion = 0

                #revisar la empresa y servicio en cada oracion
                for oracion in oraciones:  

                    #recolecto cada servicio de la empresa con sus alias
                    servicio_empresa_dic = datos[0].dic_emp.get(c)


                    #contiene cada servicio de la empresa
                    servicio_individual_de_empresa = servicio_empresa_dic.keys()

                    #recolecto las palabras positivas y negativas
                    for dato_for_empresa in datos:
                        palabras_positivas = dato_for_empresa.dic_sen.get("Positivo")
                        palabras_negativas = dato_for_empresa.dic_sen.get("Negativo")


                    #contabilizo las palabras positivas y negativas de la oracion
                    for palabra in palabras_positivas:
                        if palabra.strip(" ") in oracion:
                            positivos_oracion+=1

                    for palabra in palabras_negativas:
                        if palabra.strip(" ") in oracion:
                            negativos_oracion+=1

                    list_alias = []
                    #revisa que cada servicio y alias este en la oracion
                    for servicio in servicio_individual_de_empresa:

                        dic_alias = {}
                        
                        #consigo los alias de cada servicio
                        alias_servicio = servicio_empresa_dic.get(servicio)
                        
                        if servicio in oracion:
                           

                            
                            
                            if positivos_oracion == negativos_oracion:
                                calificacion_servicio = "neutro"

                            elif positivos_oracion > negativos_oracion:
                                calificacion_servicio = "positivo"

                            elif positivos_oracion < negativos:
                                calificacion_servicio = "negativo"

                        else:
                            servicio = "None"
                            calificacion_servicio = "None"

                        #print("")
                        #print("Servicio:", servicio)  #Servicio de la empresa
                        #print("calificacion_servicio:", calificacion_servicio)
                        #verifica si tiene alias el servicio
                        if alias_servicio != None:
                            
                            #busca si el alias esta en la oracion
                            for alias in alias_servicio:
                               
                                
                                if alias.strip(" ") in oracion:
                                    
                                    nombre_alias = alias.strip(" ")

                                    if positivos_oracion == negativos_oracion:
                                        calificacion_alias = "neutro"

                                    elif positivos_oracion > negativos_oracion:
                                        calificacion_alias = "positivo"

                                    elif positivos_oracion < negativos:
                                        calificacion_alias = "negativo"

                                        #crear diccionario para los alias
                                    dic_alias[nombre_alias] = calificacion_alias
                                
                                else:
                                    nombre_alias = "None"
                                    calificacion_alias = "None"
                                                       

                            Nuevo_Alias = Alias_servicio(servicio, calificacion_servicio, dic_alias)
                            list_alias.append(Nuevo_Alias)


                Nueva_empresa = Empresa_con_Servicio(empresa_del_mensaje, calificacion_empresa, list_alias)
                list_empresas.append(Nueva_empresa)



        Nueva_respuesta = Respuesta(fecha_mensaje, calificacion_mensaje, list_empresas)
        list_respuestas.append(Nueva_respuesta)



   

    for element in list_respuestas:
        print("fecha:",element.Fecha)
        print("calificacion_mensaje:",element.Calificacion_mensaje)

        lista_empresas = element.empresa_con_servicios
        for work in lista_empresas:
            print("empresa:",work.nombre_empresa)
            print("calificacion_empresa:",work.calificacion_empresa)

            lista_servers = work.servicios
            for server in lista_servers:
                print("nombre_servicio:",server.nombre_servicio)
                print("calificacion_servicio:",server.calificacion_servicio)
                print(server.alias.items())

        print("") 


    return mensaje_de_todo




@app.route('/ConsultarFecha', methods=['POST'])  #post

def ConsultarFechas():
    return "consultando fechas"


@app.route('/ProcesarMensaje', methods=['POST'])  #post

def ProcesarMensaje():
    return "porcesando"


@app.route('/Grafica', methods=['GET'])  #get

def Grafica():
    return "graficando"












if __name__== '__main__':
       #lista de diccionarios, este sirve
                            #para el boton enviar
                            #al iniciar el programa se crea la lista que sera la base de datos
    app.run(debug=True)