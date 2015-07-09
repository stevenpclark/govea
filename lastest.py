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
			('hidden4', layers.DenseLayer),
			('hidden5', layers.DenseLayer),
			('output', layers.DenseLayer),
			],
		input_shape=(None, 4, 19, 19),
		conv1_num_filters=32, conv1_filter_size=(3,3),
		conv2_num_filters=32, conv2_filter_size=(3,3),
		hidden4_num_units=200,
		hidden5_num_units=200,
		output_num_units=19*19, output_nonlinearity=None,

		update_learning_rate=0.01,
		update_momentum=0.9,

		regression=True,
		max_epochs=100,
		verbose=1,
		)

patterns = extract_patterns(max_num_patterns=50)
X = [p.stimulus for p in patterns]
y = [p.response for p in patterns]

#print X
#print y

X = np.vstack(X).reshape(-1,4,19,19)
print X.shape
y = np.vstack(y).reshape(-1,361)
print y.shape

net.fit(X,y)
