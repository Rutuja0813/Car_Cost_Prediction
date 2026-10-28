import streamlit as st
from pathlib import Path


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="SmartCar - Car Price Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


# =========================================================
# FIND CAR BANNER IMAGE
# =========================================================

IMAGE_PATH = None

possible_extensions = [
    "jpg",
    "jpeg",
    "png",
    "webp"
]

for extension in possible_extensions:

    possible_file = ASSETS_DIR / f"car_banner.{extension}"

    if possible_file.is_file():
        IMAGE_PATH = possible_file
        break


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Page spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* SmartCar title */
    .main-title {
        font-size: 48px;
        font-weight: 700;
        color: #172554;
        margin-bottom: 0;
    }

    /* Subtitle */
    .subtitle {
        font-size: 20px;
        color: #64748b;
        margin-bottom: 20px;
    }

    /* Feature cards */
    .feature-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        background-color: #f8fafc;
        min-height: 180px;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Banner */
    .banner-container {
        margin-top: 10px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🚗 SmartCar</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Car Price Prediction</div>',
    unsafe_allow_html=True
)


# =========================================================
# HERO BANNER
# =========================================================

if IMAGE_PATH is not None:

    st.markdown(
        '<div class="banner-container">',
        unsafe_allow_html=True
    )

    st.image(
        str(IMAGE_PATH),
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.error("❌ Car banner image was not found.")

    st.write("Python searched inside:")

    st.code(str(ASSETS_DIR))

    st.write("Files currently found in the assets folder:")

    if ASSETS_DIR.exists():

        files_found = list(ASSETS_DIR.iterdir())

        if files_found:

            for file in files_found:
                st.write("📄", file.name)

        else:

            st.warning("The assets folder is empty.")

    else:

        st.error("❌ The assets folder does not exist.")


# =========================================================
# HERO TEXT
# =========================================================

st.markdown(
    """
    # Know Your Car's True Value

    Get accurate car price predictions using machine learning.

    Compare vehicles, explore market trends and make smarter decisions.
    """
)


# =========================================================
# PREDICT PRICE BUTTON
# =========================================================

if st.button(
    "🔮 Predict Car Price",
    type="primary",
    use_container_width=True
):

    st.switch_page("pages/1_Predict_Price.py")


st.divider()


# =========================================================
# SMART FEATURES
# =========================================================

st.header("⭐ Smart Features")

col1, col2, col3, col4 = st.columns(4)


# =========================================================
# FEATURE 1 - PRICE PREDICTION
# =========================================================

with col1:

    st.markdown("### 💰 Price Prediction")

    st.write(
        "Get an estimated price for your car "
        "using our machine learning model."
    )

    if st.button(
        "Learn More →",
        key="price_prediction"
    ):

        st.switch_page(
            "pages/1_Predict_Price.py"
        )


# =========================================================
# FEATURE 2 - COMPARE CARS
# =========================================================

with col2:

    st.markdown("### 🔄 Compare Cars")

    st.write(
        "Compare specifications and prices "
        "of different cars side by side."
    )

    if st.button(
        "Learn More →",
        key="compare_cars"
    ):

        st.switch_page(
            "pages/2_Compare_Cars.py"
        )


# =========================================================
# FEATURE 3 - MARKET ANALYSIS
# =========================================================

with col3:

    st.markdown("### 📊 Market Analysis")

    st.write(
        "Explore car prices using graphs "
        "and detailed market information."
    )

    if st.button(
        "Learn More →",
        key="market_analysis"
    ):

        st.switch_page(
            "pages/4_Market_Analysis.py"
        )


# =========================================================
# FEATURE 4 - RECOMMENDATIONS
# =========================================================

with col4:

    st.markdown("### 💡 Smart Recommendations")

    st.write(
        "Explore cars based on your "
        "budget and requirements."
    )

    if st.button(
        "Learn More →",
        key="recommendations"
    ):

        st.switch_page(
            "pages/3_Browse_Cars.py"
        )


st.divider()


# =========================================================
# HOW IT WORKS
# =========================================================

st.header("🚀 How It Works")

st.caption(
    "Get your car's estimated value in four simple steps."
)

col1, col2, col3, col4 = st.columns(4)


# =========================================================
# STEP 1
# =========================================================

with col1:

    st.markdown("### 1️⃣ Enter Car Details")

    st.write(
        "Provide basic information about your car."
    )


# =========================================================
# STEP 2
# =========================================================

with col2:

    st.markdown("### 2️⃣ AI Processes Data")

    st.write(
        "Our machine learning model analyzes "
        "your car information."
    )


# =========================================================
# STEP 3
# =========================================================

with col3:

    st.markdown("### 3️⃣ Get Estimated Price")

    st.write(
        "View the predicted price of your car."
    )


# =========================================================
# STEP 4
# =========================================================

with col4:

    st.markdown("### 4️⃣ Make a Decision")

    st.write(
        "Compare cars and make a smarter decision."
    )


st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "🚗 SmartCar | AI-Powered Car Price Prediction"
)