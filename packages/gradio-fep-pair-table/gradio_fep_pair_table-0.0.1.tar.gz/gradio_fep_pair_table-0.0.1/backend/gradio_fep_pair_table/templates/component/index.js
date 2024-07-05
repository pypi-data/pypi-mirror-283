const {
  SvelteComponent: et,
  assign: tt,
  create_slot: it,
  detach: nt,
  element: rt,
  get_all_dirty_from_scope: at,
  get_slot_changes: st,
  get_spread_update: ot,
  init: lt,
  insert: ct,
  safe_not_equal: dt,
  set_dynamic_element_data: Ce,
  set_style: U,
  toggle_class: q,
  transition_in: Xe,
  transition_out: We,
  update_slot_base: ft
} = window.__gradio__svelte__internal;
function ut(i) {
  let e, t, n;
  const r = (
    /*#slots*/
    i[18].default
  ), a = it(
    r,
    i,
    /*$$scope*/
    i[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      i[7]
    ) },
    { id: (
      /*elem_id*/
      i[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      i[3].join(" ") + " svelte-nl1om8"
    }
  ], d = {};
  for (let o = 0; o < s.length; o += 1)
    d = tt(d, s[o]);
  return {
    c() {
      e = rt(
        /*tag*/
        i[14]
      ), a && a.c(), Ce(
        /*tag*/
        i[14]
      )(e, d), q(
        e,
        "hidden",
        /*visible*/
        i[10] === !1
      ), q(
        e,
        "padded",
        /*padding*/
        i[6]
      ), q(
        e,
        "border_focus",
        /*border_mode*/
        i[5] === "focus"
      ), q(
        e,
        "border_contrast",
        /*border_mode*/
        i[5] === "contrast"
      ), q(e, "hide-container", !/*explicit_call*/
      i[8] && !/*container*/
      i[9]), U(
        e,
        "height",
        /*get_dimension*/
        i[15](
          /*height*/
          i[0]
        )
      ), U(e, "width", typeof /*width*/
      i[1] == "number" ? `calc(min(${/*width*/
      i[1]}px, 100%))` : (
        /*get_dimension*/
        i[15](
          /*width*/
          i[1]
        )
      )), U(
        e,
        "border-style",
        /*variant*/
        i[4]
      ), U(
        e,
        "overflow",
        /*allow_overflow*/
        i[11] ? "visible" : "hidden"
      ), U(
        e,
        "flex-grow",
        /*scale*/
        i[12]
      ), U(e, "min-width", `calc(min(${/*min_width*/
      i[13]}px, 100%))`), U(e, "border-width", "var(--block-border-width)");
    },
    m(o, l) {
      ct(o, e, l), a && a.m(e, null), n = !0;
    },
    p(o, l) {
      a && a.p && (!n || l & /*$$scope*/
      131072) && ft(
        a,
        r,
        o,
        /*$$scope*/
        o[17],
        n ? st(
          r,
          /*$$scope*/
          o[17],
          l,
          null
        ) : at(
          /*$$scope*/
          o[17]
        ),
        null
      ), Ce(
        /*tag*/
        o[14]
      )(e, d = ot(s, [
        (!n || l & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!n || l & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!n || l & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), q(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), q(
        e,
        "padded",
        /*padding*/
        o[6]
      ), q(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), q(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), q(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), l & /*height*/
      1 && U(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), l & /*width*/
      2 && U(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), l & /*variant*/
      16 && U(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), l & /*allow_overflow*/
      2048 && U(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), l & /*scale*/
      4096 && U(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), l & /*min_width*/
      8192 && U(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      n || (Xe(a, o), n = !0);
    },
    o(o) {
      We(a, o), n = !1;
    },
    d(o) {
      o && nt(e), a && a.d(o);
    }
  };
}
function ht(i) {
  let e, t = (
    /*tag*/
    i[14] && ut(i)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, r) {
      t && t.m(n, r), e = !0;
    },
    p(n, [r]) {
      /*tag*/
      n[14] && t.p(n, r);
    },
    i(n) {
      e || (Xe(t, n), e = !0);
    },
    o(n) {
      We(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function pt(i, e, t) {
  let { $$slots: n = {}, $$scope: r } = e, { height: a = void 0 } = e, { width: s = void 0 } = e, { elem_id: d = "" } = e, { elem_classes: o = [] } = e, { variant: l = "solid" } = e, { border_mode: v = "base" } = e, { padding: c = !0 } = e, { type: g = "normal" } = e, { test_id: f = void 0 } = e, { explicit_call: u = !1 } = e, { container: _ = !0 } = e, { visible: C = !0 } = e, { allow_overflow: w = !0 } = e, { scale: b = null } = e, { min_width: S = 0 } = e, M = g === "fieldset" ? "fieldset" : "div";
  const m = (h) => {
    if (h !== void 0) {
      if (typeof h == "number")
        return h + "px";
      if (typeof h == "string")
        return h;
    }
  };
  return i.$$set = (h) => {
    "height" in h && t(0, a = h.height), "width" in h && t(1, s = h.width), "elem_id" in h && t(2, d = h.elem_id), "elem_classes" in h && t(3, o = h.elem_classes), "variant" in h && t(4, l = h.variant), "border_mode" in h && t(5, v = h.border_mode), "padding" in h && t(6, c = h.padding), "type" in h && t(16, g = h.type), "test_id" in h && t(7, f = h.test_id), "explicit_call" in h && t(8, u = h.explicit_call), "container" in h && t(9, _ = h.container), "visible" in h && t(10, C = h.visible), "allow_overflow" in h && t(11, w = h.allow_overflow), "scale" in h && t(12, b = h.scale), "min_width" in h && t(13, S = h.min_width), "$$scope" in h && t(17, r = h.$$scope);
  }, [
    a,
    s,
    d,
    o,
    l,
    v,
    c,
    f,
    u,
    _,
    C,
    w,
    b,
    S,
    M,
    m,
    g,
    r,
    n
  ];
}
class vt extends et {
  constructor(e) {
    super(), lt(this, e, pt, ht, dt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const mt = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Se = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
mt.reduce(
  (i, { color: e, primary: t, secondary: n }) => ({
    ...i,
    [e]: {
      primary: Se[e][t],
      secondary: Se[e][n]
    }
  }),
  {}
);
var ve = function(i, e) {
  return ve = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(t, n) {
    t.__proto__ = n;
  } || function(t, n) {
    for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && (t[r] = n[r]);
  }, ve(i, e);
};
function fe(i, e) {
  if (typeof e != "function" && e !== null)
    throw new TypeError("Class extends value " + String(e) + " is not a constructor or null");
  ve(i, e);
  function t() {
    this.constructor = i;
  }
  i.prototype = e === null ? Object.create(e) : (t.prototype = e.prototype, new t());
}
var T = function() {
  return T = Object.assign || function(e) {
    for (var t, n = 1, r = arguments.length; n < r; n++) {
      t = arguments[n];
      for (var a in t) Object.prototype.hasOwnProperty.call(t, a) && (e[a] = t[a]);
    }
    return e;
  }, T.apply(this, arguments);
};
function V(i) {
  var e = typeof Symbol == "function" && Symbol.iterator, t = e && i[e], n = 0;
  if (t) return t.call(i);
  if (i && typeof i.length == "number") return {
    next: function() {
      return i && n >= i.length && (i = void 0), { value: i && i[n++], done: !i };
    }
  };
  throw new TypeError(e ? "Object is not iterable." : "Symbol.iterator is not defined.");
}
function gt(i, e) {
  var t = typeof Symbol == "function" && i[Symbol.iterator];
  if (!t) return i;
  var n = t.call(i), r, a = [], s;
  try {
    for (; (e === void 0 || e-- > 0) && !(r = n.next()).done; ) a.push(r.value);
  } catch (d) {
    s = { error: d };
  } finally {
    try {
      r && !r.done && (t = n.return) && t.call(n);
    } finally {
      if (s) throw s.error;
    }
  }
  return a;
}
function bt(i, e, t) {
  if (t || arguments.length === 2) for (var n = 0, r = e.length, a; n < r; n++)
    (a || !(n in e)) && (a || (a = Array.prototype.slice.call(e, 0, n)), a[n] = e[n]);
  return i.concat(a || Array.prototype.slice.call(e));
}
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Ve = (
  /** @class */
  function() {
    function i(e) {
      e === void 0 && (e = {}), this.adapter = e;
    }
    return Object.defineProperty(i, "cssClasses", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(i, "strings", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(i, "numbers", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(i, "defaultAdapter", {
      get: function() {
        return {};
      },
      enumerable: !1,
      configurable: !0
    }), i.prototype.init = function() {
    }, i.prototype.destroy = function() {
    }, i;
  }()
);
/**
 * @license
 * Copyright 2019 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function _t(i) {
  return i === void 0 && (i = window), yt(i) ? { passive: !0 } : !1;
}
function yt(i) {
  i === void 0 && (i = window);
  var e = !1;
  try {
    var t = {
      // This function will be called when the browser
      // attempts to access the passive property.
      get passive() {
        return e = !0, !1;
      }
    }, n = function() {
    };
    i.document.addEventListener("test", n, t), i.document.removeEventListener("test", n, t);
  } catch {
    e = !1;
  }
  return e;
}
const wt = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  applyPassive: _t
}, Symbol.toStringTag, { value: "Module" }));
/**
 * @license
 * Copyright 2018 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function Ct(i, e) {
  if (i.closest)
    return i.closest(e);
  for (var t = i; t; ) {
    if (Ze(t, e))
      return t;
    t = t.parentElement;
  }
  return null;
}
function Ze(i, e) {
  var t = i.matches || i.webkitMatchesSelector || i.msMatchesSelector;
  return t.call(i, e);
}
function St(i) {
  var e = i;
  if (e.offsetParent !== null)
    return e.scrollWidth;
  var t = e.cloneNode(!0);
  t.style.setProperty("position", "absolute"), t.style.setProperty("transform", "translate(-9999px, -9999px)"), document.documentElement.appendChild(t);
  var n = t.scrollWidth;
  return document.documentElement.removeChild(t), n;
}
const At = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  closest: Ct,
  estimateScrollWidth: St,
  matches: Ze
}, Symbol.toStringTag, { value: "Module" }));
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var kt = {
  // Ripple is a special case where the "root" component is really a "mixin" of sorts,
  // given that it's an 'upgrade' to an existing component. That being said it is the root
  // CSS class that all other CSS classes derive from.
  BG_FOCUSED: "mdc-ripple-upgraded--background-focused",
  FG_ACTIVATION: "mdc-ripple-upgraded--foreground-activation",
  FG_DEACTIVATION: "mdc-ripple-upgraded--foreground-deactivation",
  ROOT: "mdc-ripple-upgraded",
  UNBOUNDED: "mdc-ripple-upgraded--unbounded"
}, Dt = {
  VAR_FG_SCALE: "--mdc-ripple-fg-scale",
  VAR_FG_SIZE: "--mdc-ripple-fg-size",
  VAR_FG_TRANSLATE_END: "--mdc-ripple-fg-translate-end",
  VAR_FG_TRANSLATE_START: "--mdc-ripple-fg-translate-start",
  VAR_LEFT: "--mdc-ripple-left",
  VAR_TOP: "--mdc-ripple-top"
}, Ae = {
  DEACTIVATION_TIMEOUT_MS: 225,
  FG_DEACTIVATION_MS: 150,
  INITIAL_ORIGIN_SCALE: 0.6,
  PADDING: 10,
  TAP_DELAY_MS: 300
  // Delay between touch and simulated mouse events on touch devices
}, $;
function Mt(i, e) {
  e === void 0 && (e = !1);
  var t = i.CSS, n = $;
  if (typeof $ == "boolean" && !e)
    return $;
  var r = t && typeof t.supports == "function";
  if (!r)
    return !1;
  var a = t.supports("--css-vars", "yes"), s = t.supports("(--css-vars: yes)") && t.supports("color", "#00000000");
  return n = a || s, e || ($ = n), n;
}
function Ot(i, e, t) {
  if (!i)
    return { x: 0, y: 0 };
  var n = e.x, r = e.y, a = n + t.left, s = r + t.top, d, o;
  if (i.type === "touchstart") {
    var l = i;
    d = l.changedTouches[0].pageX - a, o = l.changedTouches[0].pageY - s;
  } else {
    var v = i;
    d = v.pageX - a, o = v.pageY - s;
  }
  return { x: d, y: o };
}
/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var ke = [
  "touchstart",
  "pointerdown",
  "mousedown",
  "keydown"
], De = [
  "touchend",
  "pointerup",
  "mouseup",
  "contextmenu"
], ee = [], Rt = (
  /** @class */
  function(i) {
    fe(e, i);
    function e(t) {
      var n = i.call(this, T(T({}, e.defaultAdapter), t)) || this;
      return n.activationAnimationHasEnded = !1, n.activationTimer = 0, n.fgDeactivationRemovalTimer = 0, n.fgScale = "0", n.frame = { width: 0, height: 0 }, n.initialSize = 0, n.layoutFrame = 0, n.maxRadius = 0, n.unboundedCoords = { left: 0, top: 0 }, n.activationState = n.defaultActivationState(), n.activationTimerCallback = function() {
        n.activationAnimationHasEnded = !0, n.runDeactivationUXLogicIfReady();
      }, n.activateHandler = function(r) {
        n.activateImpl(r);
      }, n.deactivateHandler = function() {
        n.deactivateImpl();
      }, n.focusHandler = function() {
        n.handleFocus();
      }, n.blurHandler = function() {
        n.handleBlur();
      }, n.resizeHandler = function() {
        n.layout();
      }, n;
    }
    return Object.defineProperty(e, "cssClasses", {
      get: function() {
        return kt;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "strings", {
      get: function() {
        return Dt;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "numbers", {
      get: function() {
        return Ae;
      },
      enumerable: !1,
      configurable: !0
    }), Object.defineProperty(e, "defaultAdapter", {
      get: function() {
        return {
          addClass: function() {
          },
          browserSupportsCssVars: function() {
            return !0;
          },
          computeBoundingRect: function() {
            return { top: 0, right: 0, bottom: 0, left: 0, width: 0, height: 0 };
          },
          containsEventTarget: function() {
            return !0;
          },
          deregisterDocumentInteractionHandler: function() {
          },
          deregisterInteractionHandler: function() {
          },
          deregisterResizeHandler: function() {
          },
          getWindowPageOffset: function() {
            return { x: 0, y: 0 };
          },
          isSurfaceActive: function() {
            return !0;
          },
          isSurfaceDisabled: function() {
            return !0;
          },
          isUnbounded: function() {
            return !0;
          },
          registerDocumentInteractionHandler: function() {
          },
          registerInteractionHandler: function() {
          },
          registerResizeHandler: function() {
          },
          removeClass: function() {
          },
          updateCssVariable: function() {
          }
        };
      },
      enumerable: !1,
      configurable: !0
    }), e.prototype.init = function() {
      var t = this, n = this.supportsPressRipple();
      if (this.registerRootHandlers(n), n) {
        var r = e.cssClasses, a = r.ROOT, s = r.UNBOUNDED;
        requestAnimationFrame(function() {
          t.adapter.addClass(a), t.adapter.isUnbounded() && (t.adapter.addClass(s), t.layoutInternal());
        });
      }
    }, e.prototype.destroy = function() {
      var t = this;
      if (this.supportsPressRipple()) {
        this.activationTimer && (clearTimeout(this.activationTimer), this.activationTimer = 0, this.adapter.removeClass(e.cssClasses.FG_ACTIVATION)), this.fgDeactivationRemovalTimer && (clearTimeout(this.fgDeactivationRemovalTimer), this.fgDeactivationRemovalTimer = 0, this.adapter.removeClass(e.cssClasses.FG_DEACTIVATION));
        var n = e.cssClasses, r = n.ROOT, a = n.UNBOUNDED;
        requestAnimationFrame(function() {
          t.adapter.removeClass(r), t.adapter.removeClass(a), t.removeCssVars();
        });
      }
      this.deregisterRootHandlers(), this.deregisterDeactivationHandlers();
    }, e.prototype.activate = function(t) {
      this.activateImpl(t);
    }, e.prototype.deactivate = function() {
      this.deactivateImpl();
    }, e.prototype.layout = function() {
      var t = this;
      this.layoutFrame && cancelAnimationFrame(this.layoutFrame), this.layoutFrame = requestAnimationFrame(function() {
        t.layoutInternal(), t.layoutFrame = 0;
      });
    }, e.prototype.setUnbounded = function(t) {
      var n = e.cssClasses.UNBOUNDED;
      t ? this.adapter.addClass(n) : this.adapter.removeClass(n);
    }, e.prototype.handleFocus = function() {
      var t = this;
      requestAnimationFrame(function() {
        return t.adapter.addClass(e.cssClasses.BG_FOCUSED);
      });
    }, e.prototype.handleBlur = function() {
      var t = this;
      requestAnimationFrame(function() {
        return t.adapter.removeClass(e.cssClasses.BG_FOCUSED);
      });
    }, e.prototype.supportsPressRipple = function() {
      return this.adapter.browserSupportsCssVars();
    }, e.prototype.defaultActivationState = function() {
      return {
        activationEvent: void 0,
        hasDeactivationUXRun: !1,
        isActivated: !1,
        isProgrammatic: !1,
        wasActivatedByPointer: !1,
        wasElementMadeActive: !1
      };
    }, e.prototype.registerRootHandlers = function(t) {
      var n, r;
      if (t) {
        try {
          for (var a = V(ke), s = a.next(); !s.done; s = a.next()) {
            var d = s.value;
            this.adapter.registerInteractionHandler(d, this.activateHandler);
          }
        } catch (o) {
          n = { error: o };
        } finally {
          try {
            s && !s.done && (r = a.return) && r.call(a);
          } finally {
            if (n) throw n.error;
          }
        }
        this.adapter.isUnbounded() && this.adapter.registerResizeHandler(this.resizeHandler);
      }
      this.adapter.registerInteractionHandler("focus", this.focusHandler), this.adapter.registerInteractionHandler("blur", this.blurHandler);
    }, e.prototype.registerDeactivationHandlers = function(t) {
      var n, r;
      if (t.type === "keydown")
        this.adapter.registerInteractionHandler("keyup", this.deactivateHandler);
      else
        try {
          for (var a = V(De), s = a.next(); !s.done; s = a.next()) {
            var d = s.value;
            this.adapter.registerDocumentInteractionHandler(d, this.deactivateHandler);
          }
        } catch (o) {
          n = { error: o };
        } finally {
          try {
            s && !s.done && (r = a.return) && r.call(a);
          } finally {
            if (n) throw n.error;
          }
        }
    }, e.prototype.deregisterRootHandlers = function() {
      var t, n;
      try {
        for (var r = V(ke), a = r.next(); !a.done; a = r.next()) {
          var s = a.value;
          this.adapter.deregisterInteractionHandler(s, this.activateHandler);
        }
      } catch (d) {
        t = { error: d };
      } finally {
        try {
          a && !a.done && (n = r.return) && n.call(r);
        } finally {
          if (t) throw t.error;
        }
      }
      this.adapter.deregisterInteractionHandler("focus", this.focusHandler), this.adapter.deregisterInteractionHandler("blur", this.blurHandler), this.adapter.isUnbounded() && this.adapter.deregisterResizeHandler(this.resizeHandler);
    }, e.prototype.deregisterDeactivationHandlers = function() {
      var t, n;
      this.adapter.deregisterInteractionHandler("keyup", this.deactivateHandler);
      try {
        for (var r = V(De), a = r.next(); !a.done; a = r.next()) {
          var s = a.value;
          this.adapter.deregisterDocumentInteractionHandler(s, this.deactivateHandler);
        }
      } catch (d) {
        t = { error: d };
      } finally {
        try {
          a && !a.done && (n = r.return) && n.call(r);
        } finally {
          if (t) throw t.error;
        }
      }
    }, e.prototype.removeCssVars = function() {
      var t = this, n = e.strings, r = Object.keys(n);
      r.forEach(function(a) {
        a.indexOf("VAR_") === 0 && t.adapter.updateCssVariable(n[a], null);
      });
    }, e.prototype.activateImpl = function(t) {
      var n = this;
      if (!this.adapter.isSurfaceDisabled()) {
        var r = this.activationState;
        if (!r.isActivated) {
          var a = this.previousActivationEvent, s = a && t !== void 0 && a.type !== t.type;
          if (!s) {
            r.isActivated = !0, r.isProgrammatic = t === void 0, r.activationEvent = t, r.wasActivatedByPointer = r.isProgrammatic ? !1 : t !== void 0 && (t.type === "mousedown" || t.type === "touchstart" || t.type === "pointerdown");
            var d = t !== void 0 && ee.length > 0 && ee.some(function(o) {
              return n.adapter.containsEventTarget(o);
            });
            if (d) {
              this.resetActivationState();
              return;
            }
            t !== void 0 && (ee.push(t.target), this.registerDeactivationHandlers(t)), r.wasElementMadeActive = this.checkElementMadeActive(t), r.wasElementMadeActive && this.animateActivation(), requestAnimationFrame(function() {
              ee = [], !r.wasElementMadeActive && t !== void 0 && (t.key === " " || t.keyCode === 32) && (r.wasElementMadeActive = n.checkElementMadeActive(t), r.wasElementMadeActive && n.animateActivation()), r.wasElementMadeActive || (n.activationState = n.defaultActivationState());
            });
          }
        }
      }
    }, e.prototype.checkElementMadeActive = function(t) {
      return t !== void 0 && t.type === "keydown" ? this.adapter.isSurfaceActive() : !0;
    }, e.prototype.animateActivation = function() {
      var t = this, n = e.strings, r = n.VAR_FG_TRANSLATE_START, a = n.VAR_FG_TRANSLATE_END, s = e.cssClasses, d = s.FG_DEACTIVATION, o = s.FG_ACTIVATION, l = e.numbers.DEACTIVATION_TIMEOUT_MS;
      this.layoutInternal();
      var v = "", c = "";
      if (!this.adapter.isUnbounded()) {
        var g = this.getFgTranslationCoordinates(), f = g.startPoint, u = g.endPoint;
        v = f.x + "px, " + f.y + "px", c = u.x + "px, " + u.y + "px";
      }
      this.adapter.updateCssVariable(r, v), this.adapter.updateCssVariable(a, c), clearTimeout(this.activationTimer), clearTimeout(this.fgDeactivationRemovalTimer), this.rmBoundedActivationClasses(), this.adapter.removeClass(d), this.adapter.computeBoundingRect(), this.adapter.addClass(o), this.activationTimer = setTimeout(function() {
        t.activationTimerCallback();
      }, l);
    }, e.prototype.getFgTranslationCoordinates = function() {
      var t = this.activationState, n = t.activationEvent, r = t.wasActivatedByPointer, a;
      r ? a = Ot(n, this.adapter.getWindowPageOffset(), this.adapter.computeBoundingRect()) : a = {
        x: this.frame.width / 2,
        y: this.frame.height / 2
      }, a = {
        x: a.x - this.initialSize / 2,
        y: a.y - this.initialSize / 2
      };
      var s = {
        x: this.frame.width / 2 - this.initialSize / 2,
        y: this.frame.height / 2 - this.initialSize / 2
      };
      return { startPoint: a, endPoint: s };
    }, e.prototype.runDeactivationUXLogicIfReady = function() {
      var t = this, n = e.cssClasses.FG_DEACTIVATION, r = this.activationState, a = r.hasDeactivationUXRun, s = r.isActivated, d = a || !s;
      d && this.activationAnimationHasEnded && (this.rmBoundedActivationClasses(), this.adapter.addClass(n), this.fgDeactivationRemovalTimer = setTimeout(function() {
        t.adapter.removeClass(n);
      }, Ae.FG_DEACTIVATION_MS));
    }, e.prototype.rmBoundedActivationClasses = function() {
      var t = e.cssClasses.FG_ACTIVATION;
      this.adapter.removeClass(t), this.activationAnimationHasEnded = !1, this.adapter.computeBoundingRect();
    }, e.prototype.resetActivationState = function() {
      var t = this;
      this.previousActivationEvent = this.activationState.activationEvent, this.activationState = this.defaultActivationState(), setTimeout(function() {
        return t.previousActivationEvent = void 0;
      }, e.numbers.TAP_DELAY_MS);
    }, e.prototype.deactivateImpl = function() {
      var t = this, n = this.activationState;
      if (n.isActivated) {
        var r = T({}, n);
        n.isProgrammatic ? (requestAnimationFrame(function() {
          t.animateDeactivation(r);
        }), this.resetActivationState()) : (this.deregisterDeactivationHandlers(), requestAnimationFrame(function() {
          t.activationState.hasDeactivationUXRun = !0, t.animateDeactivation(r), t.resetActivationState();
        }));
      }
    }, e.prototype.animateDeactivation = function(t) {
      var n = t.wasActivatedByPointer, r = t.wasElementMadeActive;
      (n || r) && this.runDeactivationUXLogicIfReady();
    }, e.prototype.layoutInternal = function() {
      var t = this;
      this.frame = this.adapter.computeBoundingRect();
      var n = Math.max(this.frame.height, this.frame.width), r = function() {
        var s = Math.sqrt(Math.pow(t.frame.width, 2) + Math.pow(t.frame.height, 2));
        return s + e.numbers.PADDING;
      };
      this.maxRadius = this.adapter.isUnbounded() ? n : r();
      var a = Math.floor(n * e.numbers.INITIAL_ORIGIN_SCALE);
      this.adapter.isUnbounded() && a % 2 !== 0 ? this.initialSize = a - 1 : this.initialSize = a, this.fgScale = "" + this.maxRadius / this.initialSize, this.updateLayoutCssVars();
    }, e.prototype.updateLayoutCssVars = function() {
      var t = e.strings, n = t.VAR_FG_SIZE, r = t.VAR_LEFT, a = t.VAR_TOP, s = t.VAR_FG_SCALE;
      this.adapter.updateCssVariable(n, this.initialSize + "px"), this.adapter.updateCssVariable(s, this.fgScale), this.adapter.isUnbounded() && (this.unboundedCoords = {
        left: Math.round(this.frame.width / 2 - this.initialSize / 2),
        top: Math.round(this.frame.height / 2 - this.initialSize / 2)
      }, this.adapter.updateCssVariable(r, this.unboundedCoords.left + "px"), this.adapter.updateCssVariable(a, this.unboundedCoords.top + "px"));
    }, e;
  }(Ve)
);
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Z;
(function(i) {
  i.PROCESSING = "mdc-switch--processing", i.SELECTED = "mdc-switch--selected", i.UNSELECTED = "mdc-switch--unselected";
})(Z || (Z = {}));
var Me;
(function(i) {
  i.RIPPLE = ".mdc-switch__ripple";
})(Me || (Me = {}));
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
function Ft(i, e, t) {
  var n = Ht(i, e), r = n.getObservers(e);
  return r.push(t), function() {
    r.splice(r.indexOf(t), 1);
  };
}
var ae = /* @__PURE__ */ new WeakMap();
function Ht(i, e) {
  var t = /* @__PURE__ */ new Map();
  ae.has(i) || ae.set(i, {
    isEnabled: !0,
    getObservers: function(l) {
      var v = t.get(l) || [];
      return t.has(l) || t.set(l, v), v;
    },
    installedProperties: /* @__PURE__ */ new Set()
  });
  var n = ae.get(i);
  if (n.installedProperties.has(e))
    return n;
  var r = Lt(i, e) || {
    configurable: !0,
    enumerable: !0,
    value: i[e],
    writable: !0
  }, a = T({}, r), s = r.get, d = r.set;
  if ("value" in r) {
    delete a.value, delete a.writable;
    var o = r.value;
    s = function() {
      return o;
    }, r.writable && (d = function(l) {
      o = l;
    });
  }
  return s && (a.get = function() {
    return s.call(this);
  }), d && (a.set = function(l) {
    var v, c, g = s ? s.call(this) : l;
    if (d.call(this, l), n.isEnabled && (!s || l !== g))
      try {
        for (var f = V(n.getObservers(e)), u = f.next(); !u.done; u = f.next()) {
          var _ = u.value;
          _(l, g);
        }
      } catch (C) {
        v = { error: C };
      } finally {
        try {
          u && !u.done && (c = f.return) && c.call(f);
        } finally {
          if (v) throw v.error;
        }
      }
  }), n.installedProperties.add(e), Object.defineProperty(i, e, a), n;
}
function Lt(i, e) {
  for (var t = i, n; t && (n = Object.getOwnPropertyDescriptor(t, e), !n); )
    t = Object.getPrototypeOf(t);
  return n;
}
function Ut(i, e) {
  var t = ae.get(i);
  t && (t.isEnabled = e);
}
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var It = (
  /** @class */
  function(i) {
    fe(e, i);
    function e(t) {
      var n = i.call(this, t) || this;
      return n.unobserves = /* @__PURE__ */ new Set(), n;
    }
    return e.prototype.destroy = function() {
      i.prototype.destroy.call(this), this.unobserve();
    }, e.prototype.observe = function(t, n) {
      var r, a, s = this, d = [];
      try {
        for (var o = V(Object.keys(n)), l = o.next(); !l.done; l = o.next()) {
          var v = l.value, c = n[v].bind(this);
          d.push(this.observeProperty(t, v, c));
        }
      } catch (f) {
        r = { error: f };
      } finally {
        try {
          l && !l.done && (a = o.return) && a.call(o);
        } finally {
          if (r) throw r.error;
        }
      }
      var g = function() {
        var f, u;
        try {
          for (var _ = V(d), C = _.next(); !C.done; C = _.next()) {
            var w = C.value;
            w();
          }
        } catch (b) {
          f = { error: b };
        } finally {
          try {
            C && !C.done && (u = _.return) && u.call(_);
          } finally {
            if (f) throw f.error;
          }
        }
        s.unobserves.delete(g);
      };
      return this.unobserves.add(g), g;
    }, e.prototype.observeProperty = function(t, n, r) {
      return Ft(t, n, r);
    }, e.prototype.setObserversEnabled = function(t, n) {
      Ut(t, n);
    }, e.prototype.unobserve = function() {
      var t, n;
      try {
        for (var r = V(bt([], gt(this.unobserves))), a = r.next(); !a.done; a = r.next()) {
          var s = a.value;
          s();
        }
      } catch (d) {
        t = { error: d };
      } finally {
        try {
          a && !a.done && (n = r.return) && n.call(r);
        } finally {
          if (t) throw t.error;
        }
      }
    }, e;
  }(Ve)
);
/**
 * @license
 * Copyright 2021 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
var Et = (
  /** @class */
  function(i) {
    fe(e, i);
    function e(t) {
      var n = i.call(this, t) || this;
      return n.handleClick = n.handleClick.bind(n), n;
    }
    return e.prototype.init = function() {
      this.observe(this.adapter.state, {
        disabled: this.stopProcessingIfDisabled,
        processing: this.stopProcessingIfDisabled
      });
    }, e.prototype.handleClick = function() {
      this.adapter.state.disabled || (this.adapter.state.selected = !this.adapter.state.selected);
    }, e.prototype.stopProcessingIfDisabled = function() {
      this.adapter.state.disabled && (this.adapter.state.processing = !1);
    }, e;
  }(It)
), Pt = (
  /** @class */
  function(i) {
    fe(e, i);
    function e() {
      return i !== null && i.apply(this, arguments) || this;
    }
    return e.prototype.init = function() {
      i.prototype.init.call(this), this.observe(this.adapter.state, {
        disabled: this.onDisabledChange,
        processing: this.onProcessingChange,
        selected: this.onSelectedChange
      });
    }, e.prototype.initFromDOM = function() {
      this.setObserversEnabled(this.adapter.state, !1), this.adapter.state.selected = this.adapter.hasClass(Z.SELECTED), this.onSelectedChange(), this.adapter.state.disabled = this.adapter.isDisabled(), this.adapter.state.processing = this.adapter.hasClass(Z.PROCESSING), this.setObserversEnabled(this.adapter.state, !0), this.stopProcessingIfDisabled();
    }, e.prototype.onDisabledChange = function() {
      this.adapter.setDisabled(this.adapter.state.disabled);
    }, e.prototype.onProcessingChange = function() {
      this.toggleClass(this.adapter.state.processing, Z.PROCESSING);
    }, e.prototype.onSelectedChange = function() {
      this.adapter.setAriaChecked(String(this.adapter.state.selected)), this.toggleClass(this.adapter.state.selected, Z.SELECTED), this.toggleClass(!this.adapter.state.selected, Z.UNSELECTED);
    }, e.prototype.toggleClass = function(t, n) {
      t ? this.adapter.addClass(n) : this.adapter.removeClass(n);
    }, e;
  }(Et)
);
function oe(i) {
  return Object.entries(i).filter(([e, t]) => e !== "" && t).map(([e]) => e).join(" ");
}
function te(i, e, t, n = { bubbles: !0 }, r = !1) {
  if (typeof Event > "u")
    throw new Error("Event not defined.");
  if (!i)
    throw new Error("Tried to dipatch event without element.");
  const a = new CustomEvent(e, Object.assign(Object.assign({}, n), { detail: t }));
  if (i == null || i.dispatchEvent(a), r && e.startsWith("SMUI")) {
    const s = new CustomEvent(e.replace(/^SMUI/g, () => "MDC"), Object.assign(Object.assign({}, n), { detail: t }));
    i == null || i.dispatchEvent(s), s.defaultPrevented && a.preventDefault();
  }
  return a;
}
function Oe(i, e) {
  let t = Object.getOwnPropertyNames(i);
  const n = {};
  for (let r = 0; r < t.length; r++) {
    const a = t[r], s = a.indexOf("$");
    s !== -1 && e.indexOf(a.substring(0, s + 1)) !== -1 || e.indexOf(a) === -1 && (n[a] = i[a]);
  }
  return n;
}
const Re = /^[a-z]+(?::(?:preventDefault|stopPropagation|passive|nonpassive|capture|once|self))+$/, Gt = /^[^$]+(?:\$(?:preventDefault|stopPropagation|passive|nonpassive|capture|once|self))+$/;
function Bt(i) {
  let e, t = [];
  i.$on = (r, a) => {
    let s = r, d = () => {
    };
    return e ? d = e(s, a) : t.push([s, a]), s.match(Re) && console && console.warn('Event modifiers in SMUI now use "$" instead of ":", so that all events can be bound with modifiers. Please update your event binding: ', s), () => {
      d();
    };
  };
  function n(r) {
    const a = i.$$.callbacks[r.type];
    a && a.slice().forEach((s) => s.call(this, r));
  }
  return (r) => {
    const a = [], s = {};
    e = (d, o) => {
      let l = d, v = o, c = !1;
      const g = l.match(Re), f = l.match(Gt), u = g || f;
      if (l.match(/^SMUI:\w+:/)) {
        const w = l.split(":");
        let b = "";
        for (let S = 0; S < w.length; S++)
          b += S === w.length - 1 ? ":" + w[S] : w[S].split("-").map((M) => M.slice(0, 1).toUpperCase() + M.slice(1)).join("");
        console.warn(`The event ${l.split("$")[0]} has been renamed to ${b.split("$")[0]}.`), l = b;
      }
      if (u) {
        const w = l.split(g ? ":" : "$");
        l = w[0];
        const b = w.slice(1).reduce((S, M) => (S[M] = !0, S), {});
        b.passive && (c = c || {}, c.passive = !0), b.nonpassive && (c = c || {}, c.passive = !1), b.capture && (c = c || {}, c.capture = !0), b.once && (c = c || {}, c.once = !0), b.preventDefault && (v = zt(v)), b.stopPropagation && (v = jt(v)), b.stopImmediatePropagation && (v = qt(v)), b.self && (v = Xt(r, v)), b.trusted && (v = Wt(v));
      }
      const _ = Fe(r, l, v, c), C = () => {
        _();
        const w = a.indexOf(C);
        w > -1 && a.splice(w, 1);
      };
      return a.push(C), l in s || (s[l] = Fe(r, l, n)), C;
    };
    for (let d = 0; d < t.length; d++)
      e(t[d][0], t[d][1]);
    return {
      destroy: () => {
        for (let d = 0; d < a.length; d++)
          a[d]();
        for (let d of Object.entries(s))
          d[1]();
      }
    };
  };
}
function Fe(i, e, t, n) {
  return i.addEventListener(e, t, n), () => i.removeEventListener(e, t, n);
}
function zt(i) {
  return function(e) {
    return e.preventDefault(), i.call(this, e);
  };
}
function jt(i) {
  return function(e) {
    return e.stopPropagation(), i.call(this, e);
  };
}
function qt(i) {
  return function(e) {
    return e.stopImmediatePropagation(), i.call(this, e);
  };
}
function Xt(i, e) {
  return function(t) {
    if (t.target === i)
      return e.call(this, t);
  };
}
function Wt(i) {
  return function(e) {
    if (e.isTrusted)
      return i.call(this, e);
  };
}
function He(i, e) {
  let t = Object.getOwnPropertyNames(i);
  const n = {};
  for (let r = 0; r < t.length; r++) {
    const a = t[r];
    a.substring(0, e.length) === e && (n[a.substring(e.length)] = i[a]);
  }
  return n;
}
function Je(i, e) {
  let t = [];
  if (e)
    for (let n = 0; n < e.length; n++) {
      const r = e[n], a = Array.isArray(r) ? r[0] : r;
      Array.isArray(r) && r.length > 1 ? t.push(a(i, r[1])) : t.push(a(i));
    }
  return {
    update(n) {
      if ((n && n.length || 0) != t.length)
        throw new Error("You must not change the length of an actions array.");
      if (n)
        for (let r = 0; r < n.length; r++) {
          const a = t[r];
          if (a && a.update) {
            const s = n[r];
            Array.isArray(s) && s.length > 1 ? a.update(s[1]) : a.update();
          }
        }
    },
    destroy() {
      for (let n = 0; n < t.length; n++) {
        const r = t[n];
        r && r.destroy && r.destroy();
      }
    }
  };
}
const { getContext: Vt } = window.__gradio__svelte__internal, { applyPassive: ie } = wt, { matches: Zt } = At;
function Jt(i, { ripple: e = !0, surface: t = !1, unbounded: n = !1, disabled: r = !1, color: a, active: s, rippleElement: d, eventTarget: o, activeTarget: l, addClass: v = (u) => i.classList.add(u), removeClass: c = (u) => i.classList.remove(u), addStyle: g = (u, _) => i.style.setProperty(u, _), initPromise: f = Promise.resolve() } = {}) {
  let u, _ = Vt("SMUI:addLayoutListener"), C, w = s, b = o, S = l;
  function M() {
    t ? (v("mdc-ripple-surface"), a === "primary" ? (v("smui-ripple-surface--primary"), c("smui-ripple-surface--secondary")) : a === "secondary" ? (c("smui-ripple-surface--primary"), v("smui-ripple-surface--secondary")) : (c("smui-ripple-surface--primary"), c("smui-ripple-surface--secondary"))) : (c("mdc-ripple-surface"), c("smui-ripple-surface--primary"), c("smui-ripple-surface--secondary")), u && w !== s && (w = s, s ? u.activate() : s === !1 && u.deactivate()), e && !u ? (u = new Rt({
      addClass: v,
      browserSupportsCssVars: () => Mt(window),
      computeBoundingRect: () => (d || i).getBoundingClientRect(),
      containsEventTarget: (h) => i.contains(h),
      deregisterDocumentInteractionHandler: (h, A) => document.documentElement.removeEventListener(h, A, ie()),
      deregisterInteractionHandler: (h, A) => (o || i).removeEventListener(h, A, ie()),
      deregisterResizeHandler: (h) => window.removeEventListener("resize", h),
      getWindowPageOffset: () => ({
        x: window.pageXOffset,
        y: window.pageYOffset
      }),
      isSurfaceActive: () => s ?? Zt(l || i, ":active"),
      isSurfaceDisabled: () => !!r,
      isUnbounded: () => !!n,
      registerDocumentInteractionHandler: (h, A) => document.documentElement.addEventListener(h, A, ie()),
      registerInteractionHandler: (h, A) => (o || i).addEventListener(h, A, ie()),
      registerResizeHandler: (h) => window.addEventListener("resize", h),
      removeClass: c,
      updateCssVariable: g
    }), f.then(() => {
      u && (u.init(), u.setUnbounded(n));
    })) : u && !e && f.then(() => {
      u && (u.destroy(), u = void 0);
    }), u && (b !== o || S !== l) && (b = o, S = l, u.destroy(), requestAnimationFrame(() => {
      u && (u.init(), u.setUnbounded(n));
    })), !e && n && v("mdc-ripple-upgraded--unbounded");
  }
  M(), _ && (C = _(m));
  function m() {
    u && u.layout();
  }
  return {
    update(h) {
      ({
        ripple: e,
        surface: t,
        unbounded: n,
        disabled: r,
        color: a,
        active: s,
        rippleElement: d,
        eventTarget: o,
        activeTarget: l,
        addClass: v,
        removeClass: c,
        addStyle: g,
        initPromise: f
      } = Object.assign({ ripple: !0, surface: !1, unbounded: !1, disabled: !1, color: void 0, active: void 0, rippleElement: void 0, eventTarget: void 0, activeTarget: void 0, addClass: (A) => i.classList.add(A), removeClass: (A) => i.classList.remove(A), addStyle: (A, y) => i.style.setProperty(A, y), initPromise: Promise.resolve() }, h)), M();
    },
    destroy() {
      u && (u.destroy(), u = void 0, c("mdc-ripple-surface"), c("smui-ripple-surface--primary"), c("smui-ripple-surface--secondary")), C && C();
    }
  };
}
const {
  SvelteComponent: Kt,
  action_destroyer: se,
  append: L,
  assign: le,
  attr: P,
  binding_callbacks: Le,
  compute_rest_props: Ue,
  detach: ge,
  element: W,
  exclude_internal_props: Qt,
  get_spread_update: Ke,
  init: Tt,
  insert: be,
  is_function: me,
  listen: xt,
  noop: Ie,
  run_all: Nt,
  safe_not_equal: Yt,
  set_attributes: ce,
  space: N,
  svg_element: ne
} = window.__gradio__svelte__internal, { onMount: $t, getContext: ei } = window.__gradio__svelte__internal, { get_current_component: ti } = window.__gradio__svelte__internal;
function Ee(i) {
  let e, t, n, r, a, s, d, o, l, v, c = [
    {
      class: d = oe({
        [
          /*icons$class*/
          i[8]
        ]: !0,
        "mdc-switch__icons": !0
      })
    },
    He(
      /*$$restProps*/
      i[19],
      "icons$"
    )
  ], g = {};
  for (let f = 0; f < c.length; f += 1)
    g = le(g, c[f]);
  return {
    c() {
      e = W("div"), t = ne("svg"), n = ne("path"), r = N(), a = ne("svg"), s = ne("path"), P(n, "d", "M19.69,5.23L8.96,15.96l-4.23-4.23L2.96,13.5l6,6L21.46,7L19.69,5.23z"), P(t, "class", "mdc-switch__icon mdc-switch__icon--on"), P(t, "viewBox", "0 0 24 24"), P(s, "d", "M20 13H4v-2h16v2z"), P(a, "class", "mdc-switch__icon mdc-switch__icon--off"), P(a, "viewBox", "0 0 24 24"), ce(e, g);
    },
    m(f, u) {
      be(f, e, u), L(e, t), L(t, n), L(e, r), L(e, a), L(a, s), l || (v = se(o = Je.call(
        null,
        e,
        /*icons$use*/
        i[7]
      )), l = !0);
    },
    p(f, u) {
      ce(e, g = Ke(c, [
        u[0] & /*icons$class*/
        256 && d !== (d = oe({
          [
            /*icons$class*/
            f[8]
          ]: !0,
          "mdc-switch__icons": !0
        })) && { class: d },
        u[0] & /*$$restProps*/
        524288 && He(
          /*$$restProps*/
          f[19],
          "icons$"
        )
      ])), o && me(o.update) && u[0] & /*icons$use*/
      128 && o.update.call(
        null,
        /*icons$use*/
        f[7]
      );
    },
    d(f) {
      f && ge(e), l = !1, v();
    }
  };
}
function Pe(i) {
  let e;
  return {
    c() {
      e = W("div"), e.innerHTML = '<div class="mdc-switch__focus-ring"></div>', P(e, "class", "mdc-switch__focus-ring-wrapper");
    },
    m(t, n) {
      be(t, e, n);
    },
    d(t) {
      t && ge(e);
    }
  };
}
function ii(i) {
  let e, t, n, r, a, s, d, o, l, v, c, g, f, u, _, C, w = (
    /*icons*/
    i[6] && Ee(i)
  ), b = (
    /*focusRing*/
    i[4] && Pe()
  ), S = [
    {
      class: c = oe({
        [
          /*className*/
          i[3]
        ]: !0,
        "mdc-switch": !0,
        "mdc-switch--unselected": !/*selected*/
        i[10],
        "mdc-switch--selected": (
          /*selected*/
          i[10]
        ),
        "mdc-switch--processing": (
          /*processing*/
          i[1]
        ),
        "smui-switch--color-secondary": (
          /*color*/
          i[5] === "secondary"
        ),
        .../*internalClasses*/
        i[12]
      })
    },
    { type: "button" },
    { role: "switch" },
    {
      "aria-checked": g = /*selected*/
      i[10] ? "true" : "false"
    },
    { disabled: (
      /*disabled*/
      i[0]
    ) },
    /*inputProps*/
    i[16],
    Oe(
      /*$$restProps*/
      i[19],
      ["icons$"]
    )
  ], M = {};
  for (let m = 0; m < S.length; m += 1)
    M = le(M, S[m]);
  return {
    c() {
      e = W("button"), t = W("div"), n = N(), r = W("div"), a = W("div"), s = W("div"), s.innerHTML = '<div class="mdc-elevation-overlay"></div>', d = N(), o = W("div"), l = N(), w && w.c(), v = N(), b && b.c(), P(t, "class", "mdc-switch__track"), P(s, "class", "mdc-switch__shadow"), P(o, "class", "mdc-switch__ripple"), P(a, "class", "mdc-switch__handle"), P(r, "class", "mdc-switch__handle-track"), ce(e, M);
    },
    m(m, h) {
      be(m, e, h), L(e, t), L(e, n), L(e, r), L(r, a), L(a, s), L(a, d), L(a, o), i[28](o), L(a, l), w && w.m(a, null), L(e, v), b && b.m(e, null), e.autofocus && e.focus(), i[29](e), _ || (C = [
        se(f = Je.call(
          null,
          e,
          /*use*/
          i[2]
        )),
        se(
          /*forwardEvents*/
          i[15].call(null, e)
        ),
        se(u = Jt.call(null, e, {
          unbounded: !0,
          color: (
            /*color*/
            i[5]
          ),
          active: (
            /*rippleActive*/
            i[14]
          ),
          rippleElement: (
            /*rippleElement*/
            i[13]
          ),
          disabled: (
            /*disabled*/
            i[0]
          ),
          addClass: (
            /*addClass*/
            i[17]
          ),
          removeClass: (
            /*removeClass*/
            i[18]
          )
        })),
        xt(
          e,
          "click",
          /*click_handler*/
          i[30]
        )
      ], _ = !0);
    },
    p(m, h) {
      /*icons*/
      m[6] ? w ? w.p(m, h) : (w = Ee(m), w.c(), w.m(a, null)) : w && (w.d(1), w = null), /*focusRing*/
      m[4] ? b || (b = Pe(), b.c(), b.m(e, null)) : b && (b.d(1), b = null), ce(e, M = Ke(S, [
        h[0] & /*className, selected, processing, color, internalClasses*/
        5162 && c !== (c = oe({
          [
            /*className*/
            m[3]
          ]: !0,
          "mdc-switch": !0,
          "mdc-switch--unselected": !/*selected*/
          m[10],
          "mdc-switch--selected": (
            /*selected*/
            m[10]
          ),
          "mdc-switch--processing": (
            /*processing*/
            m[1]
          ),
          "smui-switch--color-secondary": (
            /*color*/
            m[5] === "secondary"
          ),
          .../*internalClasses*/
          m[12]
        })) && { class: c },
        { type: "button" },
        { role: "switch" },
        h[0] & /*selected*/
        1024 && g !== (g = /*selected*/
        m[10] ? "true" : "false") && {
          "aria-checked": g
        },
        h[0] & /*disabled*/
        1 && { disabled: (
          /*disabled*/
          m[0]
        ) },
        /*inputProps*/
        m[16],
        h[0] & /*$$restProps*/
        524288 && Oe(
          /*$$restProps*/
          m[19],
          ["icons$"]
        )
      ])), f && me(f.update) && h[0] & /*use*/
      4 && f.update.call(
        null,
        /*use*/
        m[2]
      ), u && me(u.update) && h[0] & /*color, rippleActive, rippleElement, disabled*/
      24609 && u.update.call(null, {
        unbounded: !0,
        color: (
          /*color*/
          m[5]
        ),
        active: (
          /*rippleActive*/
          m[14]
        ),
        rippleElement: (
          /*rippleElement*/
          m[13]
        ),
        disabled: (
          /*disabled*/
          m[0]
        ),
        addClass: (
          /*addClass*/
          m[17]
        ),
        removeClass: (
          /*removeClass*/
          m[18]
        )
      });
    },
    i: Ie,
    o: Ie,
    d(m) {
      m && ge(e), i[28](null), w && w.d(), b && b.d(), i[29](null), _ = !1, Nt(C);
    }
  };
}
function ni(i, e, t) {
  const n = [
    "use",
    "class",
    "disabled",
    "focusRing",
    "color",
    "group",
    "checked",
    "value",
    "processing",
    "icons",
    "icons$use",
    "icons$class",
    "getId",
    "getElement"
  ];
  let r = Ue(e, n);
  var a;
  const s = Bt(ti());
  let d = () => {
  };
  function o(p) {
    return p === d;
  }
  let { use: l = [] } = e, { class: v = "" } = e, { disabled: c = !1 } = e, { focusRing: g = !1 } = e, { color: f = "primary" } = e, { group: u = d } = e, { checked: _ = d } = e, { value: C = null } = e, { processing: w = !1 } = e, { icons: b = !0 } = e, { icons$use: S = [] } = e, { icons$class: M = "" } = e, m, h, A = {}, y, F = !1, I = (a = ei("SMUI:generic:input:props")) !== null && a !== void 0 ? a : {}, D = o(u) ? o(_) ? !1 : _ : u.indexOf(C) !== -1, z = {
    get disabled() {
      return c;
    },
    set disabled(p) {
      t(0, c = p);
    },
    get processing() {
      return w;
    },
    set processing(p) {
      t(1, w = p);
    },
    get selected() {
      return D;
    },
    set selected(p) {
      t(10, D = p);
    }
  }, k = _, O = o(u) ? [] : [...u], G = D;
  $t(() => {
    t(11, h = new Pt({
      addClass: K,
      hasClass: J,
      isDisabled: () => c,
      removeClass: j,
      setAriaChecked: () => {
      },
      // Handled automatically.
      setDisabled: (E) => {
        t(0, c = E);
      },
      state: z
    }));
    const p = {
      get element() {
        return ue();
      },
      get checked() {
        return D;
      },
      set checked(E) {
        D !== E && (z.selected = E, m && te(m, "SMUISwitch:change", { selected: E, value: C }));
      },
      activateRipple() {
        c || t(14, F = !0);
      },
      deactivateRipple() {
        t(14, F = !1);
      }
    };
    return te(m, "SMUIGenericInput:mount", p), h.init(), h.initFromDOM(), () => {
      te(m, "SMUIGenericInput:unmount", p), h.destroy();
    };
  });
  function J(p) {
    return p in A ? A[p] : ue().classList.contains(p);
  }
  function K(p) {
    A[p] || t(12, A[p] = !0, A);
  }
  function j(p) {
    (!(p in A) || A[p]) && t(12, A[p] = !1, A);
  }
  function x() {
    return I && I.id;
  }
  function ue() {
    return m;
  }
  function Ne(p) {
    Le[p ? "unshift" : "push"](() => {
      y = p, t(13, y);
    });
  }
  function Ye(p) {
    Le[p ? "unshift" : "push"](() => {
      m = p, t(9, m);
    });
  }
  const $e = () => h && h.handleClick();
  return i.$$set = (p) => {
    e = le(le({}, e), Qt(p)), t(19, r = Ue(e, n)), "use" in p && t(2, l = p.use), "class" in p && t(3, v = p.class), "disabled" in p && t(0, c = p.disabled), "focusRing" in p && t(4, g = p.focusRing), "color" in p && t(5, f = p.color), "group" in p && t(20, u = p.group), "checked" in p && t(21, _ = p.checked), "value" in p && t(22, C = p.value), "processing" in p && t(1, w = p.processing), "icons" in p && t(6, b = p.icons), "icons$use" in p && t(7, S = p.icons$use), "icons$class" in p && t(8, M = p.icons$class);
  }, i.$$.update = () => {
    if (i.$$.dirty[0] & /*group, previousSelected, selected, value, previousGroup, checked, previousChecked, element*/
    242222592) {
      let p = !1;
      if (!o(u))
        if (G !== D) {
          const E = u.indexOf(C);
          D && E === -1 ? (u.push(C), t(20, u), t(27, G), t(10, D), t(22, C), t(26, O), t(21, _), t(25, k), t(9, m)) : !D && E !== -1 && (u.splice(E, 1), t(20, u), t(27, G), t(10, D), t(22, C), t(26, O), t(21, _), t(25, k), t(9, m)), p = !0;
        } else {
          const E = O.indexOf(C), we = u.indexOf(C);
          E > -1 && we === -1 ? z.selected = !1 : we > -1 && E === -1 && (z.selected = !0);
        }
      o(_) ? G !== D && (p = !0) : _ !== D && (_ === k ? (t(21, _ = D), p = !0) : z.selected = _), t(25, k = _), t(26, O = o(u) ? [] : [...u]), t(27, G = D), p && m && te(m, "SMUISwitch:change", { selected: D, value: C });
    }
  }, [
    c,
    w,
    l,
    v,
    g,
    f,
    b,
    S,
    M,
    m,
    D,
    h,
    A,
    y,
    F,
    s,
    I,
    K,
    j,
    r,
    u,
    _,
    C,
    x,
    ue,
    k,
    O,
    G,
    Ne,
    Ye,
    $e
  ];
}
class ri extends Kt {
  constructor(e) {
    super(), Tt(
      this,
      e,
      ni,
      ii,
      Yt,
      {
        use: 2,
        class: 3,
        disabled: 0,
        focusRing: 4,
        color: 5,
        group: 20,
        checked: 21,
        value: 22,
        processing: 1,
        icons: 6,
        icons$use: 7,
        icons$class: 8,
        getId: 23,
        getElement: 24
      },
      null,
      [-1, -1]
    );
  }
  get getId() {
    return this.$$.ctx[23];
  }
  get getElement() {
    return this.$$.ctx[24];
  }
}
const {
  SvelteComponent: ai,
  add_flush_callback: si,
  append: R,
  attr: B,
  bind: oi,
  binding_callbacks: li,
  check_outros: ci,
  create_component: Qe,
  destroy_component: Te,
  destroy_each: Ge,
  detach: _e,
  element: X,
  ensure_array_like: re,
  flush: H,
  group_outros: di,
  init: fi,
  insert: ye,
  listen: ui,
  mount_component: xe,
  noop: hi,
  safe_not_equal: pi,
  set_data: he,
  space: Q,
  text: pe,
  transition_in: Y,
  transition_out: de
} = window.__gradio__svelte__internal;
function Be(i, e, t) {
  const n = i.slice();
  return n[24] = e[t], n[25] = e, n[8] = t, n;
}
function ze(i, e, t) {
  const n = i.slice();
  return n[26] = e[t], n;
}
function je(i) {
  let e;
  return {
    c() {
      e = X("th"), e.textContent = `${/*header*/
      i[26]}`;
    },
    m(t, n) {
      ye(t, e, n);
    },
    p: hi,
    d(t) {
      t && _e(e);
    }
  };
}
function qe(i) {
  var z;
  let e, t, n = (
    /*data*/
    i[24].ligandA + ""
  ), r, a, s, d = (
    /*data*/
    i[24].ligandB + ""
  ), o, l, v, c = (
    /*data*/
    ((z = i[24].similarity) == null ? void 0 : z.toFixed(3)) + ""
  ), g, f, u, _, C, w, b, S, M, m, h, A;
  function y(k) {
    i[17](
      k,
      /*data*/
      i[24]
    );
  }
  function F(...k) {
    return (
      /*SMUISwitch_change_handler*/
      i[18](
        /*data*/
        i[24],
        /*index*/
        i[8],
        ...k
      )
    );
  }
  let I = {};
  /*data*/
  i[24].link !== void 0 && (I.checked = /*data*/
  i[24].link), _ = new ri({ props: I }), li.push(() => oi(_, "checked", y)), _.$on("SMUISwitch:change", F);
  function D() {
    return (
      /*click_handler*/
      i[19](
        /*data*/
        i[24],
        /*index*/
        i[8]
      )
    );
  }
  return {
    c() {
      e = X("tr"), t = X("td"), r = pe(n), a = Q(), s = X("td"), o = pe(d), l = Q(), v = X("td"), g = pe(c), f = Q(), u = X("td"), Qe(_.$$.fragment), w = Q(), b = X("td"), S = X("button"), S.innerHTML = '<svg width="1em" height="1em" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.75 5.83398C1.75 3.50065 2.91667 2.33398 5.25 2.33398" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"></path><path d="M11.6641 8.75C11.6641 11.0833 10.4974 12.25 8.16406 12.25" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"></path><path d="M8.16406 5.25065C8.16406 3.63983 9.46991 2.33398 11.0807 2.33398H12.2474V6.41732H8.16406V5.25065Z" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path><path d="M1.75 8.16602H5.83333V9.33268C5.83333 10.9435 4.52748 12.2493 2.91667 12.2493H1.75V8.16602Z" stroke="#A2A5C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"></path></svg>', M = Q(), B(t, "class", "svelte-ca3kvl"), B(s, "class", "svelte-ca3kvl"), B(v, "class", "svelte-ca3kvl"), B(u, "class", "svelte-ca3kvl"), B(b, "class", "svelte-ca3kvl"), B(e, "class", "svelte-ca3kvl");
    },
    m(k, O) {
      ye(k, e, O), R(e, t), R(t, r), R(e, a), R(e, s), R(s, o), R(e, l), R(e, v), R(v, g), R(e, f), R(e, u), xe(_, u, null), R(e, w), R(e, b), R(b, S), R(e, M), m = !0, h || (A = ui(S, "click", D), h = !0);
    },
    p(k, O) {
      var J;
      i = k, (!m || O & /*tableData*/
      128) && n !== (n = /*data*/
      i[24].ligandA + "") && he(r, n), (!m || O & /*tableData*/
      128) && d !== (d = /*data*/
      i[24].ligandB + "") && he(o, d), (!m || O & /*tableData*/
      128) && c !== (c = /*data*/
      ((J = i[24].similarity) == null ? void 0 : J.toFixed(3)) + "") && he(g, c);
      const G = {};
      !C && O & /*tableData*/
      128 && (C = !0, G.checked = /*data*/
      i[24].link, si(() => C = !1)), _.$set(G);
    },
    i(k) {
      m || (Y(_.$$.fragment, k), m = !0);
    },
    o(k) {
      de(_.$$.fragment, k), m = !1;
    },
    d(k) {
      k && _e(e), Te(_), h = !1, A();
    }
  };
}
function vi(i) {
  let e, t, n, r, a, s = re(
    /*headers*/
    i[9]
  ), d = [];
  for (let c = 0; c < s.length; c += 1)
    d[c] = je(ze(i, s, c));
  let o = re(
    /*tableData*/
    i[7]
  ), l = [];
  for (let c = 0; c < o.length; c += 1)
    l[c] = qe(Be(i, o, c));
  const v = (c) => de(l[c], 1, 1, () => {
    l[c] = null;
  });
  return {
    c() {
      e = X("table"), t = X("tr");
      for (let c = 0; c < d.length; c += 1)
        d[c].c();
      n = Q();
      for (let c = 0; c < l.length; c += 1)
        l[c].c();
      B(t, "class", "svelte-ca3kvl"), B(e, "border", "1"), B(e, "class", "fep-pair-table svelte-ca3kvl"), B(e, "id", r = "fep-pair-table-update" + /*index*/
      i[8]);
    },
    m(c, g) {
      ye(c, e, g), R(e, t);
      for (let f = 0; f < d.length; f += 1)
        d[f] && d[f].m(t, null);
      R(e, n);
      for (let f = 0; f < l.length; f += 1)
        l[f] && l[f].m(e, null);
      a = !0;
    },
    p(c, g) {
      if (g & /*headers*/
      512) {
        s = re(
          /*headers*/
          c[9]
        );
        let f;
        for (f = 0; f < s.length; f += 1) {
          const u = ze(c, s, f);
          d[f] ? d[f].p(u, g) : (d[f] = je(u), d[f].c(), d[f].m(t, null));
        }
        for (; f < d.length; f += 1)
          d[f].d(1);
        d.length = s.length;
      }
      if (g & /*value, JSON, tableData, gradio*/
      131) {
        o = re(
          /*tableData*/
          c[7]
        );
        let f;
        for (f = 0; f < o.length; f += 1) {
          const u = Be(c, o, f);
          l[f] ? (l[f].p(u, g), Y(l[f], 1)) : (l[f] = qe(u), l[f].c(), Y(l[f], 1), l[f].m(e, null));
        }
        for (di(), f = o.length; f < l.length; f += 1)
          v(f);
        ci();
      }
      (!a || g & /*index*/
      256 && r !== (r = "fep-pair-table-update" + /*index*/
      c[8])) && B(e, "id", r);
    },
    i(c) {
      if (!a) {
        for (let g = 0; g < o.length; g += 1)
          Y(l[g]);
        a = !0;
      }
    },
    o(c) {
      l = l.filter(Boolean);
      for (let g = 0; g < l.length; g += 1)
        de(l[g]);
      a = !1;
    },
    d(c) {
      c && _e(e), Ge(d, c), Ge(l, c);
    }
  };
}
function mi(i) {
  let e, t;
  return e = new vt({
    props: {
      visible: (
        /*visible*/
        i[4]
      ),
      elem_id: (
        /*elem_id*/
        i[2]
      ),
      elem_classes: (
        /*elem_classes*/
        i[3]
      ),
      scale: (
        /*scale*/
        i[5]
      ),
      min_width: (
        /*min_width*/
        i[6]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [vi] },
      $$scope: { ctx: i }
    }
  }), {
    c() {
      Qe(e.$$.fragment);
    },
    m(n, r) {
      xe(e, n, r), t = !0;
    },
    p(n, [r]) {
      const a = {};
      r & /*visible*/
      16 && (a.visible = /*visible*/
      n[4]), r & /*elem_id*/
      4 && (a.elem_id = /*elem_id*/
      n[2]), r & /*elem_classes*/
      8 && (a.elem_classes = /*elem_classes*/
      n[3]), r & /*scale*/
      32 && (a.scale = /*scale*/
      n[5]), r & /*min_width*/
      64 && (a.min_width = /*min_width*/
      n[6]), r & /*$$scope, index, tableData, value, gradio*/
      536871299 && (a.$$scope = { dirty: r, ctx: n }), e.$set(a);
    },
    i(n) {
      t || (Y(e.$$.fragment, n), t = !0);
    },
    o(n) {
      de(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Te(e, n);
    }
  };
}
function gi(i, e, t) {
  this && this.__awaiter;
  let { gradio: n } = e, { label: r = "Textbox" } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { visible: d = !0 } = e, { value: o = "" } = e, { placeholder: l = "" } = e, { show_label: v } = e, { scale: c = null } = e, { min_width: g = void 0 } = e, { loading_status: f = void 0 } = e, { value_is_output: u = !1 } = e, { interactive: _ } = e, { rtl: C = !1 } = e;
  const w = ["LigandA", "LigandB", "Similarity", "Link", "Mapping"];
  let b = [], S = 1;
  const M = () => {
    const { pairs: y } = JSON.parse(l);
    t(7, b = [...y]), t(8, S++, S);
  };
  function m(y, F) {
    i.$$.not_equal(F.link, y) && (F.link = y, t(7, b));
  }
  const h = (y, F, I) => {
    t(0, o = JSON.stringify({
      res: { ...y, link: b[F].link },
      type: "Link",
      index: F
    })), n.dispatch("change");
  }, A = (y, F) => {
    t(0, o = JSON.stringify({ res: y, type: "Mapping", index: F })), n.dispatch("change");
  };
  return i.$$set = (y) => {
    "gradio" in y && t(1, n = y.gradio), "label" in y && t(10, r = y.label), "elem_id" in y && t(2, a = y.elem_id), "elem_classes" in y && t(3, s = y.elem_classes), "visible" in y && t(4, d = y.visible), "value" in y && t(0, o = y.value), "placeholder" in y && t(11, l = y.placeholder), "show_label" in y && t(12, v = y.show_label), "scale" in y && t(5, c = y.scale), "min_width" in y && t(6, g = y.min_width), "loading_status" in y && t(13, f = y.loading_status), "value_is_output" in y && t(14, u = y.value_is_output), "interactive" in y && t(15, _ = y.interactive), "rtl" in y && t(16, C = y.rtl);
  }, i.$$.update = () => {
    i.$$.dirty & /*value*/
    1 && o === null && t(0, o = ""), i.$$.dirty & /*value*/
    1, i.$$.dirty & /*placeholder*/
    2048 && M();
  }, [
    o,
    n,
    a,
    s,
    d,
    c,
    g,
    b,
    S,
    w,
    r,
    l,
    v,
    f,
    u,
    _,
    C,
    m,
    h,
    A
  ];
}
class bi extends ai {
  constructor(e) {
    super(), fi(this, e, gi, mi, pi, {
      gradio: 1,
      label: 10,
      elem_id: 2,
      elem_classes: 3,
      visible: 4,
      value: 0,
      placeholder: 11,
      show_label: 12,
      scale: 5,
      min_width: 6,
      loading_status: 13,
      value_is_output: 14,
      interactive: 15,
      rtl: 16
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), H();
  }
  get label() {
    return this.$$.ctx[10];
  }
  set label(e) {
    this.$$set({ label: e }), H();
  }
  get elem_id() {
    return this.$$.ctx[2];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), H();
  }
  get elem_classes() {
    return this.$$.ctx[3];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), H();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({ visible: e }), H();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), H();
  }
  get placeholder() {
    return this.$$.ctx[11];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), H();
  }
  get show_label() {
    return this.$$.ctx[12];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), H();
  }
  get scale() {
    return this.$$.ctx[5];
  }
  set scale(e) {
    this.$$set({ scale: e }), H();
  }
  get min_width() {
    return this.$$.ctx[6];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), H();
  }
  get loading_status() {
    return this.$$.ctx[13];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), H();
  }
  get value_is_output() {
    return this.$$.ctx[14];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), H();
  }
  get interactive() {
    return this.$$.ctx[15];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), H();
  }
  get rtl() {
    return this.$$.ctx[16];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), H();
  }
}
export {
  bi as default
};
