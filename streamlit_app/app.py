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
    initial_sidebar_state="collapsed" # Hide sidebar by default since we use top nav
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

# Top Horizontal Navigation
# Calculate cart items for label
cart_label = "Cart"
if st.session_state.cart:
    cart_count = len(st.session_state.cart)
    cart_label = f"Cart ({cart_count})"

selected = option_menu(
    menu_title=None, # Hide title
    options=["Mains", "Sides", "Beverages", "Desserts", "Cart"],
    icons=['egg-fried', 'circle', 'cup-straw', 'cake', 'cart'],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#262730"},
        "icon": {"color": "#3b82f6", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#374151"},
        "nav-link-selected": {"background-color": "#3b82f6"},
    }
)

# Header with Title
st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🍽️ Modern Cafeteria</h1>", unsafe_allow_html=True)

# Main Content
db = get_db()
category_map = {
    "Mains": "mains",
    "Sides": "sides",
    "Beverages": "beverages",
    "Desserts": "desserts"
}

if selected == "Cart":
    st.subheader("🛍️ Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Go add some delicious food!")
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/11329/11329060.png" width="200">
            </div>
        """, unsafe_allow_html=True)
    else:
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.write(f"**{item['name']}**")
                    st.caption(f"${item['price']:.2f} each")
                with col2:
                    st.write(f"x {item['quantity']}")
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
            
    # Show Bill Section
    st.divider()
    if st.session_state.cart:
        if st.checkbox("🧾 Show Bill", help="Generate a receipt for the current cart"):
            total_bill = sum(item['subtotal'] for item in st.session_state.cart)
            
            # Generate Receipt HTML
            receipt_html = f"""
            <div class="receipt-container">
                <div class="receipt-header">
                    <p class="receipt-title">RECEIPT</p>
                    <p style="font-size: 12px; color: #666; margin-top: 5px;">Modern Cafeteria</p>
                </div>
                
                <div class="dashed-line"></div>
                
                <div style="margin-bottom: 15px;">
            """
            
            for item in st.session_state.cart:
                receipt_html += f"""
                <div class="receipt-item">
                    <span class="item-name">{item['quantity']}x {item['name']}</span>
                    <span class="item-price">${item['subtotal']:.2f}</span>
                </div>
                """
                
            receipt_html += f"""
                </div>
                
                <div class="dashed-line"></div>
                
                <div class="receipt-total">
                    <span>TOTAL</span>
                    <span>${total_bill:.2f}</span>
                </div>
                
                <div class="dashed-line"></div>
                
                <div class="receipt-footer">
                    <p>THANK YOU!</p>
                    <p>Visit Again</p>
                </div>
            </div>
            """
            
            st.markdown(receipt_html, unsafe_allow_html=True)
            
            # Print Button (using JavaScript)
            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                <button onclick="window.print()" style="
                    background-color: #4b5563; 
                    color: white; 
                    border: none; 
                    padding: 8px 16px; 
                    border-radius: 4px; 
                    cursor: pointer;
                    font-size: 14px;">
                    🖨️ Print Receipt
                </button>
            </div>
            """, unsafe_allow_html=True)

else:
    # Menu View
    category_key = category_map[selected]
    
    # Fetch items
    items = db.query(models.MenuItem).filter(models.MenuItem.category == category_key).all()
    
    # Grid Layout
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i % 3]:
            with st.container(border=True): # Use Streamlit's native border container for the card look
                st.image(item.image_url, use_container_width=True)
                st.markdown(f"""
                <div style="padding: 10px;">
                    <h3 style="margin: 0; font-size: 1.2rem;">{item.name}</h3>
                    <p style="color: #9ca3af; font-size: 0.9em; margin: 5px 0;">{item.description}</p>
                    <p style="color: #f59e0b; font-weight: bold; font-size: 1.1rem; margin: 0;">${item.price:.2f}</p>
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
