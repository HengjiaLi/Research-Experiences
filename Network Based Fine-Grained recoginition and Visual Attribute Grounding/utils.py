from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import csv
import os
#import PTL
from scipy import misc

from  bird_dataset_generator import BirdClassificationGenerator


#pre-processing stuff
def gray2rgb(img, path):
	if len(img.shape) < 3:
		img = np.stack((img,)*3,axis=2)
	return img

def random_flip_lr(img):
	rand_num = np.random.rand(1)
	if rand_num > 0.5:
		img = np.flip(img, 1)
	return img

def random_brightness(img):
	rand_num = np.random.randint(3, high=10, size=1)/10.0
	img = img * rand_num;
	img = img.astype(dtype=np.uint8)
	return img


def normalize_input(img, height):
	img = img.astype(dtype=np.float32)
	img[:,:,0] -= 103.939
	img[:,:,1] -= 116.779
	img[:,:,2] -= 123.68
	#img = np.divide(img, 255.0)
	return img 

def add_random_noise(img):
	return img + np.random.normal(0, 50.0, (img.shape))

def preprocess_image(img, height, width, set_type):
	img = misc.imresize(np.asarray(img), (height, width))
	#if set_type == 'train':   
		#img = random_flip_lr(img)
		#img = random_brightness(img)
	#img = normalize_input(img, height)
	#img = add_random_noise(img)
	return img



# return a batch of input(images, labels) to feed into plavceholders
def get_batch(generator_type, set_type, height, width):
	imgs = []
	if set_type == 'train' or set_type == 'val':
		for paths, bbs, labels, classes in generator_type:
			for i  in range(len(paths)):
				
				img = gray2rgb(misc.imread(paths[i]), paths[i])
				img = img[bbs[i][1]:bbs[i][1]+bbs[i][3], bbs[i][0]:bbs[i][0]+bbs[i][2],:]
				img = preprocess_image(img, height, width, set_type)
				imgs.append(img)
			imgs = np.asarray(imgs)
			break
		return imgs, labels,classes
	else:
		for paths, bbs in generator_type:
			for i  in range(len(paths)):
				paths ='./splitted\\images\\001.Black_footed_Albatross/Black_Footed_Albatross_0046_18.jpg'
				img = gray2rgb(misc.imread(paths[i]), paths[i])
				img = img[bbs[i][1]:bbs[i][1]+bbs[i][3], bbs[i][0]:bbs[i][0]+bbs[i][2],:]
				imgs.append(preprocess_image(img, height, width, set_type))
			imgs = np.asarray(imgs)
			break
		return imgs, None



#store in required csv format
def save_csv(model_pred, obj):
	with open('submission.csv',"w") as f:
		writer = csv.writer(f, delimiter=',',  quotechar='"', quoting=csv.QUOTE_ALL)
		row = ['Id', 'Category']
		writer.writerow(row)
		for i in range(len(obj.test_list)):
			row = []
			row.append(obj.test_list[i]) 
			row.append(model_pred[i]+1)
			writer.writerow(row)
			
def path_join(dirname,filenames):
	return [os.path.join(dirname, filename) for filename in filenames]

def plot_images(images, class_names, cls_true, cls_pred=None, smooth=True):

	assert len(images) == len(cls_true)

	# Create figure with sub-plots.
	fig, axes = plt.subplots(3, 3)

	# Adjust vertical spacing.
	if cls_pred is None:
		hspace = 0.3
	else:
		hspace = 0.6
	fig.subplots_adjust(hspace=hspace, wspace=0.3)

	# Interpolation type.
	if smooth:
		interpolation = 'spline16'
	else:
		interpolation = 'nearest'

	for i, ax in enumerate(axes.flat):
		# There may be less than 9 images, ensure it doesn't crash.
		if i < len(images):
			# Plot image.
			ax.imshow(images[i],
					  interpolation=interpolation)

			# Name of the true class.
			cls_true_name = class_names[cls_true[i]+1]

			# Show true and predicted classes.
			if cls_pred is None:
				xlabel = "True: {0}".format(cls_true_name)
			else:
				# Name of the predicted class.
				cls_pred_name = class_names[cls_pred[i]]

				xlabel = "True: {0}\nPred: {1}".format(cls_true_name, cls_pred_name)

			# Show the classes as the label on the x-axis.
			ax.set_xlabel(xlabel)
		
		# Remove ticks from the plot.
		ax.set_xticks([])
		ax.set_yticks([])
	
	# Ensure the plot is shown correctly with multiple plots
	# in a single Notebook cell.
	plt.show()
	
# Import a function from sklearn to calculate the confusion-matrix.
from sklearn.metrics import confusion_matrix

def print_confusion_matrix(cls_pred):
	# cls_pred is an array of the predicted class-number for
	# all images in the test-set.

	# Get the confusion matrix using sklearn.
	cm = confusion_matrix(y_true=cls_test,	# True class for test-set.
						  y_pred=cls_pred)	# Predicted class.

	print("Confusion matrix:")
	
	# Print the confusion matrix as text.
	print(cm)
	
	# Print the class-names for easy reference.
	for i, class_name in enumerate(class_names):
		print("({0}) {1}".format(i, class_name))	

def plot_example_errors(cls_pred):
	# cls_pred is an array of the predicted class-number for
	# all images in the test-set.

	# Boolean array whether the predicted class is incorrect.
	incorrect = (cls_pred != cls_test)

	# Get the file-paths for images that were incorrectly classified.
	image_paths = np.array(image_paths_test)[incorrect]

	# Load the first 9 images.
	images = load_images(image_paths=image_paths[0:9])
	
	# Get the predicted classes for those images.
	cls_pred = cls_pred[incorrect]

	# Get the true classes for those images.
	cls_true = cls_test[incorrect]
	
	# Plot the 9 images we have loaded and their corresponding classes.
	# We have only loaded 9 images so there is no need to slice those again.
	plot_images(images=images,
				cls_true=cls_true[0:9],
				cls_pred=cls_pred[0:9])		

def example_errors():
	# The Keras data-generator for the test-set must be reset
	# before processing. This is because the generator will loop
	# infinitely and keep an internal index into the dataset.
	# So it might start in the middle of the test-set if we do
	# not reset it first. This makes it impossible to match the
	# predicted classes with the input images.
	# If we reset the generator, then it always starts at the
	# beginning so we know exactly which input-images were used.
	generator_test.reset()
	
	# Predict the classes for all images in the test-set.
	y_pred = new_model.predict_generator(generator_test,
										 steps=steps_test)

	# Convert the predicted classes from arrays to integers.
	cls_pred = np.argmax(y_pred,axis=1)

	# Plot examples of mis-classified images.
	plot_example_errors(cls_pred)
	
	# Print the confusion matrix.
	print_confusion_matrix(cls_pred)	

def plot_training_history(history):
	# Get the classification accuracy and loss-value
	# for the training-set.
	class_acc = history.history['Bird_type_acc']
	class_losses = history.history['Bird_type_loss']
	pdf_losses = history.history['Attribute/Filter_PDF_loss']
	pdf_acc = history.history['Attribute/Filter_PDF_acc']
	
	# Get it for the validation-set (we only use the test-set).
	val_class_acc = history.history['val_Bird_type_acc']
	val_class_losses = history.history['val_Bird_type_loss']
	val_pdf_losses = history.history['val_Attribute/Filter_PDF_loss']
	val_pdf_acc = history.history['val_Attribute/Filter_PDF_acc']	
	
	f, (ax1, ax2) = plt.subplots(1, 2, sharex=True,figsize=(20, 10))
	# Plot the accuracy and loss-values for the training-set.
	ax1.plot(class_acc, linestyle='-', color='b', label='Training Bird_type_Acc.')
	ax1.plot(class_losses, 'o', color='b', label='Training Bird_type_Loss')
	ax1.plot(pdf_acc, '--', color='r', label='Training pdf_Acc')
	ax1.plot(pdf_losses, 'o', color='r', label='Training pdf_Loss')
	ax1.legend()
	# Plot it for the test-set.
	ax2.plot(val_class_acc, linestyle='-', color='b', label='Testing Bird_type_Acc.')
	ax2.plot(val_class_losses, 'o', color='b', label='Testing Bird_type_Loss')
	ax2.plot(val_pdf_acc, '--', color='r', label='Testing pdf_Acc')
	ax2.plot(val_pdf_losses, 'o', color='r', label='Testing pdf_Loss')
	ax2.legend()
	# Plot title and legend.
	

	# Ensure the plot shows correctly.
	plt.show()
	
def load_images(image_paths):
	# Load the images from disk.
	images = [plt.imread(path) for path in image_paths]

	# Convert to a numpy array and return it.
	return np.asarray(images)	