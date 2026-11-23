# Importa la clase Servicio, de la cual heredará esta clase.
from modelos.servicio import Servicio
# Importa la excepción para controlar datos inválidos.
from excepciones.errores import DatoInvalidoError
# Clase AsesoriaPersonalizada que hereda de Servicio.
class AsesoriaEspecializada(Servicio):
    # Constructor: inicializa los datos de la asesoría personalizada.
    def __init__(self, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()
    # Valida que la duración de la asesoría no supere las 8 horas.        
    def validar_parametros(self, duracion):
        if float(duracion) > 8:
            raise DatoInvalidoError("Una asesoria no puede superar 8 horas.")
    # Devuelve una descripción de la asesoría,
    # incluyendo su nombre, especialidad y tarifa por hora.        
    def describir(self):
        return f"Asesoria: {self.nombre} | Especialidad: {self.especialidad} | ${self.tarifa_hora:,.0f}/hora"