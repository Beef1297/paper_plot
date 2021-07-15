# Paper Plot

- Work in Progress
- matplotlib や seaborn のメソッドのラッパー
- 論文に載せるグラフを簡単に作れるために細かい設定を避けるために作成


## 対応している (する予定) グラフ

### plot_data | 線グラフ

- データを直線でつないでプロットする
- plt.plot に対応

### fill_between | 標準偏差などを塗って表現する

- 線グラフに対して標準偏差や誤差などを線の背景の領域を塗って表現する
- plt.fill_between を利用

### bar | 棒グラフ

- 棒グラフ

### barh | 横棒グラフ

- 横棒グラフ (棒グラフと統合可能か)

### errorbar

- エラーバーをプロットする
- 棒グラフを作る際に設定可能ですが，別途用意しました

### scatter | 散布図

### regression | 回帰直線を引く

- scatter との併用を想定

### boxplot | 箱ひげ図