import json
import time

from database import SessionLocal
from models import Product
from semantic_search import get_embedding


db = SessionLocal()

products = db.query(Product).filter(Product.embedding == None).all()

print(f"Products without embeddings: {len(products)}")

for i, product in enumerate(products, start=1):
    text = f"{product.name}. {product.description}. Category: {product.category}"

    embedding = get_embedding(text)

    product.embedding = json.dumps(embedding)
    db.commit()

    print(f"Embedded {i}/{len(products)}: {product.name}")

    # avoid hitting Gemini free-tier rate limits
    if i % 80 == 0:
        print("Waiting for rate limit...")
        time.sleep(65)

db.close()

print("Embedding generation complete.")