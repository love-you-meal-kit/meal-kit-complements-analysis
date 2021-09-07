#!/usr/bin/env python
# coding: utf-8

# # **2. 데이터 전처리**

# In[3]:


pip install konlpy


# In[4]:


pip install customized_konlpy


# In[5]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

from ckonlpy.tag import Twitter
from konlpy.tag import Okt
from konlpy.tag import Komoran
from collections import Counter
from wordcloud import WordCloud


# In[6]:


twitter=Twitter()


# In[7]:


df=pd.read_csv("크롤링 결과.csv")
df.head()


# In[8]:


#본문 리스트 만들기
word_list=[]
word_list=df['Content']
word_list=word_list.reset_index(drop=True)
word_list


# In[9]:


#기사중복 삭제
df_drop=df.drop_duplicates(['Date','Title','Content'], keep='first')


# In[10]:


#index reset
df=df_drop.reset_index(drop=True)


# In[11]:


#행,열 최대로 보기
pd.set_option('display.max_row', None)
pd.set_option('display.max_columns', None)


# In[12]:


df.head()
len(df)


# In[13]:


#기사 본문만 가져오기
content=df["Content"]
content.head()


# In[14]:


#None값 제거
drop_row = content.dropna(axis=0)
df=pd.DataFrame([drop_row])
df= df.transpose()


# In[15]:


len(df)


# # **2-1 kkma 사용자 사전 추가**

# In[16]:


#사전에 단어 추가
twitter.add_dictionary('밀키트', 'Noun')
twitter.add_dictionary('코로나19', 'Noun')
twitter.add_dictionary('간편식', 'Noun')
twitter.add_dictionary('프레시지', 'Noun')
twitter.add_dictionary('식재료', 'Noun')
twitter.add_dictionary('GS리테일', 'Noun')
twitter.add_dictionary('한국야쿠르트', 'Noun')
twitter.add_dictionary('소상공인', 'Noun')
twitter.add_dictionary('심플리쿡', 'Noun')
twitter.add_dictionary('피코크', 'Noun')
twitter.add_dictionary('집밥', 'Noun')
twitter.add_dictionary('CJ제일제당', 'Noun')
twitter.add_dictionary('잇츠온', 'Noun')
twitter.add_dictionary('CJ', 'Noun')
twitter.add_dictionary('GS25', 'Noun')
twitter.add_dictionary('론칭', 'Noun')
twitter.add_dictionary('SSG닷컴', 'Noun')
twitter.add_dictionary('쿡킷', 'Noun')
twitter.add_dictionary('현대백화점', 'Noun')
twitter.add_dictionary('지속적', 'Noun')
twitter.add_dictionary('리테일', 'Noun')
twitter.add_dictionary('KT', 'Noun')
twitter.add_dictionary('1인', 'Noun')
twitter.add_dictionary('새벽배송', 'Noun')
twitter.add_dictionary('마켓컬리', 'Noun')
twitter.add_dictionary('SNS', 'Noun')
twitter.add_dictionary('신선식품', 'Noun')
twitter.add_dictionary('롯데백화점', 'Noun')
twitter.add_dictionary('대표적', 'Noun')
twitter.add_dictionary('편스토랑', 'Noun')
twitter.add_dictionary('온라인몰', 'Noun')
twitter.add_dictionary('기획전', 'Noun')
twitter.add_dictionary('언택트', 'Noun')
twitter.add_dictionary('마이셰프', 'Noun')
twitter.add_dictionary('집콕', 'Noun')
twitter.add_dictionary('본격적', 'Noun')
twitter.add_dictionary('현대그린푸드', 'Noun')
twitter.add_dictionary('시그니처', 'Noun')
twitter.add_dictionary('PB', 'Noun')
twitter.add_dictionary('11번가', 'Noun')
twitter.add_dictionary('RMR', 'Noun')
twitter.add_dictionary('식품업계', 'Noun')
twitter.add_dictionary('아이들', 'Noun')
twitter.add_dictionary('LG', 'Noun')


# # **2-2 형태소 분석(명사 추출)**

# In[18]:


from konlpy.tag import Kkma
from konlpy.utils import pprint
from tqdm import tqdm
kkma = Kkma()


# In[19]:


nouns = [] 
for x in tqdm(content):
    try:
        nouns.append(kkma.nouns(x))
    except:
        nouns.append(["None"])


# In[20]:


#명사 추출 결과값 열에 추가
konlpy_df= df.copy()
konlpy_df["ContentNoun"] = nouns


# In[22]:


#json 파일로 저장
konlpy_df.to_json("mealkit_전처리.json",orient="table")


# In[23]:


from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
import pickle
import re


# In[24]:


corpus = pd.read_json("mealkit_전처리.json",orient="table")


# # **2-3 정규화**

# In[17]:


#단어 교체(밀 키트 -> 밀키트)
content=df['Content'].map(lambda x: str(x).replace('밀 키트','밀키트'))
len(content)


# In[25]:


#단어 교체(11번 -> 11번가)
def change(text):
    text=','.join(text)
    text_list=text.split(',')
    result=[]
    for c in text_list:
        if c=='11번':
            c=c.replace('11번','11번가')
        if c=='인공지능':
            c=c.replace('인공지능','AI')
        result.append(c)
    result=','.join(result)
    return result


# In[26]:


corpus['ContentNoun']=corpus['ContentNoun'].map(lambda x: change(x))


# # **2-4 한글자 제거**

# In[27]:


def remove(text):
    text_list=text.split(',')
    result=[]
    for n in text_list:
        if len(n)>1:
            result.append(n)
    result=','.join(result)
    return result

corpus['ContentNoun']=corpus['ContentNoun'].map(lambda x: remove(x))


# # **2-5 불용어 처리**

# ## 불용어 제거
# - 사이트 이용
#     - [사이트1](https://bab2min.tistory.com/544)
#     - [사이트2](https://www.ranks.nl/stopwords/korean)
# - 직접 제거
#     - ./삭제 단어.xlsx

# In[28]:


#직접 제거
stopword1 = pd.read_csv("./불용어 처리.txt",header=None,sep="\t")
stopword1 = list(stopword1[0])
len(stopword1)


# In[29]:


stopword2 = pd.read_csv("한국어불용어100.txt",header=None,sep="\t")
stopword2 = list(stopword2[0])
len(stopword2)


# In[30]:


stopword3 = pd.read_csv("한국어불용어100_2.txt",header=None)
stopword3 = list(stopword3[0])
len(stopword3)


# In[31]:


stopword = list(set(stopword1 + stopword2 + stopword3))
print("불용어 개수 :",len(stopword))


# In[32]:


noun=corpus['ContentNoun']


# In[33]:


noun = [x for x in noun if x not in stopword]
print(noun[:1])


# # **2-6 전처리 결과값**

# In[34]:


file=pd.DataFrame(noun, columns=['키워드'])
file.to_csv("단어(전처리 후).csv",encoding="utf-8-sig")


# In[35]:


file.head()


# ### **※ 전처리 중 bigkinds에서 전처리 키워드를 제공하여, 이후부터는 해당 데이터(밀키트 뉴스데이터.csv)를 사용함**
