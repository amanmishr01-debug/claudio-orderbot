import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ── Restaurant Info ──────────────────────────────────────────────
RESTAURANT_NAME = "Claudio Pizzeria"
RESTAURANT_ADDRESS = "598 10th Ave, New York, NY 10036"
RESTAURANT_PHONE = "(212) 586-3145"
PICKUP_ETA = "~25 minutes"
DELIVERY_ETA = "~30-35 minutes"

# ── Full Menu (scraped from claudiopizzeriamenu.com) ─────────────
MENU = """
=== QUICK BITES ===
Knot Parm (Chicken Parm hero on a giant garlic knot) - $13.47

=== PIZZA (Whole Pies) ===
Regular Cheese Pizza - $19.00
Sicilian Cheese Pizza - $30.00
Grandma Pizza (crispy thin square, marinara, basil oil, parmigiano, mozzarella) - $31.50
Grandma Vodka Pizza (crispy thin square, vodka sauce, basil oil, parmigiano, mozzarella) - $32.00
Upside Down Sicilian Pizza (mozzarella, sauce on top, Romano) - $31.00
Burrata Grandma Pizza (crispy thin square, basil oil, parmigiano, cherry tomatoes, balsamic glaze, marinara) - $31.00
The Hells Kitchen Diavola Sicilian Pizza (diavola sauce, mozzarella, imported pepperoni) - $36.00
Spicy Rigatoni Vodka Pizza (spicy vodka sauce, rigatoni, fresh mozzarella) - $35.00
The Trio Pizza (mozzarella, pesto, vodka sauce & marinara) - $32.00
La Claudia Pizza (crispy thin square, tomato confit, pesto sauce) - $35.50
The Fig Pizza (fig preserves, prosciutto, arugula, fresh figs, goat cheese & balsamic glaze) - $38.00
Claudio's Special Pizza (choice of 3 toppings) - $27.00
Margherita Pizza (fresh mozzarella, marinara, basil oil, parmigiano) - $24.50
White Pizza (mozzarella and ricotta) - $22.50
White Veggie Pizza (mozzarella, ricotta + choice of spinach/broccoli/mushrooms/eggplant) - $24.50
Il Giardino Pizza (arugula, roasted peppers, kalamata olives, cherry tomatoes, balsamic, fresh mozzarella) - $24.50
Spicy Buffalo Chicken Pizza (mozzarella, blue cheese & buffalo sauce) - $24.50
Chicken BBQ Pizza - $24.50
Chicken Bacon & Ranch Pizza - $24.50
Claudio's Meat Lover Pizza (sausage, pepperoni, meatball, ham) - $24.50
Claudio's Veggie Delight Pizza (broccoli, spinach, black olives, mushrooms, green peppers, onions) - $24.50
Claudio's Supreme Pizza (sausage, pepperoni, onions, peppers, mushrooms) - $24.50
Caesar Salad Pizza (romaine, Caesar dressing, grilled chicken) - $24.50
EL Ranchero Pizza (chicken, tomato, onions, ranch, chipotle aioli) - $25.50
Vodka Roni Pizza (vodka sauce, fresh mozzarella, imported pepperoni & pesto) - $26.50
Chicken Parm Pizza (chicken cutlet, fresh mozzarella, marinara) - $25.50

=== CAULIFLOWER CRUST GLUTEN FREE PIZZA ===
GF Cheese Pizza - $18.00
GF Specialty Pizzas (Trio, Special, Margherita, White, White Veggie, Il Giardino, Buffalo Chicken, BBQ Chicken, Bacon Ranch, Meat Lover, Veggie Delight, Supreme, Caesar Salad, EL Ranchero, Vodka Roni, Chicken Parm) - $24.00 each

=== PIZZA BY THE SLICE ===
Regular Slice - $4.42
Pepperoni Slice - $5.46
Sausage Slice - $5.46
Mushroom Slice - $5.46
Eggplant Parm Slice - $5.46
Sicilian Slice - $5.20
Upside Down Slice - $5.46
Grandma Slice - $5.46
Chicken Bacon Ranch Slice - $6.50
Chicken Buffalo Slice - $6.50
Vegetable Slice - $6.50
Hell's Kitchen Slice - $7.02
Il Giardino Slice - $7.54
Il Giardino Prosciutto Slice - $8.16
Spicy Toni Slice (spicy vodka sauce, rigatoni, mozzarella) - $7.12
The Fig Slice - $8.32
Meatlover Slice - $6.50
Margarita Slice - $5.46
Trio Slice - $5.72
La Burrata Slice - $7.54
La Claudia Slice - $7.54

=== APPETIZERS & SIDES ===
Garlic Knots - $4.75
Garlic Knots with Mozzarella - $7.00
Garlic Bread - $5.75
Garlic Bread with Cheese - $6.75
Garlic Cheesy Sticks (with marinara & vodka sauce) - $13.00
Mozzarella Sticks - $9.50
Beef Patties - $4.25
Beef Patties with Cheese - $5.25
Beef Patties with Cheese & Pepperoni - $6.25
Buffalo Wings (plain, buffalo or bbq, with blue cheese) - $10.75
French Fries - $5.00
French Fries with Mozzarella - $6.75
Coco Bread - $2.50
Fried Ravioli (with sauce) - $9.50
Sauteed Broccoli - $9.50
Sauteed Spinach - $9.50
Meatballs - $13.75
Meatballs with Ricotta - $15.75
Chicken Meatballs - $13.75
Eggplant Meatballs - $13.75
Chicken Fingers (with BBQ, ranch, or honey) - $11.75
Chicken Fingers with Fries - $14.75
Side of Sausage - $11.00
Zucchini Fritti (with marinara) - $9.50
Calamari Fritti (with marinara) - $15.00
Riceball - $5.00
Riceball Meal (topped with ricotta, mozzarella, marinara) - $9.50
Potato Croquettes - $5.00
Side of Chicken (grilled or breaded) - $11.75

=== SOUPS (served with bread) ===
Chicken Noodle Soup - $6.50
Lentil Soup - $6.50
Minestrone Soup - $6.50
Pasta Fagioli Soup - $6.50

=== SALADS ===
Garden Salad - $10.50
Greek Salad - $11.75
Caesar Salad - $11.75
Arugula Salad (baby arugula, feta, walnuts, balsamic) - $12.75
Caprese Salad (fresh mozzarella, tomato, roasted peppers, olives) - $14.00
Cold Antipasto Salad (ham, salami, provolone, giardiniera, lettuce, tomatoes) - $15.00

=== SPECIALTY ROLLS ===
Meatball Roll - $10.50
Spinach Roll - $10.50
Chicken Buffalo Roll - $10.50
Chicken Roll - $10.50
Eggplant Roll - $10.50
Sausage & Pepper Roll - $10.50
Pepperoni Roll - $10.50
Broccoli Roll - $10.50
Plain Calzone - $10.50
Veggie Stromboli - $10.50
Meat Stromboli - $10.50

=== PINWHEELS ===
Pepperoni Pinwheel - $6.95
Sausage Pinwheel - $6.95
Spinach Pinwheel - $6.95
Philly Cheesesteak Pinwheel - $7.50
Buffalo Chicken Pinwheel - $7.50
Penne Vodka Pinwheel - $7.50

=== HEROES ===
Chicken Parmigiana Hero - $14.95
Eggplant Parmigiana Hero - $14.95
Meatball Parmigiana Hero - $14.95
Sausage Parmigiana Hero - $14.95
Shrimp Parmigiana Hero - $15.95
Veal Parmigiana Hero - $15.95
Grilled Chicken Hero - $14.95
Fried Chicken Hero - $14.95
The Bensonhurst Hero (sausage, peppers & onions) - $14.95
Claudio's Chicken Hero (grilled chicken, fresh mozzarella, roasted peppers) - $15.85
Caprese Hero (fresh mozzarella, tomato, basil) - $14.95
Italian Hero (prosciutto di Parma, roasted peppers, fresh mozzarella, olive oil) - $14.95
Ham Salami & Provolone Hero - $12.75

=== BURGERS (served with fries & side salad) ===
Claudio's Burger (angus, cheese, red onions, lettuce, tomato) - $14.00
The Hell's Kitchen Burger (angus, pepper jack, jalapenos, onions, sriracha mayo) - $15.50
Claudio's Burger Special (angus, cheese, bacon, mushroom, onions) - $17.00

=== WRAPS (plain or whole wheat) ===
Caesar Chicken Wrap - $9.75
Greek Style Wrap - $9.75
Philly Cheese Steak Wrap - $9.75
Buffalo Spicy Wrap - $9.75
Chicken Bacon Ranch Wrap - $9.75

=== PASTA DISHES ===
Pasta with Marinara Sauce - $14.75
Pasta with Garlic & Oil - $14.75
Pasta with Broccoli Garlic & Oil - $15.75
Pasta Bolognese - $16.75
Pasta with Vodka Sauce - $16.50
Pasta with Spicy Vodka Sauce - $17.50
Spaghetti Alla Carbonara - $16.50
Pasta with Alfredo Sauce - $16.75
Pasta with Pesto Sauce - $16.00
Pasta with Clam Sauce (red or white) - $16.00
Pasta Primavera - $16.75
Pasta with Butter Sauce - $10.50
Pasta Alla Puttanesca - $10.50

=== BAKED PASTA (served with bread) ===
Baked Ziti - $16.50
Baked Ziti Sicilian Style (with eggplant) - $17.50
Homemade Lasagna - $17.50
Ravioli (cheese, marinara, mozzarella) - $16.50
Lobster Ravioli (vodka sauce) - $18.50
Spinach Ravioli - $15.75
Stuffed Shells - $15.50

=== DINNERS (includes pasta & side salad) ===
Chicken Parmigiana - $20.95
Eggplant Parmigiana - $20.95
Sausage Parmigiana - $20.95
Meatball Parmigiana - $20.95
Chicken Francaise - $22.95
Shrimp Parmigiana - $22.50
Chicken Marsala - $23.95
Veal Parmigiana - $23.95
Veal Marsala - $23.95
Shrimp Scampi - $24.95
Shrimp Fra Diavolo - $24.95

=== DESSERTS ===
Cannoli - $6.50
Tiramisu - $6.50
New York Cheesecake - $6.50
Carrot Cake - $6.50
Red Velvet Cake - $6.50
Chocolate Fudge Cake - $6.50
Rainbow Cake - $6.50

=== DRINKS ===
Soda - $2.30
Poland Spring Water - $1.95
San Pellegrino Fruit - $3.50
San Pellegrino Sparkling Water - $4.00
Snapple - $3.75
Joe Tea - $4.99
"""

SYSTEM_PROMPT = f"""You are the friendly order assistant for {RESTAURANT_NAME}, located at {RESTAURANT_ADDRESS}.

You help customers place orders through a conversational chat. Be warm, helpful, and brief.

IMPORTANT RESPONSE FORMAT:
You MUST respond in valid JSON with exactly two fields:
1. "message": Your conversational response text
2. "options": An array of clickable option strings for the customer (2-6 options). Use these strategically:
   - For menu browsing: show category options
   - For item selection: show popular items in that category
   - For customization: show available choices
   - Always include a "Something else" or "View more options" when relevant
   - At checkout: show "Pickup" and "Delivery"

FLOW:
1. Greet the customer and ask what they'd like to order. Show main menu categories as options.
2. When they pick a category, show popular items. Keep descriptions short.
3. After each item is added, ask if they want anything else. Show options like "Add more items", "View menu categories", "Checkout".
4. At checkout, ask for the customer's FULL NAME for the order.
5. Then ask for their PHONE NUMBER so the restaurant can reach them about the order.
6. Then ask how they'd like to PAY. Show "Cash" and "Card" as options.
7. Then ask "Pickup" or "Delivery" as options.
8. If PICKUP: Show the restaurant address ({RESTAURANT_ADDRESS}) and say pickup will be ready in {PICKUP_ETA}.
9. If DELIVERY: Ask for their delivery address. Once provided, confirm and say estimated delivery is {DELIVERY_ETA}.
10. At the end, provide a clean order summary with: customer name, phone number, payment method, pickup/delivery, all items with individual prices, subtotal, NYC tax (8.875%), and final total.

MENU:
{MENU}

RULES:
- Only offer items that are on the menu above
- Always confirm prices from the menu
- Keep responses concise and friendly
- If a customer asks for something not on the menu, politely let them know and suggest alternatives
- ALWAYS collect the customer's full name, phone number, and payment method (cash or card) BEFORE asking pickup or delivery
- ALWAYS apply NYC restaurant sales tax of 8.875% to every order
- For the order summary, include: customer full name, phone number, payment method (cash/card), pickup or delivery, each item with its price, subtotal (before tax), tax amount (8.875%), and final total (subtotal + tax)
- ALWAYS respond in valid JSON format with "message" and "options" fields
- Options should be short (2-5 words each)
- Include 2-6 options per response

Example response format:
{{"message": "Welcome to Claudio Pizzeria! What can I get started for you today?", "options": ["Pizza", "Pasta", "Heroes & Wraps", "Appetizers & Sides", "Salads", "Drinks & Desserts"]}}
"""


# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{RESTAURANT_NAME} - Order Online",
    page_icon="🍕",
    layout="centered",
)

# ── Custom Styling ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@400;600&display=swap');

    .restaurant-header {
        text-align: center;
        padding: 1.5rem 0 1rem;
    }
    .restaurant-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #C41E3A;
        margin-bottom: 0.2rem;
    }
    .restaurant-header p {
        font-family: 'Source Sans 3', sans-serif;
        color: #666;
        font-size: 0.95rem;
    }
    .restaurant-header .address {
        font-size: 0.85rem;
        color: #888;
    }

    /* Style the option buttons */
    .stButton > button {
        border: 1.5px solid #C41E3A !important;
        border-radius: 20px !important;
        color: #C41E3A !important;
        background-color: white !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.4rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #C41E3A !important;
        color: white !important;
    }

    /* Chat message styling */
    .stChatMessage {
        font-family: 'Source Sans 3', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="restaurant-header">
    <h1>🍕 {RESTAURANT_NAME}</h1>
    <p>Order your favorite food — powered by AI</p>
    <p class="address">📍 {RESTAURANT_ADDRESS} &nbsp;|&nbsp; 📞 {RESTAURANT_PHONE}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Session State Init ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_options" not in st.session_state:
    st.session_state.current_options = []
if "awaiting_address" not in st.session_state:
    st.session_state.awaiting_address = False
if "initialized" not in st.session_state:
    st.session_state.initialized = False


def get_ai_response(user_input):
    """Send message to AI and get structured response."""
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7,
    )

    raw = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": raw})

    # Parse the JSON response
    try:
        # Clean up potential markdown formatting
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("```", 1)[0]
        parsed = json.loads(cleaned)
        message = parsed.get("message", raw)
        options = parsed.get("options", [])
    except (json.JSONDecodeError, KeyError):
        message = raw
        options = []

    return message, options


def handle_input(user_input):
    """Process user input and update chat."""
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    message, options = get_ai_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": message})
    st.session_state.current_options = options


# ── Initialize with greeting ─────────────────────────────────────
if not st.session_state.initialized:
    message, options = get_ai_response("Hi, I'd like to place an order.")
    st.session_state.chat_history.append({"role": "assistant", "content": message})
    st.session_state.current_options = options
    st.session_state.initialized = True

# ── Display Chat History ─────────────────────────────────────────
for msg in st.session_state.chat_history:
    avatar = "🍕" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ── Display Option Buttons ───────────────────────────────────────
if st.session_state.current_options:
    cols = st.columns(min(len(st.session_state.current_options), 3))
    for i, option in enumerate(st.session_state.current_options):
        col_idx = i % min(len(st.session_state.current_options), 3)
        with cols[col_idx]:
            if st.button(option, key=f"opt_{len(st.session_state.chat_history)}_{i}"):
                handle_input(option)
                st.rerun()

# ── Text Input (always available for custom requests) ────────────
if prompt := st.chat_input("Type your order or request here..."):
    handle_input(prompt)
    st.rerun()

# ── Footer ───────────────────────────────────────────────────────
st.markdown("---")
st.caption(f"📍 {RESTAURANT_ADDRESS} &nbsp;|&nbsp; 📞 {RESTAURANT_PHONE} &nbsp;|&nbsp; Open 9:00 AM - 3:00 AM")
