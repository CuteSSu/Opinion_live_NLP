
import pandas as pd
import re
import kss



df = pd.read_excel('./data/댓글_naver.xlsx')  ##경로
#df2 = pd.read_excel('./data/댓글_youtube.xlsx')
#df = pd.concat([df1, df2])

# 이모티콘
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\U00010000-\U0010ffff""]+", flags=re.UNICODE)
print("3")

# html 태그
cleanr1 = re.compile('</?br/?>')
cleanr2 = re.compile('/?&quot/?')
cleanr3 = re.compile('/?&lt/?')
cleanr4 = re.compile('</?a href.*/?>')
cleanr5 = re.compile('/?&gt/?')
cleanr6 = re.compile('</?i/?>')
cleanr7 = re.compile('/?j&amp;j/?')
cleanr8 = re.compile('/?&#39;/?')
cleanr9 = re.compile('</?b/?>')

comment_result = []
print("4")
# 이모티콘, html 태그 삭제
for i in range(len(df)):
    tokens = re.sub(emoji_pattern,"",df['command'].iloc[i])
    tokens = re.sub(cleanr1,"",tokens)
    tokens = re.sub(cleanr2,"",tokens)
    tokens = re.sub(cleanr3,"",tokens)
    tokens = re.sub(cleanr4,"",tokens)
    tokens = re.sub(cleanr5,"",tokens)
    tokens = re.sub(cleanr6,"",tokens)
    tokens = re.sub(cleanr7,"",tokens)
    tokens = re.sub(cleanr8,"",tokens)
    tokens = re.sub(cleanr9,"",tokens)
    comment_result.append(tokens)
print("5")
# 정제된 댓글 데이터 프레임 생성
comment_result = pd.DataFrame(comment_result, columns=["command"])
df02 = pd.DataFrame(comment_result)
print("6")
print("정제후 df길이: ", len(df02))
print(df02.head(10))

df02=df02.dropna(axis=0)

sentences = []
for i in df02['command']:
    print(i)
    sent = kss.split_sentences(i)
    sentences = sentences + sent

print("6")
df03 = pd.DataFrame(sentences, columns=["command"])
print("문장나눈후: ", len(df03))
df03=df03.drop_duplicates('command')
df03 = df03.dropna(axis=0)
print("중복제거후: ", len(df03))

sen=[]

for i in df03['command']:
  text = re.sub('[一-龥豈-龎]+', 'sumin', i)

  if len(text)<120 and 'sumin' not in text:
    sen.append(text)

df04 = pd.DataFrame(sen, columns=["command"])
print("장문, 한자 제거후: ", len(df04))

#엑셀저장
df04.to_excel('./data/댓글_total.xlsx')
