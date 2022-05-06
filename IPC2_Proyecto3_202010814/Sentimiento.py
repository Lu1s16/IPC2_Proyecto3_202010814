class Sentimientos:


    def __init__(self):
        self.diccionario_sentimientos = {}

    def crear_diccionario(self, sentimiento, palabra):
        
        #creo el diccionario
        self.diccionario_sentimientos[sentimiento] = palabra
        

    def get_dic_sentimientos(self):
        return self.diccionario_sentimientos