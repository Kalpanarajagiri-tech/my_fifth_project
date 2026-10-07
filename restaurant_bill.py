import streamlit as st
from datetime import datetime
import random

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Foodie Hub - Restaurant Billing",
    page_icon="🍔",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    .main {
        background-color: #f8f9fa;
    }

    .title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #ff4b4b;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .menu-card {
        background-color: white;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        margin-bottom: 15px;
    }

    .bill-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #dddddd;
    }

    .total {
        font-size: 28px;
        font-weight: bold;
        color: #ff4b4b;
    }

    .footer {
        text-align: center;
        color: #777;
        margin-top: 40px;
        padding: 20px;
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# MENU
# --------------------------------------------------

menu = {

    "🍕 Pizza": {
        "Margherita Pizza": 249,
        "Farmhouse Pizza": 299,
        "Cheese Burst Pizza": 349
    },

    "🍔 Burgers": {
        "Classic Burger": 129,
        "Cheese Burger": 159,
        "Veg Supreme Burger": 179
    },

    "🍝 Main Course": {
        "White Sauce Pasta": 199,
        "Red Sauce Pasta": 189,
        "Veg Biryani": 179
    },

    "🍟 Snacks": {
        "French Fries": 89,
        "Peri Peri Fries": 119,
        "Veg Nuggets": 129
    },

    "🥤 Beverages": {
        "Cold Drink": 49,
        "Fresh Lime Soda": 69,
        "Milkshake": 99
    },

    "🍰 Desserts": {
        "Ice Cream": 79,
        "Chocolate Brownie": 129,
        "Gulab Jamun": 89
    }
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🍔 FOODIE HUB</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Restaurant Billing & Order Management System</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# CUSTOMER DETAILS
# --------------------------------------------------

st.subheader("👤 Customer Details")

col1, col2, col3 = st.columns(3)

with col1:
    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter customer name"
    )

with col2:
    table_number = st.selectbox(
        "Table Number",
        ["Takeaway", "Table 1", "Table 2", "Table 3",
         "Table 4", "Table 5", "Table 6"]
    )

with col3:
    order_type = st.selectbox(
        "Order Type",
        ["Dine In", "Takeaway"]
    )

st.divider()

# --------------------------------------------------
# MAIN LAYOUT
# --------------------------------------------------

menu_col, bill_col = st.columns([1.5, 1])

# ==================================================
# MENU SECTION
# ==================================================

with menu_col:

    st.subheader("🍽️ Our Menu")

    for category, items in menu.items():

        st.markdown(f"### {category}")

        for item, price in items.items():

            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{item}**")

            with col2:
                st.write(f"₹{price}")

            with col3:

                if st.button(
                    "➕ Add",
                    key=f"add_{item}",
                    use_container_width=True
                ):

                    if item in st.session_state.cart:
                        st.session_state.cart[item]["quantity"] += 1
                    else:
                        st.session_state.cart[item] = {
                            "price": price,
                            "quantity": 1
                        }

                    st.rerun()

# ==================================================
# BILL SECTION
# ==================================================

with bill_col:

    st.subheader("🧾 Your Order")

    if len(st.session_state.cart) == 0:

        st.info(
            "🛒 Your cart is empty.\n\n"
            "Click **Add** beside a food item."
        )

    else:

        subtotal = 0

        # ------------------------------------------
        # CART ITEMS
        # ------------------------------------------

        for item, details in list(
            st.session_state.cart.items()
        ):

            price = details["price"]
            quantity = details["quantity"]

            item_total = price * quantity

            subtotal += item_total

            st.markdown(
                f"**{item}**  \n"
                f"₹{price} × {quantity} = **₹{item_total}**"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                if st.button(
                    "➖",
                    key=f"minus_{item}"
                ):

                    st.session_state.cart[item]["quantity"] -= 1

                    if st.session_state.cart[item]["quantity"] <= 0:
                        del st.session_state.cart[item]

                    st.rerun()

            with col2:

                st.write(
                    f"Qty: {quantity}"
                )

            with col3:

                if st.button(
                    "➕",
                    key=f"plus_{item}"
                ):

                    st.session_state.cart[item]["quantity"] += 1

                    st.rerun()

            st.divider()

        # ------------------------------------------
        # BILL CALCULATION
        # ------------------------------------------

        st.markdown("### 💰 Bill Summary")

        discount_percent = st.slider(
            "Discount (%)",
            min_value=0,
            max_value=30,
            value=0
        )

        gst_percent = st.selectbox(
            "GST (%)",
            [0, 5, 12, 18],
            index=1
        )

        discount = subtotal * discount_percent / 100

        amount_after_discount = subtotal - discount

        gst = amount_after_discount * gst_percent / 100

        grand_total = amount_after_discount + gst

        # ------------------------------------------
        # SUMMARY
        # ------------------------------------------

        st.write(f"Subtotal: **₹{subtotal:.2f}**")

        st.write(
            f"Discount ({discount_percent}%): "
            f"**- ₹{discount:.2f}**"
        )

        st.write(
            f"GST ({gst_percent}%): "
            f"**₹{gst:.2f}**"
        )

        st.divider()

        st.markdown(
            f'<div class="total">'
            f'Grand Total: ₹{grand_total:.2f}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.write("")

        # ------------------------------------------
        # GENERATE BILL
        # ------------------------------------------

        if st.button(
            "🧾 Generate Final Bill",
            type="primary",
            use_container_width=True
        ):

            bill_number = random.randint(
                10000,
                99999
            )

            current_time = datetime.now()

            bill_text = ""

            bill_text += "================================\n"
            bill_text += "          FOODIE HUB\n"
            bill_text += "       RESTAURANT BILL\n"
            bill_text += "================================\n"

            bill_text += f"Bill No: {bill_number}\n"
            bill_text += (
                f"Date: "
                f"{current_time.strftime('%d-%m-%Y %I:%M %p')}\n"
            )

            bill_text += (
                f"Customer: "
                f"{customer_name if customer_name else 'Guest'}\n"
            )

            bill_text += f"Order Type: {order_type}\n"
            bill_text += f"Table: {table_number}\n"

            bill_text += "--------------------------------\n"

            for item, details in st.session_state.cart.items():

                price = details["price"]
                quantity = details["quantity"]

                item_total = price * quantity

                bill_text += (
                    f"{item}\n"
                    f"{quantity} x ₹{price} = ₹{item_total}\n"
                )

            bill_text += "--------------------------------\n"

            bill_text += f"Subtotal: ₹{subtotal:.2f}\n"
            bill_text += f"Discount: -₹{discount:.2f}\n"
            bill_text += f"GST: ₹{gst:.2f}\n"

            bill_text += "--------------------------------\n"

            bill_text += (
                f"GRAND TOTAL: ₹{grand_total:.2f}\n"
            )

            bill_text += "================================\n"
            bill_text += "       Thank You! Visit Again ❤️\n"
            bill_text += "================================\n"

            st.success("✅ Bill generated successfully!")

            st.download_button(
                label="📥 Download Bill",
                data=bill_text,
                file_name=f"FoodieHub_Bill_{bill_number}.txt",
                mime="text/plain",
                use_container_width=True
            )

        # ------------------------------------------
        # CLEAR CART
        # ------------------------------------------

        if st.button(
            "🗑️ Clear Order",
            use_container_width=True
        ):

            st.session_state.cart = {}

            st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="footer">'
    '🍔 Foodie Hub Restaurant Billing System '
    '• Built with Python & Streamlit ❤️'
    '</div>',
    unsafe_allow_html=True
)