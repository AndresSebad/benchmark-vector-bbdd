import psycopg as pg
from pgvector.psycopg import register_vector
import pandas as pd
import numpy as np
from connections import dbname, user, password, host, port
import timeit



class DatabaseBenchmark:
    """
    Clase para benchmark de postgres
    """
    def __init__(self, db_connection, vectorizer, trunc, table = 'embeddings', cost_per_hour = False):
        """
        db_connection: Conexión a base de datos
        vectorizer: text to vector vectorizer
        trunc: trunc svd from sparse matrix to lower dim matrix
        """

        self.db_connection = db_connection
        self.cost_per_hour = cost_per_hour
        self.vectorizer = vectorizer
        self.trunc = trunc
        self.table = table

    def query(self, query_string, n_results = 1):
        """
        query_string: vector de representación de un texto
        n_results: numeros de vecinos a buscar
        """
        query_vector = self.trunc.transform(self.vectorizer.transform([query_string]))[0].tolist()
        
        with self.db_connection.cursor() as cur:
            
            query = "SELECT * FROM {0} ORDER BY embedding <-> '{1}' LIMIT {2};".format(self.table, query_vector, n_results) 
        
            results = cur.execute(query)

            return [record for record in results]  
#       

    def build_index(self, method = 'ivfflat'):
        """
        incompleta, probar con datos
        """
        with self.db_connection.cursor() as cur:
        
            query = 'CREATE INDEX ON {0} USING {1} (embedding vector_l2_ops);'.format(self.table, method)
            
            results = cur.execute(query)
#       

    def measure_qps(self, query_string, num_queries=5, n_results = 1):
        
        start_time = timeit.default_timer()
        for _ in range(num_queries):
            self.query(query_string= query_string, n_results= n_results)
        end_time = timeit.default_timer()
        
        qps = num_queries / (end_time - start_time)
        
        return qps
    
    def measure_qp_dollar(self, qps):
        if self.cost_per_hour is False:
            return "No hay costo por hora"
        qp_dollar = (qps / self.cost_per_hour) * 3600
        return qp_dollar
    
    def measure_latency(self, query_string, ):

        
        start_time = timeit.default_timer()
        self.query(query_string, 1)
        latency = timeit.default_timer() - start_time
        
        return latency
    
    def measure_index_building_time(self):

        
        start_time = timeit.default_timer()
        self.build_index()
        index_building_time = timeit.default_timer() - start_time
        
        return index_building_time