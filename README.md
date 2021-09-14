# 온라인 댓글의 화행 분석을 통한 사회적 여론 추정
> 2021 데이터 청년 캠퍼스 서울여대

<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Flask-26689A?style=flat-square&logo=Flask&logoColor=white"/></br>
<img src="https://img.shields.io/badge/colab-F9AB00?style=flat-square&logo=Google Colab&logoColor=white"/> <img src="https://img.shields.io/badge/pycham-00A98F?style=flat-square&logo=PyCharm&logoColor=white"/>

**[참고] 깃헙에서 파이참 버전은 웹사이트 구동하는 서비스를 위한 코드이고
 코랩버전은 결과까지만 반영한 코드입니다. 
 크롤링, 모델링 등 기본 코드는 똑같습니다. 서비스 시연전까지 모든 과정은 코랩에서 진행하였고, 웹페이지 구동을 파이참에서 했기에 이 점이 다릅니다. 



## [ Index ]
1. Description
   - 프로젝트 개요
   - 프로젝트 주제 설명
2. 프로젝트 과정
   - 개발 과정

</br>


***
## 프로젝트 개요
#### 📅 기간:  2021/07/30 - 2021/09/10
#### 👩‍🎓 조원: 김수민, 김성윤, 임수희, 전민경, 조은수
<table>
  <tr>
    <td>주차</td>
    <td>활동</td>
  </tr>
  <tr>
    <td colspan="1">1주차</td>
    <td colspan="1">주제 잡기, 기사 댓글 크롤링, 댓글 전처리</td>
  </tr>
  <tr>
    <td colspan="1">2주차</td>
    <td colspan="1">화행에 대한 연구 및 화행 카테고리 선정, 라벨링, 학습 데이터셋 구축</td>
  </tr>
    <tr>
    <td colspan="1">3주차</td>
    <td colspan="1">bert, electra 모델들 비교 및 공부</td>
  </tr>
   <tr>
    <td colspan="1">4주차</td>
    <td colspan="1">모델 finetuning</td>
  </tr>
   <tr>
    <td colspan="1">5주차</td>
    <td colspan="1">ppt 발표 자료 제작, 토픽 모델링, 감정 분석, 웹페이지 구축</td>
  </tr>
   <tr>
    <td colspan="1">6주차</td>
    <td colspan="1">ppt 발표 자료 수정, 웹페이지 구축 수정</td>
  </tr>
</table>

</br>
</br>

## 프로젝트 주제
### *화행분석으로 댓글을 통해 여론 파악* </br>
<strong> ❓ 화행이란</strong></br>
-> 언어행위나 의사소통 과정에서 발화자가 가지는 의도</br>
</br>
<strong>❓ 감정, 감성 분석이 아닌 화행 분석을 한 이유</strong></br>
-> 댓글을 통해 여론 파악을 하기 위해서는 단순하게 댓글이 전체적으로 긍정적인지, 부정적인지 파악하는 것에 그치지 않고 발화자의 실질적 의도를 파악하는 것이 더 자세하게 여론을 파악할 수 있다고 판단</br>


***
</br>
</br>

## 개발과정
### ✔ 1주차 | 주제 정하기, 댓글 크롤링, 텍스트 전처리
##### <span style="color:red">1] 댓글 크롤링</span>
유튜브, 네이버, 다음 3 플랫폼에 대해서 기사 댓글 크롤링
유튜브: 유튜브 api를 통해 크롤링
네이버: 키워드를 통해 크롤링
다음: 키워드를 통해 크롤링



##### <span style="color:red">2] 텍스트 전처리</span>
크롤링한 댓글 데이터를 이모티콘, html 태그, 한자, 장문 제거

</br>

### ✔ 2주차 | 화행 카테고리 정하기, 화행 카테고리별 패턴 정하기, 라벨링
##### <span style="color:red">3] 화행 카테고리 정하기</span>
+ 정종수 교수님의 [한국어 화행 이론](http://contents.kocw.or.kr/KOCW/document/2015/hanyang/jeongjongsu1) 기반으로 기본 카테고리 설정
+ 댓글 특성상 특수 화행이 존재하여 새로운 화행 카테고리 선정(화행 교수님들께 자문 구하여 적합성 판단)  



##### <span style="color:red">4] 텍스트 전처리, 학습 데이터셋 구축</span>
1. 맞춤법 검사: 부산대 맞춤법 검사, 한셀
2. 문장 나누기: kss분류기
3. 형태소 분석: mecab, okt
4. 구문으로 묶기: 직접 댓글을 보고 grammar수정, 사용자 사전 수정
5. 문장과 구(pharse)로 이루어진 학습 데이터셋 구축
6. 댓글 데이터를 보고 각 화행별로 분류하기 위한 패턴 정의: 정해진 카테고리에 라벨링 하기 위해서 댓글보고 패턴 정의
7. 데이터셋에 대한 라벨링


</br>

### ✔ 3주차 | 모델 공부하기, Bert와 Electra 비교
##### <span style="color:red">5] 모델 비교 </span>
+ 한국어로 pre-trained된 모델을 찾아서 accuracy 비교
+ etri의 korbert는 따로 open api를 받고 학습 데이터를 기관으로 부터 받아야되는 과정이 필요

모델 | Bert Multilingual | [KorBert](https://aiopen.etri.re.kr/service_dataset.php)  | [HanBert](https://github.com/monologg/HanBert-Transformers.git) | [KoBert](https://github.com/SKTBrain/KoBERT.git) | [KoElectra](https://github.com/monologg/KoELECTRA.git) | [KcElectra](https://github.com/Beomi/KcELECTRA.git)
---- |----------------- | -------  | ------- | ------ | --------- | ---------
dataset | 104개 언어의 위키피디아 코퍼스  | 한국어 신문기사와 백과사전 | 일반문서와 특허문서의 3.7억개 문장  | 한국어 위키피디아 코퍼스  | 32GB의 한국어 text | 14GB의 네이버 뉴스 댓글, 대댓글  | 14GB의 네이버 뉴스 댓글, 대댓글  
accuracy | 0.72 | 0.78  |  0.80 | 0.79  | 0.73  |  0.74  |  0.79  

👉 <strong>Electra?</strong>학습 데이터셋이 적기때문에 (약 4천개) 작은 데이터셋으로도 성능이 잘 나오는 electra선택 </br>
👉 <strong>Kc?</strong>댓글 데이터 특성상 비정형화된 한국어가 많아서 네이버 기사 댓글로 학습한 KcElectra선택

</br>

### ✔ 4주차 | 모델 fine tuning
##### <span style="color:red">6] fine turing </span>
+ 이진분류 모델이였던 electra를 다중 분류 모델로 튜닝
+ batch size, learing rate, epochs, max_len, AdamP/W: 여러가지 조합으로 최적의 조합 선정


</br>

### ✔ 5주차 | 감정분석, 토픽 모델링, 데모 웹사이트 제작
##### <span style="color:red">7] 감정분석</span>
전체적인 댓글의 동향을 먼저 파악하기 위해 감정 분석 진행
- electra모델 사용
- 네이버 영화리뷰를 학습데이터셋으로 사용

</br>

##### <span style="color:red">8] 토픽 모델링</span>
각 화행 별로 토픽 모델링 진행
LDA 시각화 함

```python
import pyLDAvis.gensim_models
```
pyLDAvis.gensim_models는 <strong>코랩</strong>에서 에러가 나서 코랩 환경에서 사용시 pyLDAvis버전을 [2.1.2]( https://pyldavis.readthedocs.io/en/latest/history.html)로해야된다, <strong>주피터</strong>에서는 gensim_models 가능 `(2021/08/25기준)`  


</br>

### ✔ 6주차 | 데모 웹사이트 수정 및 발표 자료 수정
##### <span style="color:red">9] 웹페이지</span>
대시보드 페이지 생성(감성분석, 화행분석, 토픽모델링)
- flask

![dashboard](https://user-images.githubusercontent.com/29356103/133049954-1727f903-4524-4a6a-95d9-0593fcb14ce7.png)


</br>

***
## 발표 PPT

![슬라이드1](https://user-images.githubusercontent.com/29356103/133043053-b4b4d752-69d4-48a7-b2fb-5b3a74cf6bdc.PNG)
![슬라이드2](https://user-images.githubusercontent.com/29356103/133043057-33436b06-e0cd-4d56-8f71-c0561a3efee3.PNG)
![슬라이드3](https://user-images.githubusercontent.com/29356103/133043060-5160b34c-1795-43c5-9ce2-7755b36c38d1.PNG)
![슬라이드4](https://user-images.githubusercontent.com/29356103/133043064-a571e73f-0fc0-416c-a58a-1dcefb11a119.PNG)
![슬라이드5](https://user-images.githubusercontent.com/29356103/133043066-105bcf9f-d737-4089-bf8e-5c75b124a231.PNG)
![슬라이드6](https://user-images.githubusercontent.com/29356103/133043067-3c7c5ec0-1716-45da-9ee2-c7c38a43f950.PNG)
![슬라이드7](https://user-images.githubusercontent.com/29356103/133043069-8491ff4a-2c34-47d8-9c96-11c0dd0c1bb9.PNG)
![슬라이드8](https://user-images.githubusercontent.com/29356103/133043072-6ec71d04-356a-4ca6-a0be-f481e432acae.PNG)
![슬라이드9](https://user-images.githubusercontent.com/29356103/133043075-c8ffd0d8-2f7d-452b-a015-968b7a55b72d.PNG)
![슬라이드10](https://user-images.githubusercontent.com/29356103/133043076-f0b4e7d4-3141-4174-bcd7-b2af2bc0f4b2.PNG)
![슬라이드11](https://user-images.githubusercontent.com/29356103/133043077-fac61c84-72d1-4a1a-9646-08f253de9943.PNG)
![슬라이드12](https://user-images.githubusercontent.com/29356103/133043079-7e8727e2-ed04-4600-8bb5-66acfe678fdb.PNG)
![슬라이드13](https://user-images.githubusercontent.com/29356103/133043081-459716cd-c7ea-432d-af92-2baa3732eda0.PNG)
![슬라이드14](https://user-images.githubusercontent.com/29356103/133043083-1c49ca36-645e-4d64-96fe-55e66acc8d89.PNG)
![슬라이드15](https://user-images.githubusercontent.com/29356103/133043086-cb18aff2-04c7-41ba-8bbd-c78b63a7ad18.PNG)
![슬라이드16](https://user-images.githubusercontent.com/29356103/133043087-53ec5675-eef4-4d0f-96e6-ca4dd69ab675.PNG)
![슬라이드17](https://user-images.githubusercontent.com/29356103/133043090-8d11e380-64f1-4353-94d7-d6782aa5e1a0.PNG)
![슬라이드18](https://user-images.githubusercontent.com/29356103/133043092-82f63fa8-9ed6-44c5-abe7-f0f31c465a7a.PNG)
![슬라이드19](https://user-images.githubusercontent.com/29356103/133043095-e1baf33d-8866-4874-85d1-a009dfec08a7.PNG)
![슬라이드20](https://user-images.githubusercontent.com/29356103/133043097-0441016f-68ed-4456-ae3f-c9736cea94e3.PNG)
![슬라이드21](https://user-images.githubusercontent.com/29356103/133043100-44146c43-36dd-4654-b90c-b2c68c5e4540.PNG)
![슬라이드22](https://user-images.githubusercontent.com/29356103/133043103-e81a280d-2be5-4761-8f31-c06a7d836965.PNG)
![슬라이드23](https://user-images.githubusercontent.com/29356103/133043104-844decc0-d8d1-412b-ae69-fa922716db93.PNG)
![슬라이드24](https://user-images.githubusercontent.com/29356103/133043109-15398029-a339-4005-8af5-f5762ee51954.PNG)
![슬라이드25](https://user-images.githubusercontent.com/29356103/133043113-5bb24eb0-4625-4161-9d90-e9af881ece5c.PNG)
![슬라이드26](https://user-images.githubusercontent.com/29356103/133043115-bb8c9012-5bc7-4596-bcca-8cc214f16711.PNG)
![슬라이드27](https://user-images.githubusercontent.com/29356103/133043119-9f3bf696-a9b8-47e9-971e-1f93724d1d30.PNG)
![슬라이드28](https://user-images.githubusercontent.com/29356103/133043120-1d1c4380-8a37-4673-88f2-92c6314c2e23.PNG)
![슬라이드29](https://user-images.githubusercontent.com/29356103/133043121-9eb5ef95-4658-4f9c-a841-faa89913449e.PNG)
![슬라이드30](https://user-images.githubusercontent.com/29356103/133043123-b65b3ca2-84f3-4fd6-9b3b-94658a014398.PNG)
![슬라이드31](https://user-images.githubusercontent.com/29356103/133043126-9af6f3ac-d35d-447b-9fe8-8a7e0b8a2449.PNG)
![슬라이드32](https://user-images.githubusercontent.com/29356103/133043129-53f6748a-dbeb-4da6-ae2f-4de98c9f8713.PNG)



***
write by @CuteSSu
