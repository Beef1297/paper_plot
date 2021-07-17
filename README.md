# Paper Plot

- Work in Progress
- matplotlib や seaborn のメソッドのラッパー
- 論文に載せるグラフを簡単に作れるために細かい設定を避けるために作成

## props

- 各関数は辞書型配列を props として渡すことができます
- これによって，各グラフの細かいパラメータをカスタマイズ可能です
- 渡すことのできるパラメータについては各グラフのドキュメントに記載されている引数です
- 箱ひげ図 (boxplot)
    - https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html
- 棒グラフ (bar)
    - 

## Tips: matplotlib について理解する

- matplotlib 全体について理解を深める
    - https://qiita.com/skotaro/items/08dc0b8c5704c94eafb9
- rcParams の設定について
    - https://qiita.com/aurueps/items/d04a3bb127e2d6e6c21b
    
- ticker や locator の設定について
    - このサンプルが分かりやすいです
    - https://matplotlib.org/3.1.1/gallery/ticks_and_spines/tick-locators.html
- 軸ラベルを回転させたい
    - https://www.delftstack.com/ja/howto/matplotlib/how-to-rotate-x-axis-tick-label-text-in-matplotlib/

```python
# plt を使う場合
plt.xticks(rotation=XXX) or plt.yticks(rotation=XXX)
# axes を使う場合
ax.tick_params(axis='x', labelrotation=XXX)
ax.tick_params(axis='y', labelrotation=XXX)
```

