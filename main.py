# Crear una Api rest
from fastapi import FastAPI, status, Response
from models import User
from connection import connect

db = connect()

tags_metadata=[
    {
        "name": "TEST2",
        "description": "Bienvenida",
    },
    {
        "name": "Users",
        "description": "Muestra los gestión de los usuarios",
    },
]

app = FastAPI(title="DataScience Course",
              openapi_tags=tags_metadata,
              contact={"name": "Luis Vallejo", "María Mendoza"
                       "url": "https://es.linkedin.com/in/isabel-maniega-cuadrado-40a8356b",
                       "email": "isabelmaniega@hotmail.com",
                },
              openapi_url="/api/v0.1/openapi.json")

# Crear un listado:
database = [{"id": 1, "name": "Juan Perez", "age": 25, "profesion": "Ingeniero"},
            {"id": 2, "name": "Susana Ruiz", "age": 45, "profesion": "Profesora"}]

@app.get("/", tags=["TEST"], description="Mostrar la información de la WEB")
async def info():
    return {"msg": "Bienvenido a nuestra Api Rest"}

# Mostrar el listado: GET
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["Users"],
         description="Mostrar todos los usuarios")
async def show():
    return database

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
