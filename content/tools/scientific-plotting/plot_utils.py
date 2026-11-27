"""実験データCSVからのMatplotlibグラフ作成で共通利用するヘルパー。"""

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

FIGSIZE = (6.4, 4.8)
DPI = 200


def read_column(csvfile: str, col: int) -> pd.DataFrame:
    """CSVから指定した1列（ヘッダなし）を読み込む。"""
    return pd.read_csv(csvfile, header=None, usecols=[col])


def new_figure() -> tuple[Figure, Axes]:
    """透明背景・単一軸の図を作成する。"""
    fig = plt.figure(
        figsize=FIGSIZE, dpi=DPI, facecolor="w", linewidth=0, edgecolor="w"
    )
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0)
    return fig, ax


def new_twinx_figure() -> tuple[Figure, Axes, Axes]:
    """透明背景・双方向Y軸（twinx）の図を作成する。"""
    fig, ax1 = plt.subplots(figsize=FIGSIZE, dpi=DPI, facecolor="w", edgecolor="w")
    ax1.patch.set_alpha(0)
    ax2 = ax1.twinx()
    return fig, ax1, ax2


def combine_twinx_legend(ax1: Axes, ax2: Axes, loc=2, borderaxespad: float = 0.0):
    """twinx で分かれた2軸の凡例を1つにまとめて ax1 に表示する。"""
    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(
        handler1 + handler2, label1 + label2, loc=loc, borderaxespad=borderaxespad
    )
