
import tensorflow.keras as keras
import numpy  as np
import pandas as pd
import os
from sklearn import metrics
from keras.models import Sequential
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding,Dropout,Conv1D,ReLU,GlobalMaxPool1D,InputLayer

# 预处理类，词处理
class preprocesser(object):

    def read_txt(self, txt_path):

        with open(txt_path, "r", encoding='utf-8') as f:
            data = f.readlines()
        labels = []
        contents = []

        for line in data:
            # label, content = line.strip().split('\t')
            # labels.append(label)
            # contents.append(content)
            parts = line.strip().split('\t')
            if len(parts) == 2:  # Ensure both label and content are present
                label, content = parts
                labels.append(label)
                contents.append(content)

        return labels, contents


    def get_vocab_id(self):

        vocab_path = "vocab.txt"
        with open(vocab_path, "r", encoding="utf-8") as f:
            infile = f.readlines()
        vocabs = list([word.replace("\n", "") for word in infile])
        vocabs_dict = dict(zip(vocabs, range(len(vocabs))))
        return vocabs, vocabs_dict

    def get_category_id(self):
        """
        返回分类种类的索引
        :return: 返回分类种类的字典
        """
        categories = ["法学",  "农学", "药学",  "数学", "科技", "教育", "政治"]
        cates_dict = dict(zip(categories, range(len(categories))))
        return cates_dict

    def word2idx(self, txt_path, max_length):

        vocabs, vocabs_dict = self.get_vocab_id()
        # cates_dict:各分类的索引
        cates_dict = self.get_category_id()


        # 读取语料
        labels, contents = self.read_txt(txt_path)

        # labels_idx：用来存放语料中的分类
        labels_idx = []
        # contents_idx:用来存放语料中各样本的索引
        contents_idx = []

        # 遍历语料
        for idx in range(len(contents)):
            # tmp:存放当前语句index
            tmp = []
            # 将该idx(样本)的标签加入至labels_idx中
            labels_idx.append(cates_dict[labels[idx]])

            # contents[idx]:为该语料中的样本遍历项
            # 遍历contents中各词并将其转换为索引后加入contents_idx中
            for word in contents[idx]:
                if word in vocabs:
                    tmp.append(vocabs_dict[word])
                else:
                    # 第5000位设置为未知字符
                    tmp.append(5000)
            # 将该样本index后结果存入contents_idx作为结果等待传回
            contents_idx.append(tmp)

        # 将各样本长度pad至max_length
        x_pad = keras.preprocessing.sequence.pad_sequences(contents_idx, max_length)
        y_pad = keras.utils.to_categorical(labels_idx, num_classes=len(cates_dict))

        return x_pad, y_pad

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

        x_pad = keras.preprocessing.sequence.pad_sequences([result], max_length)
        return x_pad

# 参数设定
num_classes = 7
vocab_size = 7000
seq_length = 600

conv1_num_filters = 128
conv1_kernel_size = 1

conv2_num_filters = 64
conv2_kernel_size = 1

hidden_dim = 128
dropout_keep_prob = 0.5

batch_size = 64

trainingSet_path = "train.txt"
valSet_path = "val.txt"
model_save_path = "TextCNN_model.h5"
testingSet_path = "test.txt"

pre = preprocesser()
#创建模型
def TextCNN():

    model = Sequential()
    model.add(InputLayer((seq_length,)))
    model.add(Embedding(vocab_size+1, 256, input_length=seq_length))
    model.add(Conv1D(conv1_num_filters, conv1_kernel_size, padding="SAME"))
    model.add(Conv1D(conv2_num_filters, conv2_kernel_size, padding="SAME"))
    model.add(GlobalMaxPool1D())
    model.add(Dense(hidden_dim))
    model.add(Dropout(dropout_keep_prob))
    model.add(ReLU())
    model.add(Dense(num_classes, activation="softmax"))
    model.compile(loss="categorical_crossentropy",
                  optimizer="adam",
                  metrics=["acc"])
    return model

# 训练函数
def train(epochs):

    model = TextCNN()
    model.summary()

    x_train, y_train = pre.word2idx(trainingSet_path, max_length=seq_length)
    x_val, y_val = pre.word2idx(valSet_path, max_length=seq_length)

    model.fit(x_train, y_train,batch_size=batch_size,epochs=epochs,validation_data=(x_val, y_val))

    model.save(model_save_path, overwrite=True)

# 测试函数
def test():

    if os.path.exists(model_save_path):
        model = keras.models.load_model(model_save_path)
        print("-----model loaded-----")
        model.summary()

    x_test, y_test = pre.word2idx(testingSet_path, max_length=seq_length)
    print(x_test.shape)
    print(type(x_test))
    print(y_test.shape)
    pre_test = model.predict(x_test)
    print(metrics.classification_report(np.argmax(pre_test, axis=1), np.argmax(y_test, axis=1)))


if __name__ == '__main__':

    train(20)
    # test.train(1)
    model = keras.models.load_model(model_save_path)
    print("-----model loaded-----")
    model.summary()
    test = preprocesser()

    # 测试文本
    x_test = "基于高等数学在高职院校中的现状，明确高等数学在高职教育中的地位，制定科学、合理的课程标准，加强高等数学教学资源建设，改革高等数学课堂教学，制定科学的考核方式和评价方法"
    x_test = test.word2idx_for_sample(x_test, 600)

    categories = ["法学", "农学", "药学",  "数学", "科技", "教育", "政治"]

    pre_test = model.predict(x_test)

    index = int(np.argmax(pre_test, axis=1)[0])

    print('该为:', categories[index])
