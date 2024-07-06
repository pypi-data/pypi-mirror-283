function sl() {
}
function wn(t, l) {
  return t != t ? l == l : t !== l || t && typeof t == "object" || typeof t == "function";
}
function Jl(t) {
  const l = typeof t == "string" && t.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return l ? [parseFloat(l[1]), l[2] || "px"] : [
    /** @type {number} */
    t,
    "px"
  ];
}
const Jt = typeof window < "u";
let Rl = Jt ? () => window.performance.now() : () => Date.now(), Rt = Jt ? (t) => requestAnimationFrame(t) : sl;
const Ie = /* @__PURE__ */ new Set();
function Xt(t) {
  Ie.forEach((l) => {
    l.c(t) || (Ie.delete(l), l.f());
  }), Ie.size !== 0 && Rt(Xt);
}
function pn(t) {
  let l;
  return Ie.size === 0 && Rt(Xt), {
    promise: new Promise((e) => {
      Ie.add(l = { c: t, f: e });
    }),
    abort() {
      Ie.delete(l);
    }
  };
}
function kn(t) {
  const l = t - 1;
  return l * l * l + 1;
}
function Xl(t, { delay: l = 0, duration: e = 400, easing: n = kn, x: i = 0, y: o = 0, opacity: u = 0 } = {}) {
  const f = getComputedStyle(t), s = +f.opacity, r = f.transform === "none" ? "" : f.transform, a = s * (1 - u), [m, v] = Jl(i), [h, y] = Jl(o);
  return {
    delay: l,
    duration: e,
    easing: n,
    css: (b, c) => `
			transform: ${r} translate(${(1 - b) * m}${v}, ${(1 - b) * h}${y});
			opacity: ${s - a * c}`
  };
}
const Le = [];
function vn(t, l = sl) {
  let e;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (wn(t, f) && (t = f, e)) {
      const s = !Le.length;
      for (const r of n)
        r[1](), Le.push(r, t);
      if (s) {
        for (let r = 0; r < Le.length; r += 2)
          Le[r][0](Le[r + 1]);
        Le.length = 0;
      }
    }
  }
  function o(f) {
    i(f(t));
  }
  function u(f, s = sl) {
    const r = [f, s];
    return n.add(r), n.size === 1 && (e = l(i, o) || sl), f(t), () => {
      n.delete(r), n.size === 0 && e && (e(), e = null);
    };
  }
  return { set: i, update: o, subscribe: u };
}
function Yl(t) {
  return Object.prototype.toString.call(t) === "[object Date]";
}
function Nl(t, l, e, n) {
  if (typeof e == "number" || Yl(e)) {
    const i = n - e, o = (e - l) / (t.dt || 1 / 60), u = t.opts.stiffness * i, f = t.opts.damping * o, s = (u - f) * t.inv_mass, r = (o + s) * t.dt;
    return Math.abs(r) < t.opts.precision && Math.abs(i) < t.opts.precision ? n : (t.settled = !1, Yl(e) ? new Date(e.getTime() + r) : e + r);
  } else {
    if (Array.isArray(e))
      return e.map(
        (i, o) => Nl(t, l[o], e[o], n[o])
      );
    if (typeof e == "object") {
      const i = {};
      for (const o in e)
        i[o] = Nl(t, l[o], e[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function Gl(t, l = {}) {
  const e = vn(t), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = l;
  let u, f, s, r = t, a = t, m = 1, v = 0, h = !1;
  function y(c, d = {}) {
    a = c;
    const j = s = {};
    return t == null || d.hard || b.stiffness >= 1 && b.damping >= 1 ? (h = !0, u = Rl(), r = c, e.set(t = a), Promise.resolve()) : (d.soft && (v = 1 / ((d.soft === !0 ? 0.5 : +d.soft) * 60), m = 0), f || (u = Rl(), h = !1, f = pn((_) => {
      if (h)
        return h = !1, f = null, !1;
      m = Math.min(m + v, 1);
      const w = {
        inv_mass: m,
        opts: b,
        settled: !0,
        dt: (_ - u) * 60 / 1e3
      }, S = Nl(w, r, t, a);
      return u = _, r = t, e.set(t = S), w.settled && (f = null), !w.settled;
    })), new Promise((_) => {
      f.promise.then(() => {
        j === s && _();
      });
    }));
  }
  const b = {
    set: y,
    update: (c, d) => y(c(a, t), d),
    subscribe: e.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return b;
}
const {
  SvelteComponent: yn,
  add_render_callback: Yt,
  append: tl,
  attr: $,
  binding_callbacks: Kl,
  check_outros: jn,
  create_bidirectional_transition: Ql,
  destroy_each: Cn,
  detach: Ke,
  element: rl,
  empty: qn,
  ensure_array_like: Wl,
  group_outros: Sn,
  init: En,
  insert: Qe,
  listen: Fl,
  prevent_default: Nn,
  run_all: Fn,
  safe_not_equal: Ln,
  set_data: zn,
  set_style: ye,
  space: Ll,
  text: Mn,
  toggle_class: fe,
  transition_in: yl,
  transition_out: xl
} = window.__gradio__svelte__internal, { createEventDispatcher: On } = window.__gradio__svelte__internal;
function $l(t, l, e) {
  const n = t.slice();
  return n[26] = l[e], n;
}
function et(t) {
  let l, e, n, i, o, u = Wl(
    /*filtered_indices*/
    t[1]
  ), f = [];
  for (let s = 0; s < u.length; s += 1)
    f[s] = lt($l(t, u, s));
  return {
    c() {
      l = rl("ul");
      for (let s = 0; s < f.length; s += 1)
        f[s].c();
      $(l, "class", "options svelte-yuohum"), $(l, "role", "listbox"), ye(
        l,
        "top",
        /*top*/
        t[9]
      ), ye(
        l,
        "bottom",
        /*bottom*/
        t[10]
      ), ye(l, "max-height", `calc(${/*max_height*/
      t[11]}px - var(--window-padding))`), ye(
        l,
        "width",
        /*input_width*/
        t[8] + "px"
      );
    },
    m(s, r) {
      Qe(s, l, r);
      for (let a = 0; a < f.length; a += 1)
        f[a] && f[a].m(l, null);
      t[23](l), n = !0, i || (o = Fl(l, "mousedown", Nn(
        /*mousedown_handler*/
        t[22]
      )), i = !0);
    },
    p(s, r) {
      if (r & /*filtered_indices, choices, selected_indices, active_index*/
      51) {
        u = Wl(
          /*filtered_indices*/
          s[1]
        );
        let a;
        for (a = 0; a < u.length; a += 1) {
          const m = $l(s, u, a);
          f[a] ? f[a].p(m, r) : (f[a] = lt(m), f[a].c(), f[a].m(l, null));
        }
        for (; a < f.length; a += 1)
          f[a].d(1);
        f.length = u.length;
      }
      r & /*top*/
      512 && ye(
        l,
        "top",
        /*top*/
        s[9]
      ), r & /*bottom*/
      1024 && ye(
        l,
        "bottom",
        /*bottom*/
        s[10]
      ), r & /*max_height*/
      2048 && ye(l, "max-height", `calc(${/*max_height*/
      s[11]}px - var(--window-padding))`), r & /*input_width*/
      256 && ye(
        l,
        "width",
        /*input_width*/
        s[8] + "px"
      );
    },
    i(s) {
      n || (s && Yt(() => {
        n && (e || (e = Ql(l, Xl, { duration: 200, y: 5 }, !0)), e.run(1));
      }), n = !0);
    },
    o(s) {
      s && (e || (e = Ql(l, Xl, { duration: 200, y: 5 }, !1)), e.run(0)), n = !1;
    },
    d(s) {
      s && Ke(l), Cn(f, s), t[23](null), s && e && e.end(), i = !1, o();
    }
  };
}
function lt(t) {
  let l, e, n, i = (
    /*choices*/
    t[0][
      /*index*/
      t[26]
    ][0] + ""
  ), o, u, f, s, r;
  return {
    c() {
      l = rl("li"), e = rl("span"), e.textContent = "✓", n = Ll(), o = Mn(i), u = Ll(), $(e, "class", "inner-item svelte-yuohum"), fe(e, "hide", !/*selected_indices*/
      t[4].includes(
        /*index*/
        t[26]
      )), $(l, "class", "item svelte-yuohum"), $(l, "data-index", f = /*index*/
      t[26]), $(l, "aria-label", s = /*choices*/
      t[0][
        /*index*/
        t[26]
      ][0]), $(l, "data-testid", "dropdown-option"), $(l, "role", "option"), $(l, "aria-selected", r = /*selected_indices*/
      t[4].includes(
        /*index*/
        t[26]
      )), fe(
        l,
        "selected",
        /*selected_indices*/
        t[4].includes(
          /*index*/
          t[26]
        )
      ), fe(
        l,
        "active",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      ), fe(
        l,
        "bg-gray-100",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      ), fe(
        l,
        "dark:bg-gray-600",
        /*index*/
        t[26] === /*active_index*/
        t[5]
      );
    },
    m(a, m) {
      Qe(a, l, m), tl(l, e), tl(l, n), tl(l, o), tl(l, u);
    },
    p(a, m) {
      m & /*selected_indices, filtered_indices*/
      18 && fe(e, "hide", !/*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )), m & /*choices, filtered_indices*/
      3 && i !== (i = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0] + "") && zn(o, i), m & /*filtered_indices*/
      2 && f !== (f = /*index*/
      a[26]) && $(l, "data-index", f), m & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      a[0][
        /*index*/
        a[26]
      ][0]) && $(l, "aria-label", s), m & /*selected_indices, filtered_indices*/
      18 && r !== (r = /*selected_indices*/
      a[4].includes(
        /*index*/
        a[26]
      )) && $(l, "aria-selected", r), m & /*selected_indices, filtered_indices*/
      18 && fe(
        l,
        "selected",
        /*selected_indices*/
        a[4].includes(
          /*index*/
          a[26]
        )
      ), m & /*filtered_indices, active_index*/
      34 && fe(
        l,
        "active",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), m & /*filtered_indices, active_index*/
      34 && fe(
        l,
        "bg-gray-100",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      ), m & /*filtered_indices, active_index*/
      34 && fe(
        l,
        "dark:bg-gray-600",
        /*index*/
        a[26] === /*active_index*/
        a[5]
      );
    },
    d(a) {
      a && Ke(l);
    }
  };
}
function An(t) {
  let l, e, n, i, o;
  Yt(
    /*onwindowresize*/
    t[20]
  );
  let u = (
    /*show_options*/
    t[2] && !/*disabled*/
    t[3] && et(t)
  );
  return {
    c() {
      l = rl("div"), e = Ll(), u && u.c(), n = qn(), $(l, "class", "reference");
    },
    m(f, s) {
      Qe(f, l, s), t[21](l), Qe(f, e, s), u && u.m(f, s), Qe(f, n, s), i || (o = [
        Fl(
          window,
          "scroll",
          /*scroll_listener*/
          t[13]
        ),
        Fl(
          window,
          "resize",
          /*onwindowresize*/
          t[20]
        )
      ], i = !0);
    },
    p(f, [s]) {
      /*show_options*/
      f[2] && !/*disabled*/
      f[3] ? u ? (u.p(f, s), s & /*show_options, disabled*/
      12 && yl(u, 1)) : (u = et(f), u.c(), yl(u, 1), u.m(n.parentNode, n)) : u && (Sn(), xl(u, 1, 1, () => {
        u = null;
      }), jn());
    },
    i(f) {
      yl(u);
    },
    o(f) {
      xl(u);
    },
    d(f) {
      f && (Ke(l), Ke(e), Ke(n)), t[21](null), u && u.d(f), i = !1, Fn(o);
    }
  };
}
function Vn(t, l, e) {
  var n, i;
  let { choices: o } = l, { filtered_indices: u } = l, { show_options: f = !1 } = l, { disabled: s = !1 } = l, { selected_indices: r = [] } = l, { active_index: a = null } = l, m, v, h, y, b, c, d, j, _, w;
  function S() {
    const { top: F, bottom: I } = b.getBoundingClientRect();
    e(17, m = F), e(18, v = w - I);
  }
  let p = null;
  function N() {
    f && (p !== null && clearTimeout(p), p = setTimeout(
      () => {
        S(), p = null;
      },
      10
    ));
  }
  const q = On();
  function E() {
    e(12, w = window.innerHeight);
  }
  function B(F) {
    Kl[F ? "unshift" : "push"](() => {
      b = F, e(6, b);
    });
  }
  const T = (F) => q("change", F);
  function le(F) {
    Kl[F ? "unshift" : "push"](() => {
      c = F, e(7, c);
    });
  }
  return t.$$set = (F) => {
    "choices" in F && e(0, o = F.choices), "filtered_indices" in F && e(1, u = F.filtered_indices), "show_options" in F && e(2, f = F.show_options), "disabled" in F && e(3, s = F.disabled), "selected_indices" in F && e(4, r = F.selected_indices), "active_index" in F && e(5, a = F.active_index);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    1016020) {
      if (f && b) {
        if (c && r.length > 0) {
          let I = c.querySelectorAll("li");
          for (const H of Array.from(I))
            if (H.getAttribute("data-index") === r[0].toString()) {
              e(15, n = c?.scrollTo) === null || n === void 0 || n.call(c, 0, H.offsetTop);
              break;
            }
        }
        S();
        const F = e(16, i = b.parentElement) === null || i === void 0 ? void 0 : i.getBoundingClientRect();
        e(19, h = F?.height || 0), e(8, y = F?.width || 0);
      }
      v > m ? (e(9, d = `${m}px`), e(11, _ = v), e(10, j = null)) : (e(10, j = `${v + h}px`), e(11, _ = m - h), e(9, d = null));
    }
  }, [
    o,
    u,
    f,
    s,
    r,
    a,
    b,
    c,
    y,
    d,
    j,
    _,
    w,
    N,
    q,
    n,
    i,
    m,
    v,
    h,
    E,
    B,
    T,
    le
  ];
}
class Gt extends yn {
  constructor(l) {
    super(), En(this, l, Vn, An, Ln, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
const {
  SvelteComponent: Dn,
  assign: Bn,
  create_slot: Tn,
  detach: Un,
  element: Zn,
  get_all_dirty_from_scope: Pn,
  get_slot_changes: In,
  get_spread_update: Hn,
  init: Jn,
  insert: Rn,
  safe_not_equal: Xn,
  set_dynamic_element_data: tt,
  set_style: W,
  toggle_class: je,
  transition_in: Kt,
  transition_out: Qt,
  update_slot_base: Yn
} = window.__gradio__svelte__internal;
function Gn(t) {
  let l, e, n;
  const i = (
    /*#slots*/
    t[18].default
  ), o = Tn(
    i,
    t,
    /*$$scope*/
    t[17],
    null
  );
  let u = [
    { "data-testid": (
      /*test_id*/
      t[7]
    ) },
    { id: (
      /*elem_id*/
      t[2]
    ) },
    {
      class: e = "block " + /*elem_classes*/
      t[3].join(" ") + " svelte-1t38q2d"
    }
  ], f = {};
  for (let s = 0; s < u.length; s += 1)
    f = Bn(f, u[s]);
  return {
    c() {
      l = Zn(
        /*tag*/
        t[14]
      ), o && o.c(), tt(
        /*tag*/
        t[14]
      )(l, f), je(
        l,
        "hidden",
        /*visible*/
        t[10] === !1
      ), je(
        l,
        "padded",
        /*padding*/
        t[6]
      ), je(
        l,
        "border_focus",
        /*border_mode*/
        t[5] === "focus"
      ), je(l, "hide-container", !/*explicit_call*/
      t[8] && !/*container*/
      t[9]), W(
        l,
        "height",
        /*get_dimension*/
        t[15](
          /*height*/
          t[0]
        )
      ), W(l, "width", typeof /*width*/
      t[1] == "number" ? `calc(min(${/*width*/
      t[1]}px, 100%))` : (
        /*get_dimension*/
        t[15](
          /*width*/
          t[1]
        )
      )), W(
        l,
        "border-style",
        /*variant*/
        t[4]
      ), W(
        l,
        "overflow",
        /*allow_overflow*/
        t[11] ? "visible" : "hidden"
      ), W(
        l,
        "flex-grow",
        /*scale*/
        t[12]
      ), W(l, "min-width", `calc(min(${/*min_width*/
      t[13]}px, 100%))`), W(l, "border-width", "var(--block-border-width)");
    },
    m(s, r) {
      Rn(s, l, r), o && o.m(l, null), n = !0;
    },
    p(s, r) {
      o && o.p && (!n || r & /*$$scope*/
      131072) && Yn(
        o,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? In(
          i,
          /*$$scope*/
          s[17],
          r,
          null
        ) : Pn(
          /*$$scope*/
          s[17]
        ),
        null
      ), tt(
        /*tag*/
        s[14]
      )(l, f = Hn(u, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && e !== (e = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-1t38q2d")) && { class: e }
      ])), je(
        l,
        "hidden",
        /*visible*/
        s[10] === !1
      ), je(
        l,
        "padded",
        /*padding*/
        s[6]
      ), je(
        l,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), je(l, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), r & /*height*/
      1 && W(
        l,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), r & /*width*/
      2 && W(l, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), r & /*variant*/
      16 && W(
        l,
        "border-style",
        /*variant*/
        s[4]
      ), r & /*allow_overflow*/
      2048 && W(
        l,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && W(
        l,
        "flex-grow",
        /*scale*/
        s[12]
      ), r & /*min_width*/
      8192 && W(l, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (Kt(o, s), n = !0);
    },
    o(s) {
      Qt(o, s), n = !1;
    },
    d(s) {
      s && Un(l), o && o.d(s);
    }
  };
}
function Kn(t) {
  let l, e = (
    /*tag*/
    t[14] && Gn(t)
  );
  return {
    c() {
      e && e.c();
    },
    m(n, i) {
      e && e.m(n, i), l = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && e.p(n, i);
    },
    i(n) {
      l || (Kt(e, n), l = !0);
    },
    o(n) {
      Qt(e, n), l = !1;
    },
    d(n) {
      e && e.d(n);
    }
  };
}
function Qn(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { height: o = void 0 } = l, { width: u = void 0 } = l, { elem_id: f = "" } = l, { elem_classes: s = [] } = l, { variant: r = "solid" } = l, { border_mode: a = "base" } = l, { padding: m = !0 } = l, { type: v = "normal" } = l, { test_id: h = void 0 } = l, { explicit_call: y = !1 } = l, { container: b = !0 } = l, { visible: c = !0 } = l, { allow_overflow: d = !0 } = l, { scale: j = null } = l, { min_width: _ = 0 } = l, w = v === "fieldset" ? "fieldset" : "div";
  const S = (p) => {
    if (p !== void 0) {
      if (typeof p == "number")
        return p + "px";
      if (typeof p == "string")
        return p;
    }
  };
  return t.$$set = (p) => {
    "height" in p && e(0, o = p.height), "width" in p && e(1, u = p.width), "elem_id" in p && e(2, f = p.elem_id), "elem_classes" in p && e(3, s = p.elem_classes), "variant" in p && e(4, r = p.variant), "border_mode" in p && e(5, a = p.border_mode), "padding" in p && e(6, m = p.padding), "type" in p && e(16, v = p.type), "test_id" in p && e(7, h = p.test_id), "explicit_call" in p && e(8, y = p.explicit_call), "container" in p && e(9, b = p.container), "visible" in p && e(10, c = p.visible), "allow_overflow" in p && e(11, d = p.allow_overflow), "scale" in p && e(12, j = p.scale), "min_width" in p && e(13, _ = p.min_width), "$$scope" in p && e(17, i = p.$$scope);
  }, [
    o,
    u,
    f,
    s,
    r,
    a,
    m,
    h,
    y,
    b,
    c,
    d,
    j,
    _,
    w,
    S,
    v,
    i,
    n
  ];
}
class Wn extends Dn {
  constructor(l) {
    super(), Jn(this, l, Qn, Kn, Xn, {
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
const {
  SvelteComponent: xn,
  attr: $n,
  create_slot: ei,
  detach: li,
  element: ti,
  get_all_dirty_from_scope: ni,
  get_slot_changes: ii,
  init: si,
  insert: fi,
  safe_not_equal: oi,
  transition_in: ui,
  transition_out: ri,
  update_slot_base: ai
} = window.__gradio__svelte__internal;
function _i(t) {
  let l, e;
  const n = (
    /*#slots*/
    t[1].default
  ), i = ei(
    n,
    t,
    /*$$scope*/
    t[0],
    null
  );
  return {
    c() {
      l = ti("div"), i && i.c(), $n(l, "class", "svelte-1hnfib2");
    },
    m(o, u) {
      fi(o, l, u), i && i.m(l, null), e = !0;
    },
    p(o, [u]) {
      i && i.p && (!e || u & /*$$scope*/
      1) && ai(
        i,
        n,
        o,
        /*$$scope*/
        o[0],
        e ? ii(
          n,
          /*$$scope*/
          o[0],
          u,
          null
        ) : ni(
          /*$$scope*/
          o[0]
        ),
        null
      );
    },
    i(o) {
      e || (ui(i, o), e = !0);
    },
    o(o) {
      ri(i, o), e = !1;
    },
    d(o) {
      o && li(l), i && i.d(o);
    }
  };
}
function ci(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l;
  return t.$$set = (o) => {
    "$$scope" in o && e(0, i = o.$$scope);
  }, [i, n];
}
class di extends xn {
  constructor(l) {
    super(), si(this, l, ci, _i, oi, {});
  }
}
const {
  SvelteComponent: mi,
  attr: nt,
  check_outros: bi,
  create_component: hi,
  create_slot: gi,
  destroy_component: wi,
  detach: fl,
  element: pi,
  empty: ki,
  get_all_dirty_from_scope: vi,
  get_slot_changes: yi,
  group_outros: ji,
  init: Ci,
  insert: ol,
  mount_component: qi,
  safe_not_equal: Si,
  set_data: Ei,
  space: Ni,
  text: Fi,
  toggle_class: ze,
  transition_in: Ye,
  transition_out: ul,
  update_slot_base: Li
} = window.__gradio__svelte__internal;
function it(t) {
  let l, e;
  return l = new di({
    props: {
      $$slots: { default: [zi] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      hi(l.$$.fragment);
    },
    m(n, i) {
      qi(l, n, i), e = !0;
    },
    p(n, i) {
      const o = {};
      i & /*$$scope, info*/
      10 && (o.$$scope = { dirty: i, ctx: n }), l.$set(o);
    },
    i(n) {
      e || (Ye(l.$$.fragment, n), e = !0);
    },
    o(n) {
      ul(l.$$.fragment, n), e = !1;
    },
    d(n) {
      wi(l, n);
    }
  };
}
function zi(t) {
  let l;
  return {
    c() {
      l = Fi(
        /*info*/
        t[1]
      );
    },
    m(e, n) {
      ol(e, l, n);
    },
    p(e, n) {
      n & /*info*/
      2 && Ei(
        l,
        /*info*/
        e[1]
      );
    },
    d(e) {
      e && fl(l);
    }
  };
}
function Mi(t) {
  let l, e, n, i;
  const o = (
    /*#slots*/
    t[2].default
  ), u = gi(
    o,
    t,
    /*$$scope*/
    t[3],
    null
  );
  let f = (
    /*info*/
    t[1] && it(t)
  );
  return {
    c() {
      l = pi("span"), u && u.c(), e = Ni(), f && f.c(), n = ki(), nt(l, "data-testid", "block-info"), nt(l, "class", "svelte-22c38v"), ze(l, "sr-only", !/*show_label*/
      t[0]), ze(l, "hide", !/*show_label*/
      t[0]), ze(
        l,
        "has-info",
        /*info*/
        t[1] != null
      );
    },
    m(s, r) {
      ol(s, l, r), u && u.m(l, null), ol(s, e, r), f && f.m(s, r), ol(s, n, r), i = !0;
    },
    p(s, [r]) {
      u && u.p && (!i || r & /*$$scope*/
      8) && Li(
        u,
        o,
        s,
        /*$$scope*/
        s[3],
        i ? yi(
          o,
          /*$$scope*/
          s[3],
          r,
          null
        ) : vi(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || r & /*show_label*/
      1) && ze(l, "sr-only", !/*show_label*/
      s[0]), (!i || r & /*show_label*/
      1) && ze(l, "hide", !/*show_label*/
      s[0]), (!i || r & /*info*/
      2) && ze(
        l,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? f ? (f.p(s, r), r & /*info*/
      2 && Ye(f, 1)) : (f = it(s), f.c(), Ye(f, 1), f.m(n.parentNode, n)) : f && (ji(), ul(f, 1, 1, () => {
        f = null;
      }), bi());
    },
    i(s) {
      i || (Ye(u, s), Ye(f), i = !0);
    },
    o(s) {
      ul(u, s), ul(f), i = !1;
    },
    d(s) {
      s && (fl(l), fl(e), fl(n)), u && u.d(s), f && f.d(s);
    }
  };
}
function Oi(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { show_label: o = !0 } = l, { info: u = void 0 } = l;
  return t.$$set = (f) => {
    "show_label" in f && e(0, o = f.show_label), "info" in f && e(1, u = f.info), "$$scope" in f && e(3, i = f.$$scope);
  }, [o, u, n, i];
}
class Wt extends mi {
  constructor(l) {
    super(), Ci(this, l, Oi, Mi, Si, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Ai,
  append: Vi,
  attr: Me,
  detach: Di,
  init: Bi,
  insert: Ti,
  noop: jl,
  safe_not_equal: Ui,
  svg_element: st
} = window.__gradio__svelte__internal;
function Zi(t) {
  let l, e;
  return {
    c() {
      l = st("svg"), e = st("path"), Me(e, "d", "M5 8l4 4 4-4z"), Me(l, "class", "dropdown-arrow svelte-145leq6"), Me(l, "xmlns", "http://www.w3.org/2000/svg"), Me(l, "width", "100%"), Me(l, "height", "100%"), Me(l, "viewBox", "0 0 18 18");
    },
    m(n, i) {
      Ti(n, l, i), Vi(l, e);
    },
    p: jl,
    i: jl,
    o: jl,
    d(n) {
      n && Di(l);
    }
  };
}
class xt extends Ai {
  constructor(l) {
    super(), Bi(this, l, null, Zi, Ui, {});
  }
}
const {
  SvelteComponent: Pi,
  append: Ii,
  attr: Cl,
  detach: Hi,
  init: Ji,
  insert: Ri,
  noop: ql,
  safe_not_equal: Xi,
  svg_element: ft
} = window.__gradio__svelte__internal;
function Yi(t) {
  let l, e;
  return {
    c() {
      l = ft("svg"), e = ft("path"), Cl(e, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), Cl(l, "xmlns", "http://www.w3.org/2000/svg"), Cl(l, "viewBox", "0 0 24 24");
    },
    m(n, i) {
      Ri(n, l, i), Ii(l, e);
    },
    p: ql,
    i: ql,
    o: ql,
    d(n) {
      n && Hi(l);
    }
  };
}
class $t extends Pi {
  constructor(l) {
    super(), Ji(this, l, null, Yi, Xi, {});
  }
}
const Gi = [
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
], ot = {
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
Gi.reduce(
  (t, { color: l, primary: e, secondary: n }) => ({
    ...t,
    [l]: {
      primary: ot[l][e],
      secondary: ot[l][n]
    }
  }),
  {}
);
function Ki(t, l) {
  return (t % l + l) % l;
}
function zl(t, l) {
  return t.reduce((e, n, i) => ((!l || n[0].toLowerCase().includes(l.toLowerCase())) && e.push(i), e), []);
}
function en(t, l, e) {
  t("change", l), e || t("input");
}
function ln(t, l, e) {
  if (t.key === "Escape")
    return [!1, l];
  if ((t.key === "ArrowDown" || t.key === "ArrowUp") && e.length >= 0)
    if (l === null)
      l = t.key === "ArrowDown" ? e[0] : e[e.length - 1];
    else {
      const n = e.indexOf(l), i = t.key === "ArrowUp" ? -1 : 1;
      l = e[Ki(n + i, e.length)];
    }
  return [!0, l];
}
const {
  SvelteComponent: Qi,
  append: Ne,
  attr: x,
  binding_callbacks: Wi,
  check_outros: xi,
  create_component: Ml,
  destroy_component: Ol,
  detach: Ul,
  element: Be,
  group_outros: $i,
  init: es,
  insert: Zl,
  listen: Xe,
  mount_component: Al,
  run_all: ls,
  safe_not_equal: ts,
  set_data: ns,
  set_input_value: ut,
  space: Sl,
  text: is,
  toggle_class: Oe,
  transition_in: Te,
  transition_out: Ge
} = window.__gradio__svelte__internal, { createEventDispatcher: ss, afterUpdate: fs } = window.__gradio__svelte__internal;
function os(t) {
  let l;
  return {
    c() {
      l = is(
        /*label*/
        t[0]
      );
    },
    m(e, n) {
      Zl(e, l, n);
    },
    p(e, n) {
      n[0] & /*label*/
      1 && ns(
        l,
        /*label*/
        e[0]
      );
    },
    d(e) {
      e && Ul(l);
    }
  };
}
function rt(t) {
  let l, e, n;
  return e = new xt({}), {
    c() {
      l = Be("div"), Ml(e.$$.fragment), x(l, "class", "icon-wrap svelte-1m1zvyj");
    },
    m(i, o) {
      Zl(i, l, o), Al(e, l, null), n = !0;
    },
    i(i) {
      n || (Te(e.$$.fragment, i), n = !0);
    },
    o(i) {
      Ge(e.$$.fragment, i), n = !1;
    },
    d(i) {
      i && Ul(l), Ol(e);
    }
  };
}
function us(t) {
  let l, e, n, i, o, u, f, s, r, a, m, v, h, y;
  e = new Wt({
    props: {
      show_label: (
        /*show_label*/
        t[4]
      ),
      info: (
        /*info*/
        t[1]
      ),
      $$slots: { default: [os] },
      $$scope: { ctx: t }
    }
  });
  let b = !/*disabled*/
  t[3] && rt();
  return m = new Gt({
    props: {
      show_options: (
        /*show_options*/
        t[12]
      ),
      choices: (
        /*choices*/
        t[2]
      ),
      filtered_indices: (
        /*filtered_indices*/
        t[10]
      ),
      disabled: (
        /*disabled*/
        t[3]
      ),
      selected_indices: (
        /*selected_index*/
        t[11] === null ? [] : [
          /*selected_index*/
          t[11]
        ]
      ),
      active_index: (
        /*active_index*/
        t[14]
      )
    }
  }), m.$on(
    "change",
    /*handle_option_selected*/
    t[16]
  ), {
    c() {
      l = Be("div"), Ml(e.$$.fragment), n = Sl(), i = Be("div"), o = Be("div"), u = Be("div"), f = Be("input"), r = Sl(), b && b.c(), a = Sl(), Ml(m.$$.fragment), x(f, "role", "listbox"), x(f, "aria-controls", "dropdown-options"), x(
        f,
        "aria-expanded",
        /*show_options*/
        t[12]
      ), x(
        f,
        "aria-label",
        /*label*/
        t[0]
      ), x(f, "class", "border-none svelte-1m1zvyj"), f.disabled = /*disabled*/
      t[3], x(f, "autocomplete", "off"), f.readOnly = s = !/*filterable*/
      t[7], Oe(f, "subdued", !/*choices_names*/
      t[13].includes(
        /*input_text*/
        t[9]
      ) && !/*allow_custom_value*/
      t[6]), x(u, "class", "secondary-wrap svelte-1m1zvyj"), x(o, "class", "wrap-inner svelte-1m1zvyj"), Oe(
        o,
        "show_options",
        /*show_options*/
        t[12]
      ), x(i, "class", "wrap svelte-1m1zvyj"), x(l, "class", "svelte-1m1zvyj"), Oe(
        l,
        "container",
        /*container*/
        t[5]
      );
    },
    m(c, d) {
      Zl(c, l, d), Al(e, l, null), Ne(l, n), Ne(l, i), Ne(i, o), Ne(o, u), Ne(u, f), ut(
        f,
        /*input_text*/
        t[9]
      ), t[29](f), Ne(u, r), b && b.m(u, null), Ne(i, a), Al(m, i, null), v = !0, h || (y = [
        Xe(
          f,
          "input",
          /*input_input_handler*/
          t[28]
        ),
        Xe(
          f,
          "keydown",
          /*handle_key_down*/
          t[19]
        ),
        Xe(
          f,
          "keyup",
          /*keyup_handler*/
          t[30]
        ),
        Xe(
          f,
          "blur",
          /*handle_blur*/
          t[18]
        ),
        Xe(
          f,
          "focus",
          /*handle_focus*/
          t[17]
        )
      ], h = !0);
    },
    p(c, d) {
      const j = {};
      d[0] & /*show_label*/
      16 && (j.show_label = /*show_label*/
      c[4]), d[0] & /*info*/
      2 && (j.info = /*info*/
      c[1]), d[0] & /*label*/
      1 | d[1] & /*$$scope*/
      4 && (j.$$scope = { dirty: d, ctx: c }), e.$set(j), (!v || d[0] & /*show_options*/
      4096) && x(
        f,
        "aria-expanded",
        /*show_options*/
        c[12]
      ), (!v || d[0] & /*label*/
      1) && x(
        f,
        "aria-label",
        /*label*/
        c[0]
      ), (!v || d[0] & /*disabled*/
      8) && (f.disabled = /*disabled*/
      c[3]), (!v || d[0] & /*filterable*/
      128 && s !== (s = !/*filterable*/
      c[7])) && (f.readOnly = s), d[0] & /*input_text*/
      512 && f.value !== /*input_text*/
      c[9] && ut(
        f,
        /*input_text*/
        c[9]
      ), (!v || d[0] & /*choices_names, input_text, allow_custom_value*/
      8768) && Oe(f, "subdued", !/*choices_names*/
      c[13].includes(
        /*input_text*/
        c[9]
      ) && !/*allow_custom_value*/
      c[6]), /*disabled*/
      c[3] ? b && ($i(), Ge(b, 1, 1, () => {
        b = null;
      }), xi()) : b ? d[0] & /*disabled*/
      8 && Te(b, 1) : (b = rt(), b.c(), Te(b, 1), b.m(u, null)), (!v || d[0] & /*show_options*/
      4096) && Oe(
        o,
        "show_options",
        /*show_options*/
        c[12]
      );
      const _ = {};
      d[0] & /*show_options*/
      4096 && (_.show_options = /*show_options*/
      c[12]), d[0] & /*choices*/
      4 && (_.choices = /*choices*/
      c[2]), d[0] & /*filtered_indices*/
      1024 && (_.filtered_indices = /*filtered_indices*/
      c[10]), d[0] & /*disabled*/
      8 && (_.disabled = /*disabled*/
      c[3]), d[0] & /*selected_index*/
      2048 && (_.selected_indices = /*selected_index*/
      c[11] === null ? [] : [
        /*selected_index*/
        c[11]
      ]), d[0] & /*active_index*/
      16384 && (_.active_index = /*active_index*/
      c[14]), m.$set(_), (!v || d[0] & /*container*/
      32) && Oe(
        l,
        "container",
        /*container*/
        c[5]
      );
    },
    i(c) {
      v || (Te(e.$$.fragment, c), Te(b), Te(m.$$.fragment, c), v = !0);
    },
    o(c) {
      Ge(e.$$.fragment, c), Ge(b), Ge(m.$$.fragment, c), v = !1;
    },
    d(c) {
      c && Ul(l), Ol(e), t[29](null), b && b.d(), Ol(m), h = !1, ls(y);
    }
  };
}
function rs(t, l, e) {
  let { label: n } = l, { info: i = void 0 } = l, { value: o = [] } = l, u = [], { value_is_output: f = !1 } = l, { choices: s } = l, r, { disabled: a = !1 } = l, { show_label: m } = l, { container: v = !0 } = l, { allow_custom_value: h = !1 } = l, { filterable: y = !0 } = l, b, c = !1, d, j, _ = "", w = "", S = !1, p = [], N = null, q = null, E;
  const B = ss();
  o ? (E = s.map((g) => g[1]).indexOf(o), q = E, q === -1 ? (u = o, q = null) : ([_, u] = s[q], w = _), le()) : s.length > 0 && (E = 0, q = 0, [_, o] = s[q], u = o, w = _);
  function T() {
    e(13, d = s.map((g) => g[0])), e(24, j = s.map((g) => g[1]));
  }
  function le() {
    T(), o === void 0 ? (e(9, _ = ""), e(11, q = null)) : j.includes(o) ? (e(9, _ = d[j.indexOf(o)]), e(11, q = j.indexOf(o))) : h ? (e(9, _ = o), e(11, q = null)) : (e(9, _ = ""), e(11, q = null)), e(27, E = q);
  }
  function F(g) {
    if (e(11, q = parseInt(g.detail.target.dataset.index)), isNaN(q)) {
      e(11, q = null);
      return;
    }
    e(12, c = !1), e(14, N = null), b.blur();
  }
  function I(g) {
    e(10, p = s.map((X, Y) => Y)), e(12, c = !0), B("focus");
  }
  function H() {
    h ? e(20, o = _) : e(9, _ = d[j.indexOf(o)]), e(12, c = !1), e(14, N = null), B("blur");
  }
  function ce(g) {
    e(12, [c, N] = ln(g, N, p), c, (e(14, N), e(2, s), e(23, r), e(6, h), e(9, _), e(10, p), e(8, b), e(25, w), e(11, q), e(27, E), e(26, S), e(24, j))), g.key === "Enter" && (N !== null ? (e(11, q = N), e(12, c = !1), b.blur(), e(14, N = null)) : d.includes(_) ? (e(11, q = d.indexOf(_)), e(12, c = !1), e(14, N = null), b.blur()) : h && (e(20, o = _), e(11, q = null), e(12, c = !1), e(14, N = null), b.blur()));
  }
  fs(() => {
    e(21, f = !1), e(26, S = !0);
  });
  function we() {
    _ = this.value, e(9, _), e(11, q), e(27, E), e(26, S), e(2, s), e(24, j);
  }
  function pe(g) {
    Wi[g ? "unshift" : "push"](() => {
      b = g, e(8, b);
    });
  }
  const ke = (g) => B("key_up", { key: g.key, input_value: _ });
  return t.$$set = (g) => {
    "label" in g && e(0, n = g.label), "info" in g && e(1, i = g.info), "value" in g && e(20, o = g.value), "value_is_output" in g && e(21, f = g.value_is_output), "choices" in g && e(2, s = g.choices), "disabled" in g && e(3, a = g.disabled), "show_label" in g && e(4, m = g.show_label), "container" in g && e(5, v = g.container), "allow_custom_value" in g && e(6, h = g.allow_custom_value), "filterable" in g && e(7, y = g.filterable);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*selected_index, old_selected_index, initialized, choices, choices_values*/
    218105860 && q !== E && q !== null && S && (e(9, [_, o] = s[q], _, (e(20, o), e(11, q), e(27, E), e(26, S), e(2, s), e(24, j))), e(27, E = q), B("select", {
      index: q,
      value: j[q],
      selected: !0
    })), t.$$.dirty[0] & /*value, old_value, value_is_output*/
    7340032 && o != u && (le(), en(B, o, f), e(22, u = o)), t.$$.dirty[0] & /*choices*/
    4 && T(), t.$$.dirty[0] & /*choices, old_choices, allow_custom_value, input_text, filtered_indices, filter_input*/
    8390468 && s !== r && (h || le(), e(23, r = s), e(10, p = zl(s, _)), !h && p.length > 0 && e(14, N = p[0]), b == document.activeElement && e(12, c = !0)), t.$$.dirty[0] & /*input_text, old_input_text, choices, allow_custom_value, filtered_indices*/
    33556036 && _ !== w && (e(10, p = zl(s, _)), e(25, w = _), !h && p.length > 0 && e(14, N = p[0]));
  }, [
    n,
    i,
    s,
    a,
    m,
    v,
    h,
    y,
    b,
    _,
    p,
    q,
    c,
    d,
    N,
    B,
    F,
    I,
    H,
    ce,
    o,
    f,
    u,
    r,
    j,
    w,
    S,
    E,
    we,
    pe,
    ke
  ];
}
class as extends Qi {
  constructor(l) {
    super(), es(
      this,
      l,
      rs,
      us,
      ts,
      {
        label: 0,
        info: 1,
        value: 20,
        value_is_output: 21,
        choices: 2,
        disabled: 3,
        show_label: 4,
        container: 5,
        allow_custom_value: 6,
        filterable: 7
      },
      null,
      [-1, -1]
    );
  }
}
function Ue(t) {
  let l = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; t > 1e3 && e < l.length - 1; )
    t /= 1e3, e++;
  let n = l[e];
  return (Number.isInteger(t) ? t : t.toFixed(1)) + n;
}
const {
  SvelteComponent: _s,
  append: ie,
  attr: O,
  component_subscribe: at,
  detach: cs,
  element: ds,
  init: ms,
  insert: bs,
  noop: _t,
  safe_not_equal: hs,
  set_style: nl,
  svg_element: se,
  toggle_class: ct
} = window.__gradio__svelte__internal, { onMount: gs } = window.__gradio__svelte__internal;
function ws(t) {
  let l, e, n, i, o, u, f, s, r, a, m, v;
  return {
    c() {
      l = ds("div"), e = se("svg"), n = se("g"), i = se("path"), o = se("path"), u = se("path"), f = se("path"), s = se("g"), r = se("path"), a = se("path"), m = se("path"), v = se("path"), O(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), O(i, "fill", "#FF7C00"), O(i, "fill-opacity", "0.4"), O(i, "class", "svelte-43sxxs"), O(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), O(o, "fill", "#FF7C00"), O(o, "class", "svelte-43sxxs"), O(u, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), O(u, "fill", "#FF7C00"), O(u, "fill-opacity", "0.4"), O(u, "class", "svelte-43sxxs"), O(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), O(f, "fill", "#FF7C00"), O(f, "class", "svelte-43sxxs"), nl(n, "transform", "translate(" + /*$top*/
      t[1][0] + "px, " + /*$top*/
      t[1][1] + "px)"), O(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), O(r, "fill", "#FF7C00"), O(r, "fill-opacity", "0.4"), O(r, "class", "svelte-43sxxs"), O(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), O(a, "fill", "#FF7C00"), O(a, "class", "svelte-43sxxs"), O(m, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), O(m, "fill", "#FF7C00"), O(m, "fill-opacity", "0.4"), O(m, "class", "svelte-43sxxs"), O(v, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), O(v, "fill", "#FF7C00"), O(v, "class", "svelte-43sxxs"), nl(s, "transform", "translate(" + /*$bottom*/
      t[2][0] + "px, " + /*$bottom*/
      t[2][1] + "px)"), O(e, "viewBox", "-1200 -1200 3000 3000"), O(e, "fill", "none"), O(e, "xmlns", "http://www.w3.org/2000/svg"), O(e, "class", "svelte-43sxxs"), O(l, "class", "svelte-43sxxs"), ct(
        l,
        "margin",
        /*margin*/
        t[0]
      );
    },
    m(h, y) {
      bs(h, l, y), ie(l, e), ie(e, n), ie(n, i), ie(n, o), ie(n, u), ie(n, f), ie(e, s), ie(s, r), ie(s, a), ie(s, m), ie(s, v);
    },
    p(h, [y]) {
      y & /*$top*/
      2 && nl(n, "transform", "translate(" + /*$top*/
      h[1][0] + "px, " + /*$top*/
      h[1][1] + "px)"), y & /*$bottom*/
      4 && nl(s, "transform", "translate(" + /*$bottom*/
      h[2][0] + "px, " + /*$bottom*/
      h[2][1] + "px)"), y & /*margin*/
      1 && ct(
        l,
        "margin",
        /*margin*/
        h[0]
      );
    },
    i: _t,
    o: _t,
    d(h) {
      h && cs(l);
    }
  };
}
function ps(t, l, e) {
  let n, i;
  var o = this && this.__awaiter || function(h, y, b, c) {
    function d(j) {
      return j instanceof b ? j : new b(function(_) {
        _(j);
      });
    }
    return new (b || (b = Promise))(function(j, _) {
      function w(N) {
        try {
          p(c.next(N));
        } catch (q) {
          _(q);
        }
      }
      function S(N) {
        try {
          p(c.throw(N));
        } catch (q) {
          _(q);
        }
      }
      function p(N) {
        N.done ? j(N.value) : d(N.value).then(w, S);
      }
      p((c = c.apply(h, y || [])).next());
    });
  };
  let { margin: u = !0 } = l;
  const f = Gl([0, 0]);
  at(t, f, (h) => e(1, n = h));
  const s = Gl([0, 0]);
  at(t, s, (h) => e(2, i = h));
  let r;
  function a() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 140]), s.set([-125, -140])]), yield Promise.all([f.set([-125, 140]), s.set([125, -140])]), yield Promise.all([f.set([-125, 0]), s.set([125, -0])]), yield Promise.all([f.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function m() {
    return o(this, void 0, void 0, function* () {
      yield a(), r || m();
    });
  }
  function v() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 0]), s.set([-125, 0])]), m();
    });
  }
  return gs(() => (v(), () => r = !0)), t.$$set = (h) => {
    "margin" in h && e(0, u = h.margin);
  }, [u, n, i, f, s];
}
class ks extends _s {
  constructor(l) {
    super(), ms(this, l, ps, ws, hs, { margin: 0 });
  }
}
const {
  SvelteComponent: vs,
  append: Fe,
  attr: re,
  binding_callbacks: dt,
  check_outros: tn,
  create_component: ys,
  create_slot: js,
  destroy_component: Cs,
  destroy_each: nn,
  detach: L,
  element: be,
  empty: Re,
  ensure_array_like: al,
  get_all_dirty_from_scope: qs,
  get_slot_changes: Ss,
  group_outros: sn,
  init: Es,
  insert: z,
  mount_component: Ns,
  noop: Vl,
  safe_not_equal: Fs,
  set_data: ne,
  set_style: Ce,
  space: ae,
  text: D,
  toggle_class: te,
  transition_in: He,
  transition_out: Je,
  update_slot_base: Ls
} = window.__gradio__svelte__internal, { tick: zs } = window.__gradio__svelte__internal, { onDestroy: Ms } = window.__gradio__svelte__internal, Os = (t) => ({}), mt = (t) => ({});
function bt(t, l, e) {
  const n = t.slice();
  return n[39] = l[e], n[41] = e, n;
}
function ht(t, l, e) {
  const n = t.slice();
  return n[39] = l[e], n;
}
function As(t) {
  let l, e = (
    /*i18n*/
    t[1]("common.error") + ""
  ), n, i, o;
  const u = (
    /*#slots*/
    t[29].error
  ), f = js(
    u,
    t,
    /*$$scope*/
    t[28],
    mt
  );
  return {
    c() {
      l = be("span"), n = D(e), i = ae(), f && f.c(), re(l, "class", "error svelte-1yserjw");
    },
    m(s, r) {
      z(s, l, r), Fe(l, n), z(s, i, r), f && f.m(s, r), o = !0;
    },
    p(s, r) {
      (!o || r[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      s[1]("common.error") + "") && ne(n, e), f && f.p && (!o || r[0] & /*$$scope*/
      268435456) && Ls(
        f,
        u,
        s,
        /*$$scope*/
        s[28],
        o ? Ss(
          u,
          /*$$scope*/
          s[28],
          r,
          Os
        ) : qs(
          /*$$scope*/
          s[28]
        ),
        mt
      );
    },
    i(s) {
      o || (He(f, s), o = !0);
    },
    o(s) {
      Je(f, s), o = !1;
    },
    d(s) {
      s && (L(l), L(i)), f && f.d(s);
    }
  };
}
function Vs(t) {
  let l, e, n, i, o, u, f, s, r, a = (
    /*variant*/
    t[8] === "default" && /*show_eta_bar*/
    t[18] && /*show_progress*/
    t[6] === "full" && gt(t)
  );
  function m(_, w) {
    if (
      /*progress*/
      _[7]
    ) return Ts;
    if (
      /*queue_position*/
      _[2] !== null && /*queue_size*/
      _[3] !== void 0 && /*queue_position*/
      _[2] >= 0
    ) return Bs;
    if (
      /*queue_position*/
      _[2] === 0
    ) return Ds;
  }
  let v = m(t), h = v && v(t), y = (
    /*timer*/
    t[5] && kt(t)
  );
  const b = [Is, Ps], c = [];
  function d(_, w) {
    return (
      /*last_progress_level*/
      _[15] != null ? 0 : (
        /*show_progress*/
        _[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = d(t)) && (u = c[o] = b[o](t));
  let j = !/*timer*/
  t[5] && Et(t);
  return {
    c() {
      a && a.c(), l = ae(), e = be("div"), h && h.c(), n = ae(), y && y.c(), i = ae(), u && u.c(), f = ae(), j && j.c(), s = Re(), re(e, "class", "progress-text svelte-1yserjw"), te(
        e,
        "meta-text-center",
        /*variant*/
        t[8] === "center"
      ), te(
        e,
        "meta-text",
        /*variant*/
        t[8] === "default"
      );
    },
    m(_, w) {
      a && a.m(_, w), z(_, l, w), z(_, e, w), h && h.m(e, null), Fe(e, n), y && y.m(e, null), z(_, i, w), ~o && c[o].m(_, w), z(_, f, w), j && j.m(_, w), z(_, s, w), r = !0;
    },
    p(_, w) {
      /*variant*/
      _[8] === "default" && /*show_eta_bar*/
      _[18] && /*show_progress*/
      _[6] === "full" ? a ? a.p(_, w) : (a = gt(_), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null), v === (v = m(_)) && h ? h.p(_, w) : (h && h.d(1), h = v && v(_), h && (h.c(), h.m(e, n))), /*timer*/
      _[5] ? y ? y.p(_, w) : (y = kt(_), y.c(), y.m(e, null)) : y && (y.d(1), y = null), (!r || w[0] & /*variant*/
      256) && te(
        e,
        "meta-text-center",
        /*variant*/
        _[8] === "center"
      ), (!r || w[0] & /*variant*/
      256) && te(
        e,
        "meta-text",
        /*variant*/
        _[8] === "default"
      );
      let S = o;
      o = d(_), o === S ? ~o && c[o].p(_, w) : (u && (sn(), Je(c[S], 1, 1, () => {
        c[S] = null;
      }), tn()), ~o ? (u = c[o], u ? u.p(_, w) : (u = c[o] = b[o](_), u.c()), He(u, 1), u.m(f.parentNode, f)) : u = null), /*timer*/
      _[5] ? j && (j.d(1), j = null) : j ? j.p(_, w) : (j = Et(_), j.c(), j.m(s.parentNode, s));
    },
    i(_) {
      r || (He(u), r = !0);
    },
    o(_) {
      Je(u), r = !1;
    },
    d(_) {
      _ && (L(l), L(e), L(i), L(f), L(s)), a && a.d(_), h && h.d(), y && y.d(), ~o && c[o].d(_), j && j.d(_);
    }
  };
}
function gt(t) {
  let l, e = `translateX(${/*eta_level*/
  (t[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      l = be("div"), re(l, "class", "eta-bar svelte-1yserjw"), Ce(l, "transform", e);
    },
    m(n, i) {
      z(n, l, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Ce(l, "transform", e);
    },
    d(n) {
      n && L(l);
    }
  };
}
function Ds(t) {
  let l;
  return {
    c() {
      l = D("processing |");
    },
    m(e, n) {
      z(e, l, n);
    },
    p: Vl,
    d(e) {
      e && L(l);
    }
  };
}
function Bs(t) {
  let l, e = (
    /*queue_position*/
    t[2] + 1 + ""
  ), n, i, o, u;
  return {
    c() {
      l = D("queue: "), n = D(e), i = D("/"), o = D(
        /*queue_size*/
        t[3]
      ), u = D(" |");
    },
    m(f, s) {
      z(f, l, s), z(f, n, s), z(f, i, s), z(f, o, s), z(f, u, s);
    },
    p(f, s) {
      s[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      f[2] + 1 + "") && ne(n, e), s[0] & /*queue_size*/
      8 && ne(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (L(l), L(n), L(i), L(o), L(u));
    }
  };
}
function Ts(t) {
  let l, e = al(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < e.length; i += 1)
    n[i] = pt(ht(t, e, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      l = Re();
    },
    m(i, o) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, o);
      z(i, l, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        e = al(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < e.length; u += 1) {
          const f = ht(i, e, u);
          n[u] ? n[u].p(f, o) : (n[u] = pt(f), n[u].c(), n[u].m(l.parentNode, l));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = e.length;
      }
    },
    d(i) {
      i && L(l), nn(n, i);
    }
  };
}
function wt(t) {
  let l, e = (
    /*p*/
    t[39].unit + ""
  ), n, i, o = " ", u;
  function f(a, m) {
    return (
      /*p*/
      a[39].length != null ? Zs : Us
    );
  }
  let s = f(t), r = s(t);
  return {
    c() {
      r.c(), l = ae(), n = D(e), i = D(" | "), u = D(o);
    },
    m(a, m) {
      r.m(a, m), z(a, l, m), z(a, n, m), z(a, i, m), z(a, u, m);
    },
    p(a, m) {
      s === (s = f(a)) && r ? r.p(a, m) : (r.d(1), r = s(a), r && (r.c(), r.m(l.parentNode, l))), m[0] & /*progress*/
      128 && e !== (e = /*p*/
      a[39].unit + "") && ne(n, e);
    },
    d(a) {
      a && (L(l), L(n), L(i), L(u)), r.d(a);
    }
  };
}
function Us(t) {
  let l = Ue(
    /*p*/
    t[39].index || 0
  ) + "", e;
  return {
    c() {
      e = D(l);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && l !== (l = Ue(
        /*p*/
        n[39].index || 0
      ) + "") && ne(e, l);
    },
    d(n) {
      n && L(e);
    }
  };
}
function Zs(t) {
  let l = Ue(
    /*p*/
    t[39].index || 0
  ) + "", e, n, i = Ue(
    /*p*/
    t[39].length
  ) + "", o;
  return {
    c() {
      e = D(l), n = D("/"), o = D(i);
    },
    m(u, f) {
      z(u, e, f), z(u, n, f), z(u, o, f);
    },
    p(u, f) {
      f[0] & /*progress*/
      128 && l !== (l = Ue(
        /*p*/
        u[39].index || 0
      ) + "") && ne(e, l), f[0] & /*progress*/
      128 && i !== (i = Ue(
        /*p*/
        u[39].length
      ) + "") && ne(o, i);
    },
    d(u) {
      u && (L(e), L(n), L(o));
    }
  };
}
function pt(t) {
  let l, e = (
    /*p*/
    t[39].index != null && wt(t)
  );
  return {
    c() {
      e && e.c(), l = Re();
    },
    m(n, i) {
      e && e.m(n, i), z(n, l, i);
    },
    p(n, i) {
      /*p*/
      n[39].index != null ? e ? e.p(n, i) : (e = wt(n), e.c(), e.m(l.parentNode, l)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && L(l), e && e.d(n);
    }
  };
}
function kt(t) {
  let l, e = (
    /*eta*/
    t[0] ? `/${/*formatted_eta*/
    t[19]}` : ""
  ), n, i;
  return {
    c() {
      l = D(
        /*formatted_timer*/
        t[20]
      ), n = D(e), i = D("s");
    },
    m(o, u) {
      z(o, l, u), z(o, n, u), z(o, i, u);
    },
    p(o, u) {
      u[0] & /*formatted_timer*/
      1048576 && ne(
        l,
        /*formatted_timer*/
        o[20]
      ), u[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && ne(n, e);
    },
    d(o) {
      o && (L(l), L(n), L(i));
    }
  };
}
function Ps(t) {
  let l, e;
  return l = new ks({
    props: { margin: (
      /*variant*/
      t[8] === "default"
    ) }
  }), {
    c() {
      ys(l.$$.fragment);
    },
    m(n, i) {
      Ns(l, n, i), e = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), l.$set(o);
    },
    i(n) {
      e || (He(l.$$.fragment, n), e = !0);
    },
    o(n) {
      Je(l.$$.fragment, n), e = !1;
    },
    d(n) {
      Cs(l, n);
    }
  };
}
function Is(t) {
  let l, e, n, i, o, u = `${/*last_progress_level*/
  t[15] * 100}%`, f = (
    /*progress*/
    t[7] != null && vt(t)
  );
  return {
    c() {
      l = be("div"), e = be("div"), f && f.c(), n = ae(), i = be("div"), o = be("div"), re(e, "class", "progress-level-inner svelte-1yserjw"), re(o, "class", "progress-bar svelte-1yserjw"), Ce(o, "width", u), re(i, "class", "progress-bar-wrap svelte-1yserjw"), re(l, "class", "progress-level svelte-1yserjw");
    },
    m(s, r) {
      z(s, l, r), Fe(l, e), f && f.m(e, null), Fe(l, n), Fe(l, i), Fe(i, o), t[30](o);
    },
    p(s, r) {
      /*progress*/
      s[7] != null ? f ? f.p(s, r) : (f = vt(s), f.c(), f.m(e, null)) : f && (f.d(1), f = null), r[0] & /*last_progress_level*/
      32768 && u !== (u = `${/*last_progress_level*/
      s[15] * 100}%`) && Ce(o, "width", u);
    },
    i: Vl,
    o: Vl,
    d(s) {
      s && L(l), f && f.d(), t[30](null);
    }
  };
}
function vt(t) {
  let l, e = al(
    /*progress*/
    t[7]
  ), n = [];
  for (let i = 0; i < e.length; i += 1)
    n[i] = St(bt(t, e, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      l = Re();
    },
    m(i, o) {
      for (let u = 0; u < n.length; u += 1)
        n[u] && n[u].m(i, o);
      z(i, l, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        e = al(
          /*progress*/
          i[7]
        );
        let u;
        for (u = 0; u < e.length; u += 1) {
          const f = bt(i, e, u);
          n[u] ? n[u].p(f, o) : (n[u] = St(f), n[u].c(), n[u].m(l.parentNode, l));
        }
        for (; u < n.length; u += 1)
          n[u].d(1);
        n.length = e.length;
      }
    },
    d(i) {
      i && L(l), nn(n, i);
    }
  };
}
function yt(t) {
  let l, e, n, i, o = (
    /*i*/
    t[41] !== 0 && Hs()
  ), u = (
    /*p*/
    t[39].desc != null && jt(t)
  ), f = (
    /*p*/
    t[39].desc != null && /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[41]
    ] != null && Ct()
  ), s = (
    /*progress_level*/
    t[14] != null && qt(t)
  );
  return {
    c() {
      o && o.c(), l = ae(), u && u.c(), e = ae(), f && f.c(), n = ae(), s && s.c(), i = Re();
    },
    m(r, a) {
      o && o.m(r, a), z(r, l, a), u && u.m(r, a), z(r, e, a), f && f.m(r, a), z(r, n, a), s && s.m(r, a), z(r, i, a);
    },
    p(r, a) {
      /*p*/
      r[39].desc != null ? u ? u.p(r, a) : (u = jt(r), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), /*p*/
      r[39].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[41]
      ] != null ? f || (f = Ct(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      r[14] != null ? s ? s.p(r, a) : (s = qt(r), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(r) {
      r && (L(l), L(e), L(n), L(i)), o && o.d(r), u && u.d(r), f && f.d(r), s && s.d(r);
    }
  };
}
function Hs(t) {
  let l;
  return {
    c() {
      l = D(" /");
    },
    m(e, n) {
      z(e, l, n);
    },
    d(e) {
      e && L(l);
    }
  };
}
function jt(t) {
  let l = (
    /*p*/
    t[39].desc + ""
  ), e;
  return {
    c() {
      e = D(l);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && l !== (l = /*p*/
      n[39].desc + "") && ne(e, l);
    },
    d(n) {
      n && L(e);
    }
  };
}
function Ct(t) {
  let l;
  return {
    c() {
      l = D("-");
    },
    m(e, n) {
      z(e, l, n);
    },
    d(e) {
      e && L(l);
    }
  };
}
function qt(t) {
  let l = (100 * /*progress_level*/
  (t[14][
    /*i*/
    t[41]
  ] || 0)).toFixed(1) + "", e, n;
  return {
    c() {
      e = D(l), n = D("%");
    },
    m(i, o) {
      z(i, e, o), z(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && l !== (l = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[41]
      ] || 0)).toFixed(1) + "") && ne(e, l);
    },
    d(i) {
      i && (L(e), L(n));
    }
  };
}
function St(t) {
  let l, e = (
    /*p*/
    (t[39].desc != null || /*progress_level*/
    t[14] && /*progress_level*/
    t[14][
      /*i*/
      t[41]
    ] != null) && yt(t)
  );
  return {
    c() {
      e && e.c(), l = Re();
    },
    m(n, i) {
      e && e.m(n, i), z(n, l, i);
    },
    p(n, i) {
      /*p*/
      n[39].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[41]
      ] != null ? e ? e.p(n, i) : (e = yt(n), e.c(), e.m(l.parentNode, l)) : e && (e.d(1), e = null);
    },
    d(n) {
      n && L(l), e && e.d(n);
    }
  };
}
function Et(t) {
  let l, e;
  return {
    c() {
      l = be("p"), e = D(
        /*loading_text*/
        t[9]
      ), re(l, "class", "loading svelte-1yserjw");
    },
    m(n, i) {
      z(n, l, i), Fe(l, e);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && ne(
        e,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && L(l);
    }
  };
}
function Js(t) {
  let l, e, n, i, o;
  const u = [Vs, As], f = [];
  function s(r, a) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = s(t)) && (n = f[e] = u[e](t)), {
    c() {
      l = be("div"), n && n.c(), re(l, "class", i = "wrap " + /*variant*/
      t[8] + " " + /*show_progress*/
      t[6] + " svelte-1yserjw"), te(l, "hide", !/*status*/
      t[4] || /*status*/
      t[4] === "complete" || /*show_progress*/
      t[6] === "hidden"), te(
        l,
        "translucent",
        /*variant*/
        t[8] === "center" && /*status*/
        (t[4] === "pending" || /*status*/
        t[4] === "error") || /*translucent*/
        t[11] || /*show_progress*/
        t[6] === "minimal"
      ), te(
        l,
        "generating",
        /*status*/
        t[4] === "generating"
      ), te(
        l,
        "border",
        /*border*/
        t[12]
      ), Ce(
        l,
        "position",
        /*absolute*/
        t[10] ? "absolute" : "static"
      ), Ce(
        l,
        "padding",
        /*absolute*/
        t[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, a) {
      z(r, l, a), ~e && f[e].m(l, null), t[31](l), o = !0;
    },
    p(r, a) {
      let m = e;
      e = s(r), e === m ? ~e && f[e].p(r, a) : (n && (sn(), Je(f[m], 1, 1, () => {
        f[m] = null;
      }), tn()), ~e ? (n = f[e], n ? n.p(r, a) : (n = f[e] = u[e](r), n.c()), He(n, 1), n.m(l, null)) : n = null), (!o || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-1yserjw")) && re(l, "class", i), (!o || a[0] & /*variant, show_progress, status, show_progress*/
      336) && te(l, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!o || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && te(
        l,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!o || a[0] & /*variant, show_progress, status*/
      336) && te(
        l,
        "generating",
        /*status*/
        r[4] === "generating"
      ), (!o || a[0] & /*variant, show_progress, border*/
      4416) && te(
        l,
        "border",
        /*border*/
        r[12]
      ), a[0] & /*absolute*/
      1024 && Ce(
        l,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && Ce(
        l,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      o || (He(n), o = !0);
    },
    o(r) {
      Je(n), o = !1;
    },
    d(r) {
      r && L(l), ~e && f[e].d(), t[31](null);
    }
  };
}
var Rs = function(t, l, e, n) {
  function i(o) {
    return o instanceof e ? o : new e(function(u) {
      u(o);
    });
  }
  return new (e || (e = Promise))(function(o, u) {
    function f(a) {
      try {
        r(n.next(a));
      } catch (m) {
        u(m);
      }
    }
    function s(a) {
      try {
        r(n.throw(a));
      } catch (m) {
        u(m);
      }
    }
    function r(a) {
      a.done ? o(a.value) : i(a.value).then(f, s);
    }
    r((n = n.apply(t, l || [])).next());
  });
};
let il = [], El = !1;
function Xs(t) {
  return Rs(this, arguments, void 0, function* (l, e = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
      if (il.push(l), !El) El = !0;
      else return;
      yield zs(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < il.length; i++) {
          const u = il[i].getBoundingClientRect();
          (i === 0 || u.top + window.scrollY <= n[0]) && (n[0] = u.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), El = !1, il = [];
      });
    }
  });
}
function Ys(t, l, e) {
  let n, { $$slots: i = {}, $$scope: o } = l;
  this && this.__awaiter;
  let { i18n: u } = l, { eta: f = null } = l, { queue_position: s } = l, { queue_size: r } = l, { status: a } = l, { scroll_to_output: m = !1 } = l, { timer: v = !0 } = l, { show_progress: h = "full" } = l, { message: y = null } = l, { progress: b = null } = l, { variant: c = "default" } = l, { loading_text: d = "Loading..." } = l, { absolute: j = !0 } = l, { translucent: _ = !1 } = l, { border: w = !1 } = l, { autoscroll: S } = l, p, N = !1, q = 0, E = 0, B = null, T = null, le = 0, F = null, I, H = null, ce = !0;
  const we = () => {
    e(0, f = e(26, B = e(19, g = null))), e(24, q = performance.now()), e(25, E = 0), N = !0, pe();
  };
  function pe() {
    requestAnimationFrame(() => {
      e(25, E = (performance.now() - q) / 1e3), N && pe();
    });
  }
  function ke() {
    e(25, E = 0), e(0, f = e(26, B = e(19, g = null))), N && (N = !1);
  }
  Ms(() => {
    N && ke();
  });
  let g = null;
  function X(C) {
    dt[C ? "unshift" : "push"](() => {
      H = C, e(16, H), e(7, b), e(14, F), e(15, I);
    });
  }
  function Y(C) {
    dt[C ? "unshift" : "push"](() => {
      p = C, e(13, p);
    });
  }
  return t.$$set = (C) => {
    "i18n" in C && e(1, u = C.i18n), "eta" in C && e(0, f = C.eta), "queue_position" in C && e(2, s = C.queue_position), "queue_size" in C && e(3, r = C.queue_size), "status" in C && e(4, a = C.status), "scroll_to_output" in C && e(21, m = C.scroll_to_output), "timer" in C && e(5, v = C.timer), "show_progress" in C && e(6, h = C.show_progress), "message" in C && e(22, y = C.message), "progress" in C && e(7, b = C.progress), "variant" in C && e(8, c = C.variant), "loading_text" in C && e(9, d = C.loading_text), "absolute" in C && e(10, j = C.absolute), "translucent" in C && e(11, _ = C.translucent), "border" in C && e(12, w = C.border), "autoscroll" in C && e(23, S = C.autoscroll), "$$scope" in C && e(28, o = C.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (f === null && e(0, f = B), f != null && B !== f && (e(27, T = (performance.now() - q) / 1e3 + f), e(19, g = T.toFixed(1)), e(26, B = f))), t.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && e(17, le = T === null || T <= 0 || !E ? null : Math.min(E / T, 1)), t.$$.dirty[0] & /*progress*/
    128 && b != null && e(18, ce = !1), t.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (b != null ? e(14, F = b.map((C) => {
      if (C.index != null && C.length != null)
        return C.index / C.length;
      if (C.progress != null)
        return C.progress;
    })) : e(14, F = null), F ? (e(15, I = F[F.length - 1]), H && (I === 0 ? e(16, H.style.transition = "0", H) : e(16, H.style.transition = "150ms", H))) : e(15, I = void 0)), t.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? we() : ke()), t.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && p && m && (a === "pending" || a === "complete") && Xs(p, S), t.$$.dirty[0] & /*status, message*/
    4194320, t.$$.dirty[0] & /*timer_diff*/
    33554432 && e(20, n = E.toFixed(1));
  }, [
    f,
    u,
    s,
    r,
    a,
    v,
    h,
    b,
    c,
    d,
    j,
    _,
    w,
    p,
    F,
    I,
    H,
    le,
    ce,
    g,
    n,
    m,
    y,
    S,
    q,
    E,
    B,
    T,
    o,
    i,
    X,
    Y
  ];
}
class Gs extends vs {
  constructor(l) {
    super(), Es(
      this,
      l,
      Ys,
      Js,
      Fs,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
class Ks {
  constructor({
    name: l,
    token: e,
    param_specs: n
  }) {
    this.name = l, this.token = e, this.param_specs = n || new Object();
  }
}
const {
  SvelteComponent: Qs,
  append: fn,
  attr: V,
  bubble: Ws,
  check_outros: xs,
  create_slot: on,
  detach: el,
  element: hl,
  empty: $s,
  get_all_dirty_from_scope: un,
  get_slot_changes: rn,
  group_outros: ef,
  init: lf,
  insert: ll,
  listen: tf,
  safe_not_equal: nf,
  set_style: G,
  space: an,
  src_url_equal: _l,
  toggle_class: Ze,
  transition_in: cl,
  transition_out: dl,
  update_slot_base: _n
} = window.__gradio__svelte__internal;
function sf(t) {
  let l, e, n, i, o, u, f = (
    /*icon*/
    t[7] && Nt(t)
  );
  const s = (
    /*#slots*/
    t[12].default
  ), r = on(
    s,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      l = hl("button"), f && f.c(), e = an(), r && r.c(), V(l, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), V(
        l,
        "id",
        /*elem_id*/
        t[0]
      ), l.disabled = /*disabled*/
      t[8], Ze(l, "hidden", !/*visible*/
      t[2]), G(
        l,
        "flex-grow",
        /*scale*/
        t[9]
      ), G(
        l,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), G(l, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(a, m) {
      ll(a, l, m), f && f.m(l, null), fn(l, e), r && r.m(l, null), i = !0, o || (u = tf(
        l,
        "click",
        /*click_handler*/
        t[13]
      ), o = !0);
    },
    p(a, m) {
      /*icon*/
      a[7] ? f ? f.p(a, m) : (f = Nt(a), f.c(), f.m(l, e)) : f && (f.d(1), f = null), r && r.p && (!i || m & /*$$scope*/
      2048) && _n(
        r,
        s,
        a,
        /*$$scope*/
        a[11],
        i ? rn(
          s,
          /*$$scope*/
          a[11],
          m,
          null
        ) : un(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || m & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && V(l, "class", n), (!i || m & /*elem_id*/
      1) && V(
        l,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || m & /*disabled*/
      256) && (l.disabled = /*disabled*/
      a[8]), (!i || m & /*size, variant, elem_classes, visible*/
      30) && Ze(l, "hidden", !/*visible*/
      a[2]), m & /*scale*/
      512 && G(
        l,
        "flex-grow",
        /*scale*/
        a[9]
      ), m & /*scale*/
      512 && G(
        l,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), m & /*min_width*/
      1024 && G(l, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (cl(r, a), i = !0);
    },
    o(a) {
      dl(r, a), i = !1;
    },
    d(a) {
      a && el(l), f && f.d(), r && r.d(a), o = !1, u();
    }
  };
}
function ff(t) {
  let l, e, n, i, o = (
    /*icon*/
    t[7] && Ft(t)
  );
  const u = (
    /*#slots*/
    t[12].default
  ), f = on(
    u,
    t,
    /*$$scope*/
    t[11],
    null
  );
  return {
    c() {
      l = hl("a"), o && o.c(), e = an(), f && f.c(), V(
        l,
        "href",
        /*link*/
        t[6]
      ), V(l, "rel", "noopener noreferrer"), V(
        l,
        "aria-disabled",
        /*disabled*/
        t[8]
      ), V(l, "class", n = /*size*/
      t[4] + " " + /*variant*/
      t[3] + " " + /*elem_classes*/
      t[1].join(" ") + " svelte-8huxfn"), V(
        l,
        "id",
        /*elem_id*/
        t[0]
      ), Ze(l, "hidden", !/*visible*/
      t[2]), Ze(
        l,
        "disabled",
        /*disabled*/
        t[8]
      ), G(
        l,
        "flex-grow",
        /*scale*/
        t[9]
      ), G(
        l,
        "pointer-events",
        /*disabled*/
        t[8] ? "none" : null
      ), G(
        l,
        "width",
        /*scale*/
        t[9] === 0 ? "fit-content" : null
      ), G(l, "min-width", typeof /*min_width*/
      t[10] == "number" ? `calc(min(${/*min_width*/
      t[10]}px, 100%))` : null);
    },
    m(s, r) {
      ll(s, l, r), o && o.m(l, null), fn(l, e), f && f.m(l, null), i = !0;
    },
    p(s, r) {
      /*icon*/
      s[7] ? o ? o.p(s, r) : (o = Ft(s), o.c(), o.m(l, e)) : o && (o.d(1), o = null), f && f.p && (!i || r & /*$$scope*/
      2048) && _n(
        f,
        u,
        s,
        /*$$scope*/
        s[11],
        i ? rn(
          u,
          /*$$scope*/
          s[11],
          r,
          null
        ) : un(
          /*$$scope*/
          s[11]
        ),
        null
      ), (!i || r & /*link*/
      64) && V(
        l,
        "href",
        /*link*/
        s[6]
      ), (!i || r & /*disabled*/
      256) && V(
        l,
        "aria-disabled",
        /*disabled*/
        s[8]
      ), (!i || r & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      s[4] + " " + /*variant*/
      s[3] + " " + /*elem_classes*/
      s[1].join(" ") + " svelte-8huxfn")) && V(l, "class", n), (!i || r & /*elem_id*/
      1) && V(
        l,
        "id",
        /*elem_id*/
        s[0]
      ), (!i || r & /*size, variant, elem_classes, visible*/
      30) && Ze(l, "hidden", !/*visible*/
      s[2]), (!i || r & /*size, variant, elem_classes, disabled*/
      282) && Ze(
        l,
        "disabled",
        /*disabled*/
        s[8]
      ), r & /*scale*/
      512 && G(
        l,
        "flex-grow",
        /*scale*/
        s[9]
      ), r & /*disabled*/
      256 && G(
        l,
        "pointer-events",
        /*disabled*/
        s[8] ? "none" : null
      ), r & /*scale*/
      512 && G(
        l,
        "width",
        /*scale*/
        s[9] === 0 ? "fit-content" : null
      ), r & /*min_width*/
      1024 && G(l, "min-width", typeof /*min_width*/
      s[10] == "number" ? `calc(min(${/*min_width*/
      s[10]}px, 100%))` : null);
    },
    i(s) {
      i || (cl(f, s), i = !0);
    },
    o(s) {
      dl(f, s), i = !1;
    },
    d(s) {
      s && el(l), o && o.d(), f && f.d(s);
    }
  };
}
function Nt(t) {
  let l, e, n;
  return {
    c() {
      l = hl("img"), V(l, "class", "button-icon svelte-8huxfn"), _l(l.src, e = /*icon*/
      t[7].url) || V(l, "src", e), V(l, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, o) {
      ll(i, l, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !_l(l.src, e = /*icon*/
      i[7].url) && V(l, "src", e), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && V(l, "alt", n);
    },
    d(i) {
      i && el(l);
    }
  };
}
function Ft(t) {
  let l, e, n;
  return {
    c() {
      l = hl("img"), V(l, "class", "button-icon svelte-8huxfn"), _l(l.src, e = /*icon*/
      t[7].url) || V(l, "src", e), V(l, "alt", n = `${/*value*/
      t[5]} icon`);
    },
    m(i, o) {
      ll(i, l, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !_l(l.src, e = /*icon*/
      i[7].url) && V(l, "src", e), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && V(l, "alt", n);
    },
    d(i) {
      i && el(l);
    }
  };
}
function of(t) {
  let l, e, n, i;
  const o = [ff, sf], u = [];
  function f(s, r) {
    return (
      /*link*/
      s[6] && /*link*/
      s[6].length > 0 ? 0 : 1
    );
  }
  return l = f(t), e = u[l] = o[l](t), {
    c() {
      e.c(), n = $s();
    },
    m(s, r) {
      u[l].m(s, r), ll(s, n, r), i = !0;
    },
    p(s, [r]) {
      let a = l;
      l = f(s), l === a ? u[l].p(s, r) : (ef(), dl(u[a], 1, 1, () => {
        u[a] = null;
      }), xs(), e = u[l], e ? e.p(s, r) : (e = u[l] = o[l](s), e.c()), cl(e, 1), e.m(n.parentNode, n));
    },
    i(s) {
      i || (cl(e), i = !0);
    },
    o(s) {
      dl(e), i = !1;
    },
    d(s) {
      s && el(n), u[l].d(s);
    }
  };
}
function uf(t, l, e) {
  let { $$slots: n = {}, $$scope: i } = l, { elem_id: o = "" } = l, { elem_classes: u = [] } = l, { visible: f = !0 } = l, { variant: s = "secondary" } = l, { size: r = "lg" } = l, { value: a = null } = l, { link: m = null } = l, { icon: v = null } = l, { disabled: h = !1 } = l, { scale: y = null } = l, { min_width: b = void 0 } = l;
  function c(d) {
    Ws.call(this, t, d);
  }
  return t.$$set = (d) => {
    "elem_id" in d && e(0, o = d.elem_id), "elem_classes" in d && e(1, u = d.elem_classes), "visible" in d && e(2, f = d.visible), "variant" in d && e(3, s = d.variant), "size" in d && e(4, r = d.size), "value" in d && e(5, a = d.value), "link" in d && e(6, m = d.link), "icon" in d && e(7, v = d.icon), "disabled" in d && e(8, h = d.disabled), "scale" in d && e(9, y = d.scale), "min_width" in d && e(10, b = d.min_width), "$$scope" in d && e(11, i = d.$$scope);
  }, [
    o,
    u,
    f,
    s,
    r,
    a,
    m,
    v,
    h,
    y,
    b,
    i,
    n,
    c
  ];
}
class rf extends Qs {
  constructor(l) {
    super(), lf(this, l, uf, of, nf, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
const {
  SvelteComponent: af,
  attr: _f,
  detach: cf,
  element: df,
  init: mf,
  insert: bf,
  noop: Lt,
  safe_not_equal: hf,
  toggle_class: Ae
} = window.__gradio__svelte__internal;
function gf(t) {
  let l;
  return {
    c() {
      l = df("div"), l.textContent = `${/*names_string*/
      t[2]}`, _f(l, "class", "svelte-1gecy8w"), Ae(
        l,
        "table",
        /*type*/
        t[0] === "table"
      ), Ae(
        l,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), Ae(
        l,
        "selected",
        /*selected*/
        t[1]
      );
    },
    m(e, n) {
      bf(e, l, n);
    },
    p(e, [n]) {
      n & /*type*/
      1 && Ae(
        l,
        "table",
        /*type*/
        e[0] === "table"
      ), n & /*type*/
      1 && Ae(
        l,
        "gallery",
        /*type*/
        e[0] === "gallery"
      ), n & /*selected*/
      2 && Ae(
        l,
        "selected",
        /*selected*/
        e[1]
      );
    },
    i: Lt,
    o: Lt,
    d(e) {
      e && cf(l);
    }
  };
}
function wf(t, l, e) {
  let { value: n } = l, { type: i } = l, { selected: o = !1 } = l, { choices: u } = l, r = (n ? Array.isArray(n) ? n : [n] : []).map((a) => {
    var m;
    return (m = u.find((v) => v[1] === a)) === null || m === void 0 ? void 0 : m[0];
  }).filter((a) => a !== void 0).join(", ");
  return t.$$set = (a) => {
    "value" in a && e(3, n = a.value), "type" in a && e(0, i = a.type), "selected" in a && e(1, o = a.selected), "choices" in a && e(4, u = a.choices);
  }, [i, o, r, n, u];
}
class Yf extends af {
  constructor(l) {
    super(), mf(this, l, wf, gf, hf, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
const {
  SvelteComponent: pf,
  append: oe,
  attr: P,
  binding_callbacks: kf,
  check_outros: ml,
  create_component: We,
  destroy_component: xe,
  destroy_each: vf,
  detach: he,
  element: ue,
  ensure_array_like: zt,
  group_outros: bl,
  init: yf,
  insert: ge,
  listen: de,
  mount_component: $e,
  prevent_default: Mt,
  run_all: Pl,
  safe_not_equal: jf,
  set_data: Il,
  set_input_value: Ot,
  space: Pe,
  text: Hl,
  toggle_class: Ve,
  transition_in: J,
  transition_out: ee
} = window.__gradio__svelte__internal, { afterUpdate: Cf, createEventDispatcher: qf } = window.__gradio__svelte__internal;
function At(t, l, e) {
  const n = t.slice();
  return n[40] = l[e], n;
}
function Sf(t) {
  let l;
  return {
    c() {
      l = Hl(
        /*label*/
        t[0]
      );
    },
    m(e, n) {
      ge(e, l, n);
    },
    p(e, n) {
      n[0] & /*label*/
      1 && Il(
        l,
        /*label*/
        e[0]
      );
    },
    d(e) {
      e && he(l);
    }
  };
}
function Ef(t) {
  let l = (
    /*s*/
    t[40] + ""
  ), e;
  return {
    c() {
      e = Hl(l);
    },
    m(n, i) {
      ge(n, e, i);
    },
    p(n, i) {
      i[0] & /*selected_indices*/
      4096 && l !== (l = /*s*/
      n[40] + "") && Il(e, l);
    },
    d(n) {
      n && he(e);
    }
  };
}
function Nf(t) {
  let l = (
    /*choices_names*/
    t[15][
      /*s*/
      t[40]
    ] + ""
  ), e;
  return {
    c() {
      e = Hl(l);
    },
    m(n, i) {
      ge(n, e, i);
    },
    p(n, i) {
      i[0] & /*choices_names, selected_indices*/
      36864 && l !== (l = /*choices_names*/
      n[15][
        /*s*/
        n[40]
      ] + "") && Il(e, l);
    },
    d(n) {
      n && he(e);
    }
  };
}
function Vt(t) {
  let l, e, n, i, o, u;
  e = new $t({});
  function f() {
    return (
      /*click_handler*/
      t[31](
        /*s*/
        t[40]
      )
    );
  }
  function s(...r) {
    return (
      /*keydown_handler*/
      t[32](
        /*s*/
        t[40],
        ...r
      )
    );
  }
  return {
    c() {
      l = ue("div"), We(e.$$.fragment), P(l, "class", "token-remove svelte-xtjjyg"), P(l, "role", "button"), P(l, "tabindex", "0"), P(l, "title", n = /*i18n*/
      t[9]("common.remove") + " " + /*s*/
      t[40]);
    },
    m(r, a) {
      ge(r, l, a), $e(e, l, null), i = !0, o || (u = [
        de(l, "click", Mt(f)),
        de(l, "keydown", Mt(s))
      ], o = !0);
    },
    p(r, a) {
      t = r, (!i || a[0] & /*i18n, selected_indices*/
      4608 && n !== (n = /*i18n*/
      t[9]("common.remove") + " " + /*s*/
      t[40])) && P(l, "title", n);
    },
    i(r) {
      i || (J(e.$$.fragment, r), i = !0);
    },
    o(r) {
      ee(e.$$.fragment, r), i = !1;
    },
    d(r) {
      r && he(l), xe(e), o = !1, Pl(u);
    }
  };
}
function Dt(t) {
  let l, e, n, i;
  function o(r, a) {
    return typeof /*s*/
    r[40] == "number" ? Nf : Ef;
  }
  let u = o(t), f = u(t), s = !/*disabled*/
  t[4] && Vt(t);
  return {
    c() {
      l = ue("div"), e = ue("span"), f.c(), n = Pe(), s && s.c(), P(e, "class", "svelte-xtjjyg"), P(l, "class", "token svelte-xtjjyg");
    },
    m(r, a) {
      ge(r, l, a), oe(l, e), f.m(e, null), oe(l, n), s && s.m(l, null), i = !0;
    },
    p(r, a) {
      u === (u = o(r)) && f ? f.p(r, a) : (f.d(1), f = u(r), f && (f.c(), f.m(e, null))), /*disabled*/
      r[4] ? s && (bl(), ee(s, 1, 1, () => {
        s = null;
      }), ml()) : s ? (s.p(r, a), a[0] & /*disabled*/
      16 && J(s, 1)) : (s = Vt(r), s.c(), J(s, 1), s.m(l, null));
    },
    i(r) {
      i || (J(s), i = !0);
    },
    o(r) {
      ee(s), i = !1;
    },
    d(r) {
      r && he(l), f.d(), s && s.d();
    }
  };
}
function Bt(t) {
  let l, e, n, i, o = (
    /*selected_indices*/
    t[12].length > 0 && Tt(t)
  );
  return n = new xt({}), {
    c() {
      o && o.c(), l = Pe(), e = ue("span"), We(n.$$.fragment), P(e, "class", "icon-wrap svelte-xtjjyg");
    },
    m(u, f) {
      o && o.m(u, f), ge(u, l, f), ge(u, e, f), $e(n, e, null), i = !0;
    },
    p(u, f) {
      /*selected_indices*/
      u[12].length > 0 ? o ? (o.p(u, f), f[0] & /*selected_indices*/
      4096 && J(o, 1)) : (o = Tt(u), o.c(), J(o, 1), o.m(l.parentNode, l)) : o && (bl(), ee(o, 1, 1, () => {
        o = null;
      }), ml());
    },
    i(u) {
      i || (J(o), J(n.$$.fragment, u), i = !0);
    },
    o(u) {
      ee(o), ee(n.$$.fragment, u), i = !1;
    },
    d(u) {
      u && (he(l), he(e)), o && o.d(u), xe(n);
    }
  };
}
function Tt(t) {
  let l, e, n, i, o, u;
  return e = new $t({}), {
    c() {
      l = ue("div"), We(e.$$.fragment), P(l, "role", "button"), P(l, "tabindex", "0"), P(l, "class", "token-remove remove-all svelte-xtjjyg"), P(l, "title", n = /*i18n*/
      t[9]("common.clear"));
    },
    m(f, s) {
      ge(f, l, s), $e(e, l, null), i = !0, o || (u = [
        de(
          l,
          "click",
          /*remove_all*/
          t[21]
        ),
        de(
          l,
          "keydown",
          /*keydown_handler_1*/
          t[36]
        )
      ], o = !0);
    },
    p(f, s) {
      (!i || s[0] & /*i18n*/
      512 && n !== (n = /*i18n*/
      f[9]("common.clear"))) && P(l, "title", n);
    },
    i(f) {
      i || (J(e.$$.fragment, f), i = !0);
    },
    o(f) {
      ee(e.$$.fragment, f), i = !1;
    },
    d(f) {
      f && he(l), xe(e), o = !1, Pl(u);
    }
  };
}
function Ff(t) {
  let l, e, n, i, o, u, f, s, r, a, m, v, h, y, b;
  e = new Wt({
    props: {
      show_label: (
        /*show_label*/
        t[5]
      ),
      info: (
        /*info*/
        t[1]
      ),
      $$slots: { default: [Sf] },
      $$scope: { ctx: t }
    }
  });
  let c = zt(
    /*selected_indices*/
    t[12]
  ), d = [];
  for (let w = 0; w < c.length; w += 1)
    d[w] = Dt(At(t, c, w));
  const j = (w) => ee(d[w], 1, 1, () => {
    d[w] = null;
  });
  let _ = !/*disabled*/
  t[4] && Bt(t);
  return v = new Gt({
    props: {
      show_options: (
        /*show_options*/
        t[14]
      ),
      choices: (
        /*choices*/
        t[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        t[11]
      ),
      disabled: (
        /*disabled*/
        t[4]
      ),
      selected_indices: (
        /*selected_indices*/
        t[12]
      ),
      active_index: (
        /*active_index*/
        t[16]
      )
    }
  }), v.$on(
    "change",
    /*handle_option_selected*/
    t[20]
  ), {
    c() {
      l = ue("label"), We(e.$$.fragment), n = Pe(), i = ue("div"), o = ue("div");
      for (let w = 0; w < d.length; w += 1)
        d[w].c();
      u = Pe(), f = ue("div"), s = ue("input"), a = Pe(), _ && _.c(), m = Pe(), We(v.$$.fragment), P(s, "class", "border-none svelte-xtjjyg"), s.disabled = /*disabled*/
      t[4], P(s, "autocomplete", "off"), s.readOnly = r = !/*filterable*/
      t[8], Ve(s, "subdued", !/*choices_names*/
      t[15].includes(
        /*input_text*/
        t[10]
      ) && !/*allow_custom_value*/
      t[7] || /*selected_indices*/
      t[12].length === /*max_choices*/
      t[2]), P(f, "class", "secondary-wrap svelte-xtjjyg"), P(o, "class", "wrap-inner svelte-xtjjyg"), Ve(
        o,
        "show_options",
        /*show_options*/
        t[14]
      ), P(i, "class", "wrap svelte-xtjjyg"), P(l, "class", "svelte-xtjjyg"), Ve(
        l,
        "container",
        /*container*/
        t[6]
      );
    },
    m(w, S) {
      ge(w, l, S), $e(e, l, null), oe(l, n), oe(l, i), oe(i, o);
      for (let p = 0; p < d.length; p += 1)
        d[p] && d[p].m(o, null);
      oe(o, u), oe(o, f), oe(f, s), Ot(
        s,
        /*input_text*/
        t[10]
      ), t[34](s), oe(f, a), _ && _.m(f, null), oe(i, m), $e(v, i, null), h = !0, y || (b = [
        de(
          s,
          "input",
          /*input_input_handler*/
          t[33]
        ),
        de(
          s,
          "keydown",
          /*handle_key_down*/
          t[23]
        ),
        de(
          s,
          "keyup",
          /*keyup_handler*/
          t[35]
        ),
        de(
          s,
          "blur",
          /*handle_blur*/
          t[18]
        ),
        de(
          s,
          "focus",
          /*handle_focus*/
          t[22]
        )
      ], y = !0);
    },
    p(w, S) {
      const p = {};
      if (S[0] & /*show_label*/
      32 && (p.show_label = /*show_label*/
      w[5]), S[0] & /*info*/
      2 && (p.info = /*info*/
      w[1]), S[0] & /*label*/
      1 | S[1] & /*$$scope*/
      4096 && (p.$$scope = { dirty: S, ctx: w }), e.$set(p), S[0] & /*i18n, selected_indices, remove_selected_choice, disabled, choices_names*/
      561680) {
        c = zt(
          /*selected_indices*/
          w[12]
        );
        let q;
        for (q = 0; q < c.length; q += 1) {
          const E = At(w, c, q);
          d[q] ? (d[q].p(E, S), J(d[q], 1)) : (d[q] = Dt(E), d[q].c(), J(d[q], 1), d[q].m(o, u));
        }
        for (bl(), q = c.length; q < d.length; q += 1)
          j(q);
        ml();
      }
      (!h || S[0] & /*disabled*/
      16) && (s.disabled = /*disabled*/
      w[4]), (!h || S[0] & /*filterable*/
      256 && r !== (r = !/*filterable*/
      w[8])) && (s.readOnly = r), S[0] & /*input_text*/
      1024 && s.value !== /*input_text*/
      w[10] && Ot(
        s,
        /*input_text*/
        w[10]
      ), (!h || S[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && Ve(s, "subdued", !/*choices_names*/
      w[15].includes(
        /*input_text*/
        w[10]
      ) && !/*allow_custom_value*/
      w[7] || /*selected_indices*/
      w[12].length === /*max_choices*/
      w[2]), /*disabled*/
      w[4] ? _ && (bl(), ee(_, 1, 1, () => {
        _ = null;
      }), ml()) : _ ? (_.p(w, S), S[0] & /*disabled*/
      16 && J(_, 1)) : (_ = Bt(w), _.c(), J(_, 1), _.m(f, null)), (!h || S[0] & /*show_options*/
      16384) && Ve(
        o,
        "show_options",
        /*show_options*/
        w[14]
      );
      const N = {};
      S[0] & /*show_options*/
      16384 && (N.show_options = /*show_options*/
      w[14]), S[0] & /*choices*/
      8 && (N.choices = /*choices*/
      w[3]), S[0] & /*filtered_indices*/
      2048 && (N.filtered_indices = /*filtered_indices*/
      w[11]), S[0] & /*disabled*/
      16 && (N.disabled = /*disabled*/
      w[4]), S[0] & /*selected_indices*/
      4096 && (N.selected_indices = /*selected_indices*/
      w[12]), S[0] & /*active_index*/
      65536 && (N.active_index = /*active_index*/
      w[16]), v.$set(N), (!h || S[0] & /*container*/
      64) && Ve(
        l,
        "container",
        /*container*/
        w[6]
      );
    },
    i(w) {
      if (!h) {
        J(e.$$.fragment, w);
        for (let S = 0; S < c.length; S += 1)
          J(d[S]);
        J(_), J(v.$$.fragment, w), h = !0;
      }
    },
    o(w) {
      ee(e.$$.fragment, w), d = d.filter(Boolean);
      for (let S = 0; S < d.length; S += 1)
        ee(d[S]);
      ee(_), ee(v.$$.fragment, w), h = !1;
    },
    d(w) {
      w && he(l), xe(e), vf(d, w), t[34](null), _ && _.d(), xe(v), y = !1, Pl(b);
    }
  };
}
function Lf(t, l, e) {
  let { label: n } = l, { info: i = void 0 } = l, { value: o = [] } = l, u = [], { value_is_output: f = !1 } = l, { max_choices: s = null } = l, { choices: r } = l, a, { disabled: m = !1 } = l, { show_label: v } = l, { container: h = !0 } = l, { allow_custom_value: y = !1 } = l, { filterable: b = !0 } = l, { i18n: c } = l, d, j = "", _ = "", w = !1, S, p, N = [], q = null, E = [], B = [];
  const T = qf();
  Array.isArray(o) && o.forEach((k) => {
    const U = r.map((ve) => ve[1]).indexOf(k);
    U !== -1 ? E.push(U) : E.push(k);
  });
  function le() {
    y || e(10, j = ""), y && j !== "" && (I(j), e(10, j = "")), e(14, w = !1), e(16, q = null), T("blur");
  }
  function F(k) {
    e(12, E = E.filter((U) => U !== k)), T("select", {
      index: typeof k == "number" ? k : -1,
      value: typeof k == "number" ? p[k] : k,
      selected: !1
    });
  }
  function I(k) {
    (s === null || E.length < s) && (e(12, E = [...E, k]), T("select", {
      index: typeof k == "number" ? k : -1,
      value: typeof k == "number" ? p[k] : k,
      selected: !0
    })), E.length === s && (e(14, w = !1), e(16, q = null), d.blur());
  }
  function H(k) {
    const U = parseInt(k.detail.target.dataset.index);
    ce(U);
  }
  function ce(k) {
    E.includes(k) ? F(k) : I(k), e(10, j = "");
  }
  function we(k) {
    e(12, E = []), e(10, j = ""), k.preventDefault();
  }
  function pe(k) {
    e(11, N = r.map((U, ve) => ve)), (s === null || E.length < s) && e(14, w = !0), T("focus");
  }
  function ke(k) {
    e(14, [w, q] = ln(k, q, N), w, (e(16, q), e(3, r), e(27, a), e(10, j), e(28, _), e(7, y), e(11, N))), k.key === "Enter" && (q !== null ? ce(q) : y && (I(j), e(10, j = ""))), k.key === "Backspace" && j === "" && e(12, E = [...E.slice(0, -1)]), E.length === s && (e(14, w = !1), e(16, q = null));
  }
  function g() {
    o === void 0 ? e(12, E = []) : Array.isArray(o) && e(12, E = o.map((k) => {
      const U = p.indexOf(k);
      if (U !== -1)
        return U;
      if (y)
        return k;
    }).filter((k) => k !== void 0));
  }
  Cf(() => {
    e(25, f = !1);
  });
  const X = (k) => F(k), Y = (k, U) => {
    U.key === "Enter" && F(k);
  };
  function C() {
    j = this.value, e(10, j);
  }
  function R(k) {
    kf[k ? "unshift" : "push"](() => {
      d = k, e(13, d);
    });
  }
  const A = (k) => T("key_up", { key: k.key, input_value: j }), M = (k) => {
    k.key === "Enter" && we(k);
  };
  return t.$$set = (k) => {
    "label" in k && e(0, n = k.label), "info" in k && e(1, i = k.info), "value" in k && e(24, o = k.value), "value_is_output" in k && e(25, f = k.value_is_output), "max_choices" in k && e(2, s = k.max_choices), "choices" in k && e(3, r = k.choices), "disabled" in k && e(4, m = k.disabled), "show_label" in k && e(5, v = k.show_label), "container" in k && e(6, h = k.container), "allow_custom_value" in k && e(7, y = k.allow_custom_value), "filterable" in k && e(8, b = k.filterable), "i18n" in k && e(9, c = k.i18n);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*choices*/
    8 && (e(15, S = r.map((k) => k[0])), e(29, p = r.map((k) => k[1]))), t.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    402656392 && (r !== a || j !== _) && (e(11, N = zl(r, j)), e(27, a = r), e(28, _ = j), y || e(16, q = N[0])), t.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    1610616832 && JSON.stringify(E) != JSON.stringify(B) && (e(24, o = E.map((k) => typeof k == "number" ? p[k] : k)), e(30, B = E.slice())), t.$$.dirty[0] & /*value, old_value, value_is_output*/
    117440512 && JSON.stringify(o) != JSON.stringify(u) && (en(T, o, f), e(26, u = Array.isArray(o) ? o.slice() : o)), t.$$.dirty[0] & /*value*/
    16777216 && g();
  }, [
    n,
    i,
    s,
    r,
    m,
    v,
    h,
    y,
    b,
    c,
    j,
    N,
    E,
    d,
    w,
    S,
    q,
    T,
    le,
    F,
    H,
    we,
    pe,
    ke,
    o,
    f,
    u,
    a,
    _,
    p,
    B,
    X,
    Y,
    C,
    R,
    A,
    M
  ];
}
class Gf extends pf {
  constructor(l) {
    super(), yf(
      this,
      l,
      Lf,
      Ff,
      jf,
      {
        label: 0,
        info: 1,
        value: 24,
        value_is_output: 25,
        max_choices: 2,
        choices: 3,
        disabled: 4,
        show_label: 5,
        container: 6,
        allow_custom_value: 7,
        filterable: 8,
        i18n: 9
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: zf,
  add_flush_callback: Mf,
  append: De,
  assign: Of,
  attr: Z,
  bind: Af,
  binding_callbacks: Vf,
  check_outros: cn,
  create_component: gl,
  destroy_component: wl,
  detach: K,
  element: me,
  empty: dn,
  get_spread_object: Df,
  get_spread_update: Bf,
  group_outros: mn,
  init: Tf,
  insert: Q,
  listen: Dl,
  mount_component: pl,
  run_all: Uf,
  safe_not_equal: Zf,
  set_input_value: Ut,
  space: qe,
  text: Pf,
  transition_in: _e,
  transition_out: Se
} = window.__gradio__svelte__internal;
function Zt(t) {
  let l, e, n, i, o, u, f, s, r, a = (
    /*show_token_textbox*/
    t[9] && Pt(t)
  );
  function m(b) {
    t[20](b);
  }
  let v = {
    choices: (
      /*pipelines*/
      t[7]
    ),
    label: "Select the pipeline to use: ",
    info: (
      /*info*/
      t[3]
    ),
    show_label: (
      /*show_label*/
      t[8]
    ),
    container: (
      /*container*/
      t[11]
    ),
    disabled: !/*interactive*/
    t[16]
  };
  /*value_is_output*/
  t[2] !== void 0 && (v.value_is_output = /*value_is_output*/
  t[2]), e = new as({ props: v }), Vf.push(() => Af(e, "value_is_output", m)), e.$on(
    "input",
    /*input_handler*/
    t[21]
  ), e.$on(
    "select",
    /*select_handler*/
    t[22]
  ), e.$on(
    "blur",
    /*blur_handler*/
    t[23]
  ), e.$on(
    "focus",
    /*focus_handler*/
    t[24]
  ), e.$on(
    "key_up",
    /*key_up_handler*/
    t[25]
  );
  let h = (
    /*enable_edition*/
    t[10] && It(t)
  ), y = (
    /*value*/
    t[0].name !== "" && Ht(t)
  );
  return {
    c() {
      a && a.c(), l = qe(), gl(e.$$.fragment), i = qe(), h && h.c(), o = qe(), u = me("div"), f = qe(), y && y.c(), s = dn(), Z(u, "class", "params-control svelte-1nstxj7"), Z(u, "id", "params-control");
    },
    m(b, c) {
      a && a.m(b, c), Q(b, l, c), pl(e, b, c), Q(b, i, c), h && h.m(b, c), Q(b, o, c), Q(b, u, c), Q(b, f, c), y && y.m(b, c), Q(b, s, c), r = !0;
    },
    p(b, c) {
      /*show_token_textbox*/
      b[9] ? a ? a.p(b, c) : (a = Pt(b), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null);
      const d = {};
      c[0] & /*pipelines*/
      128 && (d.choices = /*pipelines*/
      b[7]), c[0] & /*info*/
      8 && (d.info = /*info*/
      b[3]), c[0] & /*show_label*/
      256 && (d.show_label = /*show_label*/
      b[8]), c[0] & /*container*/
      2048 && (d.container = /*container*/
      b[11]), c[0] & /*interactive*/
      65536 && (d.disabled = !/*interactive*/
      b[16]), !n && c[0] & /*value_is_output*/
      4 && (n = !0, d.value_is_output = /*value_is_output*/
      b[2], Mf(() => n = !1)), e.$set(d), /*enable_edition*/
      b[10] ? h ? h.p(b, c) : (h = It(b), h.c(), h.m(o.parentNode, o)) : h && (h.d(1), h = null), /*value*/
      b[0].name !== "" ? y ? (y.p(b, c), c[0] & /*value*/
      1 && _e(y, 1)) : (y = Ht(b), y.c(), _e(y, 1), y.m(s.parentNode, s)) : y && (mn(), Se(y, 1, 1, () => {
        y = null;
      }), cn());
    },
    i(b) {
      r || (_e(e.$$.fragment, b), _e(y), r = !0);
    },
    o(b) {
      Se(e.$$.fragment, b), Se(y), r = !1;
    },
    d(b) {
      b && (K(l), K(i), K(o), K(u), K(f), K(s)), a && a.d(b), wl(e, b), h && h.d(b), y && y.d(b);
    }
  };
}
function Pt(t) {
  let l, e, n, i, o, u;
  return {
    c() {
      l = me("label"), l.textContent = "Enter your Hugging Face token:", e = qe(), n = me("input"), Z(l, "for", "token"), Z(l, "class", "label svelte-1nstxj7"), Z(n, "data-testid", "textbox"), Z(n, "type", "text"), Z(n, "class", "text-area svelte-1nstxj7"), Z(n, "name", "token"), Z(n, "id", "token"), Z(n, "placeholder", "hf_xxxxxxx..."), Z(n, "aria-label", "Enter your Hugging Face token"), Z(n, "maxlength", "50"), n.disabled = i = !/*interactive*/
      t[16];
    },
    m(f, s) {
      Q(f, l, s), Q(f, e, s), Q(f, n, s), Ut(
        n,
        /*value*/
        t[0].token
      ), o || (u = Dl(
        n,
        "input",
        /*input_input_handler*/
        t[19]
      ), o = !0);
    },
    p(f, s) {
      s[0] & /*interactive*/
      65536 && i !== (i = !/*interactive*/
      f[16]) && (n.disabled = i), s[0] & /*value*/
      1 && n.value !== /*value*/
      f[0].token && Ut(
        n,
        /*value*/
        f[0].token
      );
    },
    d(f) {
      f && (K(l), K(e), K(n)), o = !1, u();
    }
  };
}
function It(t) {
  let l, e, n, i, o, u, f, s, r, a, m;
  return {
    c() {
      l = me("div"), e = me("p"), e.textContent = "Show configuration", n = qe(), i = me("label"), o = me("input"), f = qe(), s = me("span"), Z(o, "type", "checkbox"), o.disabled = u = /*value*/
      t[0].name == "", Z(o, "class", "svelte-1nstxj7"), Z(s, "class", "slider round svelte-1nstxj7"), Z(i, "class", "switch svelte-1nstxj7"), Z(i, "title", r = /*value*/
      t[0].name == "" ? "Please select a pipeline first" : "Show pipeline config"), Z(l, "class", "toggle-config svelte-1nstxj7");
    },
    m(v, h) {
      Q(v, l, h), De(l, e), De(l, n), De(l, i), De(i, o), o.checked = /*show_config*/
      t[1], De(i, f), De(i, s), a || (m = [
        Dl(
          o,
          "change",
          /*input_change_handler*/
          t[26]
        ),
        Dl(
          o,
          "input",
          /*input_handler_1*/
          t[27]
        )
      ], a = !0);
    },
    p(v, h) {
      h[0] & /*value*/
      1 && u !== (u = /*value*/
      v[0].name == "") && (o.disabled = u), h[0] & /*show_config*/
      2 && (o.checked = /*show_config*/
      v[1]), h[0] & /*value*/
      1 && r !== (r = /*value*/
      v[0].name == "" ? "Please select a pipeline first" : "Show pipeline config") && Z(i, "title", r);
    },
    d(v) {
      v && K(l), a = !1, Uf(m);
    }
  };
}
function Ht(t) {
  let l, e, n;
  return e = new rf({
    props: {
      elem_id: (
        /*elem_id*/
        t[4]
      ),
      elem_classes: (
        /*elem_classes*/
        t[5]
      ),
      scale: (
        /*scale*/
        t[12]
      ),
      min_width: (
        /*min_width*/
        t[13]
      ),
      visible: (
        /*show_config*/
        t[1]
      ),
      $$slots: { default: [If] },
      $$scope: { ctx: t }
    }
  }), e.$on(
    "click",
    /*click_handler*/
    t[28]
  ), {
    c() {
      l = me("div"), gl(e.$$.fragment), Z(l, "class", "validation svelte-1nstxj7");
    },
    m(i, o) {
      Q(i, l, o), pl(e, l, null), n = !0;
    },
    p(i, o) {
      const u = {};
      o[0] & /*elem_id*/
      16 && (u.elem_id = /*elem_id*/
      i[4]), o[0] & /*elem_classes*/
      32 && (u.elem_classes = /*elem_classes*/
      i[5]), o[0] & /*scale*/
      4096 && (u.scale = /*scale*/
      i[12]), o[0] & /*min_width*/
      8192 && (u.min_width = /*min_width*/
      i[13]), o[0] & /*show_config*/
      2 && (u.visible = /*show_config*/
      i[1]), o[1] & /*$$scope*/
      4 && (u.$$scope = { dirty: o, ctx: i }), e.$set(u);
    },
    i(i) {
      n || (_e(e.$$.fragment, i), n = !0);
    },
    o(i) {
      Se(e.$$.fragment, i), n = !1;
    },
    d(i) {
      i && K(l), wl(e);
    }
  };
}
function If(t) {
  let l;
  return {
    c() {
      l = Pf("Update parameters");
    },
    m(e, n) {
      Q(e, l, n);
    },
    d(e) {
      e && K(l);
    }
  };
}
function Hf(t) {
  let l, e, n, i;
  const o = [
    {
      autoscroll: (
        /*gradio*/
        t[15].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      t[15].i18n
    ) },
    /*loading_status*/
    t[14]
  ];
  let u = {};
  for (let s = 0; s < o.length; s += 1)
    u = Of(u, o[s]);
  l = new Gs({ props: u });
  let f = (
    /*visible*/
    t[6] && Zt(t)
  );
  return {
    c() {
      gl(l.$$.fragment), e = qe(), f && f.c(), n = dn();
    },
    m(s, r) {
      pl(l, s, r), Q(s, e, r), f && f.m(s, r), Q(s, n, r), i = !0;
    },
    p(s, r) {
      const a = r[0] & /*gradio, loading_status*/
      49152 ? Bf(o, [
        r[0] & /*gradio*/
        32768 && {
          autoscroll: (
            /*gradio*/
            s[15].autoscroll
          )
        },
        r[0] & /*gradio*/
        32768 && { i18n: (
          /*gradio*/
          s[15].i18n
        ) },
        r[0] & /*loading_status*/
        16384 && Df(
          /*loading_status*/
          s[14]
        )
      ]) : {};
      l.$set(a), /*visible*/
      s[6] ? f ? (f.p(s, r), r[0] & /*visible*/
      64 && _e(f, 1)) : (f = Zt(s), f.c(), _e(f, 1), f.m(n.parentNode, n)) : f && (mn(), Se(f, 1, 1, () => {
        f = null;
      }), cn());
    },
    i(s) {
      i || (_e(l.$$.fragment, s), _e(f), i = !0);
    },
    o(s) {
      Se(l.$$.fragment, s), Se(f), i = !1;
    },
    d(s) {
      s && (K(e), K(n)), wl(l, s), f && f.d(s);
    }
  };
}
function Jf(t) {
  let l, e;
  return l = new Wn({
    props: {
      visible: (
        /*visible*/
        t[6]
      ),
      elem_id: (
        /*elem_id*/
        t[4]
      ),
      elem_classes: (
        /*elem_classes*/
        t[5]
      ),
      padding: (
        /*container*/
        t[11]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        t[12]
      ),
      min_width: (
        /*min_width*/
        t[13]
      ),
      $$slots: { default: [Hf] },
      $$scope: { ctx: t }
    }
  }), {
    c() {
      gl(l.$$.fragment);
    },
    m(n, i) {
      pl(l, n, i), e = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      64 && (o.visible = /*visible*/
      n[6]), i[0] & /*elem_id*/
      16 && (o.elem_id = /*elem_id*/
      n[4]), i[0] & /*elem_classes*/
      32 && (o.elem_classes = /*elem_classes*/
      n[5]), i[0] & /*container*/
      2048 && (o.padding = /*container*/
      n[11]), i[0] & /*scale*/
      4096 && (o.scale = /*scale*/
      n[12]), i[0] & /*min_width*/
      8192 && (o.min_width = /*min_width*/
      n[13]), i[0] & /*elem_id, elem_classes, scale, min_width, show_config, gradio, value, paramsViewNeedUpdate, enable_edition, pipelines, info, show_label, container, interactive, value_is_output, show_token_textbox, visible, loading_status*/
      262143 | i[1] & /*$$scope*/
      4 && (o.$$scope = { dirty: i, ctx: n }), l.$set(o);
    },
    i(n) {
      e || (_e(l.$$.fragment, n), e = !0);
    },
    o(n) {
      Se(l.$$.fragment, n), e = !1;
    },
    d(n) {
      wl(l, n);
    }
  };
}
function Bl(t) {
  const l = /* @__PURE__ */ new Map();
  if (!t)
    return l;
  for (const e in t)
    t.hasOwnProperty(e) && (typeof t[e] == "object" && t[e] !== null ? l.set(e, Bl(t[e])) : l.set(e, t[e]));
  return l;
}
function bn(t) {
  return Object.fromEntries(Array.from(t.entries(), ([e, n]) => n instanceof Map ? [e, bn(n)] : [e, n]));
}
function Tl(t, l) {
  const e = document.createElement("label");
  e.textContent = l, t.appendChild(e);
}
function Rf(t, l, e) {
  const n = document.createElement("input"), i = t.id;
  Tl(t, i.split("-").at(-1)), n.type = "number", n.value = l, n.contentEditable = String(e), t.appendChild(n);
}
function Xf(t, l, e) {
  let { info: n = void 0 } = l, { elem_id: i = "" } = l, { elem_classes: o = [] } = l, { visible: u = !0 } = l, { value: f = new Ks({ name: "", token: "" }) } = l, { value_is_output: s = !1 } = l, { pipelines: r } = l, { show_label: a } = l, { show_token_textbox: m } = l, { show_config: v = !1 } = l, { enable_edition: h = !1 } = l, { container: y = !0 } = l, { scale: b = null } = l, { min_width: c = void 0 } = l, { loading_status: d } = l, { gradio: j } = l, { interactive: _ } = l, w = !1;
  function S(g) {
    g !== "" && (e(0, f.name = g, f), e(0, f.param_specs = {}, f), j.dispatch("select", f), e(17, w = !0));
  }
  function p(g, X) {
    const Y = g.split("-");
    let C = Bl(f.param_specs);
    var R = C;
    Y.forEach((A) => {
      R = R.get(A);
    }), R.set("value", X), e(0, f.param_specs = bn(C), f);
  }
  function N(g, X, Y) {
    const C = document.createElement("select"), R = g.id;
    Tl(g, R.split("-").at(-1)), X.forEach((A) => {
      const M = document.createElement("option");
      M.textContent = A, M.value = A, C.appendChild(M), A === Y && (M.selected = !0);
    }), C.addEventListener("change", (A) => {
      p(R, C.value);
    }), g.appendChild(C);
  }
  function q(g, X, Y, C, R) {
    const A = document.createElement("input"), M = document.createElement("input"), k = g.id;
    Tl(g, k.split("-").at(-1)), A.type = "range", A.min = X, A.max = Y, A.value = C, A.step = R, A.addEventListener("input", (U) => {
      M.value = A.value, p(k, A.value);
    }), g.appendChild(A), M.type = "number", M.min = X, M.max = Y, M.value = C, M.step = R, M.contentEditable = "true", M.addEventListener("input", (U) => {
      A.value = M.value, p(k, A.value);
    }), g.appendChild(M);
  }
  function E(g, X, Y) {
    X.forEach((C, R) => {
      const A = (Y ? Y + "-" : "") + R;
      if (C.values().next().value instanceof Map) {
        const M = document.createElement("fieldset");
        M.innerHTML = "<legend>" + A + "<legend>", M.id = A, g.appendChild(M), E(M, C, R);
      } else {
        const M = document.createElement("div");
        switch (M.id = A, M.classList.add("param"), g.appendChild(M), C.get("component")) {
          case "slider":
            q(M, C.get("min"), C.get("max"), C.get("value"), C.get("step"));
            break;
          case "dropdown":
            N(M, C.get("choices"), C.get("value"));
            break;
          case "textbox":
            Rf(M, C.get("value"), !1);
            break;
        }
      }
    });
  }
  function B() {
    f.token = this.value, e(0, f);
  }
  function T(g) {
    s = g, e(2, s);
  }
  const le = () => j.dispatch("input"), F = (g) => S(g.detail.value), I = () => j.dispatch("blur"), H = () => j.dispatch("focus"), ce = (g) => j.dispatch("key_up", g.detail);
  function we() {
    v = this.checked, e(1, v);
  }
  const pe = () => {
    e(17, w = !0), e(1, v = !v);
  }, ke = () => j.dispatch("change", f);
  return t.$$set = (g) => {
    "info" in g && e(3, n = g.info), "elem_id" in g && e(4, i = g.elem_id), "elem_classes" in g && e(5, o = g.elem_classes), "visible" in g && e(6, u = g.visible), "value" in g && e(0, f = g.value), "value_is_output" in g && e(2, s = g.value_is_output), "pipelines" in g && e(7, r = g.pipelines), "show_label" in g && e(8, a = g.show_label), "show_token_textbox" in g && e(9, m = g.show_token_textbox), "show_config" in g && e(1, v = g.show_config), "enable_edition" in g && e(10, h = g.enable_edition), "container" in g && e(11, y = g.container), "scale" in g && e(12, b = g.scale), "min_width" in g && e(13, c = g.min_width), "loading_status" in g && e(14, d = g.loading_status), "gradio" in g && e(15, j = g.gradio), "interactive" in g && e(16, _ = g.interactive);
  }, t.$$.update = () => {
    if (t.$$.dirty[0] & /*value, paramsViewNeedUpdate, show_config*/
    131075 && Object.keys(f.param_specs).length > 0 && w) {
      const g = document.getElementById("params-control");
      if (g.replaceChildren(), v) {
        let X = Bl(f.param_specs);
        E(g, X), e(17, w = !1);
      }
    }
  }, [
    f,
    v,
    s,
    n,
    i,
    o,
    u,
    r,
    a,
    m,
    h,
    y,
    b,
    c,
    d,
    j,
    _,
    w,
    S,
    B,
    T,
    le,
    F,
    I,
    H,
    ce,
    we,
    pe,
    ke
  ];
}
class Kf extends zf {
  constructor(l) {
    super(), Tf(
      this,
      l,
      Xf,
      Jf,
      Zf,
      {
        info: 3,
        elem_id: 4,
        elem_classes: 5,
        visible: 6,
        value: 0,
        value_is_output: 2,
        pipelines: 7,
        show_label: 8,
        show_token_textbox: 9,
        show_config: 1,
        enable_edition: 10,
        container: 11,
        scale: 12,
        min_width: 13,
        loading_status: 14,
        gradio: 15,
        interactive: 16
      },
      null,
      [-1, -1]
    );
  }
}
export {
  as as BaseDropdown,
  Yf as BaseExample,
  Gf as BaseMultiselect,
  Kf as default
};
