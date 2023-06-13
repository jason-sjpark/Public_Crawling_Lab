import json
import pandas as pd

with open('18.json', encoding='utf-8-sig') as f:
    news = json.loads(f.read())  ## json 라이브러리 이용

#news의 댓글 dict, 0번 유저의 댓글 기록, 이 댓글기록 dict를 dataframe으로 변환
ls_dic_reply_history = news['dic_reply'][0]['dic_history']['dic_reply_history']
df_dic_reply_history = pd.DataFrame(ls_dic_reply_history)
print(df_dic_reply_history)

