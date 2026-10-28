import streamlit as st


st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)


st.title("ℹ️ About SmartCar")


st.subheader(
    "🚗 Smart Car Cost Prediction System"
)


st.write(
    """
    SmartCar is a machine-learning-based car price
    prediction project developed as a BSCCS mini project.
    """
)


st.divider()


st.header("🎯 Project Objective")


st.write(
    """
    The objective of this project is to predict the
    estimated price of a used car based on its
    characteristics such as brand, model, year,
    fuel type, transmission, kilometers driven,
    engine, ownership and mileage.
    """
)


st.header("🧠 Machine Learning")


st.write(
    """
    A Random Forest Regression model is used to
    estimate the car price from historical car data.
    """
)


st.header("⭐ Features")


features = [
    "AI-based car price prediction",
    "Car comparison",
    "Car browsing and filtering",
    "Market price analysis",
    "Interactive graphs",
    "Estimated price range"
]


for feature in features:

    st.write(
        f"✅ {feature}"
    )


st.header("🛠️ Technologies")


st.write(
    """
    Python

    Streamlit

    Pandas

    NumPy

    Scikit-learn

    Plotly

    Machine Learning
    """
)
