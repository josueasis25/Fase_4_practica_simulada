from modelos.servicio import Servicio
from excepciones.errores import DatoInvalidoError

class ServicioSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        try:
            self.capacidad = int(capacidad)
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError("La capacidad debe ser en numero entero") from exc
        if self.capacidad < 1:
            raise DatoInvalidoError("La capacidad minima es de 1.")
        
    def validar_parametros(self, duracion):
        if float(duracion) > 12:
            raise DatoInvalidoError("Una sala no puede reservarse por mas de 12 horas")
    
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        costo = super().calcular_costo(duracion, impuesto, descuento)
        return round(costo * 1.10, 2) if self.capacidad > 20 else costo
    
    def describir(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} | ${self.tarifa_hora:,.0f}/hora"