# Importa la clase Servicio desde el módulo modelos.servicio.
# Esta clase será la clase padre de ServicioSala.
from modelos.servicio import Servicio
# Importa la excepción personalizada para controlar datos inválidos.
from excepciones.errores import DatoInvalidoError
# Define la clase ServicioSala, que hereda los atributos y métodos de Servicio.
class ServicioSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        try:
            self.capacidad = int(capacidad)
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError("La capacidad debe ser en numero entero") from exc
        if self.capacidad < 1:
            raise DatoInvalidoError("La capacidad minima es de 1.")
    # Define un método para validar los parámetros de una reserva.
    # Recibe la duración de la reserva en horas.    
    def validar_parametros(self, duracion):
        if float(duracion) > 12:
            raise DatoInvalidoError("Una sala no puede reservarse por mas de 12 horas")
    # Define el método encargado de calcular el costo de reservar la sala.
    # Recibe la duración, el impuesto y el descuento.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        costo = super().calcular_costo(duracion, impuesto, descuento)
        return round(costo * 1.10, 2) if self.capacidad > 20 else costo
    # Define un método que devuelve una descripción de la sala.
    def describir(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} | ${self.tarifa_hora:,.0f}/hora"