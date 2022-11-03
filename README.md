DM_Center (Data Management Center)
----------------------------------

1. Objetivo
-----------

Es una aplicación creada con Python 3.8.10 para la gestión de los datos mediante el empleo de una API Rest creada apartir del Framework de Python FastAPI.

2. Funcionalidad
----------------

----------- Gestión de la tabla notas ------------

Creados distintos métodos para la gestión de la tabla notas:

* [GET] http://localhost:8000/getData/

Muestra la información relativa a todos los usuarios registrados en la aplicación.

* [GET] http://localhost:8000/getData/id

Muestra la información relativa a un usuario registrados en la aplicación.

* [POST] http://localhost:8000/postData/

Inserta la información relativa a un usuario en la aplicación.

* [PUT] http://localhost:8000/putData/id

Actualizar la información relativa a un usuario en la aplicación.

* [DELETE] http://localhost:8000/deleteData/id

Elimina la información relativa a un usuario en la aplicación.

* [DELETE] http://localhost:8000/deleteData/

Elimina la información relativa a todos usuarios en la aplicación.



----------- Gestión de datos financieros en la tabla Amazon ------------

Creados distintos métodos para la creación y gestión de la tabla Amazon:

* [GET] http://localhost:8000/Finanzas/

Muestra la descripción de la tabla amazon y sus funcionalidades

* [GET] http://localhost:8000/getFechas/date

Muestra la entrada de la tabla a que hace referencia la fecha "date"

* [GET] http://localhost:8000/getAmazon

Muestra todas las entradas de la tabla Amazon cargada en la base de datos

* [GET] http://localhost:8000/getDescribe/

Muestra los valores estadisticos de cada una de las columnas de la base de datos

* [POST] http://localhost:8000/postAmazon/fecha_inicio,fecha_fin

Inserta en la base de datos la información bursatil de Amazon entre la fecha_inicio y la fecha_fin

* [DELETE] http://localhost:8000//deleteamazon/date

Elimina la información relativa a una fecha de la base de datos


3. Estructura del proyecto
--------------------------

El proyecto consta de:
* Una rama **main** para los desarrollos definitivos.
* Una rama **develop_sql** para los desarrollos con conexión a base de datos de tipo SQL, como es PostgreSQL.
* Una rama **develop_mongo** para los desarrollos con conexión a base de datos de tipo NoSQL, como es MongoDB.
