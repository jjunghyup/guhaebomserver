import pickle
import numpy as np
import xgboost as xgb
from app.service import job_category, ability


job_category_dictionary = {}
ability_dictionary = {}
for doc in job_category.find({}, {'_id': False}):
    job_category_dictionary[doc['id']] = doc['value']

for doc in ability.find({}, {'_id': False}):
    ability_dictionary[doc['value']] = int(doc['id'])

loaded_model = pickle.load(open("./app/util/save_data/job_category.pickle.dat", "rb"))


def one_hot_encoding(word_list):
    one_hot_vector = [0]*(len(ability_dictionary))
    for word in word_list:
        if word == '':
            continue
        index=ability_dictionary[word]
        one_hot_vector[index]=1
    return one_hot_vector


def predict_job_category(query_str, max=10):
    word_list = query_str.lstrip(' ').rstrip(' ').split(',')
    x = one_hot_encoding(word_list)
    xg_test = xgb.DMatrix(x)
    output = loaded_model.predict(xg_test)
    arr, ind = top_k(output, max)
    rank_array = []
    for k in ind[0]:
        rank_array.append(job_category_dictionary[str(k)])
    return rank_array


def top_k(input, k=1, sorted=True):
    """Top k max pooling
    Args:
        input(ndarray): convolutional feature in heigh x width x channel format
        k(int): if k==1, it is equal to normal max pooling
        sorted(bool): whether to return the array sorted by channel value
    Returns:
        ndarray: k x (height x width)
        ndarray: k
    """
    ind = np.argpartition(input, -k)[..., -k:]
    def get_entries(input, ind, sorted):
        if len(ind.shape) == 1:
            if sorted:
                ind = ind[np.argsort(-input[ind])]
            return input[ind], ind
        output, ind = zip(*[get_entries(inp, id, sorted) for inp, id in zip(input, ind)])
        return np.array(output), np.array(ind)
    return get_entries(input, ind, sorted)


if __name__ == '__main__':
    predict_job_category('주유,세차')




