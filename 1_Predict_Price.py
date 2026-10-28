
import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# -------------------------------------------------
# PROJECT PATH
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.prediction import load_model, predict_price


# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="SmartCar - Predict Car Price",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 SmartCar - Car Price Prediction")
st.write("Enter your car details to estimate its resale price.")
st.divider()


# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------

@st.cache_data
def get_car_data():
    possible_files = [
        PROJECT_ROOT / "car_data_expanded.csv",
        PROJECT_ROOT / "car_data_expanded.csv",
        PROJECT_ROOT / "car_data.csv",
    ]

    for file_path in possible_files:
        if file_path.exists():
            data = pd.read_csv(file_path)

            required_columns = [
                "brand", "model", "year", "fuel",
                "transmission", "km_driven", "engine",
                "owners", "mileage", "price"
            ]

            missing = [
                column for column in required_columns
                if column not in data.columns
            ]

            if missing:
                raise ValueError(
                    f"Missing CSV columns: {', '.join(missing)}"
                )

            data = data.dropna(subset=required_columns)
            return data

    raise FileNotFoundError(
        "Dataset not found. Place car_data_expanded_1200.csv "
        "or car_data_expanded.csv in the main project folder."
    )


try:
    df = get_car_data()

except Exception as error:
    st.error(f"Could not load the car dataset: {error}")
    st.stop()


# -------------------------------------------------
# LOAD TRAINED MODEL
# -------------------------------------------------

try:
    model = load_model()

except Exception as error:
    st.error("Could not load the trained model.")
    st.write(str(error))
    st.info(
        "Check that car_price_model.pkl exists and that "
        "the model has been trained using train_model.py."
    )
    st.stop()


# -------------------------------------------------
# PREPARE DROPDOWN OPTIONS
# -------------------------------------------------

brands = sorted(df["brand"].astype(str).unique().tolist())

fuel_types = sorted(
    df["fuel"].astype(str).unique().tolist()
)

transmissions = sorted(
    df["transmission"].astype(str).unique().tolist()
)


if not brands or not fuel_types or not transmissions:
    st.error("The dataset does not contain enough car details.")
    st.stop()


# -------------------------------------------------
# CAR DETAILS FORM
# -------------------------------------------------

st.subheader("📋 Enter Car Details")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        brand = st.selectbox("Car Brand", brands)

        brand_models = sorted(
            df.loc[df["brand"] == brand, "model"]
            .astype(str)
            .unique()
            .tolist()
        )

        model_name = st.selectbox("Car Model", brand_models)

        min_year = int(df["year"].min())
        max_year = max(2026, int(df["year"].max()))

        year = st.number_input(
            "Manufacturing Year",
            min_value=min_year,
            max_value=max_year,
            value=min(2020, max_year),
            step=1
        )

        fuel = st.selectbox("Fuel Type", fuel_types)

        transmission = st.selectbox(
            "Transmission",
            transmissions
        )

    with col2:
        km_driven = st.number_input(
            "Kilometers Driven",
            min_value=0,
            max_value=1_000_000,
            value=40_000,
            step=1_000
        )

        engine = st.number_input(
            "Engine Capacity (cc)",
            min_value=500.0,
            max_value=8_000.0,
            value=1500.0,
            step=50.0
        )

        owners = st.number_input(
            "Previous Owners",
            min_value=0,
            max_value=10,
            value=1,
            step=1
        )

        mileage = st.number_input(
            "Mileage (km/l)",
            min_value=1.0,
            max_value=100.0,
            value=18.0,
            step=0.5
        )

    submitted = st.form_submit_button(
        "🔮 Predict Car Price",
        use_container_width=True
    )


# -------------------------------------------------
# PREDICT PRICE
# -------------------------------------------------

if submitted:
    try:
        price = predict_price(
            model=model,
            brand=brand,
            model_name=model_name,
            year=int(year),
            fuel=fuel,
            transmission=transmission,
            km_driven=int(km_driven),
            engine=float(engine),
            owners=int(owners),
            mileage=float(mileage)
        )

        price = float(price)

        if not pd.notna(price) or price <= 0:
            raise ValueError(
                "The model returned an invalid price. "
                "Please check the training data and model."
            )

        st.success("Price prediction completed!")

        st.divider()
        st.subheader("💰 Estimated Car Price")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Estimated Price",
                f"₹{price:,.0f}"
            )

        with col2:
            st.metric(
                "Illustrative Lower Range",
                f"₹{price * 0.90:,.0f}"
            )

        with col3:
            st.metric(
                "Illustrative Upper Range",
                f"₹{price * 1.10:,.0f}"
            )

        st.caption(
            "The ±10% range is illustrative, not a validated "
            "confidence interval or guaranteed market price."
        )

        st.divider()
        st.subheader("🚘 Your Car Details")

        details_col1, details_col2 = st.columns(2)

        with details_col1:
            st.write(f"**Brand:** {brand.title()}")
            st.write(f"**Model:** {model_name.title()}")
            st.write(f"**Year:** {int(year)}")
            st.write(f"**Fuel:** {fuel.title()}")
            st.write(f"**Transmission:** {transmission.title()}")

        with details_col2:
            st.write(f"**Kilometers driven:** {km_driven:,.0f} km")
            st.write(f"**Engine:** {engine:,.0f} cc")
            st.write(f"**Previous owners:** {owners}")
            st.write(f"**Mileage:** {mileage} km/l")

    except Exception as error:
        st.error("Price prediction failed.")
        st.code(str(error))

st.divider()
st.caption(
    "SmartCar | BSc Computer Science Mini Project | "
    "Predictions depend on the dataset and trained model."
)