from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from app.config import settings
import numpy as np
from typing import List, Dict, Any
import uuid

# Initialize Pinecone with new API - handle dummy credentials gracefully
try:
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    pinecone_available = True
except Exception as e:
    print(f"Pinecone initialization failed (using dummy credentials): {e}")
    pc = None
    pinecone_available = False

# 2. Initialize Sentence Transformer model
# Using 'all-MiniLM-L6-v2' which produces 384-dimensional vectors
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading SentenceTransformer model: {e}")
    # A real app might have better error handling or a fallback.
    model = None

INDEX_NAME = settings.INDEX_NAME

# In-memory storage for testing without Pinecone
in_memory_documents = []
in_memory_embeddings = []

MIN_SIMILARITY_THRESHOLD = 0.4 # Only return results above this similarity

def create_pinecone_index_if_not_exists():
    """
    Checks if the target Pinecone index exists, and creates it if it doesn't.
    """
    if not pinecone_available:
        print("Pinecone not available (using dummy credentials). Using in-memory storage.")
        return
        
    if model is None:
        print("SentenceTransformer model not loaded. Cannot create index.")
        return
        
    try:
        if pc is None:
            print("Pinecone client is None. Using in-memory storage.")
            return
            
        if INDEX_NAME not in pc.list_indexes().names():
            print(f"Index '{INDEX_NAME}' not found. Creating a new one...")
            pc.create_index(
                name=INDEX_NAME,
                dimension=model.get_sentence_embedding_dimension(),
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            print(f"Index '{INDEX_NAME}' created successfully.")
        else:
            print(f"Index '{INDEX_NAME}' already exists.")
    except Exception as e:
        print(f"Error creating Pinecone index (using dummy credentials): {e}")

def embed_and_store(doc_id: str, text: str):
    """
    Embeds a chunk of text and stores it in the Pinecone index or in-memory storage.
    """
    if model is None:
        raise Exception("SentenceTransformer model is not available.")

    try:
        # Create embedding
        embedding = model.encode(text).tolist()
        
        # Store in Pinecone if available
        if pinecone_available and pc is not None:
            try:
                index = pc.Index(INDEX_NAME)
                index.upsert(vectors=[(doc_id, embedding, {"text": text})])
                print(f"Successfully embedded and stored document chunk: {doc_id}")
            except Exception as e:
                print(f"Error storing in Pinecone: {e}")
                # Fall back to in-memory storage
                store_in_memory(doc_id, text, embedding)
        else:
            # Use in-memory storage
            store_in_memory(doc_id, text, embedding)
            
    except Exception as e:
        print(f"Error creating embedding: {e}")
        raise

def store_in_memory(doc_id: str, text: str, embedding: List[float]):
    """
    Store document in in-memory storage for testing.
    """
    global in_memory_documents, in_memory_embeddings
    
    if model is None:
        print("Model not available for embedding")
        return
    
    # Split text into chunks for better search
    chunks = split_text_into_chunks(text, max_chunk_size=1000)
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc_id}_chunk_{i}"
        chunk_embedding = model.encode(chunk).tolist()
        
        in_memory_documents.append({
            "id": chunk_id,
            "text": chunk,
            "metadata": {"text": chunk, "doc_id": doc_id}
        })
        in_memory_embeddings.append(chunk_embedding)
    
    print(f"Stored document {doc_id} in memory with {len(chunks)} chunks")

def split_text_into_chunks(text: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Split text into smaller chunks for better search results.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        if current_size + len(word) + 1 > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = len(word)
        else:
            current_chunk.append(word)
            current_size += len(word) + 1
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def search_documents(query: str, top_k: int = 5):
    """
    Embeds a query and searches for similar documents in Pinecone or in-memory storage.
    """
    if model is None:
        raise Exception("SentenceTransformer model is not available.")
        
    try:
        query_embedding = model.encode(query).tolist()
        
        # Try Pinecone first
        if pinecone_available and pc is not None:
            try:
                index = pc.Index(INDEX_NAME)
                results = index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True
                )
                # Handle different Pinecone result formats and ensure JSON serializable
                if hasattr(results, 'matches'):
                    matches = results.matches
                elif isinstance(results, dict) and 'matches' in results:
                    matches = results['matches']
                else:
                    matches = []
                
                # Convert to proper format and filter by similarity threshold
                formatted_results = []
                for match in matches:
                    score = float(match.score)
                    if score >= MIN_SIMILARITY_THRESHOLD:
                        formatted_results.append({
                            "id": str(match.id),
                            "score": score,
                            "metadata": {
                                "text": str(match.metadata.get("text", "")),
                                "doc_id": str(match.metadata.get("doc_id", ""))
                            }
                        })
                return formatted_results
            except Exception as e:
                print(f"Error searching Pinecone: {e}")
                # Fall back to in-memory search
                return search_in_memory(query_embedding, top_k)
        else:
            # Use in-memory search
            return search_in_memory(query_embedding, top_k)
            
    except Exception as e:
        print(f"Error searching documents: {e}")
        return []

def search_in_memory(query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
    """
    Search documents stored in memory using cosine similarity.
    """
    if not in_memory_embeddings:
        return []
    
    # Calculate cosine similarities
    similarities = []
    for i, doc_embedding in enumerate(in_memory_embeddings):
        similarity = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((similarity, i))
    
    # Sort by similarity and get top_k results
    similarities.sort(reverse=True)
    results = []
    
    count = 0
    for similarity, idx in similarities:
        if similarity >= MIN_SIMILARITY_THRESHOLD:
            doc = in_memory_documents[idx]
            results.append({
                "id": str(doc["id"]),
                "score": float(similarity),
                "metadata": {
                    "text": str(doc["metadata"]["text"]),
                    "doc_id": str(doc["metadata"]["doc_id"])
                }
            })
            count += 1
            if count >= top_k:
                break
    
    return results

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    vec1_array = np.array(vec1)
    vec2_array = np.array(vec2)
    
    dot_product = np.dot(vec1_array, vec2_array)
    norm1 = np.linalg.norm(vec1_array)
    norm2 = np.linalg.norm(vec2_array)
    
    if norm1 == 0 or norm2 == 0:
        return 0
    
    return float(dot_product / (norm1 * norm2)) 