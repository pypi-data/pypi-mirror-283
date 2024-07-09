from datadashr.core.vector_stores import VectorStore
from datadashr.core.embeddings import Embedding
from datetime import datetime

# Inizializza l'embedding
emb = Embedding(embedding_type='fastembed')
embedding_function = emb.get_embedding()  # Ottieni l'oggetto embedding corretto

print(emb.model_info)

# Esempio per FAISS
store_faiss = VectorStore(store_type='faiss', embedding_function=embedding_function)
store_faiss.load_and_add_documents_from_directory('documents_directory', chunk_size=1000, chunk_overlap=0)
results = store_faiss.similarity_search("What did the president say about Ketanji Brown Jackson")
print("FAISS - Before deletion:")
print(results[0].page_content)
store_faiss.delete_documents_by_metadata(source="state_of_the_union.txt")
results = store_faiss.similarity_search("What did the president say about Ketanji Brown Jackson")
print("FAISS - After deletion:")
print(results[0].page_content if results else "No documents found.")

# Esempio per ChromaDB
store_chroma = VectorStore(store_type='chromadb', embedding_function=embedding_function, persist_directory='./chroma_db')
store_chroma.load_and_add_documents_from_directory('documents_directory', chunk_size=1000, chunk_overlap=0)
results = store_chroma.similarity_search("What did the president say about Ketanji Brown Jackson")
print("ChromaDB - Before deletion:")
print(results[0].page_content)
store_chroma.delete_documents_by_metadata(source="state_of_the_union.txt")
results = store_chroma.similarity_search("What did the president say about Ketanji Brown Jackson")
print("ChromaDB - After deletion:")
print(results[0].page_content if results else "No documents found.")

# Esempio per Pinecone
store_pinecone = VectorStore(store_type='pinecone', embedding_function=embedding_function, api_key='YOUR_PINECONE_API_KEY', index_name='langchain-index')
store_pinecone.load_and_add_documents_from_directory('documents_directory', chunk_size=1000, chunk_overlap=0)
results = store_pinecone.similarity_search("What did the president say about Ketanji Brown Jackson")
print("Pinecone - Before deletion:")
print(results[0].page_content)
store_pinecone.delete_documents_by_metadata(source="state_of_the_union.txt")
results = store_pinecone.similarity_search("What did the president say about Ketanji Brown Jackson")
print("Pinecone - After deletion:")
print(results[0].page_content if results else "No documents found.")

# Esempio per Elasticsearch
store_elastic = VectorStore(store_type='elasticsearch', embedding_function=embedding_function, hosts=["http://localhost:9200"], es_user='elastic', es_password='changeme', index_name='test_index')
store_elastic.load_and_add_documents_from_directory('documents_directory', chunk_size=1000, chunk_overlap=0)
results = store_elastic.similarity_search("What did the president say about Ketanji Brown Jackson")
print("Elasticsearch - Before deletion:")
print(results[0].page_content)
store_elastic.delete_documents_by_metadata(source="state_of_the_union.txt")
results = store_elastic.similarity_search("What did the president say about Ketanji Brown Jackson")
print("Elasticsearch - After deletion:")
print(results[0].page_content if results else "No documents found.")

# Esempio per Qdrant
store_qdrant = VectorStore(store_type='qdrant', embedding_function=embedding_function, url='YOUR_QDRANT_URL', api_key='YOUR_QDRANT_API_KEY', collection_name='my_documents')
store_qdrant.load_and_add_documents_from_directory('documents_directory', chunk_size=1000, chunk_overlap=0)
results = store_qdrant.similarity_search("What did the president say about Ketanji Brown Jackson")
print("Qdrant - Before deletion:")
print(results[0].page_content)
store_qdrant.delete_documents_by_metadata(source="state_of_the_union.txt")
results = store_qdrant.similarity_search("What did the president say about Ketanji Brown Jackson")
print("Qdrant - After deletion:")
print(results[0].page_content if results else "No documents found.")
