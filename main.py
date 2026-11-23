# Importa la clase VentanaPrincipal desde el módulo ventana_principal,
# ubicado dentro del paquete interfaz.
from interfaz.ventana_principal import VentanaPrincipal

# Comprueba si este archivo se está ejecutando directamente
# y no está siendo importado desde otro archivo.
if __name__ == "__main__":
    # Crea una instancia (objeto) de la clase VentanaPrincipal.
    # Esto permite construir y mostrar la ventana principal del programa.
    ventana = VentanaPrincipal()
    # Inicia el bucle principal de Tkinter.
    # Mantiene la ventana abierta, permite interactuar con los botones,
    # campos de texto y demás elementos de la interfaz gráfica.
    ventana.mainloop()