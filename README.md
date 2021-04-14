# TestEvertec
* Para Realizar las Pruebas de la aplicación ejecutar python manage.py test orders 
* Para Simular el cron para actualizar ordenes pendientes [que fueron procesadas por ejemplo pero se cerro el navegador] ejecutar python manage.py orders simulatecron
* La Aplicación por defecto se ejecuta en http://127.0.0.1:8000/ si se ha de utilizar otra ip o puerto cambiar la variable SITE_URL en el settings [test_evertec/settings.py]
* Para las credenciales de placetopay se creo la variable PLACE_TO_PAY_CONFIG en el settings
