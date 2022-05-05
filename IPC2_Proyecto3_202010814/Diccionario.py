from Diccionarios import Diccionarios

class Diccionario:

    def __init__ (self):
        self.lista_datos = []


    def crear_lista_diccionarios(self, dic_sentimientos, dic_empresas):
        #creo lista diccionario
        nuevos_diccionarios = Diccionarios(dic_sentimientos, dic_empresas)
        self.lista_datos.append(nuevos_diccionarios)


    def get_lista(self):
        return self.lista_datos


