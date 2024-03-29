# -*- coding: utf-8 -*-
"""a wrapper for matplotlib to make figures for paper

Todo:
    * improve the way to set font and axis parameters
    * refactor methods

"""

# データ処理に使うライブラリ
import os
import numpy as np
import re
from sklearn import linear_model # 散布図の中で単回帰分析する用
import pandas as pd
from typing import Tuple

# 描画系のライブラリ
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# from matplotlib.image import BboxImage, imread
# from matplotlib.transforms import Bbox, TransformedBbox
import matplotlib.font_manager as fm

def initialize(figsize: Tuple[int, int] = (5, 5), font_family: str = "Arial", style: str = "seaborn-paper", **kwargs) -> matplotlib.pyplot.figure: 
    """全般的な設定を行う関数
        * フォントの設定: 細かくフォントを設定するのは大変なので日本語か，英語フォントを適当に設定しイラレなどで修正する方針
        * pdf.fonttype の設定
        * tick や grid などの設定
        * fig を返す
    """
    plt.rcParams["font.family"] = font_family

    # pdf で書き出した際にフォントが埋め込まれるようにする
    plt.rcParams["pdf.fonttype"] = 42 # TrueType

    # 大元のスタイルを変更して，細かい部分を調整
    plt.style.use(style)
    _props = {
        "axes.grid": True, # グラフのグリッド線の表示
        "grid.linestyle": '-', # グリッドの線のスタイル
        "grid.color": "0.8", # 0~1.0 の数値を文字列として渡すとグレースケールとして設定可能
        "xtick.direction": 'in', # x軸の tick (目盛り) の方向をグラフの内側に 'out' にすると外側
        "ytick.direction": 'in', # y軸の tick の方向を内側に
        "xtick.top": False, # 上側の目盛りは表示しない
        "ytick.right": False, # 右側の目盛りは表示しない
        "xtick.bottom": True, # 下側の目盛りを表示する
        "ytick.left": True, # 左側の目盛りを表示する
        "xtick.major.size": 7.0,
        "xtick.minor.size": 4.0,
        "ytick.major.size": 7.0,
        "ytick.minor.size": 4.0,
        "axes.linewidth": 1.0, # グラフの枠線の太さ
        "axes.edgecolor": "0.3", # 0~1.0 の数値を文字列として渡すとグレースケールとして設定可能
        "axes.axisbelow": True # axis と tick の表示順について (True: 両方とも他の要素の下に)
    }
    custom_props = {**_props, **kwargs}
    # パラメータを更新
    plt.rcParams.update(**custom_props)
    fig = plt.figure(figsize=figsize)

    return fig

def create_new_axis(fig: plt.figure, id: int) -> matplotlib.axes.SubplotBase :
    """新しいaxisを作成する関数
    """
    ax = fig.add_subplot(id)
    return ax

def add_new_axis(fig: plt.figure, rect:Tuple[float, float, float, float]) -> matplotlib.axes.SubplotBase :
    ax = fig.add_axes(rect)
    return ax

def check_setting_matplotlib(key: str) :
    params = plt.rcParams
    print("check parameters (rcParams) including '{}' ------".format(key))
    for k, v in params.items() :
        if re.search(key, k) :
            print("{0}: {1}".format(k, v))
    
            

def print_stylelist() -> list:
    """デフォルトで利用可能なグラフのスタイルリストを表示する
    * 詳しくは web へ
    """
    print("This is a list of available styles: {}".format(plt.style.available))
    return plt.style.available

def print_example_fonts() :
    print(
        """
examples of available fonts 
(English) Times New Roman, Arial
Windows (Japanese): Yu Gothic, Yu Mincho
Mac (Japanese): Hiragino Maru Gothic Pro, Hiragino Mincho ProN
        """
    )

def search_systemfont_list(keyword="gothic") -> list:
    """利用可能なシステムフォントのパスを返す
    * 全て表示すると可視性が悪いので，キーワードとマッチしたものを返す
    """
    font_list = np.array(fm.findSystemFonts())
    extract = [path for path in font_list if re.match(".*{}.*".format(keyword), p)]
    print(extract)
    return extract

def search_font_from_matplotlib(font: str ="Arial") -> list :
    """matplotlib から設定可能なフォントの名前を返す
    * システムフォントではなく matplotlib rcParams にあるフォントから探索
    * rcparams のkey と index を返す
    """
    font_list = fm.get_fontconfig_fonts()
    names = [fm.FontProperties(fname=fname).get_name() for fname in font_list]
    match_names = []
    for i, name in enumerate(names):
        if re.match(".*{}.*".format(font), name):
            match_names.append(name)

    return match_names


def set_axes_params(fig: plt.figure, ax: matplotlib.axes.SubplotBase,
                    ylabel: str = "ylabel", xlabel: str = "xlabel",
                    xmajtick_num: int = None, ymajtick_num: int = None,
                    xmintick_num: int = None, ymintick_num: int = None,
                    xmaj_ticker: matplotlib.ticker.Locator = None,
                    xmin_ticker: matplotlib.ticker.Locator = None,
                    ymaj_ticker: matplotlib.ticker.Locator = None,
                    ymin_ticker: matplotlib.ticker.Locator = None,
                    xtick_label: str = None, ytick_label: str = None,
                    ticklabelsize: int = 11, labelsize: int = 18,
                   **props) :
    """軸の設定を行う関数
    * 枠線やグリッド，フォントサイズ，locatorやtickerをプロットした後に調整する
    """
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    if ymaj_ticker is not None:
        ax.yaxis.set_major_locator(ymaj_ticker)
    else:
        ax.yaxis.set_major_locator(ticker.AutoLocator())

    if ymin_ticker is not None:
        ax.yaxis.set_minor_locator(ymin_ticker)
    else:
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # TODO: ticker を渡すようにして設定できるようにする．
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
#         ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
#         ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    if xmin_ticker is not None:
        ax.xaxis.set_minor_locator(xmin_ticker)
    else:
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

    if xmaj_ticker is not None:
        ax.xaxis.set_major_locator(xmaj_ticker)
    else:
        ax.xaxis.set_major_locator(ticker.AutoLocator())

    if xtick_label:
        ax.xaxis.set_major_locator(ticker.FixedLocator(xtick_label))
#         ax.xaxis.set_major_locator(ticker.MaxNLocator(len(xtick_label)))
    if ytick_label:
        ax.yaxis.set_major_locator(ticker.FixedLocator(ytick_label))
#         ax.yaxis.set_major_locator(ticker.MaxNLocator(len(ytick_label)))

    if xmajtick_num:
        ax.xaxis.set_major_locator(ticker.LinearLocator(xmajtick_num))
    if ymajtick_num:
        ax.yaxis.set_major_locator(ticker.LinearLocator(ymajtick_num))
    
    if xmintick_num:
        ax.xaxis.set_minor_locator(ticker.LinearLocator(xmintick_num))
    if ymintick_num:
        ax.yaxis.set_minor_locator(ticker.LinearLocator(ymintick_num))

    # ticker がずれるときは手動で設定すると上手くいく時がある
#         ax.set_xticks(np.arange(xrange[0], xrange[1]+xrange[2], xrange[2]))
#         ax.set_yticks(np.arange(yrange[0], yrange[1]+yrange[2], yrange[2]))
#         ax.set_yticks(np.arange(yrange[0], yrange[1]+yrange[2], yrange[2]/2), minor=True)

    # TODO: label サイズとかは設定を分けたほうがいい
    ax.tick_params(axis='x', labelsize=ticklabelsize, width=0.5)
    ax.tick_params(axis='y', labelsize=ticklabelsize, width=0.5)
    ax.set_xlabel(xlabel, fontsize=labelsize)
    ax.set_ylabel(ylabel, fontsize=labelsize)
    ax.set(**props)

    # 余白の設定
    margin=[0.075, 0.95, 0.20, 1]
    fig.subplots_adjust(left=margin[0], right=margin[1], bottom=margin[2], top=margin[3])

    return


def plot_data(ax: matplotlib.axes.SubplotBase, x: list, datas: list, labels: list = None, **props) :
    """データを直線でプロットしていく関数
    """
    for i in range(0, len(datas)) :
        ax.plot(x, datas[i], label=labels[i])

    return

# TODO: hatch の取り扱い (どうしても引数が多くなる)
def fill_between(ax: matplotlib.axes.SubplotBase, x: list, upper_edge: list, lower_edge: list, hatch_fill: bool = None, **props) :
    """指定領域を塗りつぶす関数
    """
    hatches = cycle(["/", "\\"])
    for i in range(0, len(datas)) :
        _default_props = {
            "alpha": 0.1
        }
        _p = {**_default_props, **props}
        if (hatch_fill) :
            _hatch = next(hatches)
            poly_collection = ax.fill_between(x, upper_edge, lower_edge, hatch=_hatch, **_p)
        else :
            ax.fill_between(x, upper_edge, lower_edge, **_p)

def bar(ax: matplotlib.axes.SubplotBase, x_pos: list, y: list, sd: list = None, vertical: bool = True, **props) :
    """棒グラフをプロットする関数
    エラーバーも設定できるようにすべきか
    縦棒グラフの幅を設定する時は "width", 横棒グラフの幅を設定する時は "height"
    の設定を props で渡す
    """

    _default_props = {
        "width": 0.6,
        "linewidth": 0.5,
        "align": "center",
        "edgecolor": "black",
        "color": "white"
    }
    _props = {**_default_props, **props}
    
    if (vertical) :
        ax.bar(x_pos, y, **_props)
    else :
        ax.barh(x_pos, y, **props)
    return

def errorbar(ax: matplotlib.axes.SubplotBase, xpos: list, y: list, yerr: list, **props) :
    """エラーバーを別途プロットする関数
    x, y座標が必要になるので二度手間ではある
    """
    _default_props = {
        "fmt": "none",
        "elinewidth": 0.5,
        "capsize": 2,
        "capthick": 0.75,
        "ecolor": "lightsteelblue",
        "alpha": 0.85
    }
    _p = {**_default_props, **props}
    ax.errorbar(x_pos, y, yerr=sd, **_p)


def scatter(ax: matplotlib.axes.SubplotBase, x: list, y: list, **props) :
    """散布図をプロットする関数
    color や marker の候補を記載しておく
    """
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#ab1225', '#ccaabb']
    markers = ['o', # circle
               'v', # triangle_down
               '^', # triangle_up
               '<', # triangle_left
               '>', # triangle_right
               'x', # x
               '*', # star
               'h', # hexagon1
               's', # square
               'd', # thin_diamond
               'H', # hexagon2
               ]

    _default_props = {
        "s": 20,
        "c": colors[0],
        "marker": "o",
        "alpha": 0.5
    }
    _p = {**_default_props, **props}
    ax.scatter(x, y, **_p)

    return

def regression(ax: matplotlib.axes.SubplotBase, x: list, y: list, **props) :
    """回帰直線をプロットする関数
    # データに対して回帰直線を引く関数. scatter との併用を想定
    # データは二次元配列で渡す
    # WIP: 現在は簡単にsklearnを利用した最小二乗法のみ
    """
    # 念のために ndarrayに変換 (型の統一)
    X = np.array(x, dtype=float)
    if (X.ndim <= 1) :
        print("X array was 1D and shape is changed by X.reshape(-1, 1)")
        X = X.reshape(-1, 1)
    Y = np.array(y, dtype=float)
    if (Y.ndim <= 1) :
        print("Y array was 1D and shape is changed by Y.reshape(-1, 1)")
        Y = Y.reshape(-1, 1)
    reg = linear_model.LinearRegression().fit(X, Y)

    _default_props = {
        "linestyle": "--",
        "color": '#1f77b4',
        "linewidth": 1.5,
    }
    _p = {**_default_props, **props}
    ax.plot(X, reg.predict(X), **_p)
    return

def boxplot(ax: matplotlib.axes.SubplotBase, tdata: list, pattern_label=None, **props) :
    """箱ひげ図をプロットする関数
    meanpointprops: 平均値を表す点のプロパティ
    meanlineprops: 平均値を線で表す時のプロパティ
    flierprops: 外れ値のプロパティ
    パラメータ例:
    notch (default: False): 箱にノッチを表示する
    vert (default: True): デフォルトでTrue, Falseの場合横にプロットされる
    showfliers (default: True): 外れ値を表示するかどうか
    """
    _linewidth = 3.0
#     flierprops = dict(marker="x", markeredgecolor="black", alpha=0.5)
    meanpointprops = dict(marker='D', markerfacecolor="tab:orange", 
                          markeredgecolor="black", alpha=1.0, linewidth=0.1,
                          markersize=4)

    meanlineprops = dict(linestyle="-", linewidth=2.0, color="tab:orange")
    _default_props = dict(
                boxprops=dict(linewidth=_linewidth-2),
                medianprops=dict(color="green", linewidth=_linewidth),
                flierprops = dict(marker="x", linewidth=_linewidth/3.0, 
                                  markeredgecolor='0.3'),
                meanprops = meanpointprops,
                whiskerprops=dict(linewidth=_linewidth-2), #ひげの部分
                capprops=dict(linewidth=_linewidth-2) #最小値，最大値の部分
            )

    _p = {**_default_props, **props}
    ax.boxplot(tdata,**_p)

    return


def display_process() :
    """グラフを表示する処理
    難しいことはしていないが，tight_layout() を呼ぶようにしている
    jupyter を利用する場合は利用しなくてもグラフを表示可能
    """
    plt.show()
    plt.tight_layout()
    return

def save(fig: plt.figure, path: str, dpi: int = 450) :
    """グラフを保存する処理
    重複の確認を行い，上書きを防止する
    """
    if (os.path.isfile(path)) :
        raise(Exception("{} is already exist.".format(path)))
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, dpi=dpi)
    return

