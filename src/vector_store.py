import chromadb 
from sentence_transformers import SentenceTransformer

# Use the same model used when creating the database
model = SentenceTransformer("all-MiniLM-L6-v2")

#open the saved vector database
client = chromadb.PersistentClient(path="data/vector_db")
collection = client.get_collection(name="Rupsa_Sacco")

def search_sacco(question, results_count=3):
    """search the VectorDB for the most relevant SACCO information."""
    question_vector = model.encode(question).tolist()
    return collection.query(query_embeddings=[question_vector], n_results=results_count)

if __name__ == "__main__":
    question = input("Ask Rupsa Sacco question:").strip()
if not question:
    print("Please enter a question.")
    raise SystemExit

results = search_sacco(question)
print("\nRELEVANT SACCO INFORMATION")
print("=" * 60)

for i, document in enumerate(results["documents"][0], 1):
    source = results["metadatas"][0][i - i]["source"]
print(f"\nRESULT {i}")
print(f"source: {source}")
print(document)
print("-" * 60)