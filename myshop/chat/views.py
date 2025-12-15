import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from products.models import Product
from .models import ChatMessage

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# FAISS knowledge base path
KB_INDEX_PATH = "chat/vectorstore"

# Initialize embeddings and vectorstore (lazy loading)
_embeddings = None
_vectorstore = None

def get_vectorstore():
    """Lazy load the vectorstore to avoid loading it at import time"""
    global _embeddings, _vectorstore
    if _vectorstore is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        _vectorstore = FAISS.load_local(
            KB_INDEX_PATH, 
            _embeddings,
            allow_dangerous_deserialization=True
        )
    return _vectorstore


# -------------------- Helper Functions --------------------

def retrieve_manual_context(query, k=3):
    """Retrieve context from the manual using FAISS vector search"""
    try:
        vectorstore = get_vectorstore()
        results = vectorstore.similarity_search(query, k=k)
        return "\n".join([r.page_content for r in results])
    except Exception as e:
        print(f"Error retrieving manual context: {e}")
        return ""


def retrieve_product_context(query):
    """Search products in database based on query"""
    try:
        products = Product.objects.filter(name__icontains=query)[:5]
        if not products:
            return ""
        
        lines = []
        for p in products:
            lines.append(
                f"Product Name: {p.name}\n"
                f"Category: {p.category.name if p.category else 'N/A'}\n"
                f"Price: ${p.price}\n"
                f"Availability: {'In stock' if p.stock > 0 else 'Out of stock'}\n"
                f"Description: {p.description}"
            )
        return "\n\n".join(lines)
    except Exception as e:
        print(f"Error retrieving product context: {e}")
        return ""


def retrieve_order_context(user, query):
    """Retrieve user's order history (requires Order and OrderItem models)"""
    try:
        from .models import Order, OrderItem
        orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
        if not orders:
            return ""
        
        lines = []
        for order in orders:
            for item in OrderItem.objects.filter(order=order):
                if query.lower() in item.product.name.lower():
                    lines.append(
                        f"Order ID: {order.id}\n"
                        f"Product: {item.product.name}\n"
                        f"Quantity: {item.quantity}\n"
                        f"Status: {order.status}"
                    )
        return "\n\n".join(lines)
    except ImportError:
        return ""
    except Exception as e:
        print(f"Error retrieving order context: {e}")
        return ""


def generate_with_gemini_flash(prompt: str):
    """
    Generate text using Gemini 2.0 Flash model via Google Generative AI SDK
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not configured in .env file"
    
    try:
        # Initialize the model with configuration
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )
        
        # Generate response
        response = model.generate_content(prompt)
        
        # Extract text from response
        if response and response.text:
            return response.text
        else:
            return "Sorry, I couldn't generate a response. Please try again."
            
    except Exception as e:
        error_msg = str(e)
        
        # Handle specific error cases
        if "429" in error_msg or "quota" in error_msg.lower():
            return "⏳ I'm experiencing high traffic. Please wait a moment and try again."
        elif "API key" in error_msg:
            return "Error: Invalid API key. Please check your configuration."
        else:
            print(f"Gemini API error: {error_msg}")
            return f"Sorry, I encountered an error. Please try again later."


# -------------------- Views --------------------

@csrf_exempt
def chatbot_api(request):
    """
    Main chatbot API endpoint with RAG (Retrieval Augmented Generation)
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
    try:
        data = json.loads(request.body)
        query = data.get("message", "").strip()
        
        if not query:
            return JsonResponse({"reply": "Please type something."})
        
        # Retrieve contexts from different sources
        manual_ctx = retrieve_manual_context(query)
        product_ctx = retrieve_product_context(query)
        
        # Only get order context if user is authenticated
        order_ctx = ""
        if request.user.is_authenticated:
            order_ctx = retrieve_order_context(request.user, query)
        
        # Combine all contexts
        context_parts = [manual_ctx, product_ctx, order_ctx]
        combined_context = "\n---\n".join([ctx for ctx in context_parts if ctx])
        
        # Build the prompt for Gemini
        if combined_context:
            prompt = (
                f"You are a helpful e-commerce assistant for Shopzy.\n\n"
                f"Context from our knowledge base:\n{combined_context}\n\n"
                f"User question: {query}\n\n"
                f"Answer concisely and helpfully based on the context provided. "
                f"If the context doesn't contain relevant information, say so politely."
            )
        else:
            # If no context found, still try to help
            prompt = (
                f"You are a helpful e-commerce assistant for Shopzy.\n\n"
                f"User question: {query}\n\n"
                f"Answer helpfully. If you don't have specific information, "
                f"let them know politely and offer general assistance."
            )
        
        # Generate response using Gemini
        reply = generate_with_gemini_flash(prompt)
        
        # Save chat message to database
        try:
            ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=query,
                response=reply
            )
        except Exception as e:
            print(f"Error saving chat message: {e}")
        
        return JsonResponse({"reply": reply})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        print(f"Chatbot API error: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def chatbot_test_page(request):
    """Render the chatbot test page"""
    return render(request, "chat/test.html")