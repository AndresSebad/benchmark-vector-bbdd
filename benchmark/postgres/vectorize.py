from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import numpy as np

def vectorize_embed(data: pd.DataFrame, datacol:str = 'TEXTO', dim = 64) -> np.array:
    
    vectorizer = TfidfVectorizer()
    emb = vectorizer.fit_transform(data['TEXTO'])
    svd = TruncatedSVD(dim)
    embedding = svd.fit_transform(emb)
    
    return vectorizer, svd, embedding

def gen_dataset(dataurl: str = 'textos.csv', datacol:str = 'TEXTO', dim = 64) ->pd.DataFrame:
    data = pd.read_csv(dataurl)
    vectorizer, svd, embedding = vectorize_embed(data, datacol, dim)
    data = data.drop(columns = datacol).reset_index(drop = True)
    data['embedding'] = [vec.tolist() for vec in embedding]
    return vectorizer, svd, data
    