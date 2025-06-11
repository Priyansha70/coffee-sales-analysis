import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Coffee Sales Dashboard", layout="centered")

st.title("☕ Coffee Sales Dashboard")
st.markdown("Visualize vending machine trends and coffee sales performance.")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("coffee_sales.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["hour"] = df["datetime"].dt.hour
    return df

df = load_data()

# Sidebar: Coffee selection
coffee_types = df["coffee_name"].unique()
selected_coffee = st.sidebar.selectbox("Select a Coffee Type", coffee_types)

# Line Chart: Monthly sales of selected coffee
monthly_sales = df[df["coffee_name"] == selected_coffee].groupby("month").size()

st.subheader(f"📈 Monthly Sales for {selected_coffee}")
st.line_chart(monthly_sales)

# Bar Chart: Total revenue by product
revenue_by_product = df.groupby("coffee_name")["money"].sum().sort_values(ascending=False)

st.subheader("💰 Total Revenue by Coffee Type")
st.bar_chart(revenue_by_product)

# Pie Chart: Payment method distribution
payment_counts = df["cash_type"].value_counts()

st.subheader("💳 Payment Method Distribution")
fig, ax = plt.subplots()
ax.pie(payment_counts, labels=payment_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)
