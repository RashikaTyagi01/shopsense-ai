from intent_parser import parse_intent
from semantic_search import semantic_search
from reorder import get_last_purchase, get_previous_product
from cart import get_user_cart, add_to_cart

def handle_request(user_id: int, user_message: str):
    intent=parse_intent(user_message)
    request_type=intent["request_type"]

    if request_type == "discovery":
        discovery_result= semantic_search(intent["search_query"], max_price=intent["max_price"], max_delivery_days=intent["max_delivery_days"], exclude=intent["exclude"])
        cart=get_user_cart(user_id)
        return {"intent":intent, "discovery":discovery_result, "cart":cart}
    
    if request_type == "reorder":
        if intent["reorder_product"]:
            reorder_result= get_previous_product(user_id, intent["reorder_product"])
        else:
            reorder_result= get_last_purchase(user_id)
        if reorder_result:
            cart=add_to_cart(user_id,reorder_result["product_id"],reorder_result["quantity"])
        else:
            cart=get_user_cart(user_id)

        if not reorder_result:
            return {"intent": intent, "reorder": None, "message": "This item was not found in your purchase history."}
        
        return {"intent":intent, "reorder": reorder_result, "cart": cart}
        
    if request_type == "mixed":
        if intent["reorder_product"]:
            reorder_result = get_previous_product(user_id, intent["reorder_product"])
        else:
            reorder_result = get_last_purchase(user_id)

        if reorder_result:
            cart = add_to_cart(
                user_id,
                reorder_result["product_id"],
                reorder_result["quantity"]
            )
        else:
            cart = get_user_cart(user_id)
            
        discovery_result = semantic_search(intent["search_query"], max_price=intent["max_price"], max_delivery_days=intent["max_delivery_days"], exclude=intent["exclude"])
        return {"intent":intent, "reorder":reorder_result, "discovery":discovery_result, "cart":cart}

    
