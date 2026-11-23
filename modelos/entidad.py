# Importa ABC y abstractmethod para crear clases abstractas
# y metodos que las clases hijas estan obligadas a implementar.
from abc import ABC, abstractmethod
# Importa datetime para obtener la fecha y hora actual.
from datetime import datetime
# Importa uuid4 para generar identificadores unicos.
from uuid import uuid4
# Clase abstracta Entidad que sirve como clase base
# para las demas clases del sistema.
class Entidad(ABC):
    # Constructor: inicializa el identificador y la fecha de creacion.
    def __init__(self):
        # Genera un identificador unico de 8 caracteres en mayusculas.        
        self.__id = str(uuid4())[:8].upper()
        # Guarda la fecha y hora en que se crea la entidad.
        self.__fecha_creacion = datetime.now()
    
    # Permite consultar el identificador de la entidad.
    @property
    def id(self):
        return self.__id
    
    # Permite consultar la fecha de creacion.
    @property
    def fecha_creacion(self):
        return self.__fecha_creacion
    
    # Metodo abstracto que obliga a las clases hijas
    # a implementar su propia descripcion.
    @abstractmethod
    def describir(self):
        pass