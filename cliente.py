import socket

lista = """
    1.Usuario
    2.Crear carpeta
    3.Delete Carpeta
    4.Subir archivo
    5.Descargar Archivo
"""

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
    c.connect(("localhost",4000))

    while True:
        print(lista)
        opcion = input("Accion: ")
        c.send(opcion.encode())

        if opcion == "cerrar":
            c.close()
            break
        elif opcion == "1":
            try:
                print("Bienvenido a la creacion de usuarios")
                user = input("Usuario: ")
                contr = input("Passwd: ")
                mensaje = "{},{}".format(user,contr) 
                c.send(mensaje.encode())
                respuesta_server = c.recv(1024).decode()
                print(respuesta_server)
                
            except Exception as e:
                print(e)

        elif opcion == "2":
            try:
                print("Bienvenido a la creacion de carpetas")
                user = input("Usuario: ")
                contr = input("Passwd: ")
                mensaje = "{},{}".format(user,contr)
                c.send(mensaje.encode())
                respuesta_server = c.recv(1024).decode()

                if bool(respuesta_server):
                    nombre_carpeta = input("Dime el nombre de la carpeta: ")
                    c.send(nombre_carpeta.encode())
                else:
                    print("Confirmacion Negativa")
            except Exception as e:
                print(e)

        elif opcion == "3":
            try:
                print("Bienvenido al apartado de borrar carpetas")
                user = input("Usuario: ")
                contr = input("Passwd: ")
                mensaje = "{},{}".format(user,contr)
                c.send(mensaje.encode())
                respuesta_server = c.recv(1024).decode()
                
                if bool(respuesta_server):
                    carpeta_borrar = input("Dime la carpeta que deseas borrar")
                    c.send(carpeta_borrar.encode())
            except Exception as e:
                print(e)
            
        elif opcion == "4":
            try:
                print("Bienvenido al apartado de Subir Archivos")
                user = input("Usuario: ")
                contr = input("Passwd: ")
                mensaje = "{},{}".format(user,contr)
                c.send(mensaje.encode())
                respuesta_server = c.recv(1024).decode()
                if bool(respuesta_server):
                    lista_archivos_cliente = c.recv(1024).decode()
                    print(lista_archivos_cliente)
                    archivo_a_subir = input("Dime el archivo que deseas subir: ")
                    c.send(archivo_a_subir.encode())
            except Exception as e:
                print(e)
                    

        elif opcion == "5":
            try:
                print("Bienvenenido al apartado de Descarga de Archivos")
                user = input("Usuario: ")
                contr = input("Passwd: ")
                mensaje = "{},{}".format(user,contr)
                c.send(mensaje.encode())
                respuesta_server = c.recv(1024).decode()
                if bool(respuesta_server):
                    lista_archivos = c.recv(1024).decode()
                    print(lista_archivos)
                    archivo_borrar = input("Dime el archivo que deseas descargar: ")
                    c.send(archivo_borrar.encode())
            except Exception as e:
                print(e)

            




        

        
            
                
            



