---
title: "pn 接合のビルトイン電位と空乏層幅"
date: 2026-11-27
draft: false
summary: "階段型 pn 接合のビルトイン電位と空乏層幅の式を整理し、Si の典型値で計算してみる。"
---

## 設定

p 型側のアクセプタ密度を $N_A$、n 型側のドナー密度を $N_D$ とする階段型(abrupt)の pn 接合を考えます。
不純物はすべてイオン化しているとし、真性キャリア密度を $n_i$、温度を $T$ とします。

## ビルトイン電位

熱平衡ではフェルミ準位が接合全体で一定になり、その結果として p 側と n 側の間に電位差が生じます。
これがビルトイン電位 $V_{bi}$ で、

$$
V_{bi} = \frac{k_B T}{q} \ln\!\left(\frac{N_A N_D}{n_i^2}\right)
$$

と表されます。$k_B T / q$ は熱電圧で、$T = 300\ \mathrm{K}$ では約 $25.9\ \mathrm{mV}$ です。

## 空乏層幅

空乏近似のもとでポアソン方程式を解くと、空乏層の全幅 $W$ は

$$
W = \sqrt{\frac{2 \varepsilon_s V_{bi}}{q} \left(\frac{1}{N_A} + \frac{1}{N_D}\right)}
$$

となります($\varepsilon_s$ は半導体の誘電率)。電荷中性条件 $N_A x_p = N_D x_n$ から、
n 側・p 側への広がりはそれぞれ

$$
x_n = W \frac{N_A}{N_A + N_D}, \qquad x_p = W \frac{N_D}{N_A + N_D}
$$

です。不純物密度の**低い側**に空乏層が大きく広がることがわかります。

## Si での計算例

$T = 300\ \mathrm{K}$、$n_i = 1.0 \times 10^{10}\ \mathrm{cm^{-3}}$、$\varepsilon_s = 11.7\,\varepsilon_0$ として、
$N_A = 10^{17}\ \mathrm{cm^{-3}}$、$N_D = 10^{16}\ \mathrm{cm^{-3}}$ の場合を計算します。

```python
import math

k_B = 1.380649e-23        # J/K
q = 1.602176634e-19       # C
eps0 = 8.8541878128e-14   # F/cm

T = 300.0
n_i = 1.0e10              # cm^-3
N_A, N_D = 1e17, 1e16     # cm^-3
eps_s = 11.7 * eps0

V_t = k_B * T / q
V_bi = V_t * math.log(N_A * N_D / n_i**2)
W = math.sqrt(2 * eps_s * V_bi / q * (1 / N_A + 1 / N_D))
x_n = W * N_A / (N_A + N_D)
x_p = W * N_D / (N_A + N_D)

print(f"V_bi = {V_bi:.3f} V")       # 0.774 V
print(f"W    = {W * 1e4:.3f} um")   # 0.332 um
print(f"x_n  = {x_n * 1e4:.3f} um") # 0.302 um
print(f"x_p  = {x_p * 1e4:.4f} um") # 0.0302 um
```

結果は $V_{bi} \approx 0.774\ \mathrm{V}$、$W \approx 0.332\ \mu\mathrm{m}$ で、
空乏層の約 9 割が不純物密度の低い n 側($x_n \approx 0.302\ \mu\mathrm{m}$)に広がっています。

## メモ

- $n_i$ の値は文献によって $1.0 \times 10^{10}$ や $9.65 \times 10^{9}\ \mathrm{cm^{-3}}$ などと少し異なり、$V_{bi}$ が数 mV 変わります。
- 逆バイアス $V_R$ をかけると、$W$ の式の $V_{bi}$ が $V_{bi} + V_R$ に置き換わります。
