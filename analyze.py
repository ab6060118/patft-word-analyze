from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import MySQLdb
import pandas as pd
import threading as td
from queue import Queue

class Analyze:
    db = None
    result = None
    classified = dict()

    def __init__(self):
        self.db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="example", database="patft")

    def load(self):
        cursor = self.db.cursor()
        command = 'SELECT * FROM post_v1 LIMIT 30000'
        cursor.execute(command)
        self.result = cursor.fetchall()

    def classification(self):
        for row in self.result:
            classes = re.findall(r"\b[A-Z]\d\d[A-Z]\b", row[4])
            for cls in classes:
                if cls not in self.classified:
                    self.classified[cls] = set()
                self.classified[cls].add(row)
        print(len(self.classified))

    def doAnalyze(self):
        for key, posts in self.classified.items():
            print(key, 'start', len(posts))
            vectorizer = TfidfVectorizer(stop_words=None, token_pattern="(?u)\\b\\w\\w+\\b")
            X = vectorizer.fit_transform(list(map(lambda post: ' '.join([post[2], post[3], post[6]]), posts)))
            r = pd.DataFrame(X.toarray(),columns=vectorizer.get_feature_names(), index=list(map(lambda p: p[0], posts)))
            print(key, 'done')

analyzer = Analyze()

analyzer.load()
analyzer.classification()
analyzer.doAnalyze()
