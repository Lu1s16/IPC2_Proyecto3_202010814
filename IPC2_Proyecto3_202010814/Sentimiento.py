class Sentimientos:


    def __init__(self):
        self.diccionario_sentimientos = {}

    def crear_diccionario(self, sentimiento, palabra):
        print("se agrego")
        #creo el diccionario
        self.diccionario_sentimientos[sentimiento] = palabra
        print('\t', self.diccionario_sentimientos.items())

    def get_dic_sentimientos(self):
        return self.diccionario_sentimientos