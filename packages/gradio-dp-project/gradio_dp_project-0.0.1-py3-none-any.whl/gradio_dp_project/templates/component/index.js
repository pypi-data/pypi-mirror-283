const {
  SvelteComponent: $t,
  assign: el,
  create_slot: tl,
  detach: ll,
  element: nl,
  get_all_dirty_from_scope: il,
  get_slot_changes: fl,
  get_spread_update: ol,
  init: sl,
  insert: al,
  safe_not_equal: rl,
  set_dynamic_element_data: xe,
  set_style: I,
  toggle_class: Y,
  transition_in: Vt,
  transition_out: It,
  update_slot_base: _l
} = window.__gradio__svelte__internal;
function ul(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), f = tl(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let s = 0; s < o.length; s += 1)
    r = el(r, o[s]);
  return {
    c() {
      e = nl(
        /*tag*/
        n[14]
      ), f && f.c(), xe(
        /*tag*/
        n[14]
      )(e, r), Y(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), Y(
        e,
        "padded",
        /*padding*/
        n[6]
      ), Y(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), Y(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), Y(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), I(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), I(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), I(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), I(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), I(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), I(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), I(e, "border-width", "var(--block-border-width)");
    },
    m(s, a) {
      al(s, e, a), f && f.m(e, null), l = !0;
    },
    p(s, a) {
      f && f.p && (!l || a & /*$$scope*/
      131072) && _l(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        l ? fl(
          i,
          /*$$scope*/
          s[17],
          a,
          null
        ) : il(
          /*$$scope*/
          s[17]
        ),
        null
      ), xe(
        /*tag*/
        s[14]
      )(e, r = ol(o, [
        (!l || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!l || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!l || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Y(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), Y(
        e,
        "padded",
        /*padding*/
        s[6]
      ), Y(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), Y(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), Y(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), a & /*height*/
      1 && I(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), a & /*width*/
      2 && I(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), a & /*variant*/
      16 && I(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), a & /*allow_overflow*/
      2048 && I(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && I(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), a & /*min_width*/
      8192 && I(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      l || (Vt(f, s), l = !0);
    },
    o(s) {
      It(f, s), l = !1;
    },
    d(s) {
      s && ll(e), f && f.d(s);
    }
  };
}
function cl(n) {
  let e, t = (
    /*tag*/
    n[14] && ul(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (Vt(t, l), e = !0);
    },
    o(l) {
      It(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function dl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: o = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: s = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: u = !0 } = e, { type: w = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: g = !1 } = e, { container: b = !0 } = e, { visible: h = !0 } = e, { allow_overflow: F = !0 } = e, { scale: c = null } = e, { min_width: m = 0 } = e, C = w === "fieldset" ? "fieldset" : "div";
  const z = (k) => {
    if (k !== void 0) {
      if (typeof k == "number")
        return k + "px";
      if (typeof k == "string")
        return k;
    }
  };
  return n.$$set = (k) => {
    "height" in k && t(0, f = k.height), "width" in k && t(1, o = k.width), "elem_id" in k && t(2, r = k.elem_id), "elem_classes" in k && t(3, s = k.elem_classes), "variant" in k && t(4, a = k.variant), "border_mode" in k && t(5, _ = k.border_mode), "padding" in k && t(6, u = k.padding), "type" in k && t(16, w = k.type), "test_id" in k && t(7, d = k.test_id), "explicit_call" in k && t(8, g = k.explicit_call), "container" in k && t(9, b = k.container), "visible" in k && t(10, h = k.visible), "allow_overflow" in k && t(11, F = k.allow_overflow), "scale" in k && t(12, c = k.scale), "min_width" in k && t(13, m = k.min_width), "$$scope" in k && t(17, i = k.$$scope);
  }, [
    f,
    o,
    r,
    s,
    a,
    _,
    u,
    d,
    g,
    b,
    h,
    F,
    c,
    m,
    C,
    z,
    w,
    i,
    l
  ];
}
class ml extends $t {
  constructor(e) {
    super(), sl(this, e, dl, cl, rl, {
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
  SvelteComponent: bl,
  attr: hl,
  create_slot: gl,
  detach: wl,
  element: pl,
  get_all_dirty_from_scope: kl,
  get_slot_changes: vl,
  init: yl,
  insert: ql,
  safe_not_equal: Cl,
  transition_in: Ml,
  transition_out: Fl,
  update_slot_base: jl
} = window.__gradio__svelte__internal;
function Ll(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = gl(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = pl("div"), i && i.c(), hl(e, "class", "svelte-1hnfib2");
    },
    m(f, o) {
      ql(f, e, o), i && i.m(e, null), t = !0;
    },
    p(f, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && jl(
        i,
        l,
        f,
        /*$$scope*/
        f[0],
        t ? vl(
          l,
          /*$$scope*/
          f[0],
          o,
          null
        ) : kl(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (Ml(i, f), t = !0);
    },
    o(f) {
      Fl(i, f), t = !1;
    },
    d(f) {
      f && wl(e), i && i.d(f);
    }
  };
}
function Sl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, l];
}
class zl extends bl {
  constructor(e) {
    super(), yl(this, e, Sl, Ll, Cl, {});
  }
}
const {
  SvelteComponent: Nl,
  attr: $e,
  check_outros: Vl,
  create_component: Il,
  create_slot: Zl,
  destroy_component: Al,
  detach: Le,
  element: Bl,
  empty: El,
  get_all_dirty_from_scope: Pl,
  get_slot_changes: Dl,
  group_outros: Tl,
  init: Kl,
  insert: Se,
  mount_component: Ol,
  safe_not_equal: Xl,
  set_data: Yl,
  space: Gl,
  text: Rl,
  toggle_class: oe,
  transition_in: be,
  transition_out: ze,
  update_slot_base: Hl
} = window.__gradio__svelte__internal;
function et(n) {
  let e, t;
  return e = new zl({
    props: {
      $$slots: { default: [Jl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Il(e.$$.fragment);
    },
    m(l, i) {
      Ol(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (be(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ze(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Al(e, l);
    }
  };
}
function Jl(n) {
  let e;
  return {
    c() {
      e = Rl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Se(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Yl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Le(e);
    }
  };
}
function Ql(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[2].default
  ), o = Zl(
    f,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && et(n)
  );
  return {
    c() {
      e = Bl("span"), o && o.c(), t = Gl(), r && r.c(), l = El(), $e(e, "data-testid", "block-info"), $e(e, "class", "svelte-22c38v"), oe(e, "sr-only", !/*show_label*/
      n[0]), oe(e, "hide", !/*show_label*/
      n[0]), oe(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(s, a) {
      Se(s, e, a), o && o.m(e, null), Se(s, t, a), r && r.m(s, a), Se(s, l, a), i = !0;
    },
    p(s, [a]) {
      o && o.p && (!i || a & /*$$scope*/
      8) && Hl(
        o,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? Dl(
          f,
          /*$$scope*/
          s[3],
          a,
          null
        ) : Pl(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && oe(e, "sr-only", !/*show_label*/
      s[0]), (!i || a & /*show_label*/
      1) && oe(e, "hide", !/*show_label*/
      s[0]), (!i || a & /*info*/
      2) && oe(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? r ? (r.p(s, a), a & /*info*/
      2 && be(r, 1)) : (r = et(s), r.c(), be(r, 1), r.m(l.parentNode, l)) : r && (Tl(), ze(r, 1, 1, () => {
        r = null;
      }), Vl());
    },
    i(s) {
      i || (be(o, s), be(r), i = !0);
    },
    o(s) {
      ze(o, s), ze(r), i = !1;
    },
    d(s) {
      s && (Le(e), Le(t), Le(l)), o && o.d(s), r && r.d(s);
    }
  };
}
function Ul(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: o = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, o = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, o, l, i];
}
class Wl extends Nl {
  constructor(e) {
    super(), Kl(this, e, Ul, Ql, Xl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: xl,
  append: Ke,
  attr: U,
  bubble: $l,
  create_component: en,
  destroy_component: tn,
  detach: Zt,
  element: Oe,
  init: ln,
  insert: At,
  listen: nn,
  mount_component: fn,
  safe_not_equal: on,
  set_data: sn,
  set_style: se,
  space: an,
  text: rn,
  toggle_class: N,
  transition_in: _n,
  transition_out: un
} = window.__gradio__svelte__internal;
function tt(n) {
  let e, t;
  return {
    c() {
      e = Oe("span"), t = rn(
        /*label*/
        n[1]
      ), U(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      At(l, e, i), Ke(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && sn(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Zt(e);
    }
  };
}
function cn(n) {
  let e, t, l, i, f, o, r, s = (
    /*show_label*/
    n[2] && tt(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Oe("button"), s && s.c(), t = an(), l = Oe("div"), en(i.$$.fragment), U(l, "class", "svelte-1lrphxw"), N(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), N(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), N(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], U(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), U(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), U(
        e,
        "title",
        /*label*/
        n[1]
      ), U(e, "class", "svelte-1lrphxw"), N(
        e,
        "pending",
        /*pending*/
        n[3]
      ), N(
        e,
        "padded",
        /*padded*/
        n[5]
      ), N(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), N(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), se(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), se(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), se(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(a, _) {
      At(a, e, _), s && s.m(e, null), Ke(e, t), Ke(e, l), fn(i, l, null), f = !0, o || (r = nn(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), o = !0);
    },
    p(a, [_]) {
      /*show_label*/
      a[2] ? s ? s.p(a, _) : (s = tt(a), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!f || _ & /*size*/
      16) && N(
        l,
        "small",
        /*size*/
        a[4] === "small"
      ), (!f || _ & /*size*/
      16) && N(
        l,
        "large",
        /*size*/
        a[4] === "large"
      ), (!f || _ & /*size*/
      16) && N(
        l,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!f || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!f || _ & /*label*/
      2) && U(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!f || _ & /*hasPopup*/
      256) && U(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!f || _ & /*label*/
      2) && U(
        e,
        "title",
        /*label*/
        a[1]
      ), (!f || _ & /*pending*/
      8) && N(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!f || _ & /*padded*/
      32) && N(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!f || _ & /*highlight*/
      64) && N(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!f || _ & /*transparent*/
      512) && N(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), _ & /*disabled, _color*/
      4224 && se(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && se(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), _ & /*offset*/
      2048 && se(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      f || (_n(i.$$.fragment, a), f = !0);
    },
    o(a) {
      un(i.$$.fragment, a), f = !1;
    },
    d(a) {
      a && Zt(e), s && s.d(), tn(i), o = !1, r();
    }
  };
}
function dn(n, e, t) {
  let l, { Icon: i } = e, { label: f = "" } = e, { show_label: o = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: a = !0 } = e, { highlight: _ = !1 } = e, { disabled: u = !1 } = e, { hasPopup: w = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: g = !1 } = e, { background: b = "var(--background-fill-primary)" } = e, { offset: h = 0 } = e;
  function F(c) {
    $l.call(this, n, c);
  }
  return n.$$set = (c) => {
    "Icon" in c && t(0, i = c.Icon), "label" in c && t(1, f = c.label), "show_label" in c && t(2, o = c.show_label), "pending" in c && t(3, r = c.pending), "size" in c && t(4, s = c.size), "padded" in c && t(5, a = c.padded), "highlight" in c && t(6, _ = c.highlight), "disabled" in c && t(7, u = c.disabled), "hasPopup" in c && t(8, w = c.hasPopup), "color" in c && t(13, d = c.color), "transparent" in c && t(9, g = c.transparent), "background" in c && t(10, b = c.background), "offset" in c && t(11, h = c.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = _ ? "var(--color-accent)" : d);
  }, [
    i,
    f,
    o,
    r,
    s,
    a,
    _,
    u,
    w,
    g,
    b,
    h,
    l,
    d,
    F
  ];
}
class mn extends xl {
  constructor(e) {
    super(), ln(this, e, dn, cn, on, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: bn,
  append: Ee,
  attr: D,
  detach: hn,
  init: gn,
  insert: wn,
  noop: Pe,
  safe_not_equal: pn,
  set_style: G,
  svg_element: Me
} = window.__gradio__svelte__internal;
function kn(n) {
  let e, t, l, i;
  return {
    c() {
      e = Me("svg"), t = Me("g"), l = Me("path"), i = Me("path"), D(l, "d", "M18,6L6.087,17.913"), G(l, "fill", "none"), G(l, "fill-rule", "nonzero"), G(l, "stroke-width", "2px"), D(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), D(i, "d", "M4.364,4.364L19.636,19.636"), G(i, "fill", "none"), G(i, "fill-rule", "nonzero"), G(i, "stroke-width", "2px"), D(e, "width", "100%"), D(e, "height", "100%"), D(e, "viewBox", "0 0 24 24"), D(e, "version", "1.1"), D(e, "xmlns", "http://www.w3.org/2000/svg"), D(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), D(e, "xml:space", "preserve"), D(e, "stroke", "currentColor"), G(e, "fill-rule", "evenodd"), G(e, "clip-rule", "evenodd"), G(e, "stroke-linecap", "round"), G(e, "stroke-linejoin", "round");
    },
    m(f, o) {
      wn(f, e, o), Ee(e, t), Ee(t, l), Ee(e, i);
    },
    p: Pe,
    i: Pe,
    o: Pe,
    d(f) {
      f && hn(e);
    }
  };
}
class vn extends bn {
  constructor(e) {
    super(), gn(this, e, null, kn, pn, {});
  }
}
const yn = [
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
], lt = {
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
yn.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: lt[e][t],
      secondary: lt[e][l]
    }
  }),
  {}
);
function re(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function Ne() {
}
function qn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Bt = typeof window < "u";
let nt = Bt ? () => window.performance.now() : () => Date.now(), Et = Bt ? (n) => requestAnimationFrame(n) : Ne;
const ue = /* @__PURE__ */ new Set();
function Pt(n) {
  ue.forEach((e) => {
    e.c(n) || (ue.delete(e), e.f());
  }), ue.size !== 0 && Et(Pt);
}
function Cn(n) {
  let e;
  return ue.size === 0 && Et(Pt), {
    promise: new Promise((t) => {
      ue.add(e = { c: n, f: t });
    }),
    abort() {
      ue.delete(e);
    }
  };
}
const ae = [];
function Mn(n, e = Ne) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (qn(n, r) && (n = r, t)) {
      const s = !ae.length;
      for (const a of l)
        a[1](), ae.push(a, n);
      if (s) {
        for (let a = 0; a < ae.length; a += 2)
          ae[a][0](ae[a + 1]);
        ae.length = 0;
      }
    }
  }
  function f(r) {
    i(r(n));
  }
  function o(r, s = Ne) {
    const a = [r, s];
    return l.add(a), l.size === 1 && (t = e(i, f) || Ne), r(n), () => {
      l.delete(a), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: o };
}
function it(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Xe(n, e, t, l) {
  if (typeof t == "number" || it(t)) {
    const i = l - t, f = (t - e) / (n.dt || 1 / 60), o = n.opts.stiffness * i, r = n.opts.damping * f, s = (o - r) * n.inv_mass, a = (f + s) * n.dt;
    return Math.abs(a) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, it(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Xe(n, e[f], t[f], l[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Xe(n, e[f], t[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function ft(n, e = {}) {
  const t = Mn(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let o, r, s, a = n, _ = n, u = 1, w = 0, d = !1;
  function g(h, F = {}) {
    _ = h;
    const c = s = {};
    return n == null || F.hard || b.stiffness >= 1 && b.damping >= 1 ? (d = !0, o = nt(), a = h, t.set(n = _), Promise.resolve()) : (F.soft && (w = 1 / ((F.soft === !0 ? 0.5 : +F.soft) * 60), u = 0), r || (o = nt(), d = !1, r = Cn((m) => {
      if (d)
        return d = !1, r = null, !1;
      u = Math.min(u + w, 1);
      const C = {
        inv_mass: u,
        opts: b,
        settled: !0,
        dt: (m - o) * 60 / 1e3
      }, z = Xe(C, a, n, _);
      return o = m, a = n, t.set(n = z), C.settled && (r = null), !C.settled;
    })), new Promise((m) => {
      r.promise.then(() => {
        c === s && m();
      });
    }));
  }
  const b = {
    set: g,
    update: (h, F) => g(h(_, n), F),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return b;
}
const {
  SvelteComponent: Fn,
  append: T,
  attr: M,
  component_subscribe: ot,
  detach: jn,
  element: Ln,
  init: Sn,
  insert: zn,
  noop: st,
  safe_not_equal: Nn,
  set_style: Fe,
  svg_element: K,
  toggle_class: at
} = window.__gradio__svelte__internal, { onMount: Vn } = window.__gradio__svelte__internal;
function In(n) {
  let e, t, l, i, f, o, r, s, a, _, u, w;
  return {
    c() {
      e = Ln("div"), t = K("svg"), l = K("g"), i = K("path"), f = K("path"), o = K("path"), r = K("path"), s = K("g"), a = K("path"), _ = K("path"), u = K("path"), w = K("path"), M(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), M(i, "fill", "#FF7C00"), M(i, "fill-opacity", "0.4"), M(i, "class", "svelte-43sxxs"), M(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), M(f, "fill", "#FF7C00"), M(f, "class", "svelte-43sxxs"), M(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), M(o, "fill", "#FF7C00"), M(o, "fill-opacity", "0.4"), M(o, "class", "svelte-43sxxs"), M(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), M(r, "fill", "#FF7C00"), M(r, "class", "svelte-43sxxs"), Fe(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), M(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), M(a, "fill", "#FF7C00"), M(a, "fill-opacity", "0.4"), M(a, "class", "svelte-43sxxs"), M(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), M(_, "fill", "#FF7C00"), M(_, "class", "svelte-43sxxs"), M(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), M(u, "fill", "#FF7C00"), M(u, "fill-opacity", "0.4"), M(u, "class", "svelte-43sxxs"), M(w, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), M(w, "fill", "#FF7C00"), M(w, "class", "svelte-43sxxs"), Fe(s, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), M(t, "viewBox", "-1200 -1200 3000 3000"), M(t, "fill", "none"), M(t, "xmlns", "http://www.w3.org/2000/svg"), M(t, "class", "svelte-43sxxs"), M(e, "class", "svelte-43sxxs"), at(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(d, g) {
      zn(d, e, g), T(e, t), T(t, l), T(l, i), T(l, f), T(l, o), T(l, r), T(t, s), T(s, a), T(s, _), T(s, u), T(s, w);
    },
    p(d, [g]) {
      g & /*$top*/
      2 && Fe(l, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), g & /*$bottom*/
      4 && Fe(s, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), g & /*margin*/
      1 && at(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: st,
    o: st,
    d(d) {
      d && jn(e);
    }
  };
}
function Zn(n, e, t) {
  let l, i;
  var f = this && this.__awaiter || function(d, g, b, h) {
    function F(c) {
      return c instanceof b ? c : new b(function(m) {
        m(c);
      });
    }
    return new (b || (b = Promise))(function(c, m) {
      function C(L) {
        try {
          k(h.next(L));
        } catch (P) {
          m(P);
        }
      }
      function z(L) {
        try {
          k(h.throw(L));
        } catch (P) {
          m(P);
        }
      }
      function k(L) {
        L.done ? c(L.value) : F(L.value).then(C, z);
      }
      k((h = h.apply(d, g || [])).next());
    });
  };
  let { margin: o = !0 } = e;
  const r = ft([0, 0]);
  ot(n, r, (d) => t(1, l = d));
  const s = ft([0, 0]);
  ot(n, s, (d) => t(2, i = d));
  let a;
  function _() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function u() {
    return f(this, void 0, void 0, function* () {
      yield _(), a || u();
    });
  }
  function w() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), u();
    });
  }
  return Vn(() => (w(), () => a = !0)), n.$$set = (d) => {
    "margin" in d && t(0, o = d.margin);
  }, [o, l, i, r, s];
}
class An extends Fn {
  constructor(e) {
    super(), Sn(this, e, Zn, In, Nn, { margin: 0 });
  }
}
const {
  SvelteComponent: Bn,
  append: ne,
  attr: X,
  binding_callbacks: rt,
  check_outros: Ye,
  create_component: Dt,
  create_slot: Tt,
  destroy_component: Kt,
  destroy_each: Ot,
  detach: v,
  element: R,
  empty: ce,
  ensure_array_like: Ie,
  get_all_dirty_from_scope: Xt,
  get_slot_changes: Yt,
  group_outros: Ge,
  init: En,
  insert: y,
  mount_component: Gt,
  noop: Re,
  safe_not_equal: Pn,
  set_data: E,
  set_style: te,
  space: B,
  text: j,
  toggle_class: A,
  transition_in: O,
  transition_out: H,
  update_slot_base: Rt
} = window.__gradio__svelte__internal, { tick: Dn } = window.__gradio__svelte__internal, { onDestroy: Tn } = window.__gradio__svelte__internal, { createEventDispatcher: Kn } = window.__gradio__svelte__internal, On = (n) => ({}), _t = (n) => ({}), Xn = (n) => ({}), ut = (n) => ({});
function ct(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l[43] = t, l;
}
function dt(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l;
}
function Yn(n) {
  let e, t, l, i, f = (
    /*i18n*/
    n[1]("common.error") + ""
  ), o, r, s;
  t = new mn({
    props: {
      Icon: vn,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const a = (
    /*#slots*/
    n[30].error
  ), _ = Tt(
    a,
    n,
    /*$$scope*/
    n[29],
    _t
  );
  return {
    c() {
      e = R("div"), Dt(t.$$.fragment), l = B(), i = R("span"), o = j(f), r = B(), _ && _.c(), X(e, "class", "clear-status svelte-16nch4a"), X(i, "class", "error svelte-16nch4a");
    },
    m(u, w) {
      y(u, e, w), Gt(t, e, null), y(u, l, w), y(u, i, w), ne(i, o), y(u, r, w), _ && _.m(u, w), s = !0;
    },
    p(u, w) {
      const d = {};
      w[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      u[1]("common.clear")), t.$set(d), (!s || w[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      u[1]("common.error") + "") && E(o, f), _ && _.p && (!s || w[0] & /*$$scope*/
      536870912) && Rt(
        _,
        a,
        u,
        /*$$scope*/
        u[29],
        s ? Yt(
          a,
          /*$$scope*/
          u[29],
          w,
          On
        ) : Xt(
          /*$$scope*/
          u[29]
        ),
        _t
      );
    },
    i(u) {
      s || (O(t.$$.fragment, u), O(_, u), s = !0);
    },
    o(u) {
      H(t.$$.fragment, u), H(_, u), s = !1;
    },
    d(u) {
      u && (v(e), v(l), v(i), v(r)), Kt(t), _ && _.d(u);
    }
  };
}
function Gn(n) {
  let e, t, l, i, f, o, r, s, a, _ = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && mt(n)
  );
  function u(m, C) {
    if (
      /*progress*/
      m[7]
    )
      return Jn;
    if (
      /*queue_position*/
      m[2] !== null && /*queue_size*/
      m[3] !== void 0 && /*queue_position*/
      m[2] >= 0
    )
      return Hn;
    if (
      /*queue_position*/
      m[2] === 0
    )
      return Rn;
  }
  let w = u(n), d = w && w(n), g = (
    /*timer*/
    n[5] && gt(n)
  );
  const b = [xn, Wn], h = [];
  function F(m, C) {
    return (
      /*last_progress_level*/
      m[15] != null ? 0 : (
        /*show_progress*/
        m[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = F(n)) && (o = h[f] = b[f](n));
  let c = !/*timer*/
  n[5] && Ct(n);
  return {
    c() {
      _ && _.c(), e = B(), t = R("div"), d && d.c(), l = B(), g && g.c(), i = B(), o && o.c(), r = B(), c && c.c(), s = ce(), X(t, "class", "progress-text svelte-16nch4a"), A(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), A(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(m, C) {
      _ && _.m(m, C), y(m, e, C), y(m, t, C), d && d.m(t, null), ne(t, l), g && g.m(t, null), y(m, i, C), ~f && h[f].m(m, C), y(m, r, C), c && c.m(m, C), y(m, s, C), a = !0;
    },
    p(m, C) {
      /*variant*/
      m[8] === "default" && /*show_eta_bar*/
      m[18] && /*show_progress*/
      m[6] === "full" ? _ ? _.p(m, C) : (_ = mt(m), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), w === (w = u(m)) && d ? d.p(m, C) : (d && d.d(1), d = w && w(m), d && (d.c(), d.m(t, l))), /*timer*/
      m[5] ? g ? g.p(m, C) : (g = gt(m), g.c(), g.m(t, null)) : g && (g.d(1), g = null), (!a || C[0] & /*variant*/
      256) && A(
        t,
        "meta-text-center",
        /*variant*/
        m[8] === "center"
      ), (!a || C[0] & /*variant*/
      256) && A(
        t,
        "meta-text",
        /*variant*/
        m[8] === "default"
      );
      let z = f;
      f = F(m), f === z ? ~f && h[f].p(m, C) : (o && (Ge(), H(h[z], 1, 1, () => {
        h[z] = null;
      }), Ye()), ~f ? (o = h[f], o ? o.p(m, C) : (o = h[f] = b[f](m), o.c()), O(o, 1), o.m(r.parentNode, r)) : o = null), /*timer*/
      m[5] ? c && (Ge(), H(c, 1, 1, () => {
        c = null;
      }), Ye()) : c ? (c.p(m, C), C[0] & /*timer*/
      32 && O(c, 1)) : (c = Ct(m), c.c(), O(c, 1), c.m(s.parentNode, s));
    },
    i(m) {
      a || (O(o), O(c), a = !0);
    },
    o(m) {
      H(o), H(c), a = !1;
    },
    d(m) {
      m && (v(e), v(t), v(i), v(r), v(s)), _ && _.d(m), d && d.d(), g && g.d(), ~f && h[f].d(m), c && c.d(m);
    }
  };
}
function mt(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = R("div"), X(e, "class", "eta-bar svelte-16nch4a"), te(e, "transform", t);
    },
    m(l, i) {
      y(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && te(e, "transform", t);
    },
    d(l) {
      l && v(e);
    }
  };
}
function Rn(n) {
  let e;
  return {
    c() {
      e = j("processing |");
    },
    m(t, l) {
      y(t, e, l);
    },
    p: Re,
    d(t) {
      t && v(e);
    }
  };
}
function Hn(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, o;
  return {
    c() {
      e = j("queue: "), l = j(t), i = j("/"), f = j(
        /*queue_size*/
        n[3]
      ), o = j(" |");
    },
    m(r, s) {
      y(r, e, s), y(r, l, s), y(r, i, s), y(r, f, s), y(r, o, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && E(l, t), s[0] & /*queue_size*/
      8 && E(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (v(e), v(l), v(i), v(f), v(o));
    }
  };
}
function Jn(n) {
  let e, t = Ie(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = ht(dt(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ce();
    },
    m(i, f) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const r = dt(i, t, o);
          l[o] ? l[o].p(r, f) : (l[o] = ht(r), l[o].c(), l[o].m(e.parentNode, e));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && v(e), Ot(l, i);
    }
  };
}
function bt(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), l, i, f = " ", o;
  function r(_, u) {
    return (
      /*p*/
      _[41].length != null ? Un : Qn
    );
  }
  let s = r(n), a = s(n);
  return {
    c() {
      a.c(), e = B(), l = j(t), i = j(" | "), o = j(f);
    },
    m(_, u) {
      a.m(_, u), y(_, e, u), y(_, l, u), y(_, i, u), y(_, o, u);
    },
    p(_, u) {
      s === (s = r(_)) && a ? a.p(_, u) : (a.d(1), a = s(_), a && (a.c(), a.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && E(l, t);
    },
    d(_) {
      _ && (v(e), v(l), v(i), v(o)), a.d(_);
    }
  };
}
function Qn(n) {
  let e = re(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = j(e);
    },
    m(l, i) {
      y(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = re(
        /*p*/
        l[41].index || 0
      ) + "") && E(t, e);
    },
    d(l) {
      l && v(t);
    }
  };
}
function Un(n) {
  let e = re(
    /*p*/
    n[41].index || 0
  ) + "", t, l, i = re(
    /*p*/
    n[41].length
  ) + "", f;
  return {
    c() {
      t = j(e), l = j("/"), f = j(i);
    },
    m(o, r) {
      y(o, t, r), y(o, l, r), y(o, f, r);
    },
    p(o, r) {
      r[0] & /*progress*/
      128 && e !== (e = re(
        /*p*/
        o[41].index || 0
      ) + "") && E(t, e), r[0] & /*progress*/
      128 && i !== (i = re(
        /*p*/
        o[41].length
      ) + "") && E(f, i);
    },
    d(o) {
      o && (v(t), v(l), v(f));
    }
  };
}
function ht(n) {
  let e, t = (
    /*p*/
    n[41].index != null && bt(n)
  );
  return {
    c() {
      t && t.c(), e = ce();
    },
    m(l, i) {
      t && t.m(l, i), y(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].index != null ? t ? t.p(l, i) : (t = bt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && v(e), t && t.d(l);
    }
  };
}
function gt(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = j(
        /*formatted_timer*/
        n[20]
      ), l = j(t), i = j("s");
    },
    m(f, o) {
      y(f, e, o), y(f, l, o), y(f, i, o);
    },
    p(f, o) {
      o[0] & /*formatted_timer*/
      1048576 && E(
        e,
        /*formatted_timer*/
        f[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && E(l, t);
    },
    d(f) {
      f && (v(e), v(l), v(i));
    }
  };
}
function Wn(n) {
  let e, t;
  return e = new An({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Dt(e.$$.fragment);
    },
    m(l, i) {
      Gt(e, l, i), t = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), e.$set(f);
    },
    i(l) {
      t || (O(e.$$.fragment, l), t = !0);
    },
    o(l) {
      H(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Kt(e, l);
    }
  };
}
function xn(n) {
  let e, t, l, i, f, o = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && wt(n)
  );
  return {
    c() {
      e = R("div"), t = R("div"), r && r.c(), l = B(), i = R("div"), f = R("div"), X(t, "class", "progress-level-inner svelte-16nch4a"), X(f, "class", "progress-bar svelte-16nch4a"), te(f, "width", o), X(i, "class", "progress-bar-wrap svelte-16nch4a"), X(e, "class", "progress-level svelte-16nch4a");
    },
    m(s, a) {
      y(s, e, a), ne(e, t), r && r.m(t, null), ne(e, l), ne(e, i), ne(i, f), n[31](f);
    },
    p(s, a) {
      /*progress*/
      s[7] != null ? r ? r.p(s, a) : (r = wt(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      s[15] * 100}%`) && te(f, "width", o);
    },
    i: Re,
    o: Re,
    d(s) {
      s && v(e), r && r.d(), n[31](null);
    }
  };
}
function wt(n) {
  let e, t = Ie(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = qt(ct(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = ce();
    },
    m(i, f) {
      for (let o = 0; o < l.length; o += 1)
        l[o] && l[o].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Ie(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const r = ct(i, t, o);
          l[o] ? l[o].p(r, f) : (l[o] = qt(r), l[o].c(), l[o].m(e.parentNode, e));
        }
        for (; o < l.length; o += 1)
          l[o].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && v(e), Ot(l, i);
    }
  };
}
function pt(n) {
  let e, t, l, i, f = (
    /*i*/
    n[43] !== 0 && $n()
  ), o = (
    /*p*/
    n[41].desc != null && kt(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && vt()
  ), s = (
    /*progress_level*/
    n[14] != null && yt(n)
  );
  return {
    c() {
      f && f.c(), e = B(), o && o.c(), t = B(), r && r.c(), l = B(), s && s.c(), i = ce();
    },
    m(a, _) {
      f && f.m(a, _), y(a, e, _), o && o.m(a, _), y(a, t, _), r && r.m(a, _), y(a, l, _), s && s.m(a, _), y(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[41].desc != null ? o ? o.p(a, _) : (o = kt(a), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? r || (r = vt(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? s ? s.p(a, _) : (s = yt(a), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(a) {
      a && (v(e), v(t), v(l), v(i)), f && f.d(a), o && o.d(a), r && r.d(a), s && s.d(a);
    }
  };
}
function $n(n) {
  let e;
  return {
    c() {
      e = j(" /");
    },
    m(t, l) {
      y(t, e, l);
    },
    d(t) {
      t && v(e);
    }
  };
}
function kt(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = j(e);
    },
    m(l, i) {
      y(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[41].desc + "") && E(t, e);
    },
    d(l) {
      l && v(t);
    }
  };
}
function vt(n) {
  let e;
  return {
    c() {
      e = j("-");
    },
    m(t, l) {
      y(t, e, l);
    },
    d(t) {
      t && v(e);
    }
  };
}
function yt(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = j(e), l = j("%");
    },
    m(i, f) {
      y(i, t, f), y(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && E(t, e);
    },
    d(i) {
      i && (v(t), v(l));
    }
  };
}
function qt(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && pt(n)
  );
  return {
    c() {
      t && t.c(), e = ce();
    },
    m(l, i) {
      t && t.m(l, i), y(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[43]
      ] != null ? t ? t.p(l, i) : (t = pt(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && v(e), t && t.d(l);
    }
  };
}
function Ct(n) {
  let e, t, l, i;
  const f = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), o = Tt(
    f,
    n,
    /*$$scope*/
    n[29],
    ut
  );
  return {
    c() {
      e = R("p"), t = j(
        /*loading_text*/
        n[9]
      ), l = B(), o && o.c(), X(e, "class", "loading svelte-16nch4a");
    },
    m(r, s) {
      y(r, e, s), ne(e, t), y(r, l, s), o && o.m(r, s), i = !0;
    },
    p(r, s) {
      (!i || s[0] & /*loading_text*/
      512) && E(
        t,
        /*loading_text*/
        r[9]
      ), o && o.p && (!i || s[0] & /*$$scope*/
      536870912) && Rt(
        o,
        f,
        r,
        /*$$scope*/
        r[29],
        i ? Yt(
          f,
          /*$$scope*/
          r[29],
          s,
          Xn
        ) : Xt(
          /*$$scope*/
          r[29]
        ),
        ut
      );
    },
    i(r) {
      i || (O(o, r), i = !0);
    },
    o(r) {
      H(o, r), i = !1;
    },
    d(r) {
      r && (v(e), v(l)), o && o.d(r);
    }
  };
}
function ei(n) {
  let e, t, l, i, f;
  const o = [Gn, Yn], r = [];
  function s(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(n)) && (l = r[t] = o[t](n)), {
    c() {
      e = R("div"), l && l.c(), X(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-16nch4a"), A(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), A(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), A(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), A(
        e,
        "border",
        /*border*/
        n[12]
      ), te(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), te(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      y(a, e, _), ~t && r[t].m(e, null), n[33](e), f = !0;
    },
    p(a, _) {
      let u = t;
      t = s(a), t === u ? ~t && r[t].p(a, _) : (l && (Ge(), H(r[u], 1, 1, () => {
        r[u] = null;
      }), Ye()), ~t ? (l = r[t], l ? l.p(a, _) : (l = r[t] = o[t](a), l.c()), O(l, 1), l.m(e, null)) : l = null), (!f || _[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      a[8] + " " + /*show_progress*/
      a[6] + " svelte-16nch4a")) && X(e, "class", i), (!f || _[0] & /*variant, show_progress, status, show_progress*/
      336) && A(e, "hide", !/*status*/
      a[4] || /*status*/
      a[4] === "complete" || /*show_progress*/
      a[6] === "hidden"), (!f || _[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && A(
        e,
        "translucent",
        /*variant*/
        a[8] === "center" && /*status*/
        (a[4] === "pending" || /*status*/
        a[4] === "error") || /*translucent*/
        a[11] || /*show_progress*/
        a[6] === "minimal"
      ), (!f || _[0] & /*variant, show_progress, status*/
      336) && A(
        e,
        "generating",
        /*status*/
        a[4] === "generating"
      ), (!f || _[0] & /*variant, show_progress, border*/
      4416) && A(
        e,
        "border",
        /*border*/
        a[12]
      ), _[0] & /*absolute*/
      1024 && te(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && te(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (O(l), f = !0);
    },
    o(a) {
      H(l), f = !1;
    },
    d(a) {
      a && v(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var ti = function(n, e, t, l) {
  function i(f) {
    return f instanceof t ? f : new t(function(o) {
      o(f);
    });
  }
  return new (t || (t = Promise))(function(f, o) {
    function r(_) {
      try {
        a(l.next(_));
      } catch (u) {
        o(u);
      }
    }
    function s(_) {
      try {
        a(l.throw(_));
      } catch (u) {
        o(u);
      }
    }
    function a(_) {
      _.done ? f(_.value) : i(_.value).then(r, s);
    }
    a((l = l.apply(n, e || [])).next());
  });
};
let je = [], De = !1;
function li(n) {
  return ti(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (je.push(e), !De)
        De = !0;
      else
        return;
      yield Dn(), requestAnimationFrame(() => {
        let l = [0, 0];
        for (let i = 0; i < je.length; i++) {
          const o = je[i].getBoundingClientRect();
          (i === 0 || o.top + window.scrollY <= l[0]) && (l[0] = o.top + window.scrollY, l[1] = i);
        }
        window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), De = !1, je = [];
      });
    }
  });
}
function ni(n, e, t) {
  let l, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const o = Kn();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: a } = e, { queue_size: _ } = e, { status: u } = e, { scroll_to_output: w = !1 } = e, { timer: d = !0 } = e, { show_progress: g = "full" } = e, { message: b = null } = e, { progress: h = null } = e, { variant: F = "default" } = e, { loading_text: c = "Loading..." } = e, { absolute: m = !0 } = e, { translucent: C = !1 } = e, { border: z = !1 } = e, { autoscroll: k } = e, L, P = !1, ie = 0, J = 0, W = null, q = null, x = 0, S = null, Z, V = null, $ = !0;
  const fe = () => {
    t(0, s = t(27, W = t(19, ee = null))), t(25, ie = performance.now()), t(26, J = 0), P = !0, ke();
  };
  function ke() {
    requestAnimationFrame(() => {
      t(26, J = (performance.now() - ie) / 1e3), P && ke();
    });
  }
  function ve() {
    t(26, J = 0), t(0, s = t(27, W = t(19, ee = null))), P && (P = !1);
  }
  Tn(() => {
    P && ve();
  });
  let ee = null;
  function Q(p) {
    rt[p ? "unshift" : "push"](() => {
      V = p, t(16, V), t(7, h), t(14, S), t(15, Z);
    });
  }
  const de = () => {
    o("clear_status");
  };
  function Jt(p) {
    rt[p ? "unshift" : "push"](() => {
      L = p, t(13, L);
    });
  }
  return n.$$set = (p) => {
    "i18n" in p && t(1, r = p.i18n), "eta" in p && t(0, s = p.eta), "queue_position" in p && t(2, a = p.queue_position), "queue_size" in p && t(3, _ = p.queue_size), "status" in p && t(4, u = p.status), "scroll_to_output" in p && t(22, w = p.scroll_to_output), "timer" in p && t(5, d = p.timer), "show_progress" in p && t(6, g = p.show_progress), "message" in p && t(23, b = p.message), "progress" in p && t(7, h = p.progress), "variant" in p && t(8, F = p.variant), "loading_text" in p && t(9, c = p.loading_text), "absolute" in p && t(10, m = p.absolute), "translucent" in p && t(11, C = p.translucent), "border" in p && t(12, z = p.border), "autoscroll" in p && t(24, k = p.autoscroll), "$$scope" in p && t(29, f = p.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = W), s != null && W !== s && (t(28, q = (performance.now() - ie) / 1e3 + s), t(19, ee = q.toFixed(1)), t(27, W = s))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, x = q === null || q <= 0 || !J ? null : Math.min(J / q, 1)), n.$$.dirty[0] & /*progress*/
    128 && h != null && t(18, $ = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (h != null ? t(14, S = h.map((p) => {
      if (p.index != null && p.length != null)
        return p.index / p.length;
      if (p.progress != null)
        return p.progress;
    })) : t(14, S = null), S ? (t(15, Z = S[S.length - 1]), V && (Z === 0 ? t(16, V.style.transition = "0", V) : t(16, V.style.transition = "150ms", V))) : t(15, Z = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? fe() : ve()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && L && w && (u === "pending" || u === "complete") && li(L, k), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = J.toFixed(1));
  }, [
    s,
    r,
    a,
    _,
    u,
    d,
    g,
    h,
    F,
    c,
    m,
    C,
    z,
    L,
    S,
    Z,
    V,
    x,
    $,
    ee,
    l,
    o,
    w,
    b,
    k,
    ie,
    J,
    W,
    q,
    f,
    i,
    Q,
    de,
    Jt
  ];
}
class ii extends Bn {
  constructor(e) {
    super(), En(
      this,
      e,
      ni,
      ei,
      Pn,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: fi,
  add_render_callback: oi,
  append: he,
  assign: si,
  attr: Ve,
  check_outros: ai,
  create_component: He,
  destroy_component: Je,
  destroy_each: ri,
  detach: we,
  element: Ze,
  ensure_array_like: Mt,
  get_spread_object: _i,
  get_spread_update: ui,
  group_outros: ci,
  init: di,
  insert: pe,
  listen: mi,
  mount_component: Qe,
  safe_not_equal: bi,
  select_option: Ft,
  select_value: hi,
  set_data: Ue,
  set_input_value: jt,
  space: Te,
  text: We,
  toggle_class: gi,
  transition_in: _e,
  transition_out: ge
} = window.__gradio__svelte__internal, { onMount: wi } = window.__gradio__svelte__internal;
function Lt(n, e, t) {
  const l = n.slice();
  return l[25] = e[t], l;
}
function St(n) {
  let e, t;
  const l = [
    {
      autoscroll: (
        /*gradio*/
        n[10].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[10].i18n
    ) },
    /*loading_status*/
    n[9]
  ];
  let i = {};
  for (let f = 0; f < l.length; f += 1)
    i = si(i, l[f]);
  return e = new ii({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[18]
  ), {
    c() {
      He(e.$$.fragment);
    },
    m(f, o) {
      Qe(e, f, o), t = !0;
    },
    p(f, o) {
      const r = o & /*gradio, loading_status*/
      1536 ? ui(l, [
        o & /*gradio*/
        1024 && {
          autoscroll: (
            /*gradio*/
            f[10].autoscroll
          )
        },
        o & /*gradio*/
        1024 && { i18n: (
          /*gradio*/
          f[10].i18n
        ) },
        o & /*loading_status*/
        512 && _i(
          /*loading_status*/
          f[9]
        )
      ]) : {};
      e.$set(r);
    },
    i(f) {
      t || (_e(e.$$.fragment, f), t = !0);
    },
    o(f) {
      ge(e.$$.fragment, f), t = !1;
    },
    d(f) {
      Je(e, f);
    }
  };
}
function pi(n) {
  let e;
  return {
    c() {
      e = We(
        /*label*/
        n[4]
      );
    },
    m(t, l) {
      pe(t, e, l);
    },
    p(t, l) {
      l & /*label*/
      16 && Ue(
        e,
        /*label*/
        t[4]
      );
    },
    d(t) {
      t && we(e);
    }
  };
}
function zt(n) {
  let e, t = (
    /*item*/
    n[25][0] + ""
  ), l, i;
  return {
    c() {
      e = Ze("option"), l = We(t), e.__value = i = /*item*/
      n[25][1], jt(e, e.__value);
    },
    m(f, o) {
      pe(f, e, o), he(e, l);
    },
    p(f, o) {
      o & /*options*/
      16384 && t !== (t = /*item*/
      f[25][0] + "") && Ue(l, t), o & /*options*/
      16384 && i !== (i = /*item*/
      f[25][1]) && (e.__value = i, jt(e, e.__value));
    },
    d(f) {
      f && we(e);
    }
  };
}
function Nt(n) {
  let e, t;
  return {
    c() {
      e = Ze("span"), t = We(
        /*errMsg*/
        n[12]
      ), Ve(e, "class", "dp_project--error svelte-l3vjji");
    },
    m(l, i) {
      pe(l, e, i), he(e, t);
    },
    p(l, i) {
      i & /*errMsg*/
      4096 && Ue(
        t,
        /*errMsg*/
        l[12]
      );
    },
    d(l) {
      l && we(e);
    }
  };
}
function ki(n) {
  let e, t, l, i, f, o, r, s, a, _, u = (
    /*loading_status*/
    n[9] && St(n)
  );
  l = new Wl({
    props: {
      show_label: (
        /*show_label*/
        n[6]
      ),
      info: void 0,
      $$slots: { default: [pi] },
      $$scope: { ctx: n }
    }
  });
  let w = Mt(
    /*options*/
    n[14]
  ), d = [];
  for (let b = 0; b < w.length; b += 1)
    d[b] = zt(Lt(n, w, b));
  let g = (
    /*isError*/
    n[13] && Nt(n)
  );
  return {
    c() {
      u && u.c(), e = Te(), t = Ze("label"), He(l.$$.fragment), i = Te(), f = Ze("select");
      for (let b = 0; b < d.length; b += 1)
        d[b].c();
      r = Te(), g && g.c(), Ve(
        f,
        "placeholder",
        /*placeholder*/
        n[5]
      ), f.disabled = o = !/*interactive*/
      n[11], Ve(f, "class", "svelte-l3vjji"), /*value*/
      n[0] === void 0 && oi(() => (
        /*select_change_handler*/
        n[19].call(f)
      )), gi(t, "container", Ht);
    },
    m(b, h) {
      u && u.m(b, h), pe(b, e, h), pe(b, t, h), Qe(l, t, null), he(t, i), he(t, f);
      for (let F = 0; F < d.length; F += 1)
        d[F] && d[F].m(f, null);
      Ft(
        f,
        /*value*/
        n[0],
        !0
      ), he(t, r), g && g.m(t, null), s = !0, a || (_ = mi(
        f,
        "change",
        /*select_change_handler*/
        n[19]
      ), a = !0);
    },
    p(b, h) {
      /*loading_status*/
      b[9] ? u ? (u.p(b, h), h & /*loading_status*/
      512 && _e(u, 1)) : (u = St(b), u.c(), _e(u, 1), u.m(e.parentNode, e)) : u && (ci(), ge(u, 1, 1, () => {
        u = null;
      }), ai());
      const F = {};
      if (h & /*show_label*/
      64 && (F.show_label = /*show_label*/
      b[6]), h & /*$$scope, label*/
      268435472 && (F.$$scope = { dirty: h, ctx: b }), l.$set(F), h & /*options*/
      16384) {
        w = Mt(
          /*options*/
          b[14]
        );
        let c;
        for (c = 0; c < w.length; c += 1) {
          const m = Lt(b, w, c);
          d[c] ? d[c].p(m, h) : (d[c] = zt(m), d[c].c(), d[c].m(f, null));
        }
        for (; c < d.length; c += 1)
          d[c].d(1);
        d.length = w.length;
      }
      (!s || h & /*placeholder*/
      32) && Ve(
        f,
        "placeholder",
        /*placeholder*/
        b[5]
      ), (!s || h & /*interactive*/
      2048 && o !== (o = !/*interactive*/
      b[11])) && (f.disabled = o), h & /*value, options*/
      16385 && Ft(
        f,
        /*value*/
        b[0]
      ), /*isError*/
      b[13] ? g ? g.p(b, h) : (g = Nt(b), g.c(), g.m(t, null)) : g && (g.d(1), g = null);
    },
    i(b) {
      s || (_e(u), _e(l.$$.fragment, b), s = !0);
    },
    o(b) {
      ge(u), ge(l.$$.fragment, b), s = !1;
    },
    d(b) {
      b && (we(e), we(t)), u && u.d(b), Je(l), ri(d, b), g && g.d(), a = !1, _();
    }
  };
}
function vi(n) {
  let e, t;
  return e = new ml({
    props: {
      visible: (
        /*visible*/
        n[3]
      ),
      elem_id: (
        /*elem_id*/
        n[1]
      ),
      elem_classes: (
        /*elem_classes*/
        n[2]
      ),
      padding: Ht,
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[7]
      ),
      min_width: (
        /*min_width*/
        n[8]
      ),
      $$slots: { default: [ki] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      He(e.$$.fragment);
    },
    m(l, i) {
      Qe(e, l, i), t = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      8 && (f.visible = /*visible*/
      l[3]), i & /*elem_id*/
      2 && (f.elem_id = /*elem_id*/
      l[1]), i & /*elem_classes*/
      4 && (f.elem_classes = /*elem_classes*/
      l[2]), i & /*scale*/
      128 && (f.scale = /*scale*/
      l[7]), i & /*min_width*/
      256 && (f.min_width = /*min_width*/
      l[8]), i & /*$$scope, errMsg, isError, placeholder, interactive, value, options, show_label, label, gradio, loading_status*/
      268467825 && (f.$$scope = { dirty: i, ctx: l }), e.$set(f);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ge(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Je(e, l);
    }
  };
}
const Ht = !0;
function yi(n, e, t) {
  var l = this && this.__awaiter || function(q, x, S, Z) {
    function V($) {
      return $ instanceof S ? $ : new S(function(fe) {
        fe($);
      });
    }
    return new (S || (S = Promise))(function($, fe) {
      function ke(Q) {
        try {
          ee(Z.next(Q));
        } catch (de) {
          fe(de);
        }
      }
      function ve(Q) {
        try {
          ee(Z.throw(Q));
        } catch (de) {
          fe(de);
        }
      }
      function ee(Q) {
        Q.done ? $(Q.value) : V(Q.value).then(ke, ve);
      }
      ee((Z = Z.apply(q, x || [])).next());
    });
  };
  let { elem_id: i = "" } = e, { elem_classes: f = [] } = e, { visible: o = !0 } = e, { value: r } = e, { value_is_output: s = !1 } = e, { choices: a } = e, { label: _ = "project" } = e, { placeholder: u = "Select a project" } = e, { show_label: w } = e, { scale: d = null } = e, { min_width: g = void 0 } = e, { loading_status: b } = e, { gradio: h } = e, { interactive: F } = e, c = !1, { errMsg: m = "Please select a project" } = e;
  function C() {
    return t(13, c = !r), c;
  }
  let z = /* @__PURE__ */ new Map();
  function k() {
    document.cookie.split(";").forEach((q) => {
      const [x, S] = q.trim().split("=");
      z.set(x, S);
    });
  }
  let L = [];
  function P() {
    return l(this, void 0, void 0, function* () {
      const q = z.get("appAccessKey"), x = z.get("clientName"), S = yield fetch("https://openapi.test.dp.tech/openapi/v1/open/user/project/list", {
        headers: { accessKey: q, "x-app-key": x }
      });
      if (S.ok) {
        const Z = yield S.json();
        t(14, L = Z.data.items.map((V) => [V.projectName, V.projectId]));
      }
    });
  }
  wi(() => {
    k(), P();
  });
  function ie() {
    h.dispatch("change"), s || h.dispatch("input");
  }
  const J = () => h.dispatch("clear_status", b);
  function W() {
    r = hi(this), t(0, r), t(14, L);
  }
  return n.$$set = (q) => {
    "elem_id" in q && t(1, i = q.elem_id), "elem_classes" in q && t(2, f = q.elem_classes), "visible" in q && t(3, o = q.visible), "value" in q && t(0, r = q.value), "value_is_output" in q && t(15, s = q.value_is_output), "choices" in q && t(16, a = q.choices), "label" in q && t(4, _ = q.label), "placeholder" in q && t(5, u = q.placeholder), "show_label" in q && t(6, w = q.show_label), "scale" in q && t(7, d = q.scale), "min_width" in q && t(8, g = q.min_width), "loading_status" in q && t(9, b = q.loading_status), "gradio" in q && t(10, h = q.gradio), "interactive" in q && t(11, F = q.interactive), "errMsg" in q && t(12, m = q.errMsg);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    1 && (C(), ie());
  }, [
    r,
    i,
    f,
    o,
    _,
    u,
    w,
    d,
    g,
    b,
    h,
    F,
    m,
    c,
    L,
    s,
    a,
    C,
    J,
    W
  ];
}
class qi extends fi {
  constructor(e) {
    super(), di(this, e, yi, vi, bi, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 0,
      value_is_output: 15,
      choices: 16,
      label: 4,
      placeholder: 5,
      show_label: 6,
      scale: 7,
      min_width: 8,
      loading_status: 9,
      gradio: 10,
      interactive: 11,
      errMsg: 12,
      validate: 17
    });
  }
  get validate() {
    return this.$$.ctx[17];
  }
}
export {
  qi as default
};
