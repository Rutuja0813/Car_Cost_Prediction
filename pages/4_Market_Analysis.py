import streamlit as st
import plotly.express as px

from utils.data_loader import load_car_data


st.set_page_config(
    page_title="Market Analysis",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Car Market Analysis")


df = load_car_data()


if df.empty:

    st.error(
        "Dataset not found."
    )

    st.stop()


# -------------------------------------------------
# STATISTICS
# -------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Price",
        f"₹{df['price'].mean():,.0f}"
    )


with col2:

    st.metric(
        "Minimum Price",
        f"₹{df['price'].min():,.0f}"
    )


with col3:

    st.metric(
        "Maximum Price",
        f"₹{df['price'].max():,.0f}"
    )


st.divider()


# -------------------------------------------------
# PRICE VS YEAR
# -------------------------------------------------

st.subheader(
    "📈 Price vs Manufacturing Year"
)


fig1 = px.scatter(
    df,
    x="year",
    y="price",
    title="Car Price vs Year",
    hover_data=[
        "brand",
        "model"
    ]
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# -------------------------------------------------
# PRICE VS KM
# -------------------------------------------------

st.subheader(
    "🛣️ Price vs Kilometers Driven"
)


fig2 = px.scatter(
    df,
    x="km_driven",
    y="price",
    title="Car Price vs Kilometers"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# -------------------------------------------------
# BRAND PRICE
# -------------------------------------------------

st.subheader(
    "🏷️ Average Price by Brand"
)


brand_price = (
    df.groupby("brand")["price"]
    .mean()
    .reset_index()
    .sort_values(
        "price",
        ascending=False
    )
)


fig3 = px.bar(
    brand_price,
    x="brand",
    y="price",
    title="Average Price by Brand"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)
