from os import path
import utils
import NeuralNetworks

##############################################################################

FILE_R = "text2.txt"
FILE_W = "resultText2"
MODEL_FILENAME = "rnn_model.h5"
DATA_FILENAME = "data2"
COUNT_CLASS = 2
BATCH = 1
LENGTH_SEQ = 20
COUNT_PARAMETERS = 6

##############################################################################

all_x, all_y, all_z = utils.unpack_train_data(DATA_FILENAME)
x, z = utils.prepare_real_data(all_x, all_z, LENGTH_SEQ)

if path.exists(MODEL_FILENAME):
    nn = NeuralNetworks.load_model(MODEL_FILENAME)
    y = utils.to_binary(nn.predict(x, BATCH))
    utils.markup_text(FILE_W, FILE_R, y, z, LENGTH_SEQ)
else:
    print("not found model nn")
    exit()
