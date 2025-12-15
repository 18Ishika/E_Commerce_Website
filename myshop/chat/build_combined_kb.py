import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS
from products.models import Product

MANUAL_PATH = "chat/manual/shopzy_manual.txt"

def load_manual(path=MANUAL_PATH):
    if not os.path.exists(path):
        print(f"Warning: Manual file not found at {path}")
        return ""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def build_knowledge_base():
    print("Loading manual...")
    manual_text = load_manual()
    
    print("Fetching products from database...")
    products = Product.objects.all()
    
    product_texts = []
    for product in products:
        product_text = f"""
        Product: {product.name}
        Category: {product.category.name if hasattr(product, 'category') else 'N/A'}
        Price: ${product.price}
        Description: {product.description}
        """
        product_texts.append(product_text)
    
    all_text = manual_text + "\n\n" + "\n\n".join(product_texts)
    
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(all_text)
    
    print(f"Created {len(chunks)} chunks")
    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    print("Building FAISS index...")
    vectorstore = FAISS.from_texts(chunks, embeddings)
    
    vectorstore.save_local("chat/vectorstore")
    print("Knowledge base saved successfully!")

if __name__ == "__main__":
    build_knowledge_base()