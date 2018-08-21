class Config(dict):
    def __init__(self):
        # name of features
        self['feature_name'] = ['buy1', 'bc1', 'sale1', 'sc1']

        # name of labels
        self['label_name'] = ['mid_price_delta']

        # number of features
        self['feature_num'] = len(self['feature_name'])

        # proportion of training set: training / (training + testing)
        self['training_set_proportion'] = 0.3

        # time step (each step takes 3 sec)
        self['time_step'] = 5

        # batch size (number of window)
        self['batch_size'] = 150

        # epoch
        self['epoch'] = 100

        # data file path
        self['data_file_path'] = 'data/SH600031_18.6.15-18.6.20.csv'

        # use previous model
        self['use_previous_model'] = False

        # model file path
        self['model_file_path'] = 'model/'

        # file name
        self['file_name'] = 'test.h5'

    def update(self, **kwargs):
        for key in kwargs:
            self[key] = kwargs[key]


class LSTM_Config(Config):
    def __init__(self):
        Config.__init__(self)
        # name of features
        self['feature_name'] = ['buy1', 'bc1',  'sale1', 'sc1']

        # name of labels
        self['label_name'] = ['mid_price_delta']

        # number of features
        self['feature_num'] = len(self['feature_name'])

        # time step (each step takes 3 sec)
        self['time_step'] = 5

        # batch size (number of window)
        self['batch_size'] = 150

        # number of neurons of each LSTM layer
        self['LSTM_neuron_num'] = [20, 10, 5]

        # epoch
        self['epoch'] = 100

        # file name
        self['file_name'] = 'lstm_test.h5'


class CNN_Config(Config):
    def __init__(self):
        Config.__init__(self)
        # name of features
        self['feature_name'] = ['buy5', 'bc5', 'buy4', 'bc4', 'buy3', 'bc3', 'buy2', 'bc2', 'buy1', 'bc1',
                               'sale1', 'sc1', 'sale2', 'sc2', 'sale3', 'sc3', 'sale4', 'sc4', 'sale5', 'sc5']

        # name of labels
        self['label_name'] = ['mid_price_delta']

        # number of features
        self['feature_num'] = len(self['feature_name'])

        # time step (each step takes 3 sec)
        self['time_step'] = 10

        # batch size (number of window)
        self['batch_size'] = 150

        # epoch
        self['epoch'] = 100

        # file name
        self['file_name'] = 'cnn_test.h5'