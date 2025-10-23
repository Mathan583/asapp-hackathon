import chromadb
from chromadb.config import Settings

class VectorDB:
    def __init__(self, path="data/chroma_airline"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection_name = "intent_vectors"
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Intent vectors for airline chatbot"}
            )

    def insert(self, vectors):
        # Generate unique IDs for the vectors
        import uuid
        ids = [str(uuid.uuid4()) for _ in vectors]
        
        # Insert vectors into ChromaDB
        self.collection.add(
            embeddings=vectors,
            ids=ids
        )
        return ids

    def search(self, query_vec, limit=2):
        # Search for similar vectors
        results = self.collection.query(
            query_embeddings=query_vec,
            n_results=limit
        )
        return results
