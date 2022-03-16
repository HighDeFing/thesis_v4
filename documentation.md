## Preparación

Instalar python3 si no esta, version 3.8.10
`sudo apt install python3`

Instalar docker

`sudo apt-get update`

## Haystack

### Para ejecutar elasticsearch lo hacemos desde docker:

1. Instalamos y ejecutamos DockerDesktop
2. Ejecutamos (para la primera vez):

```bash
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.13.0
docker run --name es01-test --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.0
```

3. Para el resto de las ejecuciones:
```bash
docker start es01-test -a
```

### Para ejecutar kibana:

1. En una nueva terminal ejecutamos (por primera vez):
```bash
docker pull docker.elastic.co/kibana/kibana:7.13.0
docker run --name kib01-test --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" docker.elastic.co/kibana/kibana:7.13.0
```

1.1 
`docker run --name kib-01 -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://node01:9200" docker.elastic.co/kibana/kibana:7.13.0`

2. Para el resto de las ejecuciones:
```bash
docker start kib01-test -a


```

3. Para acceder a Kibana, ir al link `http://localhost:5601`


## Ejecución

We create a virtual env with:

1. `python3 -m venv env`

Accedemos al ambiente virtual:
2. `source env/bin/activate`

Ejecutamos en el directorio donde esta `setup.py`:

3. `env/bin/python3 setup.py install --user`

Ejectuamos la instalacion: 
4. `/path/to/python/interpreter setup.py install --user`

En mi caso seria: `env/bin/python3 setup.py install --user`

5. Ejecutamos `pip install -e .` en el directorio donde esta el setup.

Esto ahora nos permite importar scripts hermanos en python con importes absolutos.

`pip install Unidecode` para los acentos


## Criterio de clasificación

Para determinar que una tesis es escaneada y no contiene texto, se revizaron 5 tesis del primer lote inicial y se determino revisando todas las hojas manualmente que la mayoria eran imagenes. Con esto en mente y teniendo en cuenta que se requiere clasificar por carrera y esta informacion se encuentra normalmente en las primeras paginas de las tesis, el criterio para determinar si una tesis mayoritariamente imagenes que requieres OCR (Reconocimineto optico de caracteres) para pasar a texto queda de la siguiente manera:

- La primera hoja es imagen o no.
- La segunda hoja es imagen o no.
- La hoja del medio mas uno es imagen o no.
- La hoja del final -20 es imagen o no (esto es por la bibliografia).
- Una hoja aleatoria que no sea la primera ni la segunda es imagen o no.

Para determinar si es imagen o no se utilizo la funcion de `pdfplumber` `extract_text()` si esta funcion retornaba '' un caracter vacio significaba que la pagina no contiene texto crudo si no en formato de una imagen escaneada.

Si el archivo pdf cumple con 3 de las 5 condiciones se considera que es imagen, de lo contrario es texto.

Las 5 tesis revisadas en cuestion:
1) http://saber.ucv.ve/handle/10872/315
2) http://saber.ucv.ve/handle/10872/336
3) http://saber.ucv.ve/handle/10872/341
4) http://saber.ucv.ve/handle/10872/318
5) http://saber.ucv.ve/handle/10872/314 (El resumen era texto pero el resto era escaneado) 


## Criterio de busqueda de carrera

Para determinar la escuela a la que pertenece una tesis, se tiene que pasar el texto de las paginas pdf a texto crudo, este texto tiene que pasar por un proceso de limpiado para eliminar multiples espacios en blanco, acentos y saltos de linea. Estos luego son comparados por las carreras en `escuelas.json`.

No es sensible a mayusculas.
La oracion de especificacion de la escuela tiene que ser exacta, esta se puede ser encontrar en el encabezado o por la firma del acta.
Por lo tanto se especifica en que paginas se buscara la escuela en las primeras 10 paginas si ocurre 1 match entonces se declarara esa como la escuela.

## Para scraping

1. Ejecutar scraperv3 en scraper_files, poner la cantidad de tesis a poner en la tabla.
2. Descargar laas tesis en thesis_downloader.py en download_files, recordar colocar el nombre del csv donde estan laos url de las tesis del paso anterior.
3. Ejecutar luego index_scan en preprocessing_files, recordar cambiar los parametros que son.


