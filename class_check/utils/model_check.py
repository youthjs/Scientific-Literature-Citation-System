# -*- coding: utf-8 -*-
# FileName  : image_check.py
import tensorflow as tf
from .conf import model_path, vocab_path
import numpy as np

news_name = ["法学", "农学", "药学",  "数学", "科技", "教育", "政治"]
model = tf.keras.models.load_model(model_path)
# news_name = ["经济学类", "法学类", "计算机类", "农学类", "药学类", "管理学类", "数学类", "科技类", "教育类", "政治类", "体育类", "娱乐类", "游戏类", "财经类", "时尚类", "房产类", "家居类", "时政类"]
# model = tf.keras.models.load_model(model_path)


class preprocesser:
    def get_vocab_id(self):
        with open(vocab_path, "r", encoding="utf-8") as f:
            infile = f.readlines()
        vocabs = list([word.replace("\n", "") for word in infile])
        vocabs_dict = dict(zip(vocabs, range(len(vocabs))))
        return vocabs, vocabs_dict

    def word2idx_for_sample(self, sentence, max_length):
        # vocabs:分词词汇表
        # vocabs_dict:各分词的索引
        vocabs, vocabs_dict = self.get_vocab_id()
        result = []
        # 遍历语料
        for word in sentence:
            # tmp:存放当前语句index
            if word in vocabs:
                result.append(vocabs_dict[word])
            else:
                # 第5000位设置为未知字符，实际中为vocabs_dict[5000]，使得vocabs_dict长度变成len(vocabs_dict+1)
                result.append(5000)

        x_pad = tf.keras.preprocessing.sequence.pad_sequences([result], max_length)
        return x_pad


def check_handle(x_test):
    test = preprocesser()
    x_test = test.word2idx_for_sample(x_test, 600)
    pre_test = model.predict(x_test)
    index = int(np.argmax(pre_test, axis=1)[0])
    result = news_name[index]
    print('类别：{}'.format(result))
    return result
