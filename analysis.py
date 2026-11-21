import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#↑cmd で pip install seaborn を実行しておくこと
from sklearn.datasets import load_iris
#データ読み込み
#CSV
df = pd.read_csv('C:\\Users\\ara05\\Music\\python\\6-1116\\iris.csv')

#データの大雑把な確認
#最初の数行
print(df.head())
print(df.columns)
#ランダムに 5 行表示
print(df.sample(n=5))
#基本統計量の確認＜平均、中央値、標準偏差等＞
print(df.describe())
#ヒストグラムで可視化
#df['カラム名'].hist()
plt.figure(1)
df["sepal_length"].hist()


#sns.scatterplot(x='カラム名', y='カラム名', data=df) 種類ごとに表示
plt.figure(2)
for species, group in df.groupby("species"):
    plt.scatter(
        group["sepal_length"],
        group["sepal_width"],
        label=species
    )

plt.xlabel("sepal length (cm)")
plt.ylabel("sepal width (cm)")
plt.legend(title="species")


#相関行列を表示
numeric_df = df.select_dtypes(include=np.number)
correlation_matrix = numeric_df.corr()
print(correlation_matrix)
plt.show()
