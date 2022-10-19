import pymongo
import settings

def connect():
    cliente = pymongo.MongoClient(settings.HOST, settings.PORT)
    
    db = cliente.EmpleadosFei
    return db