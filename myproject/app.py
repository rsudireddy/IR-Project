import pickle

# Load the index.pkl file
with open('index.pkl', 'rb') as f:
    index = pickle.load(f)

# Print the contents of index.pkl
for idx, doc_info in index.items():
    print(f"Document at index {idx}:")
    print(doc_info)
    print()  # Add a blank line for readability
