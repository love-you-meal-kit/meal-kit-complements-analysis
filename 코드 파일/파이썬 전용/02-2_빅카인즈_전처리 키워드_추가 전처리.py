#!/usr/bin/env python
# coding: utf-8

# # ** 2-7 추가 전처리**

# ### **빅카인즈에서 제공한 키워드(밀키트 뉴스데이터.csv)에 대해 연구목적에 맞게 추가적으로 전처리를 진행함**

# In[ ]:


import pandas as pd
df=pd.read_csv("밀키트 뉴스데이터.csv")


# In[ ]:


#단어 교체
def change(text):
    text_list=text.split(',')
    result=[]
    for c in text_list:
        if c=='11번':
            c=c.replace('11번','11번가')
        if c=='인공지능':
            c=c.replace('인공지능','AI')
        result.append(c)
    return result


# In[ ]:


df['키워드']=df['키워드'].map(lambda x: change(x))


# In[ ]:


stopwords=pd.read_csv('불용어 처리.txt',header=None)


# In[ ]:


stopwords=stopwords[0].tolist()


# In[ ]:


#불용어처리
def remove(text,stopwords):
    keywords=','.join([c for c in text if c not in stopwords])
    return keywords


# In[ ]:


df['키워드']=df['키워드'].map(lambda x: remove(x,stopwords) )


# In[ ]:


df=df['키워드']


# In[ ]:


df


# In[ ]:


df=df[:5506]
df


# In[ ]:


df.to_csv('밀키트 뉴스데이터 전처리_최종.csv',encoding='utf-8-sig')

