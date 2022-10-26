from datetime import date
import psycopg2 
from psycopg2 import sql 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import settings
from connection import connect
from fastapi import status

class crud:
    def createDatabase():
        conn = psycopg2.connect(user=settings.USER,
                                password=settings.PASSWORD,
                                host=settings.HOST,
                                port=settings.PORT)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        try:
            cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier("test")))
        except psycopg2.Error as e:
            return str(e)

        cur.close()
        conn.close()
        
    def createTablaNotas():
        # Conexión a base de datos PostgreSQL
        cur, conn = connect()
        try:
            query = "CREATE TABLE notas"
            query += "(Id SERIAL PRIMARY KEY, "
            query += "Nombre varchar(80), "
            query += "Edad int," 
            query += "Notas real," 
            query += "Fecha date);"
            cur.execute(query)
        except psycopg2.Error as e:
            return str(e)

        conn.commit()
        cur.close()
        conn.close()

    def mostrar(tabla, column, valor, response):
        # Conexión a base de datos PostgreSQL
        cur, conn = connect()
        datos={}

        # Generamos y ejecutamos la query
        try:
            query = f"SELECT * FROM {tabla} WHERE {column} = {valor};"
            cur.execute(query)
            rows = cur.fetchall()
            if rows == []:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"id":valor , f"msg":"User Not Found"}
            else:
                datos["Id"]=rows[0][0]
                datos["Nombre"]=rows[0][1]
                datos["Edad"]=rows[0][2]
                datos["Nota"]=rows[0][3]
                datos["Fecha"]=rows[0][4]                
                response.status_code = status.HTTP_200_OK
                cur.close()
                conn.close()
                return datos

        except psycopg2.Error as e:
            error = "Error mostrar registros: %s" + str(e)
            cur.close()
            conn.close()  
            return {f"msg":error}
