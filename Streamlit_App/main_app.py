# main_app.py

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np
# Import functions from other files
from model_utils import load_model, generate_forecast
from assistant_utils import ai_assistant_interaction
from plot_utils import (
    plot_aggregated_forecast,
    plot_cumulative_sales_chart,
    plot_sales_heatmap,
    plot_resource_allocation  # Import the new function
)

# Simple authentication
def authenticate(username, password):
    return username == "admin" and password == "password"

# Define login and logout functions
def login():
    username = st.session_state['username_input']
    password = st.session_state['password_input']
    if authenticate(username, password):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.sidebar.success("Logged in successfully.")
    else:
        st.sidebar.error("Incorrect username or password.")

def logout():
    # Clear session state variables
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state['logged_in'] = False
    st.sidebar.success("Logged out successfully.")

# Page configuration
st.set_page_config(page_title="Comprehensive Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# User Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Sidebar - Login/Logout
if not st.session_state['logged_in']:
    st.sidebar.text_input("Username", key='username_input')
    st.sidebar.text_input("Password", type="password", key='password_input')
    st.sidebar.button('Login', on_click=login)
else:
    st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
    st.sidebar.button('Logout', on_click=logout)

# Main Application
if st.session_state.get('logged_in'):
    st.title('Comprehensive Dashboard for Fashion Retail Sales Prediction with AI Assistant')

    st.write("""
        Welcome to the Fashion Retail Forecast and AI Assistant Dashboard!

        This dashboard has three main features:

        1. **Interacting with an AI Assistant**: You can ask questions related to fashion retail data or general sales trends.
        2. **Viewing Sales Forecasts**: Access sales forecasts for fashion retail products.
        3. **Resource Allocation Dashboard**: Assist in planning by forecasting resource requirements based on sales predictions.

        **Please note:** Our predictive model uses historical data to make forecasts. While we strive for accuracy, the model may have limitations due to factors like data quality, market volatility, and unforeseen events. Always consider these forecasts as estimates and complement them with professional judgment.
    """)

    tab1, tab2, tab3 = st.tabs(["Chat with AI", "Fashion Retail Forecast", "Resource Allocation Dashboard"])

    # Load the model
    model = load_model('autoarima_model.pkl')

    # AI Assistant Interaction
    with tab1:
        ai_assistant_interaction(model, generate_forecast)

    # Forecast Dashboard
    with tab2:
        st.subheader('Fashion Retail Trend Forecast Dashboard')
        st.write("""
            This section provides sales forecasts for various fashion retail products.
            Use the options below to specify the date range and product types you're interested in.
            The model uses historical data to make these forecasts, which are shown in the interactive charts below.

            **Limitations of the Predictive Model:**
            - **Data Quality**: The accuracy of the forecasts depends on the quality and completeness of the historical data.
            - **Market Volatility**: Sudden market changes, economic events, or unforeseen circumstances may impact actual sales differently than predicted.
            - **Assumptions**: The model makes certain assumptions about trends and patterns that may not hold in all situations.

            **Please use these forecasts as guidance and complement them with professional expertise and current market analysis.**
        """)

        # Date range selection
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Select start date", datetime.today())
        end_date = col2.date_input("Select end date", datetime.today() + timedelta(days=90))

        if (end_date - start_date).days < 30:
            st.warning("Please select a date range of at least 30 days for meaningful predictions.")

        # Product type selection
        product_types = [
            "Women's Dresses", "Jeans", "Casual Wear", "Formal Wear", "Athletic Apparel",
            "Footwear", "Accessories", "Handbags", "Children's Clothing", "All Products"
        ]
        selected_products = st.multiselect("Select product types", product_types, default=["All Products"])

        if st.button('Predict Sales', key='predict'):
            if model:
                # If "All Products" is selected, include all products
                if "All Products" in selected_products:
                    selected_products = product_types[:-1]  # Exclude "All Products" from the list

                # Generate forecasts for all selected products
                all_forecasts = []
                for product_type in selected_products:
                    forecast_df = generate_forecast(start_date, end_date, product_type, model)
                    if forecast_df is not None:
                        all_forecasts.append(forecast_df)
                    else:
                        st.error(f"Could not generate forecast for {product_type}.")

                if all_forecasts:
                    combined_forecast_df = pd.concat(all_forecasts, ignore_index=True)

                    # Aggregate forecasts
                    aggregated_forecast = combined_forecast_df.groupby('Date').sum().reset_index()
                    aggregated_forecast['Product'] = 'All Products'

                    # Create tabs for multiple charts
                    chart_tab1, chart_tab2, chart_tab3 = st.tabs(
                        ["Aggregated Forecast", "Cumulative Sales", "Sales Heatmap"]
                    )

                    with chart_tab1:
                        st.subheader("Aggregated Sales Forecast")
                        plot_aggregated_forecast(aggregated_forecast)

                    with chart_tab2:
                        st.subheader("Cumulative Sales Forecast")
                        plot_cumulative_sales_chart(aggregated_forecast)

                    with chart_tab3:
                        st.subheader("Sales Forecast Heatmap")
                        plot_sales_heatmap(combined_forecast_df)
                else:
                    st.error("No forecasts to display.")
            else:
                st.error('Model not loaded. Please check model path or load model.')

    # Resource Allocation Dashboard
    with tab3:
        st.subheader('Resource Allocation Dashboard')
        st.write("""
            This section assists in operational planning and workforce management by calculating resource requirements based on forecasted sales volumes.
            Use the options below to specify the date range and product types you're interested in.
            The model calculates the resources needed to meet the predicted demand, helping you optimize your operations.

            **Assumptions:**
            - **Resource Factor:** For this example, we assume that 0.1 staff hours are required per unit sold. You can adjust this factor in the model according to your business needs.
        """)

        # Date range selection
        col1_res, col2_res = st.columns(2)
        start_date_res = col1_res.date_input("Select start date for resource allocation", datetime.today(), key='res_start_date')
        end_date_res = col2_res.date_input("Select end date for resource allocation", datetime.today() + timedelta(days=90), key='res_end_date')

        if (end_date_res - start_date_res).days < 30:
            st.warning("Please select a date range of at least 30 days for meaningful predictions.")

        # Product type selection
        product_types_res = [
            "Women's Dresses", "Jeans", "Casual Wear", "Formal Wear", "Athletic Apparel",
            "Footwear", "Accessories", "Handbags", "Children's Clothing", "All Products"
        ]
        selected_products_res = st.multiselect("Select product types for resource allocation", product_types_res, default=["All Products"], key='res_products')

        if st.button('Calculate Resource Requirements', key='calculate_resources'):
            if model:
                # If "All Products" is selected, include all products
                if "All Products" in selected_products_res:
                    selected_products_res = product_types_res[:-1]  # Exclude "All Products" from the list

                # Generate forecasts and resource requirements for all selected products
                all_resource_forecasts = []
                for product_type in selected_products_res:
                    forecast_df = generate_forecast(start_date_res, end_date_res, product_type, model)
                    if forecast_df is not None:
                        all_resource_forecasts.append(forecast_df[['Date', 'Resource Requirement']])
                    else:
                        st.error(f"Could not generate resource requirements for {product_type}.")

                if all_resource_forecasts:
                    combined_resource_df = pd.concat(all_resource_forecasts, ignore_index=True)
                    # Aggregate resource requirements
                    aggregated_resource = combined_resource_df.groupby('Date').sum().reset_index()

                    # Plot resource allocation
                    plot_resource_allocation(aggregated_resource)
                else:
                    st.error("No resource requirements to display.")
            else:
                st.error('Model not loaded. Please check model path or load model.')

else:
    st.sidebar.warning("Please log in to access the dashboard.")
