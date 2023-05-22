# Equivalente a menu.oy pero con interfaz grafica
import helpers
import database as db
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


# Mixin: Clase que contiene una o varias definiciones y que podemos heredarlas en otras clases
class CenterWidgetMixin:
    def center(self):
        self.update()

        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # Ancho de la pantalla entre 2 menos el ancho de la ventana entre 2
        x = int(ws/2 - w/2)

        # Altura de la pantalla entre 2 menos la altura de la ventana entre 2
        y = int(hs/2 - h/2)

        # self.geometry(WIDTHxHEIGHT+OFFSET_X+OFFSET_Y)
        self.geometry(f"{w}x{h}+{x}+{y}")

# Widget que maneja las subventanas(Toplevel)


class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.center()
        # Impiden que puedas realizar acciones hasta cerrar la subventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Frame superior
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        # Cajas de texto del frame superior
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        # Validacion dni en tiempo real
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        # Validacion nombre en tiempo real
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        # Validacion apellido en tiempo real
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        # Frame inferior
        frame = Frame(self)
        frame.pack(pady=10)

        # Boton crear y cancelar del frame inferior
        crear = Button(frame, text="Crear", command=self.create_client)
        crear.config(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [0, 0, 0]
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    # Funcion que inserta el cliente en el Treeview desde la subventana
    def create_client(self):
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        # Realizamos los cambios en el csv
        db.Clientes.crear(self.dni.get(), self.nombre.get(),
                          self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    # Funcion que valida el DNI, Nombre y Apellido en tiempo real y lo muestra mediante colores
    def validate(self, event, index):
        valor = event.widget.get()
        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure(
            {"bg": "MediumSpringGreen" if valido else "IndianRed"})

        # Cambiar el estado del boton en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1]
                          else DISABLED)


class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.center()
        # Impiden que puedas realizar acciones hasta cerrar la subventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Frame superior
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        # Cajas de texto del frame superior
        dni = Entry(frame)
        dni.grid(row=1, column=0)

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        # Validacion nombre en tiempo real
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        # Validacion apellido en tiempo real
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        # Recuperamos el cliente y campos seleccionado en el treeview y se insertan en la subventana
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        # Frame inferior
        frame = Frame(self)
        frame.pack(pady=10)

        # Boton crear y cancelar del frame inferior
        actualizar = Button(frame, text="Actualizar", command=self.edit_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [1, 1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    # Funcion que inserta el cliente en el Treeview desde la subventana
    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        # Realizamos los cambios en el csv
        db.Clientes.modificar(
            self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    # Funcion que valida el DNI, Nombre y Apellido en tiempo real y lo muestra mediante colores
    def validate(self, event, index):
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure(
            {"bg": "MediumSpringGreen" if valido else "IndianRed"})

        # Cambiar el estado del boton en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1]
                               else DISABLED)


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        # Hereda los metodos del constructor
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.center()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        # '#0' es la primera columna que crea por defecto (no nos interesa)
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        scrollbar = Scrollbar(frame)
        # "fill=Y rellena la barra  verticalmente"
        scrollbar.pack(side=RIGHT, fill=Y)
        # Establece el comando al que tiene la barra de scroll
        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido))

        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text="Crear", command=self.create).grid(row=0, column=0)
        Button(frame, text="Modificar", command=self.edit).grid(row=0, column=1)
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2)

        # Exportamos como un atributo de instancia para tener acceso a este widget desde los demas metodos
        self.treeview = treeview

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            # Almacena en "campos" los valores del registro cliente seleccionado
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title=" Confirmar borrado",
                message=f"Borrar {campos[1]} {campos[2]}?",
                icon=WARNING
            )
            if confirmar:
                self.treeview.delete(cliente)
                # Realizamos los cambios en el csv
                db.Clientes.borrar(campos[0])

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
