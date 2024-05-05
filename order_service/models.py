from pydantic import BaseModel

class Order(BaseModel):
    user_id: str
    product_id: str
    quantity: int