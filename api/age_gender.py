from keras.models import Model
from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPool2D, GlobalMaxPool2D, Dropout
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import numpy as np
import os


from utils import SIMILAR_THRESHOLD, checkpoint_path, max_age, save_dir, distance
from preprocess import preprocess

model = tf.keras.models.load_model(checkpoint_path)

feature_extractor = Model(inputs = model.input, outputs = model.get_layer('global_max_pooling2d').output)

# feature_extractor.summary()

predictor = Model(inputs = model.get_layer('global_max_pooling2d').output, outputs = model.output)

# predictor.summary()

import cv2
import torch
import torchreid
from torchvision import transforms
import numpy as np

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load pre-trained model
model = torchreid.models.build_model(
    name='osnet_x1_0',
    num_classes=751,
    loss='softmax',
    pretrained=True
)

model = model.to(device)
model.eval()

# Load pre-trained weights
model.load_state_dict(torch.load('model.pth'))
model.eval()

transformer = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((256, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def predict(feature):
    # print(feature.shape)
    age_pred, race_pred, gender_pred = predictor.predict(feature, verbose=0)
    
    gender_pred = gender_pred.argmax(axis=-1)
    age_pred = age_pred * max_age
    gender = 'm' if int(gender_pred) == 0 else 'f'
    return int(age_pred), gender

def get_feature(img):
    img = transformer(img)
    img = torch.unsqueeze(img, 0)  # Add batch dimension
    img = img.to(device)

    # Forward pass
    features = model(img)
    return features

def get_id(feature):
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            print(file)
            f = os.path.join(root, file)
            temp = np.load(f)
            temp = torch.Tensor(temp)
            similarity = torch.nn.functional.cosine_similarity(temp, feature).item()
            print(similarity)
            if similarity == 1:
                temp = file.find('_')
                id = file[:temp]
                return id
    return None

def check_was_in(feature):
    for root, dirs, files in os.walk(save_dir):
        for file in files:
            f = os.path.join(root, file)
            temp = np.load(f)
            temp = torch.Tensor(temp)
            similarity = torch.nn.functional.cosine_similarity(temp, feature).item()
            if similarity > SIMILAR_THRESHOLD:
                temp = file.find('_')
                id = file[:temp]
                return id
    return None