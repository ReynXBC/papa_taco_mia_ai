import tensorflow as tf
import keras
from keras import layers, Sequential
from keras.layers import Dense, Input, Flatten, Conv2D, MaxPool2D
import os

x_train = []
 
model = Sequential([
          Input(shape=(32,32,3,)),
          Conv2D(filters=6, kernel_size=(5,5), padding="same", activation="relu"),
          MaxPool2D(pool_size=(2,2)),
          Conv2D(filters=16, kernel_size=(5,5), padding="same", activation="relu"),
          MaxPool2D(pool_size=(2, 2)),
          Conv2D(filters=120, kernel_size=(5,5), padding="same", activation="relu"),
          Flatten(),
          Dense(units=84, activation="relu"),
          Dense(units=10, activation="softmax"),
      ])
 
print (model.summary())