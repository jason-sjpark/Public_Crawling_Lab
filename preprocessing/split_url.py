import pandas as pd

origin = pd.read_csv('final_simple_stat.csv')
file1 = pd.DataFrame(columns=['title','date','n_reply','url'])
file2 = pd.DataFrame(columns=['title','date','n_reply','url'])
file3 = pd.DataFrame(columns=['title','date','n_reply','url'])

for i in range(len(origin)):
    if i%3 == 0:
        file1.loc[len(file1)] = origin.loc[i]
    elif i%3 == 1:
        file2.loc[len(file2)] = origin.loc[i]
    else:
        file3.loc[len(file3)] = origin.loc[i]

file1.to_csv('file1.csv')
file2.to_csv('file2.csv')
file3.to_csv('file3.csv')