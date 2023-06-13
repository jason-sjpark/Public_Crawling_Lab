from pandas import Series, DataFrame
import pandas as pd
from pivottablejs import pivot_ui
from pandasgui import show
raw_data = {'col0': [1, 2, 3, 4],
            'col1': [10, 20, 30, 40],
            'col2': [100, 200, 300, 400]}
data = DataFrame(raw_data)
data2 = pd.DataFrame({'idx':[1],'dfs2':[data]})
# dic = dict(a=data)
# raw2 = {'d' : dic}
# df = DataFrame(raw2)
# print(df)
# print('\n')
# print(df['d'])
# print('\n')
# print(df['d']['a'])
#


df = pd.DataFrame({'idx':[1], 'dfs':[data2]})
print(df.loc[0]['dfs'].loc[0]['dfs2']['col0'])



print(df)
show(data)
# for news in ls_news:
#     for reply in ls_reply:
#         for pre_reply in ls_pre_reply: