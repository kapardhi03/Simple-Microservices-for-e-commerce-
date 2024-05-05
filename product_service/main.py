from fastapi import FastAPI, HTTPException, Depends
from models import Product
from mongo import fetch_documents, insert_document, delete_document, update_document
from auth_service.main import oauth2_scheme

app = FastAPI()

@app.post("/products")
async def create_product(product: Product, token: str = Depends(oauth2_scheme)):
    result = insert_document("product_db", "products", product.dict())
    if result["status"]:
        return {"message": "Product created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error creating product")

@app.get("/products")
async def get_products(token: str = Depends(oauth2_scheme)):
    products = fetch_documents("product_db", "products", {})
    if products["status"]:
        return products["data"]
    else:
        raise HTTPException(status_code=500, detail="Error retrieving products")

@app.put("/products/{product_id}")
async def update_product(product_id: str, product: Product, token: str = Depends(oauth2_scheme)):
    result = update_document("product_db", "products", "_id", product_id, "price", product.price)
    if result["status"]:
        return {"message": "Product updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error updating product")

@app.delete("/products/{product_id}")
async def delete_product(product_id: str, token: str = Depends(oauth2_scheme)):
    result = delete_document("product_db", "products", {"_id": product_id})
    if result["status"]:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error deleting product")