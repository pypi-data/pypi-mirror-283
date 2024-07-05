# my_pm10_predictor/model_loader.py

import os
import pickle
from keras.models import load_model
from keras.losses import MeanSquaredError

def get_model_path(filename):
    # Get the path to the models directory relative to this file
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, '../models', filename)

def load_pickle_model(filename):
    file_path = get_model_path(filename)
    return pickle.load(open(file_path, "rb"))

def load_keras_model(filename, custom_objects=None):
    if custom_objects is None:
        custom_objects = {'mse': MeanSquaredError()}
    file_path = get_model_path(filename)
    return load_model(file_path, custom_objects=custom_objects)
