from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam


def build_model(states, actions):
    model = Sequential()
    model.add(Dense(256, input_shape=states, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Flatten())  
    model.add(Dense(actions, activation='linear'))
    return model


