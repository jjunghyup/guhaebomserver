# coding: utf-8
import os
import anago
from app.util.lexical_analyze import morphs


class EntityModel:
    def __init__(self, weight_file_name, param_file_name, preprocessor_file_name):
        print("* Loading Result Entity Predict Model...")
        self.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
        self.model = None
        self._load_model(weight_file_name, param_file_name, preprocessor_file_name)

    def _add_train_data_root(self, filename):
        return self.ROOT_DIR + "/util/save_data/" + filename

    def _load_model(self, weight_file_name, param_file_name, preprocessor_file_name):
        weight_file = self._add_train_data_root(weight_file_name)
        params_file = self._add_train_data_root(param_file_name)
        preprocessor_file = self._add_train_data_root(preprocessor_file_name)
        self.model = anago.Sequence.load(weight_file, params_file, preprocessor_file)

    def predict(self, input_text):
        text = ""
        for morph in morphs(input_text):
            text = text + " " + morph
        return self.model.analyze(text)

#
if __name__ == '__main__':
    model = EntityModel('job_matching_entity.weight', 'job_matching_entity.params', 'job_matching_entity.preprocessor')
    print(model.predict("편의점 알바 구해줘"))
