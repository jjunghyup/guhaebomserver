# coding: utf-8
import os
from keras.preprocessing.sequence import pad_sequences
from app.util.model.char_cnn_model import load_model
from app.util.lexical_analyze import morphs


class IntentModel:
    def __init__(self):
        print("* Loading Intent Predict Model...")
        self.ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
        self.train_folder_path = self.ROOT_DIR + "/util/save_data/"
        self.weight = self.train_folder_path + 'intent.weight'
        self.params = self.train_folder_path +'intent.params'
        self.preprocessor = self.train_folder_path +'intent.preprocessor'
        self.intent_list = {'0': '안녕', '1': '알바구하기', '2': '신청하기'}
        self.load_model()
        self.intent_model._make_predict_function()
        self.x_predict = None
        self.tokenizer_filename = self.preprocessor
        self.train_config_filename = self.params

    def load_model(self):
        self.intent_model, self.tokenizer = load_model(self.weight, self.params, self.preprocessor)

    def inference_embed(self, data):
        encode_raw = morphs(data)
        self.x_predict = self.tokenizer.texts_to_sequences([encode_raw])

    def predict(self, data):
        self.inference_embed(data)
        self.x_predict = pad_sequences(self.x_predict, maxlen=self.intent_model.get_input_shape_at(0)[1])
        y = self.intent_model.predict(self.x_predict, 128, 2)
        # print(str(y))
        # print(str(y.argmax()))
        return self.intent_list.get(str(y.argmax()))


if __name__ == '__main__':
    model = IntentModel()
    print(model.predict("카페 일자리 구해줘"))
