#!/usr/bin/env python
# coding: utf-8

# # **토픽모델링**

# ### **데이터 읽기**

# In[ ]:


import pandas as pd


# In[ ]:


#데이터 읽기
Corpus_all = pd.read_csv("밀키트 뉴스데이터 전처리_최종.csv", encoding="utf8")
print("데이터 개수 :",len(Corpus_all))
Corpus_all.head()


# ### **주요 단어 빈도 확인**

# In[ ]:


Corpus_org = Corpus_all["키워드"]
Corpus = [wl.split(",")  for wl in Corpus_org]


# In[ ]:


def isHangulOrAlphabet(word):
    return word[0].isalpha() 


# In[ ]:


isHangulOrAlphabet("12")


# In[ ]:


for wl in Corpus[:3]:
  print(wl)


# In[ ]:


def Word_count(corpus):
    word_cnt = dict()
    for text in corpus:
        for word in text:
            if word_cnt.get(word):
                word_cnt[word]+=1
            else:
                word_cnt[word]=1
    cnt_df = pd.DataFrame.from_dict(word_cnt, orient='index')
    cnt_df.columns = ["개수"]
    cnt_df = cnt_df.sort_values(["개수"],ascending=False)
    return word_cnt, cnt_df


# In[ ]:


Words_cnt, Cnt_df = Word_count(Corpus)


# In[ ]:


len(Cnt_df)


# In[ ]:


# 저장
Cnt_df.to_csv("주요 단어빈도.csv", encoding="utf-8-sig")


# # **3-1 LDA  토픽모델링**

# In[ ]:


pip install gensim


# In[ ]:


pip install pyLDAvis


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
import pickle
from gensim import corpora
import gensim


# In[ ]:


class LDA_model:
    def __init__(self,corpus):
        self.corpus = corpus
        return;
    def mk_detokenized_doc(self):
        self.detokenized_doc = []
        for i in range(len(self.corpus)):
            try:
                t = ' '.join(self.corpus.iloc[i])
                self.detokenized_doc.append(t)
            except:
                print(i)
        return;
    def tf_idf_vector(self,max_features):
        self.vectorizer = TfidfVectorizer(max_features= max_features) # 상위 1000개의 단어 보존
        self.X = self.vectorizer.fit_transform(self.detokenized_doc)
        return;
    def mk_word2id(self):
        self.word2id = defaultdict(lambda : 0)
        for idx, feature in enumerate(self.vectorizer.get_feature_names()):
            self.word2id[feature] = idx
        return;
    def print_word2id(self,n=1):
        for i, sent in enumerate(self.detokenized_doc):
            print('====== document[%d] ======' % i)
            print( [ (token, self.X[i, self.word2id[token]]) for token in sent.split() ] )
            if i==n:
                break
        return;
    def mk_lda_model(self,n_topic=10,max_iter=1):
        self.lda_model=LatentDirichletAllocation(n_components=n_topic,learning_method='online',random_state=777,max_iter=max_iter)
        self.lda_top=self.lda_model.fit_transform(self.X)
        return;
    def print_lda(self):
        print("-------------------------------------")
        print(self.lda_model.components_)
        print(self.lda_model.components_.shape) 
        return;
    def print_topic_lda(self,n=5):
        print("-------------------------------------")
        terms = self.vectorizer.get_feature_names() # 단어 집합. 1,000개의 단어가 저장됨.
        for idx, topic in enumerate(self.lda_model.components_):
            print("Topic %d:" % (idx+1), [(terms[i], topic[i].round(2)) for i in topic.argsort()[:-n - 1:-1]])
        return;


# In[ ]:


model_all = LDA_model(Corpus)


# # **3-2 LDA 토픽모델링 시각화**

# - 토픽별 단어 분포

# In[ ]:


dictionary = corpora.Dictionary(model_all.corpus)
corpus = [dictionary.doc2bow(text) for text in model_all.corpus]
NUM_TOPICS = 9
num_words = 30
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
topics = ldamodel.print_topics(num_words=num_words)
for topic in topics:
    print(topic)
dictionary.save('dictionary_전처리.gensim')
pickle.dump(corpus, open('corpus_전처리.pkl', 'wb'))
ldamodel.save('gensim_model_전처리.gensim')


# In[ ]:


pip install pyLDAvis


# In[ ]:


import pyLDAvis
import pyLDAvis.gensim_models
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary)
pyLDAvis.save_html(vis,"lda_전처리.html")


# In[ ]:


len(dictionary) # 각 단어의 정수형 표시


# In[ ]:


NUM_TOPICS = 9
num_words = 30
#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
topics = ldamodel.print_topics(num_words=num_words)
for topic in topics:
    print(topic)


# ---
# # **불러와서 분석**

# In[ ]:


dictionary = gensim.corpora.Dictionary.load('dictionary_전처리.gensim')
corpus = pickle.load(open('corpus_전처리.pkl', 'rb'))
ldamodel = gensim.models.ldamodel.LdaModel.load('gensim_model_전처리.gensim')

