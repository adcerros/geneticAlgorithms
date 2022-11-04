///////////////////////////////////////////////////
Intrucciones para la ejecución de cualquiera de las dos versiones del programa:

Los parametros de entrada del programa contienen datos por defecto por 
lo que puede ejecutarse el script directamente en cualquier IDE o terminal.

Si se desean cambiar los parametros puede realizarse directamente mediante 
la modificación de los parámetros de entrada de la funcion run_multiple 
que dado que soporta la ejecución multihilo de varias ejecuciones 
con distintos parametros recibe una lista de listas de la forma:

[[Ejecucion1], [Ejecucion2] ...]

Donde cada lista ejecucion es de la forma:

[[tamaño_poblacion, rondas, numero_genes(motores), tasa_reemplazo, tamaño_familia, b(parametro de la tasa de aprendizaje)], [Ejecuicion_2], ...]

A la finalizacion del programa se obtendran los ficheros con los datos (mejor_fitness, media_varianzas, variedad_genetica) 
generados en el directorio del script y la grafica correspondiente a los mismos

NOTA: LAS EJECUCIONES DEBEN TENER PARAMETROS DISTINTOS O PUEDE 
PRODUCIRSE UNA SOBREESCRITURA POR ALGUNO DE LOS HILOS EN UNO DE LOS ARCIVOS DE DATOS


/////////////////////////////////////////////////////
Instrucciones para la generación de graficas:

Mover al directorio donde se encuentra el script los archivos de la carpeta data para los cuales se desee una grafica
Comentar la llamada a la funcion run_multiple para realizar unicamente la ejecucion de la funcion collect_data 


/////////////////////////////////////////////////////
Documentación:

En la carpeta Data puede encontrarse:

Los archivos con los datos recogidos en cada una de las ejecuciones
La carpeta graficas, que contiene las graficas de cada una de las comparaciones 
