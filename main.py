# Crear una Api rest
from fastapi import FastAPI, status, Response
from models import Empleado
from connection import connect

import pandas as pd
import yfinance as yf
from CRUD import crud

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
    {
        "name": "Cotización Google",
        "description": "Muestra los datos capturados de YFinance",
    },
]
nombres = "Belen Aristizabal, Jessenia Gutierrez, Rosana Longares, "
nombres += "Adrián Mencias, María Mendoza, Luis Vallejo"
nombres += "Cristina Lendinez, Etty Guerra, Francisco Javier Florido"
nombres += "Javier López, Jerónimo Guitierrez, Carlos Javier Cuenca"

app = FastAPI(title="Base de datos Empleados Fei y Base de datos cotización Google YFinance",
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
        del fila["_id"]
        lista_empleados.append(fila)
    return lista_empleados
        

# Mostrar un dato listado: GET
@app.get("/getData/{numero_empleado}", status_code=status.HTTP_200_OK, tags=["Empleados"],
         description="Mostrar un empleado")
async def showOne(numero_empleado: int, response: Response):
    try:
        empleado = db.Empleados.find_one({"numero_empleado": numero_empleado})
        empleado["_id"] = str(empleado["_id"])
        return empleado
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"numero_empleado": numero_empleado, "msg":"Empleado Not Found"}

# Insertar ejemplos: many
@app.post("/insertExemple/", status_code=status.HTTP_200_OK, tags=["Empleados"],
         description="Crea usuarios para testear")
async def insertManyEx(response: Response):
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
    db.Empleados.insert_one(item.dict())
    return item

# Actualizar un dato del listado: PUT
@app.put("/putData/{numero_empleado}", tags=["Empleados"],
         description="Actualizar empleado")
async def update(item: Empleado, numero_empleado: int, response: Response):
    try:
        empleado = db.Empleados.find_one({"numero_empleado": numero_empleado})
        dict=item.dict()
        for k,v in dict.items():
            db.Empleados.update_one({"_id":empleado["_id"]},{"$set":{k:v}})
        response.status_code = status.HTTP_200_OK
        return item
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"id": numero_empleado, "msg":"Empleado Not Found"}

# Eliminar un dato: Delete
@app.delete("/deleteData/{numero_empleado}", tags=["Empleados"],
            description="Eliminar un usuario")
async def deleteOne(numero_empleado: int, response: Response):
    try:
        empleado = db.Empleados.find_one({"numero_empleado": numero_empleado})
        db.Empleados.delete_one({"_id":empleado["_id"]})
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"numero_empleado": numero_empleado, "msg": "Eliminado"}
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"id": numero_empleado, "msg":"Empleado Not Found"}

#Eliminar todos los datos: Delete
@app.delete("/deleteData/", tags=["Empleados"],
            description="Eliminar todos los empleados")
 
async def delete(response: Response):
    db.Empleados.delete_many({})
    response.status_code = status.HTTP_200_OK
    return {"msg": []}


#####################################################################################
#                   GESTION DE BBDD DE COTIZACION DE GOOGLE                       
#
#####################################################################################
# POST BBDD YFinance
@app.post("/insertYFinance/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="Carga cotización Google de YFinance")
async def post(response: Response):
    
    nombredb="DBGoogle"
    coleccion="Yfinance"
    num_registros= crud.insertDocument(nombredb, coleccion)
    if num_registros != 0:
        response.status_code = status.HTTP_200_OK
        return "Tabla Creada y datos YFinance cargados"
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"msg": "No existen registros a cargar en la tabla"}

# Mostrar el listado: GET
@app.get("/GetDescribe/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="Muestra el describe de finanzas")
async def Muestra_describe():
    nombredb="DBGoogle"
    coleccion="Yfinance"
    dic1 = crud.mostrar_describe(nombredb, coleccion)
    return dic1