# Desafío Sin Límites
## Benchmark Bases de Datos Vectoriales
* Chroma
* Qdrant
* PgVector
* Elastic

### Tareas
* Función para medir Latencia:
   * Indexación
   * Query (Similitud)

### Pruebas con Dataset de Textos Literarios en Español

Para llevar a cabo las pruebas, utilizaremos el dataset disponible en Kaggle, que contiene textos literarios escritos en español, cada uno acompañado por el nombre del autor y el título de la obra. El dataset puede ser encontrado en el siguiente enlace: [Dataset en Kaggle](https://www.kaggle.com/datasets/baldrodin/spanish-language-literature?select=textos.csv).

### Vectorización de Textos

Se requiere que todas las bases de datos vectoriales empleen el `TfidfVectorizer` proporcionado por la biblioteca scikit-learn. Este vectorizador se encarga de convertir los textos en una matriz de características TF-IDF que posteriormente puede ser utilizada en diversos modelos de Machine Learning. La documentación oficial del `TfidfVectorizer` puede ser consultada en el siguiente enlace: [Documentación de TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).
