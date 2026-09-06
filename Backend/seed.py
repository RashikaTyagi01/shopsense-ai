from database import SessionLocal
from models import Product

db=SessionLocal()
products = [
    Product(
        name="Bluetooth Earbuds",
        description="Compact wireless earbuds with clear audio",
        price=1499,
        quantity=20,
        category="Electronics",
        delivery_days=1
    ),

    Product(
        name="Running Shoes",
        description="Lightweight cushioned shoes for jogging and daily runs",
        price=2499,
        quantity=10,
        category="Footwear",
        delivery_days=2
    ),

    Product(
        name="Gaming Mouse",
        description="Ergonomic RGB gaming mouse with adjustable DPI",
        price=1299,
        quantity=15,
        category="Electronics",
        delivery_days=2
    ),

    Product(
        name="Mechanical Keyboard",
        description="Mechanical keyboard suitable for gaming and coding",
        price=3499,
        quantity=8,
        category="Electronics",
        delivery_days=3
    ),

    Product(
    name="Walking Shoes",
    description="Soft supportive shoes for long walks",
    price=1999,
    quantity=14,
    category="Footwear",
    delivery_days=1
    ),

Product(
    name="Cotton T-Shirt",
    description="Soft breathable cotton t-shirt",
    price=699,
    quantity=30,
    category="Clothing",
    delivery_days=1
),

Product(
    name="Laptop Backpack",
    description="Water resistant backpack with padded laptop compartment",
    price=1499,
    quantity=18,
    category="Accessories",
    delivery_days=2
),

Product(
    name="Shampoo",
    description="Gentle daily shampoo for healthy hair",
    price=349,
    quantity=35,
    category="Personal Care",
    delivery_days=1
),

Product(
    name="Face Moisturizer",
    description="Lightweight daily moisturizer for dry skin",
    price=599,
    quantity=20,
    category="Personal Care",
    delivery_days=2
),

Product(
    name="Steel Water Bottle",
    description="Insulated stainless steel water bottle",
    price=899,
    quantity=25,
    category="Home",
    delivery_days=1
)
]
for product in products:
    existing=db.query(Product).filter(Product.name==product.name).first()
    if not existing:
        db.add(product)

db.commit()
db.close()