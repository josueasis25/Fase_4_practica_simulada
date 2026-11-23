# Importa abstractmethod para definir métodos que las clases hijas
# están obligadas a implementar.
from abc import abstractmethod
# Importa la clase Entidad, de la cual heredará Servicio.
from modelos.entidad import Entidad
# Importa la excepción para controlar datos inválidos.
from excepciones.errores import DatoInvalidoError, ServicioNoDisponibleError
# Clase Servicio que hereda los atributos y métodos de Entidad.
class Servicio(Entidad):
    # Constructor: inicializa los datos generales de un servicio. 
    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        # Comprueba que el nombre sea un texto válido y no esté vacío.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio")
        self.nombre = nombre.strip()
        # Intenta convertir la tarifa por hora a un número decimal.
        try:
            self.tarifa_hora = float(tarifa_hora)
        # Captura errores si la tarifa no es un valor numérico.
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError("La tarifa debe ser numerica") from exc
        # Comprueba que la tarifa sea mayor que cero.
        if self.tarifa_hora <= 0:
            raise DatoInvalidoError("La tarifa debe ser mayor que cero.")
        self.disponible = bool(disponible)
    # Comprueba si el servicio se encuentra disponible.    
    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio {self.nombre} no esta disponible")

    # Calcula el costo total del servicio teniendo en cuenta
    # su duración, el impuesto y el descuento.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        # Intenta convertir los valores recibidos a números decimales.
        try:
            duracion, impuesto, descuento = float(duracion), float(impuesto), float(descuento)
        # Captura errores si alguno de los valores no es numérico.
        except (TypeError, ValueError) as exc:
            raise DatoInvalidoError("Duracion, impuesto y descuento deben ser numericos.") from exc
        # Comprueba que el impuesto y el descuento estén entre 0 y 100.
        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatoInvalidoError("Impuesto y descuento deben estar entre 0 y 100")
        if duracion <= 0:
            raise DatoInvalidoError("La duracion debe ser mayor de cero")
        subtotal = self.tarifa_hora * duracion
        base = subtotal - subtotal * descuento / 100
        return round(base + base * impuesto / 100, 2)
    
    def calcular_costo_con_impuesto(self, duracion, impuesto):
        return self.calcular_costo(duracion, impuesto, 0)
    
    def calcular_costo_con_descuento(self, duracion, descuento):
        return self.calcular_costo(duracion, 0, descuento)
    
    # Método abstracto que obliga a las clases hijas
    # a implementar su propia descripción del servicio.
    @abstractmethod
    def describir(self):
        pass

    # Método abstracto que obliga a las clases hijas
    # a implementar la validación de los parámetros de duración.
    @abstractmethod
    def validar_parametros(self, duracion):
        pass