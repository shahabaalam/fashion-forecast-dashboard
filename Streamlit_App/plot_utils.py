# plot_utils.py

import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def plot_aggregated_forecast(aggregated_forecast):
    # Plot aggregated forecast
    fig = go.Figure()

    # Create a trace for the forecast line
    fig.add_trace(go.Scatter(
        x=aggregated_forecast['Date'],
        y=aggregated_forecast['Forecast'],
        mode='lines+markers',
        line=dict(width=2, color='white'),
        marker=dict(size=5, color='white'),
        name='Forecast',
    ))

    # Fill positive area (Profit) with green color
    fig.add_trace(go.Scatter(
        x=aggregated_forecast['Date'],
        y=aggregated_forecast['Forecast'].clip(lower=0),
        mode='lines',
        line=dict(width=0),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.5)',
        name='Profit',
        hoverinfo='skip',
        showlegend=True
    ))

    # Fill negative area (Loss) with red color
    fig.add_trace(go.Scatter(
        x=aggregated_forecast['Date'],
        y=aggregated_forecast['Forecast'].clip(upper=0),
        mode='lines',
        line=dict(width=0),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.5)',
        name='Loss',
        hoverinfo='skip',
        showlegend=True
    ))

    # Update layout
    fig.update_layout(
        title='Aggregated Sales Forecast for All Products',
        xaxis_title='Date',
        yaxis_title='Predicted Sales (Profit/Loss)',
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color="white"),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Help message
    st.markdown("""
        **How to Interpret the Plot:**

        - **Forecast Line**: The white line represents the aggregated predicted sales for all selected products over the chosen date range.
        - **Profit Area (Green)**: The green shaded area under the forecast line indicates periods where sales are positive (profit).
        - **Loss Area (Red)**: The red shaded area below the forecast line indicates periods where sales are negative (loss).
        - **Hover Information**: When you hover over the plot, you'll see the forecasted sales value for each date.
        - **Date Axis**: Represents the time period of the forecast.
        - **Sales Axis**: Shows the predicted sales values, with positive values indicating profit and negative values indicating loss.

        Use this plot to understand the overall profit and loss trend for all products combined. The color coding helps quickly identify profitable and non-profitable periods.
    """)

def plot_cumulative_sales_chart(aggregated_forecast):
    # Calculate cumulative sales
    aggregated_forecast = aggregated_forecast.sort_values('Date')
    aggregated_forecast['Cumulative Forecast'] = aggregated_forecast['Forecast'].cumsum()

    fig = go.Figure()

    # Create a trace for the cumulative forecast line
    fig.add_trace(go.Scatter(
        x=aggregated_forecast['Date'],
        y=aggregated_forecast['Cumulative Forecast'],
        mode='lines+markers',
        line=dict(width=2, color='white'),
        marker=dict(size=5, color='white'),
        name='Cumulative Sales',
    ))

    # Fill positive area (Cumulative Profit) with green color
    fig.add_trace(go.Scatter(
        x=aggregated_forecast['Date'],
        y=aggregated_forecast['Cumulative Forecast'].clip(lower=0),
        mode='lines',
        line=dict(width=0),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.5)',
        name='Cumulative Profit',
        hoverinfo='skip',
        showlegend=True
    ))

    # Fill negative area (Cumulative Loss) with red color
    fig.add_trace(go.Scatter(
        x=aggregated_forecast['Date'],
        y=aggregated_forecast['Cumulative Forecast'].clip(upper=0),
        mode='lines',
        line=dict(width=0),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.5)',
        name='Cumulative Loss',
        hoverinfo='skip',
        showlegend=True
    ))

    # Update layout
    fig.update_layout(
        title='Cumulative Sales Forecast',
        xaxis_title='Date',
        yaxis_title='Cumulative Predicted Sales (Profit/Loss)',
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color="white"),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Help message
    st.markdown("""
        **How to Interpret the Plot:**

        - **Cumulative Sales Line**: The white line represents the cumulative predicted sales over the selected date range.
        - **Cumulative Profit Area (Green)**: The green shaded area indicates periods where the cumulative sales are positive.
        - **Cumulative Loss Area (Red)**: The red shaded area indicates periods where the cumulative sales are negative.
        - **Hover Information**: When you hover over the plot, you'll see the cumulative predicted sales value for each date.
        - **Date Axis**: Represents the time period of the forecast.
        - **Cumulative Sales Axis**: Shows the cumulative predicted sales values, with positive values indicating profit and negative values indicating loss.

        Use this plot to understand the overall cumulative profit and loss trend over time. The color coding helps quickly identify periods of overall profitability and losses.
    """)

def plot_sales_heatmap(combined_forecast_df):
    # Pivot the data to create a matrix for the heatmap
    heatmap_data = combined_forecast_df.pivot(index='Product', columns='Date', values='Forecast')

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns.strftime('%b %Y'),
        y=heatmap_data.index,
        colorscale='Viridis',
        colorbar_title='Predicted Sales'
    ))

    # Update layout with black background
    fig.update_layout(
        title='Sales Forecast Heatmap',
        xaxis_title='Date',
        yaxis_title='Product',
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    # Help message
    st.markdown("""
        **How to Interpret the Heatmap:**

        - **Color Intensity:** Represents the magnitude of predicted sales.
        - **Darker Colors:** Indicate higher sales predictions.
        - **Lighter Colors:** Indicate lower sales predictions.
        - **Axes:** Products are listed on the y-axis and dates on the x-axis.

        The heatmap provides a visual overview of sales performance across different products and time periods, helping identify patterns and anomalies.
    """)

def plot_resource_allocation(resource_df):
    fig = go.Figure()

    # Add bars for resource requirements
    fig.add_trace(go.Bar(
        x=resource_df['Date'],
        y=resource_df['Resource Requirement'],
        marker_color='orange',
        name='Resource Requirement',
    ))

    # Update layout with black background
    fig.update_layout(
        title='Resource Allocation Forecast',
        xaxis_title='Date',
        yaxis_title='Resource Requirement (Staff Hours)',
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color="white"),
        hovermode='x',
        showlegend=False,
        xaxis_tickformat='%b %Y'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Help message
    st.markdown("""
        **How to Interpret the Resource Allocation Chart:**

        - **Bars:** Represent the forecasted resource requirements (e.g., staff hours needed) for each period.
        - **Bar Height:** Indicates the magnitude of resources required to meet the forecasted sales.
        - **Date Axis:** Shows the time period of the forecast.
        - **Resource Axis:** Displays the required resources (e.g., total staff hours).

        This chart helps you plan and allocate resources effectively to meet the predicted demand, optimizing operational efficiency.
    """)
