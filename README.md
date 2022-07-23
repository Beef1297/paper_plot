# Paper Plot

- matplotlib や seaborn のメソッドのラッパー
- 論文に載せるグラフを簡単に作れるように作成．
    - 細かい設定を避けられるようにしたい
    - ただ，どうしても細かく調整したいところがでてくるので，そこをサポートできるようにしたい

- 基本的に，完成品を作るのではなく大枠をpythonなどで作成し，最終的にillustratorなどで細かい部分を詰める (フォントの種類やサイズ，ラベルの位置，線の太さ etc.) ようにするのがおすすめです

## 使い方

### python のインストール

- pythonをインストールしvenvを使って，仮想環境で作業することをおすすめします (condaでも大丈夫だと思います)．
  - Windowsでのインストールについて: https://www.python.jp/install/windows/install.html

- Windowsの場合は，下記のようなコマンドで環境を作ることができます．

```
py -m venv [環境の名前]
```

- あまり良くない方法だとは思いますが，ホームディレクトリに一つ普段使い用の仮想環境を作ってしまって，環境を毎回立ち上げるのが面倒なのでpowershellが起動するときにその環境を自動的にActivateするようにしています．
  - https://stackoverflow.com/questions/66293194/how-do-i-activate-a-python-venv-automatically-when-starting-powershell



### 依存ライブラリのインストール

- requirements.txt にあるライブラリをインストールすれば，動かせると思います
  - 動かせれば何でも大丈夫だと思いますが，jupyter (jupyterlab) を主に使ってグラフを作っています．

```
# jupyterlab
numpy
scikit-learn
scipy
seaborn
matplotlib
pandas
```

- jupyterlabについて
  - https://jupyter.org/
  - https://qiita.com/kirikei/items/a1639954ce5ccaf7ac3c
  - もしjupyterlabを使う場合は，いろいろ設定を修正することをおすすめします
  - 特に補完系があると便利です （僕はまだちゃんと動かせてないのですが）


## 使用例


```python
from paper_plot import paper_plot as pplt
import seaborn as sns

fmri = sns.load_dataset("fmri")
fig = pplt.initialize(font_family="Arial")
ax1 = pplt.create_new_axis(fig, 111)
pplt.scatter(ax1, fmri["timepoint"], fmri["signal"])
# pplt.bar(ax1, fmri["timepoint"], fmri["signal"])
pplt.set_axes_params(
    fig, ax1,xlabel="timepoint", ylabel="signal",
    ticklabelsize=15, **{"ylim": (-1.0, 1.0)})
pplt.display_process()
# pp.save("sample.png")
```

## [matplotlib のTips](Tips.md)

- 手が届かない範囲で，自分でいろいろ細かく調整する際の手がかりになればいいなと思い随時メモをしています．
