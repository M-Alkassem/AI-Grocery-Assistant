import streamlit as st
import requests
import uuid
from datetime import datetime
import re
import time

# 🔹 Chat URL N8N
CHAT_URL = #n8n webhook URL

st.set_page_config(
    page_title="Friendly Grocer",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        padding: 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 0;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Custom header */
    .custom-header {
        background-color: #e0e0e0;
        padding: 15px 30px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #d0d0d0;
        margin: -70px -50px 0 -50px;
    }
    
    .header-title {
        font-size: 20px;
        font-weight: 600;
        color: #333;
        margin-left: 20px;
    }
    
    /* Chat container */
    .chat-container {
        background-color: #ffffff;
        height: calc(100vh - 200px);
        overflow-y: auto;
        padding: 20px 30px;
        margin: 0;
    }
    
    /* Message styling */
    .message {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: flex-start;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        overflow: hidden;
    }
    
    .message-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .message-content {
        flex: 1;
    }
    
    .message-sender {
        font-weight: 600;
        font-size: 14px;
        color: #333;
        margin-bottom: 2px;
    }
    
    .message-time {
        font-size: 11px;
        color: #999;
        margin-left: 8px;
    }
    
    .message-text {
        font-size: 14px;
        color: #333;
        line-height: 1.5;
        margin-top: 4px;
    }
    
    .message-bubble {
        background-color: #f0f0f0;
        padding: 10px 14px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        color: #333;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: flex-start;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
        padding: 10px 14px;
        background-color: #f0f0f0;
        border-radius: 12px;
        margin-top: 4px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background-color: #999;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    /* Input area */
    .input-area {
        background-color: #ffffff;
        border-top: 1px solid #e0e0e0;
        padding: 15px 30px;
        position: fixed;
        bottom: 0;
        right: 0;
        left: 300px;
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    /* Sidebar sections */
    .sidebar-section {
        padding: 20px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .sidebar-title {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .sidebar-item {
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.2s;
        font-size: 14px;
        color: #555;
    }
    
    .sidebar-item:hover {
        background-color: #f5f5f5;
    }
    
    .sidebar-item.active {
        background-color: #e8e8e8;
        font-weight: 500;
    }
    
    .badge {
        background-color: #333;
        color: white;
        border-radius: 12px;
        padding: 2px 8px;
        font-size: 11px;
        font-weight: 600;
        float: right;
    }
    
    /* Bot info card */
    .bot-card {
        text-align: center;
        padding: 30px 20px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .bot-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 0 auto 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
    }
    
    .bot-name {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        margin-bottom: 5px;
    }
    
    .bot-status {
        font-size: 13px;
        color: #4CAF50;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #4CAF50;
        border-radius: 50%;
    }
    
    .action-buttons {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 15px;
    }
    
    .action-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #333;
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }
    
    /* Contact info */
    .contact-info {
        padding: 20px;
        font-size: 13px;
        color: #666;
    }
    
    .contact-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    
    .contact-label {
        color: #999;
    }
    
    .contact-value {
        color: #333;
        font-weight: 500;
    }
    
    /* Checkout button */
    .checkout-btn {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    .checkout-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    
    /* Cart total */
    .cart-total {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        padding: 10px 15px;
        background-color: #f9f9f9;
        border-radius: 8px;
        margin-top: 10px;
        display: flex;
        justify-content: space-between;
    }
    
    /* Streamlit input customization */
    .stChatInput {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    
    /* Hide default streamlit elements */
    .stChatInput > div {
        border: none;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #999;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    /* New Order button */
    .new-order-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        width: 100%;
    }
    
    .new-order-btn:hover {
        background: linear-gradient(135deg, #5568d3 0%, #653a8b 100%);
    }
    </style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cart_items" not in st.session_state:
    st.session_state.cart_items = []

if "cart_total" not in st.session_state:
    st.session_state.cart_total = 0.0

if "recent_items" not in st.session_state:
    st.session_state.recent_items = [
        "Apples", "Bananas", "Carrots", "Dairy", "Eggs", 
        "Fish", "Grapes", "Honey", "Juice"
    ]

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

def extract_price_from_text(text):
    """Extract price/total from bot response with multiple pattern matching"""
    pattern1 = r'(?:total|price|cost|amount)(?:\s+is)?(?:\s*:)?\s*(\d+(?:\.\d+)?)\s*(?:AED|aed|Aed)'
    pattern2 = r'(\d+(?:\.\d+)?)\s*(?:AED|aed|Aed)'
    pattern3 = r'(?:comes to|is|equals)\s*(\d+(?:\.\d+)?)'
    
    for pattern in [pattern1, pattern2, pattern3]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                continue
    
    return None

def extract_cart_info_from_text(text):
    """Extract both items and prices from bot response"""
    items_added = []
    total_price = None
    
    if any(phrase in text.lower() for phrase in [
        "added to your cart", 
        "added to cart",
        "has been added",
        "have been added"
    ]):
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(kg|g|lbs?|oz|pieces?|pcs?|items?)?\s*(?:of\s+)?([A-Za-z\s]+?)(?:\s+for\s+(\d+(?:\.\d+)?)\s*(?:AED|aed))?(?:\s+(?:have been|has been|been)?\s*added)',
            r'([A-Za-z][A-Za-z\s]+?)\s*(?:\((\d+(?:\.\d+)?)\s*(?:AED|aed)\))?\s*(?:have been|has been|been)?\s*added',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                
                if len(groups) >= 3 and groups[0] and groups[0][0].isdigit():
                    quantity = groups[0]
                    unit = groups[1] if groups[1] else ""
                    product = groups[2].strip()
                    price = groups[3] if len(groups) > 3 and groups[3] else None
                    
                    cart_item = f"{quantity}{unit} {product}".strip()
                elif len(groups) >= 1:
                    product = groups[0].strip()
                    price = groups[1] if len(groups) > 1 and groups[1] else None
                    cart_item = product
                else:
                    continue
                

                cart_item = cart_item.strip().title()
                cart_item = re.sub(r'\s+(Have Been|Has Been|Been|To Your|Your|The)\s*$', '', cart_item, flags=re.IGNORECASE).strip()
                
                if cart_item and len(cart_item) > 2:
                    item_info = {"name": cart_item, "price": float(price) if price else 0.0}
                    items_added.append(item_info)
    

    total_price = extract_price_from_text(text)
    
    return items_added, total_price


with st.sidebar:
    
    st.markdown("""
        <div class="bot-card">
            <div class="bot-avatar">🛒</div>
            <div class="bot-name">Grocery Bot</div>
            <div class="bot-status">
                <span class="status-dot"></span>
                Available now
            </div>
            <div class="action-buttons">
                <button class="action-btn">💬</button>
                <button class="action-btn">📞</button>
                <button class="action-btn">📹</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
   
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🛒 Your Cart</div>', unsafe_allow_html=True)
    
    if not st.session_state.cart_items:
        st.markdown('<div style="color: #999; font-size: 13px; padding: 10px;">Your cart is empty</div>', unsafe_allow_html=True)
    else:
        
        unique_items = list(dict.fromkeys(st.session_state.cart_items))
        for item in unique_items:
           
            clean_item = item
            
            words = clean_item.split()
            if len(words) > 1:
               
                seen = set()
                filtered = []
                for word in words:
                    word_lower = word.lower().strip('.,!?')
                    if word_lower not in seen:
                        seen.add(word_lower)
                        filtered.append(word)
                clean_item = ' '.join(filtered)
            
            st.markdown(f'<div class="sidebar-item">• {clean_item}</div>', unsafe_allow_html=True)
        

        st.markdown(f"""
            <div class="cart-total">
                <span>Total:</span>
                <span>{st.session_state.cart_total:.2f} AED</span>
            </div>
        """, unsafe_allow_html=True)
        
        
        if st.button("🛍️ Proceed to Checkout", key="checkout_btn", use_container_width=True):
            st.session_state.messages.append({
                "role": "user", 
                "content": "I want to proceed to checkout"
            })
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
   
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    if st.button("🆕 Start New Order", key="new_order", use_container_width=True):
        st.session_state.messages = []
        st.session_state.cart_items = []
        st.session_state.cart_total = 0.0
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.is_loading = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📦 Recent Items</div>', unsafe_allow_html=True)
    for item in st.session_state.recent_items:
        badge_html = ''
        if item == "Dairy":
            badge_html = '<span class="badge">1</span>'
        elif item == "Honey":
            badge_html = '<span class="badge">7</span>'
        st.markdown(f'<div class="sidebar-item">{item}{badge_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
  
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">👥 Group Orders</div>', unsafe_allow_html=True)
    group_orders = [
        "Apples, Bananas",
        "Carrots, Eggs",
        "Dairy, Grapes, Honey",
        "Fish, Juice",
        "Eggs, Fish, Juice"
    ]
    for i, order in enumerate(group_orders):
        badge_html = '<span class="badge">+10</span>' if i == 3 else ''
        st.markdown(f'<div class="sidebar-item">{order}{badge_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
  
    st.markdown("""
        <div class="contact-info">
            <div style="font-weight: 600; margin-bottom: 10px;">Customer Support</div>
            <div class="contact-row">
                <span class="contact-label">Email</span>
                <span class="contact-value">support@grocerybot.com</span>
            </div>
            <div class="contact-row">
                <span class="contact-label">Chat</span>
                <span class="contact-value">Available 24/7</span>
            </div>
            <div class="contact-row">
                <span class="contact-label">Local time</span>
                <span class="contact-value">11:58 AM</span>
            </div>
        </div>
    """, unsafe_allow_html=True)



st.markdown("""
    <div class="custom-header">
        <div style="font-size: 24px;">🔍</div>
        <div class="header-title">Grocery Shopping Assistant</div>
    </div>
""", unsafe_allow_html=True)


st.markdown('<div class="chat-container">', unsafe_allow_html=True)


for msg in st.session_state.messages:
    current_time = datetime.now().strftime("%I:%M %p")
    
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="message">
                <div class="message-avatar">👤</div>
                <div class="message-content">
                    <div>
                        <span class="message-sender">You</span>
                        <span class="message-time">{current_time}</span>
                    </div>
                    <div class="message-bubble">{msg['content']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <div>
                        <span class="message-sender">Grocery Bot</span>
                        <span class="message-time">{current_time}</span>
                    </div>
                    <div class="message-text">{msg['content']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


if st.session_state.is_loading:
    st.markdown("""
        <div class="typing-indicator">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div>
                    <span class="message-sender">Grocery Bot</span>
                    <span class="message-time">typing...</span>
                </div>
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


user_input = st.chat_input("Ask About products...")


if user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.is_loading = True
    st.rerun()

if st.session_state.is_loading and len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
       
        payload = {
            "sessionId": st.session_state.session_id,
            "action": "sendMessage",
            "chatInput": last_message["content"]
        }
        headers = {"Content-Type": "application/json"}

        try:
           
            response = requests.post(CHAT_URL, json=payload, headers=headers, timeout=15)
            data = response.json()

            
            reply = ""
            if isinstance(data, dict):
                reply = data.get("text", data.get("output", "Sorry, I couldn't understand that."))
                
                
                if "cart" in data or "cartItems" in data:
                    cart_data = data.get("cart", data.get("cartItems", []))
                    if cart_data:
                        st.session_state.cart_items = cart_data
                
               
                if "total" in data:
                    st.session_state.cart_total = float(data["total"])
                elif "cartTotal" in data:
                    st.session_state.cart_total = float(data["cartTotal"])
                    
            elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                reply = data[0].get("text", data[0].get("output", "Sorry, I couldn't understand that."))
                
            
                if "cart" in data[0] or "cartItems" in data[0]:
                    cart_data = data[0].get("cart", data[0].get("cartItems", []))
                    if cart_data:
                        st.session_state.cart_items = cart_data
                
                if "total" in data[0]:
                    st.session_state.cart_total = float(data[0]["total"])
                elif "cartTotal" in data[0]:
                    st.session_state.cart_total = float(data[0]["cartTotal"])
            else:
                reply = "Sorry, I couldn't understand that."
            
           
            items_from_text, price_from_text = extract_cart_info_from_text(reply)
            
           
            for item_info in items_from_text:
                item_name = item_info["name"]
                if item_name not in st.session_state.cart_items:
                    st.session_state.cart_items.append(item_name)
            
            
            if price_from_text is not None:
                st.session_state.cart_total = price_from_text

        except requests.Timeout:
            reply = "Request timed out. Please try again."
        except Exception as e:
            reply = f"Failed to connect: {e}"

       
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.is_loading = False
        st.rerun()