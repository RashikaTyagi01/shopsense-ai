from fastapi import FastAPI
from database import engine,Base,SessionLocal
from models import Product, PurchaseHistory, CartItem
from semantic_search import semantic_search
from reorder import get_last_purchase, get_previous_product
from assistant_service import handle_request
from cart import get_user_cart, add_to_cart, remove_from_cart, update_cart_quantity, clear_cart
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


Base.metadata.create_all(bind=engine)


@app.get("/")   
def home():
    return {"message":"Shopping Assistant API"}     


@app.get("/products")
def get_all_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int):
    db=SessionLocal()
    product=db.query(Product).filter(Product.id==id).first()
    db.close()
    if product:
        return product
    return {"message": "Product Not Found"}

@app.get("/products/filter/")
def filter_products(max_price: float=None, max_delivery_days: int=None, exclude: str=None):
    db=SessionLocal()
    query=db.query(Product)
    if max_price is not None:
        query=query.filter(Product.price<=max_price)
    if max_delivery_days is not None:
        query=query.filter(Product.delivery_days<=max_delivery_days)
    query=query.filter(Product.quantity>0)
    products=query.all()
    if exclude:
        products=[
            p for p in products
            if exclude.lower() not in p.name.lower()
            and exclude.lower() not in p.description.lower()
        ]
    db.close()
    return products

@app.get("/semantic-search/")
def search(query: str,max_price: float=None, max_delivery_days: int=None, exclude: str=None):
    results = semantic_search(query, max_price=max_price, max_delivery_days=max_delivery_days, exclude=exclude)
    if not results:
        return {"message":"No matching products found"}
    return results

@app.get("/history/{user_id}")
def get_history(user_id: int):
    db=SessionLocal()
    history=db.query(PurchaseHistory).filter(PurchaseHistory.user_id==user_id).all()
    results=[]
    for item in history:
        product=db.query(Product).filter(Product.id==item.product_id).first()
        results.append({
            "purchase_id": item.id,
            "product_id": item.product_id,
            "product_name": product.name if product else None,
            "quantity": item.quantity,
            "purchase_date": item.purchase_date
        })
    db.close()
    return results


@app.get("/reorder/{user_id}")
def reorder(user_id: int):
    result=get_last_purchase(user_id)
    if not result:
        return {"message":"No previous purchase found"}
    return result


@app.get("/reorder/{user_id}/{product_name}")
def reorder_product(user_id: int, product_name: str):
    result = get_previous_product(user_id,product_name)
    if not result:
        return {"message":"Product not found in purchase history"}
    return result


@app.get("/assistant")
def shopping_assistant(user_id: int, message: str):
    return handle_request(user_id,message)

@app.post("/cart/add/")
def add_product_to_cart(user_id: int, product_id: int, quantity: int=1):
    db=SessionLocal()
    product=db.query(Product).filter(Product.id==product_id).first()
    db.close()
    if not product:
        return {"message": "Product not found"}
    return add_to_cart(
        user_id,
        product_id,
        quantity
    )


@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    return get_user_cart(user_id)


@app.delete("/cart/remove/")
def remove_product_from_cart(user_id: int, product_id: int):
    return remove_from_cart(user_id,product_id)


@app.put("/cart/update/")
def update_product_quantity(user_id: int, product_id: int, quantity: int):
    return update_cart_quantity(user_id,product_id,quantity)


@app.delete("/cart/clear/{user_id}")
def clear_user_cart(user_id:int):
    return clear_cart(user_id)

