import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 E-Commerce Sales Analysis Dashboard")
st.markdown("Analyze sales performance, revenue, and customer trends.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload E-Commerce Sales CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Read Data
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Convert Order Date
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])

    # KPIs
    st.subheader("📊 Key Performance Indicators")

    total_sales = df['Sales'].sum()
    total_orders = len(df)
    avg_order_value = total_sales / total_orders

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹{total_sales:,.2f}")
    col2.metric("Total Orders", total_orders)
    col3.metric("Avg Order Value", f"₹{avg_order_value:,.2f}")

    # Sales by Category
    if 'Category' in df.columns:
        st.subheader("📦 Sales by Category")

        category_sales = df.groupby('Category')['Sales'].sum().reset_index()

        fig = px.bar(
            category_sales,
            x='Category',
            y='Sales',
            color='Category',
            title='Sales by Category'
        )

        st.plotly_chart(fig, use_container_width=True)

    # Sales Trend
    if 'Order Date' in df.columns:
        st.subheader("📈 Sales Trend")

        sales_trend = (
            df.groupby('Order Date')['Sales']
            .sum()
            .reset_index()
        )

        fig2 = px.line(
            sales_trend,
            x='Order Date',
            y='Sales',
            title='Daily Sales Trend'
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Top Products
    if 'Product Name' in df.columns:
        st.subheader("🏆 Top 10 Products")

        top_products = (
            df.groupby('Product Name')['Sales']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig3 = px.bar(
            top_products,
            x='Sales',
            y='Product Name',
            orientation='h',
            title='Top 10 Products'
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Region Analysis
    if 'Region' in df.columns:
        st.subheader("🌍 Sales by Region")

        region_sales = (
            df.groupby('Region')['Sales']
            .sum()
            .reset_index()
        )

        fig4 = px.pie(
            region_sales,
            names='Region',
            values='Sales',
            title='Regional Sales Distribution'
        )

        st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("👆 Upload a CSV file to begin analysis.")