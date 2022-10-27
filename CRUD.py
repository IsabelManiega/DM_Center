import pymongo
import pandas as pd
import yfinance as yf
from connection_generica import connect


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

        # Lo convertimos en lista de diccionarios para cargarlo a la BBDD Mongo
        df_y_dic = df_y.to_dict('records')

        db = connect(nombredb)

        db[coleccion].insert_many(df_y_dic)

    def mostrar_datos_coleccion(nombredb, coleccion):
        # conexión a base de datos
        bbdd = pymongo.MongoClient("localhost", 27017)

        db = bbdd[nombredb]

        datos = db[coleccion].find({})
        for dato in datos:
            print(dato)