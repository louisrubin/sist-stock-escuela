# LIBRERIAS QUE IMPORTE
import sqlite3
import time
import os


"""
==============================================================

CONSIGNA: 

La escuela tiene remeras, buzos, polleras y chombas para vender (que fabrica la gente de FP). 
Hacer un sistema que permita llevar el stock (cuando entran, quien las llevan y que cantidades)
y cuando se venden, con nro de factura, etc.

==============================================================
"""

def insertar_datos(tabla_num):
    # FUNCION PARA INSERTAR DATOS A UNA TABLA QUE ESPERA UN DATO POR PARAMETRO 'tabla_num'
    conexion = conectar_base_datos()
    cursor = conexion.cursor()
    query1 = generar_query_insert(tabla_id= tabla_num)  # FUNCION

    compra = False

    datos = []      # LISTA VACIA DONDE SE ALMACENARÁN LOS DATOS PARA INSERTAR DESPUES EN LA BASE DE DATOS

    try:
        # EL 'try/except' ES COMO UN 'if' PERO CON ERRORES

        for column in TABLAS[tabla_num-1]['columns']:

            if column == 'fecha':
                t1 = time.localtime()
                t2 = time.strftime('%d/%m/%Y', t1)
                datos.append(t2)

            elif  column == 'hora':
                t1 = time.localtime()
                t2 = time.strftime("%H:%M:%S", t1)
                datos.append(t2)

            else:
                data = input(f" (X - SALIR) - INGRESE {column.upper()}: ")

                if data.lower() != 'x':
                    
                    if column == 'cantidad':

                        stock = list(sub[0] for sub in cursor.execute("SELECT stock FROM inventario WHERE nombre = '" + datos[0] + "'").fetchall())[0]      # res = list(sub[0] for sub in test_tuple)
                        id_update = list(sub[0] for sub in cursor.execute("SELECT id FROM inventario WHERE nombre = '" + datos[0] + "'").fetchall())[0]

                        
                        new_cantidad = stock - int(data)
                        compra = True
                    
                    datos.append(data)  
                else:
                    break

        if compra == True:      # SI LA VARIABLE 'compra' ES VERDADERO SIGNIFICA UNA COMPRA Y GENERA UNA QUERY  'UPDATE' RESTANTO EL STOCK
            query2 = "UPDATE inventario SET stock = " + str(new_cantidad) + " WHERE id = " + str(id_update)
            cursor.execute(query2)
        
        
        cursor.execute(query1,datos)
        conexion.commit()
        print("--------------------------------------------------------------------------------------------")
        print("\nDATOS AGREGADOS: ",datos)
        print("\n... STOCK DEL INVENTARIO ACTUALIZADO ...")
        input("\n<continue>")

    except:
        # EXCEPCION
        print("-------------------------------------------")
        print("\n OPERACION CANCELADA O PRODUCTO NO ENCONTRADO")
        print("... LOS DATOS NO FUERON AGREGADOS ...")
        input("\n<continue>")



def consultar_compra(wea=""):
    if wea is None:
        conexion = sqlite3.connect('base_de_datos.db')
        cursor = conexion.cursor()

        nro_factura = input("INGRESE EL NUMERO DE FACTURA: ")                       # res = list(sub[0] for sub in test_tuple)
        query1 = "SELECT * FROM compra WHERE nro_factura = "+ nro_factura

        try:
            dni = list(sub[5] for sub in cursor.execute("SELECT * FROM compra WHERE nro_factura = " + nro_factura ).fetchall())[0]
            query2 = "SELECT * FROM cliente WHERE dni = " + str(dni)

            print(" \n DATOS DE LA COMPRA: ",conexion.execute(query1).fetchall())
            print(" DATOS DEL CLIENTE: ",conexion.execute(query2).fetchall())
            input("\n<continue>")

        except:
            print(" ..... NO HAY REGISTRO DE ESA COMPRAS .....\n")
            input("\n<continue>")



def ver_stock(wea=""):
    if wea is None:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()

        stock = cursor.execute("SELECT nombre, stock FROM inventario").fetchall()   # PIDE A LA BASE DE DATOS QUE DEVUELVA 'nombre, stock' DE LA TABLA 'inventario' 
                                                                                    # Y LO ALMACENA EN UNA VARIABLE 'stock'
        print("\n------------------ INVENTARIO ------------------")
        for x in stock:
            print(x)
        print("----------------------------------------------")
        input("\n<continue>")



def ver_proveedores(wea=""):
    if wea is None:
        conexion = conectar_base_datos()
        cursor = conexion.cursor()
        print("\n----------------------- PROVEEDORES -----------------------\n")
        print(cursor.execute("SELECT nombre, domicilio, telefono FROM proveedores").fetchall())     # IGUAL QUE EN LA FUNCION 'ver_stock' PERO ESTE NO ALMACENA EN NINGUNA VARIABLE
        print("--------------------------------------------------------")
        input("\n<continue>")


MENU = [
    # UNA LISTA CON DICCIONARIOS DENTRO, Y DENTRO DEL DICCIONARIO 'submenu' HAY OTRO LISTA CON OTRO DICCIONARIO
    {'id': 1, 'nombre':'VENTAS','submenu':[{'id':1, 'nombre':'AGREGAR COMPRA', 'funcion': insertar_datos, 'tab_id': 2},   # agregar compra, consultar alguna venta, 
                                           {'id':2, 'nombre':'CONSULTAR VENTA', 'funcion': consultar_compra, 'tab_id': None}
                                            ]},                                     

    {'id': 2, 'nombre':'STOCK','submenu':[{'id':1, 'nombre':'VER STOCK', 'funcion': ver_stock, 'tab_id': None},     # consultar stock de algun producto, agregar stock
                                          {'id':2, 'nombre':'AGREGAR STOCK', 'funcion': insertar_datos, 'tab_id': 3},
                                            ]},

    {'id': 3, 'nombre':'PROVEEDORES','submenu':[{'id':1, 'nombre':'VER PROVEEDORES', 'funcion': ver_proveedores, 'tab_id': None},
                                                {'id':2, 'nombre':'AGREGAR PROVEEDOR', 'funcion': insertar_datos, 'tab_id': 4},
                                                ]},
    {'id': 4, 'nombre': 'SALIR'}
]

TABLAS = [
    # LISTA DE TABLAS EN LA BASE DE DATOS, SI HAY QUE AGREGAR OTRA TRABA SIMPLEMENTE SE AGREGA ACA Y UNA FUNCION RECORRE ESTA LISTA Y AGREGA LA NUEVA TABLA ;)
    {'id': 1, 'nombre':'clientes','columns': ('DNI', 'apellido', 'nombre', 'domicilio', 'telefono')},
    {'id': 2, 'nombre':'compra','columns': ('producto', 'cantidad', 'importe', 'forma_pago', 'DNI_cliente', 'fecha', 'hora')},
    {'id': 3, 'nombre':'inventario','columns': ('nombre', 'stock')},
    {'id': 4, 'nombre':'proveedores','columns': ('nombre', 'domicilio', 'telefono')},
]


def imprimir_menu(menu=MENU):
    # FUNCION QUE IMPRIME EL MENU PRINCIPAL Y RETORNA AL FINAL UNA FUNCION QUE SE ENCUENTRA EN LA LISTA 'MENU' Y CON UN 'tab_id'
    n = 1
    for item in menu:
        print(f"[{n}] - {item['nombre']}")
        n += 1
    print()

    opcion1 = int(input("-> "))

    if opcion1 == 4:    # AQUI SI EL USUARIO INGRESA EL NUMERO 4, SE LLAMA A UNA FUNCION 'quit()' QUE SALE DEL PROGRAMA
        print("\n BIBLIOGRAFIA USADA:\n - https://likegeeks.com/python-sqlite3-tutorial/")
        print(" - https://www.programiz.com/python-programming/time")
        print("- https://developers.google.com/edu/python/lists\n")
        quit()          

    elif opcion1 < n:
    
        n = 1
        for subitem in menu[opcion1-1]['submenu']:       # este segundo FOR imprime el 'sub-menu' de cada item
            print(f"[{n}] - {subitem['nombre']}")
            n += 1
        print()

        opcion2 = int(input("-> "))

        funcion = menu[opcion1-1]['submenu'][opcion2-1]['funcion']
        tab_id = menu[opcion1-1]['submenu'][opcion2-1]['tab_id']

        return funcion(tab_id)      # AQUI LA FUNCION - RETORNA - OTRA FUNCION QUE SE ENCUENTRA EN LA LISTA 'MENU'




def conectar_base_datos():
    # funcion que crea y conecta con la base de datos
    conexion = sqlite3.connect('base_de_datos.db')
    return conexion



def creacion_tablas():
    # funcion que crea todas las tablas que necesitamos
    cursor = conectar_base_datos()

    tabla_clientes = "CREATE TABLE IF NOT EXISTS cliente(dni integer PRIMARY KEY NOT NULL, nombre text NOT NULL, apellido text NOT NULL, domicilio text NOT NULL, telefono integer NOT NULL)"
    tabla_compra = "CREATE TABLE IF NOT EXISTS compra(nro_factura integer PRIMARY KEY NOT NULL, producto text NOT NULL, cantidad int NOT NULL, importe integer NOT NULL, forma_pago text NOT NULL, dni_cliente integer NOT NULL, fecha date NOT NULL, hora time NOT NULL)"
    tabla_ropas = "CREATE TABLE IF NOT EXISTS inventario(ID integer PRIMARY KEY NOT NULL, nombre text NOT NULL, stock integer NOT NULL)"
    tabla_proveedores = "CREATE TABLE IF NOT EXISTS proveedores(ID integer PRIMARY KEY NOT NULL, nombre text NOT NULL, domicilio text NOT NULL, telefono integer NOT NULL)"

    cursor.execute(tabla_clientes)
    cursor.execute(tabla_compra)
    cursor.execute(tabla_ropas)
    cursor.execute(tabla_proveedores)

def generar_query_insert(tabla_id, lista=TABLAS):
    # funcion para generar un string INSERT, una consulta automática que despues se usa para la base de datos

    for menu in lista:
        if menu['id'] == tabla_id:
            break

    sql1 = "INSERT INTO "+ menu['nombre'] + "("
    sql2 = " VALUES ("
    cont= 1

    for colum in menu['columns']:

        if cont < len(menu['columns']):         
            sql1 += colum + ", "
            sql2 += "?, "
            
                
        else:
            sql1 += colum + ")"
            sql2 += "?)"
        cont += 1

    sql = sql1 + sql2

    return sql     # RETORNA LA QUERY



# ====================================================================================================================
# ====================================================================================================================


creacion_tablas()

while True:     # UN CICLO WHILE DONDE IMPRIME EL MEMNU PRINCIPAL
    os.system("cls")    # ESTO LIMPIA EL CMD CON EL COMANDO 'cls'
    imprimir_menu()
