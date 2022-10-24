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
nombres = "Belen Aristizabal, Jessenia Gutierrez, Rosana Longares, "
nombres += "Adrián Mencias, María Mendoza, Luis Vallejo"
app = FastAPI(title="Base de datos Empleados Fei",
              openapi_tags=tags_metadata,
              
              contact={"name": nombres},
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
@app.get("/getData/{numero_empleado}", status_code=status.HTTP_200_OK, tags=["Empleados"],
         description="Mostrar un empleado")
async def showOne(numero_empleado: int, response: Response):
    empleados = db.Empleados.find({})
    for empleado in empleados:
        if empleado["numero_empleado"] == numero_empleado:
            idMongo = empleado["_id"]
            dict_aux = {
                "numero_empleado": empleado["numero_empleado"],
                "nombre": empleado["nombre"],
                "edad": empleado["edad"],
                "cargo": empleado["cargo"],
                "departamento": empleado["departamento"],
                "salario": empleado["salario"]
            }
            response.status_code = status.HTTP_200_OK
            return dict_aux
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"numero_empleado": numero_empleado, "msg":"Empleado Not Found"}

# Insertar ejemplos: many
@app.post("/insertExemple/", status_code=status.HTTP_200_OK, tags=["Empleados"],
         description="Crea usuarios para testear")
async def show(response: Response):
    dict_list = [
        {"numero_empleado": 1,"nombre": "Pedro López", "edad": 25, "cargo": "Gerente","departamento":"IT", "salario": 2000}, 
        {"numero_empleado": 2,"nombre": "Julia García", "edad": 22, "cargo": "CEO","departamento":"Administración", "salario": 5500},
        {"numero_empleado": 3,"nombre": "Amparo Mayoral", "edad": 28, "cargo": "Junior","departamento":"Programación", "salario": 1500},
        {"numero_empleado": 4,"nombre": "Juan Martinez", "edad": 30, "cargo": "Senior","departamento":"Arte", "salario": 2300}
    ]
    db.Empleados.insert_many(dict_list)
    response.status_code = status.HTTP_200_OK
    return "Ejemplos insertados"

#  Insertar un dato en es listado: POST
@app.post("/postData/", status_code=status.HTTP_201_CREATED, tags=["Empleados"],
          description="Insertar un Empleado")
async def insert(item: Empleado):
    db.Empleados.insert_one(item)
    return item

# Actualizar un dato del listado: PUT
@app.put("/putData/{numero_empleado}", tags=["Empleados"],
         description="Actualizar empleado")
async def update(item: Empleado, numero_empleado: int, response: Response):
    for dato in db.Empleados.find({}):
        if dato["numero_empleado"] == numero_empleado:
            idMongo=dato["_id"]    
            dict=item.dict()
            for k,v in dict.items():
                db.Empleados.update_one({"_id":idMongo},{"$set":{k:v}})
            response.status_code = status.HTTP_200_OK
            return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"id": numero_empleado, "msg":"Empleado Not Found"}

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

#Eliminar todos los datos: Delete
@app.delete("/deleteData/", tags=["Empleados"],
            description="Eliminar todos los empleados")
 
async def delete(response: Response):
    db.Empleados.delete_many({})
    response.status_code = status.HTTP_200_OK
    return {"msg": []}
