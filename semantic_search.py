import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_search(query, products, top_k=3):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    query_embedding = model.encode([query])[0]

    results = []

    for row in products:
        phone_id, name, brand, specifications, price, embedding_data = row
        embedding = np.frombuffer(embedding_data, dtype=np.float32)
        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
        results.append((phone_id, name, brand, specifications, price, similarity))

    # Sort results based on similarity score
    results = sorted(results, key=lambda x: x[5], reverse=True)

    # Return top-k matching mobile phones
    top_results = results[:top_k]

    return str(top_results)

