# Importa la clase Servicio, de la cual heredará AlquilerEquipo.
from modelos.servicio import Servicio
# Importa la excepción personalizada para informar errores en los datos.
from excepciones.errores import DatoInvalidoError
# Define la clase AlquilerEquipo como una especialización de Servicio.
class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_hora, unidades, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        try:
            self.unidades = int(unidades)
        except(TypeError, ValueError) as exc:
            raise DatoInvalidoError("Las unidades deben ser un numero entero") from exc
        if self.unidades < 1:
            raise DatoInvalidoError("Debe existir al menos una unidad")
    # Inicializa un servicio de alquiler de equipos.
    def validar_parametros(self, duracion):
        if float(duracion) > 72:
            raise DatoInvalidoError("El alquiler no puede superar 72 horas.")
    # Valida que la duración del alquiler no supere el límite permitido.    
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        return round(super().calcular_costo(duracion, impuesto, descuento) * 1.15, 2)
    # Calcula el costo del alquiler aplicando un recargo adicional del 15 %.    
    def describir(self):
        return f"Equipo: {self.nombre} | Unidades: {self.unidades} | ${self.tarifa_hora:,.0f}/hora"