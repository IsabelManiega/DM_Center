# Crear una Api rest
from fastapi import FastAPI, status, Response
from models import Empleado
from connection import connect

db = connect()

tags_metadata=[
    {
        "name": "TEST",
        "description": "Bienvenida",
    },
    {
        "name": "Empleados",
        "description": "Muestra los gestión de los empleados",
    },
]

app = FastAPI(title="Base de datos Empleados Fei",
              openapi_tags=tags_metadata,
              contact={"name": "Belen Aristizabal, Rosana Longares, Adrián Mencias, María Mendoza, Luis Vallejo"},
              openapi_url="/api/v0.1/openapi.json")



@app.get("/", tags=["TEST"], description="Mostrar la información de la WEB")
async def info():
    return {"msg": "Bienvenido a nuestra Api Rest"}

# Mostrar el listado: GET
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["Empleados"],
         description="Muestra todos los empleados")
async def show():
    empleados = db.Empleados.find({})
    lista_empleados = []
    for fila in empleados:
        dict_aux = {
            "numero_empleado": fila["numero_empleado"],
            "nombre": fila["nombre"],
            "edad": fila["edad"],
            "cargo": fila["cargo"],
            "departamento": fila["departamento"],
            "salario": fila["salario"]
        }
        lista_empleados.append(dict_aux)
    return lista_empleados
        

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
@app.delete("/deleteData/{numero_empleado}", tags=["Empleados"],
            description="Eliminar un usuario")
async def deleteOne(numero_empleado: int, response: Response):
    datos = db.Empleados.find({})
    for dato in datos:
        if dato["numero_empleado"] == numero_empleado:
            idMongo = dato["_id"]
            db.Empleados.delete_one({"_id": idMongo})
            response.status_code = status.HTTP_204_NO_CONTENT           
            return {"numero_empleado": numero_empleado, "msg": "Eliminado"}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"numero_empleado": numero_empleado, "msg":"Empleado Not Found"}

@app.delete("/deleteData/", tags=["Users"],
            description="Eliminar todos usuario")
async def delete(response: Response):
    database.clear()
    response.status_code = status.HTTP_200_OK
    return {"msg": []}
