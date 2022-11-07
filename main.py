# Crear una Api rest
import psycopg2
from fastapi import FastAPI, status, Response
from models import User
from connection import connect
# from mostrardatostabla import mostrar
from CRUD import crud
import quandl
import yfinance as yf
import dask.dataframe as dd
import datetime
import pandas as pd

crud.createDatabase()
crud.createTablaNotas()
crud.createTablaAmazon()

tags_metadata=[
    {
        "name": "TEST",
        "description": "Bienvenida",
    },
    {
        "name": "Notas",
        "description": "Muestra la gestión de la tabla Notas",
    },
    {
        "name": "FINANZAS",
        "description": "Muestra datos financieros de Amazon"
    }
]
nombres = "Jerónimo Guitierrez, Francisco Javier Florido, Cristina Lendinez, "
nombres += "Javier López, Etty Guerra, Carlos Javier Cuenca, Jessenia Gutierrez Nagua,\
            Adrian Mencias Del Olmo, Luis Vallejo Carretero, María Belen Aristizabal,\
            Rosana Longares Herrero, María Mendoza"

app = FastAPI(title="BBDD Test",
              openapi_tags=tags_metadata,
              contact={"name": nombres},
              openapi_url="/api/v0.1/openapi.json")

@app.post("/insertar/", status_code=status.HTTP_201_CREATED, tags=["Notas"],
          description="Insertar datos de prueba")
async def Insertar_datos_prueba():
    try:
        cur, conn = connect()
        cur.execute("INSERT INTO notas VALUES(default, %s, %s, %s, %s);", ('Ana',20,7.5,'2022-10-20'))
        cur.execute("INSERT INTO notas VALUES(default, %s, %s, %s, %s);", ('Juan',21,8.5,'2022-10-21'))
        cur.execute("INSERT INTO notas VALUES(default, %s, %s, %s, %s);", ('Luisa',22,9.5,'2022-10-22'))
        cur.execute("INSERT INTO notas VALUES(default, %s, %s, %s, %s);", ('Pedro',23,3.5,'2022-10-23'))
        cur.execute("INSERT INTO notas VALUES(default, %s, %s, %s, %s);", ('Laura',24,10.0,'2022-10-24'))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        #return ("Error insertar registros: %s" % str(e))
        return {f"msg":"Error al insertar registros: %s" % str(e) }
    finally:
        cur.close()
        conn.close()
        return ("insertados 5 registros en la tabla notas")

@app.get("/", tags=["TEST"], description="Mostrar la información de la WEB")
async def info():
    return {"msg": "Bienvenido a nuestra Api Rest"}

# Mostrar el listado: GET
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["Notas"],
         description="Mostrar todos los registros")
async def show():
    try:
        datos_return=[]
        datos={}
        cur, conn = connect()
        cur.execute("SELECT * FROM notas;")
        rows = cur.fetchall()
        for row in rows:
            datos["Id"]=row[0]
            datos["Nombre"]=row[1]
            datos["Edad"]=row[2]
            datos["Nota"]=row[3]
            datos["Fecha"]=row[4]
            datos_return.append(datos)
            datos={}
    except psycopg2.Error as e:
         return {f"msg":"Error al insertar registros: %s" % str(e) }
    finally:
        cur.close()
        conn.close()
        return datos_return


# Mostrar un dato listado: GET ID
@app.get("/getData/{item_id}", status_code=status.HTTP_200_OK, tags=["Notas"],
         description="Mostrar los datos de un registro")
async def showOne(id_buscar: int, response: Response):
    
    return crud.mostrar("notas", "id", id_buscar, response)

#  Insertar un dato en es listado: POST
@app.post("/postData/", status_code=status.HTTP_201_CREATED, tags=["Notas"],
          description="Insertar un registro")
async def insert(item: User, response: Response):
     
    cur, conn = connect()
    try:
        cur.execute(f"INSERT INTO notas (Nombre, Edad, Notas, Fecha) VALUES('{item.Nombre}', {item.Edad}, {item.Notas}, '{item.Fecha}');")
        
        conn.commit()   
        cur.close()
        conn.close()
        
        return {"msg": ["Se han insertado los datos correctamente"]}
    except psycopg2.Error as e:
        response.status_code=status.HTTP_404_NOT_FOUND
        print("Error actualizar registro: %s" % str(e))
        conn.rollback()
        cur.close()
        conn.close()
        print(f'Se han añadido los datos correctamente. registros borrados {cur.rowcount}')
        return "Error registro: %s" % str(e)
   
    
    
# Actualizar un dato del listado: PUT
@app.put("/putData/{id}", status_code=status.HTTP_200_OK, tags=["Notas"],
         description="Actualizar un registro")
async def update(id: int, item: User, response: Response):

    cur, conn = connect()
    try:
        cur.execute(f"UPDATE notas SET Nombre='{item.Nombre}'  WHERE Id={id};")
    except psycopg2.Error as e:
        print("Error actualizar registro: %s" % str(e))
        conn.rollback()
        print(f'Se han añadido los datos correctamente. registros borrados {cur.rowcount}')
        
    conn.commit()   
    cur.close()
    conn.close()
    response.status_code = status.HTTP_200_OK
    return {"msg": ["Se han actualizado los datos correctamente"]}
    

# Eliminar un dato: Delete
@app.delete("/deleteData/{item_id}", status_code=status.HTTP_200_OK, tags=["Notas"],
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
            cur.close()
            conn.close()
            return "Error Eliminando registro: %s" % str(e)

        # Actualizamos y cerramos la base de datos
        cur.close()
        conn.close()

        response.status_code = status.HTTP_200_OK
        return {"msg": ["Se ha elimindo el dato correctamente"]}

@app.delete("/deleteData/", tags=["Notas"],
            description="Eliminar todos los registros")

async def delete(response: Response):
# Conexión a base de datos PostgreSQL
    cur, conn = connect()

    try:
        cur.execute("DELETE FROM notas;")
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return "Error al borrar la tabla: %s" % str(e)
        
    cur.close()
    conn.close()
    response.status_code = status.HTTP_200_OK
    return {"msg": ["Se han eliminado los datos correctamente"]}

# GET/notasbetween: Adrian
@app.get("/getNotaBetween/{nota1},{nota2}", status_code=status.HTTP_200_OK, tags=["Notas"],
            description="Mostrar las notas entre nota1 y nota2")
async def show_between(nota1:float, nota2:float):
    try:
        datos_return=[]
        datos={}
        cur, conn = connect()
        if nota1 > nota2:
            return "msg: Error al mostrar datos: Nota1 debe ser menor que Nota2"
        cur.execute(f"SELECT * FROM notas WHERE notas BETWEEN {nota1} AND {nota2};")
        rows = cur.fetchall()
        for row in rows:
            datos["Id"]=row[0]
            datos["Nombre"]=row[1]
            datos["Edad"]=row[2]
            datos["Nota"]=row[3]
            datos["Fecha"]=row[4]
            datos_return.append(datos)
            datos={}
        return datos_return
    except psycopg2.Error as e:
         return {f"msg":"Error al mostrar registros: %s" % str(e) }
    finally:
        cur.close()
        conn.close()
        


    #__________________________ Actividad Suplementaria _______________________________

""" 
    Rosana --> GET/fechas
    Luis --> POST quandl/yfinance
    Adrian --> POST filtrado
    Jessenia --> GET
    Fernanda --> GET/describe
    Belen --> DELETE (id) 
"""

@app.get("/Finanzas/", tags=["FINANZAS"], description="Información de la WEB: WIKI/AMZN")
async def bienvenida():
    description = """ Bienvenido a nuestra Api Rest del Mercado Global:
    En la parte anterior añadir:
        POST: añadir el filtrado de un determinado dato.
    
    Añadir al Backend una conexión a quandl/yfinance y realizar:
        POST: realizar una petición por fecha a quandl/yfinance e insertar en base de datos.
        GET: muestra los datos que hay en base de datos.
        GET/Fechas: mostrar los datos por fechas concretas.
        GET/describe: realizar una petición a la base de datos, crear un dataframe con dask y responder con el describe.
        DELETE/ID: Elimina un dato concreto de la base de datos.
    
     """
    return description
    # return {"msg": "Bienvenido a nuestra Api Rest del Mercado Global"}

# GET/fechas: Rosana
@app.get("/getFechas/{date}", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="GET/Fechas: mostrar los datos por fechas concretas.")
async def get_Fechas(date:str, response: Response):

    # Conexión a base de datos PostgreSQL
    cur, conn = connect()
    datos={}

    try:        
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        cur.execute(f"SELECT * FROM amazon WHERE date = '{date}';")
        row = cur.fetchall() 
        if row == []:
            response.status_code=status.HTTP_404_NOT_FOUND
            # Actualizamos y cerramos la base de datos
            cur.close()
            conn.close()
            return "Error mostrando datos por fecha"
            
        print(row)       
        datos["Date"]=row[0][0]
        datos["Open"]=row[0][1]
        datos["High"]=row[0][2]
        datos["Low"]=row[0][3]
        datos["Close"]=row[0][4]
        datos["Volume"]=row[0][5]
            
        cur.close()
        conn.close()
        return datos
        
        return row
    except psycopg2.Error as e:
        response.status_code=status.HTTP_404_NOT_FOUND

        # Actualizamos y cerramos la base de datos
        cur.close()
        conn.close()
        
        return "Error mostrando datos por fecha: %s" % str(e)
   

# POST quandl/yfinance: Luis
@app.post("/postAmazon/{fecha_inicio},{fecha_fin}", status_code=status.HTTP_201_CREATED, tags=["FINANZAS"],
          description="POST: realizar una petición por fecha a quandl/yfinance e insertar en base de datos.")
async def postAmzn(fecha_inicio:datetime.date,fecha_fin:datetime.date, response:Response):
    print("Principio función")
    cur, conn = connect()
    if fecha_inicio > fecha_fin: return "Error: Fechas incorrectas"
    try:
        data = quandl.get("WIKI/AMZN", start_date=fecha_inicio, end_date=fecha_fin)
        print("Datos insertados con Quandl")
    except:
        data = yf.download("AMZN", fecha_inicio, fecha_fin)
        print("Datos insertados con Yahoo Finance")

    data = data[["Open","High","Low","Close","Volume"]]
    try:
        print("Borrando datos anteriores")
        cur.execute("DELETE FROM amazon;")
        print("Datos borrados")
        
        print(data.head())
        for index, row in data.iterrows():
            query = "INSERT INTO amazon (date, open, high, low, close, volume) "
            op = float(row["Open"])
            hi = float(row["High"])
            low = float(row["Low"])
            cl = float(row["Close"])
            vol = float (row["Volume"])
            query += "VALUES('{0}', {1}, {2}, {3}, {4}, {5});".format(index,op,hi,low,cl,vol)
            cur.execute(query)
            conn.commit()
        cur.close()
        conn.close()
        return "Datos insertados en la base de datos"
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        return "Error al insertar los datos {0}".format(e)

    

# GET: Jessenia
@app.get("/getAmazon/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="GET: muestra los datos que hay en base de datos.")
async def showAmazon():
    try:
        lista_datos=[]
        datos={}
        cur, conn = connect()
        cur.execute("SELECT * FROM amazon;")
        rows = cur.fetchall()
        for row in rows:
            datos["Date"]=row[0]
            datos["Open"]=row[1]
            datos["High"]=row[2]
            datos["Low"]=row[3]
            datos["Close"]=row[4]
            datos["Volume"]=row[5]
            lista_datos.append(datos)
            datos={}
    except psycopg2.Error as e:
         return {f"msg":"Error al mostrar registros: %s" % str(e) }
    finally:
        cur.close()
        conn.close()
        return lista_datos

# GET/describe/mostar: Fernanda
@app.get("/getDescribe/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="GET/describe: realizar una petición a la base de datos, crear un dataframe con dask y responder con el describe.")
async def get_describe(response: Response):
    
    cur, conn = connect()
    try:
        df = pd.read_sql('SELECT * FROM amazon', conn)
        # print(df)
        ddf = dd.from_pandas(df, npartitions=3)
        # print(ddf.compute())
        ddf_describe = ddf.describe().compute()
        # print(ddf_describe)
        response.status_code=status.HTTP_200_OK
        return ddf_describe        
    except Exception as e:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {f"msg":"Error al mostrar data frame: %s" % str(e) }
    finally:
        cur.close()
        conn.close()
        

# DELETE (id): Belen 
@app.delete("/deleteamazon/{date}", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
            description="DELETE/ID: Elimina una fecha concreta de la base de datos.")
async def delete_date(date: str, response: Response):
    # Conexión a base de datos PostgreSQL
    cur, conn = connect()
    # Generamos y ejecutamos la query
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d' )
        query = f"DELETE FROM amazon WHERE Date = '{date}';"
        output = cur.execute(query)
        if output == None:
            response.status_code=status.HTTP_404_NOT_FOUND
            return "Registro no encontrado"
        conn.commit()
    except psycopg2.Error as e:
        response.status_code=status.HTTP_404_NOT_FOUND
        cur.close()
        conn.close()
        return "Error Eliminando registro: %s" % str(e)

        # Actualizamos y cerramos la base de datos
    cur.close()
    conn.close()

    response.status_code = status.HTTP_200_OK
    return {"msg": ["Se ha elimindo la fecha correctamente"]}
    
    