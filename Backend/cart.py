from database import SessionLocal
from models import CartItem, Product

def get_user_cart(user_id):
    db = SessionLocal()
    cart_rows=db.query(CartItem).filter(CartItem.user_id==user_id).all()
    items=[]
    for row in cart_rows:
        product=db.query(Product).filter(Product.id==row.product_id).first()
        if product:
            items.append({
                "product_id":product.id,
                "product_name":product.name,
                "price":product.price,
                "quantity":row.quantity
            }
            )
    total_price=sum(item["price"]*item["quantity"] for item in items)
    db.close()
    return {"items":items, "total_price":total_price}


def add_to_cart(user_id, product_id, quantity=1):
    db=SessionLocal()
    
    product=db.query(Product).filter(Product.id==product_id).first()
    if not product:
        db.close()
        return {"message": "Product not found"}
    
    if quantity<=0:
        return {"message": "Quantity must be greater than 0"}
    
    existing_item=db.query(CartItem).filter(CartItem.user_id==user_id, CartItem.product_id==product_id).first()
    if existing_item:
        new_quantity=existing_item.quantity+quantity
        if new_quantity > product.quantity:
            return {"message": "Requested quantity exceeds available stock"}
        existing_item.quantity=new_quantity
    else:
        if quantity > product.quantity:
            return {"message": "Requested quantity exceeds available stock"}
        new_item=CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(new_item)

    db.commit()
    db.close()
    return get_user_cart(user_id)


def remove_from_cart(user_id,product_id):
    db=SessionLocal()
    cart_item=db.query(CartItem).filter(CartItem.user_id==user_id, CartItem.product_id==product_id).first()
    if not cart_item:
        db.close()
        return {"message": "Item not found in cart"}
    db.delete(cart_item)
    db.commit()
    db.close()
    return get_user_cart(user_id)

def update_cart_quantity(user_id, product_id, quantity):
    db=SessionLocal()
    
    if quantity<=0:
        db.close()
        return {"message":"Quantity must be greater than 0"}
    
    cart_item=db.query(CartItem).filter(CartItem.user_id==user_id, CartItem.product_id==product_id).first()
    product=db.query(Product).filter(Product.id==product_id).first()
    if not cart_item:
        db.close()
        return {"message":"Item not found in cart"}
    if not product:
        db.close()
        return {"message":"Product not found"}
        
    if quantity > product.quantity:
        return {"message": "Requested quantity exceeds available stock"}
    
    cart_item.quantity=quantity
    db.commit()
    db.close()
    return get_user_cart(user_id)


def clear_cart(user_id):
    db=SessionLocal()
    cart_items=db.query(CartItem).filter(CartItem.user_id==user_id).all()
    if not cart_items:
        db.close()
        return {"message": "Cart is already empty"}
    db.query(CartItem).filter(CartItem.user_id==user_id).delete()
    db.commit()
    db.close()
    return get_user_cart(user_id)
