import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from products.models import Product
from .models import ChatMessage

# -------------------------------------------------
# ENV & GEMINI CONFIG
# -------------------------------------------------

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# -------------------------------------------------
# FAISS VECTOR STORE (MANUAL / FAQ / DOCS)
# -------------------------------------------------

KB_INDEX_PATH = "chat/vectorstore"

_embeddings = None
_vectorstore = None


def get_vectorstore():
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


def retrieve_manual_context(query, k=3):
    try:
        vectorstore = get_vectorstore()
        results = vectorstore.similarity_search(query, k=k)
        return "\n".join([r.page_content for r in results])
    except Exception as e:
        print("Manual context error:", e)
        return ""


# -------------------------------------------------
# PRODUCT & REVIEW CONTEXT (CATALOG ONLY)
# -------------------------------------------------

def retrieve_product_context(query):
    products = Product.objects.filter(name__icontains=query)[:5]

    if not products.exists():
        return ""

    lines = ["Product catalog details:"]
    for p in products:
        lines.append(
            f"""
Product Name: {p.name}
Price: ₹{p.price}
Category: {p.category.name if p.category else "N/A"}
Stock Available: {p.stock}
"""
        )
    return "\n".join(lines)


def retrieve_review_context(query):
    from products.models import Review

    reviews = Review.objects.filter(
        product__name__icontains=query
    ).select_related("product")[:3]

    if not reviews.exists():
        return ""

    lines = ["Customer reviews:"]
    for r in reviews:
        lines.append(
            f"- {r.product.name}: {r.rating}★ — {r.review_text}"
        )

    return "\n".join(lines)


# -------------------------------------------------
# GEMINI FLASH GENERATION
# -------------------------------------------------

def generate_with_gemini_flash(prompt: str):
    if not GEMINI_API_KEY:
        return "Error: Gemini API key is not configured."

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.6,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
        )

        response = model.generate_content(prompt)

        if response and response.text:
            return response.text

        return "Sorry, I couldn't generate a response."

    except Exception as e:
        msg = str(e).lower()
        print("Gemini error:", e)

        if "quota" in msg or "429" in msg:
            return "⏳ I'm a bit busy right now. Please try again shortly."
        elif "api key" in msg:
            return "Invalid API key. Please check configuration."
        else:
            return "Something went wrong while generating a reply."


# -------------------------------------------------
# CHATBOT API VIEW (CATALOG BOT)
# -------------------------------------------------

@csrf_exempt
def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body)
        query = data.get("message", "").strip()

        if not query:
            return JsonResponse({"reply": "Please enter a message."})

        contexts = [
            retrieve_manual_context(query),
            retrieve_product_context(query),
            retrieve_review_context(query),
        ]
        memory=chat_memory(request)
        combined_context = "\n---\n".join([c for c in contexts if c])

        prompt = f"""
You are a smart e-commerce product assistant for Shopzy.

Rules:
- Answer ONLY using product catalog, stock, category, pricing, or reviews.
- THe prices listed are in rupees.
-If you dont know the answer reply apologetically and provide clear response.
- Do NOT talk about user accounts, carts, orders, or payments.
- If stock is unavailable or low, mention it clearly.
- If the product is not found, say so politely.

Conversation history:
{memory}
Context:
{combined_context}

User Question:
{query}


Provide a clear and helpful response.
"""

        reply = generate_with_gemini_flash(prompt)
        chat_memory(request, query, reply)

        ChatMessage.objects.create(
            user=None,
            message=query,
            response=reply
        )

        return JsonResponse({"reply": reply})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        print("Chatbot API error:", e)
        return JsonResponse({"error": "Internal server error"}, status=500)


# -------------------------------------------------
# TEST PAGE
# -------------------------------------------------

def chatbot_test_page(request):
    return render(request, "chat/test.html")

def chat_memory(request,user_msg=None,bot_msg=None):
    memory=request.session.get("chat_memory",[])
    if user_msg and bot_msg:
        memory.append(f"User: {user_msg}\nAssistant: {bot_msg}")
        memory=memory[-6:]
        request.session["chat_memory"]=memory
        request.session.modified=True
    return "\n".join(memory)