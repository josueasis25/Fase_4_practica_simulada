# Importa el módulo re para validar el formato de los correos electrónicos.
import re
# Importa la clase abstracta Entidad, de la cual heredará Cliente.
from modelos.entidad import Entidad
# Importa la excepción para controlar los datos inválidos.
from excepciones.errores import DatoInvalidoError
# Clase Cliente que hereda los atributos y métodos de Entidad.
class Cliente(Entidad):
    # Constructor: inicializa los datos del cliente.
    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
    # Devuelve el nombre y el documento del cliente.    
    def registrar_cliente(self):
        return f"nombre: {self.nombre}\ndocumento: {self.documento}"         
    # Permite consultar el nombre del cliente.    
    @property
    def nombre(self):
        return self.__nombre
    # Valida y asigna el nombre del cliente.    
    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip().title()
    # Permite consultar el documento del cliente.        
    @property
    def documento(self):
        return self.__documento
    # Valida y asigna el documento del cliente.   
    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or not 5 <= len(valor) <= 15:
            raise DatoInvalidoError("El documento debe contener entre 5 y 15 dígitos")
        self.__documento = valor
    # Permite consultar el correo electrónico del cliente.       
    @property
    def correo(self):
        return self.__correo
    # Valida y asigna el correo electrónico del cliente.    
    @correo.setter
    def correo(self, valor):
        valor = str(valor).strip()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise DatoInvalidoError("El correo electronico no tiene un formato valido")
        self.__correo = valor.lower()
    # Permite consultar el teléfono del cliente.        
    @property
    def telefono(self):
        return self.__telefono
    # Valida y asigna el teléfono del cliente.
    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if not valor.isdigit() or not 7 <= len(valor) <= 15:
            raise DatoInvalidoError("El telefono debe contener entre 7 y 15 digitos.")
        self.__telefono = valor
    # Devuelve una descripción resumida del cliente.        
    def describir(self):
        return f"{self.nombre} | CC: {self.documento} | {self.correo}"