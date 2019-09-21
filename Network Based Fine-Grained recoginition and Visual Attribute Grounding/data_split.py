## split train and test image ides
import numpy as np
from sklearn.model_selection import train_test_split

train_ids = []
test_ids = []

with open('train_test_split.txt') as train_test_data:
	# for im_id, line in enumerate(train_test_data):
		# check = int(line.strip().split()[1])
		# if check == 1:
			# train_ids.append(im_id+1)
			
		# else:
			# test_ids.append(im_id+1)


	# Generate our own train and test list
	file_length = 0
	file_length = sum(1 for line in train_test_data)
	y = range(1,file_length)
	train_ids, test_ids = train_test_split(y, test_size = 0.1, random_state = 42)
	train_ids = sorted(train_ids)
	test_ids = sorted(test_ids)
# print(train_ids)		
# print(np.shape(train_ids))	
# print(np.shape(test_ids))	
## split train and test image directories
with open('images.txt') as im_directory, open('splitted/images_test_dir.txt','w') as test_dir, open('splitted/images_train_dir.txt','w') as train_dir:
	for im_id, line in enumerate(im_directory):
		if im_id+1 in train_ids:
			train_dir.write(line)
		else:
			test_dir.write(line)

## split bounding box into train and test files
with open('bounding_boxes.txt') as im_box, open('splitted/images_test_box.txt','w') as testbox_dir, open('splitted/images_train_box.txt','w') as trainbox_dir:
	for im_id,line in enumerate(im_box):
		if im_id+1 in train_ids:
			trainbox_dir.write(line)
		else:
			testbox_dir.write(line)

## split pre-classified labels
with open('image_class_labels.txt') as im_label, open('splitted/images_test_label.txt','w') as testlabel, open('splitted/images_train_label.txt','w') as trainlabel:
	for im_id,line in enumerate(im_label):
		if im_id+1 in train_ids:
			trainlabel.write(line)
		else:
			testlabel.write(line)
			



