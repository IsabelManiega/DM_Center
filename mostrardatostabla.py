import psycopg2
from connection import connect

def mostrar(tabla, column, valor, response):
        # Conexión a base de datos PostgreSQL
        cur, conn = connect()
        rows = []

        # Generamos y ejecutamos la query
        try:
            query = f"SELECT * FROM {tabla} WHERE {column} = {valor};"
            cur.execute(query)
            rows = cur.fetchall()
        except psycopg2.Error as e:
            error = "Error mostrar registros: %s" + str(e)
            return {f"msg":error}
        # Actualizamos y cerramos la base de datos
        conn.commit()
        cur.close()
        conn.close()

        # Solo necesario este control para controlar que devuelva valores vacios
        if rows == []:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"id":valor , f"msg":"User Not Found"}
        else:
            response.status_code = status.HTTP_200_OK
            return rows
