import logging
from pathlib import Path

from modelos.cliente import Cliente
from modelos.reserva import Reserva
from servicios.sala import ServicioSala
from servicios.equipo import AlquilerEquipo
from servicios.asesoria import AsesoriaEspecializada
from excepciones.errores import DatoInvalidoError, ClienteNoEncontradoError, ParametroFaltanteError


class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []
        self.configurar_logs()

    @staticmethod
    def configurar_logs():
        carpeta = Path(__file__).resolve().parent.parent / "logs"
        carpeta.mkdir(exist_ok=True)
        logger = logging.getLogger("SoftwareFJ")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.FileHandler(carpeta / "software_fj.log", encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            logger.addHandler(handler)

    @property
    def logger(self):
        return logging.getLogger("SoftwareFJ")

    def registrar_cliente(self, nombre, documento, correo, telefono):
        try:
            if any(c.documento == str(documento).strip() for c in self.clientes):
                raise DatoInvalidoError("Ya existe un cliente con ese documento")
            cliente = Cliente(nombre, documento, correo, telefono)
            self.clientes.append(cliente)
        except Exception:
            self.logger.exception("Error al registrar cliente.")
            raise
        else:
            self.logger.info("Cliente registrado: %s", cliente.id)
            return cliente
        finally:
            self.logger.info("Finalizo registro de cliente")

    def agregar_servicio(self, tipo, nombre, tarifa, extra, disponible=True):
        try:
            tipo = tipo.lower()
            if tipo == "sala":
                servicio = ServicioSala(nombre, tarifa, extra, disponible)
            elif tipo == "equipo":
                servicio = AlquilerEquipo(nombre, tarifa, extra, disponible)
            elif tipo == "asesoria":
                servicio = AsesoriaEspecializada(nombre, tarifa, extra, disponible)
            else:
                raise DatoInvalidoError("Tipo de servicio desconocido")
            self.servicios.append(servicio)
        except Exception:
            self.logger.exception("Error al crear servicio.")
            raise
        else:
            self.logger.info("Servicio creado: %s", servicio.id)
            return servicio

    def buscar_cliente(self, documento):
        for cliente in self.clientes:
            if cliente.documento == str(documento).strip():
                return cliente
        raise ClienteNoEncontradoError("No se encontro el cliente")

    def buscar_servicio(self, servicio_id):
        for servicio in self.servicios:
            if servicio.id == servicio_id:
                return servicio
        raise DatoInvalidoError("No se encontro el servicio")

    def crear_reserva(self, documento, servicio_id, duracion, impuesto=19, descuento=0):
        try:
            if not str(documento).strip() or not servicio_id or str(duracion).strip() == "":
                raise ParametroFaltanteError("Faltan parametros obligatorios para la reserva")
            cliente = self.buscar_cliente(documento)
            servicio = self.buscar_servicio(servicio_id)
            servicio.validar_disponibilidad()
            reserva = Reserva(cliente, servicio, duracion, impuesto, descuento)
            self.reservas.append(reserva)
        except Exception:
            self.logger.exception("Error al crear reserva")
            raise
        else:
            self.logger.info("Reserva creada: %s", reserva.id)
            return reserva
        finally:
            self.logger.info("Finalizo creacion de reserva")

    def buscar_reserva(self, reserva_id):
        for reserva in self.reservas:
            if reserva.id == reserva_id:
                return reserva
        raise DatoInvalidoError("No se encontro la reserva.")

    def confirmar_reserva(self, reserva_id):
        try:
            reserva = self.buscar_reserva(reserva_id)
            reserva.procesar()
        except Exception:
            self.logger.exception("Error al confirmar reserva.")
            raise
        else:
            self.logger.info("Reserva confirmada: %s", reserva_id)
            return reserva

    def cancelar_reserva(self, reserva_id):
        try:
            reserva = self.buscar_reserva(reserva_id)
            reserva.cancelar()
        except Exception:
            self.logger.exception("Error al cancelar reserva.")
            raise
        else:
            self.logger.info("Reserva cancelada: %s", reserva_id)
            return reserva

    def demostracion(self):
        resultados = []
        estado = {}

        def crear_sala():
            estado["sala"] = self.agregar_servicio("sala", "Sala reuniones", 50000, 12)

        def reserva_valida():
            estado["reserva"] = self.crear_reserva("10000001", estado["sala"].id, 2)

        def servicio_no_disponible():
            cerrada = self.agregar_servicio("sala", "Sala cerrada", 30000, 5, False)
            self.crear_reserva("10000001", cerrada.id, 1)

        operaciones = [
            ("Cliente valido 1", lambda: self.registrar_cliente("Laura Gomez", "10000001", "laura@email.com", "3001234567")),
            ("Cliente valido 2", lambda: self.registrar_cliente("Carlos Perez", "10000002", "carlos@email.com", "3101234567")),
            ("Cliente invalido", lambda: self.registrar_cliente("Jo", "ABC", "correo-email", "123")),
            ("Crear sala", crear_sala),
            ("Crear equipo", lambda: self.agregar_servicio("equipo", "Proyector", 20000, 4)),
            ("Crear asesoria", lambda: self.agregar_servicio("asesoria", "Consultoria TI", 80000, "Tecnologia")),
            ("Servicio invalido", lambda: self.agregar_servicio("otro", "Servicio", 10000, 1)),
            ("Reserva valida", reserva_valida),
            ("Cliente inexistente", lambda: self.crear_reserva("99999999", estado["sala"].id, 1)),
            ("Duracion invalida", lambda: self.crear_reserva("10000001", estado["sala"].id, -5)),
            ("Duracion excede limite", lambda: self.crear_reserva("10000001", estado["sala"].id, 20)),
            ("Parametro faltante", lambda: self.crear_reserva("", estado["sala"].id, 1)),
            ("Servicio no disponible", servicio_no_disponible),
            ("Confirmar reserva", lambda: self.confirmar_reserva(estado["reserva"].id)),
            ("Cancelar reserva", lambda: self.cancelar_reserva(estado["reserva"].id)),
            ("Confirmar reserva cancelada", lambda: self.confirmar_reserva(estado["reserva"].id)),
        ]
        for nombre, operacion in operaciones:
            try:
                operacion()
            except Exception as exc:
                self.logger.exception("Demostracion: %s", nombre)
                resultados.append(f"ERROR CONTROLADO: {nombre} - {exc}")
            else:
                resultados.append(f"CORRECTO: {nombre}")
        return resultados