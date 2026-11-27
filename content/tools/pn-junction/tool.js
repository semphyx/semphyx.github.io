// pn 接合の計算機(階段型接合・空乏近似)
(function () {
  var root = document.getElementById("pn-tool");
  if (!root) return;
  var form = root.querySelector("form");
  var out = function (k) { return root.querySelector('[data-out="' + k + '"]'); };

  var KB = 1.380649e-23;        // J/K
  var Q = 1.602176634e-19;      // C
  var EPS0 = 8.8541878128e-14;  // F/cm
  // 300 K での代表値
  var MATERIALS = {
    si:   { ni: "1.0e10", er: "11.7" },
    ge:   { ni: "2.0e13", er: "16.0" },
    gaas: { ni: "2.1e6",  er: "12.9" }
  };

  var num = function (name) { return Number(String(form.elements[name].value).trim()); };
  var fmtLen = function (cm) {
    var um = cm * 1e4;
    return um >= 0.1 ? um.toPrecision(3) + " μm" : (um * 1000).toPrecision(3) + " nm";
  };

  function calc() {
    var na = num("na"), nd = num("nd"), t = num("t"), ni = num("ni"), er = num("er"), vr = num("vr");
    var err = out("error");
    var bad = [na, nd, t, ni, er].some(function (v) { return !(v > 0); }) || !isFinite(vr);
    var vbi = (KB * t / Q) * Math.log(na * nd / (ni * ni));
    if (!bad && !(vbi > 0)) bad = "N_A·N_D が n_i² より大きくなるように入力してください。";
    if (!bad && vbi + vr <= 0) bad = "順バイアスが V_bi を超えています(V_R > −V_bi にしてください)。";
    if (bad) {
      ["vbi", "w", "xn", "xp", "emax"].forEach(function (k) { out(k).textContent = "–"; });
      err.textContent = typeof bad === "string" ? bad : "正の数を入力してください。";
      err.hidden = false;
      return;
    }
    err.hidden = true;
    var eps = er * EPS0;
    var w = Math.sqrt(2 * eps * (vbi + vr) / Q * (1 / na + 1 / nd));
    var xn = w * na / (na + nd), xp = w * nd / (na + nd);
    var emax = Q * nd * xn / eps;  // V/cm
    out("vbi").textContent = vbi.toFixed(3) + " V";
    out("w").textContent = fmtLen(w);
    out("xn").textContent = fmtLen(xn);
    out("xp").textContent = fmtLen(xp);
    out("emax").textContent = (emax / 1000).toPrecision(3) + " kV/cm";
  }

  form.elements.material.addEventListener("change", function () {
    var m = MATERIALS[form.elements.material.value];
    form.elements.ni.value = m.ni;
    form.elements.er.value = m.er;
    calc();
  });
  form.addEventListener("input", calc);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  calc();
})();
