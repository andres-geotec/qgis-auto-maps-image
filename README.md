# qgis-auto-maps-image

Para su ejecición es necesario cargar los datos separados por variable en una carpeta junto con los templates ubicados en la carpeta resources y espesificar la ruta en la variable path.


## tiempos_hospitalarios

Genera la estructura de las variables para cada mapa del reporte a partir de la fuente --COVID19MEXICOTOT.


## respuestaHospilataria

Genera los mapas estáticos de cada variable y acumulados, por Cuantiles y Natural Breakes.


## respuestaHospilatariaGif

Genera los mapas por semana por clasificaión definida.


## gif.py

Genera los mapas gif a partir de los mapas por semana.


# Pendientes

- Cargar los datos de los mapas a partir de un archivo separado por comas y no por un arreglo en el código como se hace ahora.
- Integrar el script que genere el ppt automáticamente.
- Configurar el entorno para la ejecución del api PyQgis desde consola.
- Adecuar las rutas para la estructura del repositorio `coronavirus.data`.

