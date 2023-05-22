# Contiene funciones auxiliares de uso general
import os
import platform
import re


def limpiar_pantalla():
    # operador ternario
    os.system('cls') if platform.system() == "Windows" else os.system('clear')


def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    # Ejecutar instruccion si se cumple una condicion, en caso contrario no hace nada
    print(mensaje) if mensaje else None

    while True:
        texto = input("> ")
        # validacion para que un texto tenga exactamente los caracteres que quieres
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto


def dni_valido(dni, lista):
    # Dos digitos y una letra mayuscula
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe cumplir el formato")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("DNI utilizado por otro cliente.")
            return False
    return True
