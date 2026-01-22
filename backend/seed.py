from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models

def seed_data():
    db = SessionLocal()
    
    # Check if data exists
    if db.query(models.MenuItem).count() > 0:
        print("Data already seeded!")
        return

    menu_items = {
        "mains": [
            {"name": "Grilled Chicken", "price": 12.99, "desc": "Tender grilled chicken breast with herbs"},
            {"name": "Beef Burger", "price": 10.99, "desc": "Juicy beef patty with fresh toppings"},
            {"name": "Fish & Chips", "price": 14.99, "desc": "Crispy battered fish with golden fries"},
            {"name": "Pasta Carbonara", "price": 11.99, "desc": "Classic Italian pasta with creamy sauce"},
            {"name": "Vegetarian Pizza", "price": 13.99, "desc": "Fresh vegetables on crispy crust"}
        ],
        "sides": [
            {"name": "French Fries", "price": 4.99, "desc": "Golden crispy potato fries"},
            {"name": "Onion Rings", "price": 5.99, "desc": "Crispy beer-battered onion rings"},
            {"name": "Garden Salad", "price": 6.99, "desc": "Fresh mixed greens with dressing"},
            {"name": "Mashed Potatoes", "price": 4.99, "desc": "Creamy whipped potatoes"},
            {"name": "Coleslaw", "price": 3.99, "desc": "Fresh cabbage slaw with tangy dressing"}
        ],
        "beverages": [
            {"name": "Coca Cola", "price": 2.99, "desc": "Classic refreshing cola"},
            {"name": "Orange Juice", "price": 3.99, "desc": "Fresh squeezed orange juice"},
            {"name": "Coffee", "price": 2.49, "desc": "Premium roasted coffee"},
            {"name": "Iced Tea", "price": 2.99, "desc": "Refreshing iced tea"},
            {"name": "Water", "price": 1.99, "desc": "Pure spring water"}
        ],
        "desserts": [
            {"name": "Chocolate Cake", "price": 6.99, "desc": "Rich chocolate layer cake"},
            {"name": "Ice Cream", "price": 4.99, "desc": "Creamy vanilla ice cream"},
            {"name": "Apple Pie", "price": 5.99, "desc": "Classic apple pie with cinnamon"},
            {"name": "Cheesecake", "price": 7.99, "desc": "New York style cheesecake"},
            {"name": "Cookies", "price": 3.99, "desc": "Freshly baked chocolate chip cookies"}
        ]
    }

    print("Seeding data...")
    for category, items in menu_items.items():
        for item in items:
            db_item = models.MenuItem(
                name=item["name"],
                category=category,
                price=item["price"],
                description=item["desc"]
            )
            db.add(db_item)
    
    db.commit()
    print("Seeding complete!")
    db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    seed_data()
