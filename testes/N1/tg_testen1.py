# -*- coding: utf-8 -*-
"""tg_testeN1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RRZ3pA6phPxZqmYTW4XxkQtT4_7vTq2U
"""

from google.colab import drive

drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from keras import datasets, Model, layers
from keras.optimizers import Adam
from keras import Sequential
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.applications import VGG16, DenseNet121
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

model = Sequential([DenseNet121(input_shape=shape, 
                                weights='imagenet',
                                include_top=False),
                    layers.GlobalAveragePooling2D(),
                    layers.Dense(2, activation='sigmoid')])
model.summary()

# Compila o modelo definindo: otimizador, metrica e loss function
model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])


checkpoint = ModelCheckpoint('/content/drive/My Drive/Colab Notebooks/Testes do Projeto/Testes Nathan/Teste N1/model_healthy_N1.hdf5', 
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

modelo_salvo = load_model('/content/drive/My Drive/Colab Notebooks/Testes do Projeto/Testes Nathan/Teste N1/model_healthy_N1.hdf5')