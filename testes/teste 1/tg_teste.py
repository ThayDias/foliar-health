# -*- coding: utf-8 -*-
"""tg_teste.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VE79kadB7EJJvSWNRrYjYeWUqBIFdaVu
"""

from google.colab import drive

drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

import time
import os
import datetime


from keras import datasets, Model
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras import Sequential
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.applications import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from keras import backend
import tensorflow as tf

from keras.preprocessing.image import load_img, img_to_array

# path = '/content/drive/My Drive/Colab Notebooks (1)/Datasets/train_healthy/'
path = '/content/drive/My Drive/Colab Notebooks/Datasets/train_healthy/'
BATCH_SIZE = 50

# setando a normalização e a % de dados para a validação
data_generator = ImageDataGenerator(rescale=1./255, validation_split=0.3)

train_generator = data_generator.flow_from_directory(path, shuffle=True, seed=13, class_mode='categorical', batch_size=BATCH_SIZE, subset="training")
validation_generator = data_generator.flow_from_directory(path, shuffle=True, seed=13, class_mode='categorical', batch_size=BATCH_SIZE, subset="validation")
shape = train_generator.image_shape

def build_model(shape=(256,256)):
  model = Sequential()

  # primeira camada adiciona o shape do input
  # também é possível alterar a inicializacao, bias, entre outros -- https://keras.io/layers/convolutional/#conv2d
  model.add(Conv2D(filters=64, kernel_size=2, activation='relu', input_shape=shape))
  #Tamanho do downsampling
  model.add(MaxPooling2D(pool_size=2))
  # Fracao das unidades que serao zeradas
  model.add(Dropout(0.3))

  # Segunda camada
  model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
  model.add(MaxPooling2D(pool_size=2))
  model.add(Dropout(0.3))

  # Da um reshape no output transformando em array
  model.add(Flatten())

  # Camada full-connected 
  model.add(Dense(256, activation='relu'))
  model.add(Dropout(0.5))

  #Camada de saida com o resultado das classes
  model.add(Dense(2, activation='sigmoid'))

  return model

model = build_model(shape)
model.summary()

# Compila o modelo definindo: otimizador, metrica e loss function
model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])


checkpoint = ModelCheckpoint('model_healthy.hdf5', 
                             monitor='val_loss', 
                             verbose=1, mode='min', 
                             save_best_only=True)

early_stop = EarlyStopping(monitor='val_loss',
                                   min_delta=0.001,
                                   patience=5,
                                   mode='min',
                                   verbose=1)

historico = model.fit_generator(generator=train_generator,
                    steps_per_epoch = train_generator.samples//BATCH_SIZE,
                    validation_data=validation_generator,
                    validation_steps=validation_generator.samples//BATCH_SIZE,
                    epochs= 50,
                    callbacks=[checkpoint, early_stop]
                    )

modelo_salvo = load_model('model_healthy.hdf5')

plt.plot(historico.history['accuracy'])
plt.plot(historico.history['val_accuracy'])

plt.title('Acurácia por épocas')

plt.xlabel('Épocas')
plt.ylabel('Acurácia')

plt.legend(['treino', 'validação'])

plt.plot(historico.history['loss'])
plt.plot(historico.history['val_loss'])

plt.title('Perdas por épocas')

plt.xlabel('Épocas')
plt.ylabel('Perda')

plt.legend(['treino', 'validação'])