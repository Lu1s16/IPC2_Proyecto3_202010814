class Respuesta:

    def __init__(self, fecha, calificacion_mensaje, empresa_con_servicios):
        self.Fecha = fecha #fecha del mensaje sin hora
        self.Calificacion_mensaje = calificacion_mensaje  #positivo, negativo neutro del mensaje
        self.empresa_con_servicios = empresa_con_servicios 
        #objeto con nombre, calificación y objeto empresa

class Empresa_con_Servicio:

    def __init__(self, nombre_empresa, calificacion_empresa, servicios):
        self.nombre_empresa = nombre_empresa #nombre de la empresa
        self.calificacion_empresa = calificacion_empresa #calificación de la empresa
        self.servicios = servicios 
        # lista de objetos con nombre_servicio, calificacion_servicio, diccionario alias


class Alias_servicio:
    def __init__(self, nombre_servicio, calificacion_servicio, alias):

        self.nombre_servicio = nombre_servicio #nombre servicio
        self.calificacion_servicio = calificacion_servicio #calificacion servicio
        self.alias = alias 
        #lista de diccionarios de alias con clave: nombre alias, valor: calificacion