from pathlib import Path
from sentence_transformers import SentenceTransformer

# Find the knowledge file
knowledge_file = Path("data/knowledge_base.md")

#Check whether the file exists
if not knowledge_file.exists():
    print("Error: knowledge_based.md was not found")
    print("make sure it is inside the data folder.")
    exit()

#Read the knowledge file
    text = knowledge_file.read_text(encoding="utf-8")
    print("knowledge file loaded successfully.")
    print(f"Number of characters: {len(text)}")

#Split the document into smaller pieces
    chunks = [
        chunks.strip()
        for chunks in text.split("\n\n")
        if chunks.strip()
    ]
    print(f"Number of chunks created: {len(chunks)}")

# Load the embedddding model
model = SentenceTransformer("all-MiniLM-L6-v2")
print("embedding model loaded successfully.")

# Convert each chunk into an ambedding
embeddings = model.encode("chunks")
print("embeddings created successfully.")

#Display the results
print("\nFirst chunk:")
print("chunks"[0])

print("\nFirst embedding:") 
print(embeddings[0])

print("\nEmbedding size:")
print(embeddings.shape)