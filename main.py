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

crud.createDatabase()
crud.createTablaNotas()
crud.createTablaAmazon()


tags_metadata=[
    {
        "name": "TEST",
        "description": "Bienvenida",
    },
    {
        "name": "Test",
        "description": "Muestra la gestión de la tabla Notas",
    },
    {
        "name": "PENDIENTES",
        "description":" ",
    },
    {
        "name": "TERMINADOS",
        "description":" ",
    },
    {
        "name": "FINANZAS",
        "description": "Muestra datos financieros de Amazon"
    }
]
nombres = "Jerónimo Guitierrez, Francisco Javier Florido, Cristina Lendinez, "
nombres += "Javier López, Etty Guerra, Carlos Javier Cuenca, Jessenia Gutierrez Nagua, Adrian Mencias Del Olmo, Luis Vallejo Carretero, María Belen Aristizabal, Rosana Longares Herrero, María Mendoza"

app = FastAPI(title="BBDD Test",
              openapi_tags=tags_metadata,
              contact={"name": nombres},
              openapi_url="/api/v0.1/openapi.json")

@app.post("/insertar/", status_code=status.HTTP_201_CREATED, tags=["Datos de prueba"],
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
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["TERMINADOS"],
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
@app.get("/getData/{item_id}", status_code=status.HTTP_200_OK, tags=["TERMINADOS"],
         description="Mostrar los datos de un registro")
async def showOne(id_buscar: int, response: Response):
    
    return crud.mostrar("notas", "id", id_buscar, response)

#  Insertar un dato en es listado: POST
@app.post("/postData/", status_code=status.HTTP_201_CREATED, tags=["PENDIENTES"],
          description="Insertar un registro")
async def insert(item: User):
    # database.append(item.dict())
    return item

# Actualizar un dato del listado: PUT
@app.put("/putData/{id}", status_code=status.HTTP_200_OK, tags=["PENDIENTES"],
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
            cur.close()
            conn.close()
            return "Error Eliminando registro: %s" % str(e)

        # Actualizamos y cerramos la base de datos
        cur.close()
        conn.close()

        response.status_code = status.HTTP_200_OK
        return {"msg": ["Se ha elimindo el dato correctamente"]}

@app.delete("/deleteData/", tags=["TERMINADOS"],
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
@app.get("/getFechas/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="GET/Fechas: mostrar los datos por fechas concretas.")
async def get_Fechas():
    pass

# POST quandl/yfinance: Luis
@app.post("/insertar/", status_code=status.HTTP_201_CREATED, tags=["FINANZAS"],
          description="POST: realizar una petición por fecha a quandl/yfinance e insertar en base de datos.")
async def post_quandl_yfinance():
    pass


# GET: Jessenia
@app.get("/getData/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="GET: muestra los datos que hay en base de datos.")
async def get_data():
    pass

# GET/describe/mostar: Fernanda
@app.get("/getDescribe/", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
         description="GET/describe: realizar una petición a la base de datos, crear un dataframe con dask y responder con el describe.")
async def get_describe():
    
    cur, conn = connect()
     
    BBDD = 'notas'
    try:
        pass
    # Equivalent to:
    # SELECT * FROM chapterFour.violations  #https://livebook.manning.com/book/data-science-at-scale-with-python-and-dask/chapter-4/84 
    # df = dd.read_sql_table('BBDD', conn, npartitions=10, index_col='id') 
    # cur.execute("SELECT * FROM %s ;" %('BBDD'))
    # rows = cur.fetchall()
    # df_dask = dd.read_csv("yellow_tripdata.csv", asume_missing=True)
    # return df_dask.describe().compute()
    
    except psycopg2.Error as e:
        print("Error al mostrar data frame: %s" %str(e))

    conn.commit()

    cur.close()
    conn.close()

# DELETE (id): Belen 
@app.delete("/deleteData/{item_id}", status_code=status.HTTP_200_OK, tags=["FINANZAS"],
            description="DELETE/ID: Elimina un dato concreto de la base de datos.")
async def delete_Id(id: int, response: Response):
    pass