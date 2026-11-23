# Importa Enum para crear un conjunto de estados posibles para las reservas.
from enum import Enum

from modelos.entidad import Entidad
# Importa las excepciones personalizadas para controlar errores en las reservas.
from excepciones.errores import ReservaInvalidaError, OperacionNoPermitidaError

# Define los posibles estados de una reserva.
class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
# Clase Reserva que hereda los atributos y métodos de Entidad.
class Reserva(Entidad):    
    # Constructor: inicializa los datos necesarios para crear una reserva.
    def __init__(self, cliente, servicio, duracion, impuesto=19, descuento=0):
        super().__init__()
        # Comprueba que se haya proporcionado un cliente y un servicio.
        if cliente is None or servicio is None:
            raise ReservaInvalidaError("Se requiere un cliente y un servicio.")
        # Asigna el cliente y el servicio a la reserva.        
        self.cliente, self.servicio = cliente, servicio
        # Intenta convertir la duración a un número decimal.
        try:
            self.duracion = float(duracion)
        # Captura errores si la duración no es un valor numérico.       
        except (TypeError, ValueError) as exc:
            raise ReservaInvalidaError("La duracion debe ser numerica.") from exc
        # Comprueba que la duración sea mayor que cero.
        if self.duracion <= 0:
            raise ReservaInvalidaError("La duracion debe ser mayor que cero.")
        # Verifica que el servicio permita la duración solicitada.
        servicio.validar_parametros(self.duracion)
        # Intenta convertir el impuesto y el descuento a números decimales.
        try:
            self.impuesto, self.descuento = float(impuesto), float(descuento)
        # Captura errores si alguno de los valores no es numérico
        # (por ejemplo, un texto vacío o con letras).
        except ( TypeError, ValueError) as exc:
            raise ReservaInvalidaError("El impuesto y el descuento deben ser numericos") from exc
        # Calcula el costo total de la reserva según el servicio,
        # la duración, el impuesto y el descuento.
        self.costo = servicio.calcular_costo(self.duracion, self.impuesto, self.descuento)
        # Establece el estado inicial de la reserva como pendiente.
        self.__estado = EstadoReserva.PENDIENTE
        # Permite consultar el estado actual de la reserva.        
    @property
    def estado(self):
        return self.__estado
    # Cambia el estado de la reserva a confirmada.
    def confirmar(self):
        if self.__estado == EstadoReserva.CANCELADA:
            raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada.")
        self.servicio.validar_disponibilidad()
        self.__estado = EstadoReserva.CONFIRMADA
    # Cambia el estado de la reserva a cancelada.  
    def cancelar(self):
        if self.__estado == EstadoReserva.CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya esta cancelada")
        self.__estado = EstadoReserva.CANCELADA
    # Intenta procesar la reserva mediante su confirmación.
    def procesar(self):
        try:
            self.confirmar()
        except Exception as exc:
            raise ReservaInvalidaError("No fue posible procesar la reserva") from exc
    # Devuelve una descripción completa de la reserva.    
    def describir(self):
        return (f"Reserva {self.id} | {self.cliente.nombre} | {self.servicio.nombre} |" 
                f"{self.duracion:g} h | ${self.costo:,.2f} | {self.estado.value}")