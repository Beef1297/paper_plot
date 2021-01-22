import os
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.image import BboxImage, imread
from matplotlib.transforms import Bbox, TransformedBbox
import matplotlib.font_manager as fm

# 散布図の中で単回帰分析する用
from sklearn import linear_model

class paper_plot :
    fig = None # コンストラクタで初期化される
    # WIP: フォントをもっと柔軟に選択できるようにする
    # フォントプロパティを渡すようにした方がいいかな
    fp_jp = fm.FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc', size=14)
    fp_en = fm.FontProperties(fname=r'C:\WINDOWS\Fonts\times.ttf', size=8)
    fp_b_century = fm.FontProperties(fname=r"C:\WINDOWS\Fonts\CENTURY.TTF", weight="bold")
    
    def __init__ (self, lang="en", figsize=(5, 5), style="seaborn-paper", **kwargs) :
        # matplotlib で利用できるフォントを利用 (日本語未対応)
        name, index = self.search_font_from_rcparams(font="Arial")
        plt.rcParams['font.family'] = plt.rcParams[name][index]
        
        # pdf で書き出した際にフォントが埋め込まれるようにする
        plt.rcParams["pdf.fonttype"] = 42 # TrueType
        
        # 大元のスタイルを変更して，細かい部分を調整
        plt.style.use(style)
        _props = {
            "axes.grid": True,
            "grid.linestyle": '-',
            "xtick.direction": 'in',
            "ytick.direction": 'in',
            "xtick.top": False,
            "ytick.right": False,
            "xtick.bottom": True,
            "ytick.left": True,
            "axes.linewidth": 1.0,
            "axes.axisbelow": True
        }
        custom_props = {**_props, **kwargs}
        # パラメータを更新
        plt.rcParams.update(**custom_props)
        self.fig = plt.figure(figsize=figsize)
        
        return

    def create_new_axis(self, id) :
        ax = self.fig.add_subplot(id)
        return ax
    
    # スタイルリストを表示 (詳しくはwebへ)
    def print_stylelist(self) :
        print("This is a list of available styles: {}".format(plt.style.available))
        return plt.style.available
    
    # 利用できるシステムフォントを表示
    def print_systemfontlist(self, keyword="gothic") :
        font_list = np.array(fm.findSystemFonts())
        extract = [path for path in font_list if re.match(".*{}.*".format(keyword), p)]
        print(extract)
        return extract
    
    # デフォルトで利用可能なフォントの中からkeywordと一致するものを検索
    def search_font_from_rcparams(self, font="Arial") :
        keys = ["font.cursive", "font.fantasy", "font.monospace",
                "font.sans-serif", "font.serif"]
        key = "font.sans-serif"
        index = 0
        
        for k in keys:
            for i, name in enumerate(plt.rcParams[k]):
                if re.match(".*{}.*".format(font), name):
                    key = k
                    index = i
                    break
        
        return (key, index)
    
    # 枠線やグリッド，フォントサイズ，locatorやtickerをプロットした後に調整する
    def set_axes_params(self, ax, ylabel="ylabel", xlabel="xlabel",
                        xmaj_ticker=None, xmin_ticker=None,
                        ymaj_ticker=None, ymin_ticker=None,
                        tick_label=None, xtickrotation=0, ticklabelsize=11,
                       **props) :
        
        ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
        if ymaj_ticker is not None:
            ax.yaxis.set_major_locator(ymaj_ticker)
        else:
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            
        if ymin_ticker is not None:
            ax.yaxis.set_minor_locator(ymin_ticker)
        else:
            ax.yaxis.set_minor_locator(ticker.AutoLocator())
            
        # TODO: ticker を渡すようにして設定できるようにする．
        ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
#         ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
#         ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        if xmin_ticker is not None:
            ax.xaxis.set_minor_locator(xmin_ticker)
        else:
            ax.xaxis.set_minor_locator(ticker.AutoLocator())

        if xmaj_ticker is not None:
            ax.xaxis.set_major_locator(xmaj_ticker)
            ax.set(xlim=(-1, 127))
            print((xmaj_ticker.tick_values(0, 127)))
        else:
            ax.xaxis.set_major_locator(ticker.AutoLocator())
        
        if tick_label:
            ax.set_xticklabels(labels=tick_label)
            
        # ticker がずれるときは手動で設定すると上手くいく時がある
#         ax.set_xticks(np.arange(xrange[0], xrange[1]+xrange[2], xrange[2]))
#         ax.set_yticks(np.arange(yrange[0], yrange[1]+yrange[2], yrange[2]))
#         ax.set_yticks(np.arange(yrange[0], yrange[1]+yrange[2], yrange[2]/2), minor=True)

        # label サイズとかは設定を分けたほうがいい
        ax.tick_params(axis='x', labelsize=ticklabelsize, width=0.5)
        ax.tick_params(axis='y', labelsize=ticklabelsize, width=0.5)
        ax.set_xlabel(xlabel, fontsize=18)
        ax.set_ylabel(ylabel, fontsize=18)
        
        # 余白の設定
        margin=[0.075, 0.95, 0.20, 1]
        self.fig.subplots_adjust(left=margin[0], right=margin[1], bottom=margin[2], top=margin[3])

#         plt.xticks(rotation=270)
        return
    

    def plot_data(self, ax, x, datas, labels=None, **props) :
        
        for i in range(0, len(datas)) :
            ax.plot(x, datas[i], label=labels[i])

        return
    
    # TODO: hatch の取り扱い (どうしても引数が多くなる)
    def fill_between(self, ax, x, upper_edge, lower_edge, hatch_fill=None, **props) :
        
        hatches = cycle(["/", "\\"])
        for i in range(0, len(datas)) :
            _default_props = {
                "alpha": 0.1
            }
            _p = {**_default_props, **props}
            if (hatch_fill) :
                _hatch = next(hatches)
                poly_collection = ax.fill_between(x, pse, mse, hatch=_hatch, **_p)
            else :
                ax.fill_between(x, pse, mse, **_p)
    
    # yerr を追加するようにすべきか
    def bar(self, ax, x_pos, y, sd=None, **props) :
        _default_props = {
            "width": 0.6,
            "linewidth": 0.5,
            "align": "center",
            "edgecolor": "black",
            "color": "white"
        }
        _props = {**_default_props, **props}
        ax.bar(x_pos, y, **_props)
        return

    def errorbar(self, ax, xpos, y, yerr, **props) :
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


    def scatter(self, ax, x, y, **props) :

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
    
    # データに対して回帰直線を引く関数. scatter との併用を想定
    # データは二次元配列で渡す
    # WIP: 現在は簡単にsklearnを利用した最小二乗法のみ
    def regression(self, ax, x, y, **props) :
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
        

    #横棒グラフ
    #現状, bar へのデータをそのまま横棒にできるようにしているのでおかしいコードになってる
    def barh(self, ax, x_pos, y, **props) :
        self.fig = plt.figure(figsize=(4.5, 6.5))
        color = {
            "black": [0.0, 0.0, 0.0, 1.0],
            "blue" : [0.2, 0.4, 0.8, 1.0]
        }

        _default_props = {
            "linewidth": 0.5,
            "align": "center",
            "color": color["blue"],
            "height": 0.5
        }
        
        ax.barh(x_pos, y, **props)
        return

    def boxplot(self, ax, tdata, pattern_label, **props) :

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
        ax.boxplot(tdata,
            #vert=False,
            #notch=True,
            #showfliers=False,
            **_p
        )

        return


    def display_process(self) :
        plt.show()
        plt.tight_layout()
        return
    
    def save(self, path) :
        if (os.path.isfile(path)) :
            raise(Exception("{} is already exist.".format(path)))
        self.fig.savefig(path, bbox_inches="tight", pad_inches=0.05, dpi=450)
        return

 