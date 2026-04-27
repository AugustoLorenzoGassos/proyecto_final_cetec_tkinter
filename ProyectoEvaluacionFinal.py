# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:06:06 2026

@author: Augusto Lorenzo Gassós

"""

import os

def registrar_membresia():
    registro_correcto = False
    while True:
        os.system("cls")
        print("Sistema de reservas para un gimnasio".center(100))
        print("Registro de usuarios".center(100))
        print("\n")
        nombre_usuario = input("Escribe el nombre del usuario: ")
        if len(nombre_usuario)>0:
            print("Tipos de membresia\n")
            print(f"{'Tipo':<40}{'Costo':^10}")
            print(f"{'1. Básica':<40}{'$300.00':^10}")
            print(f"{'2. Premium':<40}{'$500.00':^10}")
            print(f"{'3. VIP':<40}{'$800.00':^10}")
            print("\n")
            try:
                tipo_membresia = int(input("Escribe el número de la membesía a asignar: "))
            except ValueError:
                tipo_membresia = 0
            match tipo_membresia:
                case 1:
                    lista_usuarios.append(nombre_usuario)
                    lista_membresias.append("Básica")
                    lista_costos.append(300.00)
                    registro_correcto = True
                case 2:
                    registro_correcto = True
                    lista_usuarios.append(nombre_usuario)
                    lista_membresias.append("Premium")
                    lista_costos.append(500.00)
                    registro_correcto = True
                case 3:
                    registro_correcto = True
                    lista_usuarios.append(nombre_usuario)
                    lista_membresias.append("VIP")
                    lista_costos.append(800.00)
                    registro_correcto = True
                case _:
                    print("Error: membresía incorrecta")
                    registro_correcto = False
        else:
            print("Error: nombre del usuario incorrecto")
            registro_correcto = False
        """Valida que se haya registrado correectamente al usuario"""
        if registro_correcto == False:
            continuar_registro = input("Deseas intentar nuevamente el registro (S/N): " )
            if continuar_registro.lower()!="s":
                break
        else:
            break   
def ver_membresias(lista):
    os.system("cls")
    print("Sistema de reservas para un gimnasio".center(100))
    print("Registro de usuarios".center(100))
    print("\n")
    print(f"Total de reservas registradas {len(lista_usuarios)}")
    print(f"Total de dinero recaudado: {sumar_membresias(lista_costos):.2f}")
    print("\n")
    consulta_membresias(lista_usuarios,lista_membresias,lista_costos)
    
def sumar_membresias(lista):
    total = 0
    for item_membresia in lista:
        total += item_membresia
    return total

def consulta_membresias(lista1, lista2, lista3):
    print("lista de membresias".center(100))
    print(f"{'Usiario':^40}{'Membresia':^10}{'Costo':^10}")
    for a,i in enumerate(lista1):
        print(f"{i:<40}{lista2[a]:^10}{lista3[a]:^10}")
    input("\nPresione cualquier tecla para continuar...")
    
leer_opcion = 0
nombre_usuario=""
tipo_membresia = 0
nombre_membresia = ""
costo_membresia = 0

lista_usuarios = []
lista_membresias = []
lista_costos = []

while True:
    os.system("cls")
    print("Sistema de reservas para un gimnasio".center(100))
    print("Página pincipal".center(100))
    print("\n")
    print("Menú principal\n")
    print("1. Registrar nueva reserva\n2. Ver resumen de reservas\n3. Salir\n")
    try:
        leer_opcion = int(input("Escribe el número de la opción deseada: "))
    except ValueError:
        print("La opción debe de ser jun númer entre 1 y 3")
        leer_opcion = 0
    match leer_opcion:
        case 1:
            registrar_membresia()
        case 2:
            ver_membresias(lista_usuarios)
        case 3:
            break
        case _:
            print("Opción invalida")
            
    

