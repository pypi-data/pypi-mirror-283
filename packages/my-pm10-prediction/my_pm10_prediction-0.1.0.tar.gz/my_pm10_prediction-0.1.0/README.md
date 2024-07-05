# PM10_Prediction_Hourly
This package predicts PM10 values hourly using various machine learning models like XGBoost, Random Forest, SVM, GRU, and LSTM.


# Installation for Users

1. Download and save the "dist" folder

2. Recipients can install this package using 'pip':
pip install /path/to/your_package.whl

# Users can import the package into their Python enviornemnt:

3. Importing the package
from my_pm10_predictor import data_loader, model_loader, predictor, visualizer

4. Load data using your package:
df = data_loader.load_data('path/to/your/data.csv')

5. Load models using your package:
models = model_loader.load_models('path/to/your/models/')

6. Make predictions using your package:
predictions = predictor.predict_next_day(models, df)

7. Visualize predictions using your package:
visualizer.visualize_predictions(predictions)

