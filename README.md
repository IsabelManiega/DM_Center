DM_Center (Data Management Center)
----------------------------------

1. Objetivo
-----------

Es una aplicación creada con Python 3.8.10 para la gestión de los datos mediante el empleo de una API Rest creada a partir del Framework de Python FastAPI.

2. Funcionalidad
------------------

Creados distintos métodos para la gestión de los datos:

* [GET] http://localhost:8000/docs#/TEST/info__get

Muestra mensaje de bienvenida.

* [GET] http://localhost:8000/docs#/Empleados/show_getData__get

Muestra la información relativa a todos los usuarios registrados en la aplicación.

* [GET] http://localhost:8000/docs#/Empleados/showOne_getData__numero_empleado__get

Muestra la información relativa a un usuario registrados en la aplicación.

* [POST] http://localhost:8000/docs#/Empleados/insertManyEx_insertExemple__post

Inserta la información relativa a varios usuarios como modo de ejemplo en la aplicación.

* [POST] http://localhost:8000/docs#/Empleados/insert_postData__post

Inserta la información relativa a un usuario en la aplicación.

* [PUT] http://localhost:8000/docs#/Empleados/update_putData__numero_empleado__put

Actualizar la información relativa a un usuario en la aplicación.

* [DELETE] http://localhost:8000/docs#/Empleados/deleteOne_deleteData__numero_empleado__delete

Elimina la información relativa a un usuario en la aplicación.

* [DELETE] http://localhost:8000/docs#/Empleados/delete_deleteData__delete

Elimina la información relativa a todos usuarios en la aplicación.

3. Estructura del proyecto
--------------------------

El proyecto consta de:
* Una rama **main** para los desarrollos definitivos.
* Una rama **develop_sql** para los desarrollos con conexión a base de datos de tipo SQL, como es PostgreSQL.
* Una rama **develop_mongo** para los desarrollos con conexión a base de datos de tipo NoSQL, como es MongoDB.