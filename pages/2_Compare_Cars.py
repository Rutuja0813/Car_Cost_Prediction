import streamlit as st
import pandas as pd

from utils.data_loader import load_car_data


st.set_page_config(
    page_title="Compare Cars",
    page_icon="🔄",
    layout="wide"
)


st.title("🔄 Compare Cars")

st.write(
    "Compare two cars using important specifications."
)


df = load_car_data()


if df.empty:

    st.error(
        "Dataset not found."
    )

    st.stop()


brands = sorted(
    df["brand"]
    .dropna()
    .unique()
    .tolist()
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("🚗 Car 1")

    brand1 = st.selectbox(
        "Brand",
        brands,
        key="brand1"
    )

    models1 = sorted(
        df[
            df["brand"] == brand1
        ]["model"]
        .dropna()
        .unique()
        .tolist()
    )

    model1 = st.selectbox(
        "Model",
        models1,
        key="model1"
    )


with col2:

    st.subheader("🚙 Car 2")

    brand2 = st.selectbox(
        "Brand",
        brands,
        key="brand2"
    )

    models2 = sorted(
        df[
            df["brand"] == brand2
        ]["model"]
        .dropna()
        .unique()
        .tolist()
    )

    model2 = st.selectbox(
        "Model",
        models2,
        key="model2"
    )


car1 = df[
    (df["brand"] == brand1) &
    (df["model"] == model1)
].iloc[0]


car2 = df[
    (df["brand"] == brand2) &
    (df["model"] == model2)
].iloc[0]


st.divider()

comparison = pd.DataFrame({

    "Specification": [
        "Brand",
        "Model",
        "Price",
        "Year",
        "Fuel",
        "Transmission",
        "Kilometers",
        "Engine",
        "Owners",
        "Mileage"
    ],

    "Car 1": [
        brand1,
        model1,
        f"₹{car1['price']:,.0f}",
        car1["year"],
        car1["fuel"],
        car1["transmission"],
        f"{car1['km_driven']:,.0f} km",
        f"{car1['engine']} cc",
        car1["owners"],
        f"{car1['mileage']} km/l"
    ],

    "Car 2": [
        brand2,
        model2,
        f"₹{car2['price']:,.0f}",
        car2["year"],
        car2["fuel"],
        car2["transmission"],
        f"{car2['km_driven']:,.0f} km",
        f"{car2['engine']} cc",
        car2["owners"],
        f"{car2['mileage']} km/l"
    ]
})


st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)
