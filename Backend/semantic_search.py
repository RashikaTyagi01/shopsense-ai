from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from database import SessionLocal
from models import Product

model=SentenceTransformer("all-MiniLM-L6-v2")

embedding_cache={}

def get_product_embedding(product):
     if product.id not in embedding_cache:
          text = f"{product.name}. {product.description}. Category: {product.category}"
          embedding_cache[product.id] = model.encode(text)
     return embedding_cache[product.id]

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
    if not products:
        db.close()
        return []
    
    product_embeddings=[get_product_embedding(product) for product in products]
    query_embedding=model.encode(query)
    
    scores=cos_sim(query_embedding, product_embeddings)
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




    
