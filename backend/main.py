from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from . import models, database
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Modern Cafeteria API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class MenuItemBase(BaseModel):
    name: str
    category: str
    price: float
    description: str
    image_url: Optional[str] = None

class MenuItem(MenuItemBase):
    id: int
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    name: str
    price: float
    quantity: int
    subtotal: float

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    total_amount: float

class Order(BaseModel):
    id: int
    total_amount: float
    status: str
    class Config:
        from_attributes = True

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/menu", response_model=List[MenuItem])
def get_menu(db: Session = Depends(get_db)):
    return db.query(models.MenuItem).all()

@app.get("/menu/{category}", response_model=List[MenuItem])
def get_menu_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(models.MenuItem).filter(models.MenuItem.category == category).all()

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(total_amount=order.total_amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            item_name=item.name,
            price=item.price,
            quantity=item.quantity,
            subtotal=item.subtotal
        )
        db.add(db_item)
    
    db.commit()
    return db_order
