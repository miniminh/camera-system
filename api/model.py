from keras.layers import Input, Dense, BatchNormalization, Conv2D, MaxPool2D, GlobalMaxPool2D, Dropout
from keras.optimizers import SGD
from keras.models import Model
from utils import FACE_W, FACE_H

ID_GENDER_MAP = {0: 'male', 1: 'female'}
GENDER_ID_MAP = dict((g, i) for i, g in ID_GENDER_MAP.items())
ID_RACE_MAP = {0: 'white', 1: 'black', 2: 'asian', 3: 'indian', 4: 'others'}
RACE_ID_MAP = dict((r, i) for i, r in ID_RACE_MAP.items())


def conv_block(inp, filters=32, bn=True, pool=True):
    _ = Conv2D(filters=filters, kernel_size=3, activation='relu')(inp)
    if bn:
        _ = BatchNormalization()(_)
    if pool:
        _ = MaxPool2D()(_)
    return _
def create_model():
    input_layer = Input(shape=(FACE_H, FACE_W, 3))
    _ = conv_block(input_layer, filters=32, bn=False, pool=False)
    _ = conv_block(_, filters=32*2)
    _ = Dropout(0.2)(_)
    _ = conv_block(_, filters=32*3)
    _ = conv_block(_, filters=32*4)
    _ = Dropout(0.2)(_)
    _ = conv_block(_, filters=32*5)
    _ = conv_block(_, filters=32*6)
    bottleneck = GlobalMaxPool2D()(_)

    # for age calculation
    _ = Dense(units=128, activation='relu')(bottleneck)
    age_output = Dense(units=1, activation='sigmoid', name='age_output')(_)

    # for race prediction
    _ = Dense(units=128, activation='relu')(bottleneck)
    race_output = Dense(units=len(RACE_ID_MAP), activation='softmax', name='race_output')(_)

    # for gender prediction
    _ = Dense(units=128, activation='relu')(bottleneck)
    gender_output = Dense(units=len(GENDER_ID_MAP), activation='softmax', name='gender_output')(_)

    model = Model(inputs=input_layer, outputs=[age_output, race_output, gender_output])
    model.compile(optimizer='rmsprop',
                loss={'age_output': 'mse', 'race_output': 'categorical_crossentropy', 'gender_output': 'categorical_crossentropy'},
                loss_weights={'age_output': 2., 'race_output': 1.5, 'gender_output': 1.},
                metrics={'age_output': 'mae', 'race_output': 'accuracy', 'gender_output': 'accuracy'})
    return model