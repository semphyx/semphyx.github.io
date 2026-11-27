"""論文用グラフの共通Matplotlibスタイル設定。

複数のグラフ描画スクリプトで重複しがちな rcParams 設定をまとめたもの。
スクリプトごとに微妙に異なる目盛り線サイズ・ラベルサイズは引数で指定する。
"""

from matplotlib import pyplot as plt


def apply_style(
    tick_labelsize: int | None = 12,
    major_size: float = 4.0,
    major_width: float = 1.0,
    minor_size: float = 2.0,
    minor_width: float = 0.6,
) -> None:
    """論文用グラフの共通rcParamsを適用する。

    tick_labelsize=None の場合は xtick/ytick.labelsize を変更しない
    （元々未設定のスクリプトの挙動を保ちたい場合に使う）。
    """
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 12
    if tick_labelsize is not None:
        plt.rcParams["xtick.labelsize"] = tick_labelsize
        plt.rcParams["ytick.labelsize"] = tick_labelsize
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["axes.linewidth"] = 1.0
    plt.rcParams["xtick.top"] = True
    plt.rcParams["xtick.bottom"] = True
    plt.rcParams["ytick.left"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["xtick.minor.visible"] = True
    plt.rcParams["ytick.minor.visible"] = True
    plt.rcParams["xtick.major.size"] = major_size
    plt.rcParams["ytick.major.size"] = major_size
    plt.rcParams["xtick.major.width"] = major_width
    plt.rcParams["ytick.major.width"] = major_width
    plt.rcParams["xtick.minor.size"] = minor_size
    plt.rcParams["ytick.minor.size"] = minor_size
    plt.rcParams["xtick.minor.width"] = minor_width
    plt.rcParams["ytick.minor.width"] = minor_width
