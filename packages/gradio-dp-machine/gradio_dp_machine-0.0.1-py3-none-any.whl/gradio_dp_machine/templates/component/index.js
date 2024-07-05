const {
  SvelteComponent: il,
  assign: fl,
  create_slot: sl,
  detach: ol,
  element: al,
  get_all_dirty_from_scope: rl,
  get_slot_changes: _l,
  get_spread_update: ul,
  init: cl,
  insert: dl,
  safe_not_equal: ml,
  set_dynamic_element_data: lt,
  set_style: T,
  toggle_class: H,
  transition_in: Et,
  transition_out: Dt,
  update_slot_base: bl
} = window.__gradio__svelte__internal;
function hl(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), f = sl(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let o = 0; o < s.length; o += 1)
    r = fl(r, s[o]);
  return {
    c() {
      e = al(
        /*tag*/
        l[14]
      ), f && f.c(), lt(
        /*tag*/
        l[14]
      )(e, r), H(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), H(
        e,
        "padded",
        /*padding*/
        l[6]
      ), H(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), H(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), H(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), T(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), T(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), T(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), T(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), T(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), T(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), T(e, "border-width", "var(--block-border-width)");
    },
    m(o, a) {
      dl(o, e, a), f && f.m(e, null), n = !0;
    },
    p(o, a) {
      f && f.p && (!n || a & /*$$scope*/
      131072) && bl(
        f,
        i,
        o,
        /*$$scope*/
        o[17],
        n ? _l(
          i,
          /*$$scope*/
          o[17],
          a,
          null
        ) : rl(
          /*$$scope*/
          o[17]
        ),
        null
      ), lt(
        /*tag*/
        o[14]
      )(e, r = ul(s, [
        (!n || a & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!n || a & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!n || a & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), H(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), H(
        e,
        "padded",
        /*padding*/
        o[6]
      ), H(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), H(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), H(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), a & /*height*/
      1 && T(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), a & /*width*/
      2 && T(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), a & /*variant*/
      16 && T(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), a & /*allow_overflow*/
      2048 && T(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), a & /*scale*/
      4096 && T(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), a & /*min_width*/
      8192 && T(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      n || (Et(f, o), n = !0);
    },
    o(o) {
      Dt(f, o), n = !1;
    },
    d(o) {
      o && ol(e), f && f.d(o);
    }
  };
}
function gl(l) {
  let e, t = (
    /*tag*/
    l[14] && hl(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Et(t, n), e = !0);
    },
    o(n) {
      Dt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function pl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: s = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: o = [] } = e, { variant: a = "solid" } = e, { border_mode: _ = "base" } = e, { padding: c = !0 } = e, { type: w = "normal" } = e, { test_id: h = void 0 } = e, { explicit_call: C = !1 } = e, { container: k = !0 } = e, { visible: q = !0 } = e, { allow_overflow: F = !0 } = e, { scale: d = null } = e, { min_width: u = 0 } = e, p = w === "fieldset" ? "fieldset" : "div";
  const b = (m) => {
    if (m !== void 0) {
      if (typeof m == "number")
        return m + "px";
      if (typeof m == "string")
        return m;
    }
  };
  return l.$$set = (m) => {
    "height" in m && t(0, f = m.height), "width" in m && t(1, s = m.width), "elem_id" in m && t(2, r = m.elem_id), "elem_classes" in m && t(3, o = m.elem_classes), "variant" in m && t(4, a = m.variant), "border_mode" in m && t(5, _ = m.border_mode), "padding" in m && t(6, c = m.padding), "type" in m && t(16, w = m.type), "test_id" in m && t(7, h = m.test_id), "explicit_call" in m && t(8, C = m.explicit_call), "container" in m && t(9, k = m.container), "visible" in m && t(10, q = m.visible), "allow_overflow" in m && t(11, F = m.allow_overflow), "scale" in m && t(12, d = m.scale), "min_width" in m && t(13, u = m.min_width), "$$scope" in m && t(17, i = m.$$scope);
  }, [
    f,
    s,
    r,
    o,
    a,
    _,
    c,
    h,
    C,
    k,
    q,
    F,
    d,
    u,
    p,
    b,
    w,
    i,
    n
  ];
}
class wl extends il {
  constructor(e) {
    super(), cl(this, e, pl, gl, ml, {
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
  SvelteComponent: kl,
  attr: vl,
  create_slot: yl,
  detach: ql,
  element: Cl,
  get_all_dirty_from_scope: Ml,
  get_slot_changes: Fl,
  init: Ll,
  insert: Sl,
  safe_not_equal: zl,
  transition_in: Nl,
  transition_out: Vl,
  update_slot_base: Il
} = window.__gradio__svelte__internal;
function Pl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = yl(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = Cl("div"), i && i.c(), vl(e, "class", "svelte-1hnfib2");
    },
    m(f, s) {
      Sl(f, e, s), i && i.m(e, null), t = !0;
    },
    p(f, [s]) {
      i && i.p && (!t || s & /*$$scope*/
      1) && Il(
        i,
        n,
        f,
        /*$$scope*/
        f[0],
        t ? Fl(
          n,
          /*$$scope*/
          f[0],
          s,
          null
        ) : Ml(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      t || (Nl(i, f), t = !0);
    },
    o(f) {
      Vl(i, f), t = !1;
    },
    d(f) {
      f && ql(e), i && i.d(f);
    }
  };
}
function Tl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (f) => {
    "$$scope" in f && t(0, i = f.$$scope);
  }, [i, n];
}
class jl extends kl {
  constructor(e) {
    super(), Ll(this, e, Tl, Pl, zl, {});
  }
}
const {
  SvelteComponent: Zl,
  attr: nt,
  check_outros: Al,
  create_component: Bl,
  create_slot: El,
  destroy_component: Dl,
  detach: Pe,
  element: Kl,
  empty: Rl,
  get_all_dirty_from_scope: Ul,
  get_slot_changes: Gl,
  group_outros: Ol,
  init: Xl,
  insert: Te,
  mount_component: Yl,
  safe_not_equal: Hl,
  set_data: Jl,
  space: Ql,
  text: Wl,
  toggle_class: re,
  transition_in: ke,
  transition_out: je,
  update_slot_base: xl
} = window.__gradio__svelte__internal;
function it(l) {
  let e, t;
  return e = new jl({
    props: {
      $$slots: { default: [$l] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Bl(e.$$.fragment);
    },
    m(n, i) {
      Yl(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (ke(e.$$.fragment, n), t = !0);
    },
    o(n) {
      je(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Dl(e, n);
    }
  };
}
function $l(l) {
  let e;
  return {
    c() {
      e = Wl(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Te(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Jl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Pe(e);
    }
  };
}
function en(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[2].default
  ), s = El(
    f,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let r = (
    /*info*/
    l[1] && it(l)
  );
  return {
    c() {
      e = Kl("span"), s && s.c(), t = Ql(), r && r.c(), n = Rl(), nt(e, "data-testid", "block-info"), nt(e, "class", "svelte-22c38v"), re(e, "sr-only", !/*show_label*/
      l[0]), re(e, "hide", !/*show_label*/
      l[0]), re(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(o, a) {
      Te(o, e, a), s && s.m(e, null), Te(o, t, a), r && r.m(o, a), Te(o, n, a), i = !0;
    },
    p(o, [a]) {
      s && s.p && (!i || a & /*$$scope*/
      8) && xl(
        s,
        f,
        o,
        /*$$scope*/
        o[3],
        i ? Gl(
          f,
          /*$$scope*/
          o[3],
          a,
          null
        ) : Ul(
          /*$$scope*/
          o[3]
        ),
        null
      ), (!i || a & /*show_label*/
      1) && re(e, "sr-only", !/*show_label*/
      o[0]), (!i || a & /*show_label*/
      1) && re(e, "hide", !/*show_label*/
      o[0]), (!i || a & /*info*/
      2) && re(
        e,
        "has-info",
        /*info*/
        o[1] != null
      ), /*info*/
      o[1] ? r ? (r.p(o, a), a & /*info*/
      2 && ke(r, 1)) : (r = it(o), r.c(), ke(r, 1), r.m(n.parentNode, n)) : r && (Ol(), je(r, 1, 1, () => {
        r = null;
      }), Al());
    },
    i(o) {
      i || (ke(s, o), ke(r), i = !0);
    },
    o(o) {
      je(s, o), je(r), i = !1;
    },
    d(o) {
      o && (Pe(e), Pe(t), Pe(n)), s && s.d(o), r && r.d(o);
    }
  };
}
function tn(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: s = void 0 } = e;
  return l.$$set = (r) => {
    "show_label" in r && t(0, f = r.show_label), "info" in r && t(1, s = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [f, s, n, i];
}
class ln extends Zl {
  constructor(e) {
    super(), Xl(this, e, tn, en, Hl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: nn,
  append: Oe,
  attr: $,
  bubble: fn,
  create_component: sn,
  destroy_component: on,
  detach: Kt,
  element: Xe,
  init: an,
  insert: Rt,
  listen: rn,
  mount_component: _n,
  safe_not_equal: un,
  set_data: cn,
  set_style: _e,
  space: dn,
  text: mn,
  toggle_class: I,
  transition_in: bn,
  transition_out: hn
} = window.__gradio__svelte__internal;
function ft(l) {
  let e, t;
  return {
    c() {
      e = Xe("span"), t = mn(
        /*label*/
        l[1]
      ), $(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Rt(n, e, i), Oe(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && cn(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && Kt(e);
    }
  };
}
function gn(l) {
  let e, t, n, i, f, s, r, o = (
    /*show_label*/
    l[2] && ft(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = Xe("button"), o && o.c(), t = dn(), n = Xe("div"), sn(i.$$.fragment), $(n, "class", "svelte-1lrphxw"), I(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), I(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), I(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], $(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), $(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), $(
        e,
        "title",
        /*label*/
        l[1]
      ), $(e, "class", "svelte-1lrphxw"), I(
        e,
        "pending",
        /*pending*/
        l[3]
      ), I(
        e,
        "padded",
        /*padded*/
        l[5]
      ), I(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), I(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), _e(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), _e(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), _e(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(a, _) {
      Rt(a, e, _), o && o.m(e, null), Oe(e, t), Oe(e, n), _n(i, n, null), f = !0, s || (r = rn(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), s = !0);
    },
    p(a, [_]) {
      /*show_label*/
      a[2] ? o ? o.p(a, _) : (o = ft(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), (!f || _ & /*size*/
      16) && I(
        n,
        "small",
        /*size*/
        a[4] === "small"
      ), (!f || _ & /*size*/
      16) && I(
        n,
        "large",
        /*size*/
        a[4] === "large"
      ), (!f || _ & /*size*/
      16) && I(
        n,
        "medium",
        /*size*/
        a[4] === "medium"
      ), (!f || _ & /*disabled*/
      128) && (e.disabled = /*disabled*/
      a[7]), (!f || _ & /*label*/
      2) && $(
        e,
        "aria-label",
        /*label*/
        a[1]
      ), (!f || _ & /*hasPopup*/
      256) && $(
        e,
        "aria-haspopup",
        /*hasPopup*/
        a[8]
      ), (!f || _ & /*label*/
      2) && $(
        e,
        "title",
        /*label*/
        a[1]
      ), (!f || _ & /*pending*/
      8) && I(
        e,
        "pending",
        /*pending*/
        a[3]
      ), (!f || _ & /*padded*/
      32) && I(
        e,
        "padded",
        /*padded*/
        a[5]
      ), (!f || _ & /*highlight*/
      64) && I(
        e,
        "highlight",
        /*highlight*/
        a[6]
      ), (!f || _ & /*transparent*/
      512) && I(
        e,
        "transparent",
        /*transparent*/
        a[9]
      ), _ & /*disabled, _color*/
      4224 && _e(e, "color", !/*disabled*/
      a[7] && /*_color*/
      a[12] ? (
        /*_color*/
        a[12]
      ) : "var(--block-label-text-color)"), _ & /*disabled, background*/
      1152 && _e(e, "--bg-color", /*disabled*/
      a[7] ? "auto" : (
        /*background*/
        a[10]
      )), _ & /*offset*/
      2048 && _e(
        e,
        "margin-left",
        /*offset*/
        a[11] + "px"
      );
    },
    i(a) {
      f || (bn(i.$$.fragment, a), f = !0);
    },
    o(a) {
      hn(i.$$.fragment, a), f = !1;
    },
    d(a) {
      a && Kt(e), o && o.d(), on(i), s = !1, r();
    }
  };
}
function pn(l, e, t) {
  let n, { Icon: i } = e, { label: f = "" } = e, { show_label: s = !1 } = e, { pending: r = !1 } = e, { size: o = "small" } = e, { padded: a = !0 } = e, { highlight: _ = !1 } = e, { disabled: c = !1 } = e, { hasPopup: w = !1 } = e, { color: h = "var(--block-label-text-color)" } = e, { transparent: C = !1 } = e, { background: k = "var(--background-fill-primary)" } = e, { offset: q = 0 } = e;
  function F(d) {
    fn.call(this, l, d);
  }
  return l.$$set = (d) => {
    "Icon" in d && t(0, i = d.Icon), "label" in d && t(1, f = d.label), "show_label" in d && t(2, s = d.show_label), "pending" in d && t(3, r = d.pending), "size" in d && t(4, o = d.size), "padded" in d && t(5, a = d.padded), "highlight" in d && t(6, _ = d.highlight), "disabled" in d && t(7, c = d.disabled), "hasPopup" in d && t(8, w = d.hasPopup), "color" in d && t(13, h = d.color), "transparent" in d && t(9, C = d.transparent), "background" in d && t(10, k = d.background), "offset" in d && t(11, q = d.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = _ ? "var(--color-accent)" : h);
  }, [
    i,
    f,
    s,
    r,
    o,
    a,
    _,
    c,
    w,
    C,
    k,
    q,
    n,
    h,
    F
  ];
}
class wn extends nn {
  constructor(e) {
    super(), an(this, e, pn, gn, un, {
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
  SvelteComponent: kn,
  append: Re,
  attr: R,
  detach: vn,
  init: yn,
  insert: qn,
  noop: Ue,
  safe_not_equal: Cn,
  set_style: J,
  svg_element: Le
} = window.__gradio__svelte__internal;
function Mn(l) {
  let e, t, n, i;
  return {
    c() {
      e = Le("svg"), t = Le("g"), n = Le("path"), i = Le("path"), R(n, "d", "M18,6L6.087,17.913"), J(n, "fill", "none"), J(n, "fill-rule", "nonzero"), J(n, "stroke-width", "2px"), R(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), R(i, "d", "M4.364,4.364L19.636,19.636"), J(i, "fill", "none"), J(i, "fill-rule", "nonzero"), J(i, "stroke-width", "2px"), R(e, "width", "100%"), R(e, "height", "100%"), R(e, "viewBox", "0 0 24 24"), R(e, "version", "1.1"), R(e, "xmlns", "http://www.w3.org/2000/svg"), R(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), R(e, "xml:space", "preserve"), R(e, "stroke", "currentColor"), J(e, "fill-rule", "evenodd"), J(e, "clip-rule", "evenodd"), J(e, "stroke-linecap", "round"), J(e, "stroke-linejoin", "round");
    },
    m(f, s) {
      qn(f, e, s), Re(e, t), Re(t, n), Re(e, i);
    },
    p: Ue,
    i: Ue,
    o: Ue,
    d(f) {
      f && vn(e);
    }
  };
}
class Fn extends kn {
  constructor(e) {
    super(), yn(this, e, null, Mn, Cn, {});
  }
}
const Ln = [
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
], st = {
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
Ln.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: st[e][t],
      secondary: st[e][n]
    }
  }),
  {}
);
function ce(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Ze() {
}
function Sn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Ut = typeof window < "u";
let ot = Ut ? () => window.performance.now() : () => Date.now(), Gt = Ut ? (l) => requestAnimationFrame(l) : Ze;
const me = /* @__PURE__ */ new Set();
function Ot(l) {
  me.forEach((e) => {
    e.c(l) || (me.delete(e), e.f());
  }), me.size !== 0 && Gt(Ot);
}
function zn(l) {
  let e;
  return me.size === 0 && Gt(Ot), {
    promise: new Promise((t) => {
      me.add(e = { c: l, f: t });
    }),
    abort() {
      me.delete(e);
    }
  };
}
const ue = [];
function Nn(l, e = Ze) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(r) {
    if (Sn(l, r) && (l = r, t)) {
      const o = !ue.length;
      for (const a of n)
        a[1](), ue.push(a, l);
      if (o) {
        for (let a = 0; a < ue.length; a += 2)
          ue[a][0](ue[a + 1]);
        ue.length = 0;
      }
    }
  }
  function f(r) {
    i(r(l));
  }
  function s(r, o = Ze) {
    const a = [r, o];
    return n.add(a), n.size === 1 && (t = e(i, f) || Ze), r(l), () => {
      n.delete(a), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function at(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ye(l, e, t, n) {
  if (typeof t == "number" || at(t)) {
    const i = n - t, f = (t - e) / (l.dt || 1 / 60), s = l.opts.stiffness * i, r = l.opts.damping * f, o = (s - r) * l.inv_mass, a = (f + o) * l.dt;
    return Math.abs(a) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, at(t) ? new Date(t.getTime() + a) : t + a);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, f) => Ye(l, e[f], t[f], n[f])
      );
    if (typeof t == "object") {
      const i = {};
      for (const f in t)
        i[f] = Ye(l, e[f], t[f], n[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function rt(l, e = {}) {
  const t = Nn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let s, r, o, a = l, _ = l, c = 1, w = 0, h = !1;
  function C(q, F = {}) {
    _ = q;
    const d = o = {};
    return l == null || F.hard || k.stiffness >= 1 && k.damping >= 1 ? (h = !0, s = ot(), a = q, t.set(l = _), Promise.resolve()) : (F.soft && (w = 1 / ((F.soft === !0 ? 0.5 : +F.soft) * 60), c = 0), r || (s = ot(), h = !1, r = zn((u) => {
      if (h)
        return h = !1, r = null, !1;
      c = Math.min(c + w, 1);
      const p = {
        inv_mass: c,
        opts: k,
        settled: !0,
        dt: (u - s) * 60 / 1e3
      }, b = Ye(p, a, l, _);
      return s = u, a = l, t.set(l = b), p.settled && (r = null), !p.settled;
    })), new Promise((u) => {
      r.promise.then(() => {
        d === o && u();
      });
    }));
  }
  const k = {
    set: C,
    update: (q, F) => C(q(_, l), F),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: f
  };
  return k;
}
const {
  SvelteComponent: Vn,
  append: U,
  attr: S,
  component_subscribe: _t,
  detach: In,
  element: Pn,
  init: Tn,
  insert: jn,
  noop: ut,
  safe_not_equal: Zn,
  set_style: Se,
  svg_element: G,
  toggle_class: ct
} = window.__gradio__svelte__internal, { onMount: An } = window.__gradio__svelte__internal;
function Bn(l) {
  let e, t, n, i, f, s, r, o, a, _, c, w;
  return {
    c() {
      e = Pn("div"), t = G("svg"), n = G("g"), i = G("path"), f = G("path"), s = G("path"), r = G("path"), o = G("g"), a = G("path"), _ = G("path"), c = G("path"), w = G("path"), S(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), S(i, "fill", "#FF7C00"), S(i, "fill-opacity", "0.4"), S(i, "class", "svelte-43sxxs"), S(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), S(f, "fill", "#FF7C00"), S(f, "class", "svelte-43sxxs"), S(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), S(s, "fill", "#FF7C00"), S(s, "fill-opacity", "0.4"), S(s, "class", "svelte-43sxxs"), S(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), S(r, "fill", "#FF7C00"), S(r, "class", "svelte-43sxxs"), Se(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), S(a, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), S(a, "fill", "#FF7C00"), S(a, "fill-opacity", "0.4"), S(a, "class", "svelte-43sxxs"), S(_, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), S(_, "fill", "#FF7C00"), S(_, "class", "svelte-43sxxs"), S(c, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), S(c, "fill", "#FF7C00"), S(c, "fill-opacity", "0.4"), S(c, "class", "svelte-43sxxs"), S(w, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), S(w, "fill", "#FF7C00"), S(w, "class", "svelte-43sxxs"), Se(o, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), S(t, "viewBox", "-1200 -1200 3000 3000"), S(t, "fill", "none"), S(t, "xmlns", "http://www.w3.org/2000/svg"), S(t, "class", "svelte-43sxxs"), S(e, "class", "svelte-43sxxs"), ct(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(h, C) {
      jn(h, e, C), U(e, t), U(t, n), U(n, i), U(n, f), U(n, s), U(n, r), U(t, o), U(o, a), U(o, _), U(o, c), U(o, w);
    },
    p(h, [C]) {
      C & /*$top*/
      2 && Se(n, "transform", "translate(" + /*$top*/
      h[1][0] + "px, " + /*$top*/
      h[1][1] + "px)"), C & /*$bottom*/
      4 && Se(o, "transform", "translate(" + /*$bottom*/
      h[2][0] + "px, " + /*$bottom*/
      h[2][1] + "px)"), C & /*margin*/
      1 && ct(
        e,
        "margin",
        /*margin*/
        h[0]
      );
    },
    i: ut,
    o: ut,
    d(h) {
      h && In(e);
    }
  };
}
function En(l, e, t) {
  let n, i;
  var f = this && this.__awaiter || function(h, C, k, q) {
    function F(d) {
      return d instanceof k ? d : new k(function(u) {
        u(d);
      });
    }
    return new (k || (k = Promise))(function(d, u) {
      function p(z) {
        try {
          m(q.next(z));
        } catch (L) {
          u(L);
        }
      }
      function b(z) {
        try {
          m(q.throw(z));
        } catch (L) {
          u(L);
        }
      }
      function m(z) {
        z.done ? d(z.value) : F(z.value).then(p, b);
      }
      m((q = q.apply(h, C || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const r = rt([0, 0]);
  _t(l, r, (h) => t(1, n = h));
  const o = rt([0, 0]);
  _t(l, o, (h) => t(2, i = h));
  let a;
  function _() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), o.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), o.set([125, -140])]), yield Promise.all([r.set([-125, 0]), o.set([125, -0])]), yield Promise.all([r.set([125, 0]), o.set([-125, 0])]);
    });
  }
  function c() {
    return f(this, void 0, void 0, function* () {
      yield _(), a || c();
    });
  }
  function w() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), o.set([-125, 0])]), c();
    });
  }
  return An(() => (w(), () => a = !0)), l.$$set = (h) => {
    "margin" in h && t(0, s = h.margin);
  }, [s, n, i, r, o];
}
class Dn extends Vn {
  constructor(e) {
    super(), Tn(this, e, En, Bn, Zn, { margin: 0 });
  }
}
const {
  SvelteComponent: Kn,
  append: oe,
  attr: X,
  binding_callbacks: dt,
  check_outros: He,
  create_component: Xt,
  create_slot: Yt,
  destroy_component: Ht,
  destroy_each: Jt,
  detach: v,
  element: Q,
  empty: ge,
  ensure_array_like: Be,
  get_all_dirty_from_scope: Qt,
  get_slot_changes: Wt,
  group_outros: Je,
  init: Rn,
  insert: y,
  mount_component: xt,
  noop: Qe,
  safe_not_equal: Un,
  set_data: E,
  set_style: fe,
  space: B,
  text: N,
  toggle_class: A,
  transition_in: O,
  transition_out: W,
  update_slot_base: $t
} = window.__gradio__svelte__internal, { tick: Gn } = window.__gradio__svelte__internal, { onDestroy: On } = window.__gradio__svelte__internal, { createEventDispatcher: Xn } = window.__gradio__svelte__internal, Yn = (l) => ({}), mt = (l) => ({}), Hn = (l) => ({}), bt = (l) => ({});
function ht(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function gt(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Jn(l) {
  let e, t, n, i, f = (
    /*i18n*/
    l[1]("common.error") + ""
  ), s, r, o;
  t = new wn({
    props: {
      Icon: Fn,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const a = (
    /*#slots*/
    l[30].error
  ), _ = Yt(
    a,
    l,
    /*$$scope*/
    l[29],
    mt
  );
  return {
    c() {
      e = Q("div"), Xt(t.$$.fragment), n = B(), i = Q("span"), s = N(f), r = B(), _ && _.c(), X(e, "class", "clear-status svelte-16nch4a"), X(i, "class", "error svelte-16nch4a");
    },
    m(c, w) {
      y(c, e, w), xt(t, e, null), y(c, n, w), y(c, i, w), oe(i, s), y(c, r, w), _ && _.m(c, w), o = !0;
    },
    p(c, w) {
      const h = {};
      w[0] & /*i18n*/
      2 && (h.label = /*i18n*/
      c[1]("common.clear")), t.$set(h), (!o || w[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      c[1]("common.error") + "") && E(s, f), _ && _.p && (!o || w[0] & /*$$scope*/
      536870912) && $t(
        _,
        a,
        c,
        /*$$scope*/
        c[29],
        o ? Wt(
          a,
          /*$$scope*/
          c[29],
          w,
          Yn
        ) : Qt(
          /*$$scope*/
          c[29]
        ),
        mt
      );
    },
    i(c) {
      o || (O(t.$$.fragment, c), O(_, c), o = !0);
    },
    o(c) {
      W(t.$$.fragment, c), W(_, c), o = !1;
    },
    d(c) {
      c && (v(e), v(n), v(i), v(r)), Ht(t), _ && _.d(c);
    }
  };
}
function Qn(l) {
  let e, t, n, i, f, s, r, o, a, _ = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && pt(l)
  );
  function c(u, p) {
    if (
      /*progress*/
      u[7]
    ) return $n;
    if (
      /*queue_position*/
      u[2] !== null && /*queue_size*/
      u[3] !== void 0 && /*queue_position*/
      u[2] >= 0
    ) return xn;
    if (
      /*queue_position*/
      u[2] === 0
    ) return Wn;
  }
  let w = c(l), h = w && w(l), C = (
    /*timer*/
    l[5] && vt(l)
  );
  const k = [ni, li], q = [];
  function F(u, p) {
    return (
      /*last_progress_level*/
      u[15] != null ? 0 : (
        /*show_progress*/
        u[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = F(l)) && (s = q[f] = k[f](l));
  let d = !/*timer*/
  l[5] && St(l);
  return {
    c() {
      _ && _.c(), e = B(), t = Q("div"), h && h.c(), n = B(), C && C.c(), i = B(), s && s.c(), r = B(), d && d.c(), o = ge(), X(t, "class", "progress-text svelte-16nch4a"), A(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), A(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(u, p) {
      _ && _.m(u, p), y(u, e, p), y(u, t, p), h && h.m(t, null), oe(t, n), C && C.m(t, null), y(u, i, p), ~f && q[f].m(u, p), y(u, r, p), d && d.m(u, p), y(u, o, p), a = !0;
    },
    p(u, p) {
      /*variant*/
      u[8] === "default" && /*show_eta_bar*/
      u[18] && /*show_progress*/
      u[6] === "full" ? _ ? _.p(u, p) : (_ = pt(u), _.c(), _.m(e.parentNode, e)) : _ && (_.d(1), _ = null), w === (w = c(u)) && h ? h.p(u, p) : (h && h.d(1), h = w && w(u), h && (h.c(), h.m(t, n))), /*timer*/
      u[5] ? C ? C.p(u, p) : (C = vt(u), C.c(), C.m(t, null)) : C && (C.d(1), C = null), (!a || p[0] & /*variant*/
      256) && A(
        t,
        "meta-text-center",
        /*variant*/
        u[8] === "center"
      ), (!a || p[0] & /*variant*/
      256) && A(
        t,
        "meta-text",
        /*variant*/
        u[8] === "default"
      );
      let b = f;
      f = F(u), f === b ? ~f && q[f].p(u, p) : (s && (Je(), W(q[b], 1, 1, () => {
        q[b] = null;
      }), He()), ~f ? (s = q[f], s ? s.p(u, p) : (s = q[f] = k[f](u), s.c()), O(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      u[5] ? d && (Je(), W(d, 1, 1, () => {
        d = null;
      }), He()) : d ? (d.p(u, p), p[0] & /*timer*/
      32 && O(d, 1)) : (d = St(u), d.c(), O(d, 1), d.m(o.parentNode, o));
    },
    i(u) {
      a || (O(s), O(d), a = !0);
    },
    o(u) {
      W(s), W(d), a = !1;
    },
    d(u) {
      u && (v(e), v(t), v(i), v(r), v(o)), _ && _.d(u), h && h.d(), C && C.d(), ~f && q[f].d(u), d && d.d(u);
    }
  };
}
function pt(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Q("div"), X(e, "class", "eta-bar svelte-16nch4a"), fe(e, "transform", t);
    },
    m(n, i) {
      y(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && fe(e, "transform", t);
    },
    d(n) {
      n && v(e);
    }
  };
}
function Wn(l) {
  let e;
  return {
    c() {
      e = N("processing |");
    },
    m(t, n) {
      y(t, e, n);
    },
    p: Qe,
    d(t) {
      t && v(e);
    }
  };
}
function xn(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, f, s;
  return {
    c() {
      e = N("queue: "), n = N(t), i = N("/"), f = N(
        /*queue_size*/
        l[3]
      ), s = N(" |");
    },
    m(r, o) {
      y(r, e, o), y(r, n, o), y(r, i, o), y(r, f, o), y(r, s, o);
    },
    p(r, o) {
      o[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && E(n, t), o[0] & /*queue_size*/
      8 && E(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (v(e), v(n), v(i), v(f), v(s));
    }
  };
}
function $n(l) {
  let e, t = Be(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = kt(gt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ge();
    },
    m(i, f) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        t = Be(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = gt(i, t, s);
          n[s] ? n[s].p(r, f) : (n[s] = kt(r), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && v(e), Jt(n, i);
    }
  };
}
function wt(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, f = " ", s;
  function r(_, c) {
    return (
      /*p*/
      _[41].length != null ? ti : ei
    );
  }
  let o = r(l), a = o(l);
  return {
    c() {
      a.c(), e = B(), n = N(t), i = N(" | "), s = N(f);
    },
    m(_, c) {
      a.m(_, c), y(_, e, c), y(_, n, c), y(_, i, c), y(_, s, c);
    },
    p(_, c) {
      o === (o = r(_)) && a ? a.p(_, c) : (a.d(1), a = o(_), a && (a.c(), a.m(e.parentNode, e))), c[0] & /*progress*/
      128 && t !== (t = /*p*/
      _[41].unit + "") && E(n, t);
    },
    d(_) {
      _ && (v(e), v(n), v(i), v(s)), a.d(_);
    }
  };
}
function ei(l) {
  let e = ce(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = N(e);
    },
    m(n, i) {
      y(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = ce(
        /*p*/
        n[41].index || 0
      ) + "") && E(t, e);
    },
    d(n) {
      n && v(t);
    }
  };
}
function ti(l) {
  let e = ce(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = ce(
    /*p*/
    l[41].length
  ) + "", f;
  return {
    c() {
      t = N(e), n = N("/"), f = N(i);
    },
    m(s, r) {
      y(s, t, r), y(s, n, r), y(s, f, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && e !== (e = ce(
        /*p*/
        s[41].index || 0
      ) + "") && E(t, e), r[0] & /*progress*/
      128 && i !== (i = ce(
        /*p*/
        s[41].length
      ) + "") && E(f, i);
    },
    d(s) {
      s && (v(t), v(n), v(f));
    }
  };
}
function kt(l) {
  let e, t = (
    /*p*/
    l[41].index != null && wt(l)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(n, i) {
      t && t.m(n, i), y(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = wt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && v(e), t && t.d(n);
    }
  };
}
function vt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = N(
        /*formatted_timer*/
        l[20]
      ), n = N(t), i = N("s");
    },
    m(f, s) {
      y(f, e, s), y(f, n, s), y(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && E(
        e,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && E(n, t);
    },
    d(f) {
      f && (v(e), v(n), v(i));
    }
  };
}
function li(l) {
  let e, t;
  return e = new Dn({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Xt(e.$$.fragment);
    },
    m(n, i) {
      xt(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      n[8] === "default"), e.$set(f);
    },
    i(n) {
      t || (O(e.$$.fragment, n), t = !0);
    },
    o(n) {
      W(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ht(e, n);
    }
  };
}
function ni(l) {
  let e, t, n, i, f, s = `${/*last_progress_level*/
  l[15] * 100}%`, r = (
    /*progress*/
    l[7] != null && yt(l)
  );
  return {
    c() {
      e = Q("div"), t = Q("div"), r && r.c(), n = B(), i = Q("div"), f = Q("div"), X(t, "class", "progress-level-inner svelte-16nch4a"), X(f, "class", "progress-bar svelte-16nch4a"), fe(f, "width", s), X(i, "class", "progress-bar-wrap svelte-16nch4a"), X(e, "class", "progress-level svelte-16nch4a");
    },
    m(o, a) {
      y(o, e, a), oe(e, t), r && r.m(t, null), oe(e, n), oe(e, i), oe(i, f), l[31](f);
    },
    p(o, a) {
      /*progress*/
      o[7] != null ? r ? r.p(o, a) : (r = yt(o), r.c(), r.m(t, null)) : r && (r.d(1), r = null), a[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      o[15] * 100}%`) && fe(f, "width", s);
    },
    i: Qe,
    o: Qe,
    d(o) {
      o && v(e), r && r.d(), l[31](null);
    }
  };
}
function yt(l) {
  let e, t = Be(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Lt(ht(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ge();
    },
    m(i, f) {
      for (let s = 0; s < n.length; s += 1)
        n[s] && n[s].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        t = Be(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const r = ht(i, t, s);
          n[s] ? n[s].p(r, f) : (n[s] = Lt(r), n[s].c(), n[s].m(e.parentNode, e));
        }
        for (; s < n.length; s += 1)
          n[s].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && v(e), Jt(n, i);
    }
  };
}
function qt(l) {
  let e, t, n, i, f = (
    /*i*/
    l[43] !== 0 && ii()
  ), s = (
    /*p*/
    l[41].desc != null && Ct(l)
  ), r = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && Mt()
  ), o = (
    /*progress_level*/
    l[14] != null && Ft(l)
  );
  return {
    c() {
      f && f.c(), e = B(), s && s.c(), t = B(), r && r.c(), n = B(), o && o.c(), i = ge();
    },
    m(a, _) {
      f && f.m(a, _), y(a, e, _), s && s.m(a, _), y(a, t, _), r && r.m(a, _), y(a, n, _), o && o.m(a, _), y(a, i, _);
    },
    p(a, _) {
      /*p*/
      a[41].desc != null ? s ? s.p(a, _) : (s = Ct(a), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      a[41].desc != null && /*progress_level*/
      a[14] && /*progress_level*/
      a[14][
        /*i*/
        a[43]
      ] != null ? r || (r = Mt(), r.c(), r.m(n.parentNode, n)) : r && (r.d(1), r = null), /*progress_level*/
      a[14] != null ? o ? o.p(a, _) : (o = Ft(a), o.c(), o.m(i.parentNode, i)) : o && (o.d(1), o = null);
    },
    d(a) {
      a && (v(e), v(t), v(n), v(i)), f && f.d(a), s && s.d(a), r && r.d(a), o && o.d(a);
    }
  };
}
function ii(l) {
  let e;
  return {
    c() {
      e = N(" /");
    },
    m(t, n) {
      y(t, e, n);
    },
    d(t) {
      t && v(e);
    }
  };
}
function Ct(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = N(e);
    },
    m(n, i) {
      y(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && E(t, e);
    },
    d(n) {
      n && v(t);
    }
  };
}
function Mt(l) {
  let e;
  return {
    c() {
      e = N("-");
    },
    m(t, n) {
      y(t, e, n);
    },
    d(t) {
      t && v(e);
    }
  };
}
function Ft(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = N(e), n = N("%");
    },
    m(i, f) {
      y(i, t, f), y(i, n, f);
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
      i && (v(t), v(n));
    }
  };
}
function Lt(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && qt(l)
  );
  return {
    c() {
      t && t.c(), e = ge();
    },
    m(n, i) {
      t && t.m(n, i), y(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = qt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && v(e), t && t.d(n);
    }
  };
}
function St(l) {
  let e, t, n, i;
  const f = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), s = Yt(
    f,
    l,
    /*$$scope*/
    l[29],
    bt
  );
  return {
    c() {
      e = Q("p"), t = N(
        /*loading_text*/
        l[9]
      ), n = B(), s && s.c(), X(e, "class", "loading svelte-16nch4a");
    },
    m(r, o) {
      y(r, e, o), oe(e, t), y(r, n, o), s && s.m(r, o), i = !0;
    },
    p(r, o) {
      (!i || o[0] & /*loading_text*/
      512) && E(
        t,
        /*loading_text*/
        r[9]
      ), s && s.p && (!i || o[0] & /*$$scope*/
      536870912) && $t(
        s,
        f,
        r,
        /*$$scope*/
        r[29],
        i ? Wt(
          f,
          /*$$scope*/
          r[29],
          o,
          Hn
        ) : Qt(
          /*$$scope*/
          r[29]
        ),
        bt
      );
    },
    i(r) {
      i || (O(s, r), i = !0);
    },
    o(r) {
      W(s, r), i = !1;
    },
    d(r) {
      r && (v(e), v(n)), s && s.d(r);
    }
  };
}
function fi(l) {
  let e, t, n, i, f;
  const s = [Qn, Jn], r = [];
  function o(a, _) {
    return (
      /*status*/
      a[4] === "pending" ? 0 : (
        /*status*/
        a[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = o(l)) && (n = r[t] = s[t](l)), {
    c() {
      e = Q("div"), n && n.c(), X(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-16nch4a"), A(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), A(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), A(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), A(
        e,
        "border",
        /*border*/
        l[12]
      ), fe(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), fe(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(a, _) {
      y(a, e, _), ~t && r[t].m(e, null), l[33](e), f = !0;
    },
    p(a, _) {
      let c = t;
      t = o(a), t === c ? ~t && r[t].p(a, _) : (n && (Je(), W(r[c], 1, 1, () => {
        r[c] = null;
      }), He()), ~t ? (n = r[t], n ? n.p(a, _) : (n = r[t] = s[t](a), n.c()), O(n, 1), n.m(e, null)) : n = null), (!f || _[0] & /*variant, show_progress*/
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
      1024 && fe(
        e,
        "position",
        /*absolute*/
        a[10] ? "absolute" : "static"
      ), _[0] & /*absolute*/
      1024 && fe(
        e,
        "padding",
        /*absolute*/
        a[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(a) {
      f || (O(n), f = !0);
    },
    o(a) {
      W(n), f = !1;
    },
    d(a) {
      a && v(e), ~t && r[t].d(), l[33](null);
    }
  };
}
var si = function(l, e, t, n) {
  function i(f) {
    return f instanceof t ? f : new t(function(s) {
      s(f);
    });
  }
  return new (t || (t = Promise))(function(f, s) {
    function r(_) {
      try {
        a(n.next(_));
      } catch (c) {
        s(c);
      }
    }
    function o(_) {
      try {
        a(n.throw(_));
      } catch (c) {
        s(c);
      }
    }
    function a(_) {
      _.done ? f(_.value) : i(_.value).then(r, o);
    }
    a((n = n.apply(l, e || [])).next());
  });
};
let ze = [], Ge = !1;
function oi(l) {
  return si(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (ze.push(e), !Ge) Ge = !0;
      else return;
      yield Gn(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < ze.length; i++) {
          const s = ze[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= n[0]) && (n[0] = s.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Ge = !1, ze = [];
      });
    }
  });
}
function ai(l, e, t) {
  let n, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const s = Xn();
  let { i18n: r } = e, { eta: o = null } = e, { queue_position: a } = e, { queue_size: _ } = e, { status: c } = e, { scroll_to_output: w = !1 } = e, { timer: h = !0 } = e, { show_progress: C = "full" } = e, { message: k = null } = e, { progress: q = null } = e, { variant: F = "default" } = e, { loading_text: d = "Loading..." } = e, { absolute: u = !0 } = e, { translucent: p = !1 } = e, { border: b = !1 } = e, { autoscroll: m } = e, z, L = !1, P = 0, Y = 0, te = null, le = null, ye = 0, M = null, D, V = null, x = !0;
  const pe = () => {
    t(0, o = t(27, te = t(19, ne = null))), t(25, P = performance.now()), t(26, Y = 0), L = !0, K();
  };
  function K() {
    requestAnimationFrame(() => {
      t(26, Y = (performance.now() - P) / 1e3), L && K();
    });
  }
  function j() {
    t(26, Y = 0), t(0, o = t(27, te = t(19, ne = null))), L && (L = !1);
  }
  On(() => {
    L && j();
  });
  let ne = null;
  function qe(g) {
    dt[g ? "unshift" : "push"](() => {
      V = g, t(16, V), t(7, q), t(14, M), t(15, D);
    });
  }
  const ie = () => {
    s("clear_status");
  };
  function Z(g) {
    dt[g ? "unshift" : "push"](() => {
      z = g, t(13, z);
    });
  }
  return l.$$set = (g) => {
    "i18n" in g && t(1, r = g.i18n), "eta" in g && t(0, o = g.eta), "queue_position" in g && t(2, a = g.queue_position), "queue_size" in g && t(3, _ = g.queue_size), "status" in g && t(4, c = g.status), "scroll_to_output" in g && t(22, w = g.scroll_to_output), "timer" in g && t(5, h = g.timer), "show_progress" in g && t(6, C = g.show_progress), "message" in g && t(23, k = g.message), "progress" in g && t(7, q = g.progress), "variant" in g && t(8, F = g.variant), "loading_text" in g && t(9, d = g.loading_text), "absolute" in g && t(10, u = g.absolute), "translucent" in g && t(11, p = g.translucent), "border" in g && t(12, b = g.border), "autoscroll" in g && t(24, m = g.autoscroll), "$$scope" in g && t(29, f = g.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (o === null && t(0, o = te), o != null && te !== o && (t(28, le = (performance.now() - P) / 1e3 + o), t(19, ne = le.toFixed(1)), t(27, te = o))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, ye = le === null || le <= 0 || !Y ? null : Math.min(Y / le, 1)), l.$$.dirty[0] & /*progress*/
    128 && q != null && t(18, x = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (q != null ? t(14, M = q.map((g) => {
      if (g.index != null && g.length != null)
        return g.index / g.length;
      if (g.progress != null)
        return g.progress;
    })) : t(14, M = null), M ? (t(15, D = M[M.length - 1]), V && (D === 0 ? t(16, V.style.transition = "0", V) : t(16, V.style.transition = "150ms", V))) : t(15, D = void 0)), l.$$.dirty[0] & /*status*/
    16 && (c === "pending" ? pe() : j()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && z && w && (c === "pending" || c === "complete") && oi(z, m), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = Y.toFixed(1));
  }, [
    o,
    r,
    a,
    _,
    c,
    h,
    C,
    q,
    F,
    d,
    u,
    p,
    b,
    z,
    M,
    D,
    V,
    ye,
    x,
    ne,
    n,
    s,
    w,
    k,
    m,
    P,
    Y,
    te,
    le,
    f,
    i,
    qe,
    ie,
    Z
  ];
}
class ri extends Kn {
  constructor(e) {
    super(), Rn(
      this,
      e,
      ai,
      fi,
      Un,
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
  SvelteComponent: _i,
  add_render_callback: zt,
  append: ee,
  assign: ui,
  attr: Ae,
  check_outros: ci,
  create_component: xe,
  destroy_component: $e,
  destroy_each: Nt,
  detach: be,
  element: ae,
  ensure_array_like: Ne,
  get_spread_object: di,
  get_spread_update: mi,
  group_outros: bi,
  init: hi,
  insert: he,
  listen: Vt,
  mount_component: et,
  noop: gi,
  run_all: pi,
  safe_not_equal: wi,
  select_option: Ve,
  select_value: It,
  set_data: tt,
  set_input_value: We,
  space: Ie,
  text: Ee,
  transition_in: de,
  transition_out: ve
} = window.__gradio__svelte__internal, { onMount: ki } = window.__gradio__svelte__internal;
function Pt(l, e, t) {
  const n = l.slice();
  return n[27] = e[t], n;
}
function Tt(l, e, t) {
  const n = l.slice();
  return n[27] = e[t], n;
}
function jt(l) {
  let e, t;
  const n = [
    {
      autoscroll: (
        /*gradio*/
        l[10].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[10].i18n
    ) },
    /*loading_status*/
    l[9]
  ];
  let i = {};
  for (let f = 0; f < n.length; f += 1)
    i = ui(i, n[f]);
  return e = new ri({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[19]
  ), {
    c() {
      xe(e.$$.fragment);
    },
    m(f, s) {
      et(e, f, s), t = !0;
    },
    p(f, s) {
      const r = s[0] & /*gradio, loading_status*/
      1536 ? mi(n, [
        s[0] & /*gradio*/
        1024 && {
          autoscroll: (
            /*gradio*/
            f[10].autoscroll
          )
        },
        s[0] & /*gradio*/
        1024 && { i18n: (
          /*gradio*/
          f[10].i18n
        ) },
        s[0] & /*loading_status*/
        512 && di(
          /*loading_status*/
          f[9]
        )
      ]) : {};
      e.$set(r);
    },
    i(f) {
      t || (de(e.$$.fragment, f), t = !0);
    },
    o(f) {
      ve(e.$$.fragment, f), t = !1;
    },
    d(f) {
      $e(e, f);
    }
  };
}
function vi(l) {
  let e;
  return {
    c() {
      e = Ee(
        /*label*/
        l[2]
      );
    },
    m(t, n) {
      he(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      4 && tt(
        e,
        /*label*/
        t[2]
      );
    },
    d(t) {
      t && be(e);
    }
  };
}
function Zt(l) {
  let e, t = (
    /*item*/
    l[27] + ""
  ), n;
  return {
    c() {
      e = ae("option"), n = Ee(t), e.__value = /*item*/
      l[27], We(e, e.__value);
    },
    m(i, f) {
      he(i, e, f), ee(e, n);
    },
    p: gi,
    d(i) {
      i && be(e);
    }
  };
}
function At(l) {
  let e, t = (
    /*item*/
    l[27][0] + ""
  ), n, i;
  return {
    c() {
      e = ae("option"), n = Ee(t), e.__value = i = /*item*/
      l[27][1], We(e, e.__value);
    },
    m(f, s) {
      he(f, e, s), ee(e, n);
    },
    p(f, s) {
      s[0] & /*machineList*/
      8192 && t !== (t = /*item*/
      f[27][0] + "") && tt(n, t), s[0] & /*machineList*/
      8192 && i !== (i = /*item*/
      f[27][1]) && (e.__value = i, We(e, e.__value));
    },
    d(f) {
      f && be(e);
    }
  };
}
function Bt(l) {
  let e, t;
  return {
    c() {
      e = ae("div"), t = Ee(
        /*errMsg*/
        l[12]
      ), Ae(e, "class", "dp_machine--error svelte-1qtc7pq");
    },
    m(n, i) {
      he(n, e, i), ee(e, t);
    },
    p(n, i) {
      i[0] & /*errMsg*/
      4096 && tt(
        t,
        /*errMsg*/
        n[12]
      );
    },
    d(n) {
      n && be(e);
    }
  };
}
function yi(l) {
  let e, t, n, i, f, s, r, o, a, _, c, w, h, C, k = (
    /*loading_status*/
    l[9] && jt(l)
  );
  n = new ln({
    props: {
      show_label: (
        /*show_label*/
        l[6]
      ),
      info: void 0,
      $$slots: { default: [vi] },
      $$scope: { ctx: l }
    }
  });
  let q = Ne(
    /*machineTypeOptions*/
    l[15]
  ), F = [];
  for (let b = 0; b < q.length; b += 1)
    F[b] = Zt(Tt(l, q, b));
  let d = Ne(
    /*machineList*/
    l[13]
  ), u = [];
  for (let b = 0; b < d.length; b += 1)
    u[b] = At(Pt(l, d, b));
  let p = (
    /*isError*/
    l[14] && Bt(l)
  );
  return {
    c() {
      k && k.c(), e = Ie(), t = ae("label"), xe(n.$$.fragment), i = Ie(), f = ae("select");
      for (let b = 0; b < F.length; b += 1)
        F[b].c();
      r = Ie(), o = ae("div"), a = ae("select");
      for (let b = 0; b < u.length; b += 1)
        u[b].c();
      c = Ie(), p && p.c(), Ae(f, "class", "dp_machine-type svelte-1qtc7pq"), f.disabled = s = !/*interactive*/
      l[11], /*machineType*/
      l[1] === void 0 && zt(() => (
        /*select0_change_handler*/
        l[20].call(f)
      )), Ae(a, "class", "dp_machine-sku svelte-1qtc7pq"), a.disabled = _ = !/*interactive*/
      l[11], /*value*/
      l[0] === void 0 && zt(() => (
        /*select1_change_handler*/
        l[21].call(a)
      )), Ae(o, "class", "dp_machine-container svelte-1qtc7pq");
    },
    m(b, m) {
      k && k.m(b, m), he(b, e, m), he(b, t, m), et(n, t, null), ee(t, i), ee(t, f);
      for (let z = 0; z < F.length; z += 1)
        F[z] && F[z].m(f, null);
      Ve(
        f,
        /*machineType*/
        l[1],
        !0
      ), ee(t, r), ee(t, o), ee(o, a);
      for (let z = 0; z < u.length; z += 1)
        u[z] && u[z].m(a, null);
      Ve(
        a,
        /*value*/
        l[0],
        !0
      ), ee(o, c), p && p.m(o, null), w = !0, h || (C = [
        Vt(
          f,
          "change",
          /*select0_change_handler*/
          l[20]
        ),
        Vt(
          a,
          "change",
          /*select1_change_handler*/
          l[21]
        )
      ], h = !0);
    },
    p(b, m) {
      /*loading_status*/
      b[9] ? k ? (k.p(b, m), m[0] & /*loading_status*/
      512 && de(k, 1)) : (k = jt(b), k.c(), de(k, 1), k.m(e.parentNode, e)) : k && (bi(), ve(k, 1, 1, () => {
        k = null;
      }), ci());
      const z = {};
      if (m[0] & /*show_label*/
      64 && (z.show_label = /*show_label*/
      b[6]), m[0] & /*label*/
      4 | m[1] & /*$$scope*/
      2 && (z.$$scope = { dirty: m, ctx: b }), n.$set(z), m[0] & /*machineTypeOptions*/
      32768) {
        q = Ne(
          /*machineTypeOptions*/
          b[15]
        );
        let L;
        for (L = 0; L < q.length; L += 1) {
          const P = Tt(b, q, L);
          F[L] ? F[L].p(P, m) : (F[L] = Zt(P), F[L].c(), F[L].m(f, null));
        }
        for (; L < F.length; L += 1)
          F[L].d(1);
        F.length = q.length;
      }
      if ((!w || m[0] & /*interactive*/
      2048 && s !== (s = !/*interactive*/
      b[11])) && (f.disabled = s), m[0] & /*machineType, machineTypeOptions*/
      32770 && Ve(
        f,
        /*machineType*/
        b[1]
      ), m[0] & /*machineList*/
      8192) {
        d = Ne(
          /*machineList*/
          b[13]
        );
        let L;
        for (L = 0; L < d.length; L += 1) {
          const P = Pt(b, d, L);
          u[L] ? u[L].p(P, m) : (u[L] = At(P), u[L].c(), u[L].m(a, null));
        }
        for (; L < u.length; L += 1)
          u[L].d(1);
        u.length = d.length;
      }
      (!w || m[0] & /*interactive*/
      2048 && _ !== (_ = !/*interactive*/
      b[11])) && (a.disabled = _), m[0] & /*value, machineList*/
      8193 && Ve(
        a,
        /*value*/
        b[0]
      ), /*isError*/
      b[14] ? p ? p.p(b, m) : (p = Bt(b), p.c(), p.m(o, null)) : p && (p.d(1), p = null);
    },
    i(b) {
      w || (de(k), de(n.$$.fragment, b), w = !0);
    },
    o(b) {
      ve(k), ve(n.$$.fragment, b), w = !1;
    },
    d(b) {
      b && (be(e), be(t)), k && k.d(b), $e(n), Nt(F, b), Nt(u, b), p && p.d(), h = !1, pi(C);
    }
  };
}
function qi(l) {
  let e, t;
  return e = new wl({
    props: {
      visible: (
        /*visible*/
        l[5]
      ),
      elem_id: (
        /*elem_id*/
        l[3]
      ),
      elem_classes: (
        /*elem_classes*/
        l[4]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        l[7]
      ),
      min_width: (
        /*min_width*/
        l[8]
      ),
      $$slots: { default: [yi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      xe(e.$$.fragment);
    },
    m(n, i) {
      et(e, n, i), t = !0;
    },
    p(n, i) {
      const f = {};
      i[0] & /*visible*/
      32 && (f.visible = /*visible*/
      n[5]), i[0] & /*elem_id*/
      8 && (f.elem_id = /*elem_id*/
      n[3]), i[0] & /*elem_classes*/
      16 && (f.elem_classes = /*elem_classes*/
      n[4]), i[0] & /*scale*/
      128 && (f.scale = /*scale*/
      n[7]), i[0] & /*min_width*/
      256 && (f.min_width = /*min_width*/
      n[8]), i[0] & /*errMsg, isError, interactive, value, machineList, machineType, show_label, label, gradio, loading_status*/
      32327 | i[1] & /*$$scope*/
      2 && (f.$$scope = { dirty: i, ctx: n }), e.$set(f);
    },
    i(n) {
      t || (de(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ve(e.$$.fragment, n), t = !1;
    },
    d(n) {
      $e(e, n);
    }
  };
}
function Ci(l, e, t) {
  var n = this && this.__awaiter || function(M, D, V, x) {
    function pe(K) {
      return K instanceof V ? K : new V(function(j) {
        j(K);
      });
    }
    return new (V || (V = Promise))(function(K, j) {
      function ne(Z) {
        try {
          ie(x.next(Z));
        } catch (g) {
          j(g);
        }
      }
      function qe(Z) {
        try {
          ie(x.throw(Z));
        } catch (g) {
          j(g);
        }
      }
      function ie(Z) {
        Z.done ? K(Z.value) : pe(Z.value).then(ne, qe);
      }
      ie((x = x.apply(M, D || [])).next());
    });
  };
  let { label: i = "machine" } = e, { elem_id: f = "" } = e, { elem_classes: s = [] } = e, { visible: r = !0 } = e, { value: o } = e, { show_label: a } = e, { scale: _ = null } = e, { min_width: c = void 0 } = e, { loading_status: w } = e, { gradio: h } = e, { interactive: C } = e, { machineType: k } = e, q = ["CPU", "GPU"], F = /* @__PURE__ */ new Map();
  function d() {
    document.cookie.split(";").forEach((M) => {
      const [D, V] = M.trim().split("=");
      F.set(D, V);
    });
  }
  let u = [], p = [], b = [];
  function m() {
    return n(this, void 0, void 0, function* () {
      const M = F.get("appAccessKey"), D = F.get("clientName"), V = (j) => fetch(`https://openapi.test.dp.tech/openapi/v1/open/sku/list?chooseType=${j}`, {
        headers: { accessKey: M, "x-app-key": D }
      }), [x, pe] = yield Promise.all([V("cpu"), V("gpu")]), K = (j, ne) => n(this, void 0, void 0, function* () {
        if (j.ok) {
          const ie = (yield j.json()).data.items.map((Z) => [Z.skuName, Z.skuId]);
          ne ? t(17, u = ie) : t(18, p = ie);
        }
      });
      K(x, !0), K(pe, !1);
    });
  }
  ki(() => {
    d(), m();
  });
  let z = !1, { errMsg: L = "Please select a machine" } = e;
  function P() {
    return t(14, z = !o), z;
  }
  function Y() {
    h.dispatch("change");
  }
  const te = () => h.dispatch("clear_status", w);
  function le() {
    k = It(this), t(1, k), t(15, q);
  }
  function ye() {
    o = It(this), t(0, o), t(1, k), t(13, b), t(1, k), t(17, u), t(18, p);
  }
  return l.$$set = (M) => {
    "label" in M && t(2, i = M.label), "elem_id" in M && t(3, f = M.elem_id), "elem_classes" in M && t(4, s = M.elem_classes), "visible" in M && t(5, r = M.visible), "value" in M && t(0, o = M.value), "show_label" in M && t(6, a = M.show_label), "scale" in M && t(7, _ = M.scale), "min_width" in M && t(8, c = M.min_width), "loading_status" in M && t(9, w = M.loading_status), "gradio" in M && t(10, h = M.gradio), "interactive" in M && t(11, C = M.interactive), "machineType" in M && t(1, k = M.machineType), "errMsg" in M && t(12, L = M.errMsg);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*machineType, cpuList, gpuList*/
    393218 && (k === "CPU" ? t(13, b = u) : t(13, b = p)), l.$$.dirty[0] & /*machineType*/
    2 && (t(0, o = void 0), Y()), l.$$.dirty[0] & /*value*/
    1 && (P(), Y());
  }, [
    o,
    k,
    i,
    f,
    s,
    r,
    a,
    _,
    c,
    w,
    h,
    C,
    L,
    b,
    z,
    q,
    P,
    u,
    p,
    te,
    le,
    ye
  ];
}
class Mi extends _i {
  constructor(e) {
    super(), hi(
      this,
      e,
      Ci,
      qi,
      wi,
      {
        label: 2,
        elem_id: 3,
        elem_classes: 4,
        visible: 5,
        value: 0,
        show_label: 6,
        scale: 7,
        min_width: 8,
        loading_status: 9,
        gradio: 10,
        interactive: 11,
        machineType: 1,
        errMsg: 12,
        validate: 16
      },
      null,
      [-1, -1]
    );
  }
  get validate() {
    return this.$$.ctx[16];
  }
}
export {
  Mi as default
};
