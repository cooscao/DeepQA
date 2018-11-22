import jieba
import pickle
import numpy as np
import torch
import sys


net_path = '/root/workspace/DeepQA1/app/net'
pkl_path = net_path + '/word2id.obj'
model_path = net_path + '/model.pt'
fake_data = [[45, 885, 45, 8532, 486, 37],
             [31507, 8532, 486, 543, 22269, 1335, 486, 66677,
              19500, 1138,4,202,486,20012,19500,50113,62717,19500,
              12816,69321,2351,19500,330,4677,19500,1335,488,548,
              59060,19500,8702,1087,486,277,2425,19500,4741,486,
              19174,19500,395,3864,555,19174,486,10591,13154,46498,
              373,2257,19500,1064,32216,47393,19500,145,18,1134,
              19500,43330,212,1046,19500,13768,68556,3124],
             [[45], [53959], [74515]],
             250001]
sys.path.append(net_path)


with open(pkl_path, 'rb') as f:
    word2id = pickle.load(f)


def seg_line(line):
    return list(jieba.cut(line))


def map_word_to_id(word):
    output = []
    if word in word2id:
        output.append(word2id[word])
    else:
        chars = list(word)
        for char in chars:
            if char in word2id:
                output.append(word2id[char])
            else:
                output.append(1)
    return output


def map_sent_to_id(sent):
    output = []
    for word in sent:
        output.extend(map_word_to_id(word))
    return output


def padding(sequence, pads=0, max_len=None, dtype='int32', return_matrix_for_size=False):
    # we should judge the rank
    if True or isinstance(sequence[0], list):
        v_length = [len(x) for x in sequence]  # every sequence length
        seq_max_len = max(v_length)
        if (max_len is None) or (max_len > seq_max_len):
            max_len = seq_max_len
        v_length = list(map(lambda z: z if z <= max_len else max_len, v_length))
        x = (np.ones((len(sequence), max_len)) * pads).astype(dtype)
        for idx, s in enumerate(sequence):
            trunc = s[:max_len]
            x[idx, :len(trunc)] = trunc
        if return_matrix_for_size:
            v_matrix = np.asanyarray([map(lambda item: 1 if item < line else 0, range(max_len)) for line in v_length],
                                     dtype=dtype)
            return x, v_matrix
        return x, np.asarray(v_length, dtype='int32')
    else:
        seq_len = len(sequence)
        if max_len is None:
            max_len = seq_len
        v_vector = sequence + [0] * (max_len - seq_len)
        padded_vector = np.asarray(v_vector, dtype=dtype)
        v_index = [1] * seq_len + [0] * (max_len - seq_len)
        padded_index = np.asanyarray(v_index, dtype=dtype)
        return padded_vector, padded_index


def pad_answer(batch):
    output = []
    length_info = [len(x[0]) for x in batch]
    max_length = max(length_info)
    for one in batch:
        output.append([x + [0] * (max_length - len(x)) for x in one])
    return output



def predict(question, model_path=model_path):
    data = [seg_line(question.q_text), seg_line(question.p_text),
       question.alternatives.split('|'), question.id]
    question = map_sent_to_id(data[0])
    doc = map_sent_to_id(data[1])
    candidates = [map_word_to_id(x) for x in data[2]]
    length = [len(x) for x in candidates]
    max_length = max(length)
    if max_length > 1:
        pad_len = [max_length - x for x in length]
        candidates = [x[0] + [0] * x[1] for x in zip(candidates, pad_len)]
    one = [question, doc, candidates, data[-1]]
    # print(one)
    query, _ = padding([one[0], fake_data[0]], max_len=18)
    passage, _ = padding([one[1], fake_data[1]], max_len=350)
    answer = pad_answer([one[2], fake_data[2]])
    with open(model_path, 'rb') as f:
        net = torch.load(f, map_location='cpu')
   #  model.eval()
    query, passage, answer = torch.LongTensor(query), torch.LongTensor(passage), torch.LongTensor(answer)
    output = net([query, passage, answer, False])
    index = output[0].item()
    return data[2][int(index)]

