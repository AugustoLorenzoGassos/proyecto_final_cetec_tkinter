# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 19:14:11 2026

@author: Augusto Lorenzo Gassós

"""

import tkinter as Tk
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox as msgbox
import datetime as dt
import Datos
import os

Usuarios, Clientes, Lotes, LotesDetalles, Inventario, ClientesMovimientos = Datos.RecuperarDatos()

lista_usuarios = Usuarios["Usuarios"]
lista_clientes = Clientes["Clientes"]
lista_lotes = Lotes["Lotes"]
lista_lotes_detalles = LotesDetalles["Detalle"]
lista_inventario = Inventario["Inventario"]
lista_clientes_movimientos = ClientesMovimientos['DetalleMovimientos']

def IniciarSesion():

    """
        Proceso que valida el usuario un contraseña en el archovo ListaUsuarios.json
        Utiliza la función ValidarUsuario para determinar si exixte el usuario y su status actual
    """
    
    Encontrado = False
    NombreCompletoUsuario = ""
    TipoUsuario = ""
    StatusUsuario = ""
    
    NombreCompletoUsuario, Encontrado, TipoUsuario, StatusUsuario = ValidarUsuario(TextoUsuario.get(), TextoContraseña.get())
    
    if Encontrado == True:
        if StatusUsuario == "A":
            Procesos(NombreCompletoUsuario,StatusUsuario)
        else:
            LblResultado["text"]="Usuario inactivo"
    else:
        LblResultado["text"]="Usuario no encontrado."

def ValidarUsuario(PUsuario, PContraseña):
    
    #Validar cedenciales del usuario para inicar sesión
    
    UsuarioRegistrado = False
    for item_usuario in lista_usuarios:
        if item_usuario["Nombre"] == PUsuario and item_usuario["Contraseña"] == PContraseña:
            UsuarioRegistrado = True
            break
    return(item_usuario["NombreCompleto"], UsuarioRegistrado, item_usuario["TipoUsuario"], item_usuario["Status"])

def Procesos(parametro_nombre_Usuario, parametro_status_usuario):

    def limpiar():
        """
        Limpia los frame para presentar los treeview que correspondan a la información solicitada desd el menu
        También limia el frame que se uitiliza para colocar los botones de acciones para cada treeview
        """
        
        for widget in frame_datos.winfo_children():
            widget.destroy()
        for widget in frame_botones.winfo_children():
            widget.destroy()
        
    #inicio de funckiones para las opciones del menu
    def ListaClientes():
        """
        Contiene las funciones que se aplican a la tabla de clientes
        """
        def ValidarCliente(CCliente):
            """
            Valida la infolrmación del cliente seleccionado en el treeview
            Recibe como parámetro la clave del cliente para buscar el registro en el archivo ListaClientes.json
            Regresa los datos del cliente en un diccionario
            """
            ClienteEncontado = False
            for item_clientes in lista_clientes:
                if item_clientes["Nombre"] == CCliente:
                    ClienteEncontado = True
                    break
            return item_clientes, ClienteEncontado

        def agregar_cliente():
            """
            agregar_cliente() inserta un cliente en el archivo ListaClientes.json
                Tiene dos funciones al interior:
                    insertar_datos_cliente() que validca la ionformación, guarda los datos y presenta nuevamentye el treeviw
                    cancelar_datos_cliente: destruye la ventana sin guardar la informciónm
            """
            def insertar_datos_cliente():
                if usuario_cliente.get()=="" or nombre_cliente.get()=="":
                    msgbox.showinfo(title="Alta de clientes",message="Los datos no se pueden quedar vacíos")
                else:
                    nuevo_cliente = {"Nombre":usuario_cliente.get(),"NombreCompleto":nombre_cliente.get(), "Status":"A"}
                    lista_clientes.append(nuevo_cliente)
                    Datos.GuardarClientes(Clientes)
                    ListaClientes()
                    """Agregar el registro el el archivo de los movimientos para el cliente"""
                    nuevo_cliente_movimientos = {'Cliente':usuario_cliente.get(),'Movimientos':[]}
                    lista_clientes_movimientos.append(nuevo_cliente_movimientos)
                    Datos.GuardarClientesMovimientos(ClientesMovimientos)
                    msgbox.showinfo(title="Alta de clientes",message="Los datos del cliente fueron almacenados correctamente.")
                    ventana_cliente.destroy()
            def cancelar_datos_cliente():
                ventana_cliente.destroy()
            """
            Inicio del proceso de lectura de datos para insertar ujn cliente
            """
            """Construye la ventana secundaria para el alta de un clinete"""
            ventana_cliente = Tk.Toplevel(PaginaPrincipal)
            ventana_cliente.title("Insertar cliente")
            ventana_cliente.geometry("300x300")
            ventana_cliente.update()
            etiquete_alta_cliente = Tk.Label(ventana_cliente, text="Alta de clientes", padx=20, pady=20)
            etiquete_alta_cliente.pack()
            """Construye el frame para los datos, coloca las etiquetas y los entry"""            
            frame_datos_cliente = ttk.Frame(ventana_cliente)
            frame_datos_cliente.pack()
            etiqueta_usuario_cliente = ttk.Label(frame_datos_cliente, text="Usuario: ")
            etiqueta_nombre_cliente = ttk.Label(frame_datos_cliente, text="Nombre del cliente: ")
            usuario_cliente = ttk.Entry(frame_datos_cliente)
            nombre_cliente = ttk.Entry(frame_datos_cliente)
            etiqueta_usuario_cliente.grid(column=0, row=0)
            usuario_cliente.grid(column=1, row=0)
            etiqueta_nombre_cliente.grid(column=0, row=1)
            nombre_cliente.grid(column=1, row=1)
            """Construye el frame para los botones y coloca los botones"""
            frame_botones_cliente = ttk.Frame(ventana_cliente)
            frame_botones_cliente.pack()
            boton_alta_clientes_aceptar = ttk.Button(frame_botones_cliente, text="Aceptar", command=insertar_datos_cliente)
            boton_alta_clientes_cancelar = ttk.Button(frame_botones_cliente, text="Cancelar", command=cancelar_datos_cliente)
            boton_alta_clientes_aceptar.grid(column=0, row=4)
            boton_alta_clientes_cancelar.grid(column=1, row=4)
            """
            Fin del proceso para insertar un cliente
            """
        def editar_cliente():
            """
            Funciones para editar los datos del cliente seleccionadl del treeview
            """
            def editar_datos_cliente():
                if usuario_cliente.get()=="" or nombre_cliente.get()=="":
                    msgbox.showinfo(title="Editar clientes",message="Los datos no se pueden quedar vacíos")
                else:
                    datos_cliente["Nombre"] = usuario_cliente.get()
                    datos_cliente["NombreCompleto"] = nombre_cliente.get()
                    Datos.GuardarClientes(Clientes)
                    ListaClientes()
                    msgbox.showinfo(title="Alta de clientes",message="Los datos del cliente fueron almacenados correctamente.")
                    ventana_cliente.destroy()
            def cancelar_datos_cliente():
                ventana_cliente.destroy()
            
            curItem = TablaClientes.focus()
            item_cliente_seleccionado = TablaClientes.item(curItem)
            
            if len(item_cliente_seleccionado['values'])>0:
                
                datos_cliente, CEncontrado = ValidarCliente(item_cliente_seleccionado['values'][0])
                
                ventana_cliente = Tk.Toplevel(PaginaPrincipal)
                ventana_cliente.title("Editar cliente")
                ventana_cliente.geometry("300x300")
                ventana_cliente.update()
                """
                Pasa los datos del cliente seleccinado a la ventana emergente
                """
                etiquete_alta_cliente = Tk.Label(ventana_cliente, text="Editar clientes", padx=20, pady=20)
                etiquete_alta_cliente.pack()
            
                frame_datos_cliente = ttk.Frame(ventana_cliente)
                frame_datos_cliente.pack()
                
                textEntryUsuario = Tk.StringVar()
                textEntryUsuario.set(datos_cliente["Nombre"])
                
                textEntryNombre = Tk.StringVar()
                textEntryNombre.set(datos_cliente["NombreCompleto"])
                
                etiqueta_usuario_cliente = ttk.Label(frame_datos_cliente, text="Usuario: ")
                etiqueta_nombre_cliente = ttk.Label(frame_datos_cliente, text="Nombre del cliente: ")
                usuario_cliente = Tk.Entry(frame_datos_cliente, textvariable=textEntryUsuario)
                nombre_cliente = Tk.Entry(frame_datos_cliente, textvariable=textEntryNombre)
                
                etiqueta_usuario_cliente.grid(column=0, row=0)
                usuario_cliente.grid(column=1, row=0)
                etiqueta_nombre_cliente.grid(column=0, row=1)
                nombre_cliente.grid(column=1, row=1)
                
                frame_botones_cliente = ttk.Frame(ventana_cliente)
                frame_botones_cliente.pack()
                boton_alta_clientes_aceptar = ttk.Button(frame_botones_cliente, text="Aceptar", command=editar_datos_cliente)
                boton_alta_clientes_cancelar = ttk.Button(frame_botones_cliente, text="Cancelar", command=cancelar_datos_cliente)
                boton_alta_clientes_aceptar.grid(column=0, row=4)
                boton_alta_clientes_cancelar.grid(column=1, row=4)

            
        def inhabilitar_cliente():
            """
            Función para cambiar el estatus del cliente entre inhabiliytado o havilitado
            """
            curItem = TablaClientes.focus()
            item_cliente_seleccionado = TablaClientes.item(curItem)
            if len(item_cliente_seleccionado['values'])>0:
                datos_cliente, CEncontrado = ValidarCliente(item_cliente_seleccionado['values'][0])
                cambiar_status_cliente = msgbox.askyesno(title="Alta de clientes", message="¿Esta seguro sde cam biar el status al cliente")
                if cambiar_status_cliente == True:
                    if datos_cliente["Status"] == "A":
                        datos_cliente["Status"] = "I"
                    else:
                        datos_cliente["Status"] = "A"
                    Datos.GuardarClientes(Clientes)
                    ListaClientes()
            else:
                msgbox.showerror(title="Alta de cliente", message="No se ha seleccionado un cliente de la lista")

        def abono_cliente():
            """Función para registrar el abono de un cliente"""
            
            def insertar_abono():
                """Validación de datos de entrada"""
                error_abono = False
                try:
                    dt.datetime.strptime(fecha_abono.get(), "%d/%m/%Y").date()
                except ValueError:
                    msgbox.showerror(title="Registro de ventas",message="Formato de fecha incorrecto.")
                    error_abono = True
                try:
                    float(importe_abono.get())
                except ValueError:
                    msgbox.showerror(title="Registro de ventas",message="Importe de compra con formato incorrecto.")
                    error_abono = True
                if error_abono == False:
                    nuevo_abono = {'TipoMovimiento':'A','FechaMovimiento':str(dt.datetime.today()),'FechaCompra':fecha_abono.get(),'ImporteMovimiento':float(importe_abono.get()),'CantidadPerfumes':0,'PerfumeCompra':'','PerfumeCompraPresentacion':'','PerfumeCompraImporte':0.0}
                    item_cliente_movimientos.append(nuevo_abono)
                    Datos.GuardarClientesMovimientos(ClientesMovimientos)
                    msgbox.showinfo("Regisgtro de abono", message="El abono se registro correctamente.")
                else:
                    msgbox.showerror("Registro de abono", message="No se pudo registrar el abono")
                
            def cancelar_abono():
                ventana_abono_cliente.destroy()
                
            curItem = TablaClientes.focus()
            item_cliente_seleccionado = TablaClientes.item(curItem)
            if len(item_cliente_seleccionado['values'])>0:
                """Obtiene la lista de los movimientos del cliente"""
                for item_cliente in lista_clientes_movimientos:
                    if item_cliente['Cliente']==item_cliente_seleccionado['values'][0]:
                        item_cliente_movimientos = item_cliente['Movimientos']
                        break
                """Si tiene movimientos se calcula el saldo y se presenta la información del cliente"""
                if len(item_cliente_movimientos)>0:
                    """Calcular saldo actual"""
                    saldo_actual=0.0
                    for item_calcular_saldo in item_cliente_movimientos:
                        if item_calcular_saldo['TipoMovimiento'] == "C":
                            saldo_actual += float(item_calcular_saldo['ImporteMovimiento'])
                        else:
                            saldo_actual -= float(item_calcular_saldo['ImporteMovimiento'])
                    """Generación de ventana y pesentación de información"""
                    ventana_abono_cliente = Tk.Toplevel(PaginaPrincipal)
                    ventana_abono_cliente.title("Registrar abono")
                    ventana_abono_cliente.geometry("300x300")
                    ventana_abono_cliente.update()
                    """
                    Pasa los datos del cliente seleccinado a la ventana emergente
                    """
                    etiqueta_abono_cliente = Tk.Label(ventana_abono_cliente, text=f"Cliente: {item_cliente_seleccionado['values'][0]} - {item_cliente_seleccionado['values'][1]}", padx=20, pady=20)
                    etiqueta_abono_saldo = Tk.Label(ventana_abono_cliente, text=f"Saldo actual: {saldo_actual:.2f}", padx=20, pady=20)
                    """Campos para el regitro del movimiento"""
                    etiqueta_importe_abono = Tk.Label(ventana_abono_cliente,text="Importe del abono: ")
                    importe_abono = Tk.Entry(ventana_abono_cliente)
                    etiqueta_fecha_abono = Tk.Label(ventana_abono_cliente, text="Fecha del abono: ")
                    fecha_abono = Tk.Entry(ventana_abono_cliente)
                    etiqueta_abono_cliente.pack()
                    etiqueta_abono_saldo.pack()
                    etiqueta_importe_abono.pack()
                    importe_abono.pack()
                    etiqueta_fecha_abono.pack()
                    fecha_abono.pack()
                    """Frame para los botones en el registro de un abobo"""
                    frame_botones_abono = ttk.Frame(ventana_abono_cliente)
                    frame_botones_abono.pack()
                    boton_alta_perfume_aceptar = ttk.Button(frame_botones_abono, text="Aceptar", command=insertar_abono)
                    boton_alta_perfume_cancelar = ttk.Button(frame_botones_abono, text="Cancelar", command=cancelar_abono)
                    boton_alta_perfume_aceptar.grid(column=0, row=4)
                    boton_alta_perfume_cancelar.grid(column=1, row=4)
                else:
                    msgbox.showinfo("Registro de abono", message="El cliente no tiene movimientos registrados")

                ListaClientes()
            else:
                msgbox.showerror(title="Registrar abono", message="No se ha seleccionado un cliente de la lista")

        def movimientos_cliente():
            """Función para mostrar los movimientos y descargar el estado de cuenta"""
            curItem = TablaClientes.focus()
            item_cliente_seleccionado = TablaClientes.item(curItem)
            if len(item_cliente_seleccionado['values'])>0:
                """Generación de ventana y pesentación de información"""
                ventana_reporte_cliente = Tk.Toplevel(PaginaPrincipal)
                ventana_reporte_cliente.title("Registrar abono")
                ventana_reporte_cliente.geometry("900x400")
                ventana_reporte_cliente.update()
                etiqueta_inicio = Tk.Label(ventana_reporte_cliente,text=f"Resumen de movimientos\nCliente: {item_cliente_seleccionado['values'][0]} - {item_cliente_seleccionado['values'][1]}")
                etiqueta_inicio.pack(padx=10, pady=10)
                """Frame para presentar el estado de cuenta (Movimientos)"""
                frame_estado_cuenta = ttk.Frame(ventana_reporte_cliente)
                frame_estado_cuenta.pack()
                """Treeview para presentar los movimientos"""          
                TablaMovimientos = ttk.Treeview(frame_estado_cuenta, columns=("C1","C2","C3","C4"), show="headings")
                TablaMovimientos.heading("C1", text="Descripción")
                TablaMovimientos.heading("C2", text="Fecha del movimiento")
                TablaMovimientos.heading("C3", text="Importe (cargo)")
                TablaMovimientos.heading("C4", text="Importe (abono)")
                TablaMovimientos.column("C1", width=350)
                TablaMovimientos.column("C2", width=140)
                TablaMovimientos.column("C3", width=100)
                TablaMovimientos.column("C4", width=100)
                TablaMovimientos.pack(side="left", fill="both", expand=True)
                barra_vertical = ttk.Scrollbar(frame_estado_cuenta, orient="vertical", command=TablaMovimientos.yview)
                barra_vertical.pack(side="right", fill="y")
                """Cálculo de cargos, abonos y saldo actual"""                
                cliente_encontrado = False
                cliente_cargos = 0
                cliente_abonos = 0
                importe_cargo = 0 
                importe_abono = 0
                for item_cliente_movimientos in lista_clientes_movimientos:
                    if item_cliente_movimientos['Cliente'] == item_cliente_seleccionado['values'][0]:
                        item_movimientos_cliente = item_cliente_movimientos['Movimientos']
                        cliente_encontrado = True
                        break
                if cliente_encontrado == True:
                    for item_movimiento in item_movimientos_cliente:
                        descripcion_movimiento = ""
                        """Cálculo de salodos y tipo de movimiento"""
                        match item_movimiento['TipoMovimiento']:
                            case "A":
                                importe_cargo = 0
                                importe_abono = float(item_movimiento['ImporteMovimiento'])
                                descripcion_movimiento = "Abono"
                                cliente_abonos += float(item_movimiento['ImporteMovimiento'])
                            case "C":
                                importe_abono = 0
                                importe_cargo = float(item_movimiento['ImporteMovimiento'])
                                descripcion_movimiento = f"Cargo ({item_movimiento['PerfumeCompra']} - {item_movimiento['PerfumeCompraPresentacion']})"
                                cliente_cargos += float(item_movimiento['ImporteMovimiento'])
                        """Llenado del treeview"""
                        TablaMovimientos.insert("", "end", values=(
                            descripcion_movimiento,
                            item_movimiento['FechaCompra'],
                            importe_cargo,
                            importe_abono))
                        """Saldos"""
                etiqueta_resumen = Tk.Label(ventana_reporte_cliente,text="Resumen de movimientos", padx=10)
                etiqueta_resumen.pack()
                frame_saldos = Tk.Frame(ventana_reporte_cliente)
                frame_saldos.pack()
                etiqueta_cargos = Tk.Label(frame_saldos,text=f"Cargos: ${cliente_cargos:.2f}")
                etiqueta_abonos = Tk.Label(frame_saldos,text=f"Cargos: ${cliente_abonos:.2f}")
                etiqueta_saldo = Tk.Label(frame_saldos,text=f"Saldo: ${(cliente_cargos-cliente_abonos):.2f}")
                etiqueta_cargos.grid(row=2, column=0, padx=20)
                etiqueta_abonos.grid(row=2,column=1, padx=20)
                etiqueta_saldo.grid(row=2, column=3, padx=20)
                """Botón para descargar el estado de cuenta"""
                boton_descargar_estado_cuenta = Tk.Button(ventana_reporte_cliente,text="Descargar estado de cuenta", command=lambda m=item_cliente_seleccionado['values'][0]: movimientos_cliente_estado_cuenta(m))
                boton_descargar_estado_cuenta.pack(padx=20,pady=20)
            else:
                msgbox.showerror(title="Movimientos del cliente", message="No se ha seleccionado un cliente de la lista")
        
        def movimientos_cliente_estado_cuenta(m):
            for item_cliente_movimientos in lista_clientes_movimientos:
                if item_cliente_movimientos['Cliente'] == m:
                    item_movimientos_cliente = item_cliente_movimientos['Movimientos']
                    break
            with open(f"EstadoCuenta_{m}.txt","w") as fEstadoCuenta:
                print("Perfumes originales Lorenzo".center(100), file=fEstadoCuenta)
                print("-"*100, file=fEstadoCuenta)
                print(f"Id del cliente: {m}", file=fEstadoCuenta)
                for cliente in lista_clientes:
                    if cliente['Nombre'] == m:
                        print(f"Nombre del cliente: {cliente['NombreCompleto']}", file=fEstadoCuenta)
                print("-"*100, file=fEstadoCuenta)
                print("Movimientos".center(100), file=fEstadoCuenta)
                print("\n", file=fEstadoCuenta)
                print(f"{'Descripción':<60}{'Fecha':^10}{'Cargos':^15}{'Abonos':^15}", file=fEstadoCuenta)
                cliente_cargos = 0
                cliente_abonos = 0
                importe_cargo = 0 
                importe_abono = 0
                for movimiento in item_movimientos_cliente:
                    descripcion_movimiento = ""
                    """Cálculo de salodos y tipo de movimiento"""
                    match movimiento['TipoMovimiento']:
                        case "A":
                            importe_cargo = 0
                            importe_abono = float(movimiento['ImporteMovimiento'])
                            descripcion_movimiento = "Abono"
                            cliente_abonos += float(movimiento['ImporteMovimiento'])
                        case "C":
                            importe_abono = 0
                            importe_cargo = float(movimiento['ImporteMovimiento'])
                            descripcion_movimiento = f"Cargo ({movimiento['PerfumeCompra']} - {movimiento['PerfumeCompraPresentacion']})"
                            cliente_cargos += float(movimiento['ImporteMovimiento'])
                    print(f"{descripcion_movimiento:<60}{movimiento['FechaCompra']:^10}{importe_cargo:^15}{importe_abono:^15}", file=fEstadoCuenta)
                print("-"*100, file=fEstadoCuenta)
                print("\n", file=fEstadoCuenta)
                print("Resumen de movimientos", file=fEstadoCuenta)
                print(f"Cargos: ${cliente_cargos:.2f}", file=fEstadoCuenta)
                print(f"Abonos: ${cliente_abonos:.2f}", file=fEstadoCuenta)
                print(f"Saldo: ${(cliente_cargos-cliente_abonos):.2f}", file=fEstadoCuenta)
                Ruta = os.path.join(os.getcwd(), f"EstadoCuenta_{m}.txt")
                msgbox.showinfo(title="Movimientos del cliente", message=f"El archivo con el estado de cuenta fue generado correctamente.\n\nUbicación:{Ruta}")
        limpiar()
        
        """
        Llenar los datos del triview con la información de los clientes
        """
        TablaClientes = ttk.Treeview(frame_datos, columns=("C1","C2","C3"), show="headings")
        TablaClientes.heading("C1", text="Usuario")
        TablaClientes.heading("C2", text="Nombre")
        TablaClientes.heading("C3", text="Status")
        TablaClientes.column("C1", width=100)
        TablaClientes.column("C2", width=700)
        TablaClientes.column("C3", width=100, anchor='center')
        
        for item_cliente in lista_clientes:
            if item_cliente['Status'].lower() == "a":
                descripcion_status = "Habilitado"
            else:
                descripcion_status = "Inhabilitado"
            TablaClientes.insert("", "end", values=(item_cliente['Nombre'],item_cliente['NombreCompleto'],descripcion_status))
        TablaClientes.pack(side="left", fill="both", expand=True)
        barra_vertical = ttk.Scrollbar(frame_datos, orient="vertical", command=TablaClientes.yview)
        barra_vertical.pack(side="right", fill="y")

        """botones para las acciones de los clientes"""
        boton_agregar_cliente = Tk.Button(frame_botones, text="Agregar", command=agregar_cliente)
        boton_editar_cliente = Tk.Button(frame_botones, text="Editar", command=editar_cliente)
        boton_inhabilitar_cliente = Tk.Button(frame_botones, text="Inhabilitar", command=inhabilitar_cliente)
        boton_abono_cliente = Tk.Button(frame_botones, text="Registrar abono", command=abono_cliente)
        boton_movimientos_cliente = Tk.Button(frame_botones, text="Estado de cuenta", command=movimientos_cliente)
        boton_agregar_cliente.grid(column=0, row=0, padx=10, pady=10)
        boton_editar_cliente.grid(column=1, row=0, padx=10, pady=10)
        boton_inhabilitar_cliente.grid(column=2, row=0, padx=10, pady=10)
        boton_abono_cliente.grid(column=3, row=0, padx=10, pady=10)
        boton_movimientos_cliente.grid(column=4, row=0, padx=10, pady=10)

    def ListaLotesPerfumes():
        """        
        Funciones que permiten insertar y actualizar los datos de los lotes de perfumes

        """
        def ValidarLote(CLote):
            """
            Función que valida la existencia de un lote y regresa los datos del mismo en un diccinario
            """
            LoteEncontado = False
    
            for item_lote in lista_lotes:
                if item_lote["id_lote"] == str(CLote):
                    LoteEncontado = True
                    break
    
            return item_lote, LoteEncontado
        
        def alta_lote_perfumes():
            
            def insertar_datos_lote():
                """"
                Proceso que valida la entrada de datos, guarda el registro en el archivo ListaLotes.json
                """
                error_lote = False
                
                if id_lote.get()=="" or fecha_lote.get()=="" or cantidad_lote.get()=="" or importe_lote.get()=="":
                    msgbox.showinfo(title="Alta de lote de perfumes",message="Los datos no se pueden quedar vacíos")
                else:
                    try:
                        dt.datetime.strptime(fecha_lote.get(), "%d/%m/%Y").date()
                    except ValueError:
                        msgbox.showerror(title="Alta de lote de perfumes",message="Formato de fecha incorrecto.")
                        error_lote = True
                    try:
                        float(importe_lote.get())
                    except ValueError:
                        msgbox.showerror(title="Alta de lote de perfumes",message="La cantidad de perfumes y el importe del lote deben de ser números.")
                        error_lote = True
                    if not cantidad_lote.get().isnumeric():
                        msgbox.showerror(title="Alta de lote de perfumes",message="La cantidad de perfumes y el importe del lote deben de ser números.")
                        error_lote = True
                        
                    if error_lote == False:
                        nuevo_lote = {"id_lote":id_lote.get(),"fecha_compra":fecha_lote.get(), "cantidad_perfumes":cantidad_lote.get(), "importe_compra":importe_lote.get()}
                        nuevo_lote_perfumes = {"IdLotes":id_lote.get(),"Perfumes":[]}
                        lista_lotes.append(nuevo_lote)
                        lista_lotes_detalles.append(nuevo_lote_perfumes)
                        Datos.GuardarLotes(Lotes)
                        Datos.GuardarLotePerfume(LotesDetalles)
                        ListaLotesPerfumes()
                        msgbox.showinfo(title="Alta de lote de perfumes",message="Los datos del lote de perfumes fueron almacenados correctamente.")
                        ventana_lote_perfumes.destroy()
                    
            def cancelar_datos_lote():
                """"
                Proceso que cancela el proceso de alta de un lote
                """
                ventana_lote_perfumes.destroy()
            
            """
            Crea la ventana donde se presentan los campos para la insertar un lote
            """
            ventana_lote_perfumes = Tk.Toplevel(PaginaPrincipal)
            ventana_lote_perfumes.title("Insertar lote de perfumes")
            ventana_lote_perfumes.geometry("400x200")
            ventana_lote_perfumes.update()
            
            etiquete_alta_lote = Tk.Label(ventana_lote_perfumes, text="Alta de lote de perfumes", padx=20, pady=20)
            etiquete_alta_lote.pack()
            
            frame_datos_lote = ttk.Frame(ventana_lote_perfumes)
            frame_datos_lote.pack()
            
            etiqueta_id_lote = ttk.Label(frame_datos_lote, text="Id del lote: ")
            etiqueta_fecha_lote = ttk.Label(frame_datos_lote, text="Fecha de compra: ")
            etiqueta_cantidad_lote = ttk.Label(frame_datos_lote, text="Cantidad de perfumes en el lote: ")
            etiqueta_importe_lote = ttk.Label(frame_datos_lote, text="Omporte total del lote: ")
            
            id_lote = ttk.Entry(frame_datos_lote)
            fecha_lote = ttk.Entry(frame_datos_lote)
            cantidad_lote = ttk.Entry(frame_datos_lote)
            importe_lote = ttk.Entry(frame_datos_lote)
            
            etiqueta_id_lote.grid(row=0, column=0)
            id_lote.grid(row=0, column=1)
            etiqueta_fecha_lote.grid(row=1, column=0)
            fecha_lote.grid(row=1, column=1)
            etiqueta_cantidad_lote.grid(row=2, column=0)
            cantidad_lote.grid(row=2, column=1)
            etiqueta_importe_lote.grid(row=3, column=0)
            importe_lote.grid(row=3, column=1)
            
            """Acckones para guardar el lote o cancelar el alta"""
            frame_botones_lote = ttk.Frame(ventana_lote_perfumes)
            frame_botones_lote.pack()
            boton_alta_lote_aceptar = ttk.Button(frame_botones_lote, text="Aceptar", command=insertar_datos_lote)
            boton_alta_lote_cancelar = ttk.Button(frame_botones_lote, text="Cancelar", command=cancelar_datos_lote)
            boton_alta_lote_aceptar.grid(column=0, row=4)
            boton_alta_lote_cancelar.grid(column=1, row=4)
        
        
        def editar_lote_perfumes():
            """Procesos para realizar la actualización d la kinformackión del lote seleccionado en el treevie"""
            def editar_datos_lote():
                """Función para guardar los datos actjualizados del lote seleccionado en el treevie en el archivo Lista_lotes.json"""
                error_lote = False
                
                if id_lote.get()=="" or fecha_lote.get()=="" or cantidad_lote.get()=="" or importe_lote.get()=="":
                    msgbox.showinfo(title="Alta de lote de perfumes",message="Los datos no se pueden quedar vacíos")
                else:
                    try:
                        dt.datetime.strptime(fecha_lote.get(), "%d/%m/%Y").date()
                    except ValueError:
                        msgbox.showinfo(title="Alta de lote de perfumes",message="Formato de fecha incorrecto.")
                        error_lote = True
                    try:
                        float(importe_lote.get())
                    except ValueError:
                        msgbox.showinfo(title="Alta de lote de perfumes",message="La cantidad de perfumes y el importe del lote deben de ser números.")
                        error_lote = True
                    if not cantidad_lote.get().isnumeric():
                        msgbox.showinfo(title="Alta de lote de perfumes",message="La cantidad de perfumes y el importe del lote deben de ser números.")
                        error_lote = True
                    if error_lote == False:
                        datos_lote["id_lote"] = id_lote.get()
                        datos_lote["fecha_compra"] = fecha_lote.get()
                        datos_lote["cantidad_perfumes"] = cantidad_lote.get()
                        datos_lote["importe_compra"] = importe_lote.get()
                        Datos.GuardarLotes(Lotes)
                        ListaLotesPerfumes()
                        msgbox.showinfo(title="Alta de lote de perfumes",message="Los datos del lote fueron almacenados correctamente.")
                        ventana_lote_perfumes.destroy()
                    
            def cancelar_datos_lote():
                ventana_lote_perfumes.destroy()
            
            """Obtiene el item seleccionado en el treeview"""
            curItem = TablaLotePerfumes.focus()
            item_lote_seleccionado = TablaLotePerfumes.item(curItem)
       
            if len(item_lote_seleccionado['values'])>0:
                
                """Regresa los datos del registro seleccionado"""
                datos_lote, CEncontrado = ValidarLote(item_lote_seleccionado['values'][0])
                
                """Crea la ven tana y presenta los datos para su edición"""
                ventana_lote_perfumes = Tk.Toplevel(PaginaPrincipal)
                ventana_lote_perfumes.title("Insertar lote de perfumes")
                ventana_lote_perfumes.geometry("400x200")
                ventana_lote_perfumes.update()
                
                etiquete_alta_lote = Tk.Label(ventana_lote_perfumes, text="Alta de lote de perfumes", padx=20, pady=20)
                etiquete_alta_lote.pack()
                
                frame_datos_lote = ttk.Frame(ventana_lote_perfumes)
                frame_datos_lote.pack()
    
                textEntryIdLote = Tk.StringVar()
                textEntryfecha_compra = Tk.StringVar()
                textEntrycantidad_perfumes = Tk.StringVar()
                textEntryimporte_compra = Tk.StringVar()
                
                textEntryIdLote.set(datos_lote["id_lote"])
                textEntryfecha_compra.set(datos_lote["fecha_compra"])
                textEntrycantidad_perfumes.set(datos_lote["cantidad_perfumes"])
                textEntryimporte_compra.set(datos_lote["importe_compra"])
                
                etiqueta_id_lote = ttk.Label(frame_datos_lote, text="Id del lote: ")
                etiqueta_fecha_lote = ttk.Label(frame_datos_lote, text="Fecha de compra: ")
                etiqueta_cantidad_lote = ttk.Label(frame_datos_lote, text="Cantidad de perfumes en el lote: ")
                etiqueta_importe_lote = ttk.Label(frame_datos_lote, text="Omporte total del lote: ")
                
                id_lote = Tk.Entry(frame_datos_lote, textvariable=textEntryIdLote)
                fecha_lote = Tk.Entry(frame_datos_lote, textvariable=textEntryfecha_compra)
                cantidad_lote = Tk.Entry(frame_datos_lote, textvariable=textEntrycantidad_perfumes)
                importe_lote = Tk.Entry(frame_datos_lote, textvariable=textEntryimporte_compra)
                
                etiqueta_id_lote.grid(row=0, column=0)
                id_lote.grid(row=0, column=1)
                etiqueta_fecha_lote.grid(row=1, column=0)
                fecha_lote.grid(row=1, column=1)
                etiqueta_cantidad_lote.grid(row=2, column=0)
                cantidad_lote.grid(row=2, column=1)
                etiqueta_importe_lote.grid(row=3, column=0)
                importe_lote.grid(row=3, column=1)
                
                """Botones con las acciones para guardar o cancelar la actualización"""
                frame_botones_lote = ttk.Frame(ventana_lote_perfumes)
                frame_botones_lote.pack()
                boton_alta_lote_aceptar = ttk.Button(frame_botones_lote, text="Aceptar", command=editar_datos_lote)
                boton_alta_lote_cancelar = ttk.Button(frame_botones_lote, text="Cancelar", command=cancelar_datos_lote)
                boton_alta_lote_aceptar.grid(column=0, row=4)
                boton_alta_lote_cancelar.grid(column=1, row=4)
            else:
                msgbox.showerror(title="Alta de lote de perfumes", message="No se ha seleccionado un lote de la lista")        
         
                
        def ver_detalles_lote():
            """Funciones con la información contenida en eun lote"""
            def ValidarLoteDetalle(CLote):
                """Función que valida la existencia de ub lote y regresa los perfumes contenidos en ese lote"""
                LoteEncontado = False
                lista_perfumes_lote=[]
                
                for item_lote_detalles in lista_lotes_detalles:
                    if item_lote_detalles["IdLotes"] == str(CLote):
                        lista_perfumes_lote = item_lote_detalles["Perfumes"]
                        LoteEncontado = True
                        break
    
                return lista_perfumes_lote, CLote, LoteEncontado
            
            def alta_perfume_dentro_lote():
                """Funciones que agregan un perfune al interior de in lote en el archivo ListaLotesDetalles.json"""    
                def insertar_perfume():
                    error_perfume = False
                    nuevo_perfume={'IdPerfume':IdPerfume.get(),'NombrePerfume':NombrePerfume.get(),'MarcaPerfume':MarcaPerfume.get(),'PresentacionPerfume':PresentacionPerfume.get(),'ImporteCompra':ImporteCompra.get(),'CantidadCompra':CantidadCompra.get(),'CantidadDisponible':CantidadCompra.get()}
                    """Validación de información"""
                    if IdPerfume.get()=="" or NombrePerfume.get()=="" or MarcaPerfume.get()=="" or PresentacionPerfume.get()=="" or ImporteCompra.get()== "" or  CantidadCompra.get() == "":
                        msgbox.showinfo(title="Alta de perfumes",message="Los campos no pueden estar vacíos.")
                        error_perfume = True
                    if not CantidadCompra.get().isnumeric():
                        msgbox.showinfo(title="Alta de perfumes",message="La cantidad comprada debe ser un número")
                        error_perfume = True
                    try:
                        float(ImporteCompra.get())
                    except:
                        msgbox.showinfo(title="Alta de perfumes",message="El importe de compra debe ser un número")
                        error_perfume = True
                    if error_perfume == False:
                        """Guardar inflormación y actualizar el treeview de perfumes"""
                        datos_lote_detalle.append(nuevo_perfume)
                        Datos.GuardarLotePerfume(LotesDetalles)
                        for item in TablaLoteDetalles.get_children():
                            TablaLoteDetalles.delete(item)
                        for item_lote_detalle in datos_lote_detalle:
                            TablaLoteDetalles.insert("", "end", values=(item_lote_detalle['IdPerfume'],item_lote_detalle['NombrePerfume'],item_lote_detalle['MarcaPerfume'],item_lote_detalle['PresentacionPerfume'],item_lote_detalle['ImporteCompra'],item_lote_detalle['CantidadCompra'],item_lote_detalle['CantidadDisponible']))
                            #TablaLoteDetalles.pack(padx=10,pady=10,expand=True)
                            
                        """Insertar o actualizar el perfume en el inventario"""
                        if len(lista_inventario)>0:
                            for item_inventario in lista_inventario:
                                print(item_inventario)
                                if item_inventario['NombrePerfume'] == NombrePerfume.get():
                                    item_inventario['Existencia'] = item_inventario['Existencia'] +  int(CantidadCompra.get())
                                    Datos.GuardarInventario(Inventario)
                                else:
                                    nuevo_inventario = {"NombrePerfume":NombrePerfume.get(),"Existencia":int(CantidadCompra.get())}
                                    lista_inventario.append(nuevo_inventario)
                                    Datos.GuardarInventario(Inventario)
                        else:
                            nuevo_inventario = {"NombrePerfume":NombrePerfume.get(),"Existencia":int(CantidadCompra.get())}
                            lista_inventario.append(nuevo_inventario)
                            Datos.GuardarInventario(Inventario)
                                
                        msgbox.showinfo(title="Alta de lote de perfumes",message="Los datos del lote de perfumes fueron almacenados correctamente.")
                        ventana_perfume.destroy()
                
                def cancelar_perfume():
                    """Función que cancela el alta de un perfuime en el lote"""
                    ventana_perfume.destroy()
                
                """Crea la ventana para dar de alta el perfume en el lote"""
                ventana_perfume = Tk.Toplevel(PaginaPrincipal)
                ventana_perfume.title("Insertar perfume")
                ventana_perfume.geometry("800x100")
                ventana_perfume.update()
            
                etiqueta_lote = Tk.Label(ventana_perfume, text=f"Lote: {ILote}", anchor="w")
                etiqueta_lote.pack()
                
                """Frame para los botones de alta"""
                frame_datos_perfume = ttk.Frame(ventana_perfume)
                frame_datos_perfume.pack()
                
                """Presenta los vampos para la captura de la información del perfume"""
                etiqueta_IdPerfume = ttk.Label(frame_datos_perfume, text="Id del perfume: ")
                etiqueta_NombrePerfume = ttk.Label(frame_datos_perfume, text="Nombre del perfume: ")
                etiqueta_MarcaPerfume = ttk.Label(frame_datos_perfume, text="Marca del perfume: ")
                etiqueta_PresentacionPerfume = ttk.Label(frame_datos_perfume, text="Presentación del perfume: ")
                etiqueta_ImporteCompra = ttk.Label(frame_datos_perfume, text="Imprte de compra: ")
                etiqueta_CantidadCompra = ttk.Label(frame_datos_perfume, text="Cantidad comprada: ")
                #etiqueta_CantidadDisponible = ttk.Label(ventana_perfume, text="Cantidad disponible: ")

                IdPerfume = Tk.Entry(frame_datos_perfume)
                NombrePerfume = Tk.Entry(frame_datos_perfume)
                MarcaPerfume = Tk.Entry(frame_datos_perfume)
                PresentacionPerfume = Tk.Entry(frame_datos_perfume)
                ImporteCompra = Tk.Entry(frame_datos_perfume)
                CantidadCompra = Tk.Entry(frame_datos_perfume)
                #CantidadDisponible = Tk.Entry(ventana_perfume)
            
                etiqueta_IdPerfume.grid(row=0, column=0)
                IdPerfume.grid(row=0, column=1)
                etiqueta_NombrePerfume.grid(row=0, column=2)
                NombrePerfume.grid(row=0,column=3)
                etiqueta_MarcaPerfume.grid(row=0, column=4)
                MarcaPerfume.grid(row=0, column=5)
                
                etiqueta_PresentacionPerfume.grid(row=1, column=0)
                PresentacionPerfume.grid(row=1, column=1)
                etiqueta_ImporteCompra.grid(row=1, column=2)
                ImporteCompra.grid(row=1, column=3)
                etiqueta_CantidadCompra.grid(row=1, column=4)
                CantidadCompra.grid(row=1, column=5)

                """Frame para los botones de alta"""
                frame_botones_perfume = ttk.Frame(ventana_perfume)
                frame_botones_perfume.pack()
                boton_alta_perfume_aceptar = ttk.Button(frame_botones_perfume, text="Aceptar", command=insertar_perfume)
                boton_alta_perfume_cancelar = ttk.Button(frame_botones_perfume, text="Cancelar", command=cancelar_perfume)
                boton_alta_perfume_aceptar.grid(column=0, row=4)
                boton_alta_perfume_cancelar.grid(column=1, row=4)

            def editar_perfume_dentro_lote():
                
                def insertar_perfume_editar():
                    error_perfume = False
                    """Validación de información"""
                    if NombrePerfume.get()=="" or MarcaPerfume.get()=="" or PresentacionPerfume.get()=="" or ImporteCompra.get()== "" or  CantidadCompra.get() == "":
                        msgbox.showinfo(title="Edición de perfumes",message="Los campos no pueden estar vacíos.")
                        error_perfume = True
                    if not CantidadCompra.get().isnumeric():
                        msgbox.showinfo(title="Edición de perfumes",message="La cantidad comprada debe ser un número")
                        error_perfume = True
                    try:
                        float(ImporteCompra.get())
                    except:
                        msgbox.showinfo(title="Edición de perfumes",message="El importe de compra debe ser un número")
                        error_perfume = True
                    if error_perfume == False:
                        """Guardar inflormación y actualizar el treeview de perfumes"""
                        for item_actualizar in datos_lote_detalle:
                            if item_actualizar['IdPerfume'] == CPerfume:
                                item_actualizar['NombrePerfume']=NombrePerfume.get()
                                item_actualizar['MarcaPerfume']=MarcaPerfume.get()
                                item_actualizar['PresentacionPerfume']=PresentacionPerfume.get()
                                item_actualizar['ImporteCompra']=ImporteCompra.get()
                                item_actualizar['CantidadCompra']=CantidadCompra.get()
                                break
                        Datos.GuardarLotePerfume(LotesDetalles)
                        for item in TablaLoteDetalles.get_children():
                            TablaLoteDetalles.delete(item)
                        for item_lote_detalle in datos_lote_detalle:
                            TablaLoteDetalles.insert("", "end", values=(item_lote_detalle['IdPerfume'],item_lote_detalle['NombrePerfume'],item_lote_detalle['MarcaPerfume'],item_lote_detalle['PresentacionPerfume'],item_lote_detalle['ImporteCompra'],item_lote_detalle['CantidadCompra'],item_lote_detalle['CantidadDisponible']))
                        msgbox.showinfo(title="Edición de perfumes",message="Los datos del lote de perfumes fueron almacenados correctamente.")
                        ventana_perfume.destroy()
                def cancelar_perfume_editar():
                    ventana_perfume.destroy()
                    
                """Funciones para editar la información de un perfume dentro del lote"""
                curItemPerfume = TablaLoteDetalles.focus()
                item_perfume_seleccionado = TablaLoteDetalles.item(curItemPerfume)
                
                """Valida que se haya sele3ccionado un perfume"""
                if len(item_perfume_seleccionado['values'])>0:
                    """Crea la ventana para dart de alta el perfume en el lote"""
                    ventana_perfume = Tk.Toplevel(PaginaPrincipal)
                    ventana_perfume.title("Insertar perfume")
                    ventana_perfume.geometry("800x100")
                    ventana_perfume.update()
                    
                    CPerfume = str(item_perfume_seleccionado['values'][0])
                    
                    etiqueta_lote = Tk.Label(ventana_perfume, text=f"Lote: {ILote}", anchor="w")
                    etiqueta_lote.pack()
                    
                    """Frame para los botones de alta"""
                    frame_datos_perfume = ttk.Frame(ventana_perfume)
                    frame_datos_perfume.pack()

                    """Cargar información a los enrty para actualizar el regisgro"""
                    #textEntry_IdPerfume = Tk.StringVar()
                    textEntry_NombrePerfume = Tk.StringVar()
                    textEntry_MarcaPerfume = Tk.StringVar()
                    textEntry_PresentacionPerfume = Tk.StringVar()
                    textEntry_ImporteCompra = Tk.StringVar()
                    textEntry_CantidadCompra = Tk.StringVar()                    
                    
                    textEntry_NombrePerfume.set(item_perfume_seleccionado["values"][1])
                    textEntry_MarcaPerfume.set(item_perfume_seleccionado["values"][2])
                    textEntry_PresentacionPerfume.set(item_perfume_seleccionado["values"][3])
                    textEntry_ImporteCompra.set(item_perfume_seleccionado["values"][4])
                    textEntry_CantidadCompra.set(item_perfume_seleccionado["values"][5])
                    
                    """Presenta los vampos para la captura de la información del perfume"""
                    #etiqueta_IdPerfume = ttk.Label(frame_datos_perfume, text="Id del perfume: ")
                    etiqueta_NombrePerfume = ttk.Label(frame_datos_perfume, text="Nombre del perfume: ")
                    etiqueta_MarcaPerfume = ttk.Label(frame_datos_perfume, text="Marca del perfume: ")
                    etiqueta_PresentacionPerfume = ttk.Label(frame_datos_perfume, text="Presentación del perfume: ")
                    etiqueta_ImporteCompra = ttk.Label(frame_datos_perfume, text="Imprte de compra: ")
                    etiqueta_CantidadCompra = ttk.Label(frame_datos_perfume, text="Cantidad comprada: ")
                    #etiqueta_CantidadDisponible = ttk.Label(ventana_perfume, text="Cantidad disponible: ")
    
                    #IdPerfume = Tk.Entry(frame_datos_perfume, textvariable=textEntry_IdPerfume)
                    NombrePerfume = Tk.Entry(frame_datos_perfume, textvariable=textEntry_NombrePerfume)
                    MarcaPerfume = Tk.Entry(frame_datos_perfume, textvariable=textEntry_MarcaPerfume)
                    PresentacionPerfume = Tk.Entry(frame_datos_perfume, textvariable=textEntry_PresentacionPerfume)
                    ImporteCompra = Tk.Entry(frame_datos_perfume, textvariable=textEntry_ImporteCompra)
                    CantidadCompra = Tk.Entry(frame_datos_perfume, textvariable=textEntry_CantidadCompra)
                    #CantidadDisponible = Tk.Entry(ventana_perfume)
                
                    #etiqueta_IdPerfume.grid(row=0, column=0)
                    #IdPerfume.grid(row=0, column=1)
                    etiqueta_NombrePerfume.grid(row=0, column=0)
                    NombrePerfume.grid(row=0,column=1)
                    etiqueta_MarcaPerfume.grid(row=0, column=2)
                    MarcaPerfume.grid(row=0, column=3)
                    etiqueta_PresentacionPerfume.grid(row=0, column=4)
                    PresentacionPerfume.grid(row=0, column=5)
                    
                    etiqueta_ImporteCompra.grid(row=1, column=0)
                    ImporteCompra.grid(row=1, column=1)
                    etiqueta_CantidadCompra.grid(row=1, column=2)
                    CantidadCompra.grid(row=1, column=3)
                    
                    """Frame para los botones de alta"""
                    frame_botones_perfume = ttk.Frame(ventana_perfume)
                    frame_botones_perfume.pack()
                    boton_alta_perfume_aceptar_aceptar = ttk.Button(frame_botones_perfume, text="Aceptar", command=insertar_perfume_editar)
                    boton_alta_perfume_cancelar = ttk.Button(frame_botones_perfume, text="Cancelar", command=cancelar_perfume_editar)
                    boton_alta_perfume_aceptar_aceptar.grid(column=0, row=4)
                    boton_alta_perfume_cancelar.grid(column=1, row=4)
                    
                else:
                    msgbox.showerror(title=f"Alta de perfume: Lote: {ILote}", message="No se ha seleccionado un perfume de la lista")        
            
            
            def eliminar_perfume_dentro_lote():
                """
                Proceso para eliminar un regisrto
                Obitiene el item seleccionado en el treeview de perfumes en el lote
                """
                curItemPerfume = TablaLoteDetalles.focus()
                item_perfume_seleccionado = TablaLoteDetalles.item(curItemPerfume)
                
                """Valida que se haya sele3ccionado un perfume"""
                if len(item_perfume_seleccionado['values'])>0:
                    """Obtiene el id del perfume seleccionado y lo busca en la lista para eliminar el registro"""
                    CPerfume = str(item_perfume_seleccionado['values'][0])
                    for item_actualizar in datos_lote_detalle:
                        if item_actualizar['IdPerfume'] == CPerfume:
                            datos_lote_detalle.remove(item_actualizar)
                            break
                    #Datos.GuardarLotePerfume(LotesDetalles)
                    for item in TablaLoteDetalles.get_children():
                        TablaLoteDetalles.delete(item)
                    for item_lote_detalle in datos_lote_detalle:
                        TablaLoteDetalles.insert("", "end", values=(item_lote_detalle['IdPerfume'],item_lote_detalle['NombrePerfume'],item_lote_detalle['MarcaPerfume'],item_lote_detalle['PresentacionPerfume'],item_lote_detalle['ImporteCompra'],item_lote_detalle['CantidadCompra'],item_lote_detalle['CantidadDisponible']))
                    msgbox.showinfo(title="Edición de perfumes",message="El perfumes fueeliminado corrctamente.")
                
            """Obtiene el item (lote) seleccionado del treeview"""
            curItem = TablaLotePerfumes.focus()
            item_lote_seleccionado = TablaLotePerfumes.item(curItem)
       
            if len(item_lote_seleccionado['values'])>0:
                
                """Valida la información del lote yu regresa la lista de loles"""
                datos_lote_detalle, ILote, CEncontrado = ValidarLoteDetalle(item_lote_seleccionado['values'][0])
                limpiar()
                
                etiqueta_lote = ttk.Label(frame_datos,text=f"Lote: {item_lote_seleccionado['values'][0]}")
                etiqueta_lote.pack()
                
                """Crea el treeview"""
                TablaLoteDetalles = ttk.Treeview(frame_datos, columns=("C1","C2","C3","C4","C5","C6","C7"), show="headings")
                TablaLoteDetalles.heading("C1", text="Id perfume")
                TablaLoteDetalles.heading("C2", text="Nombre")
                TablaLoteDetalles.heading("C3", text="Marca")
                TablaLoteDetalles.heading("C4", text="Presentación")
                TablaLoteDetalles.heading("C5", text="Importe")
                TablaLoteDetalles.heading("C6", text="Cantidad (Compra)")
                TablaLoteDetalles.heading("C7", text="Cantidad (Disponible)")
                TablaLoteDetalles.column("C1", width=100)
                TablaLoteDetalles.column("C2", width=300)
                TablaLoteDetalles.column("C3", width=200)
                TablaLoteDetalles.column("C4", width=200)
                TablaLoteDetalles.column("C5", width=50)
                TablaLoteDetalles.column("C6", width=50)
                TablaLoteDetalles.column("C7", width=50)
                
                """Llena los registgros en el treeview"""
                for item_lote_detalle in datos_lote_detalle:
                    TablaLoteDetalles.insert("", "end", values=(item_lote_detalle['IdPerfume'],item_lote_detalle['NombrePerfume'],item_lote_detalle['MarcaPerfume'],item_lote_detalle['PresentacionPerfume'],item_lote_detalle['ImporteCompra'],item_lote_detalle['CantidadCompra'],item_lote_detalle['CantidadDisponible']))
                TablaLoteDetalles.pack(side="left", fill="both", expand=True)
                #TablaLoteDetalles.pack(padx=10,pady=10,expand=True)
                barra_vertical = ttk.Scrollbar(frame_datos, orient="vertical", command=TablaLoteDetalles.yview)
                barra_vertical.pack(side="right", fill="y")
                
                """Presenta los botonoes con las acciones para el lote"""
                boton_regresar_lotes = Tk.Button(frame_botones, text="Ver lotes", command=ListaLotesPerfumes)
                boton_agregar_perfume = Tk.Button(frame_botones, text="Agregar perfume", command=alta_perfume_dentro_lote)
                boton_editar_perfume = Tk.Button(frame_botones, text="Editar perfume", command=editar_perfume_dentro_lote)
                boton_eliminar_perfume = Tk.Button(frame_botones, text="Eliminar perfume", command=eliminar_perfume_dentro_lote)
                boton_regresar_lotes.grid(column=0, row=0, padx=10, pady=10)
                boton_agregar_perfume.grid(column=1, row=0, padx=10, pady=10)
                boton_editar_perfume.grid(column=2, row=0, padx=10, pady=10)
                boton_eliminar_perfume.grid(column=3, row=0, padx=10, pady=10)
                
            else:
                msgbox.showerror(title="Alta de lote de perfumes", message="No se ha seleccionado un lote de la lista")        
            
        limpiar()
        
        """Crea el treeviw para presentar el lote de perfumes"""
        TablaLotePerfumes = ttk.Treeview(frame_datos, columns=("C1","C2","C3","C4"), show="headings")
        TablaLotePerfumes.heading("C1", text="Id. Lote")
        TablaLotePerfumes.heading("C2", text="Fecha de compra")
        TablaLotePerfumes.heading("C3", text="Cantidad de perfumes")
        TablaLotePerfumes.heading("C4", text="Importe total")
        TablaLotePerfumes.column("C1", width=100)
        TablaLotePerfumes.column("C2", width=100, anchor='center')
        TablaLotePerfumes.column("C3", width=300, anchor='center')
        TablaLotePerfumes.column("C4", width=300, anchor='e')
        
        """Llena el treview con el la lkista de los lotes"""
        for item_lote_perfumes in lista_lotes:
            TablaLotePerfumes.insert("", "end", values=(item_lote_perfumes['id_lote'],item_lote_perfumes['fecha_compra'],item_lote_perfumes['cantidad_perfumes'],item_lote_perfumes['importe_compra']))
        TablaLotePerfumes.pack(padx=10,pady=10,expand=True) 

        """Presenta los botones para las acciones en el lote de perfunmes"""        
        boton_detalles_lote = Tk.Button(frame_botones, text="Ver detalles", command=ver_detalles_lote)
        boton_agregar_lote = Tk.Button(frame_botones, text="Agregar lote", command=alta_lote_perfumes)
        boton_editar_lote = Tk.Button(frame_botones, text="Editar lote", command=editar_lote_perfumes)
        #boton_eliminar_lote = Tk.Button(frame_botones, text="Eliminar lote")
        boton_detalles_lote.grid(column=0, row=0, padx=10, pady=10)
        boton_agregar_lote.grid(column=1, row=0, padx=10, pady=10)
        boton_editar_lote.grid(column=2, row=0, padx=10, pady=10)
        #boton_eliminar_lote.grid(column=3, row=0, padx=10, pady=10)

    def registro_ventas():

        def llenar_lista_lotes():
            """Lompia y llena la lista de perfumes en inventario"""
            for item in TablaInventario.get_children():
                TablaInventario.delete(item)
            for item_inventario in lista_lotes_detalles:
                lista_perfumes_lote = item_inventario["Perfumes"]
                for item_perfumes in lista_perfumes_lote:
                    if int(item_perfumes['CantidadDisponible'])>0:
                        TablaInventario.insert("", "end", values=(item_perfumes['NombrePerfume'],item_perfumes['MarcaPerfume'],item_perfumes['PresentacionPerfume'],item_perfumes['ImporteCompra'],item_perfumes['CantidadDisponible'],item_inventario['IdLotes'],item_perfumes['IdPerfume']))
            
        def registrar_venta_cliente():

            def registrar_venta_aceptar():
                """Función para registrar la venta"""
                
                """Obtiene el id del cliente"""
                for item_cliente in lista_clientes:
                    if item_cliente['NombreCompleto'] == combo_clientes.get():
                        CCliente = item_cliente['Nombre']
                        break
                """Regisgro de la venta"""
                cliente_encontrado = False
                error_venta = False

                """Validación de datos de entrada"""
                try:
                    dt.datetime.strptime(fecha_compra.get(), "%d/%m/%Y").date()
                except ValueError:
                    msgbox.showerror(title="Registro de ventas",message="Formato de fecha incorrecto.")
                    error_venta = True
                try:
                    float(importe_compra.get())
                except ValueError:
                    msgbox.showerror(title="Registro de ventas",message="Importe de compra con formato incorrecto.")
                    error_venta = True
                try:
                    float(cantidad_compra.get())
                except ValueError:
                    msgbox.showerror(title="Registro de ventas",message="Cantidad de compra con formato incorrecto.")
                    error_venta = True
                
                """Registro del movimiento"""
                if error_venta == False:
                    if int(cantidad_compra.get())<=CantidadDisponible:
                        for item_cliente_movimientos in lista_clientes_movimientos:
                            if item_cliente_movimientos['Cliente'] == CCliente:
                                cliente_encontrado = True
                                break
                        if cliente_encontrado == True:
                                nuevo_registro_venta = {'TipoMovimiento':'C','FechaMovimiento':str(dt.datetime.today()),'FechaCompra':fecha_compra.get(),'ImporteMovimiento':float(importe_compra.get()),'CantidadPerfumes':int(cantidad_compra.get()),'PerfumeCompra':NombrePerfume,'PerfumeCompraPresentacion':PresentacionPerfume,'PerfumeCompraImporte':ImporteCompra}
                                item_cliente_movimientos['Movimientos'].append(nuevo_registro_venta)
                                Datos.GuardarClientesMovimientos(ClientesMovimientos)
                                for item_lote_perfumes in lista_lotes_detalles:
                                    if item_lote_perfumes['IdLotes']==CLote:
                                        for item_perfume in item_lote_perfumes['Perfumes']:
                                            if item_perfume['IdPerfume']==CPerfume:
                                                item_perfume['CantidadDisponible']=int(item_perfume['CantidadDisponible'])-int(cantidad_compra.get())
                                Datos.GuardarLotePerfume(LotesDetalles)
                                msgbox.showinfo("Registro de ventas", message="Venta registrada correctamente")
                                llenar_lista_lotes()
                                ventana_registro_venta.destroy()
                        else:
                            msgbox.showerror("Registro de ventas", message="No se pudo registrar la venta: Cliente no encontrado")
                    else:
                        msgbox.showerror("Registro de ventas", message="No se pudo registrar la venta: No hay existencia suficiente para registrar la venta")
                
            def registrar_venta_cancelar():
                """Cancelar el registro de la venta"""
                ventana_registro_venta.destroy()
                
            """Obtiene el item del perfume disponible"""
            curItem = TablaInventario.focus()
            item_perfume_seleccionado = TablaInventario.item(curItem)
       
            if len(item_perfume_seleccionado['values'])>0:
                """Genera la ventana para el registro de la venta"""
                ventana_registro_venta = Tk.Toplevel(PaginaPrincipal)
                ventana_registro_venta.title("Registro de ventas")
                ventana_registro_venta.geometry("400x150")
                ventana_registro_venta.update()
                
                """Genera la lista para llenar el combo de clientes"""
                lista_combo_clientes = []
                for item_cliente in lista_clientes:
                    if item_cliente['Status']=="A":
                        lista_combo_clientes.append(item_cliente['NombreCompleto'])

                frame_datos_venta = ttk.Frame(ventana_registro_venta)
                frame_datos_venta.pack()

                """Obtiene los datos del perfume seleccionado"""
                CLote = item_perfume_seleccionado["values"][5]
                CPerfume = item_perfume_seleccionado["values"][6]
                NombrePerfume = item_perfume_seleccionado["values"][0] + " - " + item_perfume_seleccionado["values"][1]
                PresentacionPerfume = item_perfume_seleccionado["values"][2]
                ImporteCompra = float(item_perfume_seleccionado["values"][3])
                CantidadDisponible = int(item_perfume_seleccionado["values"][4])
                
                """Coloca los dartos para el registro de la venta"""
                etiqueta_cliente = Tk.Label(frame_datos_venta, text="Cliente: ")
                etiqueta_cantidad_compra = Tk.Label(frame_datos_venta, text="Cantidad de perfumes a comprar: ")
                etiqueta_importe_compra = Tk.Label(frame_datos_venta, text="Importe de la comprar: ")
                etiqueta_fecha_compra = Tk.Label(frame_datos_venta, text="Fecha d compra: ")
                combo_clientes = ttk.Combobox(frame_datos_venta, values=lista_combo_clientes, state="readonly")                
                cantidad_compra = Tk.Entry(frame_datos_venta)
                importe_compra = Tk.Entry(frame_datos_venta)
                fecha_compra = Tk.Entry(frame_datos_venta)
                
                """colocación de campos"""
                etiqueta_cliente.grid(row=0, column=0)
                combo_clientes.grid(row=0, column=1)
                etiqueta_cantidad_compra.grid(row=1, column=0)
                cantidad_compra.grid(row=1, column=1)
                etiqueta_importe_compra.grid(row=2, column=0)
                importe_compra.grid(row=2, column=1)
                etiqueta_fecha_compra.grid(row=3, column=0)
                fecha_compra.grid(row=3, column=1)
                
                """Frame para los botones de registgro e venta"""
                frame_botones_venta = ttk.Frame(ventana_registro_venta)
                frame_botones_venta.pack()
                boton_registrar_venta_aceptar = ttk.Button(frame_botones_venta, text="Aceptar", command=registrar_venta_aceptar)
                boton_registrar_venta_cancelar = ttk.Button(frame_botones_venta, text="Cancelar", command=registrar_venta_cancelar)
                boton_registrar_venta_aceptar.grid(column=0, row=4)
                boton_registrar_venta_cancelar.grid(column=1, row=4)
                                
            else:
                msgbox.showerror(title="Registro de ventas", message="No se ha seleccionado un perfume de la lista")        
                
        limpiar()
        
        """
        Llenar los datos del triview con la existencia de perfumes para registrar venta
        """
        TablaInventario = ttk.Treeview(frame_datos, columns=("C1","C2","C3","C4","C5","C6","C7"), show="headings")
        TablaInventario.heading("C1", text="Nombre del perfume")
        TablaInventario.heading("C2", text="Marca")
        TablaInventario.heading("C3", text="Presentación")
        TablaInventario.heading("C4", text="Costo")
        TablaInventario.heading("C5", text="Existencia")
        TablaInventario.heading("C6", text="Lote")
        TablaInventario.heading("C7", text="Id. perfume")
        TablaInventario.column("C1", width=200)
        TablaInventario.column("C2", width=200)
        TablaInventario.column("C3", width=200)
        TablaInventario.column("C4", width=100)
        TablaInventario.column("C5", width=100)
        TablaInventario.column("C6", width=100)
        TablaInventario.column("C7", width=100)
        
        """Obtiene los perfumes en lotes con disponibilidad"""
        llenar_lista_lotes()
        """
        for item_inventario in lista_lotes_detalles:
            lista_perfumes_lote = item_inventario["Perfumes"]
            for item_perfumes in lista_perfumes_lote:
                if int(item_perfumes['CantidadDisponible'])>0:
                    TablaInventario.insert("", "end", values=(item_perfumes['NombrePerfume'],item_perfumes['MarcaPerfume'],item_perfumes['PresentacionPerfume'],item_perfumes['ImporteCompra'],item_perfumes['CantidadDisponible'],item_inventario['IdLotes'],item_perfumes['IdPerfume']))
        """
        TablaInventario.pack(side="left", fill="both", expand=True)
        barra_vertical = ttk.Scrollbar(frame_datos, orient="vertical", command=TablaInventario.yview)
        barra_vertical.pack(side="right", fill="y")
        
        boton_registrar_venta = Tk.Button(frame_botones, text="Registrar venta", command=registrar_venta_cliente)
        boton_registrar_venta.grid(row=0, column=0)
        
#Procesos====================================================================================
    
    def cerrar_sesion():
        PaginaPrincipal.destroy()
        VentanaPrincipal.destroy()

    PaginaPrincipal = Tk.Toplevel(VentanaPrincipal)
    PaginaPrincipal.geometry("1000x500")
    PaginaPrincipal.title("Ventana principal")
    PaginaPrincipal.update()

    LblSistema = Tk.Label(PaginaPrincipal, text="Sistema de adminitración y gestión\nPerfumes originales Lorenzo", padx=20, pady=20)
    LblSistema.pack()

    PaginaPrincipalAncho = PaginaPrincipal.winfo_width()
    LblUsuario = Tk.Label(PaginaPrincipal, text="Usuario: " + parametro_nombre_Usuario, width=PaginaPrincipalAncho, anchor="w")
    match parametro_status_usuario:
        case "A":
            LblStatusUsuario = Tk.Label(PaginaPrincipal, text="Status: Activo", width=PaginaPrincipalAncho, anchor="w")        
    LblUsuario.pack()
    LblStatusUsuario.pack()
    
    frame_datos = Tk.Frame(PaginaPrincipal, padx=20, pady=20)
    frame_datos.pack()

    frame_botones = Tk.Frame(PaginaPrincipal)
    frame_botones.pack()        
    
    ListaClientes()
    
    # create a menubar
    menubar = Menu(PaginaPrincipal)
    PaginaPrincipal.config(menu=menubar)
    # create the file_menu
    file_menu = Menu(
        menubar,
        tearoff=0
    )
    # add menu items to the File menu
    file_menu.add_command(label='Lista de clientes', command=ListaClientes)
    file_menu.add_command(label='Lotes de perfumes', command=ListaLotesPerfumes)
    file_menu.add_command(label='Registro de ventas', command=registro_ventas)
    file_menu.add_separator()
    file_menu.add_command(
        label='Cerrar sesión',
        command=cerrar_sesion
    )
    # add the File menu to the menubar
    menubar.add_cascade(
        label="Archivos",
        menu=file_menu
    )        

#Código principal============================================================================================================================    

VentanaPrincipal = Tk.Tk()
VentanaPrincipal.geometry("500x300")
VentanaPrincipal.title("Proyecto final - CETEC")

LblSistema = Tk.Label(VentanaPrincipal, text="Sistema de adminitración y gestión\nPerfumes originales Lorenzo", padx=20, pady=20)
LblSistema.pack()

FrameUsuario = Tk.Frame(VentanaPrincipal, pady=20)
FrameUsuario.pack()

EtiquetaUsuario = Tk.Label(FrameUsuario, text = "Usuario: ")
EtiquetaContraseña = Tk.Label(FrameUsuario, text = "Contraseña: ")
TextoUsuario = Tk.Entry(FrameUsuario)
TextoContraseña = Tk.Entry(FrameUsuario, show="*")

EtiquetaUsuario.grid(column=0, row=0)
TextoUsuario.grid(column=1, row=0)
EtiquetaContraseña.grid(column=0, row=1)
TextoContraseña.grid(column=1, row=1)

BtnIngresar = Tk.Button(VentanaPrincipal, text="Ingresar", command=IniciarSesion)
BtnIngresar.pack()

LblResultado = Tk.Label(VentanaPrincipal, text="", padx=10, pady=10)
LblResultado.pack()

VentanaPrincipal.mainloop()
