#  from apyori import apriori
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#  讀取 top 10
with open('./H01L_21_abstract_top10.csv','r') as fp:
    top10s = fp.read().splitlines()
    data = []
    #  data = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           #  ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
           #  ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
           #  ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
           #  ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]
    for i in top10s[1:]:
        data.append(list(filter(lambda w: w != '---', i.split(',')[1:])))

    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df, min_support=0.16, use_colnames=True, max_len=2)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    #  frequent_itemsets = frequent_itemsets[ frequent_itemsets['length'] == 2 ]
    result = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.1)
    #  print(result)
    result.to_csv('./test.csv')

    #  for item in association_results:
        #  pair = item[0] 
        #  items = [x for x in pair]
        #  print("Rule: " + items[0] + " -> " + items[1])
        #  print("Support: " + str(item[1]))
        #  print("Confidence: " + str(item[2][0][2]))
        #  print("Lift: " + str(item[2][0][3]))
        #  print("=====================================")
