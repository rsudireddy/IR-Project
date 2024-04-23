import pickle
import os

index_path = os.path.join(os.path.dirname(__file__), '..' ,'spiders', 'index.pkl')

with open(index_path, 'rb') as f:
    index = pickle.load(f)


for idx, doc_info in index.items():
    print(f"Document at index {idx}:")
    print(doc_info)
    print()  
