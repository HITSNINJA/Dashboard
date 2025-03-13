import streamlit as st
import pandas as pd
import plotly.express as px

orders = pd.read_csv("data/orders_dataset_cleaned.csv")
customers = pd.read_csv("data/customers_dataset.csv")
geolocation = pd.read_csv("data/geolocation_dataset.csv")

orders_customers = orders.merge(customers, on="customer_id", how="left")

geolocation_sample = geolocation.sample(n=10000, random_state=42)

st.title("E-Commerce Analysis Dashboard")

orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

orders["order_hour"] = orders["order_purchase_timestamp"].dt.hour

orders_per_hour = orders["order_hour"].value_counts().sort_index()

st.header("Frekuensi Pembelian dalam 24 Jam")
fig_order_hour = px.line(
    x=orders_per_hour.index,
    y=orders_per_hour.values,
    markers=True,
    labels={"x": "Jam", "y": "Jumlah Pesanan"},
    title="Frekuensi Pembelian dalam 24 Jam",
)
st.plotly_chart(fig_order_hour)


st.header("Wilayah dengan Penggunaan E-Commerce Terbanyak")
top_cities = orders_customers["customer_city"].value_counts().head(10)
fig_top_cities = px.bar(top_cities, x=top_cities.index, y=top_cities.values, title="Top 10 Kota dengan Penggunaan E-Commerce")
st.plotly_chart(fig_top_cities)

st.header("Wilayah dengan Penggunaan E-Commerce Tersedikit")
bottom_cities = orders_customers["customer_city"].value_counts().tail(10)
fig_bottom_cities = px.bar(bottom_cities, x=bottom_cities.index, y=bottom_cities.values, title="10 Kota dengan Penggunaan E-Commerce Terendah")
st.plotly_chart(fig_bottom_cities)

st.header("Analisis Geospatial")
fig_map = px.scatter_mapbox(
    geolocation_sample,
    lat="geolocation_lat",
    lon="geolocation_lng",
    color_discrete_sequence=["blue"],
    title="Sebaran Lokasi E-Commerce (10.000 Sampel)",
    mapbox_style="open-street-map",
    zoom=3,
)
st.plotly_chart(fig_map)
