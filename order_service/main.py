from fastapi import FastAPI, HTTPException, Depends
from models import Order
import mongo
from auth_utils import oauth2_scheme

app = FastAPI()



@app.post("/orders")
async def create_order(order: Order, token: str = Depends(oauth2_scheme)):
    product = mongo.fetch_documents("product_db", "products", {"_id": order.product_id})
    if not product["status"] or len(product["data"]) == 0:
        raise HTTPException(status_code=400, detail="Invalid product")
    
    if product["data"][0]["quantity"] < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient product quantity")
    # Create order
    result = mongo.insert_document("order_db", "orders", dict(order))
    if result["status"]:
        # Update product quantity
        mongo.update_document("product_db", "products", "_id", order.product_id, "quantity", product["data"][0]["quantity"] - order.quantity)
        return {"message": "Order created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error creating order")

@app.get("/orders")
async def get_orders(token: str = Depends(oauth2_scheme)):
    orders = mongo.fetch_documents("order_db", "orders", {"user_id": token})
    if orders["status"]:
        return orders["data"]
    else:
        raise HTTPException(status_code=500, detail="Error retrieving orders")