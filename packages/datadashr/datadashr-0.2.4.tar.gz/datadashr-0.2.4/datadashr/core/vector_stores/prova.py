from datadashr.core.vector_stores import VectorStore
from datadashr.core.embeddings import Embedding
import pandas as pd
from datadashr.core.vector_stores.chromadb_store import ChromaDBStore
from datadashr.core.vector_stores.faiss_store import FaissStore
from datadashr.config import *

def verify_documents(vector_store):
    documents = vector_store.get_all_documents()
    print(f"Total documents in store: {len(documents)}")
    for doc in documents:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")
        print('---')

def search_and_print(vector_store, query):
    results = vector_store.similarity_search(query)
    for result in results:
        print(f"Search Result Content: {result.page_content}")
        print(f"Search Result Metadata: {result.metadata}")
        print('---')

# Inizializza l'embedding
emb = Embedding(embedding_type='fastembed')
embedding_function = emb.get_embedding()  # Ottieni l'oggetto embedding corretto

print(emb.model_info)

data = {
    'employeeid': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['HR', 'IT', 'Finance'],
    'salary': [50000, 60000, 70000],
    'manager': ['Dave', 'Eva', 'Frank'],
    'projectid': [101, 102, 103],
    'projectname': ['Project A', 'Project B', 'Project C']
}

df = pd.DataFrame(data)

# Inizializza l'embedding e il vector store
emb = Embedding(embedding_type='fastembed')
vector_store = FaissStore(embedding_function=emb.get_embedding(), persist_directory=VECTOR_DIR, collection_name='my_collection')

# Aggiungi il dataframe al vector store
vector_store.add_dataframe(df, 'test_source')

# Verifica i documenti aggiunti
verify_documents(vector_store)

# Esegui una ricerca per verificare il contenuto
search_and_print(vector_store, 'Charlie salary')
