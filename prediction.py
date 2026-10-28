import os
import pickle
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "car_price_model.pkl"
)


def load_model():

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            "car_price_model.pkl not found."
        )

    with open(
        MODEL_FILE,
        "rb"
    ) as file:

        model = pickle.load(file)

    return model


def predict_price(
    model,
    brand,
    model_name,
    year,
    fuel,
    transmission,
    km_driven,
    engine,
    owners,
    mileage
):

    input_data = pd.DataFrame(
        [
            {
                "brand": brand,
                "model": model_name,
                "year": year,
                "fuel": fuel,
                "transmission": transmission,
                "km_driven": km_driven,
                "engine": engine,
                "owners": owners,
                "mileage": mileage
            }
        ]
    )

    prediction = model.predict(
        input_data
    )

    return float(prediction[0])