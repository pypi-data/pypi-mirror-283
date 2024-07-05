# pm10_data_cleaning/run_data_cleaning.py

from pm10_data_cleaning.data_cleaner import DataCleaner

def main():
    # Initialize the DataCleaner with the file path
    cleaner = DataCleaner("data/PM10_hourly_input.csv")

    # Run the data cleaning process
    cleaner.read_and_prepare() \
        .reindex_and_interpolate() \
        .handle_negative_values() \
        .remove_outliers_iqr() \
        .impute_missing_values() \
        .create_lag_features() \
        .create_rolling_statistics() \
        .drop_na()

    # Visualize correlation
    cleaner.visualize_correlation()

    # Calculate feature importance
    feature_importances = cleaner.calculate_feature_importance()
    print(feature_importances)

    # Select top N features (e.g., top 5)
    top_features = feature_importances.head(5)['Feature'].tolist()

    # Save cleaned data
    cleaner.save_cleaned_data("data/PM10_hourly_output.csv", top_features)

if __name__ == "__main__":
    main()
