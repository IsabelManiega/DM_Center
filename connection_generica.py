import pymongo
import settings

def connect(nombredb):

    # # conexión a base de datos
    bbdd = pymongo.MongoClient(settings.HOST, settings.PORT)

    # # Si no existe la base de datos la crea con el nombre qye haya en nombredb
    db = bbdd[nombredb]

    return db