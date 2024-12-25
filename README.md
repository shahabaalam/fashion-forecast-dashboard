# Fashion Forecast Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-1.24.1-blue?logo=streamlit) ![Python](https://img.shields.io/badge/Python-3.10-blue.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

## Table of Contents

- [📖 Introduction](#-introduction)
- [🎥 Demo](#-demo)
- [🚀 Features](#-features)
- [🛠️ Installation](#️-installation)
- [⚙️ Usage](#️-usage)
- [📂 Project Structure](#-project-structure)
- [🔧 Technologies Used](#-technologies-used)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📫 Contact](#-contact)

## 📖 Introduction

Welcome to the **Fashion Forecast Dashboard**! This project is an interactive Streamlit application designed to forecast sales in the fashion retail industry. By leveraging advanced machine learning models, dynamic data visualizations, and integrating the **ChatGPT API**, the dashboard empowers businesses to make data-driven decisions with ease and precision.

### **What Our App Can Do:**

- **Sales Forecasting:** Utilizes **Auto ARIMA** model to predict future sales trends, enabling proactive inventory and resource management.
  
- **Interactive Visualizations:** Utilize **Plotly** to create dynamic and responsive charts and graphs, making data exploration intuitive and insightful.
  
- **Resource Allocation Planning:** Analyze forecasted sales to optimize inventory levels and allocate resources effectively, reducing costs and improving operational efficiency.
  
- **AI-Powered Insights:** Engage with an **AI assistant powered by ChatGPT**, allowing users to query forecasts, receive intelligent data-driven responses, and gain deeper insights into sales patterns.
  
- **User-Friendly Interface:** Designed with **Streamlit** for an intuitive and responsive user experience, enabling users of all technical levels to navigate and utilize the dashboard effectively.

## 🎥 Demo

![Watch the Demo](https://img.youtube.com/vi/r2GyHu7FP3E/0.jpg)

**Watch the demo video here:** [https://youtu.be/r2GyHu7FP3E](https://youtu.be/r2GyHu7FP3E)

*Figure 1: Screenshot of the Fashion Forecast Dashboard Demo Video*

## 🚀 Features

- **Interactive Sales Forecasting:** Visualize future sales trends with dynamic charts and graphs.
- **Resource Allocation Planning:** Plan and allocate resources effectively based on predicted sales.
- **AI Assistant Integration:** Interact with an AI assistant for deeper insights and data analysis.
- **Comprehensive Data Analysis:** Analyze historical sales data using Jupyter notebooks.
- **Real-time Updates:** Streamlit's live reloading ensures that changes are reflected instantly.

## 🛠️ Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/shahabaalam/fashion-forecast-dashboard.git
cd fashion-forecast-dashboard/streamlit_app
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- **Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ Usage

Once the installation is complete, you can run the Streamlit application.

```bash
streamlit run main_app.py
```

This command will open the dashboard in your default web browser. If it doesn't open automatically, navigate to the URL provided in the terminal (typically `http://localhost:XXXX`).

## 📂 Project Structure

```
fashion-forecast-dashboard/
├── streamlit_App/
│   ├── assistant_utils.py    # Utilities for loading our chatbot
│   ├── main_app.py           # Main Streamlit application
│   ├── model_utils.py        # Utilities for loading and handling models
│   ├── plot_utils.py         # Utilities for generating plots
│   ├── autoarima_model.pkl   # Saved Forcasting model
│   ├── requirements.txt      # Python dependencies
├── Extended_Fashion_Retail_Sales.csv             # Sales dataset
├── sales_Forcasting_Using_AutoArima.ipynb        # Jupyter Notebook for data analysis
```

## 🔧 Technologies Used

- **[Streamlit](https://streamlit.io/):** For building the interactive web application.
- **[Python](https://www.python.org/):** The primary programming language.
- **[Pandas](https://pandas.pydata.org/):** Data manipulation and analysis.
- **[Plotly](https://plotly.com/python/):** Interactive plotting library.
- **[Joblib](https://joblib.readthedocs.io/en/latest/):** Model persistence and loading.
- **[pmdarima](https://pypi.org/project/pmdarima/):** Time series forecasting using AutoARIMA.
- **[Jupyter Notebook](https://jupyter.org/):** For data exploration and analysis.
- **[Git](https://git-scm.com/):** Version control system.
- **[GitHub](https://github.com/):** Hosting repository for version control and collaboration.

## 🤝 Contributing

Contributions are welcome! Whether it's reporting a bug, suggesting a feature, or submitting a pull request, your input is valuable.

### How to Contribute

1. **Fork the Repository**

   Click on the "Fork" button at the top-right corner of this page to create your own fork of the repository.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your_username/fashion-forecast-dashboard.git
   cd fashion-forecast-dashboard
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add feature: YourFeatureName"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Navigate to the original repository and click on "Compare & pull request" to submit your changes.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📫 Contact

For any inquiries or feedback, feel free to reach out:

- **Email:** [shahaba.alam@student.aiu.edu.my](mailto:shahaba.alam@student.aiu.edu.my)
- **LinkedIn:** [Shahaba Alam](https://www.linkedin.com/in/shahabaalam/)
