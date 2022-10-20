# Crear una Api rest
from fastapi import FastAPI, status, Response
from models import User
from connection import connect

# Conexión a base de datos PostgreSQL
cur, conn = connect()

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
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["Users"],
         description="Mostrar todos los usuarios")
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


# Mostrar un dato listado: GET
@app.get("/getData/{item_id}", status_code=status.HTTP_200_OK, tags=["Users"],
         description="Mostrar un usuario")
async def showOne(id: int, response: Response):
    for i in range(0,len(database)):
        if database[i]["id"] == id:
            response.status_code = status.HTTP_200_OK
            return database[i]
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"id": id, "msg":"User Not Found"}

#  Insertar un dato en es listado: POST
@app.post("/postData/", status_code=status.HTTP_201_CREATED, tags=["Users"],
          description="Insertar un usuario")
async def insert(item: User):
    database.append(item.dict())
    return item

# Actualizar un dato del listado: PUT
@app.put("/putData/{id}", status_code=status.HTTP_200_OK, tags=["Users"],
         description="Actualizar un usuario")
async def update(id: int, item: User, response: Response):
    for i in range(0,len(database)):
        if database[i]["id"] == id:
            database[i] = item.dict()
            response.status_code = status.HTTP_200_OK
            return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"id": id, "msg":"User Not Found"}

# Eliminar un dato: Delete
@app.delete("/deleteData/{id}", tags=["Users"],
            description="Eliminar un usuario")
async def deleteOne(id: int, response: Response):
    for value in database:
        if value["id"] == id:
            database.remove(value)
            response.status_code = status.HTTP_204_NO_CONTENT
            return {"item_id": id, "msg": "Eliminado"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"id": id, "msg":"User Not Found"}

@app.delete("/deleteData/", tags=["Users"],
            description="Eliminar todos usuario")
async def delete(response: Response):
    database.clear()
    response.status_code = status.HTTP_200_OK
    return {"msg": []}

conn.commit()

cur.close()
conn.close()
