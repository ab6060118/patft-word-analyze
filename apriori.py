import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#  pd.set_option('display.max_rows', None)
#  pd.set_option('display.max_columns', None)
#  讀取 top 10
with open('./H01L_21_abstract_top10.csv','r') as fp:
    top10s = fp.read().splitlines()
    data = []
    for i in top10s[1:]:
        data.append(list(filter(lambda w: w != '---', i.split(',')[1:])))

    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True, max_len=2)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    result = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.1)
    result['A'] = result['antecedents'].apply(lambda x: next(iter(x)))
    result['B'] = result['consequents'].apply(lambda x: next(iter(x)))
    result = result[['confidence', 'A', 'B']].sort_values(by=['confidence'], ascending=False)
    result.to_csv('./apriori.csv', index=False)
