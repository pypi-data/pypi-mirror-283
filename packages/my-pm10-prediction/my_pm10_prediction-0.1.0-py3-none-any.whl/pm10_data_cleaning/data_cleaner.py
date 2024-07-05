# pm10_data_cleaning/data_cleaner.py

import pandas as pd
import numpy as np
import warnings
from sklearn.impute import KNNImputer
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

class DataCleaner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def read_and_prepare(self):
        self.data = pd.read_csv(self.filepath, encoding='latin1')
        self.data["Datetime"] = pd.to_datetime(self.data["Date"] + " " + self.data["Time"], format='%d/%m/%Y %H:%M', errors='coerce')
        self.data = self.data.drop(columns=["Date", "Time"])
        self.data = self.data.drop_duplicates(subset=["Datetime"])
        return self

    def reindex_and_interpolate(self):
        full_datetime_range = pd.date_range(start=self.data["Datetime"].min(), end=self.data["Datetime"].max(), freq='H')
        self.data = self.data.set_index("Datetime").reindex(full_datetime_range)
        self.data.index.name = 'Datetime'
        self.data.interpolate(method='time', inplace=True)
        return self

    def handle_negative_values(self):
        self.data[self.data < 0] = np.nan
        return self

    def remove_outliers_iqr(self, k=1.5):
        numeric_df = self.data.select_dtypes(include=np.number)
        Q1 = numeric_df.quantile(0.25)
        Q3 = numeric_df.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        for col in numeric_df.columns:
            outlier_mask = (self.data[col] < lower_bound[col]) | (self.data[col] > upper_bound[col])
            self.data.loc[outlier_mask, col] = np.nan
        return self

    def impute_missing_values(self):
        datetime_series = self.data.index
        df_cleaned = self.data.reset_index().drop(columns=['Datetime'])
        imputer = KNNImputer(n_neighbors=2)
        df_imputed = pd.DataFrame(imputer.fit_transform(df_cleaned), columns=df_cleaned.columns)
        df_imputed['Datetime'] = datetime_series
        self.data = df_imputed.set_index('Datetime')
        return self

    def create_lag_features(self):
        self.data['PM10_Lag1'] = self.data['AC Penrose PM10 1h average [µg/m³]'].shift(1)
        self.data['PM10_Lag2'] = self.data['AC Penrose PM10 1h average [µg/m³]'].shift(2)
        self.data['PM10_Lag3'] = self.data['AC Penrose PM10 1h average [µg/m³]'].shift(3)
        return self

    def create_rolling_statistics(self):
        self.data['PM10_RollingMean3'] = self.data['AC Penrose PM10 1h average [µg/m³]'].rolling(window=3).mean()
        self.data['PM10_RollingStd3'] = self.data['AC Penrose PM10 1h average [µg/m³]'].rolling(window=3).std()
        return self

    def drop_na(self):
        self.data.dropna(inplace=True)
        return self

    def visualize_correlation(self):
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm')
        plt.show()

    def calculate_feature_importance(self):
        X = self.data.drop(columns=['AC Penrose PM10 1h average [µg/m³]'])
        y = self.data['AC Penrose PM10 1h average [µg/m³]']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        importances = model.feature_importances_
        feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
        return feature_importances.sort_values(by='Importance', ascending=False)

    def save_cleaned_data(self, output_filepath, top_features):
        columns_to_save = top_features + ['AC Penrose PM10 1h average [µg/m³]']
        self.data[columns_to_save].to_csv(output_filepath, index=True)
