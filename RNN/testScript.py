import utils
import numpy as np

##############################################################################

FILE_R = "text1.txt"
FILE_W = "resultText1_true"
DATA_FILENAME = "data1"
COUNT_CLASS = 2
LENGTH_SEQ = 20
##############################################################################

all_x, all_y, all_z = utils.unpack_train_data(DATA_FILENAME)
yy = []
for y in all_y:
      tmp = np.array([1 if i == y else 0 for i in range(COUNT_CLASS)])
      yy.append(tmp)
all_y = np.array(yy)
# x, y, z = utils.prepare_test_data(all_x, all_y, all_z, LENGTH_SEQ, COUNT_CLASS)
utils.markup_text(FILE_W, FILE_R, all_y, all_z, LENGTH_SEQ)
