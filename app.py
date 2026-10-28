
import streamlit as st

st.set_page_config(
    page_title="SmartCar - Car Price Prediction",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

home_page = st.Page(
    "home.py",
    title="Home",
    icon="🚗",
    default=True,
)

predict_page = st.Page(
    "pages/1_Predict_Price.py",
    title="Predict Price",
    icon="💰",
)

compare_page = st.Page(
    "pages/2_Compare_Cars.py",
    title="Compare Cars",
    icon="🔄",
)

browse_page = st.Page(
    "pages/3_Browse_Cars.py",
    title="Browse Cars",
    icon="🚘",
)

market_page = st.Page(
    "pages/4_Market_Analysis.py",
    title="Market Analysis",
    icon="📊",
)

about_page = st.Page(
    "pages/5_About.py",
    title="About",
    icon="ℹ️",
)

navigation = st.navigation(
    [
        home_page,
        predict_page,
        compare_page,
        browse_page,
        market_page,
        about_page,
    ]
)

navigation.run()
