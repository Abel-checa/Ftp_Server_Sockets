import mysql.connector
import logging
import time
logging.basicConfig(filename="./errores/log.txt",level= logging.INFO)

def conexion_sql(users):
    try:
        conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "abel",
        )

        cursor = conexion.cursor()
        cursor.execute("drop database if exists User")
        cursor.execute("create database User")
        cursor.execute("USE User")
        cursor.execute("CREATE TABLE Usuarios" 
        "(id INT AUTO_INCREMENT,"
        "nombre VARCHAR (32) NOT NULL,"
        "passwd VARCHAR (256),"
        "PRIMARY KEY (id));")
        
        for i in users:
            usuario = "{}".format(i.usuario)
            contr = "{}".format(i.passwd)
            print(usuario,contr)
            consulta = "INSERT INTO USUARIOS (nombre,passwd) VALUES ('{}','{}')".format(usuario,contr)
            cursor.execute(consulta)
            conexion.commit()
            logging.info("El usuario {} se ha autenticado en la base de datos el {}".format(i.usuario,time.asctime(time.localtime())))  
    except Exception as e:
        print(e)


def consulta_usuario(usuario,passwd):
    try:
        conexion = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "abel",
        )

        cursor = conexion.cursor()
        cursor.execute("USE User")
        cursor.execute("select nombre,passwd from usuarios where nombre = '{}' and passwd = '{}'".format(usuario,passwd))
        resultado = cursor.fetchall()
        if len(resultado) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)

