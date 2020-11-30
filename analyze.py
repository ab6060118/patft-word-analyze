from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import MySQLdb
import pandas as pd
import threading as td
from queue import Queue

stop_words = [
    'an', 'and', 'as', 'at',
    'by',
    'for',
    'in', 'is',
    'of', 'on', 'or',
    'the', 'to']

class Analyze:
    db = None
    result = None
    lv2 = dict()
    lv3 = dict()
    lv4 = dict()
    lv5 = dict()
    appearInDoc = dict()

    def __init__(self):
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="example", database="patft")

    def load(self):
        cursor = self.db.cursor()
        #  command = 'SELECT * FROM post_v1 LIMIT 500'
        command = 'SELECT * FROM post_v1'
        cursor.execute(command)
        self.result = cursor.fetchall()

    def classification(self):
        for row in self.result:
            classes = re.findall(r"\b[A-Z]\d\d[A-Z] \d+", row[4])
            for cls in classes:
                #  clsA = re.findall(r".", cls)[0]
                #  clsB = re.findall(r"[A-Z]\d\d", cls)[0]
                #  clsC = re.findall(r"[A-Z]\d\d", cls)[0]

                #  if clsA not in self.lv2:
                    #  self.lv2[clsA] = set()
                #  self.lv2[clsA].add(row[0])

                #  if clsB not in self.lv3:
                    #  self.lv3[clsB] = set()
                #  self.lv3[clsB].add(row[0])

                #  if cls not in self.lv4:
                    #  self.lv4[cls] = set()
                #  self.lv4[cls].add(row)

                if cls not in self.lv5:
                    self.lv5[cls] = set()
                self.lv5[cls].add(row)

        #  i = 0
        #  j = 0
        #  k = 0
        #  l = 0
        #  for key, posts in self.lv2.items():
            #  print(key, len(posts))
            #  i = i + len(posts)

        #  for key, posts in self.lv3.items():
            #  print(key, len(posts))
            #  j = j + len(posts)

        #  for key, posts in self.lv4.items():
            #  print(key, ',', len(posts))
            #  k = k + len(posts)

        #  for key, posts in self.lv5.items():
            #  print(key, ',', len(posts))
            #  l = l + len(posts)

        #  print(i, j, k, l)

    def doAnalyze(self):
        #  for key, posts in self.lv5.items():
        key = 'H01L 21'
        posts = self.lv5[key]

        #  if len(posts) < 10: continue
        vectorizer = CountVectorizer(stop_words=stop_words, token_pattern="(?u)\\b\\w\\w+\\b")
        transformer = TfidfTransformer(smooth_idf=True)
        # all
        #  X = vectorizer.fit_transform(list(map(lambda post: ' '.join([post[2], post[3], post[6]]), posts)))
        # claim
        X = vectorizer.fit_transform(list(map(lambda post: ' '.join([post[3]]), posts)))
        #  Z = transformer.fit_transform(X)

        def appearInDocMap(a1):
            a2 = vectorizer.get_feature_names()
            i = 0
            for a in a1:
                if a > 0:
                    if a2[i] not in self.appearInDoc:
                        self.appearInDoc[a2[i]] = 0
                    self.appearInDoc[a2[i]] = self.appearInDoc[a2[i]] + 1
                i = i + 1

        #word count
        def mapfn(a1, a2):
            zipped = list(zip(vectorizer.get_feature_names(), a1, a2))
            res = sorted(zipped, reverse=True, key = lambda x: x[2])
            a, b, c = zip(*res[:10])
            return list(map(lambda aa,cc: aa + '(' + str(cc) + ')', a, c))

        #TFIDF
        def mapfn1(a1):
            zipped = list(zip(vectorizer.get_feature_names(), a1))
            res = sorted(zipped, reverse=True, key = lambda x: x[1])
            a, b = zip(*res[:10])
            return a
        #appear in doc

        #word count
        #  mapped = list(map(mapfn, Z.toarray(), X.toarray()))
        #TFIDF
        #  mapped = list(map(mapfn1, Z.toarray(), X.toarray()))
        #  print(key)
        #  print('id, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10')
        #  for i in range(len(mapped)):
            #  print(
                #  list(posts)[i][0].replace(',', '') + ',',
                #  mapped[i][0] + ',',
                #  mapped[i][1] + ',',
                #  mapped[i][2] + ',',
                #  mapped[i][3] + ',',
                #  mapped[i][4] + ',',
                #  mapped[i][5] + ',',
                #  mapped[i][6] + ',',
                #  mapped[i][7] + ',',
                #  mapped[i][8] + ',',
                #  mapped[i][9] + ','
            #  )
        for post in X.toarray():
            appearInDocMap(post)

        for key, count in self.appearInDoc.items():
            print(key + ',' + str(count))

analyzer = Analyze()

analyzer.load()
analyzer.classification()
analyzer.doAnalyze()
