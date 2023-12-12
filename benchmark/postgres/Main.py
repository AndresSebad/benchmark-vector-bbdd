import psycopg as pg
from pgvector.psycopg import register_vector
import pandas as pd
import numpy as np
from connections import dbname, user, password, host, port
import timeit
from vectorize import gen_dataset
from postgres_client import DatabaseBenchmark

if __name__ == '__main__':

    ##############################
    ##########CLIENTE#############
    ##############################
    conn = pg.connect(dbname= dbname, user= user, password= password, host= host, port= port)
    conn.autocommit = True
    cursor = conn.cursor()
    sql = '''DROP database if exists vector'''
    cursor.execute(sql)
    
    sql = '''CREATE database vector'''
    cursor.execute(sql)

    conn = pg.connect(dbname= 'vector', user= user, password= password, host= host, port= port)

    conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
    register_vector(conn)
    
    table_create_command = """
    CREATE TABLE embeddings (
                id SERIAL primary key, 
                author text,
                title text,
                embedding vector(64)
                );
                """
    cur = conn.cursor()
    cur.execute(table_create_command)
    cur.close()
    conn.commit()
    

    ##############################
    ############DATA##############
    ##############################



    vectorizer, svd, data = gen_dataset("../data/textos.csv")

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