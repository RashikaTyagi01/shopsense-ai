from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

from database import SessionLocal
from models import Product
import json


load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    result=client.models.embed_content(
         model="gemini-embedding-001",
         contents=text,
         config=types.EmbedContentConfig(
              task_type="SEMANTIC_SIMILARITY",
              output_dimensionality=768
         )
    )
    return result.embeddings[0].values


def get_product_embeddings(products):
    texts = [
        f"{product.name}. {product.description}. Category: {product.category}"
        for product in products
    ]

    all_embeddings = []

    for i in range(0, len(texts), 100):
        batch = texts[i:i + 100]

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=batch,
            config=types.EmbedContentConfig(
                task_type="SEMANTIC_SIMILARITY",
                output_dimensionality=768
            )
        )

        all_embeddings.extend(
            embedding.values for embedding in result.embeddings
        )

    return all_embeddings



def semantic_search(query, top_k=3, threshold=0.4, max_price=None, max_delivery_days=None, exclude=None):
    db=SessionLocal()
    products=db.query(Product).all()
    if max_price is not None:
        products = [
            product for product in products
            if product.price <= max_price
        ]

    if max_delivery_days is not None:
        products = [
            product for product in products
            if product.delivery_days <= max_delivery_days
        ]

    if exclude:
        products = [
            product for product in products
            if exclude.lower() not in product.name.lower()
            and exclude.lower() not in product.description.lower()
        ]
    
    products = [
        product for product in products
        if product.quantity > 0
    ]
    products=[
        product for product in products
        if product.embedding
    ]
    if not products:
        db.close()
        return []
    
    product_embeddings=[
        json.loads(product.embedding)
        for product in products
    ]
    
    query_embedding=get_embedding(query)
    
    scores=cosine_similarity([query_embedding], product_embeddings)
    final_results=[]
    results=list(zip(products,scores[0]))
    results.sort(key=lambda x: x[1], reverse=True)
    for product, score in results[:top_k]:
        if float(score) >= threshold:
                final_results.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "delivery_days": product.delivery_days,
                    "score": float(score)
                })
    db.close()
    return final_results




    
