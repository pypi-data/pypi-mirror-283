import matplotlib.pyplot as plt

def visualize_predictions(last_day_pm10, last_day_dates, pred_df):
    plt.figure(figsize=(14, 7))
    
    plt.plot(last_day_dates, last_day_pm10, label="Actual PM10 Last Day", color='black')
    plt.plot(pred_df.index, pred_df['xgb'], label="XGBoost Predictions", linestyle='--')
    plt.plot(pred_df.index, pred_df['rf'], label="Random Forest Predictions", linestyle='--')
    
    plt.xlabel("Datetime")
    plt.ylabel("PM10 Values [µg/m³]")
    plt.title("Predictions vs Actual PM10 Values")
    plt.legend()
    plt.show()
