import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from TopRanker import TopRanker


def semantic_search(query, products, top_k=3):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    query_embedding = model.encode([query])[0]

    result_data_structure = TopRanker(top_k)

    for row in products:
        phone_id, name, brand, specifications, price, embedding_data = row
        embedding = np.frombuffer(embedding_data, dtype=np.float32)
        similarity = cosine_similarity([query_embedding], [embedding])[0][0]
        tuple = (phone_id, name, brand, specifications, price, similarity)
        result_data_structure.update_if_greater(tuple, is_greeater=lambda x, y: x[5] > y[5])
    results = result_data_structure.get_data()

    return str(results)
