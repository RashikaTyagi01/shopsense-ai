from database import SessionLocal
from models import Product, PurchaseHistory

def get_last_purchase(user_id:int):
    db = SessionLocal()
    last_purchase=(db.query(PurchaseHistory).filter(PurchaseHistory.user_id==user_id).order_by(PurchaseHistory.purchase_date.desc()).first())
    if not last_purchase:
        db.close()
        return None
    product = db.query(Product).filter(Product.id==last_purchase.product_id).first()
    db.close()
    if not product:
        return None
    return {
        "product_id": product.id,
        "product_name": product.name,
        "price": product.price,
        "quantity": last_purchase.quantity,
        "purchase_date": last_purchase.purchase_date
    }


#reorder func for specific product reorder requested by user using product name
def get_previous_product(user_id: int, product_name: str):
    db=SessionLocal()
    history=db.query(PurchaseHistory).filter(PurchaseHistory.user_id==user_id).order_by(PurchaseHistory.purchase_date.desc()).all()
    for item in history:
        product=db.query(Product).filter(Product.id==item.product_id).first()
        if product and product_name.lower() in product.name.lower():
            db.close()
            return {
                "product_id": product.id,
                "product_name": product.name,
                "price": product.price,
                "quantity": item.quantity,
                "purchase_date": item.purchase_date
            }
    db.close()
    return None