from datetime import date
import psycopg2 
from psycopg2 import sql 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import settings

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
conn.commit()
cur.close()
conn.close()