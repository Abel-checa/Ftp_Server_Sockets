import socket
import base_datos as bd
import os
from shutil import copy as cp
from pathlib import Path
import logging
import time

dir_usu = "./usuarios/"
dir_archivo_server = "./archivos_server/"
dir_docs_cliente = "/documentos_cliente/"

logging.basicConfig(filename="./errores/log.txt",level= logging.INFO)
    
class Usuario:
    def __init__(self,usuario,passwd):
        self.usuario = usuario
        self.passwd = passwd
        self.home = dir_usu+usuario
    def __str__(self):
        return "Usuario: {}\nPasswd: {}\nHome: {}".format(self.usuario,self.passwd,self.home)

    def crear_home(self):
        os.mkdir(self.home)
        os.mkdir(self.home+"/"+"documentos")
        logging.info("El usuario {} ha iniciado sesion el {}".format(self.usuario,time.asctime(time.localtime())))

    def crear_archivos_user(self):
        os.mkdir(self.home+"/"+"archivos_cliente")
        dir_archivos_cliente = self.home+"/"+"archivos_cliente/"
        with open(dir_archivos_cliente+"zombie.txt","a") as file:
            file.write("Este es el archivo de Zombies del cliente")
            file.close()
        with open(dir_archivos_cliente+"princesas.txt","a") as file2:
            file2.write("Este es el archivo de princesas del cliente")
            file2.close()
        
    def search_user(self,carpeta):
        os.mkdir(self.home+"/"+carpeta)
        logging.info("El usuario {} ha creado la carpeta '{}' el {}".format(self.usuario,carpeta,time.asctime(time.localtime())))

    def borrar_carpeta(self,carpeta):
        os.rmdir(self.home+"/"+carpeta)
        logging.info("El usuario {} ha borrado la carpeta '{}' el {}".format(self.usuario,carpeta,time.asctime(time.localtime())))
    


host = "localhost"
port = 4000

users = []
nombres_usuarios = []

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((host,port))
    s.listen(5)
    conn,addr = s.accept()

    with conn:
        while True:
            data_server = conn.recv(1024).decode()
            
            if data_server == "cerrar":
                conn.close()
                break

            if data_server == "1":
                mensaje = conn.recv(1024).decode()
                split = mensaje.split(",")
                user,user_passwd = split
                objeto= Usuario(user,user_passwd)
                users.append(objeto)
                objeto.crear_home()
                objeto.crear_archivos_user()
                bd.conexion_sql(users)
                conn.send(b"El usuario ha sido creado con exito!")
            elif data_server == "2":
                try:
                    mensaje = conn.recv(1024).decode()
                    split = mensaje.split(",")
                    user,user_passwd = split
                    resultado = bd.consulta_usuario(user,user_passwd)
                    if resultado:
                        conn.sendall(str(resultado).encode())
                        nombre_carpeta_cliente= conn.recv(1024).decode()
                        for i in users:
                            if i.usuario == user:
                                i.search_user(nombre_carpeta_cliente)
                except Exception as e:
                    print(e)
            
            elif data_server == "3":
                try:
                    mensaje = conn.recv(1024).decode()
                    split = mensaje.split(",")
                    user,user_passwd = split
                    resultado = bd.consulta_usuario(user,user_passwd)

                    if resultado:
                        conn.send(str(resultado).encode())
                        carpeta_borrar_cliente = conn.recv(1024).decode()
                        if (Path("{}{}/{}".format(dir_usu,user,carpeta_borrar_cliente))):
                            for i in users:
                                if i.usuario == user:
                                    i.borrar_carpeta(carpeta_borrar_cliente)
                except Exception as e:
                    print(e)

            elif data_server == "4":
                try:
                    mensaje = conn.recv(1024).decode()
                    split = mensaje.split(",")
                    user,user_passwd = split
                    resultado = bd.consulta_usuario(user,user_passwd)
                    if resultado:
                        conn.send(str(resultado).encode())
                        archivos_cliente = os.listdir("./usuarios/"+user+"/archivos_cliente/")
                        mensaje = "{},{}".format(archivos_cliente[0],archivos_cliente[1])
                        conn.send(mensaje.encode())
                        archivo_push_cliente = conn.recv(1024).decode()
                        if os.path.isfile("./usuarios/"+user+"/"+"archivos_cliente"+"/"+archivo_push_cliente):
                            cp("./usuarios/"+user+"/"+"archivos_cliente"+"/"+archivo_push_cliente,"./documentos_cliente/")
                            logging.info("El usuario {} ha subido el archivo '{}' el {}".format(user,archivo_push_cliente,time.asctime(time.localtime())))
                        else:
                            print("El archivo no existe")

                except Exception as e:
                    print(e)

            elif data_server == "5":
                try:
                    mensaje = conn.recv(1024).decode()
                    split = mensaje.split(",")
                    user,user_passwd = split
                    resultado = bd.consulta_usuario(user,user_passwd)

                    if resultado:
                        conn.send(str(resultado).encode())
                        archivos_server = os.listdir("./archivos_server")
                        mensage_lista = "{},{}".format(archivos_server[0],archivos_server[1])
                        conn.send(mensage_lista.encode())
                        archivo_descarga_cliente = conn.recv(1024).decode()
                        if os.path.isfile(dir_archivo_server+archivo_descarga_cliente):
                            cp(dir_archivo_server+archivo_descarga_cliente,dir_usu+user+"/documentos")
                            logging.info("El usuario {} ha descargado el archivo '{}' el {}".format(user,archivo_descarga_cliente,time.asctime(time.localtime())))

                    else:
                        print("Mal mal ")

                except Exception as e:
                    print(e)    
                
                

                
                    
                

            
            










        
                    
    
            
