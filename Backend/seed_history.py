from database import SessionLocal
from models import PurchaseHistory

db=SessionLocal()
# purchase = PurchaseHistory(
#     user_id=1,
#     product_id=6,
#     quantity=1,
#     purchase_date="2026-09-01"
# )
# db.add(purchase)
# db.commit()


purchase = PurchaseHistory(
    user_id=1,
    product_id=8,
    quantity=1,
    purchase_date="2026-08-25"
)
existing = db.query(PurchaseHistory).filter(PurchaseHistory.user_id==purchase.user_id, PurchaseHistory.product_id==purchase.product_id, PurchaseHistory.purchase_date==purchase.purchase_date).first()
if not existing:
    db.add(purchase)
db.commit()
db.close()