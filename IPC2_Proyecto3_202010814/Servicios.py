class Servicios:

    def __init__(self):
        self.diccionario_servicios = {}

    def crear_servicio(self, servicio, alias):
        #se crea diccionario de servicios
        self.diccionario_servicios[servicio] = alias


    def get_servicio(self):
        return self.diccionario_servicios
