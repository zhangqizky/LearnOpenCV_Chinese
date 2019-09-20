from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten,Conv2D,MaxPooling2D,BatchNormalization
import os
import pickle
from numpy.random import seed
%matplotlib inline
from matplotlib import pyplot as plt
seed(7)

batch_size = 32
num_classes = 10
epochs = 12
data_augmentation = True
num_predictions = 20
save_dir = os.path.join(os.getcwd(), 'saved_models_noBn_100_s7')
model_name = 'keras_cifar10_trained_model.h5'

(x_train,y_train),(x_test,y_test) = cifar10.load_data()

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

y_train = keras.utils.to_categorical(y_train,num_classes)
y_test = keras.utils.to_categorical(y_test,num_classes)

def cifarmodel(input_shape = (32,32,3)):
  model = Sequential()
  model.add(Conv2D(32, (3, 3), padding='same',
               input_shape=input_shape))
  model.add(Activation('relu'))
  model.add(Conv2D(32, (3, 3)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))

  model.add(Conv2D(64, (3, 3), padding='same'))
  model.add(Activation('relu'))
  model.add(Conv2D(64, (3, 3)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))

  model.add(Flatten())
  model.add(Dense(512))
  model.add(Activation('relu'))
  model.add(Dropout(0.5))
  model.add(Dense(num_classes))
  model.add(Activation('softmax'))
  
def cifarmode_withbn(input_shape=(32,32,3)):
  model2 = Sequential()
  model2.add(Conv2D(32, (3, 3), padding='same',
                   input_shape=input_shape))
  model2.add(BatchNormalization())
  model2.add(Activation('relu'))
  model2.add(Conv2D(32, (3, 3)))
  model2.add(BatchNormalization())
  model2.add(Activation('relu'))
  model2.add(MaxPooling2D(pool_size=(2, 2)))
  #model.add(Dropout(0.25))

  model2.add(Conv2D(64, (3, 3), padding='same'))
  model2.add(BatchNormalization())
  model2.add(Activation('relu'))
  model2.add(Conv2D(64, (3, 3)))
  model2.add(BatchNormalization())
  model2.add(Activation('relu'))
  model2.add(MaxPooling2D(pool_size=(2, 2)))
  #model.add(Dropout(0.25))

  model2.add(Flatten())
  model2.add(Dense(512))
  model2.add(BatchNormalization())
  model2.add(Activation('relu'))
  #model.add(Dropout(0.5))
  model2.add(Dense(num_classes))
  model2.add(BatchNormalization())
  model2.add(Activation('softmax'))
def plot_training(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(acc))

    plt.plot(epochs, acc, 'r.')
    plt.plot(epochs, val_acc, 'r')
    plt.title('Training and validation accuracy')

    # plt.figure()
    # plt.plot(epochs, loss, 'r.')
    # plt.plot(epochs, val_loss, 'r-')
    # plt.title('Training and validation loss')
    plt.show()

    plt.savefig('acc_vs_epochs.png')
def main():
    model = cifarmodel(x_train[1:])
    opt = keras.optimizers.rmsprop(lr=0.0001,decay = 1e-6)
    model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    history = model.fit(x_train,y_train,
                    batch_size = batch_size,
                    epochs =epochs,
                    validation_data=(x_test,y_test),
                    shuffle=True)
    plot_training(history)
    mode.save("weights_cifar10_%s.h5"%(str(epochs)))
if __name__ == '__main__':
    main()
  
