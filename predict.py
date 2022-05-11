from collections import Counter
from math import sqrt
import gensim
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.layers.embeddings import Embedding
from keras.models import Model
import gensim
import os
import jieba
import keras

def predict_main():
    '''
    导入需要预测的文件
    '''
    file = open("data/test_goods.txt",encoding='utf-8') 
    sentences=[]
    for line in file:
        temp=line.replace('\n','')
        sentences.append(jieba.lcut(temp))
    reviews = sentences


    if os.path.exists("model/word2VecModel"):
        print("直接调用模型")
        model = gensim.models.Word2Vec.load('model/word2VecModel')


    # 停用词的字典变量
    stopWordDict = {}

    def readStopWord(stopWordPath):
        """
        读取停用词
        """       
        with open(stopWordPath, "r",encoding='utf-8') as f:
            stopWords = f.read()
            stopWordList = stopWords.splitlines()
            
            # 将停用词用列表的形式生成，之后查找停用词时会比较快
            stopWordDict = dict(zip(stopWordList, list(range(len(stopWordList)))))
            return (stopWordDict)
    stopWordDict=readStopWord(stopWordPath="data/stopword.txt")


    wordToIndex = {}


    #生成嵌入词向量的维度
    embeddingSize = 10



    def getWordEmbedding(words):
        """
        按照我们的数据集中的单词取出预训练好的word2vec中的词向量
        """
        #中文
        model = gensim.models.Word2Vec.load('model/word2VecModel')

        vocab = []
        wordEmbedding = []

        # 添加 "pad_b" 和 "UNK",  分别表示补齐的用词和未见词 注意，这些词不要在语料中出现
        vocab.append("pad_b")
        wordEmbedding.append(np.zeros(embeddingSize))

        vocab.append("UNK")
        wordEmbedding.append(np.random.randn(embeddingSize))

        for word in words:
            vector = model.wv[word]
            vocab.append(word)
            wordEmbedding.append(vector)

        print("final vocab",vocab[10:])
        return vocab, np.array(wordEmbedding,dtype=object)


    #统一输入文本序列的定长，取了所有序列长度的均值。超出将被截断，不足则补0
    sequenceLength = 200
    #分词后保留大于等于最低词频的词
    miniFreq=1


    """
    生成词向量和词汇-索引映射字典，可以用全数据集
    """
    allWords = [word for review in reviews for word in review]


    #去掉停用词
    subWords = [word for word in allWords if word not in stopWordDict]


    #统计词频，排序
    wordCount = Counter(subWords)  
    sortWordCount = sorted(wordCount.items(), key=lambda x: x[0], reverse=True)


    #去除低频词
    words = [item[0] for item in sortWordCount if item[1] >= miniFreq ]


    #获取词列表和顺序对应的预训练权重矩阵
    vocab, wordEmbedding = getWordEmbedding(words)

    wordToIndex = dict(zip(vocab, list(range(len(vocab)))))

    def reviewProcess(review, sequenceLength, wordToIndex):
            """
            将测试中的评论里面的词，根据词表，映射为index表示
            每条评论 用index组成的定长数组来表示
            """
            
            reviewVec = np.zeros((sequenceLength))
            sequenceLen = sequenceLength
            
            # 判断当前的序列是否小于定义的固定序列长度
            if len(review) < sequenceLength:
                sequenceLen = len(review)
                
            for i in range(sequenceLen):
                if review[i] in wordToIndex:
                    reviewVec[i] = wordToIndex[review[i]]
                else:
                    reviewVec[i] = wordToIndex["UNK"]

            return reviewVec


    reviews_index = []

    # 遍历所有的文本，将文本中的词转换成index表示
    for i in range(len(reviews)):
        reviewVec = reviewProcess(reviews[i], sequenceLength, wordToIndex)
        reviews_index.append(reviewVec)
    

    rate = 0.01
    trainIndex = int(len(reviews) * rate)

    '''
    测试集
    '''
    evalReviews = np.asarray(reviews_index[trainIndex:], dtype="int64")


    model = keras.models.load_model("model/Text-Categorization.h5")

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'],run_eagerly=True)
    '''
    判断样本属于那个类别的概率
    '''
    result = model.predict(evalReviews)
    '''
    即为情感分析预测步骤
    在我这里：1是坏的0是好的！
    '''
    result_labels = np.argmax(result, axis=1)  
    print('预测结果为',result_labels)
    return result_labels


