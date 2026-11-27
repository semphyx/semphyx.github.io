"""科学誌向けの 2 パネル図(1 段幅 89 mm)を作る例:トランジスタの出力特性と伝達特性。

(a) 出力特性 I_D-V_D(ゲート電圧ごと)
(b) 伝達特性 I_D-V_G:左軸に log I_D、右の副軸に sqrt(I_D)

必要なもの: numpy, matplotlib と plot_style.py・plot_utils.py
(記事に載せている 2 ファイルを、このスクリプトと同じフォルダに置いて実行する)
実行すると figure1.pdf と figure1.png(600 dpi)を書き出す。
Python 3.10 以上、matplotlib 3.6 以上で動く。
"""
import numpy as np
from matplotlib import pyplot as plt

from plot_style import apply_style  # 記事の plot_style.py
from plot_utils import combine_twinx_legend  # 記事の plot_utils.py

MM = 1 / 25.4  # mm → インチ

# ---------------- データ:薄膜トランジスタ(n 型)の簡単なモデル ----------------
KB, Q = 1.380649e-23, 1.602176634e-19
VT = KB * 300 / Q            # 熱電圧 [V]
MU = 10.0                    # 移動度 [cm^2/Vs]
CI = 3.45e-8                 # ゲート絶縁膜の容量 [F/cm^2](SiO2 100 nm)
W_L = 10.0                   # チャネル幅 / チャネル長
VTH = 1.0                    # しきい値電圧 [V]
SS = 0.20                    # サブスレッショルドスイング [V/dec]
I_OFF = 1e-12                # オフ電流 [A]
LAM = 0.01                   # チャネル長変調 [1/V]
N_SUB = SS / (VT * np.log(10))


def v_eff(vg):
    """しきい値の前後をなめらかにつないだ実効ゲート電圧 [V]。"""
    s = 2 * N_SUB * VT
    return s * np.logaddexp(0.0, (vg - VTH) / s)


def drain_current(vg, vd):
    """線形領域から飽和領域までの I_D [A](二乗則 + チャネル長変調)。"""
    ve = v_eff(vg)
    vds = np.minimum(vd, ve)
    return MU * CI * W_L * (ve * vds - vds**2 / 2) * (1 + LAM * vd) + I_OFF


rng = np.random.default_rng(1)

# (a) 出力特性
vd = np.linspace(0, 10, 201)
vg_steps = [2, 4, 6, 8, 10]

# (b) 伝達特性(V_D = 10 V、飽和領域)。測定点を模擬して 2 % のばらつきを足す
VD_SAT = 10.0
vg = np.arange(-5.0, 10.01, 0.25)
id_meas = drain_current(vg, VD_SAT) * (1 + rng.normal(0, 0.02, vg.size))
sqrt_id = np.sqrt(id_meas)

# sqrt(I_D) の直線部分(V_G = 5〜10 V)を直線で近似し、横軸との交点からしきい値を求める
fit = vg >= 5.0
slope, icpt = np.polyfit(vg[fit], sqrt_id[fit], 1)
vth_ext = -icpt / slope
mu_sat = 2 * slope**2 / (CI * W_L)          # 飽和移動度 [cm^2/Vs]

# ---------------- スタイル ----------------
apply_style(tick_labelsize=7, major_size=3.0, major_width=0.6,
            minor_size=1.5, minor_width=0.5)   # 線は 0.5 pt 以上
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
    "font.size": 8,
    "axes.labelsize": 8,
    "legend.fontsize": 7,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.0,
    "lines.markersize": 3.0,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})
# savefig.bbox="tight" は使わない(余白が削られて図の幅が 89 mm より小さくなる)
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7"]
# 白黒印刷でも区別できるように、色に加えて線種と記号も系列ごとに変える
LINESTYLES = ["-", "--", "-.", ":", (0, (5, 1, 1, 1, 1, 1))]
MARKERS = ["o", "s", "^", "v", "D"]
C_LEFT, C_RIGHT = "#0072B2", "#D55E00"   # 主軸と副軸の色

# ---------------- 描画 ----------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(89 * MM, 100 * MM), layout="constrained")

# (a) 出力特性:ゲート電圧ごとに色・線種・記号を変える
for v, c, ls, mk in zip(vg_steps, OKABE_ITO, LINESTYLES, MARKERS, strict=True):
    ax1.plot(vd, drain_current(v, vd) * 1e6, color=c, linestyle=ls,
             marker=mk, markevery=(10, 25), markerfacecolor="none",
             markeredgewidth=0.7, label=f"{v} V")
ax1.set_xlabel(r"Drain voltage $V_D$ (V)")
ax1.set_ylabel(r"Drain current $I_D$ ($\mu$A)")
ax1.set_xlim(0, 10)
ax1.set_ylim(0, None)
ax1.legend(title=r"$V_G$", title_fontsize=7, loc="upper left",
           handlelength=1.5, borderaxespad=0.3)

# (b) 伝達特性:左軸 log I_D、右の副軸 sqrt(I_D)
ax2r = ax2.twinx()
# apply_style() は右辺にも目盛りを付けるので、主軸の右目盛りと副軸の左目盛りを消す
ax2.tick_params(axis="y", which="both", right=False)
ax2r.tick_params(axis="y", which="both", left=False, right=True)

ax2.semilogy(vg, id_meas, "o", color=C_LEFT, markerfacecolor="none",
             markeredgewidth=0.7, label=r"$I_D$")
ax2r.plot(vg, sqrt_id * 1e3, "s", color=C_RIGHT, markerfacecolor="none",
          markeredgewidth=0.7, label=r"$\sqrt{I_D}$")
v_line = np.linspace(vth_ext, 10, 20)
ax2r.plot(v_line, (slope * v_line + icpt) * 1e3, "--", color=C_RIGHT,
          linewidth=0.8, label="Linear fit")

ax2.set_xlabel(r"Gate voltage $V_G$ (V)")
ax2.set_ylabel(r"$I_D$ (A)", color=C_LEFT)
ax2r.set_ylabel(r"$\sqrt{I_D}$ (10$^{-3}$ A$^{1/2}$)", color=C_RIGHT)
ax2.tick_params(axis="y", colors=C_LEFT)       # 軸の色を系列の色にそろえる
ax2r.tick_params(axis="y", colors=C_RIGHT)
ax2r.spines["left"].set_color(C_LEFT)
ax2r.spines["right"].set_color(C_RIGHT)
ax2.set_xlim(-5, 10)
ax2.set_ylim(1e-13, 1e-2)
ax2r.set_ylim(0, sqrt_id.max() * 1e3 * 1.1)

# 測定条件(ドレイン電圧とソース電圧)を書き込む
ax2.text(0.97, 0.05, r"$V_D$ = 10 V, $V_S$ = 0 V", transform=ax2.transAxes,
         ha="right", va="bottom", fontsize=7)

# しきい値電圧(外挿)を示す
ax2r.annotate(rf"$V_{{th}}$ = {vth_ext:.2f} V", xy=(vth_ext, 0),
              xytext=(vth_ext - 4.2, 2.6), fontsize=7, color=C_RIGHT,
              arrowprops={"arrowstyle": "->", "color": C_RIGHT, "lw": 0.6})

# 主軸と副軸の凡例を 1 つにまとめる(plot_utils.combine_twinx_legend)
combine_twinx_legend(ax2, ax2r, loc="upper left", borderaxespad=0.3)

for ax, tag in [(ax1, "(a)"), (ax2, "(b)")]:
    ax.text(-0.17, 1.03, tag, transform=ax.transAxes,
            fontsize=9, fontweight="bold", va="bottom")

fig.savefig("figure1.pdf")
fig.savefig("figure1.png", dpi=600)
print(f"V_th (extrapolated) = {vth_ext:.2f} V, mu_sat = {mu_sat:.1f} cm^2/Vs")
