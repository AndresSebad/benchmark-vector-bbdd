import psycopg2 as pg
from pgvector.psycopg2 import register_vector
import pandas as pd
import numpy as np
import psutil
import timeit
from vectorize import gen_dataset
from postgres_client import DatabaseBenchmark

if __name__ == '__main__':
    # Medición inicial de recursos del sistema
    memoria_inicial = psutil.virtual_memory()
    cpu_inicial = psutil.cpu_percent(interval=1)
    io_inicial = psutil.disk_io_counters()
    red_inicial = psutil.net_io_counters()

    print('INTIALIZING DB')
    conn = pg.connect(dbname='vectordb', user='testuser', password='testpwd', host='db', port='5432')

    vectorizer, svd, data = gen_dataset("textos.csv")

    register_vector(conn)
    cur = conn.cursor()
    
    data_list = [(row['AUTOR'], row['TITULO'], np.array(row['embedding'])) for index, row in data.iterrows()]
    cur.executemany("INSERT INTO embeddings (author, title, embedding) VALUES (%s, %s, %s)", data_list)
    
    conn.commit()
    cur.close()

    bm = DatabaseBenchmark(conn, vectorizer, svd)

    # Inicia el cronómetro para medir el tiempo de ejecución
    start_time = timeit.default_timer()
    print(bm.measure_qps('dog', 100))
    print(bm.measure_index_building_time())
    end_time = timeit.default_timer()

    # Medición final de recursos del sistema
    memoria_final = psutil.virtual_memory()
    cpu_final = psutil.cpu_percent(interval=1)
    io_final = psutil.disk_io_counters()
    red_final = psutil.net_io_counters()

    # Impresión de resultados
    print(f"Uso de Memoria antes: {memoria_inicial}, después: {memoria_final}")
    print(f"Uso de CPU antes: {cpu_inicial}%, después: {cpu_final}%")
    print(f"I/O del Disco antes: {io_inicial}, después: {io_final}")
    print(f"Datos de Red antes: {red_inicial}, después: {red_final}")
    print(f"Tiempo total de ejecución: {end_time - start_time} segundos")
