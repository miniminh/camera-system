from keras.models import Model
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPool2D, GlobalMaxPool2D, Dropout
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
import numpy as np
import os

from model import create_model
from utils import SIMILAR_THRESHOLD, checkpoint_path, max_age, save_dir, distance
from preprocess import preprocess

model = create_model()

model.load_weights(checkpoint_path)

feature_extractor = Model(inputs = model.input, outputs = model.get_layer('global_max_pooling2d').output)

# feature_extractor.summary()

predictor = Model(inputs = model.get_layer('global_max_pooling2d').output, outputs = model.output)

# predictor.summary()

def predict(feature):
    print(feature.shape)
    age_pred, race_pred, gender_pred = predictor.predict(feature, verbose=False)
    
    gender_pred = gender_pred.argmax(axis=-1)
    age_pred = age_pred * max_age
    gender = 'm' if int(gender_pred) == 0 else 'f'
    return int(age_pred), gender

def get_feature(img):
    preprocessed_input = preprocess(img) # shape (198, 198, 3)
    preprocessed_input = preprocessed_input[np.newaxis, ...] # shape (1, 198, 198, 3)
    preprocessed_input = np.array(preprocessed_input) / 255.0
    # print(preprocessed_input.shape)
    feature = feature_extractor.predict(preprocessed_input, verbose=False)
    print(feature.shape)
    return feature

def already_in(feature):
    # for root, dirs, files in os.walk(save_dir):
    #     for file in files:
    #         f = os.path.join(root, file)
    #         temp = np.load(f)
    #         dis.append(distance(feature, temp))
    #         if (dis < SIMILAR_THRESHOLD):
    #             return True
    return False