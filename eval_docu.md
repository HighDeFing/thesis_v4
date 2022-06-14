# Evaluación de los documentos

Los parametros usados para la evaluacion de los documentos fueron los mismo que para el entrenamiento de los documentos, en una evaluacion aparte donde se utilizaron otros parametros en el preprocesador se obtuverion otros valores.

## Parametro de evaluacion
Los parametros viejos son:

```python
preprocessor = PreProcessor(
    split_length=200,
    split_by="word",
    split_overlap=0,
    split_respect_sentence_boundary=False,
    clean_empty_lines=False,
    clean_whitespace=False
)
```

### Caso 1:

#### TEST SET:

Retriever Recall: 0.64
Retriever Mean Avg Precision: 0.4063333333333333

#### DEV SET:

Retriever Recall: 0.75
Retriever Mean Avg Precision: 0.3371527777777778

### Caso 2:

#### TEST SET:

#### DEV SET:

### Caso 3:

#### TEST SET:

#### DEV SET:

### Caso 4:

#### TEST SET:

#### DEV SET:

### Caso 5:

#### TEST SET:

#### DEV SET:

### Caso 6:

#### TEST SET:

#### DEV SET:

### Caso 7:

#### TEST SET:

#### DEV SET:

### Caso 8:

#### TEST SET:

#### DEV SET:

### Caso 9:

#### TEST SET:

#### DEV SET:

### Caso 10:

#### TEST SET:

#### DEV SET:

### Modelo Nuevo:

#### TEST SET:

#### DEV SET:

### Modelo Viejo

#### TEST SET:

#### DEV SET:

### BM25

#### TEST SET:

#### DEV SET:


Resultados modelo nuevo:

Test:
Dev:

Resultados modelo estadistico:

Test:
Dev:

Resultados modelo mejor:

Test:
Dev:

Resultados modelo peor:

Test:
Dev:

Resultados modelo viejo:

Test:
Dev:


## Parametro de entrenamiento

Tambien son los mismo de subida.

Los parametros de entrenamiento son:

```python
preprocessor = PreProcessor(
    clean_empty_lines=False, #Not supported
    clean_whitespace=False, #Not supported
    split_by="word",
    split_length=400,
    split_respect_sentence_boundary=False, #Not supported
    split_overlap=0,
    language="es"
)
```

### Caso 1:

#### TEST SET:

#### DEV SET:

### Caso 2:

#### TEST SET:

#### DEV SET:

### Caso 3:

#### TEST SET:

#### DEV SET:

### Caso 4:

#### TEST SET:

#### DEV SET:

### Caso 5:

#### TEST SET:

#### DEV SET:

### Caso 6:

#### TEST SET:

#### DEV SET:

### Caso 7:

#### TEST SET:

#### DEV SET:

### Caso 8:

#### TEST SET:

#### DEV SET:

### Caso 9:

#### TEST SET:

#### DEV SET:

### Caso 10:

#### TEST SET:

#### DEV SET:

### Modelo Nuevo:

#### TEST SET:

#### DEV SET:

### Modelo Viejo

#### TEST SET:

#### DEV SET:

### BM25

#### TEST SET:

#### DEV SET:

Resultados modelo nuevo:

Test:
Dev:

Resultados modelo estadistico:

Test:
Dev:

Resultados modelo mejor:

Test:
Dev:

Resultados modelo peor:

Test:
Dev:

Resultados modelo viejo:

Test:
Dev:


