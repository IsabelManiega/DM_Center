from datetime import date
import psycopg2 
from psycopg2 import sql 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import settings
from connection import connect

def createDatabase():
    conn = psycopg2.connect(user=settings.USER,
                            password=settings.PASSWORD,
                            host=settings.HOST,
                            port=settings.PORT)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    try:
        cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier("test")))
    except psycopg2.Error as e:
        return str(e)

    cur.close()
    conn.close()


