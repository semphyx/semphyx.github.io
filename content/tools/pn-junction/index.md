---
title: "pn 接合の計算機"
summary: "不純物密度と温度から、ビルトイン電位・空乏層幅・最大電界を計算する。"
weight: 1
tags: ["pn接合", "空乏層"]
---

階段型 pn 接合について、空乏近似で
$V_{bi} = \frac{k_B T}{q}\ln\frac{N_A N_D}{n_i^2}$、
$W = \sqrt{\frac{2\varepsilon_s (V_{bi}+V_R)}{q}\left(\frac{1}{N_A}+\frac{1}{N_D}\right)}$
を計算します。式の導出は[ノート]({{< relref "/notes/semiconductor/pn-junction-built-in-potential" >}})を参照してください。

<div class="tool-panel" id="pn-tool">
  <form class="tool-form" autocomplete="off">
    <label><span>材料</span>
      <select name="material">
        <option value="si">Si(シリコン)</option>
        <option value="ge">Ge(ゲルマニウム)</option>
        <option value="gaas">GaAs(ヒ化ガリウム)</option>
      </select>
    </label>
    <label><span>アクセプタ密度 N<sub>A</sub> [cm⁻³]</span><input name="na" value="1e17" inputmode="decimal"></label>
    <label><span>ドナー密度 N<sub>D</sub> [cm⁻³]</span><input name="nd" value="1e16" inputmode="decimal"></label>
    <label><span>温度 T [K]</span><input name="t" value="300" inputmode="decimal"></label>
    <label><span>真性キャリア密度 n<sub>i</sub> [cm⁻³]</span><input name="ni" value="1.0e10" inputmode="decimal"></label>
    <label><span>比誘電率 ε<sub>r</sub></span><input name="er" value="11.7" inputmode="decimal"></label>
    <label><span>逆バイアス V<sub>R</sub> [V]</span><input name="vr" value="0" inputmode="decimal"></label>
  </form>
  <div class="tool-result" aria-live="polite">
    <table>
      <tbody>
        <tr><th>ビルトイン電位 V<sub>bi</sub></th><td data-out="vbi">–</td></tr>
        <tr><th>空乏層幅 W</th><td data-out="w">–</td></tr>
        <tr><th>n 側の広がり x<sub>n</sub></th><td data-out="xn">–</td></tr>
        <tr><th>p 側の広がり x<sub>p</sub></th><td data-out="xp">–</td></tr>
        <tr><th>最大電界 E<sub>max</sub></th><td data-out="emax">–</td></tr>
      </tbody>
    </table>
    <p class="tool-error" data-out="error" hidden></p>
  </div>
</div>

> [!NOTE]
> 材料を選ぶと、300 K での $n_i$ と $\varepsilon_r$ が入ります。温度を変えても $n_i$ は自動では変わらないので、必要なら $n_i$ も書き換えてください。数値は `1e16` や `2.5e17` のように入力できます。
