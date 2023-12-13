import psycopg as pg
from pgvector.psycopg import register_vector
import pandas as pd
import numpy as np
import timeit
from vectorize import gen_dataset
from postgres_client import DatabaseBenchmark

if __name__ == '__main__':

    ##############################
    ##########CLIENTE#############
    ##############################

    print('INTIALIZING DB')
    
    conn = pg.connect(dbname= 'vectordb', user= 'testuser', password= 'testpwd', host= 'db', port= '5432')

    ##############################
    ############DATA##############
    ##############################



    vectorizer, svd, data = gen_dataset("textos.csv")

    register_vector(conn)
    cur = conn.cursor()
    
    data_list = [(row['AUTOR'], row['TITULO'], np.array(row['embedding'])) for index, row in data.iterrows()]
    
    cur.executemany("INSERT INTO embeddings (author, title, embedding) VALUES (%s, %s, %s)", data_list)
    
    conn.commit()
    cur.close()

    ###########################
    ##########BM###############
    ###########################

    bm = DatabaseBenchmark(conn, vectorizer, svd)
    print(bm.measure_qps('dog', 100))
    print(bm.measure_index_building_time())