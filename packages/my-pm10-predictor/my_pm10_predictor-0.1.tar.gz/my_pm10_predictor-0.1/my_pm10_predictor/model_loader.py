import pickle
from keras.models import load_model

def load_pickle_model(file_path):
    return pickle.load(open(file_path, "rb"))

def load_keras_model(file_path, custom_objects):
    return load_model(file_path, custom_objects=custom_objects)
