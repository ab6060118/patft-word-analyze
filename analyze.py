from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import re
import MySQLdb
import pandas as pd
import csv

# 讀取 stop_words
with open('./stop_words','r') as fp:
    stop_words = fp.read().splitlines()

class Analyze:
    db = None
    key = 'H01L 21'
    result = None
    lv2 = dict()
    lv3 = dict()
    lv4 = dict()
    lv5 = dict()
    appearInDoc = dict()
    analyzeed = None

    def __init__(self):
        # 建立 mysql client
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="example", database="patft")

    def load(self):
        cursor = self.db.cursor()
        # 選取所有資料
        command = 'SELECT United_States_Patent, abstract FROM post_v1'
        cursor.execute(command)
        self.result = cursor.fetchall()

    def classification(self):
        for row in self.result:
            # 使用正規表示式將專利分類
            classes = re.findall(r"\b[A-Z]\d\d[A-Z] \d+", row[4])
            for cls in classes:
                if cls not in self.lv5:
                    self.lv5[cls] = set()
                self.lv5[cls].add(row)

    def doAnalyze(self):
        posts = self.lv5[self.key]

        # 將專利當中詞性不等於名詞的單字剔除
        stripedPosts = map(lambda post: ' '.join(map(lambda tern: tern[0],filter(lambda tern: tern[1] == 'NN', nltk.pos_tag(post[2].split())))), posts)

        vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=r'\w+')
        X = vectorizer.fit_transform(stripedPosts)
        feature_names = vectorizer.get_feature_names()

        # TFIDF
        def mapfn1(a1):
            zipped = list(zip(feature_names, a1))
            res = sorted(zipped, reverse=True, key = lambda x: x[1])
            a, b = zip(*res[:10])
            result = []
            i = 0
            for bb in b:
                if bb == 0:
                    result.append('---')
                else:
                    result.append(a[i])
                i = i + 1
            return result

        self.analyzeed = list(map(mapfn1, X.toarray()))

    def tfidf(self):
        posts = self.result
        vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=r'\w+')
        X = vectorizer.fit_transform(map(lambda post: post[1], posts))
        r = pd.DataFrame(X.toarray(),columns=vectorizer.get_feature_names(), index=map(lambda post: post[0], posts))
        r.to_csv('./tfidf1.csv')


    def output(self):
        mapped = self.analyzeed
        posts = self.lv5[self.key]
        print('id,1,2,3,4,5,6,7,8,9,10')
        for i in range(len(mapped)):
            print(
                list(posts)[i][0].replace(',', '') + ',' +
                mapped[i][0] + ',' +
                mapped[i][1] + ',' +
                mapped[i][2] + ',' +
                mapped[i][3] + ',' +
                mapped[i][4] + ',' +
                mapped[i][5] + ',' +
                mapped[i][6] + ',' +
                mapped[i][7] + ',' +
                mapped[i][8] + ',' +
                mapped[i][9]
            )

def wordCount():
    with open('./H01L_21_abstract_top10.csv','r',newline='') as fp:
        d = dict()
        rows = list(csv.reader(fp))
        for row in rows[1:]:
            for word in row[1:]:
                if word == '' or word == '---': continue
                if word not in d:
                    d[word] = 1
                else:
                    d[word] = d[word] + 1
        for key, value in d.items():
            print(key+','+str(value))

def search(keyword):
    r = pd.read_csv('./tfidf.csv', index_col=False, usecols=['id', keyword])
    r.sort_values(by=keyword,ascending=False).to_csv('./tfidf_search.csv')

def doubleSearch(keyword, k2):
    r = pd.read_csv('./tfidf.csv', index_col=False, usecols=['id', keyword, k2])
    r['sum'] = r[keyword] + r[k2]
    r.sort_values(by='sum',ascending=False).to_csv('./tfidf_search_'+keyword+'_'+k2+'.csv')

analyzer = Analyze()

#  讀取資料庫
#  analyzer.load()
#  將專利分類
#  analyzer.classification()
#  針對類別 H01L 21 進行 TFIDF 分析
#  analyzer.doAnalyze()
#  將結果輸出到畫面
#  analyzer.output()

#  wordCount()

#  讀取資料庫
#  analyzer.load()
#  tfidf analyze
#  analyzer.tfidf()

#  search
#  search('semiconductor')

doubleSearch('semiconductor', 'device')
