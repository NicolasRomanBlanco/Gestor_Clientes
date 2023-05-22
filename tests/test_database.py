import helpers
import config
import csv
import copy
import unittest
import database as db


class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            # Mockup objects (objetos de pruebas)
            db.Cliente('15J', 'Marta', 'Perez'),
            db.Cliente('46H', 'Manolo', 'Lopez'),
            db.Cliente('23M', 'Ana', 'Garcia'),
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15J')
        cliente_inexistente = db.Clientes.buscar('25X')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('99C', 'Nico', 'Roman')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '99C')
        self.assertEqual(nuevo_cliente.nombre, 'Nico')
        self.assertEqual(nuevo_cliente.apellido, 'Roman')

    def test_modificar_cliente(self):
        # Creamos una copia de un cliente
        cliente_a_modificar = copy.copy(db.Clientes.buscar('46H'))
        cliente_modificado = db.Clientes.modificar('46H', 'Paco', 'Lopez')
        self.assertEqual(cliente_a_modificar.nombre, 'Manolo')
        self.assertEqual(cliente_modificado.nombre, 'Paco')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('23M')
        cliente_rebuscado = db.Clientes.buscar('23M')
        self.assertEqual(cliente_borrado.dni, '23M')
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido("00A", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("324314A", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("F35", db.Clientes.lista))
        self.assertFalse(helpers.dni_valido("15J", db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('46H')
        db.Clientes.borrar('15J')
        db.Clientes.modificar('23M', 'Mariana', 'Garcia')

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero, delimiter=';')
            # Carga el primer cliente del fichero
            dni, nombre, apellido = next(reader)

        self.assertEqual(dni, '23M')
        self.assertEqual(nombre, 'Mariana')
        self.assertEqual(apellido, 'Garcia')
