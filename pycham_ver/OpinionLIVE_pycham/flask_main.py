from flask import Flask, render_template
##################################################################웹페이지를 위한 함수..프런트...싫어어어어어어...
import crowling_naver
import crowling_total
import Topic_Modeling

##화행분류
#import해야하는 라이브러리들
import pandas as pd
import torch
from pytorch_lightning import LightningModule
from transformers import ElectraForSequenceClassification, AutoTokenizer
import joblib

# 화행 모델 클래스
class Model(LightningModule):
    def __init__(self, **kwargs):
        super().__init__()
        self.save_hyperparameters()

        self.clsfier = ElectraForSequenceClassification.from_pretrained(self.hparams.pretrained_model, num_labels=8)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.hparams.pretrained_tokenizer
            if self.hparams.pretrained_tokenizer
            else self.hparams.pretrained_model
        )

    # forward: foward() 함수는 모델이 학습데이터를 입력받아서 forward 연산을 진행시키는 함수
    def forward(self, **kwargs):
        return self.clsfier(**kwargs)

# 화행모델 읽기
sp_model = joblib.load('./model_pkl/KcElectraModel.pkl')
def sp_infer(x):
    return torch.softmax(
        sp_model(**sp_model.tokenizer(x, return_tensors='pt')
              ).logits, dim=-1)
def speech_model():
    ##분류할 크롤링 파일 읽기
    df = pd.read_excel('./data/댓글_total.xlsx')  ##경로
    a01 = {}
    a02 = ['명령', '약속', '정표', '기대', '주장', '갈등', '진술', '질문']
    a04 = []

    df02 = pd.DataFrame(columns=['command', 'label'])

    for k in df['command']:
        a03 = 0
        # print(k)
        for i in sp_infer(k):
            for j in i:
                j = j.tolist()  # list
                # a01[a02[a03]]=j
                a01[a02[a03]] = [j]
                a03 += 1
        b = max(a01, key=a01.get)

        a04.append(b)
        df02 = df02.append({'command': k, 'label': b}, ignore_index=True)

    ##화행분류된 파일 정장
    df02.to_excel('./data/거리두기_화행분류.xlsx')  ##경로

    d01 = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in a04:
        if i == '명령':
            d01[0] += 1
        elif i == '약속':
            d01[1] += 1
        elif i == '정표':
            d01[2] += 1
        elif i == '기대':
            d01[3] += 1
        elif i == '주장':
            d01[4] += 1
        elif i == '갈등':
            d01[5] += 1
        elif i == '진술':
            d01[6] += 1
        elif i == '질문':
            d01[7] += 1

    c01 = 0
    for i in range(len(a02)):
        c01 += d01[i]
        print(a02[i], '=', d01[i], '개 입니다,')
    return d01
sp_list = speech_model()



#감정분류 model정의
class Model(LightningModule):
    def __init__(self, **kwargs):
        super().__init__()
        self.save_hyperparameters()  # 이 부분에서 self.hparams에 위 kwargs가 저장된다.

        self.clsfier = ElectraForSequenceClassification.from_pretrained(self.hparams.pretrained_model)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.hparams.pretrained_tokenizer
            if self.hparams.pretrained_tokenizer
            else self.hparams.pretrained_model
        )

    def forward(self, **kwargs):
        return self.clsfier(**kwargs)
#모델읽어오기
se_model = joblib.load("./model_pkl/SA_model.pkl")
#읽어온 모델을 사용하기 위한 함수
def se_infer(x):
    return torch.softmax(
        se_model(**se_model.tokenizer(x, return_tensors='pt')
    ).logits, dim=-1)
def sentiment_model():
    ##분류할 크롤링파일 읽기
    df = pd.read_excel('./data/댓글_total.xlsx')  ##경로

    a = df['command']
    a_to_list = a.tolist()
    print(a_to_list)

    positive = []
    negative = []

    data_len = len(a_to_list)
    print(data_len)
    result_csv=[]

    for i in a_to_list:
      b = se_infer(i)
      re = b.detach().cpu().numpy()

      if float(re[0][0]) < float(re[0][1]):
        #print("긍정 : ",i)
        positive.append(i)
      else:
        #print("부정 : ",i)
        negative.append(i)


    positive_p = len(positive) / data_len
    negative_p = len(negative) / data_len


    print("긍정",positive_p)
    print("부정",negative_p)

    return positive_p,negative_p,data_len
se_list = sentiment_model()

Topic_Modeling.topic_modeling_result()

##################################################################웹페이지를 위한 함수..프런트...싫어어어어어어...
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/base3')
def base3():
    return render_template('base3.html',data =sp_list,data2=[se_list[0],se_list[1]],data3=se_list[2])

@app.route('/loading')
def loading():
    return render_template('loading.html')


if __name__=='__main__':
    app.run()