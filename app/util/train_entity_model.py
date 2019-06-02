# coding: utf-8
import os
import anago
from app.util.db import get_entity_test_data


class TrainEntityModel:

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

    def set_train_data(self, intent):
        self.x_train, self.y_train = get_entity_test_data(intent)
        # self.x_test, self.y_test = get_entity_test_data(intent)

    def train(self):
        self.model = anago.Sequence()
        self.model.fit(self.x_train, self.y_train, self.x_test, self.y_test, epochs=self.epoch)

    def save_model_as(self, weight_filename, params_filename, processor_filename):
        weight_filename = self._add_train_data_root(weight_filename)
        params_filename = self._add_train_data_root(params_filename)
        processor_filename = self._add_train_data_root(processor_filename)

        self.model.save(weight_filename, params_filename, processor_filename)


if __name__ == '__main__':
    TM = TrainEntityModel()
    TM.set_train_data('1')
    TM.train()
    TM.save_model_as('job_matching_entity.weight', 'job_matching_entity.params', 'job_matching_entity.preprocessor')
    #
    # TM = TrainResultEntityModel()
    # TM.set_train_data('2')
    # TM.train()
    # TM.save_model_as('result_entity.weight', 'result_entity.params', 'result_entity.preprocessor')
    #
    # TM = TrainResultEntityModel()
    # TM.set_train_data('3')
    # TM.train()
    # TM.save_model_as('info_entity.weight', 'info_entity.params', 'info_entity.preprocessor')

    # --search keyword 제외--
    # TM = TrainResultEntityModel()
    # TM.set_train_data('4')
    # TM.train()
    # TM.save_model_as('job_list_entity.weight', 'job_list_entity.params', 'job_list_entity.preprocessor')
