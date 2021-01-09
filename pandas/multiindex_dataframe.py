import os
import pandas as pd
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv('./test.csv', header=0, encoding='utf-8')
df['date'] = pd.to_datetime(df['date'])
df['col_3'] = df['col_1'] * df['col_2']
print(df)

df = df.set_index(['date'])
print(df[df.index.day==15])

# df = df.reset_index().set_index(['date', 'id'])
# print(df[df.index.day==15])
# Attribute error: 'MultiIndex' object has no attribute 'day'

# MultiIndex Dataframe
df = df.reset_index()
df = df.set_index(['date'])
df = df.set_index([df.index.year, df.index.month, df.index.day, df.index, 'id'])
df.index.names = ['year', 'month', 'day', 'date', 'id']
df.sort_index()
print(df)

# sort
df_sorted = df.sort_index(level=['day', 'month'])
print(df_sorted)

# tuple
series_col1_tuple = df.loc[(2021, 1), 'col_3']
print(series_col1_tuple)
print(type(series_col1_tuple))

# xs
series_col1_xs = df.xs(2021, level='year').xs(1, level='month')['col_3']
print(type(series_col1_xs))

# histogram
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

for i, month in enumerate(df.reset_index()['month'].unique()):
    ax[i].set_title(str(month))
    pd.cut(
        # 2021年の月ごとに、col_3をヒストグラムで表示
        df.xs(2021, level='year').xs(month, level='month').reset_index()['col_3'],
        bins=3,     # 階級数
        right=False # True: aより大きくb以下; False: a以上b未満
    ) \
    .value_counts() \
    .sort_index() \
    .plot.bar(color='indigo', ax=ax[i], sharex=True, sharey=True)
plt.show()

# boxplot
df.reset_index().boxplot(
    column='col_3',
    by='month',
    figsize=(10, 5),
    meanline=True,
    showmeans=True,
    showcaps=True,
    showbox=True,
    showfliers=False
)
