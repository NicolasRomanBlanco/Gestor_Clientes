# Este fichero controlara los datos y proveera una interfaz para crear modificar y borrar informacion
import csv
import config


class Cliente:
    def __init__(self, dni, nombre, apellido):
        # con self = variables de la instancia
        # podemos crear varios clientes
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"


class Clientes:
    # variable de clase
    # solo una lista de clientes
    lista = []

    # Carga los clientes de la memoria
    with open(config.DATABASE_PATH, newline='\n') as fichero:
        reader = csv.reader(fichero, delimiter=';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    # como es un metodo estatico el sistema no pasara automaticamente la instancia
    # como primer parametro si no que no va a pasar nada
    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente

    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente

    @staticmethod
    def modificar(dni, nombre, apellido):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[indice].nombre = nombre
                Clientes.lista[indice].apellido = apellido
                Clientes.guardar()
                return cliente

    @staticmethod
    def borrar(dni):
        for indice, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(indice)
                Clientes.guardar()
                return cliente

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                # writerow toma una tupla, asi que hay que pasarlo entre parentesis para que lo tome como una
                writer.writerow(
                    (cliente.dni, cliente.nombre, cliente.apellido))
