import random

from database import SessionLocal
from models import Product

product_templates = {
    "Electronics": [
        ("Wireless Headphones", "Bluetooth over-ear headphones with clear sound"),
        ("Bluetooth Earbuds", "Compact wireless earbuds for everyday listening"),
        ("Gaming Mouse", "Ergonomic mouse with adjustable DPI"),
        ("Mechanical Keyboard", "Mechanical keyboard for gaming and coding"),
        ("Power Bank", "Portable fast-charging power bank"),
    ],

    "Footwear": [
        ("Walking Shoes", "Comfortable supportive shoes for long walks"),
        ("Running Shoes", "Lightweight cushioned shoes for jogging"),
        ("Casual Sneakers", "Everyday sneakers with soft cushioning"),
        ("Training Shoes", "Stable shoes for gym and workouts"),
    ],

    "Clothing": [
        ("Cotton T-Shirt", "Soft breathable cotton t-shirt"),
        ("Hoodie", "Warm casual hoodie for everyday wear"),
        ("Joggers", "Comfortable joggers for daily use"),
        ("Denim Jacket", "Classic casual denim jacket"),
    ],

    "Personal Care": [
        ("Shampoo", "Gentle shampoo for everyday hair care"),
        ("Face Moisturizer", "Lightweight moisturizer for daily skin hydration"),
        ("Face Wash", "Gentle cleanser for everyday facial care"),
        ("Body Lotion", "Moisturizing lotion for soft and smooth skin"),
    ],

    "Home": [
        ("Steel Water Bottle", "Insulated stainless steel bottle for daily use"),
        ("Table Lamp", "Compact LED lamp for study and work"),
        ("Storage Box", "Durable storage box for organizing household items"),
        ("Coffee Mug", "Reusable mug for hot and cold beverages"),
    ],

    "Accessories": [
        ("Laptop Backpack", "Water resistant backpack with padded laptop compartment"),
        ("Travel Pouch", "Compact organizer pouch for travel essentials"),
        ("Wallet", "Slim everyday wallet with multiple compartments"),
        ("Sunglasses", "Lightweight sunglasses for everyday outdoor use"),
    ]
}
variants = [
    "Classic",
    "Premium",
    "Lightweight",
    "Comfort",
    "Pro",
    "Everyday"
]
description_phrases = [
    "designed for everyday use",
    "with a comfortable and durable design",
    "suitable for daily activities",
    "with lightweight construction",
    "built for convenience and comfort"
]
price_ranges = {
    "Electronics": (800, 8000),
    "Footwear": (900, 4000),
    "Clothing": (400, 3000),
    "Personal Care": (200, 1500),
    "Home": (300, 3000),
    "Accessories": (300, 3500)
}
db=SessionLocal()
for i in range(200):
    category = random.choice(list(product_templates.keys()))
    base_name, base_description = random.choice(product_templates[category])
    variant=random.choice(variants)
    model_no = random.randint(100, 999)
    name = f"{variant} {base_name} {model_no}"
    description = (f"{base_description}, "
                   f"{random.choice(description_phrases)}"
                )
    min_price, max_price = price_ranges[category]
    price = random.randint(min_price, max_price)
    quantity = random.randint(0, 30)
    delivery_days = random.randint(1, 5)
    product=Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        category=category,
        delivery_days=delivery_days
    )
    existing=db.query(Product).filter(Product.name==name).first()
    if not existing:
        db.add(product)
db.commit()
db.close()

