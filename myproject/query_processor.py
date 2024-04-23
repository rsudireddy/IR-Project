import os
import pickle
from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Determine the path to index.pkl
index_path = os.path.join(os.path.dirname(__file__), 'spiders', 'index.pkl')

# Load the index.pkl file
with open(index_path, 'rb') as f:
    index = pickle.load(f)

# Continue with your Flask app setup
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([doc['document'] for doc in index.values()])

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    query_json = request.json
    query = query_json.get('query', '')

    query_vector = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    k = min(5, len(cosine_similarities))
    top_k_indices = cosine_similarities.argsort()[-k:][::-1]

    # Extract the required fields (cosine similarity, document name, and first 100 characters of the document)
    results = [{'cosine_similarity': cosine_similarities[idx], 
                'document_name': index[idx]['document_name'], 
                'snippet': index[idx]['document'][:100]} for idx in top_k_indices]
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
