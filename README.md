DM_Center (Data Management Center)
----------------------------------

1. Objetivo
-----------

Es una aplicación creada con Python 3.8.10 para la gestión de los datos mediante el empleo de una API Rest creada a partir del Framework de Python FastAPI.

2. Funcionalidad
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

3. Estructura del proyecto
--------------------------

El proyecto consta de:
* Una rama **main** para los desarrollos definitivos.
* Una rama **develop_sql** para los desarrollos con conexión a base de datos de tipo SQL, como es PostgreSQL.
* Una rama **develop_mongo** para los desarrollos con conexión a base de datos de tipo NoSQL, como es MongoDB.