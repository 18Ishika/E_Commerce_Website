from langchain_huggingface import HuggingFaceEmbeddings  # Changed this import
from langchain_community.vectorstores import FAISS

INDEX_PATH = "chat/vectorstore"

def retrieve_context(query, k=3):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(
        INDEX_PATH, 
        embeddings,
        allow_dangerous_deserialization=True  # Added this parameter
    )
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])

if __name__ == "__main__":
    q = input("Ask something: ")
    context = retrieve_context(q)
    print("\n--- Retrieved Context ---")
    print(context)