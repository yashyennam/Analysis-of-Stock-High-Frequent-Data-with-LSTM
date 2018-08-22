from keras.models import Sequential, Model
from keras.layers.core import Dense, Flatten, Activation
from keras.layers import LSTM, Conv2D, BatchNormalization, Input
from model.utils import *


class Network:
    def __init__(self, conf):
        self._time_step = conf['time_step']
        self._feature_num = conf['feature_num']
        self._batch_size = conf['batch_size']
        self._epoch = conf['epoch']
        self._shape = (conf['time_step'], conf['feature_num'])
        self._model_file_path = conf['model_file_path']
        self._model = None

    def _init_model(self, *args, **kwargs):
        pass

    def save(self, file_name):
        self._model.save_weights(self._model_file_path + file_name)

    def load(self, file_name):
        self._model.load_weights(self._model_file_path + file_name)

    def train(self, train_x, train_y):
        self._model.fit(train_x, train_y, batch_size=self._batch_size, epochs=self._epoch, verbose=1)

    def predict(self, x):
        return self._model.predict(x, self._batch_size)

    def print_model_summary(self):
        print(self._model.summary())


class LSTM_MV(Network):
    def __init__(self, conf):
        Network.__init__(self, conf)
        self._LSTM_neuron_num = conf['LSTM_neuron_num']
        self._LSTM_layer_num = len(conf['LSTM_neuron_num'])
        self._model = self._init_model()

    def _init_model(self):
        init = Input(self._shape)
        x = init
        for i in range(self._LSTM_layer_num):
            neuron_num = self._LSTM_neuron_num[i]
            if i == 0:
                lstm = LSTM(units=neuron_num, input_shape=self._shape, return_sequences=True)
            else:
                lstm = LSTM(units=neuron_num, return_sequences=True)
            x = lstm(x)
        x = Flatten()(x)

        mean = Dense(units=3)(x)
        mean = BatchNormalization()(mean)
        mean = Activation('relu')(mean)
        mean = Dense(units=1)(mean)

        variance = Dense(units=3)(x)
        variance = BatchNormalization()(variance)
        variance = Activation('relu')(variance)
        variance = Dense(units=1)(variance)

        model = Model(inputs=init, outputs=[mean, variance])
        losses = ['mse', 'mse']

        model.compile(loss=losses, optimizer='RMSProp')
        return model


class LSTMs(Network):
    def __init__(self, conf):
        Network.__init__(self, conf)
        self._LSTM_neuron_num = conf['LSTM_neuron_num']
        self._LSTM_layer_num = len(conf['LSTM_neuron_num'])
        self._model = self._init_model()
        # self.print_model_summary()

    def _init_model(self):
        model = Sequential()
        x = Input(self._shape)
        for i in range(self._LSTM_layer_num):
            neuron_num = self._LSTM_neuron_num[i]
            if i == 0:
                lstm = LSTM(units=neuron_num, input_shape=self._shape, return_sequences=True)
            else:
                lstm = LSTM(units=neuron_num, return_sequences=True)
            x = lstm(x)
        x = Flatten()(x)
        model.add(Dense(2, activation='tanh'))
        model.compile(loss='mse', optimizer='RMSProp')
        return model


class CNN(Network):
    def __init__(self, conf):
        Network.__init__(self, conf)
        self._model = self._init_model()
        # self.print_model_summary()

    def _init_model(self):
        model = Sequential()

        input_shape = (self._time_step, int(self._feature_num / 2), 2)

        model.add(Conv2D(filters=10, input_shape=input_shape, kernel_size=(3, 3)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Flatten())

        model.add(Dense(units=6))
        model.add(Activation('relu'))

        model.add(Dense(units=3))
        model.add(Activation('softmax'))

        opt = 'adam'
        model.compile(optimizer=opt, loss=drop_zero, metrics=['acc'])

        return model