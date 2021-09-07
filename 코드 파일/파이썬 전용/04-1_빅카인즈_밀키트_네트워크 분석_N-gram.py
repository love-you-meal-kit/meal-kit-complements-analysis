#!/usr/bin/env python
# coding: utf-8

# # **4. 네트워크 분석**

# ## **4-1 N-gram 분석 코드**

# In[ ]:


import pandas as pd
from collections import Counter
from nltk.util import ngrams
from itertools import tee, islice


# In[ ]:


#파일 읽기
df = pd.read_csv('밀키트 뉴스데이터 전처리_최종.csv')


# In[ ]:


df.head()


# In[ ]:


#DataFrame to list
df_list = df.values.tolist()


# In[ ]:


df_list[0][0]


# In[ ]:


def ngrams(lst, n):
    tlst = lst
    while True:
        a, b = tee(tlst)
        l = tuple(islice(a,n))
        if len(l) == n:
            yield l
            next(b)
            tlst = b
        else:
            break
    return tlst


# In[ ]:


counters = []
for index, row in df.iterrows():
    keyword_list = row.키워드.split(',')
    counters.append(Counter(ngrams(keyword_list, 2)))


# In[ ]:


counts = sum(counters, Counter())


# In[ ]:


len(counts.items())


# In[ ]:


counts.most_common(20)


# ## **4-2 N-gram 분석 결과**

# In[ ]:


result = []
for i in counts.most_common():
    row = list(i)
    data = list(i[0]) + [row[1]]
    result.append(data)


# In[ ]:


data_frame = pd.DataFrame(result, columns=['word1', 'word2', 'feq'])


# In[ ]:


data_frame.to_csv('n-gram_분석결과.csv', encoding='utf-8-sig')

