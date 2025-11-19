from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta

app = FastAPI()

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total_amount: float = 0.0
    deliveryDate: datetime

orders: Dict[int, Order] = {}
order_id_counter = 0  # глобальний лічильник ID

@app.get("/orders", response_model=List[Order])
def get_all_orders():
    return list(orders.values())

@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order_items: List[OrderItem]):
    global order_id_counter
    order_id_counter += 1
    new_id = order_id_counter

    delivery_date = datetime.now() + timedelta(days=5)

    new_order = Order(
        id=new_id,
        items=order_items,
        deliveryDate=delivery_date
    )

    orders[new_id] = new_order
    return new_order

@app.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    del orders[order_id]
    return