# Crear una Api rest
import psycopg2
from fastapi import FastAPI, status, Response
from models import User
from connection import connect

# Funciones
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
            print("Error mostrar registros: %s" % str(e))

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

tags_metadata=[
    {
        "name": "TEST",
        "description": "Bienvenida",
    },
    {
        "name": "Users",
        "description": "Muestra los gestión de los usuarios",
    },
]

app = FastAPI(title="DataScience Course",
              openapi_tags=tags_metadata,
              contact={"name": "Isabel Maniega",
                       "url": "https://es.linkedin.com/in/isabel-maniega-cuadrado-40a8356b",
                       "email": "isabelmaniega@hotmail.com",
                },
              openapi_url="/api/v0.1/openapi.json")



@app.get("/", tags=["TEST"], description="Mostrar la información de la WEB")
async def info():
    return {"msg": "Bienvenido a nuestra Api Rest"}

# Mostrar el listado: GET
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["TERMINADOS"],
         description="Mostrar todos los registros")
async def show():
    try:
        datos=[]
        cur, conn = connect()
        cur.execute("SELECT * FROM notas;")
        rows = cur.fetchall()
        for row in rows:
            datos.append(row)
    except psycopg2.Error as e:
        return "Error mostrar registros: %s" % str(e)
    finally:
        cur.close()
        conn.close()
        return datos


# Mostrar un dato listado: GET ID - CARLOS
@app.get("/getData/{item_id}", status_code=status.HTTP_200_OK, tags=["TERMINADOS"],
         description="Mostrar los datos de un registro")
async def showOne(id_buscar: int, response: Response):
    
    return mostrar("notas", "id", id_buscar, response)

#  Insertar un dato en es listado: POST
@app.post("/postData/", status_code=status.HTTP_201_CREATED, tags=["PENDIENTES"],
          description="Insertar un registro")
async def insert(item: User):
    database.append(item.dict())
    return item

# Actualizar un dato del listado: PUT
@app.put("/putData/{id}", status_code=status.HTTP_200_OK, tags=["PENDIENTES"],
         description="Actualizar un registro")
async def update(id: int, item: User, response: Response):
    for i in range(0,len(database)):
        if database[i]["id"] == id:
            database[i] = item.dict()
            response.status_code = status.HTTP_200_OK
            return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"id": id, "msg":"User Not Found"}

# Eliminar un dato: Delete
@app.delete("/deleteData/{item_id}", status_code=status.HTTP_200_OK, tags=["TERMINADOS"],
            description="Eliminar un usuario")
async def deleteOne(id: int, response: Response):
     # Conexión a base de datos PostgreSQL
        cur, conn = connect()

        # Generamos y ejecutamos la query
        try:
            query = f"DELETE FROM notas WHERE Id = {id};"
            cur.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            response.status_code=status.HTTP_404_NOT_FOUND
            conn.rollback()
            print("Error Eliminando registro: %s" % str(e))

        # Actualizamos y cerramos la base de datos
        cur.close()
        conn.close()

        response.status_code = status.HTTP_200_OK
        return {"msg": ["Se ha elimindo el dato correctamente"]}

@app.delete("/deleteData/", tags=["TERMINADOS"],
            description="Eliminar todos los registros")

async def delete(response: Response):
    try:
        cur, conn = connect()
        cur.execute("DELETE FROM notas;")
        conn.commit()
        print(f'Se ha elimindo los datos correctamente. registros borrados {cur.rowcount}')
    except psycopg2.Error as e:
        conn.rollback()
        return "Error al borrar la tablas: %s" % str(e)
        


    cur.close()
    conn.close()
    response.status_code = status.HTTP_200_OK
    return {"msg": ["Se ha elimindo los datos correctamente"]}


