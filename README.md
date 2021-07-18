# Paper Plot (WIP)

- matplotlib や seaborn のメソッドのラッパー
- 論文に載せるグラフを簡単に作れるために細かい設定を避けるために作成
    - できる限り簡単な設定で調節できるようにしたい



## props

- 各関数は辞書型配列を props として渡すことができます
- これによって，各グラフの細かいパラメータをカスタマイズ可能です
- 渡すことのできるパラメータについては各グラフのドキュメントに記載されている引数です
- 箱ひげ図 (boxplot)
    - https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html
- 棒グラフ (bar)
    - barh: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barh.html#matplotlib.pyplot.barh
    - bar: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar
- 散布図 (scatter)
    - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html

- axes の設定
    - set_axes_parameters では ticker や locator, label を設定します
    - **props は ax.set() に渡しています
    - https://matplotlib.org/stable/api/axes_api.html
    - ドキュメントにある **kwargs にあるものを設定可能です
- 基本的に axes の設定ドキュメントにあるプロパティ
    - https://matplotlib.org/stable/api/axes_api.html
- labelなどのテキストの設定は matplotlib.text() に使えるパラメータが設定可能です
    - https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text

## Tips: フォント設定について

- matplotlib にフォントを追加したい
    - https://ricrowl.hatenablog.com/entry/2020/09/14/032424

## Tips: スタイルについて

- 細かい調整をせずにデフォルトのスタイルを変更することで見た目を変更可能です
    - https://qiita.com/eriksoon/items/b93030ba4dc686ecfbba
    - https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html

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
or
ax.set_xticklabels(xticklabels, rotation=XXX) # labelを必ず渡す必要がある
ax.set_yticklabels(yticklabels, rotation=XXX) # labelを必ず渡す必要がある
```

