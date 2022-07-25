# -*- coding: utf-8 -*-
"""
- 実験結果を処理するためのクラス
- pandas で excel や csv ファイルを読み込み、データの種類や変形を行う

"""

import pandas as pd
import numpy as np
import pathlib
from typing import List, Tuple

EXCEL_SUFFIX = "xlsx"
CSV_SUFFIX = "csv"
class Data :
    def __repr__(self) :
        return str(self.df)
    
    def __str__(self) :
        return str(self.df)
    
    def __init__(self, path: str, xaxis: str = "condition", yaxis: str = "response", hue=None, col=None) :
        _path = pathlib.Path(path)
        if (not _path.exists()) :
            print("{} does not exist".format(path))
        
        suffix = _path.name.split('.')[-1] #末尾に拡張子があるとする
        print("this file's suffix is {}".format(suffix))
        
        self.df: pd.DataFrame = None
        if suffix == EXCEL_SUFFIX :
            print("load excel file")
            self.df = pd.read_excel(str(_path), index_col=None)
        elif suffix == CSV_SUFFIX :
            print("load csv file")
            self.df = pd.read_csv(str(_path), index_col=None)
            
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.hue = hue
        self.col = col


    def get_data(self) -> pd.DataFrame :
        return self.df

    def get_x_data(self) -> list:
        return self.df[self.xaxis]
    
    def get_y_data(self) -> list:
        return self.df[self.yaxis]
    
    def change_xy_axes(self) :
        axis = self.xaxis
        self.xaxis = self.yaxis
        self.yaxis = axis
        return

    def arrange_data_for_bar(self) :
        labels = self.get_x_labels()
        means = []
        std_d = []
        for l in labels :
            _d = list(self.df[self.df[self.xaxis] == l][self.yaxis])
            # print(_d)
            means.append(np.mean(_d))
            std_d.append(np.std(_d, ddof=1))
        print(labels)
        print(means)
        print(std_d)
        return (labels, means, std_d)
    
    def y_std_each_label(self) -> Tuple[list, list] :
        # label ごとの不偏標準偏差を計算する
        labels = self.get_x_labels()
        std_d = []
        for l in labels :
            _d = self.df[self.df[self.xaxis] == l][self.yaxis]
            std_d.append(np.std(list(_d), ddof=1))
        return (labels, std_d)
    
    def get_col_type(self, col: str = "condition") -> str :
        return str(self.df.dtypes[col])

    def get_xaxis_type(self) -> str :
        return self.get_col_type(self.xaxis)
    
    def get_yaxis_type(self) -> str :
        return self.get_col_type(self.yaxis)
    
    def get_x_max_min(self) -> tuple :
        return (min(self.df[self.xaxis]), max(self.df[self.xaxis]))
    
    def get_y_max_min(self) -> tuple :
        return (min(self.df[self.yaxis]), max(self.df[self.yaxis]))
    
    def get_x_labels(self) -> list:
        # x軸に該当する列の，データの種類のリストを返す
        # set() を使う方法もあるが，順番が保証されないので，避ける
        labels = []
        for e in self.df[self.xaxis] :
            if (e in labels) :
                continue
            labels.append(e)
        print("the x labels of the data: {}".format(labels))
        return labels
    
    def get_y_labels(self) -> list:
        labels = []
        for e in self.df[self.yaxis] :
            if (e in labels) :
                continue
            labels.append(e)
        print("the y labels of the data: {}".format(labels))
        return labels
        
    
if __name__ == '__main__' :
    d = Data("sample_data.xlsx")
    print(d)
    d.get_x_labels()
    d.get_y_labels()