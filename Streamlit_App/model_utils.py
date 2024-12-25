# model_utils.py

import joblib
import pandas as pd
from datetime import datetime
import numpy as np
import streamlit as st

# Load the model
def load_model(path):
    try:
        return joblib.load(path)
    except FileNotFoundError:
        st.error('Error: Model file not found.')
        return None
    except Exception as e:
        st.error(f'An error occurred while loading the model: {e}')
        return None

# Generate model predictions
def generate_forecast(start_date, end_date, product_type, model):
    if model:
        n_periods = (end_date - start_date).days // 30
        if n_periods < 1:
            n_periods = 1

        forecast, conf_int = model.predict(n_periods=n_periods, return_conf_int=True)

        # Adjust forecast to simulate different products
        adjustment_factor = (hash(product_type) % 5) / 100  # Creates a small variation
        forecast_adjusted = forecast * (1 + adjustment_factor)
        conf_int_adjusted = conf_int * (1 + adjustment_factor)

        forecast_index = pd.date_range(start=start_date, periods=n_periods, freq='M')
        forecast_df = pd.DataFrame({
            'Date': forecast_index,
            'Forecast': forecast_adjusted,
            'Lower CI': conf_int_adjusted[:, 0],
            'Upper CI': conf_int_adjusted[:, 1],
            'Product': product_type
        })

        # Calculate resource requirements (e.g., staff hours)
        # Ensure that Resource Requirement is non-negative
        resource_factor = 0.1  # Adjust this factor based on your business needs
        forecast_df['Resource Requirement'] = forecast_df['Forecast'].clip(lower=0) * resource_factor

        return forecast_df
    return None
