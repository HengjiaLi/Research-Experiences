'''
This algorithm fine-tunes a pre-trained Resnet50 model (inbuilt in Keras) on the CUB image dataset.
The output Resnet model can be used for the feature extraction application, as described in the paper:
Guo, Pei & Anderson, Connor & Pearson, Kolten & Farrell, Ryan. (2018). Neural Network Interpretation 
via Fine Grained Textual Summarization. 

Input: CUB image dataset; Keras pretrained Resnet model
Output: Fine-tuned Resnet model

'''
# important modules
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import os
import tensorflow as tf
import numpy as np
import csv
import time
from scipy import misc
import keras
from keras.utils import plot_model, to_categorical
from keras.models import Model
from keras.layers import Dense, Flatten, Dropout,GlobalAveragePooling2D,Conv2D,BatchNormalization
from keras.applications import resnet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam, RMSprop

from IPython.display import clear_output
print(keras.__version__)

# import utility functions
from utils import get_batch, save_csv, path_join, plot_images,example_errors, print_confusion_matrix, plot_example_errors, load_images
    
# Load Dataset    
dataset_dir = './splitted'
train_dir = './splitted/train_images'
test_dir = './splitted/test_images'
class_names = []
with open('classes.txt') as classes:
    spamreader = csv.reader(classes, delimiter=' ')
    for row in spamreader:
        class_names.append(row[1])

# Generate train data
x_train = []
y_train_label=[]

with open(os.path.join('splitted','images_train_dir.txt')) as train_dir, open('image_class_labels.txt') as labels:
	train_im = csv.reader(train_dir, delimiter=' ')
	label_list = list(csv.reader(labels,delimiter = ' '))
	for row in train_im:	
		nim = int(row[0])
		path = os.path.join('./splitted','train_images',row[1])
		img = misc.imread(path)
		x_train.append(img)
		y_train_label.append(to_categorical(int(label_list[nim-1][1])-1,num_classes=200))

print('Train data generation -- completed')		

# Generate test data
x_test = []
y_test_label=[]

with open(os.path.join('splitted','images_test_dir.txt')) as test_dir, open('image_class_labels.txt') as labels:
	test_im = csv.reader(test_dir, delimiter=' ')
	label_list = list(csv.reader(labels,delimiter = ' '))
	for row in test_im:	
		nim = int(row[0])
		#print(nim)
		path = os.path.join('./splitted','test_images',row[1])
		img = misc.imread(path)
		x_test.append(img)
		y_test_label.append(to_categorical(int(label_list[nim-1][1])-1,num_classes=200))

print('Test data generation -- completed')


x_train = np.array(x_train)
y_train_label=np.array(y_train_label)

x_test = np.array(x_test)
y_test_label=np.array(y_test_label)

# Load pre-trained (imagenet) model: Resnet50
model = keras.applications.ResNet50(include_top=True, weights='imagenet')
input_shape = model.layers[0].output_shape[1:3]

# define trainable layers
transfer_layer = model.get_layer('activation_49')
conv_model = Model(inputs=model.input,outputs=transfer_layer.output)
conv_model.trainable = True
for layer in conv_model.layers:
    # Boolean whether this layer is trainable.
    #trainable = ('5c' in layer.name or '5b' in layer.name or '5a' in layer.name or '4f' in layer.name or '4e' in layer.name)
    trainable = 1
    # Set the layer's bool.
    layer.trainable = trainable
    
# create the fully-connected layers for the CUB dataset
x = conv_model.output
pool1 = GlobalAveragePooling2D()(x)
dense2 = Dense(200,activation='softmax',name='Bird_type')(pool1)
# define the model for training
new_model = Model(inputs = conv_model.input,output = dense2)
# plot the structure of the network
plot_model(new_model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
with open('structure.txt','w') as fh:
	# Pass the file handle in as a lambda function to make it callable
	new_model.summary(print_fn=lambda x: fh.write(x + '\n'))

loss = ['categorical_crossentropy']
new_model.compile(optimizer=Adam(lr=1e-4), loss=loss, metrics=["accuracy"])
# train the network 
history = new_model.fit(x = x_train, y = y_train_label,
          epochs=7, batch_size = 12,validation_data = [x_test,y_test_label])
print(history.history.keys())
# summarize history for accuracy
fig1 = plt.figure()
ax1 = fig1.add_subplot(121)
ax1.plot(history.history['acc'])
ax1.plot(history.history['val_acc'])
ax1.set_title('model accuracy')
ax1.set_ylabel('accuracy')
ax1.set_xlabel('epoch')
plt.legend(['training accuracy', 'testing accuracy'], loc='best')
# summarize history for loss
ax2 = fig1.add_subplot(122)
ax2.plot(history.history['loss'])
ax2.plot(history.history['val_loss'])
ax2.set_title('model loss')
ax2.set_ylabel('loss')
ax2.set_xlabel('epoch')
plt.legend(['training loss', 'testing loss'], loc='best')
plt.show()
fig1.savefig('accuracy_transfer_learning.png')

new_model.compile(optimizer=Adam(lr=1e-5), loss=loss, metrics=["accuracy"])
# train network again with smaller a learning rate
history = new_model.fit(x = x_train, y = y_train_label,
          epochs=5, batch_size = 12,validation_data = [x_test,y_test_label])
# summarize history for accuracy
fig2 = plt.figure()
ax1 = fig2.add_subplot(121)
ax1.plot(history.history['acc'])
ax1.plot(history.history['val_acc'])
ax1.set_title('model accuracy')
ax1.set_ylabel('accuracy')
ax1.set_xlabel('epoch')
plt.legend(['training accuracy', 'testing accuracy'], loc='best')
# summarize history for loss
ax2 = fig2.add_subplot(122)
ax2.plot(history.history['loss'])
ax2.plot(history.history['val_loss'])
ax2.set_title('model loss')
ax2.set_ylabel('loss')
ax2.set_xlabel('epoch')
plt.legend(['training loss', 'testing loss'], loc='best')
plt.show()
fig2.savefig('accuracy_fine_tuning.png')

new_model.save('Final network.h5')
result = new_model.evaluate(x = x_test, y=y_test_label)
print("Test-set classification accuracy: {0:.2%}".format(result[1]))

