# Importa tkinter para crear la ventana principal de la aplicación.
import tkinter as tk
# Importa ttk para utilizar componentes gráficos mejorados
# y messagebox para mostrar ventanas de información y errores.
from tkinter import ttk, messagebox
# Importa la clase principal encargada de gestionar las operaciones del sistema.
from gestion.sistemas import SistemaSoftwareFJ
# Clase VentanaPrincipal que hereda de tk.Tk y representa
# la ventana principal de Software FJ.
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.sistema = SistemaSoftwareFJ()
        self.title("Software FJ | Gestion integral")
        self.geometry("1080x700")
        self.minsize(900, 580)
        self._estilos()
        self._interfaz()
        self._actualizar()
    # Configura los estilos de los elementos gráficos.        
    def _estilos(self):
        style = ttk.Style(self)
        style.theme_use("winnative")
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("TButton", padding=7)
        style.configure("TNotebook.Tab", padding=(15, 8))
    # Construye la estructura principal de la interfaz gráfica.    
    def _interfaz(self):
        top = tk.Frame(self, height=82)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="SOFTWARE FJ", font=("Segoe UI", 21, "bold")).pack(anchor="w", padx=22, pady=(10, 0))
        tk.Label(top, text="Gestion integral de clientes, servicios y reservas").pack(anchor="w", padx=24)
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=14, pady=14)
        self.tclientes, self.tservicios, self.treservas, self.tpruebas = [ttk.Frame(self.tabs, padding=12) for _ in range(4)]
        for tab, name in [(self.tclientes, "Clientes"), (self.tservicios, "Servicios"),
                          (self.treservas, "Reservas"), (self.tpruebas, "Pruebas y logs")]:
            self.tabs.add(tab, text=name)
        self._tab_clientes()
        self._tab_servicios()
        self._tab_reservas()
        self._tab_pruebas()
    # Crea un campo de entrada con su respectiva etiqueta.
    def _entry(self, parent, label, row, col):
        tk.Label(parent, text=label,bg="white", font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="w", padx=6, pady=4)
        e = ttk.Entry(parent, width=24)
        e.grid(row=row+1, column=col, sticky="ew", padx=6, pady=(0, 7))
        return e
    # Crea una tabla para mostrar información organizada.
    def _tree(self, parent, cols, headings):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col, head in zip(cols, headings):
            tree.heading(col, text=head)
            tree.column(col, width=130, anchor="center")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree
    # Construye la pestaña encargada de registrar y mostrar clientes.
    def _tab_clientes(self):
        box = tk.LabelFrame(self.tclientes, text="Registrar cliente", bg="white", padx=8, pady=8)
        box.pack(fill="x", pady=(0, 10))
        self.cn = self._entry(box, "Nombre completo",0 ,0)
        self.cd = self._entry(box, "Documento",0, 1)
        self.cc = self._entry(box, "Correo", 0, 2)
        self.ct = self._entry(box, "Telefono", 0, 3)
        ttk.Button(box, text="Registrar cliente", command=self._registrar).grid(row=2, column=0, columnspan=4, sticky="ew", padx=6)
        self.tc = self._tree(self.tclientes, ("id","nombre","doc","correo","tel"), ("ID","Nombre","Documento","Correo","Teléfono"))
    # Construye la pestaña para crear y consultar servicios.    
    def _tab_servicios(self):
        box = tk.LabelFrame(self.tservicios, text="Crear servicio", bg="white", padx=8, pady=8)
        box.pack(fill="x", pady=(0, 10))
        tk.Label(box, text="Tipo", bg="white").grid(row=0, column=0, sticky="w", padx=6)
        self.st = ttk.Combobox(box, values=["Sala", "Equipo", "Asesoria"], state="readonly", width=21)
        self.st.current(0)
        self.st.grid(row=1, column=0, padx=6, pady=5)
        self.sn = self._entry(box, "Nombre", 0, 1)
        self.sv = self._entry(box, "Tarifa por hora", 0, 2)
        self.se = self._entry(box, "Capacidad / Unidades / Especialidad", 0, 3)
        ttk.Button(box, text="Crear servicio", command=self._crear_servicio).grid(row=2, column=0, columnspan=4, sticky="ew", padx=6)
        self.ts = self._tree(self.tservicios, ("id", "tipo", "nombre", "tarifa", "extra"), ("ID", "Tipo", "Nombre", "Tarifa/hora", "Detalle"))
    # Construye la pestaña encargada de gestionar las reservas.    
    def _tab_reservas(self):
            box = tk.LabelFrame(self.treservas, text="Crear y gestionar reserva", bg="white", padx=8, pady=8)
            box.pack(fill="x", pady=(0, 10))
            self.rd = self._entry(box, "Documento cliente", 0, 0)
            tk.Label(box, text="Servicio", bg="white").grid(row=0, column=1, sticky="w", padx=6)
            self.rs = ttk.Combobox(box, state="readonly", width=25)
            self.rs.grid(row=1, column=1, padx=6, pady=(0,7))
            self.rh = self._entry(box, "Duración (horas)", 0, 2)
            self.rdes = self._entry(box, "Descuento (%)", 0, 3)
            ttk.Button(box, text="Crear reserva", command=self._crear_reserva).grid(row=2, column=0, padx=5, sticky="ew")
            ttk.Button(box, text="Confirmar seleccionada", command=self._confirmar).grid(row=2, column=1, padx=5, sticky="ew")
            ttk.Button(box, text="Cancelar seleccionada", command=self._cancelar).grid(row=2, column=2, columnspan=2, padx=5, sticky="ew")
            self.tr = self._tree(self.treservas, ("id","cliente","servicio","horas","costo","estado"), ("ID","Cliente","Servicio","Horas","Costo","Estado"))
    # Construye la pestaña de pruebas y consulta de registros.        
    def _tab_pruebas(self):
        tk.Label(self.tpruebas, text="Demostracion de 12 operaciones y manejo de excepciones", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        ttk.Button(self.tpruebas, text="Ejecutar demostracion", command=self._pruebas).pack(anchor="w", pady=4)
        ttk.Button(self.tpruebas, text="Abrir archivo de logs", command=self._logs).pack(anchor="w", pady=4)
        self.out = tk.Text(self.tpruebas, bg="#101c2c", fg="#d9e5f2", font=("Consolas", 9), wrap="word")
        self.out.pack(fill="both", expand=True, pady=8)
    # Ejecuta una función y controla los errores que puedan presentarse.    
    def _seguro(self, funcion):
        try:
            return funcion()
        except Exception as exc:
            messagebox.showerror("Operacion no completada", str(exc))
            return None
    # Recoge los datos de los campos y registra un nuevo cliente.    
    def _registrar(self):
        # Define la operación que se ejecutará de forma controlada.
        def accion():
            c = self.sistema.registrar_cliente(self.cn.get(), self.cd.get(), self.cc.get(), self.ct.get())
            self._actualizar()
            messagebox.showinfo("Correo", f"Cliente {c.nombre} regsitrado")
            for e in (self.cn, self.cd, self.cc, self.ct): 
                e.delete(0, "end")
        self._seguro(accion)
    # Recoge los datos y crea un nuevo servicio.        
    def _crear_servicio(self):
        # Define la operación encargada de crear el servicio.
        def accion():
            s = self.sistema.agregar_servicio(self.st.get(), self.sn.get(), self.sv.get(), self.sv.get())
            self._actualizar()
            messagebox.showinfo("Correcto", f"Servicio {s.nombre} creado")
            for e in (self.sn, self.sv, self.se):
                e.delete(0, "end")
        self._seguro(accion)
    # Recoge los datos y crea una nueva reserva.    
    def _crear_reserva(self):
        # Define la operación encargada de crear la reserva.
        def accion():
            if not self.rs.get(): raise ValueError("Seleccione un servicio")
            sid = self.rs.get().split(" | ")[0]
            r = self.sistema.crear_reserva(self.rd.get(), sid, self.rh.get(), 19, self.rdes.get() or 0)
            self._actualizar()
            messagebox.showinfo("Reserva creada", f"ID: {r.id}\nCosto: ${r.costo:,.2f}\nEstado: {r.estado.value}")
        self._seguro(accion)
    # Obtiene el identificador de la reserva seleccionada en la tabla.            
    def _id_reserva(self):
        sel = self.tr.selection()
        if not sel: raise ValueError("Seleccione una reserva")
        return self.tr.item(sel[0], "values")[0]
    # Confirma la reserva seleccionada.    
    def _confirmar(self):
        # Define la operación de confirmación.
        def accion():
            r = self.sistema.confirmar_reserva(self._id_reserva())
            self._actualizar()
            messagebox.showinfo("Correto", f"Reserva {r.id} confirmada")
        self._seguro(accion)
    # Cancela la reserva seleccionada.    
    def _cancelar(self):
        # Define la operación de cancelación.
        def accion():
            r = self.sistema.cancelar_reserva(self._id_reserva())
            self._actualizar()
            messagebox.showinfo("Correcto", f"Reserva {r.id} cancelad.")
        self._seguro(accion)
    # Actualiza las tablas y listas desplegables con los datos del sistema.        
    def _actualizar(self):
        for tree in (self.tc, self.ts, self.tr):
            tree.delete(*tree.get_children())
        for c in self.sistema.clientes:
            self.tc.insert("", "end", values=(c.id, c.nombre, c.documento, c.correo, c.telefono))
        # Lista que almacenará las opciones de servicios para las reservas.
        choices = []
        for s in self.sistema.servicios:
            tipo = s.__class__.__name__
            extra = getattr(s, "capacidad", getattr(s, "unidades", getattr(s, "especialidad", "")))
            self.ts.insert("", "end", values=(s.id, tipo, s.nombre, f"${s.tarifa_hora:,.0f}", extra))
            choices.append(f"{s.id} | {s.nombre}")
        self.rs["values"] = choices
        for r in self.sistema.reservas:
            self.tr.insert("", "end", values=(r.id, r.cliente.nombre, r.servicio.nombre, r.duracion, f"${r.costo:,.2f}", r.estado.value))
    # Ejecuta las pruebas de funcionamiento del sistema.            
    def _pruebas(self):
        results = self.sistema.demostracion()
        self.out.delete("1.0", "end")
        self.out.insert("end", "\n".join(results))
        self._actualizar()
        messagebox.showinfo("Finalizo", f"Se ejecutaron {len(results)} operacones. Consulta el archivo de logs")
    # Abre una ventana adicional para consultar el archivo de registros.        
    def _logs(self):
        from pathlib import Path
        path = Path(__file__).resolve().parent.parent / "logs" / "software_fj.log"
        win = tk.Toplevel(self)
        win.title("Registro de eventos y errores")
        win.geometry("850x500")
        txt = tk.Text(win, wrap="word", font=("Consolas", 9))
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", path.read_text(encoding="utf-8") if path.exists() else "Aun no hay registro.")
        txt.configure(state="disabled")