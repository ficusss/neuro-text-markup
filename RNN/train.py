import utils
import NeuralNetworks


##############################################################################

DATA_FILENAME = "data1"
COUNT_CLASS = 2
BATCH_TRAIN_SIZE = 700
BATCH_TEST_SIZE = 300
LENGTH_SEQ = 20
COUNT_PARAMETERS = 6
COUNT_UNITS = 32
NUM_EPOCH = 80

##############################################################################

all_x, all_y, all_z = utils.unpack_train_data(DATA_FILENAME)
train_x, train_y, test_x, test_y = utils.prepare_data(all_x, all_y, LENGTH_SEQ, COUNT_CLASS,
                                                      BATCH_TRAIN_SIZE, BATCH_TEST_SIZE)

nn = NeuralNetworks.RNN(COUNT_UNITS, (LENGTH_SEQ, COUNT_PARAMETERS), COUNT_CLASS)
nn.fit(train_x, train_y, num_epoch=NUM_EPOCH)
print(nn.score(test_x, test_y))

print("Save...")
NeuralNetworks.save_model(nn)
NeuralNetworks.plot_model(nn)
