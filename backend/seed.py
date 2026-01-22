from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine
from backend import models
import urllib.parse

import random

def get_image_url(name):
    query = urllib.parse.quote(name)
    seed = random.randint(0, 10000)
    return f"https://image.pollinations.ai/prompt/photorealistic%20real%20photo%20of%20{query},%20appetizing%20food,%20restaurant%20style,%20high%20detail,%204k?width=800&height=600&nologo=true&seed={seed}&model=flux"

def seed_data():
    db = SessionLocal()
    
    # Clear existing data
    db.query(models.OrderItem).delete()
    db.query(models.Order).delete()
    db.query(models.MenuItem).delete()
    db.commit()

    menu_items = {
        "mains": [
            {"name": "Grilled Chicken", "price": 12.99, "desc": "Tender grilled chicken breast with herbs"},
            {"name": "Beef Burger", "price": 10.99, "desc": "Juicy beef patty with fresh toppings"},
            {"name": "Fish & Chips", "price": 14.99, "desc": "Crispy battered fish with golden fries"},
            {"name": "Pasta Carbonara", "price": 11.99, "desc": "Classic Italian pasta with creamy sauce"},
            {"name": "Vegetarian Pizza", "price": 13.99, "desc": "Fresh vegetables on crispy crust"},
            {"name": "Steak Frites", "price": 24.99, "desc": "Premium ribeye steak with french fries"},
            {"name": "Butter Chicken", "price": 15.99, "desc": "Creamy Indian curry with tender chicken"},
            {"name": "Pad Thai", "price": 12.99, "desc": "Thai stir-fried rice noodles with shrimp"},
            {"name": "Lasagna", "price": 14.99, "desc": "Layered pasta with meat sauce and cheese"},
            {"name": "Sushi Platter", "price": 22.99, "desc": "Assorted fresh nigiri and maki rolls"},
            {"name": "Lobster Roll", "price": 19.99, "desc": "Fresh lobster meat in a toasted bun"},
            {"name": "BBQ Ribs", "price": 18.99, "desc": "Slow-cooked pork ribs with bbq sauce"},
            {"name": "Mushroom Risotto", "price": 13.99, "desc": "Creamy rice with wild mushrooms"},
            {"name": "Tacos Al Pastor", "price": 11.99, "desc": "Marinated pork tacos with pineapple"},
            {"name": "Chicken Parmesan", "price": 15.99, "desc": "Breaded chicken with marinara and mozzarella"},
            {"name": "Lamb Chops", "price": 26.99, "desc": "Grilled lamb chops with mint sauce"},
            {"name": "Salmon Glazed", "price": 17.99, "desc": "Pan-seared salmon with honey garlic glaze"},
            {"name": "Burrito Bowl", "price": 10.99, "desc": "Rice, beans, meat, and toppings in a bowl"},
            {"name": "Duck Confit", "price": 21.99, "desc": "Crispy duck leg with roasted potatoes"},
            {"name": "Shrimp Scampi", "price": 16.99, "desc": "Shrimp cooked in garlic butter sauce"},
            {"name": "Beef Wellington", "price": 29.99, "desc": "Beef tenderloin wrapped in puff pastry"},
            {"name": "Falafel Wrap", "price": 9.99, "desc": "Crispy falafel with tahini in pita"},
            {"name": "Chicken Tikka Masala", "price": 14.99, "desc": "Roasted chicken chunks in spicy sauce"},
            {"name": "Eggplant Parmesan", "price": 13.99, "desc": "Breaded eggplant with tomato sauce"},
            {"name": "Poke Bowl", "price": 15.99, "desc": "Raw fish salad with rice and vegetables"}
        ],
        "sides": [
            {"name": "French Fries", "price": 4.99, "desc": "Golden crispy potato fries"},
            {"name": "Onion Rings", "price": 5.99, "desc": "Crispy beer-battered onion rings"},
            {"name": "Garden Salad", "price": 6.99, "desc": "Fresh mixed greens with dressing"},
            {"name": "Mashed Potatoes", "price": 4.99, "desc": "Creamy whipped potatoes"},
            {"name": "Coleslaw", "price": 3.99, "desc": "Fresh cabbage slaw with tangy dressing"},
            {"name": "Garlic Bread", "price": 4.50, "desc": "Toasted bread with garlic butter"},
            {"name": "Mozzarella Sticks", "price": 6.99, "desc": "Fried cheese sticks with marinara"},
            {"name": "Caesar Salad", "price": 7.99, "desc": "Romaine lettuce with parmesan and croutons"},
            {"name": "Sweet Potato Fries", "price": 5.99, "desc": "Crispy sweet potato strips"},
            {"name": "Mac & Cheese", "price": 6.50, "desc": "Creamy macaroni and cheese"},
            {"name": "Spring Rolls", "price": 5.50, "desc": "Crispy vegetable filled rolls"},
            {"name": "Edamame", "price": 4.99, "desc": "Steamed soybeans with sea salt"},
            {"name": "Potato Wedges", "price": 5.50, "desc": "Seasoned thick-cut potato wedges"},
            {"name": "Corn on Cob", "price": 3.99, "desc": "Grilled sweet corn with butter"},
            {"name": "Bruschetta", "price": 6.99, "desc": "Grilled bread simply topped with tomatoes"},
            {"name": "Hummus & Pita", "price": 7.50, "desc": "Creamy chickpea dip with pita bread"},
            {"name": "Nachos", "price": 8.99, "desc": "Tortilla chips with cheese and jalapenos"},
            {"name": "Chicken Wings", "price": 9.99, "desc": "Spicy buffalo wings with ranch"},
            {"name": "Steamed Veggies", "price": 5.99, "desc": "Fresh seasonal vegetables steamed"},
            {"name": "Rice Pilaf", "price": 4.50, "desc": "Fluffy seasoned rice"},
            {"name": "Quinoa Salad", "price": 8.50, "desc": "Healthy quinoa with diced veggies"},
            {"name": "Fruit Cup", "price": 4.99, "desc": "Assorted fresh seasonal fruits"},
            {"name": "Soup of Day", "price": 5.99, "desc": "Freshly made daily soup"},
            {"name": "Bread Basket", "price": 3.99, "desc": "Assortment of fresh dinner rolls"},
            {"name": "Pickles", "price": 2.99, "desc": "Crunchy dill pickles"}
        ],
        "beverages": [
            {"name": "Coca Cola", "price": 2.99, "desc": "Classic refreshing cola"},
            {"name": "Orange Juice", "price": 3.99, "desc": "Fresh squeezed orange juice"},
            {"name": "Coffee", "price": 2.49, "desc": "Premium roasted coffee"},
            {"name": "Iced Tea", "price": 2.99, "desc": "Refreshing iced tea"},
            {"name": "Water", "price": 1.99, "desc": "Pure spring water"},
            {"name": "Lemonade", "price": 3.50, "desc": "Freshly squeezed lemon drink"},
            {"name": "Cappuccino", "price": 3.99, "desc": "Espresso with steamed milk foam"},
            {"name": "Latte", "price": 3.99, "desc": "Espresso with steamed milk"},
            {"name": "Espresso", "price": 2.50, "desc": "Strong black coffee shot"},
            {"name": "Mango Lassi", "price": 4.50, "desc": "Yogurt based mango drink"},
            {"name": "Green Tea", "price": 2.99, "desc": "Healthy hot green tea"},
            {"name": "Milkshake", "price": 5.99, "desc": "Thick ice cream shake"},
            {"name": "Smoothie", "price": 6.50, "desc": "Fruit blended healthy drink"},
            {"name": "Iced Coffee", "price": 3.99, "desc": "Chilled coffee with ice"},
            {"name": "Hot Chocolate", "price": 3.50, "desc": "Rich cocoa milk drink"},
            {"name": "Sparkling Water", "price": 2.50, "desc": "Carbonated mineral water"},
            {"name": "Ginger Ale", "price": 2.99, "desc": "Ginger flavored soft drink"},
            {"name": "Mojito (Virgin)", "price": 5.99, "desc": "Mint and lime mocktail"},
            {"name": "Apple Juice", "price": 3.50, "desc": "Sweet apple nectar"},
            {"name": "Cranberry Juice", "price": 3.50, "desc": "Tart red berry juice"},
            {"name": "Chai Latte", "price": 3.99, "desc": "Spiced tea with milk"},
            {"name": "Root Beer", "price": 2.99, "desc": "Traditional sassafras soda"},
            {"name": "Matcha Latte", "price": 4.99, "desc": "Green tea powder with milk"},
            {"name": "Coconut Water", "price": 3.99, "desc": "Natural hydration from coconuts"},
            {"name": "Bubble Tea", "price": 5.99, "desc": "Tea with tapioca pearls"}
        ],
        "desserts": [
            {"name": "Chocolate Cake", "price": 6.99, "desc": "Rich chocolate layer cake"},
            {"name": "Ice Cream", "price": 4.99, "desc": "Creamy vanilla ice cream"},
            {"name": "Apple Pie", "price": 5.99, "desc": "Classic apple pie with cinnamon"},
            {"name": "Cheesecake", "price": 7.99, "desc": "New York style cheesecake"},
            {"name": "Cookies", "price": 3.99, "desc": "Freshly baked chocolate chip cookies"},
            {"name": "Tiramisu", "price": 7.50, "desc": "Italian coffee flavored dessert"},
            {"name": "Brownie", "price": 4.50, "desc": "Dense chocolate fudge square"},
            {"name": "Creme Brulee", "price": 8.50, "desc": "Custard with caramelized sugar top"},
            {"name": "Panna Cotta", "price": 6.99, "desc": "Italian thickened cream dessert"},
            {"name": "Fruit Tart", "price": 5.99, "desc": "Pastry shell with cream and fruit"},
            {"name": "Mousse", "price": 5.50, "desc": "Light and airy chocolate dessert"},
            {"name": "Donut", "price": 2.99, "desc": "Glazed fried dough ring"},
            {"name": "Churros", "price": 4.99, "desc": "Fried dough simply dusted with sugar"},
            {"name": "Macarons", "price": 6.50, "desc": "French almond meringue cookies"},
            {"name": "Waffles", "price": 7.99, "desc": "Belgian waffles with toppings"},
            {"name": "Pancakes", "price": 7.99, "desc": "Fluffy cakes with syrup"},
            {"name": "Crepes", "price": 6.99, "desc": "Thin french pancakes"},
            {"name": "Gelato", "price": 5.50, "desc": "Dense italian ice cream"},
            {"name": "Sorbet", "price": 4.99, "desc": "Fruit based frozen dessert"},
            {"name": "Cupcake", "price": 3.50, "desc": "Small cake with frosting"},
            {"name": "Key Lime Pie", "price": 6.50, "desc": "Tangy lime custard pie"},
            {"name": "Red Velvet Cake", "price": 6.99, "desc": "Crimson colored cocoa cake"},
            {"name": "Cannoli", "price": 5.50, "desc": "Tube pastry with ricotta filling"},
            {"name": "Baklava", "price": 6.50, "desc": "Layered pastry with honey and nuts"},
            {"name": "Eclair", "price": 4.50, "desc": "Cream filled long pastry"}
        ]
    }

    print("Seeding extended data with images...")
    for category, items in menu_items.items():
        print(f"Processing {category}...")
        for item in items:
            image_url = get_image_url(item["name"])
            db_item = models.MenuItem(
                name=item["name"],
                category=category,
                price=item["price"],
                description=item["desc"],
                image_url=image_url
            )
            db.add(db_item)
    
    db.commit()
    print("Seeding complete!")
    db.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    seed_data()
