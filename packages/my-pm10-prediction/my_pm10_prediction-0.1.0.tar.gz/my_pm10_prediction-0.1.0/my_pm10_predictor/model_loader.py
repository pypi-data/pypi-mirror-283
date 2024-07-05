# my_pm10_predictor/model_loader.py

import pickle
from keras.models import load_model
from keras.losses import MeanSquaredError

def load_pickle_model(file_path):
    return pickle.load(open(file_path, "rb"))

def load_keras_model(file_path, custom_objects=None):
    if custom_objects is None:
        custom_objects = {'mse': MeanSquaredError()}
    return load_model(file_path, custom_objects=custom_objects)
