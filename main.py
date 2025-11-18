from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict
import threading

# Створення екземпляру FastAPI
app = FastAPI()

# --- Моделі даних за допомогою Pydantic ---
# Pydantic забезпечує валідацію типів та автоматичну серіалізацію/десеріалізацію
class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total_amount: float = 0.0

# --- Сховище в пам'яті ---
orders: Dict[int, Order] = {}
order_id_counter = threading.local()
order_id_counter.value = 0

# --- Ендпоінти (Path Operations) ---

# GET /orders - отримати всі замовлення
@app.get("/orders", response_model=List[Order])
def get_all_orders():
    return list(orders.values())

# POST /orders - створити нове замовлення
@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order_items: List[OrderItem]):
    order_id_counter.value += 1
    new_id = order_id_counter.value
    # У реальному застосунку тут буде логіка розрахунку total_amount
    new_order = Order(id=new_id, items=order_items)
    orders[new_id] = new_order
    return new_order

# GET /orders/{order_id} - отримати замовлення за ID
@app.get("/orders/{order_id}", response_model=Order)
def get_order_by_id(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return orders[order_id]

# DELETE /orders/{order_id} - видалити замовлення
@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    if order_id not in orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    del orders[order_id]
    return


