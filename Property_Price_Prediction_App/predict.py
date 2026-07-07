import joblib
import pandas as pd
import numpy as np

# Load deployment model
model = joblib.load("model/property_price_model.joblib")


def predict_price(
    neighborhood,
    overall_qual,
    overall_cond,
    property_size,
    gr_liv_area,
    first_flr,
    second_flr,
    year_built,
    total_sf,
    total_bath,
    house_age,
):

    input_data = pd.DataFrame({

        "Neighborhood":[neighborhood],
        "OverallQual":[overall_qual],
        "OverallCond":[overall_cond],
        "PropertySize":[property_size],
        "GrLivArea":[gr_liv_area],
        "1stFlrSF":[first_flr],
        "2ndFlrSF":[second_flr],
        "YearBuilt":[year_built],
        "TotalSF":[total_sf],
        "TotalBath":[total_bath],
        "HouseAge":[house_age]

    })

    prediction = model.predict(input_data)

    # Convert back if target was log-transformed
    prediction = np.expm1(prediction)

    return prediction[0]