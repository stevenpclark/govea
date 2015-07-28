import numpy as np
from lasagne import layers
import theano
from nolearn.lasagne import NeuralNet
from extract_patterns import extract_patterns

try:
	from lasagne.layers.cuda_convnet import Conv2DCCLayer as Conv2DLayer
except ImportError:
	Conv2DLayer = layers.Conv2DLayer

net = NeuralNet(
		layers=[
			('input', layers.InputLayer),
			('conv1', layers.Conv2DLayer),
			('conv2', layers.Conv2DLayer),
			('conv3', layers.Conv2DLayer),
			('output', layers.Conv2DLayer),
			],
		input_shape=(None, 4, 19, 19),
		conv1_num_filters=64, conv1_filter_size=(5,5), conv1_border_mode='same',
		conv2_num_filters=64, conv2_filter_size=(3,3), conv2_border_mode='same',
		conv3_num_filters=64, conv3_filter_size=(3,3), conv3_border_mode='same', 
		output_num_filters=1, output_filter_size=(3,3), output_border_mode='same',

		update_learning_rate=0.1,
		update_momentum=0.0,

		regression=True,
		max_epochs=3,
		verbose=1,
		)

patterns = extract_patterns(max_num_patterns=1000000, exploit_symmetry=False)
X = [p.stimulus for p in patterns]
y = [p.response for p in patterns]

#print X
#print y

X = np.vstack(X).reshape(-1,4,19,19)
print X.shape
y = np.vstack(y).reshape(-1,1,19,19)
print y.shape

#increase recursion limit, in case pickling requires it
import sys
sys.setrecursionlimit(10000)
import cPickle as pickle

net.fit(X,y)

with open('net.pickle', 'wb') as f:
	pickle.dump(net, f, -1)


from matplotlib import pyplot
train_loss = np.array([i["train_loss"] for i in net.train_history_])
valid_loss = np.array([i["valid_loss"] for i in net.train_history_])
pyplot.plot(train_loss, linewidth=3, label="train")
pyplot.plot(valid_loss, linewidth=3, label="valid")
pyplot.grid()
pyplot.legend()
pyplot.xlabel("epoch")
pyplot.ylabel("loss")
pyplot.ylim(1e-3, 1e-2)
pyplot.yscale("log")
pyplot.show()
