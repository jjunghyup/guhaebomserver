# coding: utf-8
import os
import pickle
import configparser
import json
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from keras.models import Model, model_from_json
from keras.layers import Input, Dense, Concatenate
from keras.layers import Convolution1D
from keras.layers import GlobalMaxPooling1D
from keras.layers import Embedding
from keras.layers import AlphaDropout
from keras.preprocessing.sequence import pad_sequences
from app.util.db import get_intent_test_data
from app.util.lexical_analyze import morphs


def load_model(weights_file, params_file, tokenizer_filename ):
    with open(tokenizer_filename, 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open(params_file) as f:
        model = model_from_json(f.read())
        model.load_weights(weights_file)

    return model, tokenizer

class CharCNN:
    def __init__(self, x_train, y_train, x_test=None, y_test=None, epoch=100):
        self.tokenizer = Tokenizer()
        self.filter_type = "multi"
        self.filter_sizes = [2,3,4,2,3,4,2,3,4]
        self.fully_connected_layers = [1024, 1024]
        self.dropout_p = 0.1
        self.optimizer = "adam"
        self.loss = "categorical_crossentropy"
        self.num_filters = len(self.filter_sizes)
        self.label_size = None
        self.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
        self.train_data_list = None
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.epoch = epoch
        self.inputs = None
        self.x = None
        self.model = None
        self.train_config_filename = 'intent.params'
        self.max_nb_words = None
        self.max_sequence_length = None

    def set_train_data(self):
        self.train_data_list = get_intent_test_data()

    def embed(self):
        for raw in self.x_train:
            self.tokenizer.fit_on_texts(raw)

        if self.x_test is not None:
            for raw in self.x_test:
                self.tokenizer.fit_on_texts(raw)

        self.x_train = self.tokenizer.texts_to_sequences(self.x_train)

        self.label_size = len(self.y_train)
        self.y_train = np_utils.to_categorical(self.y_train, self.label_size)

        if self.x_test is not None:
            self.x_test = self.tokenizer.texts_to_sequences(self.x_test)

        if self.y_test is not None:
            self.label_size = len(self.y_test)
            self.y_test = np_utils.to_categorical(self.y_test, self.label_size)

    def data_embedding(self):
        self.embed()
        self.max_nb_words = len(self.tokenizer.word_index) + 1
        self.max_sequence_length = max([len(seq) for seq in self.x_train])

        self.x_train = pad_sequences(self.x_train, maxlen=self.max_sequence_length)
        self.inputs = Input(shape=(self.max_sequence_length,), name='sent_input', dtype='int64')
        self.x = Embedding(self.max_nb_words, self.max_nb_words, input_length=self.max_sequence_length)(self.inputs)

    def model_design(self):
        convolution_output = []
        inindex = 0
        for filter_width in self.filter_sizes:
            conv = Convolution1D(filters=256,
                                 kernel_size=filter_width,
                                 activation='relu',
                                 name='Conv1D_{}_{}_{}'.format(256, filter_width, inindex))(self.x)
            pool = GlobalMaxPooling1D(name='MaxPoolingOverTime_{}_{}_{}'.format(256, filter_width, inindex))(conv)
            convolution_output.append(pool)
            inindex = inindex + 1

        self.x = Concatenate()(convolution_output)
        for fl in self.fully_connected_layers:
            self.x = Dense(fl, activation='relu', kernel_initializer='lecun_normal')(self.x)
            self.x = AlphaDropout(self.dropout_p)(self.x)

        predictions = Dense(self.label_size, activation='softmax')(self.x)
        self.model = Model(inputs=self.inputs, outputs=predictions)
        self.model.compile(optimizer=self.optimizer, loss=self.loss)
        self.model.summary()

    def fit(self):
        self.data_embedding()
        self.model_design()
        if self.x_test is None or self.x_train is None:
            self.model.fit(self.x_train, self.y_train,
                      validation_data=(self.x_train, self.y_train),
                      epochs=self.epoch,
                      batch_size=128,
                      verbose=2)
        else:
            self.model.fit(self.x_train, self.y_train,
                           validation_data=(self.x_test, self.y_test),
                           epochs=self.epoch,
                           batch_size=128,
                           verbose=2)

    def save(self, weight_filename, params_filename, processor_filename):
        self.save_tokenizer(processor_filename)
        self.save_weight_and_params(weight_filename, params_filename)

    def save_weight_and_params(self, weights_file, params_file):
        with open(params_file, 'w') as f:
            params = self.model.to_json()
            json.dump(json.loads(params), f, sort_keys=True, indent=4)
            self.model.save_weights(weights_file)

    def save_tokenizer(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
