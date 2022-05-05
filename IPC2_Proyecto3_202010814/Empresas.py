class Empresas:

    def __init__(self):
        self.diccionario_empresa = {}


    def crear_empresa(self, nombre_empresa, diccionario):
        #crear diccionario empresa
        self.diccionario_empresa[nombre_empresa] = diccionario

    
    def get_dic_empresas(self):
        return self.diccionario_empresa