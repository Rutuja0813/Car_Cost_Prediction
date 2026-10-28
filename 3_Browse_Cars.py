
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Import the data loader safely
from utils.data_loader import load_car_data

# Page configuration
st.set_page_config(
    page_title="Browse Cars | SmartCar",
    page_icon="🔎",
    layout="wide"
)

# Page title
st.title("🔎 Browse Cars")
st.write("Explore car details available in the SmartCar dataset.")

st.divider()


# Load car dataset
@st.cache_data
def get_car_data():
    try:
        data = load_car_data()

        if data is None:
            return pd.DataFrame()

        return data

    except Exception:
        # Fallback: read the CSV directly
        csv_path = PROJECT_DIR / "car_data_expanded.csv"

        if csv_path.exists():
            return pd.read_csv(csv_path)

        return pd.DataFrame()


df = get_car_data()

# Check dataset
if df.empty:
    st.error(
        "Car dataset is empty or could not be loaded. "
        "Check that car_data_expanded.csv exists in your project folder."
    )
    st.stop()

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Check required columns
required_columns = [
    "brand",
    "model",
    "year",
    "fuel",
    "transmission",
    "km_driven",
    "engine",
    "owners",
    "mileage",
    "price"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    st.error(
        "The dataset is missing these columns: "
        + ", ".join(missing_columns)
    )
    st.write("Available columns:", list(df.columns))
    st.stop()

# Convert numeric columns safely
numeric_columns = [
    "year",
    "km_driven",
    "engine",
    "owners",
    "mileage",
    "price"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows without essential information
df = df.dropna(subset=["brand", "model", "price"])

if df.empty:
    st.warning("No valid car records are available.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔧 Filter Cars")

brands = sorted(df["brand"].dropna().astype(str).unique())

selected_brands = st.sidebar.multiselect(
    "Select Brand",
    options=brands,
    default=[]
)

fuel_types = sorted(df["fuel"].dropna().astype(str).unique())

selected_fuels = st.sidebar.multiselect(
    "Select Fuel Type",
    options=fuel_types,
    default=[]
)

transmissions = sorted(
    df["transmission"].dropna().astype(str).unique()
)

selected_transmissions = st.sidebar.multiselect(
    "Select Transmission",
    options=transmissions,
    default=[]
)

years = df["year"].dropna()

if not years.empty:
    min_year = int(years.min())
    max_year = int(years.max())

    selected_years = st.sidebar.slider(
        "Manufacturing Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
else:
    selected_years = None

prices = df["price"].dropna()

if not prices.empty and prices.min() < prices.max():
    min_price = float(prices.min())
    max_price = float(prices.max())

    selected_prices = st.sidebar.slider(
        "Price Range (₹)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )
else:
    selected_prices = None

# Search by brand or model
search_text = st.text_input(
    "🔍 Search by car brand or model",
    placeholder="Example: Honda, Swift, City, BMW..."
)

# Apply filters
filtered_df = df.copy()

if selected_brands:
    filtered_df = filtered_df[
        filtered_df["brand"].astype(str).isin(selected_brands)
    ]

if selected_fuels:
    filtered_df = filtered_df[
        filtered_df["fuel"].astype(str).isin(selected_fuels)
    ]

if selected_transmissions:
    filtered_df = filtered_df[
        filtered_df["transmission"].astype(str).isin(
            selected_transmissions
        )
    ]

if selected_years is not None:
    filtered_df = filtered_df[
        filtered_df["year"].between(
            selected_years[0],
            selected_years[1]
        )
    ]

if selected_prices is not None:
    filtered_df = filtered_df[
        filtered_df["price"].between(
            selected_prices[0],
            selected_prices[1]
        )
    ]

if search_text.strip():
    search = search_text.strip().lower()

    filtered_df = filtered_df[
        filtered_df["brand"].astype(str).str.lower().str.contains(
            search, na=False
        )
        |
        filtered_df["model"].astype(str).str.lower().str.contains(
            search, na=False
        )
    ]

# Summary metrics
st.subheader("📊 Car Dataset Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Cars", f"{len(df):,}")

with col2:
    st.metric("Matching Cars", f"{len(filtered_df):,}")

with col3:
    st.metric(
        "Available Brands",
        f"{df['brand'].nunique():,}"
    )

st.divider()

# Display results
st.subheader("🚗 Available Cars")

if filtered_df.empty:
    st.warning("No cars match your filters. Please change your selection.")
else:
    display_columns = [
        "brand",
        "model",
        "year",
        "fuel",
        "transmission",
        "km_driven",
        "engine",
        "owners",
        "mileage",
        "price"
    ]

    display_df = filtered_df[display_columns].copy()

    # Format price for easier reading
    display_df["price"] = display_df["price"].apply(
        lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A"
    )

    display_df = display_df.rename(
        columns={
            "brand": "Brand",
            "model": "Model",
            "year": "Year",
            "fuel": "Fuel",
            "transmission": "Transmission",
            "km_driven": "KM Driven",
            "engine": "Engine",
            "owners": "Owners",
            "mileage": "Mileage",
            "price": "Price"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Download filtered cars
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Cars (CSV)",
        data=csv_data,
        file_name="smartcar_filtered_cars.csv",
        mime="text/csv"
    )

st.caption(
    "Note: Prices shown are based on the project's dataset. "
    "They may not represent current market prices."
)
