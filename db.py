import sqlite3
from sqlite3.dbapi2 import Cursor
import time
import os



"""
==============================================================


La escuela tiene remeras, buzos, polleras y chombas para vender (que fabrica la gente de FP). 
Hacer un sistema que permita llevar el stock (cuando entran, quien las llevan y que cantidades)
y cuando se venden, con nro de factura, etc.



==============================================================
"""




def insertar_datos(tabla_num):
    conexion = conectar_base_datos()
    cursor = conexion.cursor()
    query = generar_query_insert(tabla_id= tabla_num)

    compra = False
    datos = []
    stock = cursor.execute("select stock from inventario where id = 2").fetchall()
    print(stock)

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
            data = input(f" INGRESE {column.upper()}: ")
            """
                if column == 'cantidad':
                    cantidad = data
                    compra = True
            """
            datos.append(data)

    #if compra:
    
            
    print("DATOS AGREGADOS: ",datos)
    input("\n<continue>")

    cursor.execute(query,datos)
    conexion.commit()


def consultar_compra(wea=""):
    if wea is None:
        nro_factura = input("INGRESE EL NUMERO DE FACTURA: ")
        query = "SELECT * FROM compra WHERE nro_factura = "+ nro_factura

        conexion = sqlite3.connect('base_de_datos.db')
        con = conexion.execute(query)
        resul = con.fetchall()

        if len(resul) == 0:
            print(" ..... NO HAY REGISTRO DE COMPRAS .....\n")
            input("\n<continue>")
        else:
            print(resul)
            input("\n<continue>")

def ver_stock(wea=""):
    pass

def ver_proveedores(wea=""):
    pass


MENU = [
    {'id': 1, 'nombre':'VENTAS','submenu':[{'id':1, 'nombre':'AGREGAR COMPRA', 'funcion': insertar_datos, 'tab_id': 2},   # agregar compra, consultar alguna venta, 
                                           {'id':2, 'nombre':'CONSULTAR VENTA', 'funcion': consultar_compra, 'tab_id': None},
                                           {'id':3, 'nombre':'ELIMINAR VENTA', 'funcion': ver_stock, 'tab_id': None}
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
    {'id': 5, 'nombre':'compra_ropas','columns': ('nro_factura_compra', 'ID_ropas')},
    {'id': 6, 'nombre':'prov_ropas','columns': ('ID_prov', 'ID_ropas', 'hora', 'fecha')}
]

CONSULTAS = [
    {'id': 1, 'nombre_1':'INSERT INTO ','nombre_2':') VALUES('},
    {'id': 2, 'nombre_1':'SELECT * FROM '},     # SELECT ALL FROM
    {'id': 3, 'nombre_1':'SELECT ','nombre_2':' FROM ', 'nombre_3':' WHERE '},
    {'id': 4, 'nombre_1':'INSERT INTO ','nombre_2':') VALUES('},
]

def imprimir_menu(menu=MENU):
    n = 1
    for item in menu:
        print(f"[{n}] - {item['nombre']}")
        n += 1
    print()

    opcion1 = int(input("-> "))

    if opcion1 == 4:
        quit()          # AQUI SI EL USUARIO INGRESA EL NUMERO 4 TERMINA EL PROGRAMA

    else:
    
        n = 1
        for subitem in menu[opcion1-1]['submenu']:       # este segundo FOR imprime el 'sub-menu' de cada item
            print(f"[{n}] - {subitem['nombre']}")
            n += 1
        print()

        opcion2 = int(input("-> "))

        funcion = menu[opcion1-1]['submenu'][opcion2-1]['funcion']
        tab_id = menu[opcion1-1]['submenu'][opcion2-1]['tab_id']

        return funcion(tab_id)



def conectar_base_datos():
    # funcion que crea y conecta con la base de datos
    conexion = sqlite3.connect('base_de_datos.db')
    return conexion

def creacion_tablas():
    # funcion que crea todas las tablas que necesitamos
    cursor = conectar_base_datos()

    tabla_clientes = "CREATE TABLE IF NOT EXISTS cliente(dni integer PRIMARY KEY NOT NULL, nombre text NOT NULL, apellido text NOT NULL, domicilio text NOT NULL, telefono integer NOT NULL)"
    tabla_compra = "CREATE TABLE IF NOT EXISTS compra(nro_factura integer PRIMARY KEY NOT NULL, producto text NOT NULL, cantidad int NOT NULL, importe integer NOT NULL, forma_pago text NOT NULL, dni_cliente integer NOT NULL, fecha date NOT NULL, hora time NOT NULL, FOREIGN KEY(dni_cliente) REFERENCES cliente(dni))"
    tabla_ropas = "CREATE TABLE IF NOT EXISTS inventario(ID integer PRIMARY KEY NOT NULL, nombre text NOT NULL, stock integer NOT NULL)"
    tabla_proveedores = "CREATE TABLE IF NOT EXISTS proveedores(ID integer PRIMARY KEY NOT NULL, nombre text NOT NULL, domicilio text NOT NULL, telefono integer NOT NULL)"
    tabla_compra_ropas = "CREATE TABLE IF NOT EXISTS compra_ropas(nro_factura_compra integer NOT NULL, ID_ropas integer NOT NULL, FOREIGN KEY(nro_factura_compra) REFERENCES compra(nro_factura), FOREIGN KEY(ID_ropas) REFERENCES ropas(ID))"
    tabla_prove_ropas = "CREATE TABLE IF NOT EXISTS prov_ropas(ID_prov integer NOT NULL, ID_ropas integer NOT NULL, hora time PRYMARY KEY NOT NULL, fecha date NOT NULL, FOREIGN KEY(ID_prov) REFERENCES proveedores(ID), FOREIGN KEY(ID_ropas) REFERENCES ropas(ID))"

    cursor.execute(tabla_clientes)
    cursor.execute(tabla_compra)
    cursor.execute(tabla_ropas)
    cursor.execute(tabla_proveedores)
    cursor.execute(tabla_compra_ropas)
    cursor.execute(tabla_prove_ropas)

def generar_query_insert(tabla_id, lista=TABLAS):
    # funcion para generar una INSERT consulta automática
    for menu in lista:
        if menu['id'] == tabla_id:
            break

    sql1 = "INSERT INTO "+ menu['nombre'] +"("
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
    print(sql)

    return sql     # RETORNA LA QUERY





# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================


#conectar_base_datos()
creacion_tablas()

#generar_query_insert(2)
while True:
    os.system("cls")
    imprimir_menu()

"""
sql = "select nombre, stock from inventario"
conexion = sqlite3.connect('base_de_datos.db')

con = conexion.execute(sql)
resul = con.fetchall()
print(resul)  """



