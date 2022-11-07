	DM_Center (Data Management Center)
----------------------------------

1. Objetivo
-----------

Es una aplicación creada con Python 3.8.10 para la gestión de los datos mediante el empleo de una API Rest creada a partir del Framework de Python FastAPI.

2. Funcionalidad Etiqueta "Empleados"
------------------

Creados distintos métodos para la gestión de los datos:

* [GET] http://localhost:8000/

Muestra mensaje de bienvenida.

* [GET] http://localhost:8000/getData/

Muestra la información relativa a todos los usuarios registrados en la aplicación.

* [GET] http://127.0.0.1:8000/getData/3

Muestra la información relativa a un usuario registrados en la aplicación.

* [POST] http://127.0.0.1:8000/insertExemple/

Inserta la información relativa a varios usuarios como modo de ejemplo en la aplicación.

* [POST] http://127.0.0.1:8000/postData/

Inserta la información relativa a un usuario en la aplicación.

* [PUT] http://127.0.0.1:8000/putData/1

Actualizar la información relativa a un usuario en la aplicación.

* [DELETE] http://127.0.0.1:8000/deleteData/1

Elimina la información relativa a un usuario en la aplicación.

* [DELETE] http://127.0.0.1:8000/deleteData/

Elimina la información relativa a todos usuarios en la aplicación.

* [POST] http://127.0.0.1:8000/Filtrar/{edad1}@{edad2}

Devuelve la información relativa de la colección de empleados, que se encuentre entre las dos fechas pasadas por parámetros.


3. Funcionalidad Etiqueta "FINANZAS"
Creados distintos métodos para la gestión en MONGO, y la comunicación de con la base de datos y la colección de las cotizaciones:
Se utiliza el fichero Settings.py, para informar los parámetro de conexión a la base de datos y las colecciones. Este fichero se tiene que actualizar en cada una de las instalaciones que se realice.
    La variable DATABASE se debe informar con el nombre de la base de datos
	La variable COLECTION_1 se debe informar con la colección utilizada para las cotizaciones. 
	La variable COLECTION_2 se debe informar con la colección utilizada para los empleados. 

Se utiliza el fichero connection.py para realizar la conexión a la base de datos de mongo, a través de la librería pymongo.
Dentro del fichero CRUD.py, se implementan las funciones que realizan las consultas, inserciones y actualizaciones en la colección de cotizaciones.

* [POST] http://localhost:8000/post/insertYFinance/

Inserta en la colección de cotizaciones los datos de las cotizaciones recuperadas a través de la librería Yfinance, entre las fechas "2015-1-1", "2018-12-31".
Los campos de la coleccion son 'Date','Open', 'High', 'Low', 'Close', 'Volume'
Utiliza la función insertDocument del fichero CRUD.py, para la recopilación de datos de las cotizaciones y la inserción en la colección de cotizaciones.


* [GET] http://localhost:8000/get/GetDescribe/

Devuelve el describe de la colección de cotizciones. Utilizando la librería Dask, para el tratamiento de los datos del dataframe.
utiliza la función mostrar_describe del fichero CRUD.py, para realizar el acceso a la colección de cotizaciones y devolver el describe de los datos insertados en la colección.

* [GET] http://localhost:8000/get/GETDATE/{fecha}

Devuelve los datos de la colección de cotizaciones que coincidan con la fecha pasada por parámetro.
utiliza la función mostrar_datos_coleccion_fecha del fichero CRUD.py, para realizar el acceso a la colección y devolver los datos que coincidan con la fecha pasada por parámetro.

* [GET] http://localhost:8000/get/GETbetweenDATE/{fecha1},{fecha2}

Devuelve los datos de la colección de cotizaciones que se encuentren entre las dos fechas pasada por parémetros.
utiliza la función getbetweendates del fichero CRUD.py, para realizar el acceso a la colección y devolver los datos entre las dos fecha pasadas por parámetro.

* [GET] http://localhost:8000/GETall/

Devuelve todos los datos de la colección de cotizaciones, sin ningún filtro

* [DELETE] http://localhost:8000/DELETE/insertYFinance/{fecha}

Elimina el registro de la colección de cotizaciones que coincida con la fecha pasada por parámetro.


4. Ejecutar Aplicación
----------------------

Crear entorno virtual en la carpeta que queramos:

py -m venv env

Activar entorno virtual:

env\Scripts\activate

Instalar las librerias de requirements.txt:

pip install -r requirements.txt

Ejecutar fastapi:

uvicorn main:app --reload


5. Estructura del proyecto
--------------------------

El proyecto consta de:
* Una rama **main** para los desarrollos definitivos.
* Una rama **develop_sql** para los desarrollos con conexión a base de datos de tipo SQL, como es PostgreSQL.
* Una rama **develop_mongo** para los desarrollos con conexión a base de datos de tipo NoSQL, como es MongoDB.