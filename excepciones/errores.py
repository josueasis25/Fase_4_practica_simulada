# Clase principal que agrupa todas las excepciones personalizadas del sistema.
class ErrorSoftware(Exception):
    pass
# Se utiliza cuando se introduce un dato incorrecto o que no cumple las validaciones.
class DatoInvalidoError(ErrorSoftware):
    pass
# Se utiliza cuando se intenta buscar un cliente que no está registrado.
class ClienteNoEncontradoError(ErrorSoftware):
    pass
# Se utiliza cuando se intenta utilizar un servicio que no está disponible.
class ServicioNoDisponibleError(ErrorSoftware):
    pass
# Se utiliza cuando una reserva contiene datos incorrectos o no cumple las condiciones establecidas.
class ReservaInvalidaError(ErrorSoftware):
    pass
# Se utiliza cuando se intenta realizar una operación que no está permitida por el sistema.
class OperacionNoPermitidaError(ErrorSoftware):
    pass
# Se utiliza cuando falta un parámetro obligatorio para realizar una operación.
class ParametroFaltanteError(ErrorSoftware):
    pass