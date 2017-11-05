import keras
import utils


class RNN:
    def __init__(self, units, shape_in, count_class, optimizer="adam", loss="mean_squared_error"):
        print("Created networks...")
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.SimpleRNN(units=units, input_shape=shape_in, return_sequences=True))
        self.model.add(keras.layers.SimpleRNN(units=units, return_sequences=False))
        self.model.add(keras.layers.Dense(count_class, activation="softmax"))
        print("Initialize optimizer...")
        self.model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

    def fit(self, train_x, train_y, batch_size=32, num_epoch=100):
        self.model.fit(train_x, train_y, batch_size=batch_size, nb_epoch=num_epoch)

    def score(self, x, y, batch_size=32):
        test_res_y = self.predict(x, batch_size=batch_size)
        return utils.accuracy(test_res_y, y)

    def predict(self, x, batch_size=32):
        return utils.to_binary(self.model.predict(x, batch_size=batch_size))


def save_model(nn, filename="rnn_model.h5"):
    print("Save model...")
    nn.model.save(filename)


def load_model(filename="rnn_model.h5"):
    print(load_model)
    return keras.models.load_model(filename)


def plot_model(nn, filename="rnn_model.png"):
    print("Save plot...")
    keras.utils.plot_model(nn.model, filename, show_shapes=True)
