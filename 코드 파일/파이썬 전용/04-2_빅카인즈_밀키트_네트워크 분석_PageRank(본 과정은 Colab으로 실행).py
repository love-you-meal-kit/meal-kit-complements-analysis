#!/usr/bin/env python
# coding: utf-8

# ## **4-3 페이지랭크**

# ### **N-gram 분석 후 상위 250여개 데이터(n-gram_분석결과.csv)를 살펴 본 후, 분석 목적에 맞게 수동으로 데이터 수정(n-gram_분석결과_전처리.csv)이후 수정된 데이터를 페이지랭크 분석에 활용함**

# ### **파일 읽기 및 단어 상위 250개 가져오기**

# In[ ]:


import pandas as pd
df=pd.read_csv('n-gram_분석결과_전처리.csv')

df250 = df.iloc[:250]
wordList=[]
for row in df250.itertuples(index=False):
    if row.word1!= row.word2:
        wordList.append((row.word1,row.word2))
wordList


# In[ ]:


uniqueWordList = df250.word1.unique()


# 폰트 설치(구글 코랩에서만 가능)

# In[ ]:


get_ipython().system('sudo apt-get install -y fonts-nanum')
get_ipython().system('sudo fc-cache -fv')
get_ipython().system('rm ~/.cache/matplotlib -rf')


# In[ ]:


get_ipython().system('apt-get update -qq')
get_ipython().system('apt-get install fonts-nanum* -qq')


# ### **상위 250개 데이터 페이지 랭크 결과**

# In[ ]:


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np 
import matplotlib.font_manager as fm

a=nx.DiGraph()

node = uniqueWordList
a.add_nodes_from(node)

a.add_edges_from (wordList)
i = 0

font_location='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fontprop=fm.FontProperties(fname=font_location,size=30).get_name()

pg=nx.pagerank(a,max_iter=100)
print(pg)

pos=nx.spring_layout(a)

#Push every node to the right so that coordinates are all positive
for node in a.nodes:
    pos[node]=[pos[node][0]+1000,pos[node][1]+1000]

#Check distances between nodes for number of iterations
for x in range(20):
    for nodex in a.nodes:
      for nodey in a.nodes:
          if(nodex != nodey):
              # if y distance is too small
              if(max(pos[nodex][1],pos[nodey][1])-min(pos[nodex][1],pos[nodey][1]) <0.6):
                  # check if also x distance is too small
                  if((max(pos[nodex][0],pos[nodey][0])-min(pos[nodex][0],pos[nodey][0])<0.3)):
                      #print(nodex,nodey)
                      if(pos[nodex][1] < pos[nodey][1]):
                          pos[nodex][1] = pos[nodex][1]-0.6
                          pos[nodey][1] = pos[nodey][1]+0.6
                      else:
                          pos[nodex][1] = pos[nodex][1]+0.6
                          pos[nodey][1] = pos[nodey][1]-0.6


plt.figure(figsize=(6,6), dpi=150, facecolor='w')
nx.draw(a,pos, node_color='pink',node_size=[v * 10000 for v in pg.values()], 
        with_labels = True, font_family=fontprop, edge_cmap=plt.cm.OrRd, font_size=7, width=0.5)    #pagerank 값에 10000을 곱하여 노드 크기 설정

plt.show()


# ## **4-4 페이지랭크 분석 결과**

# ### **상위 250개 중 특정 단어 관련 페이지 랭크 결과**

# In[ ]:


result=[]
key=['제품', '요리', '지역', '사업', '코로나19', '배송', '트렌드', '플랫폼', '온라인']
for row in df200.itertuples(index=False):
    if row.word1 in key or row.word2 in key:
        result.append([row.word1,row.word2])
result=pd.DataFrame(result,columns=['word1','word2'])


# In[ ]:


result.head()


# ## **4-5 페이지랭크 시각화**

# In[ ]:


uniqueWordList = result.word1.unique()
result2=[]
for row in result.itertuples(index=False):
    result2.append((row.word1,row.word2))


a=nx.DiGraph()

node = uniqueWordList
a.add_nodes_from(node)

a.add_edges_from (result2)
i = 0
# for name in node:
#     i = i+1
#     print(["%d:%s = %s"% (i,name,str(len(a.out_edges(name))))])

font_location='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fontprop=fm.FontProperties(fname=font_location,size=30).get_name()

pg=nx.pagerank(a,max_iter=100)
print(pg)

pos=nx.spring_layout(a)

#Push every node to the right so that coordinates are all positive
for node in a.nodes:
    pos[node]=[pos[node][0]+1000,pos[node][1]+1000]

#Check distances between nodes for number of iterations
for x in range(20):
    for nodex in a.nodes:
      for nodey in a.nodes:
          if(nodex != nodey):
              # if y distance is too small
              if(max(pos[nodex][1],pos[nodey][1])-min(pos[nodex][1],pos[nodey][1]) <0.6):
                  # check if also x distance is too small
                  if((max(pos[nodex][0],pos[nodey][0])-min(pos[nodex][0],pos[nodey][0])<0.3)):
                      #print(nodex,nodey)
                      if(pos[nodex][1] < pos[nodey][1]):
                          pos[nodex][1] = pos[nodex][1]-0.6
                          pos[nodey][1] = pos[nodey][1]+0.6
                      else:
                          pos[nodex][1] = pos[nodex][1]+0.6
                          pos[nodey][1] = pos[nodey][1]-0.6


plt.figure(figsize=(15,7), dpi=130, facecolor='w')
nx.draw(a,pos=pos,node_color='lightgrey', node_size=[v * 20000 for v in pg.values()]
        ,with_labels = True, font_family=fontprop, edge_cmap=plt.cm.OrRd, font_size=7, width=0.5)

plt.show()


# In[ ]:


new=pd.DataFrame.from_dict([pg])
df = new.transpose()
df.columns=['PageRank']
df.head()
df.to_csv('pagerank결과.csv',encoding='utf-8-sig')


# *폰트 변경 시 폰트 경로 확인

# In[ ]:


font_list=fm.findSystemFonts(fontpaths=None,fontext='ttf')
font_list[:10]

