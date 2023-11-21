import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

import pandas as pd

##################################
############ CLASE ###############
##################################

class DatabaseBenchmark:
    def __init__(self, db_collection, cost_per_hour = False):
        self.db_collection = db_collection
        self.cost_per_hour = cost_per_hour

    def query(self, query_string, n_results):
        # Squared L2
        results = self.db_collection.query(
            query_texts=query_string, # Lista de strings
            n_results=n_results # Número de resultados
        )
        pass

    def build_index(self, documents, metadatas, ids):
        self.db_collection.add(
            documents=documents, # Lista Documentos
            metadatas=metadatas, # Lista de Diccionarios
            ids=ids # Lista de Ids
        )
        pass

    def measure_qps(self, num_queries=20):
        import timeit

        start_time = timeit.default_timer()
        for _ in range(num_queries):
            self.query(query_string=["¿Quién es Quijote de la Mancha?"], n_results=1)
        end_time = timeit.default_timer()

        qps = num_queries / (end_time - start_time)

        return qps

    def measure_latency(self):
        import timeit

        start_time = timeit.default_timer()
        self.query(["¿Quién es Quijote de la Mancha?"], 1)
        latency = timeit.default_timer() - start_time

        return latency

    def measure_index_building_time(self, documents, metadatas, ids):
        import timeit

        start_time = timeit.default_timer()
        self.build_index(documents, metadatas, ids)
        index_building_time = timeit.default_timer() - start_time

        return index_building_time

##################################
############ CLIENTE #############
##################################

chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
default_ef = embedding_functions.DefaultEmbeddingFunction() # all-MiniLM-L6-v2 model

##################################
########## COLECCIÓN #############
##################################

collection_status = False
while collection_status != True:
    try:
        document_collection = chroma_client.get_or_create_collection(name="documents_collection", embedding_function=default_ef)
        collection_status = True
    except Exception as e:
        pass

##################################
########## PRE PROCESS ###########
##################################

documents = pd.read_csv("../data/textos.csv")

textos = data['TEXTO'].tolist() # Lista de textos
metadatas = data[['TITULO', 'AUTOR']].to_dict('records') # Lista de diccionarios con metadatos
ids = [str(x) for x in data.index] # Lista de ids

document_collection.add(documents=documents, metadatas=metadatas, ids=ids)

##################################
########## BENCHMARK #############
##################################

Benchmark = DatabaseBenchmark(db_collection=collection, cost_per_hour = False)

ibt = Benchmark.measure_index_building_time(textos, metadatas, ids)
qps = Benchmark.measure_qps(num_queries = 20)
ql = Benchmark.measure_latency()

print(f'Index Building Time: {ibt}\nQueries Per Second: {qps}\nQuery Latency: {ql} Segundos')
