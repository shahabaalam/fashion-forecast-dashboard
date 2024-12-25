# assistant_utils.py

import streamlit as st
from openai import OpenAI
import os
from datetime import datetime, timedelta
import pandas as pd

# Initialize the OpenAI client with your API key
api_key = os.getenv('OPENAI_API_KEY', 'YOUR_API_KEY')  # Replace with your actual API key
client = OpenAI(api_key=api_key)

def ai_assistant_interaction(model, generate_forecast_function):
    st.subheader("Chat with AI Assistant")

    st.write("""
        In this section, you can ask questions related to fashion retail data, resource allocation, or general sales trends.
        The AI Assistant is trained to provide informative responses based on predictive data for fashion retail.
        You can either select a predefined question from the dropdown menu or type your own question in the text box below.
        The assistant will respond to your query, and you can also include sales forecasts and resource allocation data in the response by selecting the option.
    """)

    # Initialize conversation history if it doesn't exist
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = [
            {"role": "system", "content": "You are a fashion sales assistant with access to predictive data and resource allocation forecasts."}
        ]

    # Add "Clear" button to reset the conversation
    if st.button("Clear"):
        st.session_state["conversation_history"] = [
            {"role": "system", "content": "You are a fashion sales assistant with access to predictive data and resource allocation forecasts."}
        ]
        st.session_state["user_input"] = ""
        st.session_state["selected_question"] = ""
        st.sidebar.success("Chat history cleared. You can start a new conversation.")

    # Question options and user input for the chat
    question_options = [
        "What is the projected growth in sales for women's dresses in the upcoming winter season?",
        "How did promotional events affect jeans sales in the last quarter?",
        "What are the predicted sales figures for athletic apparel for the next six months?",
        "How have import tariffs impacted footwear sales since last year?",
        "Can you provide a month-by-month breakdown of handbag sales for last year?",
        "What impact does the holiday season have on children’s clothing sales?"
    ]

    question = st.selectbox("Choose a predefined question", [""] + question_options, key="selected_question")
    user_input = st.text_area("...or type your own question here:", value=st.session_state.get('user_input', ""), height=150, key="user_input")

    include_prediction = st.checkbox("Include Forecast and Resource Allocation in Response")

    if st.button('Send'):
        query = question if question else user_input
        if query:
            with st.spinner('Please wait... Generating response.'):

                st.session_state["conversation_history"].append({"role": "user", "content": query})

                forecast_text = ""
                if include_prediction:
                    start_date = datetime.today()
                    end_date = start_date + timedelta(days=180)
                    # Generate forecast for "All Products"
                    forecast_df = generate_forecast_function(start_date, end_date, "All Products", model)
                    if forecast_df is not None:
                        # Calculate cumulative forecast
                        forecast_df = forecast_df.sort_values('Date')
                        forecast_df['Cumulative Forecast'] = forecast_df['Forecast'].cumsum()

                        # Prepare profit/loss information
                        profit_loss = forecast_df['Forecast'].apply(lambda x: 'Profit' if x >= 0 else 'Loss')
                        forecast_df['Profit/Loss'] = profit_loss

                        # Prepare forecast text including cumulative forecast, profit/loss, and resource requirement
                        forecast_text = "\nPredicted Sales and Resource Allocation:\n" + forecast_df[['Date', 'Forecast', 'Resource Requirement', 'Cumulative Forecast', 'Profit/Loss']].to_string(index=False)
                        # Include summary statistics
                        total_forecast = forecast_df['Forecast'].sum()
                        total_cumulative = forecast_df['Cumulative Forecast'].iloc[-1]
                        total_resource = forecast_df['Resource Requirement'].sum()
                        forecast_summary = f"\nTotal Forecasted Sales: {total_forecast:.2f}\nTotal Cumulative Sales: {total_cumulative:.2f}\nTotal Resource Requirement (Staff Hours): {total_resource:.2f}"
                        forecast_text += forecast_summary

                # Prepare the messages for the OpenAI API
                messages = st.session_state["conversation_history"].copy()
                if forecast_text:
                    # Include forecast and resource allocation data in the assistant's context
                    messages.append({"role": "system", "content": f"Here is the latest forecast and resource allocation data:\n{forecast_text}"})

                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                gpt_response = response.choices[0].message.content if response.choices else "No response received."

                st.session_state["conversation_history"].append({"role": "assistant", "content": gpt_response})

                st.text_area("AI Assistant Response:", value=gpt_response, height=150)
        else:
            st.warning("Please select a question or type your own to send.")