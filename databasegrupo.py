from datetime import date
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from models import User
from connection import connect

# Conexión a base de datos PostgreSQL
cur, conn = connect()

def createTablaNotas(cur):
    try:
        query = "CREATE TABLE notas"
        query += "(Id SERIAL PRIMARY KEY, "
        query += "Nombre varchar(80), "
        query += "Edad int," 
        query += "Notas real," 
        query += "Fecha date);"
        cur.execute(query)
    except psycopg2.Error as e:
        print("Error crear la tabla Notas: %s" % str(e))

createTablaNotas(cur)

cur.close()
conn.close()


def insertarNotas(cur, nombre:str, edad:int, notas:float, ID:int, fecha:fecha):
    try:
        cur.execute(f"INSERT INTO Notas (nombre, edad, notas, ID, fecha) VALUES('{nombre}', {edad}, {notas}, {ID}, {fecha});")
    except psycopg2.Error as e:
        print("Error crear registro: %s" % str(e))

def insertNotas(cur, notas):
    for nota in notas:
        insertarNotas(cur, nota['nombre'], nota['edad'], nota['notas'], nota['ID'])