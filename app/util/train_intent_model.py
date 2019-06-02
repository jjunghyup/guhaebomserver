# coding: utf-8
import os
from app.util.model.char_cnn_model import CharCNN
from app.util.db import get_intent_test_data
from app.util.lexical_analyze import morphs


class TrainIntentModel:

    def __init__(self):
        self.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.model = None
        self.epoch = 100

    def _add_train_data_root(self, filename):
        return self.ROOT_DIR + "/util/save_data/" + filename

    def set_train_data(self):
        data = get_intent_test_data()

        inputs = []
        labels = []

        for encode_raw in data['encode']:
            encode_raw = morphs(encode_raw)
            print(encode_raw)
            inputs.append(encode_raw)

        for decode_raw in data['decode']:
            labels.append(decode_raw)

        self.x_train = inputs
        self.y_train = labels

    def train(self):
        self.model = CharCNN(self.x_train, self.y_train, epoch=self.epoch)
        self.model.fit()

    def save_model_as(self, weight_filename, params_filename, processor_filename):
        weight_filename = self._add_train_data_root(weight_filename)
        params_filename = self._add_train_data_root(params_filename)
        processor_filename = self._add_train_data_root(processor_filename)
        print(weight_filename, params_filename, processor_filename)
        self.model.save(weight_filename, params_filename, processor_filename)


if __name__ == '__main__':
    TM = TrainIntentModel()
    TM.set_train_data()
    TM.train()
    TM.save_model_as("intent.weight", "intent.params", 'intent.preprocessor')
