import pymongo
import pandas as pd
import yfinance as yf
from connection import connect
import dask.dataframe as dd
from datetime import datetime


class crud:
    def insertDocument(nombredb, coleccion):
        # IMPORTAMOS LOS DATOS DE Y FINANCE
        # Vamos a extraer las cotizaciones de Google en las mencionadas
        # Año 2015-2016-2017-2018
        # formato: Año-Mes-Día

        df_y = yf.download("GOOGL", "2015-1-1", "2018-12-31")
        
        # Sacamos el indice a una columna llamada Date
        df_y = df_y.rename_axis('Date').reset_index() 
        # Generamos el DataFrame con los campos que queremos tener   
        df_y = pd.DataFrame(df_y, columns = ['Date','Open', 'High', 'Low', 'Close', 'Volume'])
        num_registros = len(df_y)
        print(num_registros)
        if num_registros != 0:

            # Lo convertimos en lista de diccionarios para cargarlo a la BBDD Mongo
            df_y_dic = df_y.to_dict('records')

            db = connect(nombredb)

            db[coleccion].insert_many(df_y_dic)
        
        return num_registros

    def mostrar_datos_coleccion(nombredb, coleccion):
        # conexión a base de datos
        bbdd = pymongo.MongoClient("localhost", 27017)

        db = bbdd[nombredb]

        datos = db[coleccion].find({})
        for dato in datos:
            print(dato)

    def mostrar_describe(nombredb, coleccion):
        db = connect(nombredb)
        cotizaciones = db[coleccion].find({})
        lista_cotizaciones = []
        for fila in cotizaciones:
            del fila["_id"]
            lista_cotizaciones.append(fila)
        df_pandas = pd.DataFrame(lista_cotizaciones, columns=["Date","Open","High","Low","Close","Volume"])
        df_dask = dd.from_pandas(df_pandas,npartitions=1)
        df_dask = df_dask.describe().compute()
        print(df_dask)
        diccionario = df_dask.to_dict()
        print(diccionario)
        return diccionario
    
    
    def mostrar_datos_coleccion_fecha(nombredb, coleccion,fecha):
            # conexión a base de datos
            db = connect(nombredb)
            dato = db[coleccion].find_one({"Date": fecha})
            if type(dato)==dict:
                dato["_id"] = str(dato["_id"])
            return dato  
            
    def mostrar_datos_coleccion_entre_fechas(nombredb, coleccion,fecha1,fecha2):
        lista_datos=[]
        try:
                # conexión a base de datos
            db = connect(nombredb)
            datos = db[coleccion].find({"$and": [{"Date": {"$gte": fecha1}}, {"Date": {"$lte": fecha2}}]})
            for dato in datos:
                del dato["_id"]
                lista_datos.append(dato)
            return lista_datos
        except:            
            return {"Date": fecha1+fecha2, "msg":"Fechas Not Found"}



    

    def eliminar_registro(nombredb,coleccion,Fecha):
        try:
            db = connect(nombredb)
            fechalistado = datetime.strptime(Fecha, "%Y-%m-%d")
            Datos=db[coleccion].find_one({ "Date" : fechalistado})
            db[coleccion].delete_one({"_id":Datos["_id"]})
        
            return {"Fecha": Fecha, "msg": "El registro ha sido Eliminado"}
        except:
        
            return {"Fecha": Fecha, "msg":"Datos  No encontrado"}