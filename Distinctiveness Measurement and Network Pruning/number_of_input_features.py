## import libraries
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.autograd import Variable
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
# fix randomness
np.random.seed(19680805)
## predefine functions for vector calculation
def unit_vector(vector):
	return vector.numpy() / np.linalg.norm(vector)
def angle_between(v1, v2):
	v1_u = unit_vector(v1)
	v2_u = unit_vector(v2)
	return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))
# define a two layer neural network structure
class TwoLayerNet(torch.nn.Module):

	def __init__(self, n_input, n_hidden, n_output):
		super(TwoLayerNet, self).__init__()
		# define linear hidden layer output
		self.hidden = torch.nn.Linear(n_input, n_hidden)
		# define linear output layer output
		self.out = torch.nn.Linear(n_hidden, n_output)

	def forward(self, x):
		"""
			In the forward function we define the process of performing
			forward pass, that is to accept a Variable of input
			data, x, and return a Variable of output data, y_pred.
		"""
		# get hidden layer input
		h_input = self.hidden(x)
		# define activation function for hidden layer
		h_output = torch.sigmoid(h_input)
		# get output layer output
		y_pred = self.out(h_output)

		return y_pred,h_output# the hidden unit activations are also output


## Input Data
data = pd.read_excel('Jae-First_Exp_data2.xls',sheet_name = 0)
data = data.iloc[2:,:]
data.drop(data.columns[26], axis=1, inplace=True)
data = data.sample(frac=1).reset_index(drop=True)
#if large screen, then 1. if small, then zero.
data.iloc[:,1] = (data.iloc[:,1] =='L').astype(int)
data.iloc[:,3:] = (data.iloc[:,3:]-np.min(data.iloc[:,3:]))/(np.max(data.iloc[:,3:])-np.min(data.iloc[:,3:]))
#split trainng and test set
msk = np.random.rand(len(data)) < 0.8
train_data = data[msk]
test_data = data[~msk]
# some empty array for storing training history
num_of_it = 3
training_acc_before = np.zeros(len(range(4,28)))
training_acc_after = np.zeros(len(range(4,28)))
test_acc_before = np.zeros(len(range(4,28)))
test_acc_after = np.zeros(len(range(4,28)))
num_of_operation = np.zeros(len(range(4,28)))
## Training and network Reduction
for iteration in range(num_of_it):
	print(iteration)
	ind = 0
	for i in range(4,28):
		n_input = i-3#define number of input features
		print(n_input)
		train_input = train_data.iloc[:,3:i]
		train_target = train_data.iloc[:,1]

		test_input = test_data.iloc[:, 3:i]
		test_target = test_data.iloc[:,1]
		#Create tensors for training
		X = Variable(torch.Tensor(train_input.astype(float).values))
		Y = Variable(torch.Tensor(train_target.values)).long()

		n_features = X.shape[1]

		## Config Network
		hidden_neurons = 20
		input_neurons = n_features
		output_neurons = 2
		learning_rate = 0.01
		num_epochs = 1000

		net = TwoLayerNet(input_neurons, hidden_neurons, output_neurons)
		loss_func = torch.nn.CrossEntropyLoss()
		optimiser = torch.optim.Adam(net.parameters(), lr=learning_rate)
		all_losses = []
		# Train
		for epoch in range(num_epochs):
			Y_pred,h_train = net(X)
			loss = loss_func(Y_pred, Y)
			all_losses.append(loss.item())
			net.zero_grad()
			loss.backward()
			optimiser.step()
		# compute training accuracy
		_, predicted = torch.max(Y_pred, 1)
		total = predicted.size(0)
		correct = predicted.data.numpy() == Y.data.numpy()
		training_acc_before[ind]+=(100 * sum(correct)/total)
		
		# Test NN
		X_test = Variable(torch.Tensor(test_input.astype(float).values))
		Y_test = torch.Tensor(test_target.values).long()
		Y_pred_test,_ = net(X_test)

		_, predicted_test = torch.max(Y_pred_test, 1)

		# calculate test accuracy
		total_test = predicted_test.size(0)
		correct_test = sum(predicted_test.data.numpy() == Y_test.data.numpy())
		test_acc_before[ind]+=(100 * correct_test / total_test)
		
		# Compute vector angle and pruning
		magnitude = np.zeros(hidden_neurons)
		h_train -= 0.5
		operation = 0
		for i in range(hidden_neurons):
			magnitude[i] = np.linalg.norm(h_train[:,i].detach())# calculate magnitude of each activation
			if magnitude[i] < 0.1:#locate deactivated neurons by setting up a threshold, 0.1
				net.out.weight[:,i] = 0# set the outgoing weight as 0 to remove unit
				operation += 1
			for j in range(i+1,hidden_neurons):
				angle = angle_between(h_train[:,i].detach(),h_train[:,j].detach())#compute vectore angle between units
				if ((angle <= 15) and (net.out.weight[0,j] != 0)):# locate similar units
					net.out.weight[:,i] += net.out.weight[:,j]
					net.out.weight[:,j] = 0
					operation += 1
				elif ((angle >= 165)and (net.out.weight[0,j] != 0)):# locate complement units
					net.out.weight[:,i] -= net.out.weight[:,j]
					net.out.weight[:,j] = 0
					operation += 1
		num_of_operation[ind]+=(operation/hidden_neurons*100)# measure the reduction rate
		# Train after Pruning
		Y_pred,_ = net(X)
		_, predicted = torch.max(Y_pred, 1)
		total = predicted.size(0)
		correct = predicted.data.numpy() == Y.data.numpy()
		training_acc_after[ind]+=(100 * sum(correct)/total)
		# Test after Pruning
		Y_pred_test,_ = net(X_test)
		_, predicted_test = torch.max(Y_pred_test, 1)
		# calculate accuracy
		total_test = predicted_test.size(0)
		correct_test = sum(predicted_test.data.numpy() == Y_test.data.numpy())
		test_acc_after[ind]+=(100 * correct_test / total_test)
		ind+=1
# calculate mean value of accuracies
training_acc_before /=num_of_it
training_acc_after /=num_of_it
test_acc_before /=num_of_it
test_acc_after /=num_of_it
num_of_operation /= num_of_it
print(training_acc_before)
print(training_acc_after)
print(test_acc_before)
print(test_acc_after)
print(num_of_operation)
## Plot Result
fig1 = plt.figure()
ax1 = fig1.add_subplot(121)
ax1.plot(range(1,n_input+1),training_acc_before,'ro-')
ax1.plot(range(1,n_input+1),training_acc_after,'bo-')
ax1.plot(range(1,n_input+1),test_acc_before,'ro-')
ax1.plot(range(1,n_input+1),test_acc_after,'bo-')
plt.legend(['Training Accuracy before Reduction','Training Accuracy after Reduction','Test Accuracy before Reduction','Test Accuracy after Reduction'],loc='best')
ax1.set_xlabel('Number of Input Features')
ax1.set_ylabel('Accuracy')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.axis([3,n_features,0,100])

ax2 = fig1.add_subplot(122)
ax2.plot(range(1,n_input+1),num_of_operation,'ro-')
ax2.plot(range(1,n_input+1),np.absolute(np.array(training_acc_before)-np.array(training_acc_after)),'bo-')
plt.legend(['Reductions rate','Difference between accuracies'],loc='best')
ax2.set_xlabel('Number of Input Features')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax2.axis([3,n_features,0,15])
plt.show()


		
	






