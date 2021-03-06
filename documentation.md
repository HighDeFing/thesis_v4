## Preparación

Instalar python3 si no esta, version 3.8.10
`sudo apt install python3`

Instalar python3-venv si es necesario

`sudo apt install python3.8-venv`

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
3.1. `env/bin/python3 setup.py install`

Ejectuamos la instalacion: 
4. `/path/to/python/interpreter setup.py install --user`

En mi caso seria: `env/bin/python3 setup.py install --user`

5. Ejecutamos `pip install -e .` en el directorio donde esta el setup.

Esto ahora nos permite importar scripts hermanos en python con importes absolutos.

thesis_v4/env/bin/python3

6. Instalar los requerimientos

`pip install -r requirements.txt`

`pip install Unidecode` para los acentos

## Spacy

```console
$ pip install -U pip setuptools wheel
$ pip install -U spacy
$ pip install -U 'spacy[cuda101]' #gpu important to know cuda version with `nvcc --version`
$ python -m spacy download es_core_news_sm #efficinecy
$ python -m spacy download es_dep_news_trf #accuracy
```


## Pdf dealing

### Is it a pdf:


```console
$ pip install pdfminer.six
```

## Jupyter

1. Ir a el archivo de scripts y empezar por scraper_files
En este archivo se ejecuta scraperv3.py con el paramentro de cuantas tesis se desea descargar el limit es 8210

2. Este paso genera un archivo en csv_files llamado url_thesis_{#numero_tesis}.csv donde #numero de tesis es la cantidad especificada en el paso anterior. Ejemplo: url_thesis_250.csv

3. Luego de realizar el scraping es necesario descargar la tesis, para hacerlo vamos a la carpeta de download_files y ejecutamos el script thesis_downloader colocando en la `download_from_file` aqui colocamos el path donde esta el archivo anterior. Ejemplo ./csv_files/url_thesis_250.csv

4. Se tiene que verificar si todos los archivos se descargaron, esto se realiza meidante el archivo que se encuentra en scripts preprocessing_files, `check_existance.py`.

5. Luego de descargar los archivos y verificar su existencia procedemos a verificar si son texto o imagenes que necesitar OCR, para esto utilizamos el criterio de clasificacion descrito en la parte de criterio de clasificacion. Este archivo se encuentra en notebooks `delete_not_exist.ipynb`. 

6. Clasificar la escuela: Este paso es realizado por un notebook, en la carpeta notebooks, el archivo `school_matcher.ipynb`.

5.1. Instalar jupyter notebook 
`pip install notebook==6.4.10`

5.2. Instalar ipykernel
`pip install --user ipykernel`

5.3. Añadir el virtual env a jupyter.
`python -m ipykernel install --user --name=env`

5.4. Ejecutar jupyter notebook:
`jupyter notebook`

6. Spacy

Para usar spacy ejecutar

6.1. `pip install -U pip setuptools wheel`

6.2. `pip install -U spacy`

6.3. Modelo en español `python -m spacy download es_core_news_sm`

Todo esto es parte del paso anterior, para ejecutar el notebook.




## Tiempos:

- Para verificar los errores de saber si una tesis existe y es pdf lejible con 8211 tesis se tardo 2 horas.

- Para identificar si es imagen o es pdf con texto se tardo 5 horas.

- Para clasificar e identificar la carrera de la tesis se tardo





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

Se utilizo apache tika para obtener el texto de las carreras, el hecho de utilizar apache tika en vez de pdfplumber, es que apache tika es considerablemente mejor al tratar con acentos y pdfs, es en general mas preciso obteniendo las carreras.

Solo se comprobo en las primeras 6000 palabras y las ultimas 6000 paginas si habia un encuentro con una carrera. Esto ayudo a que el procesado de cada archivo fuera mas rapido, debido a que si se trata de procesar toda la tesis en apache tika esto daba errores.

La memoria y procesamiento del matcher tuvo que hacerse por batches de 20 con cada uno teniendo al alrededor de 380 tesis. Despues cada uno de los vectores resultados se unieron para dar el dataframe final con todas las tesis.

No se tiene una metrica exacta de cual fue la precision de carreras clasificadas apropiadamente, pero realizando revisiones rapidas se nota que la mayoria fue clasificada correctamente. 

## Para scraping

1. Ejecutar scraperv3 en scraper_files, poner la cantidad de tesis a poner en la tabla.
2. Descargar las tesis en thesis_downloader.py en download_files, recordar colocar el nombre del csv donde estan laos url de las tesis del paso anterior.
3. Ejecutar luego index_scan en preprocessing_files, recordar cambiar los parametros que son.

## Evaluacion

Los documentos para entrenar son de index:

1. 5567
2. 5541
3. 5576
4. 5603
5. 5602 
6. 5601
7. 5600
8. 5599
9. 5598
10. 5595
11. 5594
12. 5593
13. 5592
14. 5590
15. 5577
16. 5589
17. 5583
18. 5538
19. 5501
20. 5496

Los documentos para evaluar son de index:

1. 5728
2. 5727
3. 5726
4. 5725
5. 5628

Los documentos para probar son de index:

1. 5633
2. 5641 
3. 5631
4. 5630
5. 5629

#### Squad to DPR

Se necesita todo haystack de github. Para correr esto se debe hacer en el directorio de haystack.

path de squad: `/home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/answers_30.json`

path de dpr: `/home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/answers_30_dpr.json`

commando en haystack/haystack/utils:

Training:
`python3 haystack/utils/squad_to_dpr.py --squad_input_filename /home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/training.json --dpr_output_filename /home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/training_dpr.json`

Dev:

`python3 haystack/utils/squad_to_dpr.py --squad_input_filename /home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/dev.json --dpr_output_filename /home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/dev_dpr.json`

Test:

`python3 haystack/utils/squad_to_dpr.py --squad_input_filename /home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/test.json --dpr_output_filename /home/heider/Codes/thesis_v4/notebooks/squad_format_thesis/test_dpr.json`

Como se tiene una version mas vieja de pip recordad install haystack con:
`pip install -e '.[sql,only-faiss-gpu,only-milvus1,weaviate,graphdb,crawler,preprocessing,ocr,onnx-gpu,ray,dev]'`

### Para cada tesis se debe poner un minimo de 5 preguntas etiquetadas.

Si se etiquetan 20 tesis con 5 preguntas da un total de 100 pares de preguntas y respuestas.

### Evaluacion con los top=5:

#### Con hiperparametros:

Se pone el parametro open_domain que nos da resultado positivo si la respuesta esta en los pasages recuperados, si es falso solo da verdad si recupera el documento en especifico. 

1. Caso 1:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=5,
    batch_size=5,
    grad_acc_steps=3,
    save_dir=save_dir,
    evaluate_every=3,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
)
```

Retriever Recall: 0.64
Retriever Mean Avg Precision: 0.456

1.1 DEV SET

Retriever Recall: 0.7083333333333334
Retriever Mean Avg Precision: 0.39375

2. Caso 2:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=1,
    batch_size=8,
    grad_acc_steps=1,
    save_dir=save_dir,
    evaluate_every=40,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
    optimizer_name = "SGD",
    learning_rate = 1e-6
)
```

Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.49933333333333335

2.1. DEV SET

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.4993055555555556



3. Caso 3:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=1,
    batch_size=4,
    grad_acc_steps=1, #aqui
    save_dir=save_dir,
    evaluate_every=4, #aqui
    embed_title=True,
    num_positives=1,
    num_hard_negatives=1,
)
```

Retriever Recall: 0.6
Retriever Mean Avg Precision: 0.456

3.1. DEV SET

Retriever Recall: 0.625
Retriever Mean Avg Precision: 0.3541666666666667

4. Caso 4:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=3,
    batch_size=6,
    grad_acc_steps=1, #aqui
    save_dir=save_dir,
    evaluate_every=4, #aqui
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
)
```

Retriever Recall: 0.52
Retriever Mean Avg Precision: 0.36333333333333334

4.1. DEV SET

Retriever Recall: 0.5416666666666666
Retriever Mean Avg Precision: 0.25625000000000003

5. Caso 5:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=2,
    batch_size=4,
    grad_acc_steps=1,
    save_dir=save_dir,
    evaluate_every=6,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
    optimizer_name = "SGD"
)
```

Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.5076666666666667

5.1. DEV SET

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.5256944444444445

6. Caso 6:

```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=2,
    batch_size=5,
    grad_acc_steps=2,
    save_dir=save_dir,
    evaluate_every=6,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=1,
    optimizer_name = "AdamW"
)
```
Retriever Recall: 0.48
Retriever Mean Avg Precision: 0.38333333333333336

6.1. DEV SET

Retriever Recall: 0.5416666666666666
Retriever Mean Avg Precision: 0.2965277777777778

7. Caso 7:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=1,
    batch_size=6,
    grad_acc_steps=1,
    save_dir=save_dir,
    evaluate_every=2,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
    optimizer_name = "Adagrad"
)
```

Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.5076666666666667

7.1. DEV SET

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.5027777777777778

8. Caso 8:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=5,
    batch_size=6,
    grad_acc_steps=1,
    save_dir=save_dir,
    evaluate_every=3,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=1,
    optimizer_name = "RAdam"
)
```

Retriever Recall: 0.6
Retriever Mean Avg Precision: 0.4866666666666667

8.1. DEV SET

Retriever Recall: 0.625
Retriever Mean Avg Precision: 0.36944444444444446

9. Caso 9:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=2,
    batch_size=6,
    grad_acc_steps=1,
    save_dir=save_dir,
    evaluate_every=5,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
    optimizer_name = "SGD",
    learning_rate = 1e-6
)
```

Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.5076666666666667

9.1. DEV SET 

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.5256944444444445

10. Caso 10:
```python
retriever.train(
    data_dir=doc_dir,
    train_filename=train_filename,
    dev_filename=dev_filename,
    test_filename=dev_filename,
    n_epochs=3,
    batch_size=6,
    grad_acc_steps=1,
    save_dir=save_dir,
    evaluate_every=4,
    embed_title=True,
    num_positives=1,
    num_hard_negatives=2,
    optimizer_name = "SGD",
    learning_rate = 1e-7
)
```

Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.5076666666666667

10.1. DEV SET

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.5256944444444445

#### Modelo sin entrenar:

Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.5076666666666667

##### DEV SET

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.5256944444444445


#### Modelo sin entrenar viejo:

Retriever Recall: 0.28
Retriever Mean Avg Precision: 0.19

##### DEV SET

Retriever Recall: 0.3333333333333333
Retriever Mean Avg Precision: 0.21319444444444444

#### Modelo estadistico BM25:

Retriever Recall: 0.56
Retriever Mean Avg Precision: 0.4793333333333333

##### DEV SET

Retriever Recall: 0.7083333333333334
Retriever Mean Avg Precision: 0.5305555555555556


### Evaluacion con los top=10:

1. Caso 1:
Retriever Recall: 0.68
Retriever Mean Avg Precision: 0.42538095238095236

1.1. DEV SET:
Retriever Recall: 0.7916666666666666
Retriever Mean Avg Precision: 0.40433201058201057

2. Caso 2:

Retriever Recall: 0.8
Retriever Mean Avg Precision: 0.5023809523809525

2.1. DEV SET:

Retriever Recall: 0.7916666666666666
Retriever Mean Avg Precision: 0.50625

3. Caso 3:

Retriever Recall: 0.72
Retriever Mean Avg Precision: 0.4754920634920636

3.1. DEV SET:

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.373015873015873

4. Caso 4:

Retriever Recall: 0.6
Retriever Mean Avg Precision: 0.3734920634920635

4.1. DEV SET:

Retriever Recall: 0.7083333333333334
Retriever Mean Avg Precision: 0.2785714285714286

5. Caso 5:

Retriever Recall: 0.84
Retriever Mean Avg Precision: 0.5166666666666667

5.1. DEV SET:

Retriever Recall: 0.8333333333333334
Retriever Mean Avg Precision: 0.5385912698412699

6. Caso 6:

Retriever Recall: 0.64
Retriever Mean Avg Precision: 0.40801587301587305

6.1. DEV SET:

Retriever Recall: 0.6666666666666666
Retriever Mean Avg Precision: 0.31636904761904766

7. Caso 7:

Retriever Recall: 0.84
Retriever Mean Avg Precision: 0.5137619047619048

7.1. DEV SET:

Retriever Recall: 0.8333333333333334
Retriever Mean Avg Precision: 0.5143518518518518

8. Caso 8:

Retriever Recall: 0.8
Retriever Mean Avg Precision: 0.49866666666666676

8.1. DEV SET:

Retriever Recall: 0.7916666666666666
Retriever Mean Avg Precision: 0.39523809523809533

9. Caso 9:

Retriever Recall: 0.84
Retriever Mean Avg Precision: 0.5166666666666667

9.1. DEV SET:

Retriever Recall: 0.8333333333333334
Retriever Mean Avg Precision: 0.5385912698412699

10. Caso 10:

Retriever Recall: 0.84
Retriever Mean Avg Precision: 0.5166666666666667

10.1. DEV SET:

Retriever Recall: 0.8333333333333334
Retriever Mean Avg Precision: 0.5385912698412699


#### Modelo sin entrenar TOP 10:

Retriever Recall: 0.84
Retriever Mean Avg Precision: 0.5166666666666667

##### DEV SET:

Retriever Recall: 0.8333333333333334
Retriever Mean Avg Precision: 0.5385912698412699

#### Modelo estadistico BM25 TOP10:

Retriever Recall: 0.6
Retriever Mean Avg Precision: 0.47171428571428564

##### DEV SET:

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.5351851851851852

#### Modelo sin entrenar viejo TOP 10:

Retriever Recall: 0.4
Retriever Mean Avg Precision: 0.204

##### DEV SET:

Retriever Recall: 0.4583333333333333
Retriever Mean Avg Precision: 0.23303571428571426


##### Training and CUDA

Para hacer que funcionara el proceso de entrenamiento se necesita pytorch `1.10`.

`pip install --upgrade --force-reinstall torch==1.10.1+cu102 torchvision==0.11.2+cu102 torchaudio==0.10.1 -f https://download.pytorch.org/whl/torch_stable.html`




## CUDA and GPU

Para que funcionara con mi GPU de 3070ti tuve que utilizar este comando para tener cuda `1.11.0`.

`pip3 install --upgrade torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113`





