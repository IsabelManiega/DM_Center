import psycopg2
from connection import connect
from fastapi import FastAPI, status, Response

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
        
