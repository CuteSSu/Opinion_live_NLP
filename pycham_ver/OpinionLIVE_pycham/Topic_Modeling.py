# -*- coding: utf-8 -*-
## 토픽모델링

#import해야하는 라이브러리들
from konlpy.tag import Okt
import pandas as pd
import string # 특수문자
import re
from gensim import corpora
from gensim import models

import pyLDAvis.gensim

##%matplotlib inline

def text_cleaning(docs):
    # 한국어를 제외한 글자를 제거하는 함수.
    for doc in docs:
        doc = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힇a-zA-Z ]", "", doc)
    return docs


def define_stopwords(path):
    SW = set()
    # 불용어를 추가하는 방법 1.
    for i in string.punctuation:
        SW.add(i)

    # 불용어를 추가하는 방법 2.
    # stopwords-ko.txt에 직접 추가

    with open(path,encoding='UTF8') as f:
        for word in f:
            SW.add(word)

    return SW


def text_tokenizing(corpus, tokenizer):
    okt = Okt()
    token_corpus = []

    SW2 = [line.rstrip() for line in SW]

    if tokenizer == "noun":
        for n in range(len(corpus)):
            token_text = okt.nouns(corpus[n])
            token_text = [word for word in token_text if word not in SW2 and len(word) > 1]

            token_corpus.append(token_text)

    elif tokenizer == "morph":
        for n in range(len(corpus)):
            token_text = okt.morphs(corpus[n])
            token_text = [word for word in token_text if word not in SW2 and len(word) > 1]
            token_corpus.append(token_text)

    elif tokenizer == "word":
        for n in range(len(corpus)):
            token_text = corpus[n].split()
            token_text = [word for word in token_text if word not in SW2 and len(word) > 1]
            token_corpus.append(token_text)

    return token_corpus


def build_doc_term_mat(documents):
    # 문서-단어 행렬 만들어주는 함수.
    print("Building document-term matrix.")
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(document) for document in documents]

    return corpus, dictionary


def print_topic_words(model):
    # 토픽 모델링 결과를 출력해 주는 함수.
    print("\nPrinting topic words.\n")

    for topic_id in range(model.num_topics):
        topic_word_probs = model.show_topic(topic_id, NUM_TOPIC_WORDS)
        print("Topic ID: {}".format(topic_id))

        for topic_word, prob in topic_word_probs:
            print("\t{}\t{}".format(topic_word, prob))

        print("\n")



def topic_modeling_result():
    # 결과파일 가져오기
    topicfile = './data/거리두기_화행분류.xlsx'
    topicexcel = pd.read_excel(topicfile)

    topic_pd1 = topicexcel[topicexcel['label'] == '명령']
    topic_pd1 = topic_pd1['command']
    topic1_list = topic_pd1.tolist()

    topic_pd2 = topicexcel[topicexcel['label'] == '약속']
    topic_pd2 = topic_pd2['command']
    topic2_list = topic_pd2.tolist()

    topic_pd3 = topicexcel[topicexcel['label'] == '기대']
    topic_pd3 = topic_pd3['command']
    topic3_list = topic_pd3.tolist()

    topic_pd4 = topicexcel[topicexcel['label'] == '주장']
    topic_pd4 = topic_pd4['command']
    topic4_list = topic_pd4.tolist()

    topic_pd5 = topicexcel[topicexcel['label'] == '갈등']
    topic_pd5 = topic_pd5['command']
    topic5_list = topic_pd5.tolist()

    topic_pd6 = topicexcel[topicexcel['label'] == '질문']
    topic_pd6 = topic_pd6['command']
    topic6_list = topic_pd6.tolist()

    topic_pd7 = topicexcel[topicexcel['label'] == '진술']
    topic_pd7 = topic_pd7['command']
    topic7_list = topic_pd7.tolist()

    topic_pd8 = topicexcel[topicexcel['label'] == '정표']
    topic_pd8 = topic_pd8['command']
    topic8_list = topic_pd8.tolist()

    # 토픽 개수, 키워드 개수를 정해주는 변수
    global NUM_TOPICS, NUM_TOPIC_WORDS
    NUM_TOPICS = 3
    NUM_TOPIC_WORDS = 30

    title = ['명령NUM_30_3', '약속NUM_30_3', '기대NUM_30_3', '주장NUM_30_3', '갈등NUM_30_3','질문NUM_30_3','진술NUM_30_3','정표NUM_30_3']

    a = 0
    for i in [topic1_list, topic2_list, topic3_list, topic4_list, topic5_list, topic6_list, topic7_list,topic8_list]:
        global SW
        SW = define_stopwords("./data/stopwords-ko.txt")
        cleaned_text = text_cleaning(i)
        tokenized_text = text_tokenizing(cleaned_text, tokenizer="noun")  # tokenizer= "noun" or "word"
        tokenized_text = [item for item in tokenized_text if item != []]

        # document-term matrix를 만들고,
        corpus, dictionary = build_doc_term_mat(tokenized_text)

        # LDA를 실행.
        model = models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=30, alpha="auto",eta="auto")
        # 결과를 출력.
        print_topic_words(model)
        # pyLDAvis를 jupyter notebook에서 실행할 수 있게 활성화.
        # pyLDAvis 실행.
        data = pyLDAvis.gensim.prepare(model, corpus, dictionary)
        pyLDAvis.save_html(data, './static/LDA_output/' + str(title[a]) + '.html')
        a = a + 1

