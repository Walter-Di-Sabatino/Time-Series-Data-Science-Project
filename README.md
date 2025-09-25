
-----

# Time Series, Classification, and Clustering Project

This project analyzes two datasets from Kaggle using different data science approaches.

  * **Obesity Prediction Dataset** → Used for clustering and classification analysis.
  * **Airline Delay and Cancellation Data (2009–2018)** → Used for time series analysis and forecasting of average daily flight delays.

-----

## 🎯 Objectives

  * Explore the data using **ETL** and **visualization** techniques.
  * Apply **clustering** methods (`K-Means`, `DBSCAN`) to uncover hidden patterns.
  * Build and compare **classification** models (`Logistic Regression`, `Random Forest`, `Gradient Boosting`, `SVM`, `XGBoost`).
  * Model **time series** data with `SARIMAX` (both manual and auto-ARIMA) to forecast flight delays.

-----

## 📂 Repo Structure

  * `classification_and_clustering/` → Scripts and notebooks for the obesity dataset (preprocessing, clustering, classification, grid search).
  * `temporal_series/` → `SARIMAX` models for the flight data (stationarity analysis, forecasting).

-----

## 📊 Datasets

The following datasets are used:

1.  [Obesity Prediction Dataset](https://www.google.com/search?q=https://www.kaggle.com/datasets/mrsimple07/obesity-prediction-dataset-cleaned-and-processed)
2.  [Airline Delay and Cancellation Data (2009–2018)](https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018)

⚠️ **The datasets are not included in the repository due to their size. You must download them manually and save them into the `temporal_series/dataset` and `classification_and_clustering/dataset` folders.**

-----

## 🛠️ Requirements

To run the scripts and notebooks, you need to set up a Python environment and install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels xgboost pmdarima yellowbrick jupyter
```

-----

## 🚀 Usage

1.  Clone the repository.
2.  Download the datasets from the links above.
3.  Place the downloaded files into the corresponding `dataset` folders within `classification_and_clustering/` and `temporal_series/`.
4.  Explore the notebooks and scripts in the project folders to reproduce the analysis, visualizations, and forecasts.

-----

## 📈 Key Results

  * **Clustering**: The identified clusters do not perfectly align with the predefined obesity levels but reveal interesting and non-trivial patterns within the data.
  * **Classification**: The best performance was achieved with `Gradient Boosting` and `Random Forest`, reaching an accuracy between **0.88** and **0.89**.
  * **Time Series**: The manually configured `SARIMAX` model produced more realistic forecasts and better error metrics compared to the `auto-ARIMA` version.

-----

## 👥 Contributors

  * Walter Di Sabatino
  * Alessandra D'Anna
  * Agnese Bruglia