import streamlit as st
from datetime import date

st.set_page_config(
    page_title="My Invoice App",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 My Invoice App")
st.write("Enter customer and product details to generate an invoice.")

st.divider()

# Customer Details
st.subheader("Customer Details")

customer_name = st.text_input("Customer Name")
customer_email = st.text_input("Customer Email")
customer_phone = st.text_input("Customer Phone")
customer_address = st.text_area("Customer Address")

st.divider()

# Invoice Details
st.subheader("Invoice Details")

invoice_number = st.text_input("Invoice Number", value="INV-001")
invoice_date = st.date_input("Invoice Date", value=date.today())

st.divider()

# Product Details
st.subheader("Product Details")

number_of_products = st.number_input(
    "Number of Products",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

products = []

for i in range(int(number_of_products)):
    st.markdown(f"### Product {i + 1}")

    col1, col2, col3 = st.columns(3)

    with col1:
        product_name = st.text_input(
            "Product Name",
            key=f"name_{i}"
        )

    with col2:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
            key=f"quantity_{i}"
        )

    with col3:
        price = st.number_input(
            "Price (₹)",
            min_value=0.0,
            value=0.0,
            step=0.01,
            key=f"price_{i}"
        )

    total = quantity * price

    products.append({
        "name": product_name,
        "quantity": quantity,
        "price": price,
        "total": total
    })

st.divider()

# GST
st.subheader("Tax Details")

gst_rate = st.number_input(
    "GST (%)",
    min_value=0.0,
    max_value=100.0,
    value=18.0,
    step=0.5
)

# Calculate totals
subtotal = 0

for product in products:
    subtotal += product["total"]

gst_amount = subtotal * gst_rate / 100
grand_total = subtotal + gst_amount

st.divider()

# Generate Invoice
if st.button("Generate Invoice", type="primary"):

    if customer_name.strip() == "":
        st.error("Please enter the customer name.")

    elif all(product["name"].strip() == "" for product in products):
        st.error("Please enter at least one product name.")

    else:

        st.success("Invoice generated successfully!")

        st.subheader("🧾 Invoice")

        st.write(f"**Invoice Number:** {invoice_number}")
        st.write(f"**Date:** {invoice_date}")

        st.markdown("### Customer Information")

        st.write(f"**Name:** {customer_name}")
        st.write(f"**Email:** {customer_email}")
        st.write(f"**Phone:** {customer_phone}")
        st.write(f"**Address:** {customer_address}")

        st.markdown("### Products")

        for product in products:

            if product["name"].strip() != "":

                st.write(
                    f"**{product['name']}** — "
                    f"{product['quantity']} × ₹{product['price']:.2f} "
                    f"= **₹{product['total']:.2f}**"
                )

        st.divider()

        st.write(f"**Subtotal:** ₹{subtotal:.2f}")
        st.write(f"**GST ({gst_rate}%):** ₹{gst_amount:.2f}")
        st.write(f"### Grand Total: ₹{grand_total:.2f}")

        # Create downloadable invoice
        invoice_text = f"""
MY INVOICE
====================================

Invoice Number: {invoice_number}
Date: {invoice_date}

CUSTOMER DETAILS
------------------------------------
Name: {customer_name}
Email: {customer_email}
Phone: {customer_phone}
Address: {customer_address}

PRODUCT DETAILS
------------------------------------
"""

        for product in products:

            if product["name"].strip() != "":
                invoice_text += (
                    f"{product['name']} | "
                    f"Qty: {product['quantity']} | "
                    f"Price: ₹{product['price']:.2f} | "
                    f"Total: ₹{product['total']:.2f}\n"
                )

        invoice_text += f"""
------------------------------------

Subtotal: ₹{subtotal:.2f}
GST ({gst_rate}%): ₹{gst_amount:.2f}

GRAND TOTAL: ₹{grand_total:.2f}

====================================
Thank you for your business!
"""

        st.download_button(
            label="⬇️ Download Invoice",
            data=invoice_text,
            file_name=f"{invoice_number}.txt",
            mime="text/plain"
        )