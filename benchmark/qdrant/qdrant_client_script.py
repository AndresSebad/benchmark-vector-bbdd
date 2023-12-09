from qdrant_client import QdrantClient
from qdrant_client.http import models
import timeit
import pandas as pd
import uuid


class QdrantWrapper:
    def __init__(self):
        self.client = QdrantClient(":memory:")
        self.collection = None
        self.report = {}

    
    def create_collection(self, collection_name, vector_size=1000):
        try:
            self.collection = self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
            )
            print(self.collection)
        except Exception as e:
            print(f"Error: {e}")
    
    def add_documents(self, documents, metadata, ids):
        if self.collection is not None:
            start_time = timeit.default_timer()
            uuid_ids = [str(uuid.UUID(int=id_)) for id_ in ids]
            self.client.add(
                collection_name=self.collection,
                documents=documents,
                metadata=metadata,
                ids=uuid_ids
            )
            end_time = timeit.default_timer()
            self.report["building time"] = end_time - start_time
        pass
    
    def query_documents(self, query_text):
        if self.collection is not None:
            start_time = timeit.default_timer()
            query = self.client.query(
                collection_name=self.collection,
                query_text=query_text
                )
            end_time = timeit.default_timer()
            self.report["query time"] = end_time - start_time
            #return query
            pass
    
        

    def calculate_query_latency(self, num_queries):
        if self.collection is not None:
            start_time = timeit.default_timer()
            for _ in range(num_queries):
                self.query_documents("query test")
            end_time = timeit.default_timer()
            self.report["query latency"] = (end_time - start_time) / num_queries
            return self.report["query latency"]
        

#    def calculate_query_per_second(self, num_queries):
#        query_latency = self.calculate_query_latency(num_queries)
#        self.report["query per second"] = num_queries / query_latency
#        pass
    
    def get_report(self):
        for key in self.report:
            print(f"{key}: {self.report[key]}")
        pass    
qdrant_wrapper = QdrantWrapper()

qdrant_wrapper.create_collection("first_collection")


data = pd.read_csv("textos.csv")
textos = data['TEXTO'].tolist() # Lista de textos
metadatas = data[['TITULO', 'AUTOR']].to_dict('records') # Lista de diccionarios con metadatos
ids = [(x) for x in data.index] # Lista de ids



qdrant_wrapper.add_documents(textos, metadatas, ids)


qdrant_wrapper.query_documents("This is a query document")
qdrant_wrapper.calculate_query_latency(5)
#qdrant_wrapper.calculate_query_per_second(5)
