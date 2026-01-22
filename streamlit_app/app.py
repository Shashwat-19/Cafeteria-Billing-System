import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import sys
import os

# Add root directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import models, database

# Page config
st.set_page_config(
    page_title="Modern Cafeteria",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('streamlit_app/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Database dependency
def get_db():
    db = database.SessionLocal()
    return db

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

def add_to_cart(item, quantity):
    # Check if item exists in cart
    for cart_item in st.session_state.cart:
        if cart_item['id'] == item.id:
            cart_item['quantity'] += quantity
            cart_item['subtotal'] = cart_item['quantity'] * cart_item['price']
            st.toast(f"Updated quantity for {item.name}!", icon="✅")
            return

    # Add new item
    st.session_state.cart.append({
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'quantity': quantity,
        'subtotal': item.price * quantity
    })
    st.toast(f"Added {item.name} to cart!", icon="🛒")

def remove_from_cart(index):
    st.session_state.cart.pop(index)
    st.rerun()

def checkout():
    if not st.session_state.cart:
        st.error("Cart is empty!")
        return

    db = get_db()
    try:
        total_amount = sum(item['subtotal'] for item in st.session_state.cart)
        
        # Create Order
        db_order = models.Order(total_amount=total_amount)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # Create Order Items
        for item in st.session_state.cart:
            db_item = models.OrderItem(
                order_id=db_order.id,
                item_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            db.add(db_item)
        
        db.commit()
        st.session_state.cart = []
        st.success(f"Order #{db_order.id} placed successfully! Total: ${total_amount:.2f}")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error placing order: {str(e)}")
    finally:
        db.close()

# Sidebar
with st.sidebar:
    st.title("🍽️ Cafeteria")
    selected = option_menu(
        "Menu",
        ["Mains", "Sides", "Beverages", "Desserts", "Cart"],
        icons=['egg-fried', 'circle', 'cup-straw', 'cake', 'cart'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#262730"},
            "icon": {"color": "#3b82f6", "font-size": "20px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#374151"},
            "nav-link-selected": {"background-color": "#3b82f6"},
        }
    )
    
    # Mini Cart Preview
    if st.session_state.cart:
        st.divider()
        st.subheader("🛒 Cart Preview")
        st.write(f"Items: {len(st.session_state.cart)}")
        st.write(f"Total: ${sum(item['subtotal'] for item in st.session_state.cart):.2f}")
        if st.button("Go to Checkout"):
            # This is a bit hacky in Streamlit, ideally we just switch the view manually
            st.info("Switch to 'Cart' tab to checkout!")

# Main Content
db = get_db()
category_map = {
    "Mains": "mains",
    "Sides": "sides",
    "Beverages": "beverages",
    "Desserts": "desserts"
}

if selected == "Cart":
    st.title("🛍️ Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Go add some delicious food!")
        st.image("https://cdn-icons-png.flaticon.com/512/11329/11329060.png", width=200)
    else:
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.subheader(item['name'])
                    st.caption(f"${item['price']:.2f} each")
                with col2:
                    st.write(f"**Qty:** {item['quantity']}")
                with col3:
                    st.write(f"**${item['subtotal']:.2f}**")
                with col4:
                    if st.button("🗑️", key=f"del_{idx}"):
                        remove_from_cart(idx)
                st.divider()
        
        total = sum(item['subtotal'] for item in st.session_state.cart)
        st.subheader(f"Total: ${total:.2f}")
        
        if st.button("Confirm Order", type="primary", use_container_width=True):
            checkout()

else:
    # Menu View
    st.title(f"{selected}")
    category_key = category_map[selected]
    
    # Fetch items
    items = db.query(models.MenuItem).filter(models.MenuItem.category == category_key).all()
    
    # Grid Layout
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            with st.container():
                # Custom HTML card
                st.markdown(f"""
                <div class="menu-item-container">
                    <h3>{item.name}</h3>
                    <p style="color: #9ca3af; height: 40px; overflow: hidden;">{item.description}</p>
                    <p class="price-tag">${item.price:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Controls (Streamlit widgets must be outside raw HTML)
                col_qty, col_add = st.columns([1, 2])
                with col_qty:
                    qty = st.number_input("Qty", min_value=1, max_value=10, value=1, key=f"qty_{item.id}", label_visibility="collapsed")
                with col_add:
                    if st.button("Add to Cart", key=f"add_{item.id}", use_container_width=True):
                        add_to_cart(item, qty)

db.close()
