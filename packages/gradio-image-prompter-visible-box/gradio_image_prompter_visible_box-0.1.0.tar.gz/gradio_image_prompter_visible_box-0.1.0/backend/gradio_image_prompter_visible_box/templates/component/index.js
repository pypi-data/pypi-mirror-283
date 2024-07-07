const Wi = [
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
], Jn = {
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
Wi.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Jn[e][t],
      secondary: Jn[e][l]
    }
  }),
  {}
);
class Rt extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
async function Vi(n, e) {
  if (window.__gradio_space__ == null)
    throw new Rt("Must be on Spaces to share.");
  let t, l, i;
  t = Gi(n), l = n.split(";")[0].split(":")[1], i = "file" + l.split("/")[1];
  const o = new File([t], i, { type: l }), s = await fetch("https://huggingface.co/uploads", {
    method: "POST",
    body: o,
    headers: {
      "Content-Type": o.type,
      "X-Requested-With": "XMLHttpRequest"
    }
  });
  if (!s.ok) {
    if (s.headers.get("content-type")?.includes("application/json")) {
      const r = await s.json();
      throw new Rt(`Upload failed: ${r.error}`);
    }
    throw new Rt("Upload failed.");
  }
  return await s.text();
}
function Gi(n) {
  for (var e = n.split(","), t = e[0].match(/:(.*?);/)[1], l = atob(e[1]), i = l.length, o = new Uint8Array(i); i--; )
    o[i] = l.charCodeAt(i);
  return new Blob([o], { type: t });
}
const {
  SvelteComponent: Hi,
  assign: Ji,
  create_slot: Xi,
  detach: Yi,
  element: Ki,
  get_all_dirty_from_scope: Qi,
  get_slot_changes: $i,
  get_spread_update: xi,
  init: eo,
  insert: to,
  safe_not_equal: no,
  set_dynamic_element_data: Xn,
  set_style: fe,
  toggle_class: Re,
  transition_in: ci,
  transition_out: _i,
  update_slot_base: lo
} = window.__gradio__svelte__internal;
function io(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[17].default
  ), o = Xi(
    i,
    n,
    /*$$scope*/
    n[16],
    null
  );
  let s = [
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
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], a = {};
  for (let r = 0; r < s.length; r += 1)
    a = Ji(a, s[r]);
  return {
    c() {
      e = Ki(
        /*tag*/
        n[14]
      ), o && o.c(), Xn(
        /*tag*/
        n[14]
      )(e, a), Re(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), Re(
        e,
        "padded",
        /*padding*/
        n[6]
      ), Re(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), Re(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), fe(e, "height", typeof /*height*/
      n[0] == "number" ? (
        /*height*/
        n[0] + "px"
      ) : void 0), fe(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : void 0), fe(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), fe(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), fe(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), fe(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), fe(e, "border-width", "var(--block-border-width)");
    },
    m(r, u) {
      to(r, e, u), o && o.m(e, null), l = !0;
    },
    p(r, u) {
      o && o.p && (!l || u & /*$$scope*/
      65536) && lo(
        o,
        i,
        r,
        /*$$scope*/
        r[16],
        l ? $i(
          i,
          /*$$scope*/
          r[16],
          u,
          null
        ) : Qi(
          /*$$scope*/
          r[16]
        ),
        null
      ), Xn(
        /*tag*/
        r[14]
      )(e, a = xi(s, [
        (!l || u & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          r[7]
        ) },
        (!l || u & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          r[2]
        ) },
        (!l || u & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        r[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), Re(
        e,
        "hidden",
        /*visible*/
        r[10] === !1
      ), Re(
        e,
        "padded",
        /*padding*/
        r[6]
      ), Re(
        e,
        "border_focus",
        /*border_mode*/
        r[5] === "focus"
      ), Re(e, "hide-container", !/*explicit_call*/
      r[8] && !/*container*/
      r[9]), u & /*height*/
      1 && fe(e, "height", typeof /*height*/
      r[0] == "number" ? (
        /*height*/
        r[0] + "px"
      ) : void 0), u & /*width*/
      2 && fe(e, "width", typeof /*width*/
      r[1] == "number" ? `calc(min(${/*width*/
      r[1]}px, 100%))` : void 0), u & /*variant*/
      16 && fe(
        e,
        "border-style",
        /*variant*/
        r[4]
      ), u & /*allow_overflow*/
      2048 && fe(
        e,
        "overflow",
        /*allow_overflow*/
        r[11] ? "visible" : "hidden"
      ), u & /*scale*/
      4096 && fe(
        e,
        "flex-grow",
        /*scale*/
        r[12]
      ), u & /*min_width*/
      8192 && fe(e, "min-width", `calc(min(${/*min_width*/
      r[13]}px, 100%))`);
    },
    i(r) {
      l || (ci(o, r), l = !0);
    },
    o(r) {
      _i(o, r), l = !1;
    },
    d(r) {
      r && Yi(e), o && o.d(r);
    }
  };
}
function oo(n) {
  let e, t = (
    /*tag*/
    n[14] && io(n)
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
      e || (ci(t, l), e = !0);
    },
    o(l) {
      _i(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function so(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: s = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: r = [] } = e, { variant: u = "solid" } = e, { border_mode: f = "base" } = e, { padding: _ = !0 } = e, { type: d = "normal" } = e, { test_id: c = void 0 } = e, { explicit_call: m = !1 } = e, { container: p = !0 } = e, { visible: C = !0 } = e, { allow_overflow: b = !0 } = e, { scale: q = null } = e, { min_width: g = 0 } = e, w = d === "fieldset" ? "fieldset" : "div";
  return n.$$set = (E) => {
    "height" in E && t(0, o = E.height), "width" in E && t(1, s = E.width), "elem_id" in E && t(2, a = E.elem_id), "elem_classes" in E && t(3, r = E.elem_classes), "variant" in E && t(4, u = E.variant), "border_mode" in E && t(5, f = E.border_mode), "padding" in E && t(6, _ = E.padding), "type" in E && t(15, d = E.type), "test_id" in E && t(7, c = E.test_id), "explicit_call" in E && t(8, m = E.explicit_call), "container" in E && t(9, p = E.container), "visible" in E && t(10, C = E.visible), "allow_overflow" in E && t(11, b = E.allow_overflow), "scale" in E && t(12, q = E.scale), "min_width" in E && t(13, g = E.min_width), "$$scope" in E && t(16, i = E.$$scope);
  }, [
    o,
    s,
    a,
    r,
    u,
    f,
    _,
    c,
    m,
    p,
    C,
    b,
    q,
    g,
    w,
    d,
    i,
    l
  ];
}
class di extends Hi {
  constructor(e) {
    super(), eo(this, e, so, oo, no, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 15,
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
  SvelteComponent: ro,
  append: xt,
  attr: Nt,
  create_component: ao,
  destroy_component: uo,
  detach: fo,
  element: Yn,
  init: co,
  insert: _o,
  mount_component: ho,
  safe_not_equal: mo,
  set_data: go,
  space: po,
  text: bo,
  toggle_class: Ue,
  transition_in: wo,
  transition_out: vo
} = window.__gradio__svelte__internal;
function ko(n) {
  let e, t, l, i, o, s;
  return l = new /*Icon*/
  n[1]({}), {
    c() {
      e = Yn("label"), t = Yn("span"), ao(l.$$.fragment), i = po(), o = bo(
        /*label*/
        n[0]
      ), Nt(t, "class", "svelte-9gxdi0"), Nt(e, "for", ""), Nt(e, "data-testid", "block-label"), Nt(e, "class", "svelte-9gxdi0"), Ue(e, "hide", !/*show_label*/
      n[2]), Ue(e, "sr-only", !/*show_label*/
      n[2]), Ue(
        e,
        "float",
        /*float*/
        n[4]
      ), Ue(
        e,
        "hide-label",
        /*disable*/
        n[3]
      );
    },
    m(a, r) {
      _o(a, e, r), xt(e, t), ho(l, t, null), xt(e, i), xt(e, o), s = !0;
    },
    p(a, [r]) {
      (!s || r & /*label*/
      1) && go(
        o,
        /*label*/
        a[0]
      ), (!s || r & /*show_label*/
      4) && Ue(e, "hide", !/*show_label*/
      a[2]), (!s || r & /*show_label*/
      4) && Ue(e, "sr-only", !/*show_label*/
      a[2]), (!s || r & /*float*/
      16) && Ue(
        e,
        "float",
        /*float*/
        a[4]
      ), (!s || r & /*disable*/
      8) && Ue(
        e,
        "hide-label",
        /*disable*/
        a[3]
      );
    },
    i(a) {
      s || (wo(l.$$.fragment, a), s = !0);
    },
    o(a) {
      vo(l.$$.fragment, a), s = !1;
    },
    d(a) {
      a && fo(e), uo(l);
    }
  };
}
function yo(n, e, t) {
  let { label: l = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: s = !1 } = e, { float: a = !0 } = e;
  return n.$$set = (r) => {
    "label" in r && t(0, l = r.label), "Icon" in r && t(1, i = r.Icon), "show_label" in r && t(2, o = r.show_label), "disable" in r && t(3, s = r.disable), "float" in r && t(4, a = r.float);
  }, [l, i, o, s, a];
}
class hi extends ro {
  constructor(e) {
    super(), co(this, e, yo, ko, mo, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: qo,
  append: Mn,
  attr: je,
  bubble: So,
  create_component: Co,
  destroy_component: Eo,
  detach: mi,
  element: Nn,
  init: zo,
  insert: gi,
  listen: Do,
  mount_component: Mo,
  safe_not_equal: No,
  set_data: Io,
  set_style: It,
  space: Bo,
  text: jo,
  toggle_class: ge,
  transition_in: To,
  transition_out: Lo
} = window.__gradio__svelte__internal;
function Kn(n) {
  let e, t;
  return {
    c() {
      e = Nn("span"), t = jo(
        /*label*/
        n[1]
      ), je(e, "class", "svelte-lpi64a");
    },
    m(l, i) {
      gi(l, e, i), Mn(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && Io(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && mi(e);
    }
  };
}
function Fo(n) {
  let e, t, l, i, o, s, a, r = (
    /*show_label*/
    n[2] && Kn(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Nn("button"), r && r.c(), t = Bo(), l = Nn("div"), Co(i.$$.fragment), je(l, "class", "svelte-lpi64a"), ge(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), ge(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), e.disabled = /*disabled*/
      n[7], je(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), je(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), je(
        e,
        "title",
        /*label*/
        n[1]
      ), je(e, "class", "svelte-lpi64a"), ge(
        e,
        "pending",
        /*pending*/
        n[3]
      ), ge(
        e,
        "padded",
        /*padded*/
        n[5]
      ), ge(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), ge(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), It(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[11] ? (
        /*_color*/
        n[11]
      ) : "var(--block-label-text-color)"), It(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      ));
    },
    m(u, f) {
      gi(u, e, f), r && r.m(e, null), Mn(e, t), Mn(e, l), Mo(i, l, null), o = !0, s || (a = Do(
        e,
        "click",
        /*click_handler*/
        n[13]
      ), s = !0);
    },
    p(u, [f]) {
      /*show_label*/
      u[2] ? r ? r.p(u, f) : (r = Kn(u), r.c(), r.m(e, t)) : r && (r.d(1), r = null), (!o || f & /*size*/
      16) && ge(
        l,
        "small",
        /*size*/
        u[4] === "small"
      ), (!o || f & /*size*/
      16) && ge(
        l,
        "large",
        /*size*/
        u[4] === "large"
      ), (!o || f & /*disabled*/
      128) && (e.disabled = /*disabled*/
      u[7]), (!o || f & /*label*/
      2) && je(
        e,
        "aria-label",
        /*label*/
        u[1]
      ), (!o || f & /*hasPopup*/
      256) && je(
        e,
        "aria-haspopup",
        /*hasPopup*/
        u[8]
      ), (!o || f & /*label*/
      2) && je(
        e,
        "title",
        /*label*/
        u[1]
      ), (!o || f & /*pending*/
      8) && ge(
        e,
        "pending",
        /*pending*/
        u[3]
      ), (!o || f & /*padded*/
      32) && ge(
        e,
        "padded",
        /*padded*/
        u[5]
      ), (!o || f & /*highlight*/
      64) && ge(
        e,
        "highlight",
        /*highlight*/
        u[6]
      ), (!o || f & /*transparent*/
      512) && ge(
        e,
        "transparent",
        /*transparent*/
        u[9]
      ), f & /*disabled, _color*/
      2176 && It(e, "color", !/*disabled*/
      u[7] && /*_color*/
      u[11] ? (
        /*_color*/
        u[11]
      ) : "var(--block-label-text-color)"), f & /*disabled, background*/
      1152 && It(e, "--bg-color", /*disabled*/
      u[7] ? "auto" : (
        /*background*/
        u[10]
      ));
    },
    i(u) {
      o || (To(i.$$.fragment, u), o = !0);
    },
    o(u) {
      Lo(i.$$.fragment, u), o = !1;
    },
    d(u) {
      u && mi(e), r && r.d(), Eo(i), s = !1, a();
    }
  };
}
function Oo(n, e, t) {
  let l, { Icon: i } = e, { label: o = "" } = e, { show_label: s = !1 } = e, { pending: a = !1 } = e, { size: r = "small" } = e, { padded: u = !0 } = e, { highlight: f = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: d = !1 } = e, { color: c = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: p = "var(--background-fill-primary)" } = e;
  function C(b) {
    So.call(this, n, b);
  }
  return n.$$set = (b) => {
    "Icon" in b && t(0, i = b.Icon), "label" in b && t(1, o = b.label), "show_label" in b && t(2, s = b.show_label), "pending" in b && t(3, a = b.pending), "size" in b && t(4, r = b.size), "padded" in b && t(5, u = b.padded), "highlight" in b && t(6, f = b.highlight), "disabled" in b && t(7, _ = b.disabled), "hasPopup" in b && t(8, d = b.hasPopup), "color" in b && t(12, c = b.color), "transparent" in b && t(9, m = b.transparent), "background" in b && t(10, p = b.background);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    4160 && t(11, l = f ? "var(--color-accent)" : c);
  }, [
    i,
    o,
    s,
    a,
    r,
    u,
    f,
    _,
    d,
    m,
    p,
    l,
    c,
    C
  ];
}
class rt extends qo {
  constructor(e) {
    super(), zo(this, e, Oo, Fo, No, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 12,
      transparent: 9,
      background: 10
    });
  }
}
const {
  SvelteComponent: Ao,
  append: Po,
  attr: en,
  binding_callbacks: Ro,
  create_slot: Uo,
  detach: Zo,
  element: Qn,
  get_all_dirty_from_scope: Wo,
  get_slot_changes: Vo,
  init: Go,
  insert: Ho,
  safe_not_equal: Jo,
  toggle_class: Ze,
  transition_in: Xo,
  transition_out: Yo,
  update_slot_base: Ko
} = window.__gradio__svelte__internal;
function Qo(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[5].default
  ), o = Uo(
    i,
    n,
    /*$$scope*/
    n[4],
    null
  );
  return {
    c() {
      e = Qn("div"), t = Qn("div"), o && o.c(), en(t, "class", "icon svelte-3w3rth"), en(e, "class", "empty svelte-3w3rth"), en(e, "aria-label", "Empty value"), Ze(
        e,
        "small",
        /*size*/
        n[0] === "small"
      ), Ze(
        e,
        "large",
        /*size*/
        n[0] === "large"
      ), Ze(
        e,
        "unpadded_box",
        /*unpadded_box*/
        n[1]
      ), Ze(
        e,
        "small_parent",
        /*parent_height*/
        n[3]
      );
    },
    m(s, a) {
      Ho(s, e, a), Po(e, t), o && o.m(t, null), n[6](e), l = !0;
    },
    p(s, [a]) {
      o && o.p && (!l || a & /*$$scope*/
      16) && Ko(
        o,
        i,
        s,
        /*$$scope*/
        s[4],
        l ? Vo(
          i,
          /*$$scope*/
          s[4],
          a,
          null
        ) : Wo(
          /*$$scope*/
          s[4]
        ),
        null
      ), (!l || a & /*size*/
      1) && Ze(
        e,
        "small",
        /*size*/
        s[0] === "small"
      ), (!l || a & /*size*/
      1) && Ze(
        e,
        "large",
        /*size*/
        s[0] === "large"
      ), (!l || a & /*unpadded_box*/
      2) && Ze(
        e,
        "unpadded_box",
        /*unpadded_box*/
        s[1]
      ), (!l || a & /*parent_height*/
      8) && Ze(
        e,
        "small_parent",
        /*parent_height*/
        s[3]
      );
    },
    i(s) {
      l || (Xo(o, s), l = !0);
    },
    o(s) {
      Yo(o, s), l = !1;
    },
    d(s) {
      s && Zo(e), o && o.d(s), n[6](null);
    }
  };
}
function $o(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e, { size: s = "small" } = e, { unpadded_box: a = !1 } = e, r;
  function u(_) {
    var d;
    if (!_) return !1;
    const { height: c } = _.getBoundingClientRect(), { height: m } = ((d = _.parentElement) === null || d === void 0 ? void 0 : d.getBoundingClientRect()) || { height: c };
    return c > m + 2;
  }
  function f(_) {
    Ro[_ ? "unshift" : "push"](() => {
      r = _, t(2, r);
    });
  }
  return n.$$set = (_) => {
    "size" in _ && t(0, s = _.size), "unpadded_box" in _ && t(1, a = _.unpadded_box), "$$scope" in _ && t(4, o = _.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*el*/
    4 && t(3, l = u(r));
  }, [s, a, r, l, o, i, f];
}
class pi extends Ao {
  constructor(e) {
    super(), Go(this, e, $o, Qo, Jo, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: xo,
  append: tn,
  attr: Se,
  detach: es,
  init: ts,
  insert: ns,
  noop: nn,
  safe_not_equal: ls,
  set_style: Me,
  svg_element: Bt
} = window.__gradio__svelte__internal;
function is(n) {
  let e, t, l, i;
  return {
    c() {
      e = Bt("svg"), t = Bt("g"), l = Bt("path"), i = Bt("path"), Se(l, "d", "M18,6L6.087,17.913"), Me(l, "fill", "none"), Me(l, "fill-rule", "nonzero"), Me(l, "stroke-width", "2px"), Se(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), Se(i, "d", "M4.364,4.364L19.636,19.636"), Me(i, "fill", "none"), Me(i, "fill-rule", "nonzero"), Me(i, "stroke-width", "2px"), Se(e, "width", "100%"), Se(e, "height", "100%"), Se(e, "viewBox", "0 0 24 24"), Se(e, "version", "1.1"), Se(e, "xmlns", "http://www.w3.org/2000/svg"), Se(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), Se(e, "xml:space", "preserve"), Se(e, "stroke", "currentColor"), Me(e, "fill-rule", "evenodd"), Me(e, "clip-rule", "evenodd"), Me(e, "stroke-linecap", "round"), Me(e, "stroke-linejoin", "round");
    },
    m(o, s) {
      ns(o, e, s), tn(e, t), tn(t, l), tn(e, i);
    },
    p: nn,
    i: nn,
    o: nn,
    d(o) {
      o && es(e);
    }
  };
}
class os extends xo {
  constructor(e) {
    super(), ts(this, e, null, is, ls, {});
  }
}
const {
  SvelteComponent: ss,
  append: rs,
  attr: vt,
  detach: as,
  init: us,
  insert: fs,
  noop: ln,
  safe_not_equal: cs,
  svg_element: $n
} = window.__gradio__svelte__internal;
function _s(n) {
  let e, t;
  return {
    c() {
      e = $n("svg"), t = $n("path"), vt(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), vt(t, "fill", "currentColor"), vt(e, "id", "icon"), vt(e, "xmlns", "http://www.w3.org/2000/svg"), vt(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      fs(l, e, i), rs(e, t);
    },
    p: ln,
    i: ln,
    o: ln,
    d(l) {
      l && as(e);
    }
  };
}
class ds extends ss {
  constructor(e) {
    super(), us(this, e, null, _s, cs, {});
  }
}
const {
  SvelteComponent: hs,
  append: ms,
  attr: et,
  detach: gs,
  init: ps,
  insert: bs,
  noop: on,
  safe_not_equal: ws,
  svg_element: xn
} = window.__gradio__svelte__internal;
function vs(n) {
  let e, t;
  return {
    c() {
      e = xn("svg"), t = xn("path"), et(t, "fill", "currentColor"), et(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), et(e, "xmlns", "http://www.w3.org/2000/svg"), et(e, "width", "100%"), et(e, "height", "100%"), et(e, "viewBox", "0 0 32 32");
    },
    m(l, i) {
      bs(l, e, i), ms(e, t);
    },
    p: on,
    i: on,
    o: on,
    d(l) {
      l && gs(e);
    }
  };
}
class ks extends hs {
  constructor(e) {
    super(), ps(this, e, null, vs, ws, {});
  }
}
const {
  SvelteComponent: ys,
  append: sn,
  attr: Ce,
  detach: qs,
  init: Ss,
  insert: Cs,
  noop: rn,
  safe_not_equal: Es,
  svg_element: jt
} = window.__gradio__svelte__internal;
function zs(n) {
  let e, t, l, i;
  return {
    c() {
      e = jt("svg"), t = jt("g"), l = jt("path"), i = jt("path"), Ce(l, "fill", "currentColor"), Ce(l, "d", "m5.505 11.41l.53.53l-.53-.53ZM3 14.952h-.75H3ZM9.048 21v.75V21ZM11.41 5.505l-.53-.53l.53.53Zm1.831 12.34a.75.75 0 0 0 1.06-1.061l-1.06 1.06ZM7.216 9.697a.75.75 0 1 0-1.06 1.061l1.06-1.06Zm10.749 2.362l-5.905 5.905l1.06 1.06l5.905-5.904l-1.06-1.06Zm-11.93-.12l5.905-5.905l-1.06-1.06l-5.905 5.904l1.06 1.06Zm0 6.025c-.85-.85-1.433-1.436-1.812-1.933c-.367-.481-.473-.79-.473-1.08h-1.5c0 .749.312 1.375.78 1.99c.455.596 1.125 1.263 1.945 2.083l1.06-1.06Zm-1.06-7.086c-.82.82-1.49 1.488-1.945 2.084c-.468.614-.78 1.24-.78 1.99h1.5c0-.29.106-.6.473-1.08c.38-.498.962-1.083 1.812-1.933l-1.06-1.06Zm7.085 7.086c-.85.85-1.435 1.433-1.933 1.813c-.48.366-.79.472-1.08.472v1.5c.75 0 1.376-.312 1.99-.78c.596-.455 1.264-1.125 2.084-1.945l-1.06-1.06Zm-7.085 1.06c.82.82 1.487 1.49 2.084 1.945c.614.468 1.24.78 1.989.78v-1.5c-.29 0-.599-.106-1.08-.473c-.497-.38-1.083-.962-1.933-1.812l-1.06 1.06Zm12.99-12.99c.85.85 1.433 1.436 1.813 1.933c.366.481.472.79.472 1.08h1.5c0-.749-.312-1.375-.78-1.99c-.455-.596-1.125-1.263-1.945-2.083l-1.06 1.06Zm1.06 7.086c.82-.82 1.49-1.488 1.945-2.084c.468-.614.78-1.24.78-1.99h-1.5c0 .29-.106.6-.473 1.08c-.38.498-.962 1.083-1.812 1.933l1.06 1.06Zm0-8.146c-.82-.82-1.487-1.49-2.084-1.945c-.614-.468-1.24-.78-1.989-.78v1.5c.29 0 .599.106 1.08.473c.497.38 1.083.962 1.933 1.812l1.06-1.06Zm-7.085 1.06c.85-.85 1.435-1.433 1.933-1.812c.48-.367.79-.473 1.08-.473v-1.5c-.75 0-1.376.312-1.99.78c-.596.455-1.264 1.125-2.084 1.945l1.06 1.06Zm2.362 10.749L7.216 9.698l-1.06 1.061l7.085 7.085l1.06-1.06Z"), Ce(i, "stroke", "currentColor"), Ce(i, "stroke-linecap", "round"), Ce(i, "stroke-width", "1.5"), Ce(i, "d", "M9 21h12"), Ce(t, "fill", "none"), Ce(e, "xmlns", "http://www.w3.org/2000/svg"), Ce(e, "width", "100%"), Ce(e, "height", "100%"), Ce(e, "viewBox", "0 0 24 24");
    },
    m(o, s) {
      Cs(o, e, s), sn(e, t), sn(t, l), sn(t, i);
    },
    p: rn,
    i: rn,
    o: rn,
    d(o) {
      o && qs(e);
    }
  };
}
class Ds extends ys {
  constructor(e) {
    super(), Ss(this, e, null, zs, Es, {});
  }
}
const {
  SvelteComponent: Ms,
  append: an,
  attr: $,
  detach: Ns,
  init: Is,
  insert: Bs,
  noop: un,
  safe_not_equal: js,
  svg_element: Tt
} = window.__gradio__svelte__internal;
function Ts(n) {
  let e, t, l, i;
  return {
    c() {
      e = Tt("svg"), t = Tt("rect"), l = Tt("circle"), i = Tt("polyline"), $(t, "x", "3"), $(t, "y", "3"), $(t, "width", "18"), $(t, "height", "18"), $(t, "rx", "2"), $(t, "ry", "2"), $(l, "cx", "8.5"), $(l, "cy", "8.5"), $(l, "r", "1.5"), $(i, "points", "21 15 16 10 5 21"), $(e, "xmlns", "http://www.w3.org/2000/svg"), $(e, "width", "100%"), $(e, "height", "100%"), $(e, "viewBox", "0 0 24 24"), $(e, "fill", "none"), $(e, "stroke", "currentColor"), $(e, "stroke-width", "1.5"), $(e, "stroke-linecap", "round"), $(e, "stroke-linejoin", "round"), $(e, "class", "feather feather-image");
    },
    m(o, s) {
      Bs(o, e, s), an(e, t), an(e, l), an(e, i);
    },
    p: un,
    i: un,
    o: un,
    d(o) {
      o && Ns(e);
    }
  };
}
let Kt = class extends Ms {
  constructor(e) {
    super(), Is(this, e, null, Ts, js, {});
  }
};
const {
  SvelteComponent: Ls,
  append: Fs,
  attr: tt,
  detach: Os,
  init: As,
  insert: Ps,
  noop: fn,
  safe_not_equal: Rs,
  svg_element: el
} = window.__gradio__svelte__internal;
function Us(n) {
  let e, t;
  return {
    c() {
      e = el("svg"), t = el("path"), tt(t, "fill", "currentColor"), tt(t, "d", "M13.75 2a2.25 2.25 0 0 1 2.236 2.002V4h1.764A2.25 2.25 0 0 1 20 6.25V11h-1.5V6.25a.75.75 0 0 0-.75-.75h-2.129c-.404.603-1.091 1-1.871 1h-3.5c-.78 0-1.467-.397-1.871-1H6.25a.75.75 0 0 0-.75.75v13.5c0 .414.336.75.75.75h4.78a3.99 3.99 0 0 0 .505 1.5H6.25A2.25 2.25 0 0 1 4 19.75V6.25A2.25 2.25 0 0 1 6.25 4h1.764a2.25 2.25 0 0 1 2.236-2h3.5Zm2.245 2.096L16 4.25c0-.052-.002-.103-.005-.154ZM13.75 3.5h-3.5a.75.75 0 0 0 0 1.5h3.5a.75.75 0 0 0 0-1.5ZM15 12a3 3 0 0 0-3 3v5c0 .556.151 1.077.415 1.524l3.494-3.494a2.25 2.25 0 0 1 3.182 0l3.494 3.494c.264-.447.415-.968.415-1.524v-5a3 3 0 0 0-3-3h-5Zm0 11a2.985 2.985 0 0 1-1.524-.415l3.494-3.494a.75.75 0 0 1 1.06 0l3.494 3.494A2.985 2.985 0 0 1 20 23h-5Zm5-7a1 1 0 1 1 0-2a1 1 0 0 1 0 2Z"), tt(e, "xmlns", "http://www.w3.org/2000/svg"), tt(e, "width", "100%"), tt(e, "height", "100%"), tt(e, "viewBox", "0 0 24 24");
    },
    m(l, i) {
      Ps(l, e, i), Fs(e, t);
    },
    p: fn,
    i: fn,
    o: fn,
    d(l) {
      l && Os(e);
    }
  };
}
class Zs extends Ls {
  constructor(e) {
    super(), As(this, e, null, Us, Rs, {});
  }
}
const {
  SvelteComponent: Ws,
  append: tl,
  attr: pe,
  detach: Vs,
  init: Gs,
  insert: Hs,
  noop: cn,
  safe_not_equal: Js,
  svg_element: _n
} = window.__gradio__svelte__internal;
function Xs(n) {
  let e, t, l;
  return {
    c() {
      e = _n("svg"), t = _n("polyline"), l = _n("path"), pe(t, "points", "1 4 1 10 7 10"), pe(l, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), pe(e, "xmlns", "http://www.w3.org/2000/svg"), pe(e, "width", "100%"), pe(e, "height", "100%"), pe(e, "viewBox", "0 0 24 24"), pe(e, "fill", "none"), pe(e, "stroke", "currentColor"), pe(e, "stroke-width", "2"), pe(e, "stroke-linecap", "round"), pe(e, "stroke-linejoin", "round"), pe(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      Hs(i, e, o), tl(e, t), tl(e, l);
    },
    p: cn,
    i: cn,
    o: cn,
    d(i) {
      i && Vs(e);
    }
  };
}
class Ys extends Ws {
  constructor(e) {
    super(), Gs(this, e, null, Xs, Js, {});
  }
}
const {
  SvelteComponent: Ks,
  append: dn,
  attr: se,
  detach: Qs,
  init: $s,
  insert: xs,
  noop: hn,
  safe_not_equal: er,
  svg_element: Lt
} = window.__gradio__svelte__internal;
function tr(n) {
  let e, t, l, i;
  return {
    c() {
      e = Lt("svg"), t = Lt("path"), l = Lt("polyline"), i = Lt("line"), se(t, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), se(l, "points", "17 8 12 3 7 8"), se(i, "x1", "12"), se(i, "y1", "3"), se(i, "x2", "12"), se(i, "y2", "15"), se(e, "xmlns", "http://www.w3.org/2000/svg"), se(e, "width", "90%"), se(e, "height", "90%"), se(e, "viewBox", "0 0 24 24"), se(e, "fill", "none"), se(e, "stroke", "currentColor"), se(e, "stroke-width", "2"), se(e, "stroke-linecap", "round"), se(e, "stroke-linejoin", "round"), se(e, "class", "feather feather-upload");
    },
    m(o, s) {
      xs(o, e, s), dn(e, t), dn(e, l), dn(e, i);
    },
    p: hn,
    i: hn,
    o: hn,
    d(o) {
      o && Qs(e);
    }
  };
}
let bi = class extends Ks {
  constructor(e) {
    super(), $s(this, e, null, tr, er, {});
  }
};
const {
  SvelteComponent: nr,
  create_component: lr,
  destroy_component: ir,
  init: or,
  mount_component: sr,
  safe_not_equal: rr,
  transition_in: ar,
  transition_out: ur
} = window.__gradio__svelte__internal, { createEventDispatcher: fr } = window.__gradio__svelte__internal;
function cr(n) {
  let e, t;
  return e = new rt({
    props: {
      Icon: ds,
      label: (
        /*i18n*/
        n[2]("common.share")
      ),
      pending: (
        /*pending*/
        n[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    n[5]
  ), {
    c() {
      lr(e.$$.fragment);
    },
    m(l, i) {
      sr(e, l, i), t = !0;
    },
    p(l, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      l[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      l[3]), e.$set(o);
    },
    i(l) {
      t || (ar(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ur(e.$$.fragment, l), t = !1;
    },
    d(l) {
      ir(e, l);
    }
  };
}
function _r(n, e, t) {
  const l = fr();
  let { formatter: i } = e, { value: o } = e, { i18n: s } = e, a = !1;
  const r = async () => {
    try {
      t(3, a = !0);
      const u = await i(o);
      l("share", { description: u });
    } catch (u) {
      console.error(u);
      let f = u instanceof Rt ? u.message : "Share failed.";
      l("error", f);
    } finally {
      t(3, a = !1);
    }
  };
  return n.$$set = (u) => {
    "formatter" in u && t(0, i = u.formatter), "value" in u && t(1, o = u.value), "i18n" in u && t(2, s = u.i18n);
  }, [i, o, s, a, l, r];
}
class dr extends nr {
  constructor(e) {
    super(), or(this, e, _r, cr, rr, { formatter: 0, value: 1, i18n: 2 });
  }
}
const {
  SvelteComponent: hr,
  append: $e,
  attr: In,
  create_component: mr,
  destroy_component: gr,
  detach: Ut,
  element: Bn,
  init: pr,
  insert: Zt,
  mount_component: br,
  safe_not_equal: wr,
  set_data: jn,
  space: Tn,
  text: yt,
  toggle_class: nl,
  transition_in: vr,
  transition_out: kr
} = window.__gradio__svelte__internal;
function ll(n) {
  let e, t, l = (
    /*i18n*/
    n[1]("common.or") + ""
  ), i, o, s, a = (
    /*message*/
    (n[2] || /*i18n*/
    n[1]("upload_text.click_to_upload")) + ""
  ), r;
  return {
    c() {
      e = Bn("span"), t = yt("- "), i = yt(l), o = yt(" -"), s = Tn(), r = yt(a), In(e, "class", "or svelte-kzcjhc");
    },
    m(u, f) {
      Zt(u, e, f), $e(e, t), $e(e, i), $e(e, o), Zt(u, s, f), Zt(u, r, f);
    },
    p(u, f) {
      f & /*i18n*/
      2 && l !== (l = /*i18n*/
      u[1]("common.or") + "") && jn(i, l), f & /*message, i18n*/
      6 && a !== (a = /*message*/
      (u[2] || /*i18n*/
      u[1]("upload_text.click_to_upload")) + "") && jn(r, a);
    },
    d(u) {
      u && (Ut(e), Ut(s), Ut(r));
    }
  };
}
function yr(n) {
  let e, t, l, i, o = (
    /*i18n*/
    n[1](
      /*defs*/
      n[5][
        /*type*/
        n[0]
      ] || /*defs*/
      n[5].file
    ) + ""
  ), s, a, r;
  l = new bi({});
  let u = (
    /*mode*/
    n[3] !== "short" && ll(n)
  );
  return {
    c() {
      e = Bn("div"), t = Bn("span"), mr(l.$$.fragment), i = Tn(), s = yt(o), a = Tn(), u && u.c(), In(t, "class", "icon-wrap svelte-kzcjhc"), nl(
        t,
        "hovered",
        /*hovered*/
        n[4]
      ), In(e, "class", "wrap svelte-kzcjhc");
    },
    m(f, _) {
      Zt(f, e, _), $e(e, t), br(l, t, null), $e(e, i), $e(e, s), $e(e, a), u && u.m(e, null), r = !0;
    },
    p(f, [_]) {
      (!r || _ & /*hovered*/
      16) && nl(
        t,
        "hovered",
        /*hovered*/
        f[4]
      ), (!r || _ & /*i18n, type*/
      3) && o !== (o = /*i18n*/
      f[1](
        /*defs*/
        f[5][
          /*type*/
          f[0]
        ] || /*defs*/
        f[5].file
      ) + "") && jn(s, o), /*mode*/
      f[3] !== "short" ? u ? u.p(f, _) : (u = ll(f), u.c(), u.m(e, null)) : u && (u.d(1), u = null);
    },
    i(f) {
      r || (vr(l.$$.fragment, f), r = !0);
    },
    o(f) {
      kr(l.$$.fragment, f), r = !1;
    },
    d(f) {
      f && Ut(e), gr(l), u && u.d();
    }
  };
}
function qr(n, e, t) {
  let { type: l = "file" } = e, { i18n: i } = e, { message: o = void 0 } = e, { mode: s = "full" } = e, { hovered: a = !1 } = e;
  const r = {
    image: "upload_text.drop_image",
    video: "upload_text.drop_video",
    audio: "upload_text.drop_audio",
    file: "upload_text.drop_file",
    csv: "upload_text.drop_csv"
  };
  return n.$$set = (u) => {
    "type" in u && t(0, l = u.type), "i18n" in u && t(1, i = u.i18n), "message" in u && t(2, o = u.message), "mode" in u && t(3, s = u.mode), "hovered" in u && t(4, a = u.hovered);
  }, [l, i, o, s, a, r];
}
class Sr extends hr {
  constructor(e) {
    super(), pr(this, e, qr, yr, wr, {
      type: 0,
      i18n: 1,
      message: 2,
      mode: 3,
      hovered: 4
    });
  }
}
const {
  SvelteComponent: Cr,
  attr: Er,
  create_slot: zr,
  detach: Dr,
  element: Mr,
  get_all_dirty_from_scope: Nr,
  get_slot_changes: Ir,
  init: Br,
  insert: jr,
  safe_not_equal: Tr,
  toggle_class: il,
  transition_in: Lr,
  transition_out: Fr,
  update_slot_base: Or
} = window.__gradio__svelte__internal;
function Ar(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[2].default
  ), i = zr(
    l,
    n,
    /*$$scope*/
    n[1],
    null
  );
  return {
    c() {
      e = Mr("div"), i && i.c(), Er(e, "class", "svelte-ipfyu7"), il(
        e,
        "show_border",
        /*show_border*/
        n[0]
      );
    },
    m(o, s) {
      jr(o, e, s), i && i.m(e, null), t = !0;
    },
    p(o, [s]) {
      i && i.p && (!t || s & /*$$scope*/
      2) && Or(
        i,
        l,
        o,
        /*$$scope*/
        o[1],
        t ? Ir(
          l,
          /*$$scope*/
          o[1],
          s,
          null
        ) : Nr(
          /*$$scope*/
          o[1]
        ),
        null
      ), (!t || s & /*show_border*/
      1) && il(
        e,
        "show_border",
        /*show_border*/
        o[0]
      );
    },
    i(o) {
      t || (Lr(i, o), t = !0);
    },
    o(o) {
      Fr(i, o), t = !1;
    },
    d(o) {
      o && Dr(e), i && i.d(o);
    }
  };
}
function Pr(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_border: o = !1 } = e;
  return n.$$set = (s) => {
    "show_border" in s && t(0, o = s.show_border), "$$scope" in s && t(1, i = s.$$scope);
  }, [o, i, l];
}
class Rr extends Cr {
  constructor(e) {
    super(), Br(this, e, Pr, Ar, Tr, { show_border: 0 });
  }
}
const wi = (n) => {
  let e = n.currentTarget;
  const t = e.getBoundingClientRect(), l = e.naturalWidth / t.width, i = e.naturalHeight / t.height;
  if (l > i) {
    const a = e.naturalHeight / l, r = (t.height - a) / 2;
    var o = Math.round((n.clientX - t.left) * l), s = Math.round((n.clientY - t.top - r) * l);
  } else {
    const a = e.naturalWidth / i, r = (t.width - a) / 2;
    var o = Math.round((n.clientX - t.left - r) * i), s = Math.round((n.clientY - t.top) * i);
  }
  return o < 0 || o >= e.naturalWidth || s < 0 || s >= e.naturalHeight ? null : [o, s];
}, {
  SvelteComponent: Ur,
  append: ol,
  attr: ke,
  bubble: sl,
  check_outros: Ln,
  create_component: zt,
  destroy_component: Dt,
  detach: at,
  element: Wt,
  empty: Zr,
  group_outros: Fn,
  init: Wr,
  insert: ut,
  listen: Vr,
  mount_component: Mt,
  safe_not_equal: Gr,
  space: On,
  src_url_equal: rl,
  toggle_class: al,
  transition_in: ce,
  transition_out: De
} = window.__gradio__svelte__internal, { createEventDispatcher: Hr } = window.__gradio__svelte__internal;
function Jr(n) {
  let e, t, l, i, o, s, a, r, u, f = (
    /*show_download_button*/
    n[3] && ul(n)
  ), _ = (
    /*show_share_button*/
    n[5] && fl(n)
  );
  return {
    c() {
      e = Wt("div"), f && f.c(), t = On(), _ && _.c(), l = On(), i = Wt("button"), o = Wt("img"), ke(e, "class", "icon-buttons svelte-1e0ed51"), rl(o.src, s = /*value*/
      n[0].url) || ke(o, "src", s), ke(o, "alt", ""), ke(o, "loading", "lazy"), ke(o, "class", "svelte-1e0ed51"), al(
        o,
        "selectable",
        /*selectable*/
        n[4]
      ), ke(i, "class", "svelte-1e0ed51");
    },
    m(d, c) {
      ut(d, e, c), f && f.m(e, null), ol(e, t), _ && _.m(e, null), ut(d, l, c), ut(d, i, c), ol(i, o), a = !0, r || (u = Vr(
        i,
        "click",
        /*handle_click*/
        n[7]
      ), r = !0);
    },
    p(d, c) {
      /*show_download_button*/
      d[3] ? f ? (f.p(d, c), c & /*show_download_button*/
      8 && ce(f, 1)) : (f = ul(d), f.c(), ce(f, 1), f.m(e, t)) : f && (Fn(), De(f, 1, 1, () => {
        f = null;
      }), Ln()), /*show_share_button*/
      d[5] ? _ ? (_.p(d, c), c & /*show_share_button*/
      32 && ce(_, 1)) : (_ = fl(d), _.c(), ce(_, 1), _.m(e, null)) : _ && (Fn(), De(_, 1, 1, () => {
        _ = null;
      }), Ln()), (!a || c & /*value*/
      1 && !rl(o.src, s = /*value*/
      d[0].url)) && ke(o, "src", s), (!a || c & /*selectable*/
      16) && al(
        o,
        "selectable",
        /*selectable*/
        d[4]
      );
    },
    i(d) {
      a || (ce(f), ce(_), a = !0);
    },
    o(d) {
      De(f), De(_), a = !1;
    },
    d(d) {
      d && (at(e), at(l), at(i)), f && f.d(), _ && _.d(), r = !1, u();
    }
  };
}
function Xr(n) {
  let e, t;
  return e = new pi({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [Yr] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      zt(e.$$.fragment);
    },
    m(l, i) {
      Mt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*$$scope*/
      4096 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (ce(e.$$.fragment, l), t = !0);
    },
    o(l) {
      De(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Dt(e, l);
    }
  };
}
function ul(n) {
  let e, t, l, i, o;
  return t = new rt({
    props: {
      Icon: ks,
      label: (
        /*i18n*/
        n[6]("common.download")
      )
    }
  }), {
    c() {
      e = Wt("a"), zt(t.$$.fragment), ke(e, "href", l = /*value*/
      n[0].url), ke(e, "target", window.__is_colab__ ? "_blank" : null), ke(e, "download", i = /*value*/
      n[0].orig_name || "image");
    },
    m(s, a) {
      ut(s, e, a), Mt(t, e, null), o = !0;
    },
    p(s, a) {
      const r = {};
      a & /*i18n*/
      64 && (r.label = /*i18n*/
      s[6]("common.download")), t.$set(r), (!o || a & /*value*/
      1 && l !== (l = /*value*/
      s[0].url)) && ke(e, "href", l), (!o || a & /*value*/
      1 && i !== (i = /*value*/
      s[0].orig_name || "image")) && ke(e, "download", i);
    },
    i(s) {
      o || (ce(t.$$.fragment, s), o = !0);
    },
    o(s) {
      De(t.$$.fragment, s), o = !1;
    },
    d(s) {
      s && at(e), Dt(t);
    }
  };
}
function fl(n) {
  let e, t;
  return e = new dr({
    props: {
      i18n: (
        /*i18n*/
        n[6]
      ),
      formatter: (
        /*func*/
        n[8]
      ),
      value: (
        /*value*/
        n[0]
      )
    }
  }), e.$on(
    "share",
    /*share_handler*/
    n[9]
  ), e.$on(
    "error",
    /*error_handler*/
    n[10]
  ), {
    c() {
      zt(e.$$.fragment);
    },
    m(l, i) {
      Mt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i & /*i18n*/
      64 && (o.i18n = /*i18n*/
      l[6]), i & /*value*/
      1 && (o.value = /*value*/
      l[0]), e.$set(o);
    },
    i(l) {
      t || (ce(e.$$.fragment, l), t = !0);
    },
    o(l) {
      De(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Dt(e, l);
    }
  };
}
function Yr(n) {
  let e, t;
  return e = new Kt({}), {
    c() {
      zt(e.$$.fragment);
    },
    m(l, i) {
      Mt(e, l, i), t = !0;
    },
    i(l) {
      t || (ce(e.$$.fragment, l), t = !0);
    },
    o(l) {
      De(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Dt(e, l);
    }
  };
}
function Kr(n) {
  let e, t, l, i, o, s;
  e = new hi({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      Icon: Kt,
      label: (
        /*label*/
        n[1] || /*i18n*/
        n[6]("image.image")
      )
    }
  });
  const a = [Xr, Jr], r = [];
  function u(f, _) {
    return (
      /*value*/
      f[0] === null || !/*value*/
      f[0].url ? 0 : 1
    );
  }
  return l = u(n), i = r[l] = a[l](n), {
    c() {
      zt(e.$$.fragment), t = On(), i.c(), o = Zr();
    },
    m(f, _) {
      Mt(e, f, _), ut(f, t, _), r[l].m(f, _), ut(f, o, _), s = !0;
    },
    p(f, [_]) {
      const d = {};
      _ & /*show_label*/
      4 && (d.show_label = /*show_label*/
      f[2]), _ & /*label, i18n*/
      66 && (d.label = /*label*/
      f[1] || /*i18n*/
      f[6]("image.image")), e.$set(d);
      let c = l;
      l = u(f), l === c ? r[l].p(f, _) : (Fn(), De(r[c], 1, 1, () => {
        r[c] = null;
      }), Ln(), i = r[l], i ? i.p(f, _) : (i = r[l] = a[l](f), i.c()), ce(i, 1), i.m(o.parentNode, o));
    },
    i(f) {
      s || (ce(e.$$.fragment, f), ce(i), s = !0);
    },
    o(f) {
      De(e.$$.fragment, f), De(i), s = !1;
    },
    d(f) {
      f && (at(t), at(o)), Dt(e, f), r[l].d(f);
    }
  };
}
function Qr(n, e, t) {
  let { value: l } = e, { label: i = void 0 } = e, { show_label: o } = e, { show_download_button: s = !0 } = e, { selectable: a = !1 } = e, { show_share_button: r = !1 } = e, { i18n: u } = e;
  const f = Hr(), _ = (p) => {
    let C = wi(p);
    C && f("select", { index: C, value: null });
  }, d = async (p) => p ? `<img src="${await Vi(p)}" />` : "";
  function c(p) {
    sl.call(this, n, p);
  }
  function m(p) {
    sl.call(this, n, p);
  }
  return n.$$set = (p) => {
    "value" in p && t(0, l = p.value), "label" in p && t(1, i = p.label), "show_label" in p && t(2, o = p.show_label), "show_download_button" in p && t(3, s = p.show_download_button), "selectable" in p && t(4, a = p.selectable), "show_share_button" in p && t(5, r = p.show_share_button), "i18n" in p && t(6, u = p.i18n);
  }, [
    l,
    i,
    o,
    s,
    a,
    r,
    u,
    _,
    d,
    c,
    m
  ];
}
class $r extends Ur {
  constructor(e) {
    super(), Wr(this, e, Qr, Kr, Gr, {
      value: 0,
      label: 1,
      show_label: 2,
      show_download_button: 3,
      selectable: 4,
      show_share_button: 5,
      i18n: 6
    });
  }
}
var mn = new Intl.Collator(0, { numeric: 1 }).compare;
function cl(n, e, t) {
  return n = n.split("."), e = e.split("."), mn(n[0], e[0]) || mn(n[1], e[1]) || (e[2] = e.slice(2).join("."), t = /[.-]/.test(n[2] = n.slice(2).join(".")), t == /[.-]/.test(e[2]) ? mn(n[2], e[2]) : t ? -1 : 1);
}
function Ve(n, e, t) {
  return e.startsWith("http://") || e.startsWith("https://") ? t ? n : e : n + e;
}
function gn(n) {
  if (n.startsWith("http")) {
    const { protocol: e, host: t } = new URL(n);
    return t.endsWith("hf.space") ? {
      ws_protocol: "wss",
      host: t,
      http_protocol: e
    } : {
      ws_protocol: e === "https:" ? "wss" : "ws",
      http_protocol: e,
      host: t
    };
  } else if (n.startsWith("file:"))
    return {
      ws_protocol: "ws",
      http_protocol: "http:",
      host: "lite.local"
      // Special fake hostname only used for this case. This matches the hostname allowed in `is_self_host()` in `js/wasm/network/host.ts`.
    };
  return {
    ws_protocol: "wss",
    http_protocol: "https:",
    host: n
  };
}
const vi = /^[^\/]*\/[^\/]*$/, xr = /.*hf\.space\/{0,1}$/;
async function ea(n, e) {
  const t = {};
  e && (t.Authorization = `Bearer ${e}`);
  const l = n.trim();
  if (vi.test(l))
    try {
      const i = await fetch(
        `https://huggingface.co/api/spaces/${l}/host`,
        { headers: t }
      );
      if (i.status !== 200)
        throw new Error("Space metadata could not be loaded.");
      const o = (await i.json()).host;
      return {
        space_id: n,
        ...gn(o)
      };
    } catch (i) {
      throw new Error("Space metadata could not be loaded." + i.message);
    }
  if (xr.test(l)) {
    const { ws_protocol: i, http_protocol: o, host: s } = gn(l);
    return {
      space_id: s.replace(".hf.space", ""),
      ws_protocol: i,
      http_protocol: o,
      host: s
    };
  }
  return {
    space_id: !1,
    ...gn(l)
  };
}
function ta(n) {
  let e = {};
  return n.forEach(({ api_name: t }, l) => {
    t && (e[t] = l);
  }), e;
}
const na = /^(?=[^]*\b[dD]iscussions{0,1}\b)(?=[^]*\b[dD]isabled\b)[^]*$/;
async function _l(n) {
  try {
    const t = (await fetch(
      `https://huggingface.co/api/spaces/${n}/discussions`,
      {
        method: "HEAD"
      }
    )).headers.get("x-error-message");
    return !(t && na.test(t));
  } catch {
    return !1;
  }
}
function Te(n, e, t) {
  if (n == null)
    return null;
  if (Array.isArray(n)) {
    const l = [];
    for (const i of n)
      i == null ? l.push(null) : l.push(Te(i, e, t));
    return l;
  }
  return n.is_stream ? t == null ? new ft({
    ...n,
    url: e + "/stream/" + n.path
  }) : new ft({
    ...n,
    url: "/proxy=" + t + "stream/" + n.path
  }) : new ft({
    ...n,
    url: ia(n.path, e, t)
  });
}
function la(n) {
  try {
    const e = new URL(n);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function ia(n, e, t) {
  return n == null ? t ? `/proxy=${t}file=` : `${e}/file=` : la(n) ? n : t ? `/proxy=${t}file=${n}` : `${e}/file=${n}`;
}
async function oa(n, e, t, l = ua) {
  let i = (Array.isArray(n) ? n : [n]).map(
    (o) => o.blob
  );
  return await Promise.all(
    await l(e, i, void 0, t).then(
      async (o) => {
        if (o.error)
          throw new Error(o.error);
        return o.files ? o.files.map((s, a) => {
          const r = new ft({ ...n[a], path: s });
          return Te(r, e, null);
        }) : [];
      }
    )
  );
}
async function sa(n, e) {
  return n.map(
    (t, l) => new ft({
      path: t.name,
      orig_name: t.name,
      blob: t,
      size: t.size,
      mime_type: t.type,
      is_stream: e
    })
  );
}
class ft {
  constructor({
    path: e,
    url: t,
    orig_name: l,
    size: i,
    blob: o,
    is_stream: s,
    mime_type: a,
    alt_text: r
  }) {
    this.path = e, this.url = t, this.orig_name = l, this.size = i, this.blob = t ? void 0 : o, this.is_stream = s, this.mime_type = a, this.alt_text = r;
  }
}
const ra = "This application is too busy. Keep trying!", kt = "Connection errored out.";
let ki;
function aa(n, e) {
  return { post_data: t, upload_files: l, client: i, handle_blob: o };
  async function t(s, a, r) {
    const u = { "Content-Type": "application/json" };
    r && (u.Authorization = `Bearer ${r}`);
    try {
      var f = await n(s, {
        method: "POST",
        body: JSON.stringify(a),
        headers: u
      });
    } catch {
      return [{ error: kt }, 500];
    }
    return [await f.json(), f.status];
  }
  async function l(s, a, r, u) {
    const f = {};
    r && (f.Authorization = `Bearer ${r}`);
    const _ = 1e3, d = [];
    for (let m = 0; m < a.length; m += _) {
      const p = a.slice(m, m + _), C = new FormData();
      p.forEach((q) => {
        C.append("files", q);
      });
      try {
        const q = u ? `${s}/upload?upload_id=${u}` : `${s}/upload`;
        var c = await n(q, {
          method: "POST",
          body: C,
          headers: f
        });
      } catch {
        return { error: kt };
      }
      const b = await c.json();
      d.push(...b);
    }
    return { files: d };
  }
  async function i(s, a = { normalise_files: !0 }) {
    return new Promise(async (r) => {
      const { status_callback: u, hf_token: f, normalise_files: _ } = a, d = {
        predict: F,
        submit: ie,
        view_api: ne,
        component_server: ae
      }, c = _ ?? !0;
      if ((typeof window > "u" || !("WebSocket" in window)) && !global.Websocket) {
        const M = await import("./wrapper-6f348d45-B5bCGhfq.js");
        ki = (await import("./__vite-browser-external-DYxpcVy9.js")).Blob, global.WebSocket = M.WebSocket;
      }
      const { ws_protocol: m, http_protocol: p, host: C, space_id: b } = await ea(s, f), q = Math.random().toString(36).substring(2), g = {};
      let w, E = {}, T = !1;
      f && b && (T = await ca(b, f));
      async function L(M) {
        if (w = M, E = ta(M?.dependencies || []), w.auth_required)
          return {
            config: w,
            ...d
          };
        try {
          R = await ne(w);
        } catch (O) {
          console.error(`Could not get api details: ${O.message}`);
        }
        return {
          config: w,
          ...d
        };
      }
      let R;
      async function x(M) {
        if (u && u(M), M.status === "running")
          try {
            w = await gl(
              n,
              `${p}//${C}`,
              f
            );
            const O = await L(w);
            r(O);
          } catch (O) {
            console.error(O), u && u({
              status: "error",
              message: "Could not load this space.",
              load_status: "error",
              detail: "NOT_FOUND"
            });
          }
      }
      try {
        w = await gl(
          n,
          `${p}//${C}`,
          f
        );
        const M = await L(w);
        r(M);
      } catch (M) {
        console.error(M), b ? Pn(
          b,
          vi.test(b) ? "space_name" : "subdomain",
          x
        ) : u && u({
          status: "error",
          message: "Could not load this space.",
          load_status: "error",
          detail: "NOT_FOUND"
        });
      }
      function F(M, O, H) {
        let Z = !1, z = !1, G;
        if (typeof M == "number")
          G = w.dependencies[M];
        else {
          const S = M.replace(/^\//, "");
          G = w.dependencies[E[S]];
        }
        if (G.types.continuous)
          throw new Error(
            "Cannot call predict on this function as it may run forever. Use submit instead"
          );
        return new Promise((S, y) => {
          const k = ie(M, O, H);
          let h;
          k.on("data", (D) => {
            z && (k.destroy(), S(D)), Z = !0, h = D;
          }).on("status", (D) => {
            D.stage === "error" && y(D), D.stage === "complete" && (z = !0, Z && (k.destroy(), S(h)));
          });
        });
      }
      function ie(M, O, H, Z = null) {
        let z, G;
        if (typeof M == "number")
          z = M, G = R.unnamed_endpoints[z];
        else {
          const X = M.replace(/^\//, "");
          z = E[X], G = R.named_endpoints[M.trim()];
        }
        if (typeof z != "number")
          throw new Error(
            "There is no endpoint matching that name of fn_index matching that number."
          );
        let S, y, k = w.protocol ?? "sse";
        const h = typeof M == "number" ? "/predict" : M;
        let D, N = null, A = !1;
        const V = {};
        let U = "";
        typeof window < "u" && (U = new URLSearchParams(window.location.search).toString()), o(
          `${p}//${Ve(C, w.path, !0)}`,
          O,
          G,
          f
        ).then((X) => {
          if (D = { data: X || [], event_data: H, fn_index: z, trigger_id: Z }, _a(z, w))
            j({
              type: "status",
              endpoint: h,
              stage: "pending",
              queue: !1,
              fn_index: z,
              time: /* @__PURE__ */ new Date()
            }), t(
              `${p}//${Ve(C, w.path, !0)}/run${h.startsWith("/") ? h : `/${h}`}${U ? "?" + U : ""}`,
              {
                ...D,
                session_hash: q
              },
              f
            ).then(([K, le]) => {
              const Pe = c ? pn(
                K.data,
                G,
                w.root,
                w.root_url
              ) : K.data;
              le == 200 ? (j({
                type: "data",
                endpoint: h,
                fn_index: z,
                data: Pe,
                time: /* @__PURE__ */ new Date()
              }), j({
                type: "status",
                endpoint: h,
                fn_index: z,
                stage: "complete",
                eta: K.average_duration,
                queue: !1,
                time: /* @__PURE__ */ new Date()
              })) : j({
                type: "status",
                stage: "error",
                endpoint: h,
                fn_index: z,
                message: K.error,
                queue: !1,
                time: /* @__PURE__ */ new Date()
              });
            }).catch((K) => {
              j({
                type: "status",
                stage: "error",
                message: K.message,
                endpoint: h,
                fn_index: z,
                queue: !1,
                time: /* @__PURE__ */ new Date()
              });
            });
          else if (k == "ws") {
            j({
              type: "status",
              stage: "pending",
              queue: !0,
              endpoint: h,
              fn_index: z,
              time: /* @__PURE__ */ new Date()
            });
            let K = new URL(`${m}://${Ve(
              C,
              w.path,
              !0
            )}
							/queue/join${U ? "?" + U : ""}`);
            T && K.searchParams.set("__sign", T), S = e(K), S.onclose = (le) => {
              le.wasClean || j({
                type: "status",
                stage: "error",
                broken: !0,
                message: kt,
                queue: !0,
                endpoint: h,
                fn_index: z,
                time: /* @__PURE__ */ new Date()
              });
            }, S.onmessage = function(le) {
              const Pe = JSON.parse(le.data), { type: me, status: te, data: qe } = pl(
                Pe,
                g[z]
              );
              if (me === "update" && te && !A)
                j({
                  type: "status",
                  endpoint: h,
                  fn_index: z,
                  time: /* @__PURE__ */ new Date(),
                  ...te
                }), te.stage === "error" && S.close();
              else if (me === "hash") {
                S.send(JSON.stringify({ fn_index: z, session_hash: q }));
                return;
              } else me === "data" ? S.send(JSON.stringify({ ...D, session_hash: q })) : me === "complete" ? A = te : me === "log" ? j({
                type: "log",
                log: qe.log,
                level: qe.level,
                endpoint: h,
                fn_index: z
              }) : me === "generating" && j({
                type: "status",
                time: /* @__PURE__ */ new Date(),
                ...te,
                stage: te?.stage,
                queue: !0,
                endpoint: h,
                fn_index: z
              });
              qe && (j({
                type: "data",
                time: /* @__PURE__ */ new Date(),
                data: c ? pn(
                  qe.data,
                  G,
                  w.root,
                  w.root_url
                ) : qe.data,
                endpoint: h,
                fn_index: z
              }), A && (j({
                type: "status",
                time: /* @__PURE__ */ new Date(),
                ...A,
                stage: te?.stage,
                queue: !0,
                endpoint: h,
                fn_index: z
              }), S.close()));
            }, cl(w.version || "2.0.0", "3.6") < 0 && addEventListener(
              "open",
              () => S.send(JSON.stringify({ hash: q }))
            );
          } else {
            j({
              type: "status",
              stage: "pending",
              queue: !0,
              endpoint: h,
              fn_index: z,
              time: /* @__PURE__ */ new Date()
            });
            var he = new URLSearchParams({
              fn_index: z.toString(),
              session_hash: q
            }).toString();
            let K = new URL(
              `${p}//${Ve(
                C,
                w.path,
                !0
              )}/queue/join?${U ? U + "&" : ""}${he}`
            );
            y = new EventSource(K), y.onmessage = async function(le) {
              const Pe = JSON.parse(le.data), { type: me, status: te, data: qe } = pl(
                Pe,
                g[z]
              );
              if (me === "update" && te && !A)
                j({
                  type: "status",
                  endpoint: h,
                  fn_index: z,
                  time: /* @__PURE__ */ new Date(),
                  ...te
                }), te.stage === "error" && y.close();
              else if (me === "data") {
                N = Pe.event_id;
                let [yc, Zi] = await t(
                  `${p}//${Ve(
                    C,
                    w.path,
                    !0
                  )}/queue/data`,
                  {
                    ...D,
                    session_hash: q,
                    event_id: N
                  },
                  f
                );
                Zi !== 200 && (j({
                  type: "status",
                  stage: "error",
                  message: kt,
                  queue: !0,
                  endpoint: h,
                  fn_index: z,
                  time: /* @__PURE__ */ new Date()
                }), y.close());
              } else me === "complete" ? A = te : me === "log" ? j({
                type: "log",
                log: qe.log,
                level: qe.level,
                endpoint: h,
                fn_index: z
              }) : me === "generating" && j({
                type: "status",
                time: /* @__PURE__ */ new Date(),
                ...te,
                stage: te?.stage,
                queue: !0,
                endpoint: h,
                fn_index: z
              });
              qe && (j({
                type: "data",
                time: /* @__PURE__ */ new Date(),
                data: c ? pn(
                  qe.data,
                  G,
                  w.root,
                  w.root_url
                ) : qe.data,
                endpoint: h,
                fn_index: z
              }), A && (j({
                type: "status",
                time: /* @__PURE__ */ new Date(),
                ...A,
                stage: te?.stage,
                queue: !0,
                endpoint: h,
                fn_index: z
              }), y.close()));
            };
          }
        });
        function j(X) {
          const K = V[X.type] || [];
          K?.forEach((le) => le(X));
        }
        function v(X, he) {
          const K = V, le = K[X] || [];
          return K[X] = le, le?.push(he), { on: v, off: W, cancel: ee, destroy: re };
        }
        function W(X, he) {
          const K = V;
          let le = K[X] || [];
          return le = le?.filter((Pe) => Pe !== he), K[X] = le, { on: v, off: W, cancel: ee, destroy: re };
        }
        async function ee() {
          const X = {
            stage: "complete",
            queue: !1,
            time: /* @__PURE__ */ new Date()
          };
          A = X, j({
            ...X,
            type: "status",
            endpoint: h,
            fn_index: z
          });
          let he = {};
          k === "ws" ? (S && S.readyState === 0 ? S.addEventListener("open", () => {
            S.close();
          }) : S.close(), he = { fn_index: z, session_hash: q }) : (y.close(), he = { event_id: N });
          try {
            await n(
              `${p}//${Ve(
                C,
                w.path,
                !0
              )}/reset`,
              {
                headers: { "Content-Type": "application/json" },
                method: "POST",
                body: JSON.stringify(he)
              }
            );
          } catch {
            console.warn(
              "The `/reset` endpoint could not be called. Subsequent endpoint results may be unreliable."
            );
          }
        }
        function re() {
          for (const X in V)
            V[X].forEach((he) => {
              W(X, he);
            });
        }
        return {
          on: v,
          off: W,
          cancel: ee,
          destroy: re
        };
      }
      async function ae(M, O, H) {
        var Z;
        const z = { "Content-Type": "application/json" };
        f && (z.Authorization = `Bearer ${f}`);
        let G, S = w.components.find(
          (h) => h.id === M
        );
        (Z = S?.props) != null && Z.root_url ? G = S.props.root_url : G = `${p}//${Ve(
          C,
          w.path,
          !0
        )}/`;
        const y = await n(
          `${G}component_server/`,
          {
            method: "POST",
            body: JSON.stringify({
              data: H,
              component_id: M,
              fn_name: O,
              session_hash: q
            }),
            headers: z
          }
        );
        if (!y.ok)
          throw new Error(
            "Could not connect to component server: " + y.statusText
          );
        return await y.json();
      }
      async function ne(M) {
        if (R)
          return R;
        const O = { "Content-Type": "application/json" };
        f && (O.Authorization = `Bearer ${f}`);
        let H;
        if (cl(M.version || "2.0.0", "3.30") < 0 ? H = await n(
          "https://gradio-space-api-fetcher-v2.hf.space/api",
          {
            method: "POST",
            body: JSON.stringify({
              serialize: !1,
              config: JSON.stringify(M)
            }),
            headers: O
          }
        ) : H = await n(`${M.root}/info`, {
          headers: O
        }), !H.ok)
          throw new Error(kt);
        let Z = await H.json();
        return "api" in Z && (Z = Z.api), Z.named_endpoints["/predict"] && !Z.unnamed_endpoints[0] && (Z.unnamed_endpoints[0] = Z.named_endpoints["/predict"]), fa(Z, M, E);
      }
    });
  }
  async function o(s, a, r, u) {
    const f = await An(
      a,
      void 0,
      [],
      !0,
      r
    );
    return Promise.all(
      f.map(async ({ path: _, blob: d, type: c }) => {
        if (d) {
          const m = (await l(s, [d], u)).files[0];
          return { path: _, file_url: m, type: c, name: d?.name };
        }
        return { path: _, type: c };
      })
    ).then((_) => (_.forEach(({ path: d, file_url: c, type: m, name: p }) => {
      if (m === "Gallery")
        ml(a, c, d);
      else if (c) {
        const C = new ft({ path: c, orig_name: p });
        ml(a, C, d);
      }
    }), a));
  }
}
const { post_data: Cc, upload_files: ua, client: Ec, handle_blob: zc } = aa(
  fetch,
  (...n) => new WebSocket(...n)
);
function pn(n, e, t, l) {
  return n.map((i, o) => {
    var s, a, r, u;
    return ((a = (s = e?.returns) == null ? void 0 : s[o]) == null ? void 0 : a.component) === "File" ? Te(i, t, l) : ((u = (r = e?.returns) == null ? void 0 : r[o]) == null ? void 0 : u.component) === "Gallery" ? i.map((f) => Array.isArray(f) ? [Te(f[0], t, l), f[1]] : [Te(f, t, l), null]) : typeof i == "object" && i.path ? Te(i, t, l) : i;
  });
}
function dl(n, e, t, l) {
  switch (n.type) {
    case "string":
      return "string";
    case "boolean":
      return "boolean";
    case "number":
      return "number";
  }
  if (t === "JSONSerializable" || t === "StringSerializable")
    return "any";
  if (t === "ListStringSerializable")
    return "string[]";
  if (e === "Image")
    return l === "parameter" ? "Blob | File | Buffer" : "string";
  if (t === "FileSerializable")
    return n?.type === "array" ? l === "parameter" ? "(Blob | File | Buffer)[]" : "{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}[]" : l === "parameter" ? "Blob | File | Buffer" : "{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}";
  if (t === "GallerySerializable")
    return l === "parameter" ? "[(Blob | File | Buffer), (string | null)][]" : "[{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}, (string | null))][]";
}
function hl(n, e) {
  return e === "GallerySerializable" ? "array of [file, label] tuples" : e === "ListStringSerializable" ? "array of strings" : e === "FileSerializable" ? "array of files or single file" : n.description;
}
function fa(n, e, t) {
  const l = {
    named_endpoints: {},
    unnamed_endpoints: {}
  };
  for (const i in n) {
    const o = n[i];
    for (const s in o) {
      const a = e.dependencies[s] ? s : t[s.replace("/", "")], r = o[s];
      l[i][s] = {}, l[i][s].parameters = {}, l[i][s].returns = {}, l[i][s].type = e.dependencies[a].types, l[i][s].parameters = r.parameters.map(
        ({ label: u, component: f, type: _, serializer: d }) => ({
          label: u,
          component: f,
          type: dl(_, f, d, "parameter"),
          description: hl(_, d)
        })
      ), l[i][s].returns = r.returns.map(
        ({ label: u, component: f, type: _, serializer: d }) => ({
          label: u,
          component: f,
          type: dl(_, f, d, "return"),
          description: hl(_, d)
        })
      );
    }
  }
  return l;
}
async function ca(n, e) {
  try {
    return (await (await fetch(`https://huggingface.co/api/spaces/${n}/jwt`, {
      headers: {
        Authorization: `Bearer ${e}`
      }
    })).json()).token || !1;
  } catch (t) {
    return console.error(t), !1;
  }
}
function ml(n, e, t) {
  for (; t.length > 1; )
    n = n[t.shift()];
  n[t.shift()] = e;
}
async function An(n, e = void 0, t = [], l = !1, i = void 0) {
  if (Array.isArray(n)) {
    let o = [];
    return await Promise.all(
      n.map(async (s, a) => {
        var r;
        let u = t.slice();
        u.push(a);
        const f = await An(
          n[a],
          l ? ((r = i?.parameters[a]) == null ? void 0 : r.component) || void 0 : e,
          u,
          !1,
          i
        );
        o = o.concat(f);
      })
    ), o;
  } else {
    if (globalThis.Buffer && n instanceof globalThis.Buffer)
      return [
        {
          path: t,
          blob: e === "Image" ? !1 : new ki([n]),
          type: e
        }
      ];
    if (typeof n == "object") {
      let o = [];
      for (let s in n)
        if (n.hasOwnProperty(s)) {
          let a = t.slice();
          a.push(s), o = o.concat(
            await An(
              n[s],
              void 0,
              a,
              !1,
              i
            )
          );
        }
      return o;
    }
  }
  return [];
}
function _a(n, e) {
  var t, l, i, o;
  return !(((l = (t = e?.dependencies) == null ? void 0 : t[n]) == null ? void 0 : l.queue) === null ? e.enable_queue : (o = (i = e?.dependencies) == null ? void 0 : i[n]) != null && o.queue) || !1;
}
async function gl(n, e, t) {
  const l = {};
  if (t && (l.Authorization = `Bearer ${t}`), typeof window < "u" && window.gradio_config && location.origin !== "http://localhost:9876" && !window.gradio_config.dev_mode) {
    const i = window.gradio_config.root, o = window.gradio_config;
    return o.root = Ve(e, o.root, !1), { ...o, path: i };
  } else if (e) {
    let i = await n(`${e}/config`, {
      headers: l
    });
    if (i.status === 200) {
      const o = await i.json();
      return o.path = o.path ?? "", o.root = e, o;
    }
    throw new Error("Could not get config.");
  }
  throw new Error("No config or app endpoint found");
}
async function Pn(n, e, t) {
  let l = e === "subdomain" ? `https://huggingface.co/api/spaces/by-subdomain/${n}` : `https://huggingface.co/api/spaces/${n}`, i, o;
  try {
    if (i = await fetch(l), o = i.status, o !== 200)
      throw new Error();
    i = await i.json();
  } catch {
    t({
      status: "error",
      load_status: "error",
      message: "Could not get space status",
      detail: "NOT_FOUND"
    });
    return;
  }
  if (!i || o !== 200)
    return;
  const {
    runtime: { stage: s },
    id: a
  } = i;
  switch (s) {
    case "STOPPED":
    case "SLEEPING":
      t({
        status: "sleeping",
        load_status: "pending",
        message: "Space is asleep. Waking it up...",
        detail: s
      }), setTimeout(() => {
        Pn(n, e, t);
      }, 1e3);
      break;
    case "PAUSED":
      t({
        status: "paused",
        load_status: "error",
        message: "This space has been paused by the author. If you would like to try this demo, consider duplicating the space.",
        detail: s,
        discussions_enabled: await _l(a)
      });
      break;
    case "RUNNING":
    case "RUNNING_BUILDING":
      t({
        status: "running",
        load_status: "complete",
        message: "",
        detail: s
      });
      break;
    case "BUILDING":
      t({
        status: "building",
        load_status: "pending",
        message: "Space is building...",
        detail: s
      }), setTimeout(() => {
        Pn(n, e, t);
      }, 1e3);
      break;
    default:
      t({
        status: "space_error",
        load_status: "error",
        message: "This space is experiencing an issue.",
        detail: s,
        discussions_enabled: await _l(a)
      });
      break;
  }
}
function pl(n, e) {
  switch (n.msg) {
    case "send_data":
      return { type: "data" };
    case "send_hash":
      return { type: "hash" };
    case "queue_full":
      return {
        type: "update",
        status: {
          queue: !0,
          message: ra,
          stage: "error",
          code: n.code,
          success: n.success
        }
      };
    case "estimation":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: e || "pending",
          code: n.code,
          size: n.queue_size,
          position: n.rank,
          eta: n.rank_eta,
          success: n.success
        }
      };
    case "progress":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: "pending",
          code: n.code,
          progress_data: n.progress_data,
          success: n.success
        }
      };
    case "log":
      return { type: "log", data: n };
    case "process_generating":
      return {
        type: "generating",
        status: {
          queue: !0,
          message: n.success ? null : n.output.error,
          stage: n.success ? "generating" : "error",
          code: n.code,
          progress_data: n.progress_data,
          eta: n.average_duration
        },
        data: n.success ? n.output : null
      };
    case "process_completed":
      return "error" in n.output ? {
        type: "update",
        status: {
          queue: !0,
          message: n.output.error,
          stage: "error",
          code: n.code,
          success: n.success
        }
      } : {
        type: "complete",
        status: {
          queue: !0,
          message: n.success ? void 0 : n.output.error,
          stage: n.success ? "complete" : "error",
          code: n.code,
          progress_data: n.progress_data,
          eta: n.output.average_duration
        },
        data: n.success ? n.output : null
      };
    case "process_starts":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: "pending",
          code: n.code,
          size: n.rank,
          position: 0,
          success: n.success
        }
      };
  }
  return { type: "none", status: { stage: "error", queue: !0 } };
}
const {
  SvelteComponent: da,
  append: ue,
  attr: Ke,
  detach: yi,
  element: Qe,
  init: ha,
  insert: qi,
  noop: bl,
  safe_not_equal: ma,
  set_data: Gt,
  set_style: bn,
  space: Rn,
  text: it,
  toggle_class: wl
} = window.__gradio__svelte__internal, { onMount: ga, createEventDispatcher: pa } = window.__gradio__svelte__internal;
function vl(n) {
  let e, t, l, i, o = qt(
    /*current_file_upload*/
    n[2]
  ) + "", s, a, r, u, f = (
    /*current_file_upload*/
    n[2].orig_name + ""
  ), _;
  return {
    c() {
      e = Qe("div"), t = Qe("span"), l = Qe("div"), i = Qe("progress"), s = it(o), r = Rn(), u = Qe("span"), _ = it(f), bn(i, "visibility", "hidden"), bn(i, "height", "0"), bn(i, "width", "0"), i.value = a = qt(
        /*current_file_upload*/
        n[2]
      ), Ke(i, "max", "100"), Ke(i, "class", "svelte-12ckl9l"), Ke(l, "class", "progress-bar svelte-12ckl9l"), Ke(u, "class", "file-name svelte-12ckl9l"), Ke(e, "class", "file svelte-12ckl9l");
    },
    m(d, c) {
      qi(d, e, c), ue(e, t), ue(t, l), ue(l, i), ue(i, s), ue(e, r), ue(e, u), ue(u, _);
    },
    p(d, c) {
      c & /*current_file_upload*/
      4 && o !== (o = qt(
        /*current_file_upload*/
        d[2]
      ) + "") && Gt(s, o), c & /*current_file_upload*/
      4 && a !== (a = qt(
        /*current_file_upload*/
        d[2]
      )) && (i.value = a), c & /*current_file_upload*/
      4 && f !== (f = /*current_file_upload*/
      d[2].orig_name + "") && Gt(_, f);
    },
    d(d) {
      d && yi(e);
    }
  };
}
function ba(n) {
  let e, t, l, i = (
    /*files_with_progress*/
    n[0].length + ""
  ), o, s, a = (
    /*files_with_progress*/
    n[0].length > 1 ? "files" : "file"
  ), r, u, f, _ = (
    /*current_file_upload*/
    n[2] && vl(n)
  );
  return {
    c() {
      e = Qe("div"), t = Qe("span"), l = it("Uploading "), o = it(i), s = Rn(), r = it(a), u = it("..."), f = Rn(), _ && _.c(), Ke(t, "class", "uploading svelte-12ckl9l"), Ke(e, "class", "wrap svelte-12ckl9l"), wl(
        e,
        "progress",
        /*progress*/
        n[1]
      );
    },
    m(d, c) {
      qi(d, e, c), ue(e, t), ue(t, l), ue(t, o), ue(t, s), ue(t, r), ue(t, u), ue(e, f), _ && _.m(e, null);
    },
    p(d, [c]) {
      c & /*files_with_progress*/
      1 && i !== (i = /*files_with_progress*/
      d[0].length + "") && Gt(o, i), c & /*files_with_progress*/
      1 && a !== (a = /*files_with_progress*/
      d[0].length > 1 ? "files" : "file") && Gt(r, a), /*current_file_upload*/
      d[2] ? _ ? _.p(d, c) : (_ = vl(d), _.c(), _.m(e, null)) : _ && (_.d(1), _ = null), c & /*progress*/
      2 && wl(
        e,
        "progress",
        /*progress*/
        d[1]
      );
    },
    i: bl,
    o: bl,
    d(d) {
      d && yi(e), _ && _.d();
    }
  };
}
function qt(n) {
  return n.progress * 100 / (n.size || 0) || 0;
}
function wa(n) {
  let e = 0;
  return n.forEach((t) => {
    e += qt(t);
  }), document.documentElement.style.setProperty("--upload-progress-width", (e / n.length).toFixed(2) + "%"), e / n.length;
}
function va(n, e, t) {
  var l = this && this.__awaiter || function(c, m, p, C) {
    function b(q) {
      return q instanceof p ? q : new p(function(g) {
        g(q);
      });
    }
    return new (p || (p = Promise))(function(q, g) {
      function w(L) {
        try {
          T(C.next(L));
        } catch (R) {
          g(R);
        }
      }
      function E(L) {
        try {
          T(C.throw(L));
        } catch (R) {
          g(R);
        }
      }
      function T(L) {
        L.done ? q(L.value) : b(L.value).then(w, E);
      }
      T((C = C.apply(c, m || [])).next());
    });
  };
  let { upload_id: i } = e, { root: o } = e, { files: s } = e, a, r = !1, u, f = s.map((c) => Object.assign(Object.assign({}, c), { progress: 0 }));
  const _ = pa();
  function d(c, m) {
    t(0, f = f.map((p) => (p.orig_name === c && (p.progress += m), p)));
  }
  return ga(() => {
    a = new EventSource(`${o}/upload_progress?upload_id=${i}`), a.onmessage = function(c) {
      return l(this, void 0, void 0, function* () {
        const m = JSON.parse(c.data);
        r || t(1, r = !0), m.msg === "done" ? (a.close(), _("done")) : (t(2, u = m), d(m.orig_name, m.chunk_size));
      });
    };
  }), n.$$set = (c) => {
    "upload_id" in c && t(3, i = c.upload_id), "root" in c && t(4, o = c.root), "files" in c && t(5, s = c.files);
  }, n.$$.update = () => {
    n.$$.dirty & /*files_with_progress*/
    1 && wa(f);
  }, [f, r, u, i, o, s];
}
class ka extends da {
  constructor(e) {
    super(), ha(this, e, va, ba, ma, { upload_id: 3, root: 4, files: 5 });
  }
}
const {
  SvelteComponent: ya,
  append: kl,
  attr: be,
  binding_callbacks: qa,
  bubble: Je,
  check_outros: Sa,
  create_component: Ca,
  create_slot: Ea,
  destroy_component: za,
  detach: Si,
  element: yl,
  empty: Da,
  get_all_dirty_from_scope: Ma,
  get_slot_changes: Na,
  group_outros: Ia,
  init: Ba,
  insert: Ci,
  listen: we,
  mount_component: ja,
  prevent_default: Xe,
  run_all: Ta,
  safe_not_equal: La,
  set_style: ql,
  space: Fa,
  stop_propagation: Ye,
  toggle_class: We,
  transition_in: Ht,
  transition_out: Jt,
  update_slot_base: Oa
} = window.__gradio__svelte__internal, { createEventDispatcher: Aa, tick: Pa, getContext: Ra } = window.__gradio__svelte__internal;
function Ua(n) {
  let e, t, l, i, o, s, a, r, u, f;
  const _ = (
    /*#slots*/
    n[21].default
  ), d = Ea(
    _,
    n,
    /*$$scope*/
    n[20],
    null
  );
  return {
    c() {
      e = yl("button"), d && d.c(), t = Fa(), l = yl("input"), be(l, "aria-label", "file upload"), be(l, "type", "file"), be(
        l,
        "accept",
        /*filetype*/
        n[1]
      ), l.multiple = i = /*file_count*/
      n[5] === "multiple" || void 0, be(l, "webkitdirectory", o = /*file_count*/
      n[5] === "directory" || void 0), be(l, "mozdirectory", s = /*file_count*/
      n[5] === "directory" || void 0), be(l, "class", "svelte-1aq8tno"), be(e, "tabindex", a = /*hidden*/
      n[7] ? -1 : 0), be(e, "class", "svelte-1aq8tno"), We(
        e,
        "hidden",
        /*hidden*/
        n[7]
      ), We(
        e,
        "center",
        /*center*/
        n[3]
      ), We(
        e,
        "boundedheight",
        /*boundedheight*/
        n[2]
      ), We(
        e,
        "flex",
        /*flex*/
        n[4]
      ), ql(
        e,
        "height",
        /*include_sources*/
        n[8] ? "calc(100% - 40px" : "100%"
      );
    },
    m(c, m) {
      Ci(c, e, m), d && d.m(e, null), kl(e, t), kl(e, l), n[29](l), r = !0, u || (f = [
        we(
          l,
          "change",
          /*load_files_from_upload*/
          n[14]
        ),
        we(e, "drag", Ye(Xe(
          /*drag_handler*/
          n[22]
        ))),
        we(e, "dragstart", Ye(Xe(
          /*dragstart_handler*/
          n[23]
        ))),
        we(e, "dragend", Ye(Xe(
          /*dragend_handler*/
          n[24]
        ))),
        we(e, "dragover", Ye(Xe(
          /*dragover_handler*/
          n[25]
        ))),
        we(e, "dragenter", Ye(Xe(
          /*dragenter_handler*/
          n[26]
        ))),
        we(e, "dragleave", Ye(Xe(
          /*dragleave_handler*/
          n[27]
        ))),
        we(e, "drop", Ye(Xe(
          /*drop_handler*/
          n[28]
        ))),
        we(
          e,
          "click",
          /*open_file_upload*/
          n[9]
        ),
        we(
          e,
          "drop",
          /*loadFilesFromDrop*/
          n[15]
        ),
        we(
          e,
          "dragenter",
          /*updateDragging*/
          n[13]
        ),
        we(
          e,
          "dragleave",
          /*updateDragging*/
          n[13]
        )
      ], u = !0);
    },
    p(c, m) {
      d && d.p && (!r || m[0] & /*$$scope*/
      1048576) && Oa(
        d,
        _,
        c,
        /*$$scope*/
        c[20],
        r ? Na(
          _,
          /*$$scope*/
          c[20],
          m,
          null
        ) : Ma(
          /*$$scope*/
          c[20]
        ),
        null
      ), (!r || m[0] & /*filetype*/
      2) && be(
        l,
        "accept",
        /*filetype*/
        c[1]
      ), (!r || m[0] & /*file_count*/
      32 && i !== (i = /*file_count*/
      c[5] === "multiple" || void 0)) && (l.multiple = i), (!r || m[0] & /*file_count*/
      32 && o !== (o = /*file_count*/
      c[5] === "directory" || void 0)) && be(l, "webkitdirectory", o), (!r || m[0] & /*file_count*/
      32 && s !== (s = /*file_count*/
      c[5] === "directory" || void 0)) && be(l, "mozdirectory", s), (!r || m[0] & /*hidden*/
      128 && a !== (a = /*hidden*/
      c[7] ? -1 : 0)) && be(e, "tabindex", a), (!r || m[0] & /*hidden*/
      128) && We(
        e,
        "hidden",
        /*hidden*/
        c[7]
      ), (!r || m[0] & /*center*/
      8) && We(
        e,
        "center",
        /*center*/
        c[3]
      ), (!r || m[0] & /*boundedheight*/
      4) && We(
        e,
        "boundedheight",
        /*boundedheight*/
        c[2]
      ), (!r || m[0] & /*flex*/
      16) && We(
        e,
        "flex",
        /*flex*/
        c[4]
      ), m[0] & /*include_sources*/
      256 && ql(
        e,
        "height",
        /*include_sources*/
        c[8] ? "calc(100% - 40px" : "100%"
      );
    },
    i(c) {
      r || (Ht(d, c), r = !0);
    },
    o(c) {
      Jt(d, c), r = !1;
    },
    d(c) {
      c && Si(e), d && d.d(c), n[29](null), u = !1, Ta(f);
    }
  };
}
function Za(n) {
  let e, t;
  return e = new ka({
    props: {
      root: (
        /*root*/
        n[6]
      ),
      upload_id: (
        /*upload_id*/
        n[10]
      ),
      files: (
        /*file_data*/
        n[11]
      )
    }
  }), {
    c() {
      Ca(e.$$.fragment);
    },
    m(l, i) {
      ja(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*root*/
      64 && (o.root = /*root*/
      l[6]), i[0] & /*upload_id*/
      1024 && (o.upload_id = /*upload_id*/
      l[10]), i[0] & /*file_data*/
      2048 && (o.files = /*file_data*/
      l[11]), e.$set(o);
    },
    i(l) {
      t || (Ht(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Jt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      za(e, l);
    }
  };
}
function Wa(n) {
  let e, t, l, i;
  const o = [Za, Ua], s = [];
  function a(r, u) {
    return (
      /*uploading*/
      r[0] ? 0 : 1
    );
  }
  return e = a(n), t = s[e] = o[e](n), {
    c() {
      t.c(), l = Da();
    },
    m(r, u) {
      s[e].m(r, u), Ci(r, l, u), i = !0;
    },
    p(r, u) {
      let f = e;
      e = a(r), e === f ? s[e].p(r, u) : (Ia(), Jt(s[f], 1, 1, () => {
        s[f] = null;
      }), Sa(), t = s[e], t ? t.p(r, u) : (t = s[e] = o[e](r), t.c()), Ht(t, 1), t.m(l.parentNode, l));
    },
    i(r) {
      i || (Ht(t), i = !0);
    },
    o(r) {
      Jt(t), i = !1;
    },
    d(r) {
      r && Si(l), s[e].d(r);
    }
  };
}
function Va(n, e) {
  return !n || n === "*" ? !0 : n.endsWith("/*") ? e.startsWith(n.slice(0, -1)) : n === e;
}
function Ga(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  var o = this && this.__awaiter || function(y, k, h, D) {
    function N(A) {
      return A instanceof h ? A : new h(function(V) {
        V(A);
      });
    }
    return new (h || (h = Promise))(function(A, V) {
      function U(W) {
        try {
          v(D.next(W));
        } catch (ee) {
          V(ee);
        }
      }
      function j(W) {
        try {
          v(D.throw(W));
        } catch (ee) {
          V(ee);
        }
      }
      function v(W) {
        W.done ? A(W.value) : N(W.value).then(U, j);
      }
      v((D = D.apply(y, k || [])).next());
    });
  };
  let { filetype: s = null } = e, { dragging: a = !1 } = e, { boundedheight: r = !0 } = e, { center: u = !0 } = e, { flex: f = !0 } = e, { file_count: _ = "single" } = e, { disable_click: d = !1 } = e, { root: c } = e, { hidden: m = !1 } = e, { format: p = "file" } = e, { include_sources: C = !1 } = e, { uploading: b = !1 } = e, q, g;
  const w = Ra("upload_files");
  let E;
  const T = Aa();
  function L() {
    t(16, a = !a);
  }
  function R() {
    d || (t(12, E.value = "", E), E.click());
  }
  function x(y) {
    return o(this, void 0, void 0, function* () {
      yield Pa(), t(10, q = Math.random().toString(36).substring(2, 15)), t(0, b = !0);
      const k = yield oa(y, c, q, w);
      return T("load", _ === "single" ? k?.[0] : k), t(0, b = !1), k || [];
    });
  }
  function F(y) {
    return o(this, void 0, void 0, function* () {
      if (!y.length)
        return;
      let k = y.map((h) => new File([h], h.name));
      return t(11, g = yield sa(k)), yield x(g);
    });
  }
  function ie(y) {
    return o(this, void 0, void 0, function* () {
      const k = y.target;
      if (k.files)
        if (p != "blob")
          yield F(Array.from(k.files));
        else {
          if (_ === "single") {
            T("load", k.files[0]);
            return;
          }
          T("load", k.files);
        }
    });
  }
  function ae(y) {
    return o(this, void 0, void 0, function* () {
      var k;
      if (t(16, a = !1), !(!((k = y.dataTransfer) === null || k === void 0) && k.files)) return;
      const h = Array.from(y.dataTransfer.files).filter((D) => s?.split(",").some((N) => Va(N, D.type)) ? !0 : (T("error", `Invalid file type only ${s} allowed.`), !1));
      yield F(h);
    });
  }
  function ne(y) {
    Je.call(this, n, y);
  }
  function M(y) {
    Je.call(this, n, y);
  }
  function O(y) {
    Je.call(this, n, y);
  }
  function H(y) {
    Je.call(this, n, y);
  }
  function Z(y) {
    Je.call(this, n, y);
  }
  function z(y) {
    Je.call(this, n, y);
  }
  function G(y) {
    Je.call(this, n, y);
  }
  function S(y) {
    qa[y ? "unshift" : "push"](() => {
      E = y, t(12, E);
    });
  }
  return n.$$set = (y) => {
    "filetype" in y && t(1, s = y.filetype), "dragging" in y && t(16, a = y.dragging), "boundedheight" in y && t(2, r = y.boundedheight), "center" in y && t(3, u = y.center), "flex" in y && t(4, f = y.flex), "file_count" in y && t(5, _ = y.file_count), "disable_click" in y && t(17, d = y.disable_click), "root" in y && t(6, c = y.root), "hidden" in y && t(7, m = y.hidden), "format" in y && t(18, p = y.format), "include_sources" in y && t(8, C = y.include_sources), "uploading" in y && t(0, b = y.uploading), "$$scope" in y && t(20, i = y.$$scope);
  }, [
    b,
    s,
    r,
    u,
    f,
    _,
    c,
    m,
    C,
    R,
    q,
    g,
    E,
    L,
    ie,
    ae,
    a,
    d,
    p,
    F,
    i,
    l,
    ne,
    M,
    O,
    H,
    Z,
    z,
    G,
    S
  ];
}
class Ha extends ya {
  constructor(e) {
    super(), Ba(
      this,
      e,
      Ga,
      Wa,
      La,
      {
        filetype: 1,
        dragging: 16,
        boundedheight: 2,
        center: 3,
        flex: 4,
        file_count: 5,
        disable_click: 17,
        root: 6,
        hidden: 7,
        format: 18,
        include_sources: 8,
        uploading: 0,
        open_file_upload: 9,
        load_files: 19
      },
      null,
      [-1, -1]
    );
  }
  get open_file_upload() {
    return this.$$.ctx[9];
  }
  get load_files() {
    return this.$$.ctx[19];
  }
}
const {
  SvelteComponent: Ja,
  append: Sl,
  attr: Xa,
  create_component: wn,
  destroy_component: vn,
  detach: Ya,
  element: Ka,
  init: Qa,
  insert: $a,
  mount_component: kn,
  noop: xa,
  safe_not_equal: eu,
  space: Cl,
  transition_in: yn,
  transition_out: qn
} = window.__gradio__svelte__internal, { createEventDispatcher: tu } = window.__gradio__svelte__internal;
function nu(n) {
  let e, t, l, i, o, s, a;
  return t = new rt({
    props: { Icon: Ys, label: "Remove Last Box" }
  }), t.$on(
    "click",
    /*click_handler*/
    n[1]
  ), i = new rt({
    props: { Icon: Ds, label: "Remove All boxes" }
  }), i.$on(
    "click",
    /*click_handler_1*/
    n[2]
  ), s = new rt({
    props: { Icon: os, label: "Remove Image" }
  }), s.$on(
    "click",
    /*click_handler_2*/
    n[3]
  ), {
    c() {
      e = Ka("div"), wn(t.$$.fragment), l = Cl(), wn(i.$$.fragment), o = Cl(), wn(s.$$.fragment), Xa(e, "class", "svelte-1o7cyxy");
    },
    m(r, u) {
      $a(r, e, u), kn(t, e, null), Sl(e, l), kn(i, e, null), Sl(e, o), kn(s, e, null), a = !0;
    },
    p: xa,
    i(r) {
      a || (yn(t.$$.fragment, r), yn(i.$$.fragment, r), yn(s.$$.fragment, r), a = !0);
    },
    o(r) {
      qn(t.$$.fragment, r), qn(i.$$.fragment, r), qn(s.$$.fragment, r), a = !1;
    },
    d(r) {
      r && Ya(e), vn(t), vn(i), vn(s);
    }
  };
}
function lu(n) {
  const e = tu();
  return [e, (o) => {
    e("remove_box"), o.stopPropagation();
  }, (o) => {
    e("remove_boxes"), o.stopPropagation();
  }, (o) => {
    e("remove_image"), o.stopPropagation();
  }];
}
class iu extends Ja {
  constructor(e) {
    super(), Qa(this, e, lu, nu, eu, {});
  }
}
const {
  SvelteComponent: ou,
  append: su,
  attr: El,
  binding_callbacks: zl,
  bubble: ru,
  detach: au,
  element: Dl,
  flush: Ft,
  init: uu,
  insert: fu,
  listen: Ne,
  noop: Sn,
  run_all: cu,
  safe_not_equal: _u,
  set_style: du,
  stop_propagation: hu
} = window.__gradio__svelte__internal, { createEventDispatcher: mu, onDestroy: gu, onMount: pu, tick: bu } = window.__gradio__svelte__internal;
function wu(n) {
  let e, t, l, i;
  return {
    c() {
      e = Dl("div"), t = Dl("canvas"), du(t, "z-index", "15"), El(t, "class", "svelte-1mnpmgt"), El(e, "class", "wrap svelte-1mnpmgt");
    },
    m(o, s) {
      fu(o, e, s), su(e, t), n[13](t), n[14](e), l || (i = [
        Ne(
          t,
          "mousedown",
          /*handle_draw_start*/
          n[2]
        ),
        Ne(
          t,
          "mousemove",
          /*handle_draw_move*/
          n[3]
        ),
        Ne(
          t,
          "mouseout",
          /*handle_draw_move*/
          n[3]
        ),
        Ne(
          t,
          "mouseup",
          /*handle_draw_end*/
          n[4]
        ),
        Ne(
          t,
          "touchstart",
          /*handle_draw_start*/
          n[2]
        ),
        Ne(
          t,
          "touchmove",
          /*handle_draw_move*/
          n[3]
        ),
        Ne(
          t,
          "touchend",
          /*handle_draw_end*/
          n[4]
        ),
        Ne(
          t,
          "touchcancel",
          /*handle_draw_end*/
          n[4]
        ),
        Ne(
          t,
          "blur",
          /*handle_draw_end*/
          n[4]
        ),
        Ne(t, "click", hu(
          /*click_handler*/
          n[12]
        ))
      ], l = !0);
    },
    p: Sn,
    i: Sn,
    o: Sn,
    d(o) {
      o && au(e), n[13](null), n[14](null), l = !1, cu(i);
    }
  };
}
function vu(n, e, t) {
  var l = this && this.__awaiter || function(k, h, D, N) {
    function A(V) {
      return V instanceof D ? V : new D(function(U) {
        U(V);
      });
    }
    return new (D || (D = Promise))(function(V, U) {
      function j(ee) {
        try {
          W(N.next(ee));
        } catch (re) {
          U(re);
        }
      }
      function v(ee) {
        try {
          W(N.throw(ee));
        } catch (re) {
          U(re);
        }
      }
      function W(ee) {
        ee.done ? V(ee.value) : A(ee.value).then(j, v);
      }
      W((N = N.apply(k, h || [])).next());
    });
  };
  const i = mu();
  let { width: o = 0 } = e, { height: s = 0 } = e, { natural_width: a = 0 } = e, { natural_height: r = 0 } = e, u = [], f = [], _, d, c, m = !1, p, C, b, q, g, w = 0, E = 0, T;
  function L(k) {
    return l(this, void 0, void 0, function* () {
      yield bu(), t(1, d.width = k.width, d), t(1, d.height = k.height, d), t(1, d.style.width = `${k.width}px`, d), t(1, d.style.height = `${k.height}px`, d), t(1, d.style.marginTop = `-${k.height}px`, d);
    });
  }
  function R() {
    return l(this, void 0, void 0, function* () {
      o === w && s === E || (yield L({ width: o, height: s }), H(), setTimeout(
        () => {
          E = s, w = o;
        },
        100
      ), x());
    });
  }
  function x() {
    return u = [], f = [], H(), i("change", f), !0;
  }
  function F() {
    return u.pop(), f.pop(), H(), i("change", f), !0;
  }
  pu(() => l(void 0, void 0, void 0, function* () {
    c = d.getContext("2d"), c && (c.lineJoin = "round", c.lineCap = "round", c.strokeStyle = "#000"), T = new ResizeObserver(() => {
      R();
    }), T.observe(_), O(), x();
  })), gu(() => {
    T.unobserve(_);
  });
  function ie(k) {
    const h = d.getBoundingClientRect();
    let D, N;
    if (k instanceof MouseEvent)
      D = k.clientX, N = k.clientY;
    else if (k instanceof TouchEvent)
      D = k.changedTouches[0].clientX, N = k.changedTouches[0].clientY;
    else
      return { x: C, y: b };
    return {
      x: D - h.left,
      y: N - h.top
    };
  }
  function ae(k) {
    k.preventDefault(), m = !0, p = 0, k instanceof MouseEvent && (p = k.button);
    const { x: h, y: D } = ie(k);
    C = h, b = D;
  }
  function ne(k) {
    k.preventDefault();
    const { x: h, y: D } = ie(k);
    q = h, g = D;
  }
  function M(k) {
    if (k.preventDefault(), m) {
      const { x: h, y: D } = ie(k);
      let N = Math.min(C, h), A = Math.min(b, D), V = Math.max(C, h), U = Math.max(b, D);
      u.push([N, A, V, U]);
      let j = a / o, v = r / s, W = N == V && A == U;
      f.push([
        Math.round(N * j),
        Math.round(A * v),
        W ? p == 0 ? 1 : 0 : 2,
        W ? 0 : Math.round(
          V * j
        ),
        W ? 0 : Math.round(U * v),
        W ? 4 : 3
      ]), i("change", f);
    }
    m = !1;
  }
  function O() {
    H(), window.requestAnimationFrame(() => {
      O();
    });
  }
  function H() {
    if (c)
      if (c.clearRect(0, 0, o, s), m && q != C && b != g) {
        let k = u.slice();
        k.push([C, b, q, g]), Z(k), z(u);
      } else
        Z(u), z(u);
  }
  function Z(k) {
    c && (c.fillStyle = "rgba(0, 255, 255, 0.3)", c.beginPath(), k.forEach((h) => {
      h[0] != h[2] && h[1] != h[3] && c.rect(h[0], h[1], h[2] - h[0], h[3] - h[1]);
    }), c.fill(), c.stroke());
  }
  function z(k) {
    c && (c.beginPath(), c.fillStyle = "rgba(0, 255, 255, 1.0)", k.forEach((h, D) => {
      if (f[D][2] == 1) {
        let N = Math.sqrt(o * s) * 0.01;
        c.moveTo(h[0] + N, h[1]), c.arc(h[0], h[1], N, 0, 2 * Math.PI, !1);
      }
    }), c.fill(), c.stroke(), c.beginPath(), c.fillStyle = "rgba(255, 192, 203, 1.0)", k.forEach((h, D) => {
      if (f[D][2] == 0) {
        let N = Math.sqrt(o * s) * 0.01;
        c.moveTo(h[0] + N, h[1]), c.arc(h[0], h[1], N, 0, 2 * Math.PI, !1);
      }
    }), c.fill(), c.stroke());
  }
  function G(k) {
    ru.call(this, n, k);
  }
  function S(k) {
    zl[k ? "unshift" : "push"](() => {
      d = k, t(1, d);
    });
  }
  function y(k) {
    zl[k ? "unshift" : "push"](() => {
      _ = k, t(0, _);
    });
  }
  return n.$$set = (k) => {
    "width" in k && t(5, o = k.width), "height" in k && t(6, s = k.height), "natural_width" in k && t(7, a = k.natural_width), "natural_height" in k && t(8, r = k.natural_height);
  }, [
    _,
    d,
    ae,
    ne,
    M,
    o,
    s,
    a,
    r,
    R,
    x,
    F,
    G,
    S,
    y
  ];
}
class ku extends ou {
  constructor(e) {
    super(), uu(
      this,
      e,
      vu,
      wu,
      _u,
      {
        width: 5,
        height: 6,
        natural_width: 7,
        natural_height: 8,
        resize_canvas: 9,
        clear: 10,
        undo: 11
      },
      null,
      [-1, -1]
    );
  }
  get width() {
    return this.$$.ctx[5];
  }
  set width(e) {
    this.$$set({ width: e }), Ft();
  }
  get height() {
    return this.$$.ctx[6];
  }
  set height(e) {
    this.$$set({ height: e }), Ft();
  }
  get natural_width() {
    return this.$$.ctx[7];
  }
  set natural_width(e) {
    this.$$set({ natural_width: e }), Ft();
  }
  get natural_height() {
    return this.$$.ctx[8];
  }
  set natural_height(e) {
    this.$$set({ natural_height: e }), Ft();
  }
  get resize_canvas() {
    return this.$$.ctx[9];
  }
  get clear() {
    return this.$$.ctx[10];
  }
  get undo() {
    return this.$$.ctx[11];
  }
}
const {
  SvelteComponent: yu,
  add_flush_callback: Ml,
  append: Ot,
  attr: Ge,
  bind: Nl,
  binding_callbacks: Xt,
  bubble: qu,
  check_outros: Ct,
  create_component: _t,
  create_slot: Su,
  destroy_component: dt,
  destroy_each: Cu,
  detach: ht,
  element: Un,
  empty: Ei,
  ensure_array_like: Il,
  get_all_dirty_from_scope: Eu,
  get_slot_changes: zu,
  group_outros: Et,
  init: Du,
  insert: mt,
  listen: Bl,
  mount_component: gt,
  noop: Mu,
  run_all: Nu,
  safe_not_equal: Iu,
  space: St,
  src_url_equal: jl,
  transition_in: Y,
  transition_out: oe,
  update_slot_base: Bu
} = window.__gradio__svelte__internal, { createEventDispatcher: ju } = window.__gradio__svelte__internal;
function Tl(n, e, t) {
  const l = n.slice();
  return l[33] = e[t], l;
}
function Ll(n) {
  let e, t;
  return e = new iu({}), e.$on(
    "remove_box",
    /*remove_box_handler*/
    n[22]
  ), e.$on(
    "remove_boxes",
    /*remove_boxes_handler*/
    n[23]
  ), e.$on(
    "remove_image",
    /*remove_image_handler*/
    n[24]
  ), {
    c() {
      _t(e.$$.fragment);
    },
    m(l, i) {
      gt(e, l, i), t = !0;
    },
    p: Mu,
    i(l) {
      t || (Y(e.$$.fragment, l), t = !0);
    },
    o(l) {
      oe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      dt(e, l);
    }
  };
}
function Fl(n) {
  let e;
  const t = (
    /*#slots*/
    n[21].default
  ), l = Su(
    t,
    n,
    /*$$scope*/
    n[31],
    null
  );
  return {
    c() {
      l && l.c();
    },
    m(i, o) {
      l && l.m(i, o), e = !0;
    },
    p(i, o) {
      l && l.p && (!e || o[1] & /*$$scope*/
      1) && Bu(
        l,
        t,
        i,
        /*$$scope*/
        i[31],
        e ? zu(
          t,
          /*$$scope*/
          i[31],
          o,
          null
        ) : Eu(
          /*$$scope*/
          i[31]
        ),
        null
      );
    },
    i(i) {
      e || (Y(l, i), e = !0);
    },
    o(i) {
      oe(l, i), e = !1;
    },
    d(i) {
      l && l.d(i);
    }
  };
}
function Tu(n) {
  let e, t, l = (
    /*value*/
    n[0] === null && !/*active_tool*/
    n[6] && Fl(n)
  );
  return {
    c() {
      l && l.c(), e = Ei();
    },
    m(i, o) {
      l && l.m(i, o), mt(i, e, o), t = !0;
    },
    p(i, o) {
      /*value*/
      i[0] === null && !/*active_tool*/
      i[6] ? l ? (l.p(i, o), o[0] & /*value, active_tool*/
      65 && Y(l, 1)) : (l = Fl(i), l.c(), Y(l, 1), l.m(e.parentNode, e)) : l && (Et(), oe(l, 1, 1, () => {
        l = null;
      }), Ct());
    },
    i(i) {
      t || (Y(l), t = !0);
    },
    o(i) {
      oe(l), t = !1;
    },
    d(i) {
      i && ht(e), l && l.d(i);
    }
  };
}
function Ol(n) {
  let e, t, l, i, o, s, a, r, u = {};
  return o = new ku({ props: u }), n[29](o), o.$on(
    "change",
    /*handle_points_change*/
    n[14]
  ), {
    c() {
      e = Un("img"), i = St(), _t(o.$$.fragment), jl(e.src, t = /*value*/
      n[0].url) || Ge(e, "src", t), Ge(e, "alt", l = /*value*/
      n[0].alt_text), Ge(e, "class", "svelte-1qm7xww");
    },
    m(f, _) {
      mt(f, e, _), mt(f, i, _), gt(o, f, _), s = !0, a || (r = [
        Bl(
          e,
          "click",
          /*handle_click*/
          n[16]
        ),
        Bl(
          e,
          "load",
          /*handle_image_load*/
          n[13]
        )
      ], a = !0);
    },
    p(f, _) {
      (!s || _[0] & /*value*/
      1 && !jl(e.src, t = /*value*/
      f[0].url)) && Ge(e, "src", t), (!s || _[0] & /*value*/
      1 && l !== (l = /*value*/
      f[0].alt_text)) && Ge(e, "alt", l);
      const d = {};
      o.$set(d);
    },
    i(f) {
      s || (Y(o.$$.fragment, f), s = !0);
    },
    o(f) {
      oe(o.$$.fragment, f), s = !1;
    },
    d(f) {
      f && (ht(e), ht(i)), n[29](null), dt(o, f), a = !1, Nu(r);
    }
  };
}
function Al(n) {
  let e, t;
  return e = new Rr({
    props: {
      show_border: !/*value*/
      n[0]?.url,
      $$slots: { default: [Lu] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      _t(e.$$.fragment);
    },
    m(l, i) {
      gt(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*value*/
      1 && (o.show_border = !/*value*/
      l[0]?.url), i[0] & /*sources_list*/
      2048 | i[1] & /*$$scope*/
      1 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (Y(e.$$.fragment, l), t = !0);
    },
    o(l) {
      oe(e.$$.fragment, l), t = !1;
    },
    d(l) {
      dt(e, l);
    }
  };
}
function Pl(n) {
  let e, t;
  function l() {
    return (
      /*click_handler*/
      n[30](
        /*source*/
        n[33]
      )
    );
  }
  return e = new rt({
    props: {
      Icon: (
        /*sources_meta*/
        n[17][
          /*source*/
          n[33]
        ].icon
      ),
      size: "large",
      label: (
        /*source*/
        n[33] + "-image-toolbar-btn"
      ),
      padded: !1
    }
  }), e.$on("click", l), {
    c() {
      _t(e.$$.fragment);
    },
    m(i, o) {
      gt(e, i, o), t = !0;
    },
    p(i, o) {
      n = i;
      const s = {};
      o[0] & /*sources_list*/
      2048 && (s.Icon = /*sources_meta*/
      n[17][
        /*source*/
        n[33]
      ].icon), o[0] & /*sources_list*/
      2048 && (s.label = /*source*/
      n[33] + "-image-toolbar-btn"), e.$set(s);
    },
    i(i) {
      t || (Y(e.$$.fragment, i), t = !0);
    },
    o(i) {
      oe(e.$$.fragment, i), t = !1;
    },
    d(i) {
      dt(e, i);
    }
  };
}
function Lu(n) {
  let e, t, l = Il(
    /*sources_list*/
    n[11]
  ), i = [];
  for (let s = 0; s < l.length; s += 1)
    i[s] = Pl(Tl(n, l, s));
  const o = (s) => oe(i[s], 1, 1, () => {
    i[s] = null;
  });
  return {
    c() {
      for (let s = 0; s < i.length; s += 1)
        i[s].c();
      e = Ei();
    },
    m(s, a) {
      for (let r = 0; r < i.length; r += 1)
        i[r] && i[r].m(s, a);
      mt(s, e, a), t = !0;
    },
    p(s, a) {
      if (a[0] & /*sources_meta, sources_list, handle_toolbar*/
      395264) {
        l = Il(
          /*sources_list*/
          s[11]
        );
        let r;
        for (r = 0; r < l.length; r += 1) {
          const u = Tl(s, l, r);
          i[r] ? (i[r].p(u, a), Y(i[r], 1)) : (i[r] = Pl(u), i[r].c(), Y(i[r], 1), i[r].m(e.parentNode, e));
        }
        for (Et(), r = l.length; r < i.length; r += 1)
          o(r);
        Ct();
      }
    },
    i(s) {
      if (!t) {
        for (let a = 0; a < l.length; a += 1)
          Y(i[a]);
        t = !0;
      }
    },
    o(s) {
      i = i.filter(Boolean);
      for (let a = 0; a < i.length; a += 1)
        oe(i[a]);
      t = !1;
    },
    d(s) {
      s && ht(e), Cu(i, s);
    }
  };
}
function Fu(n) {
  let e, t, l, i, o, s, a, r, u, f, _ = (
    /*sources*/
    n[3].length > 1 || /*sources*/
    n[3].includes("clipboard")
  ), d;
  e = new hi({
    props: {
      show_label: (
        /*show_label*/
        n[2]
      ),
      Icon: Kt,
      label: (
        /*label*/
        n[1] || "Image"
      )
    }
  });
  let c = (
    /*value*/
    n[0]?.url && Ll(n)
  );
  function m(g) {
    n[26](g);
  }
  function p(g) {
    n[27](g);
  }
  let C = {
    hidden: (
      /*value*/
      n[0] !== null || /*active_tool*/
      n[6] === "webcam"
    ),
    filetype: "image/*",
    root: (
      /*root*/
      n[5]
    ),
    disable_click: !/*sources*/
    n[3].includes("upload"),
    $$slots: { default: [Tu] },
    $$scope: { ctx: n }
  };
  /*uploading*/
  n[7] !== void 0 && (C.uploading = /*uploading*/
  n[7]), /*dragging*/
  n[8] !== void 0 && (C.dragging = /*dragging*/
  n[8]), s = new Ha({ props: C }), n[25](s), Xt.push(() => Nl(s, "uploading", m)), Xt.push(() => Nl(s, "dragging", p)), s.$on(
    "load",
    /*handle_upload*/
    n[15]
  ), s.$on(
    "error",
    /*error_handler*/
    n[28]
  );
  let b = (
    /*value*/
    n[0] !== null && !/*streaming*/
    n[4] && Ol(n)
  ), q = _ && Al(n);
  return {
    c() {
      _t(e.$$.fragment), t = St(), l = Un("div"), c && c.c(), i = St(), o = Un("div"), _t(s.$$.fragment), u = St(), b && b.c(), f = St(), q && q.c(), Ge(o, "class", "upload-container svelte-1qm7xww"), Ge(l, "data-testid", "image"), Ge(l, "class", "image-container svelte-1qm7xww");
    },
    m(g, w) {
      gt(e, g, w), mt(g, t, w), mt(g, l, w), c && c.m(l, null), Ot(l, i), Ot(l, o), gt(s, o, null), Ot(o, u), b && b.m(o, null), Ot(l, f), q && q.m(l, null), d = !0;
    },
    p(g, w) {
      const E = {};
      w[0] & /*show_label*/
      4 && (E.show_label = /*show_label*/
      g[2]), w[0] & /*label*/
      2 && (E.label = /*label*/
      g[1] || "Image"), e.$set(E), /*value*/
      g[0]?.url ? c ? (c.p(g, w), w[0] & /*value*/
      1 && Y(c, 1)) : (c = Ll(g), c.c(), Y(c, 1), c.m(l, i)) : c && (Et(), oe(c, 1, 1, () => {
        c = null;
      }), Ct());
      const T = {};
      w[0] & /*value, active_tool*/
      65 && (T.hidden = /*value*/
      g[0] !== null || /*active_tool*/
      g[6] === "webcam"), w[0] & /*root*/
      32 && (T.root = /*root*/
      g[5]), w[0] & /*sources*/
      8 && (T.disable_click = !/*sources*/
      g[3].includes("upload")), w[0] & /*value, active_tool*/
      65 | w[1] & /*$$scope*/
      1 && (T.$$scope = { dirty: w, ctx: g }), !a && w[0] & /*uploading*/
      128 && (a = !0, T.uploading = /*uploading*/
      g[7], Ml(() => a = !1)), !r && w[0] & /*dragging*/
      256 && (r = !0, T.dragging = /*dragging*/
      g[8], Ml(() => r = !1)), s.$set(T), /*value*/
      g[0] !== null && !/*streaming*/
      g[4] ? b ? (b.p(g, w), w[0] & /*value, streaming*/
      17 && Y(b, 1)) : (b = Ol(g), b.c(), Y(b, 1), b.m(o, null)) : b && (Et(), oe(b, 1, 1, () => {
        b = null;
      }), Ct()), w[0] & /*sources*/
      8 && (_ = /*sources*/
      g[3].length > 1 || /*sources*/
      g[3].includes("clipboard")), _ ? q ? (q.p(g, w), w[0] & /*sources*/
      8 && Y(q, 1)) : (q = Al(g), q.c(), Y(q, 1), q.m(l, null)) : q && (Et(), oe(q, 1, 1, () => {
        q = null;
      }), Ct());
    },
    i(g) {
      d || (Y(e.$$.fragment, g), Y(c), Y(s.$$.fragment, g), Y(b), Y(q), d = !0);
    },
    o(g) {
      oe(e.$$.fragment, g), oe(c), oe(s.$$.fragment, g), oe(b), oe(q), d = !1;
    },
    d(g) {
      g && (ht(t), ht(l)), dt(e, g), c && c.d(), n[25](null), dt(s), b && b.d(), q && q.d();
    }
  };
}
function Ou(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e;
  var s = this && this.__awaiter || function(S, y, k, h) {
    function D(N) {
      return N instanceof k ? N : new k(function(A) {
        A(N);
      });
    }
    return new (k || (k = Promise))(function(N, A) {
      function V(v) {
        try {
          j(h.next(v));
        } catch (W) {
          A(W);
        }
      }
      function U(v) {
        try {
          j(h.throw(v));
        } catch (W) {
          A(W);
        }
      }
      function j(v) {
        v.done ? N(v.value) : D(v.value).then(V, U);
      }
      j((h = h.apply(S, y || [])).next());
    });
  };
  const a = ju();
  let r, { value: u } = e, { points: f } = e, { label: _ = void 0 } = e, { show_label: d } = e;
  function c(S) {
    const y = S.currentTarget;
    t(9, r.width = y.width, r), t(9, r.height = y.height, r), t(9, r.natural_width = y.naturalWidth, r), t(9, r.natural_height = y.naturalHeight, r), r.resize_canvas();
  }
  function m({ detail: S }) {
    t(19, f = S), a("points_change", S);
  }
  let { sources: p = ["upload", "clipboard"] } = e, { streaming: C = !1 } = e, { root: b } = e, { i18n: q } = e, g, w = !1, { active_tool: E = null } = e;
  function T({ detail: S }) {
    t(0, u = Te(S, b, null)), a("upload", S);
  }
  let L = !1;
  function R(S) {
    let y = wi(S);
    y && a("select", { index: y, value: null });
  }
  const x = {
    upload: {
      icon: bi,
      label: q("Upload"),
      order: 0
    },
    clipboard: {
      icon: Zs,
      label: q("Paste"),
      order: 2
    }
  };
  function F(S) {
    return s(this, void 0, void 0, function* () {
      switch (S) {
        case "clipboard":
          navigator.clipboard.read().then((y) => s(this, void 0, void 0, function* () {
            for (let k = 0; k < y.length; k++) {
              const h = y[k].types.find((D) => D.startsWith("image/"));
              if (h) {
                t(0, u = null), y[k].getType(h).then((D) => s(this, void 0, void 0, function* () {
                  const N = yield g.load_files([new File([D], `clipboard.${h.replace("image/", "")}`)]);
                  t(0, u = N?.[0] || null);
                }));
                break;
              }
            }
          }));
          break;
        case "upload":
          g.open_file_upload();
          break;
      }
    });
  }
  const ie = () => {
    r.undo();
  }, ae = () => {
    r.clear();
  }, ne = () => {
    t(0, u = null), a("clear");
  };
  function M(S) {
    Xt[S ? "unshift" : "push"](() => {
      g = S, t(10, g);
    });
  }
  function O(S) {
    w = S, t(7, w);
  }
  function H(S) {
    L = S, t(8, L);
  }
  function Z(S) {
    qu.call(this, n, S);
  }
  function z(S) {
    Xt[S ? "unshift" : "push"](() => {
      r = S, t(9, r);
    });
  }
  const G = (S) => F(S);
  return n.$$set = (S) => {
    "value" in S && t(0, u = S.value), "points" in S && t(19, f = S.points), "label" in S && t(1, _ = S.label), "show_label" in S && t(2, d = S.show_label), "sources" in S && t(3, p = S.sources), "streaming" in S && t(4, C = S.streaming), "root" in S && t(5, b = S.root), "i18n" in S && t(20, q = S.i18n), "active_tool" in S && t(6, E = S.active_tool), "$$scope" in S && t(31, o = S.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*uploading*/
    128 && w && t(0, u = null), n.$$.dirty[0] & /*value, root*/
    33 && u && !u.url && t(0, u = Te(u, b, null)), n.$$.dirty[0] & /*dragging*/
    256 && a("drag", L), n.$$.dirty[0] & /*sources*/
    8 && t(11, l = p.sort((S, y) => x[S].order - x[y].order));
  }, [
    u,
    _,
    d,
    p,
    C,
    b,
    E,
    w,
    L,
    r,
    g,
    l,
    a,
    c,
    m,
    T,
    R,
    x,
    F,
    f,
    q,
    i,
    ie,
    ae,
    ne,
    M,
    O,
    H,
    Z,
    z,
    G,
    o
  ];
}
class Au extends yu {
  constructor(e) {
    super(), Du(
      this,
      e,
      Ou,
      Fu,
      Iu,
      {
        value: 0,
        points: 19,
        label: 1,
        show_label: 2,
        sources: 3,
        streaming: 4,
        root: 5,
        i18n: 20,
        active_tool: 6
      },
      null,
      [-1, -1]
    );
  }
}
function ot(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function Vt() {
}
function Pu(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const zi = typeof window < "u";
let Rl = zi ? () => window.performance.now() : () => Date.now(), Di = zi ? (n) => requestAnimationFrame(n) : Vt;
const ct = /* @__PURE__ */ new Set();
function Mi(n) {
  ct.forEach((e) => {
    e.c(n) || (ct.delete(e), e.f());
  }), ct.size !== 0 && Di(Mi);
}
function Ru(n) {
  let e;
  return ct.size === 0 && Di(Mi), {
    promise: new Promise((t) => {
      ct.add(e = { c: n, f: t });
    }),
    abort() {
      ct.delete(e);
    }
  };
}
const nt = [];
function Uu(n, e = Vt) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(a) {
    if (Pu(n, a) && (n = a, t)) {
      const r = !nt.length;
      for (const u of l)
        u[1](), nt.push(u, n);
      if (r) {
        for (let u = 0; u < nt.length; u += 2)
          nt[u][0](nt[u + 1]);
        nt.length = 0;
      }
    }
  }
  function o(a) {
    i(a(n));
  }
  function s(a, r = Vt) {
    const u = [a, r];
    return l.add(u), l.size === 1 && (t = e(i, o) || Vt), a(n), () => {
      l.delete(u), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: s };
}
function Ul(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Zn(n, e, t, l) {
  if (typeof t == "number" || Ul(t)) {
    const i = l - t, o = (t - e) / (n.dt || 1 / 60), s = n.opts.stiffness * i, a = n.opts.damping * o, r = (s - a) * n.inv_mass, u = (o + r) * n.dt;
    return Math.abs(u) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Ul(t) ? new Date(t.getTime() + u) : t + u);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => Zn(n, e[o], t[o], l[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = Zn(n, e[o], t[o], l[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Zl(n, e = {}) {
  const t = Uu(n), { stiffness: l = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let s, a, r, u = n, f = n, _ = 1, d = 0, c = !1;
  function m(C, b = {}) {
    f = C;
    const q = r = {};
    return n == null || b.hard || p.stiffness >= 1 && p.damping >= 1 ? (c = !0, s = Rl(), u = C, t.set(n = f), Promise.resolve()) : (b.soft && (d = 1 / ((b.soft === !0 ? 0.5 : +b.soft) * 60), _ = 0), a || (s = Rl(), c = !1, a = Ru((g) => {
      if (c)
        return c = !1, a = null, !1;
      _ = Math.min(_ + d, 1);
      const w = {
        inv_mass: _,
        opts: p,
        settled: !0,
        dt: (g - s) * 60 / 1e3
      }, E = Zn(w, u, n, f);
      return s = g, u = n, t.set(n = E), w.settled && (a = null), !w.settled;
    })), new Promise((g) => {
      a.promise.then(() => {
        q === r && g();
      });
    }));
  }
  const p = {
    set: m,
    update: (C, b) => m(C(f, n), b),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: o
  };
  return p;
}
const {
  SvelteComponent: Zu,
  append: Ee,
  attr: P,
  component_subscribe: Wl,
  detach: Wu,
  element: Vu,
  init: Gu,
  insert: Hu,
  noop: Vl,
  safe_not_equal: Ju,
  set_style: At,
  svg_element: ze,
  toggle_class: Gl
} = window.__gradio__svelte__internal, { onMount: Xu } = window.__gradio__svelte__internal;
function Yu(n) {
  let e, t, l, i, o, s, a, r, u, f, _, d;
  return {
    c() {
      e = Vu("div"), t = ze("svg"), l = ze("g"), i = ze("path"), o = ze("path"), s = ze("path"), a = ze("path"), r = ze("g"), u = ze("path"), f = ze("path"), _ = ze("path"), d = ze("path"), P(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), P(i, "fill", "#FF7C00"), P(i, "fill-opacity", "0.4"), P(i, "class", "svelte-43sxxs"), P(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), P(o, "fill", "#FF7C00"), P(o, "class", "svelte-43sxxs"), P(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), P(s, "fill", "#FF7C00"), P(s, "fill-opacity", "0.4"), P(s, "class", "svelte-43sxxs"), P(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), P(a, "fill", "#FF7C00"), P(a, "class", "svelte-43sxxs"), At(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), P(u, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), P(u, "fill", "#FF7C00"), P(u, "fill-opacity", "0.4"), P(u, "class", "svelte-43sxxs"), P(f, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), P(f, "fill", "#FF7C00"), P(f, "class", "svelte-43sxxs"), P(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), P(_, "fill", "#FF7C00"), P(_, "fill-opacity", "0.4"), P(_, "class", "svelte-43sxxs"), P(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), P(d, "fill", "#FF7C00"), P(d, "class", "svelte-43sxxs"), At(r, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), P(t, "viewBox", "-1200 -1200 3000 3000"), P(t, "fill", "none"), P(t, "xmlns", "http://www.w3.org/2000/svg"), P(t, "class", "svelte-43sxxs"), P(e, "class", "svelte-43sxxs"), Gl(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(c, m) {
      Hu(c, e, m), Ee(e, t), Ee(t, l), Ee(l, i), Ee(l, o), Ee(l, s), Ee(l, a), Ee(t, r), Ee(r, u), Ee(r, f), Ee(r, _), Ee(r, d);
    },
    p(c, [m]) {
      m & /*$top*/
      2 && At(l, "transform", "translate(" + /*$top*/
      c[1][0] + "px, " + /*$top*/
      c[1][1] + "px)"), m & /*$bottom*/
      4 && At(r, "transform", "translate(" + /*$bottom*/
      c[2][0] + "px, " + /*$bottom*/
      c[2][1] + "px)"), m & /*margin*/
      1 && Gl(
        e,
        "margin",
        /*margin*/
        c[0]
      );
    },
    i: Vl,
    o: Vl,
    d(c) {
      c && Wu(e);
    }
  };
}
function Ku(n, e, t) {
  let l, i;
  var o = this && this.__awaiter || function(c, m, p, C) {
    function b(q) {
      return q instanceof p ? q : new p(function(g) {
        g(q);
      });
    }
    return new (p || (p = Promise))(function(q, g) {
      function w(L) {
        try {
          T(C.next(L));
        } catch (R) {
          g(R);
        }
      }
      function E(L) {
        try {
          T(C.throw(L));
        } catch (R) {
          g(R);
        }
      }
      function T(L) {
        L.done ? q(L.value) : b(L.value).then(w, E);
      }
      T((C = C.apply(c, m || [])).next());
    });
  };
  let { margin: s = !0 } = e;
  const a = Zl([0, 0]);
  Wl(n, a, (c) => t(1, l = c));
  const r = Zl([0, 0]);
  Wl(n, r, (c) => t(2, i = c));
  let u;
  function f() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 140]), r.set([-125, -140])]), yield Promise.all([a.set([-125, 140]), r.set([125, -140])]), yield Promise.all([a.set([-125, 0]), r.set([125, -0])]), yield Promise.all([a.set([125, 0]), r.set([-125, 0])]);
    });
  }
  function _() {
    return o(this, void 0, void 0, function* () {
      yield f(), u || _();
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 0]), r.set([-125, 0])]), _();
    });
  }
  return Xu(() => (d(), () => u = !0)), n.$$set = (c) => {
    "margin" in c && t(0, s = c.margin);
  }, [s, l, i, a, r];
}
class Qu extends Zu {
  constructor(e) {
    super(), Gu(this, e, Ku, Yu, Ju, { margin: 0 });
  }
}
const {
  SvelteComponent: $u,
  append: xe,
  attr: Ie,
  binding_callbacks: Hl,
  check_outros: Ni,
  create_component: xu,
  create_slot: ef,
  destroy_component: tf,
  destroy_each: Ii,
  detach: I,
  element: Le,
  empty: wt,
  ensure_array_like: Yt,
  get_all_dirty_from_scope: nf,
  get_slot_changes: lf,
  group_outros: Bi,
  init: of,
  insert: B,
  mount_component: sf,
  noop: Wn,
  safe_not_equal: rf,
  set_data: ye,
  set_style: He,
  space: Be,
  text: J,
  toggle_class: ve,
  transition_in: pt,
  transition_out: bt,
  update_slot_base: af
} = window.__gradio__svelte__internal, { tick: uf } = window.__gradio__svelte__internal, { onDestroy: ff } = window.__gradio__svelte__internal, cf = (n) => ({}), Jl = (n) => ({});
function Xl(n, e, t) {
  const l = n.slice();
  return l[39] = e[t], l[41] = t, l;
}
function Yl(n, e, t) {
  const l = n.slice();
  return l[39] = e[t], l;
}
function _f(n) {
  let e, t = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, o;
  const s = (
    /*#slots*/
    n[29].error
  ), a = ef(
    s,
    n,
    /*$$scope*/
    n[28],
    Jl
  );
  return {
    c() {
      e = Le("span"), l = J(t), i = Be(), a && a.c(), Ie(e, "class", "error svelte-1txqlrd");
    },
    m(r, u) {
      B(r, e, u), xe(e, l), B(r, i, u), a && a.m(r, u), o = !0;
    },
    p(r, u) {
      (!o || u[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      r[1]("common.error") + "") && ye(l, t), a && a.p && (!o || u[0] & /*$$scope*/
      268435456) && af(
        a,
        s,
        r,
        /*$$scope*/
        r[28],
        o ? lf(
          s,
          /*$$scope*/
          r[28],
          u,
          cf
        ) : nf(
          /*$$scope*/
          r[28]
        ),
        Jl
      );
    },
    i(r) {
      o || (pt(a, r), o = !0);
    },
    o(r) {
      bt(a, r), o = !1;
    },
    d(r) {
      r && (I(e), I(i)), a && a.d(r);
    }
  };
}
function df(n) {
  let e, t, l, i, o, s, a, r, u, f = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Kl(n)
  );
  function _(g, w) {
    if (
      /*progress*/
      g[7]
    ) return gf;
    if (
      /*queue_position*/
      g[2] !== null && /*queue_size*/
      g[3] !== void 0 && /*queue_position*/
      g[2] >= 0
    ) return mf;
    if (
      /*queue_position*/
      g[2] === 0
    ) return hf;
  }
  let d = _(n), c = d && d(n), m = (
    /*timer*/
    n[5] && xl(n)
  );
  const p = [vf, wf], C = [];
  function b(g, w) {
    return (
      /*last_progress_level*/
      g[15] != null ? 0 : (
        /*show_progress*/
        g[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = b(n)) && (s = C[o] = p[o](n));
  let q = !/*timer*/
  n[5] && si(n);
  return {
    c() {
      f && f.c(), e = Be(), t = Le("div"), c && c.c(), l = Be(), m && m.c(), i = Be(), s && s.c(), a = Be(), q && q.c(), r = wt(), Ie(t, "class", "progress-text svelte-1txqlrd"), ve(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), ve(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(g, w) {
      f && f.m(g, w), B(g, e, w), B(g, t, w), c && c.m(t, null), xe(t, l), m && m.m(t, null), B(g, i, w), ~o && C[o].m(g, w), B(g, a, w), q && q.m(g, w), B(g, r, w), u = !0;
    },
    p(g, w) {
      /*variant*/
      g[8] === "default" && /*show_eta_bar*/
      g[18] && /*show_progress*/
      g[6] === "full" ? f ? f.p(g, w) : (f = Kl(g), f.c(), f.m(e.parentNode, e)) : f && (f.d(1), f = null), d === (d = _(g)) && c ? c.p(g, w) : (c && c.d(1), c = d && d(g), c && (c.c(), c.m(t, l))), /*timer*/
      g[5] ? m ? m.p(g, w) : (m = xl(g), m.c(), m.m(t, null)) : m && (m.d(1), m = null), (!u || w[0] & /*variant*/
      256) && ve(
        t,
        "meta-text-center",
        /*variant*/
        g[8] === "center"
      ), (!u || w[0] & /*variant*/
      256) && ve(
        t,
        "meta-text",
        /*variant*/
        g[8] === "default"
      );
      let E = o;
      o = b(g), o === E ? ~o && C[o].p(g, w) : (s && (Bi(), bt(C[E], 1, 1, () => {
        C[E] = null;
      }), Ni()), ~o ? (s = C[o], s ? s.p(g, w) : (s = C[o] = p[o](g), s.c()), pt(s, 1), s.m(a.parentNode, a)) : s = null), /*timer*/
      g[5] ? q && (q.d(1), q = null) : q ? q.p(g, w) : (q = si(g), q.c(), q.m(r.parentNode, r));
    },
    i(g) {
      u || (pt(s), u = !0);
    },
    o(g) {
      bt(s), u = !1;
    },
    d(g) {
      g && (I(e), I(t), I(i), I(a), I(r)), f && f.d(g), c && c.d(), m && m.d(), ~o && C[o].d(g), q && q.d(g);
    }
  };
}
function Kl(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Le("div"), Ie(e, "class", "eta-bar svelte-1txqlrd"), He(e, "transform", t);
    },
    m(l, i) {
      B(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && He(e, "transform", t);
    },
    d(l) {
      l && I(e);
    }
  };
}
function hf(n) {
  let e;
  return {
    c() {
      e = J("processing |");
    },
    m(t, l) {
      B(t, e, l);
    },
    p: Wn,
    d(t) {
      t && I(e);
    }
  };
}
function mf(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, o, s;
  return {
    c() {
      e = J("queue: "), l = J(t), i = J("/"), o = J(
        /*queue_size*/
        n[3]
      ), s = J(" |");
    },
    m(a, r) {
      B(a, e, r), B(a, l, r), B(a, i, r), B(a, o, r), B(a, s, r);
    },
    p(a, r) {
      r[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      a[2] + 1 + "") && ye(l, t), r[0] & /*queue_size*/
      8 && ye(
        o,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (I(e), I(l), I(i), I(o), I(s));
    }
  };
}
function gf(n) {
  let e, t = Yt(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = $l(Yl(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = wt();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      B(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Yt(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const a = Yl(i, t, s);
          l[s] ? l[s].p(a, o) : (l[s] = $l(a), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && I(e), Ii(l, i);
    }
  };
}
function Ql(n) {
  let e, t = (
    /*p*/
    n[39].unit + ""
  ), l, i, o = " ", s;
  function a(f, _) {
    return (
      /*p*/
      f[39].length != null ? bf : pf
    );
  }
  let r = a(n), u = r(n);
  return {
    c() {
      u.c(), e = Be(), l = J(t), i = J(" | "), s = J(o);
    },
    m(f, _) {
      u.m(f, _), B(f, e, _), B(f, l, _), B(f, i, _), B(f, s, _);
    },
    p(f, _) {
      r === (r = a(f)) && u ? u.p(f, _) : (u.d(1), u = r(f), u && (u.c(), u.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      f[39].unit + "") && ye(l, t);
    },
    d(f) {
      f && (I(e), I(l), I(i), I(s)), u.d(f);
    }
  };
}
function pf(n) {
  let e = ot(
    /*p*/
    n[39].index || 0
  ) + "", t;
  return {
    c() {
      t = J(e);
    },
    m(l, i) {
      B(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = ot(
        /*p*/
        l[39].index || 0
      ) + "") && ye(t, e);
    },
    d(l) {
      l && I(t);
    }
  };
}
function bf(n) {
  let e = ot(
    /*p*/
    n[39].index || 0
  ) + "", t, l, i = ot(
    /*p*/
    n[39].length
  ) + "", o;
  return {
    c() {
      t = J(e), l = J("/"), o = J(i);
    },
    m(s, a) {
      B(s, t, a), B(s, l, a), B(s, o, a);
    },
    p(s, a) {
      a[0] & /*progress*/
      128 && e !== (e = ot(
        /*p*/
        s[39].index || 0
      ) + "") && ye(t, e), a[0] & /*progress*/
      128 && i !== (i = ot(
        /*p*/
        s[39].length
      ) + "") && ye(o, i);
    },
    d(s) {
      s && (I(t), I(l), I(o));
    }
  };
}
function $l(n) {
  let e, t = (
    /*p*/
    n[39].index != null && Ql(n)
  );
  return {
    c() {
      t && t.c(), e = wt();
    },
    m(l, i) {
      t && t.m(l, i), B(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[39].index != null ? t ? t.p(l, i) : (t = Ql(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && I(e), t && t.d(l);
    }
  };
}
function xl(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = J(
        /*formatted_timer*/
        n[20]
      ), l = J(t), i = J("s");
    },
    m(o, s) {
      B(o, e, s), B(o, l, s), B(o, i, s);
    },
    p(o, s) {
      s[0] & /*formatted_timer*/
      1048576 && ye(
        e,
        /*formatted_timer*/
        o[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && ye(l, t);
    },
    d(o) {
      o && (I(e), I(l), I(i));
    }
  };
}
function wf(n) {
  let e, t;
  return e = new Qu({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      xu(e.$$.fragment);
    },
    m(l, i) {
      sf(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      l[8] === "default"), e.$set(o);
    },
    i(l) {
      t || (pt(e.$$.fragment, l), t = !0);
    },
    o(l) {
      bt(e.$$.fragment, l), t = !1;
    },
    d(l) {
      tf(e, l);
    }
  };
}
function vf(n) {
  let e, t, l, i, o, s = `${/*last_progress_level*/
  n[15] * 100}%`, a = (
    /*progress*/
    n[7] != null && ei(n)
  );
  return {
    c() {
      e = Le("div"), t = Le("div"), a && a.c(), l = Be(), i = Le("div"), o = Le("div"), Ie(t, "class", "progress-level-inner svelte-1txqlrd"), Ie(o, "class", "progress-bar svelte-1txqlrd"), He(o, "width", s), Ie(i, "class", "progress-bar-wrap svelte-1txqlrd"), Ie(e, "class", "progress-level svelte-1txqlrd");
    },
    m(r, u) {
      B(r, e, u), xe(e, t), a && a.m(t, null), xe(e, l), xe(e, i), xe(i, o), n[30](o);
    },
    p(r, u) {
      /*progress*/
      r[7] != null ? a ? a.p(r, u) : (a = ei(r), a.c(), a.m(t, null)) : a && (a.d(1), a = null), u[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      r[15] * 100}%`) && He(o, "width", s);
    },
    i: Wn,
    o: Wn,
    d(r) {
      r && I(e), a && a.d(), n[30](null);
    }
  };
}
function ei(n) {
  let e, t = Yt(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = oi(Xl(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = wt();
    },
    m(i, o) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, o);
      B(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Yt(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < t.length; s += 1) {
          const a = Xl(i, t, s);
          l[s] ? l[s].p(a, o) : (l[s] = oi(a), l[s].c(), l[s].m(e.parentNode, e));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && I(e), Ii(l, i);
    }
  };
}
function ti(n) {
  let e, t, l, i, o = (
    /*i*/
    n[41] !== 0 && kf()
  ), s = (
    /*p*/
    n[39].desc != null && ni(n)
  ), a = (
    /*p*/
    n[39].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[41]
    ] != null && li()
  ), r = (
    /*progress_level*/
    n[14] != null && ii(n)
  );
  return {
    c() {
      o && o.c(), e = Be(), s && s.c(), t = Be(), a && a.c(), l = Be(), r && r.c(), i = wt();
    },
    m(u, f) {
      o && o.m(u, f), B(u, e, f), s && s.m(u, f), B(u, t, f), a && a.m(u, f), B(u, l, f), r && r.m(u, f), B(u, i, f);
    },
    p(u, f) {
      /*p*/
      u[39].desc != null ? s ? s.p(u, f) : (s = ni(u), s.c(), s.m(t.parentNode, t)) : s && (s.d(1), s = null), /*p*/
      u[39].desc != null && /*progress_level*/
      u[14] && /*progress_level*/
      u[14][
        /*i*/
        u[41]
      ] != null ? a || (a = li(), a.c(), a.m(l.parentNode, l)) : a && (a.d(1), a = null), /*progress_level*/
      u[14] != null ? r ? r.p(u, f) : (r = ii(u), r.c(), r.m(i.parentNode, i)) : r && (r.d(1), r = null);
    },
    d(u) {
      u && (I(e), I(t), I(l), I(i)), o && o.d(u), s && s.d(u), a && a.d(u), r && r.d(u);
    }
  };
}
function kf(n) {
  let e;
  return {
    c() {
      e = J(" /");
    },
    m(t, l) {
      B(t, e, l);
    },
    d(t) {
      t && I(e);
    }
  };
}
function ni(n) {
  let e = (
    /*p*/
    n[39].desc + ""
  ), t;
  return {
    c() {
      t = J(e);
    },
    m(l, i) {
      B(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[39].desc + "") && ye(t, e);
    },
    d(l) {
      l && I(t);
    }
  };
}
function li(n) {
  let e;
  return {
    c() {
      e = J("-");
    },
    m(t, l) {
      B(t, e, l);
    },
    d(t) {
      t && I(e);
    }
  };
}
function ii(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[41]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = J(e), l = J("%");
    },
    m(i, o) {
      B(i, t, o), B(i, l, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[41]
      ] || 0)).toFixed(1) + "") && ye(t, e);
    },
    d(i) {
      i && (I(t), I(l));
    }
  };
}
function oi(n) {
  let e, t = (
    /*p*/
    (n[39].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[41]
    ] != null) && ti(n)
  );
  return {
    c() {
      t && t.c(), e = wt();
    },
    m(l, i) {
      t && t.m(l, i), B(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[39].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[41]
      ] != null ? t ? t.p(l, i) : (t = ti(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && I(e), t && t.d(l);
    }
  };
}
function si(n) {
  let e, t;
  return {
    c() {
      e = Le("p"), t = J(
        /*loading_text*/
        n[9]
      ), Ie(e, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      B(l, e, i), xe(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && ye(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && I(e);
    }
  };
}
function yf(n) {
  let e, t, l, i, o;
  const s = [df, _f], a = [];
  function r(u, f) {
    return (
      /*status*/
      u[4] === "pending" ? 0 : (
        /*status*/
        u[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = r(n)) && (l = a[t] = s[t](n)), {
    c() {
      e = Le("div"), l && l.c(), Ie(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), ve(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), ve(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), ve(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), ve(
        e,
        "border",
        /*border*/
        n[12]
      ), He(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), He(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(u, f) {
      B(u, e, f), ~t && a[t].m(e, null), n[31](e), o = !0;
    },
    p(u, f) {
      let _ = t;
      t = r(u), t === _ ? ~t && a[t].p(u, f) : (l && (Bi(), bt(a[_], 1, 1, () => {
        a[_] = null;
      }), Ni()), ~t ? (l = a[t], l ? l.p(u, f) : (l = a[t] = s[t](u), l.c()), pt(l, 1), l.m(e, null)) : l = null), (!o || f[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      u[8] + " " + /*show_progress*/
      u[6] + " svelte-1txqlrd")) && Ie(e, "class", i), (!o || f[0] & /*variant, show_progress, status, show_progress*/
      336) && ve(e, "hide", !/*status*/
      u[4] || /*status*/
      u[4] === "complete" || /*show_progress*/
      u[6] === "hidden"), (!o || f[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && ve(
        e,
        "translucent",
        /*variant*/
        u[8] === "center" && /*status*/
        (u[4] === "pending" || /*status*/
        u[4] === "error") || /*translucent*/
        u[11] || /*show_progress*/
        u[6] === "minimal"
      ), (!o || f[0] & /*variant, show_progress, status*/
      336) && ve(
        e,
        "generating",
        /*status*/
        u[4] === "generating"
      ), (!o || f[0] & /*variant, show_progress, border*/
      4416) && ve(
        e,
        "border",
        /*border*/
        u[12]
      ), f[0] & /*absolute*/
      1024 && He(
        e,
        "position",
        /*absolute*/
        u[10] ? "absolute" : "static"
      ), f[0] & /*absolute*/
      1024 && He(
        e,
        "padding",
        /*absolute*/
        u[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(u) {
      o || (pt(l), o = !0);
    },
    o(u) {
      bt(l), o = !1;
    },
    d(u) {
      u && I(e), ~t && a[t].d(), n[31](null);
    }
  };
}
var qf = function(n, e, t, l) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(f) {
      try {
        u(l.next(f));
      } catch (_) {
        s(_);
      }
    }
    function r(f) {
      try {
        u(l.throw(f));
      } catch (_) {
        s(_);
      }
    }
    function u(f) {
      f.done ? o(f.value) : i(f.value).then(a, r);
    }
    u((l = l.apply(n, e || [])).next());
  });
};
let Pt = [], Cn = !1;
function Sf(n) {
  return qf(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Pt.push(e), !Cn) Cn = !0;
      else return;
      yield uf(), requestAnimationFrame(() => {
        let l = [0, 0];
        for (let i = 0; i < Pt.length; i++) {
          const s = Pt[i].getBoundingClientRect();
          (i === 0 || s.top + window.scrollY <= l[0]) && (l[0] = s.top + window.scrollY, l[1] = i);
        }
        window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), Cn = !1, Pt = [];
      });
    }
  });
}
function Cf(n, e, t) {
  let l, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  let { i18n: s } = e, { eta: a = null } = e, { queue: r = !1 } = e, { queue_position: u } = e, { queue_size: f } = e, { status: _ } = e, { scroll_to_output: d = !1 } = e, { timer: c = !0 } = e, { show_progress: m = "full" } = e, { message: p = null } = e, { progress: C = null } = e, { variant: b = "default" } = e, { loading_text: q = "Loading..." } = e, { absolute: g = !0 } = e, { translucent: w = !1 } = e, { border: E = !1 } = e, { autoscroll: T } = e, L, R = !1, x = 0, F = 0, ie = null, ae = 0, ne = null, M, O = null, H = !0;
  const Z = () => {
    t(25, x = performance.now()), t(26, F = 0), R = !0, z();
  };
  function z() {
    requestAnimationFrame(() => {
      t(26, F = (performance.now() - x) / 1e3), R && z();
    });
  }
  function G() {
    t(26, F = 0), R && (R = !1);
  }
  ff(() => {
    R && G();
  });
  let S = null;
  function y(h) {
    Hl[h ? "unshift" : "push"](() => {
      O = h, t(16, O), t(7, C), t(14, ne), t(15, M);
    });
  }
  function k(h) {
    Hl[h ? "unshift" : "push"](() => {
      L = h, t(13, L);
    });
  }
  return n.$$set = (h) => {
    "i18n" in h && t(1, s = h.i18n), "eta" in h && t(0, a = h.eta), "queue" in h && t(21, r = h.queue), "queue_position" in h && t(2, u = h.queue_position), "queue_size" in h && t(3, f = h.queue_size), "status" in h && t(4, _ = h.status), "scroll_to_output" in h && t(22, d = h.scroll_to_output), "timer" in h && t(5, c = h.timer), "show_progress" in h && t(6, m = h.show_progress), "message" in h && t(23, p = h.message), "progress" in h && t(7, C = h.progress), "variant" in h && t(8, b = h.variant), "loading_text" in h && t(9, q = h.loading_text), "absolute" in h && t(10, g = h.absolute), "translucent" in h && t(11, w = h.translucent), "border" in h && t(12, E = h.border), "autoscroll" in h && t(24, T = h.autoscroll), "$$scope" in h && t(28, o = h.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (a === null ? t(0, a = ie) : r && t(0, a = (performance.now() - x) / 1e3 + a), a != null && (t(19, S = a.toFixed(1)), t(27, ie = a))), n.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && t(17, ae = a === null || a <= 0 || !F ? null : Math.min(F / a, 1)), n.$$.dirty[0] & /*progress*/
    128 && C != null && t(18, H = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (C != null ? t(14, ne = C.map((h) => {
      if (h.index != null && h.length != null)
        return h.index / h.length;
      if (h.progress != null)
        return h.progress;
    })) : t(14, ne = null), ne ? (t(15, M = ne[ne.length - 1]), O && (M === 0 ? t(16, O.style.transition = "0", O) : t(16, O.style.transition = "150ms", O))) : t(15, M = void 0)), n.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? Z() : G()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && L && d && (_ === "pending" || _ === "complete") && Sf(L, T), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = F.toFixed(1));
  }, [
    a,
    s,
    u,
    f,
    _,
    c,
    m,
    C,
    b,
    q,
    g,
    w,
    E,
    L,
    ne,
    M,
    O,
    ae,
    H,
    S,
    l,
    r,
    d,
    p,
    T,
    x,
    F,
    ie,
    o,
    i,
    y,
    k
  ];
}
class ji extends $u {
  constructor(e) {
    super(), of(
      this,
      e,
      Cf,
      yf,
      rf,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
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
const { setContext: Dc, getContext: Ef } = window.__gradio__svelte__internal, zf = "WORKER_PROXY_CONTEXT_KEY";
function Df() {
  return Ef(zf);
}
function Mf(n) {
  return n.host === window.location.host || n.host === "localhost:7860" || n.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  n.host === "lite.local";
}
async function ri(n) {
  if (n == null)
    return n;
  const e = new URL(n);
  if (!Mf(e) || e.protocol !== "http:" && e.protocol !== "https:")
    return n;
  const t = Df();
  if (t == null)
    return n;
  const l = e.pathname;
  return t.httpRequest({
    method: "GET",
    path: l,
    headers: {},
    query_string: ""
  }).then((i) => {
    if (i.status !== 200)
      throw new Error(`Failed to get file ${l} from the Wasm worker.`);
    const o = new Blob([i.body], {
      type: i.headers["Content-Type"]
    });
    return URL.createObjectURL(o);
  });
}
const {
  SvelteComponent: Nf,
  append: If,
  assign: Vn,
  compute_rest_props: ai,
  detach: Gn,
  element: Ti,
  empty: Bf,
  exclude_internal_props: jf,
  get_spread_update: Tf,
  handle_promise: ui,
  init: Lf,
  insert: Hn,
  noop: st,
  safe_not_equal: Ff,
  set_attributes: fi,
  set_data: Of,
  set_style: Af,
  src_url_equal: Pf,
  text: Rf,
  update_await_block_branch: Uf
} = window.__gradio__svelte__internal;
function Zf(n) {
  let e, t = (
    /*error*/
    n[3].message + ""
  ), l;
  return {
    c() {
      e = Ti("p"), l = Rf(t), Af(e, "color", "red");
    },
    m(i, o) {
      Hn(i, e, o), If(e, l);
    },
    p(i, o) {
      o & /*src*/
      1 && t !== (t = /*error*/
      i[3].message + "") && Of(l, t);
    },
    d(i) {
      i && Gn(e);
    }
  };
}
function Wf(n) {
  let e, t, l = [
    {
      src: t = /*resolved_src*/
      n[2]
    },
    /*$$restProps*/
    n[1]
  ], i = {};
  for (let o = 0; o < l.length; o += 1)
    i = Vn(i, l[o]);
  return {
    c() {
      e = Ti("img"), fi(e, i);
    },
    m(o, s) {
      Hn(o, e, s);
    },
    p(o, s) {
      fi(e, i = Tf(l, [
        s & /*src*/
        1 && !Pf(e.src, t = /*resolved_src*/
        o[2]) && { src: t },
        s & /*$$restProps*/
        2 && /*$$restProps*/
        o[1]
      ]));
    },
    d(o) {
      o && Gn(e);
    }
  };
}
function Vf(n) {
  return { c: st, m: st, p: st, d: st };
}
function Gf(n) {
  let e, t, l = {
    ctx: n,
    current: null,
    token: null,
    hasCatch: !0,
    pending: Vf,
    then: Wf,
    catch: Zf,
    value: 2,
    error: 3
  };
  return ui(t = ri(
    /*src*/
    n[0]
  ), l), {
    c() {
      e = Bf(), l.block.c();
    },
    m(i, o) {
      Hn(i, e, o), l.block.m(i, l.anchor = o), l.mount = () => e.parentNode, l.anchor = e;
    },
    p(i, [o]) {
      n = i, l.ctx = n, o & /*src*/
      1 && t !== (t = ri(
        /*src*/
        n[0]
      )) && ui(t, l) || Uf(l, n, o);
    },
    i: st,
    o: st,
    d(i) {
      i && Gn(e), l.block.d(i), l.token = null, l = null;
    }
  };
}
function Hf(n, e, t) {
  const l = ["src"];
  let i = ai(e, l), { src: o = void 0 } = e;
  return n.$$set = (s) => {
    e = Vn(Vn({}, e), jf(s)), t(1, i = ai(e, l)), "src" in s && t(0, o = s.src);
  }, [o, i];
}
class Jf extends Nf {
  constructor(e) {
    super(), Lf(this, e, Hf, Gf, Ff, { src: 0 });
  }
}
const {
  SvelteComponent: Xf,
  attr: Yf,
  create_component: Kf,
  destroy_component: Qf,
  detach: $f,
  element: xf,
  init: ec,
  insert: tc,
  mount_component: nc,
  safe_not_equal: lc,
  toggle_class: lt,
  transition_in: ic,
  transition_out: oc
} = window.__gradio__svelte__internal;
function sc(n) {
  let e, t, l;
  return t = new Jf({
    props: {
      src: (
        /*samples_dir*/
        n[1] + /*value*/
        n[0]
      ),
      alt: ""
    }
  }), {
    c() {
      e = xf("div"), Kf(t.$$.fragment), Yf(e, "class", "container svelte-h11ksk"), lt(
        e,
        "table",
        /*type*/
        n[2] === "table"
      ), lt(
        e,
        "gallery",
        /*type*/
        n[2] === "gallery"
      ), lt(
        e,
        "selected",
        /*selected*/
        n[3]
      );
    },
    m(i, o) {
      tc(i, e, o), nc(t, e, null), l = !0;
    },
    p(i, [o]) {
      const s = {};
      o & /*samples_dir, value*/
      3 && (s.src = /*samples_dir*/
      i[1] + /*value*/
      i[0]), t.$set(s), (!l || o & /*type*/
      4) && lt(
        e,
        "table",
        /*type*/
        i[2] === "table"
      ), (!l || o & /*type*/
      4) && lt(
        e,
        "gallery",
        /*type*/
        i[2] === "gallery"
      ), (!l || o & /*selected*/
      8) && lt(
        e,
        "selected",
        /*selected*/
        i[3]
      );
    },
    i(i) {
      l || (ic(t.$$.fragment, i), l = !0);
    },
    o(i) {
      oc(t.$$.fragment, i), l = !1;
    },
    d(i) {
      i && $f(e), Qf(t);
    }
  };
}
function rc(n, e, t) {
  let { value: l } = e, { samples_dir: i } = e, { type: o } = e, { selected: s = !1 } = e;
  return n.$$set = (a) => {
    "value" in a && t(0, l = a.value), "samples_dir" in a && t(1, i = a.samples_dir), "type" in a && t(2, o = a.type), "selected" in a && t(3, s = a.selected);
  }, [l, i, o, s];
}
class Mc extends Xf {
  constructor(e) {
    super(), ec(this, e, rc, sc, lc, {
      value: 0,
      samples_dir: 1,
      type: 2,
      selected: 3
    });
  }
}
const {
  SvelteComponent: ac,
  add_flush_callback: En,
  assign: Li,
  bind: zn,
  binding_callbacks: Dn,
  bubble: uc,
  check_outros: Fi,
  create_component: Fe,
  destroy_component: Oe,
  detach: Qt,
  empty: Oi,
  flush: Q,
  get_spread_object: Ai,
  get_spread_update: Pi,
  group_outros: Ri,
  init: fc,
  insert: $t,
  mount_component: Ae,
  safe_not_equal: cc,
  space: Ui,
  transition_in: _e,
  transition_out: de
} = window.__gradio__svelte__internal;
function _c(n) {
  let e, t;
  return e = new di({
    props: {
      visible: (
        /*visible*/
        n[4]
      ),
      variant: (
        /*_image*/
        n[20] === null ? "dashed" : "solid"
      ),
      border_mode: (
        /*dragging*/
        n[21] ? "focus" : "base"
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        n[2]
      ),
      elem_classes: (
        /*elem_classes*/
        n[3]
      ),
      height: (
        /*height*/
        n[9] || void 0
      ),
      width: (
        /*width*/
        n[10]
      ),
      allow_overflow: !1,
      container: (
        /*container*/
        n[12]
      ),
      scale: (
        /*scale*/
        n[13]
      ),
      min_width: (
        /*min_width*/
        n[14]
      ),
      $$slots: { default: [bc] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Fe(e.$$.fragment);
    },
    m(l, i) {
      Ae(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*visible*/
      16 && (o.visible = /*visible*/
      l[4]), i[0] & /*_image*/
      1048576 && (o.variant = /*_image*/
      l[20] === null ? "dashed" : "solid"), i[0] & /*dragging*/
      2097152 && (o.border_mode = /*dragging*/
      l[21] ? "focus" : "base"), i[0] & /*elem_id*/
      4 && (o.elem_id = /*elem_id*/
      l[2]), i[0] & /*elem_classes*/
      8 && (o.elem_classes = /*elem_classes*/
      l[3]), i[0] & /*height*/
      512 && (o.height = /*height*/
      l[9] || void 0), i[0] & /*width*/
      1024 && (o.width = /*width*/
      l[10]), i[0] & /*container*/
      4096 && (o.container = /*container*/
      l[12]), i[0] & /*scale*/
      8192 && (o.scale = /*scale*/
      l[13]), i[0] & /*min_width*/
      16384 && (o.min_width = /*min_width*/
      l[14]), i[0] & /*root, sources, label, show_label, streaming, gradio, active_tool, _image, _points, value, dragging, loading_status*/
      16580963 | i[1] & /*$$scope*/
      4096 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      de(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Oe(e, l);
    }
  };
}
function dc(n) {
  let e, t;
  return e = new di({
    props: {
      visible: (
        /*visible*/
        n[4]
      ),
      variant: "solid",
      border_mode: (
        /*dragging*/
        n[21] ? "focus" : "base"
      ),
      padding: !1,
      elem_id: (
        /*elem_id*/
        n[2]
      ),
      elem_classes: (
        /*elem_classes*/
        n[3]
      ),
      height: (
        /*height*/
        n[9] || void 0
      ),
      width: (
        /*width*/
        n[10]
      ),
      allow_overflow: !1,
      container: (
        /*container*/
        n[12]
      ),
      scale: (
        /*scale*/
        n[13]
      ),
      min_width: (
        /*min_width*/
        n[14]
      ),
      $$slots: { default: [wc] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Fe(e.$$.fragment);
    },
    m(l, i) {
      Ae(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*visible*/
      16 && (o.visible = /*visible*/
      l[4]), i[0] & /*dragging*/
      2097152 && (o.border_mode = /*dragging*/
      l[21] ? "focus" : "base"), i[0] & /*elem_id*/
      4 && (o.elem_id = /*elem_id*/
      l[2]), i[0] & /*elem_classes*/
      8 && (o.elem_classes = /*elem_classes*/
      l[3]), i[0] & /*height*/
      512 && (o.height = /*height*/
      l[9] || void 0), i[0] & /*width*/
      1024 && (o.width = /*width*/
      l[10]), i[0] & /*container*/
      4096 && (o.container = /*container*/
      l[12]), i[0] & /*scale*/
      8192 && (o.scale = /*scale*/
      l[13]), i[0] & /*min_width*/
      16384 && (o.min_width = /*min_width*/
      l[14]), i[0] & /*_image, label, show_label, show_download_button, _selectable, show_share_button, gradio, loading_status*/
      1607906 | i[1] & /*$$scope*/
      4096 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      de(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Oe(e, l);
    }
  };
}
function hc(n) {
  let e, t;
  return e = new pi({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [gc] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Fe(e.$$.fragment);
    },
    m(l, i) {
      Ae(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[1] & /*$$scope*/
      4096 && (o.$$scope = { dirty: i, ctx: l }), e.$set(o);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      de(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Oe(e, l);
    }
  };
}
function mc(n) {
  let e, t;
  return e = new Sr({
    props: {
      i18n: (
        /*gradio*/
        n[19].i18n
      ),
      type: "image",
      mode: "short"
    }
  }), {
    c() {
      Fe(e.$$.fragment);
    },
    m(l, i) {
      Ae(e, l, i), t = !0;
    },
    p(l, i) {
      const o = {};
      i[0] & /*gradio*/
      524288 && (o.i18n = /*gradio*/
      l[19].i18n), e.$set(o);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      de(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Oe(e, l);
    }
  };
}
function gc(n) {
  let e, t;
  return e = new Kt({}), {
    c() {
      Fe(e.$$.fragment);
    },
    m(l, i) {
      Ae(e, l, i), t = !0;
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      de(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Oe(e, l);
    }
  };
}
function pc(n) {
  let e, t, l, i, o;
  const s = [mc, hc], a = [];
  function r(u, f) {
    return f[0] & /*sources*/
    65536 && (e = null), e == null && (e = !!/*sources*/
    u[16].includes("upload")), e ? 0 : 1;
  }
  return t = r(n, [-1, -1]), l = a[t] = s[t](n), {
    c() {
      l.c(), i = Oi();
    },
    m(u, f) {
      a[t].m(u, f), $t(u, i, f), o = !0;
    },
    p(u, f) {
      let _ = t;
      t = r(u, f), t === _ ? a[t].p(u, f) : (Ri(), de(a[_], 1, 1, () => {
        a[_] = null;
      }), Fi(), l = a[t], l ? l.p(u, f) : (l = a[t] = s[t](u), l.c()), _e(l, 1), l.m(i.parentNode, i));
    },
    i(u) {
      o || (_e(l), o = !0);
    },
    o(u) {
      de(l), o = !1;
    },
    d(u) {
      u && Qt(i), a[t].d(u);
    }
  };
}
function bc(n) {
  let e, t, l, i, o, s, a;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        n[19].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[19].i18n
    ) },
    /*loading_status*/
    n[1]
  ];
  let u = {};
  for (let m = 0; m < r.length; m += 1)
    u = Li(u, r[m]);
  e = new ji({ props: u });
  function f(m) {
    n[29](m);
  }
  function _(m) {
    n[30](m);
  }
  function d(m) {
    n[31](m);
  }
  let c = {
    root: (
      /*root*/
      n[8]
    ),
    sources: (
      /*sources*/
      n[16]
    ),
    label: (
      /*label*/
      n[5]
    ),
    show_label: (
      /*show_label*/
      n[6]
    ),
    streaming: (
      /*streaming*/
      n[18]
    ),
    i18n: (
      /*gradio*/
      n[19].i18n
    ),
    $$slots: { default: [pc] },
    $$scope: { ctx: n }
  };
  return (
    /*active_tool*/
    n[22] !== void 0 && (c.active_tool = /*active_tool*/
    n[22]), /*_image*/
    n[20] !== void 0 && (c.value = /*_image*/
    n[20]), /*_points*/
    n[23] !== void 0 && (c.points = /*_points*/
    n[23]), l = new Au({ props: c }), Dn.push(() => zn(l, "active_tool", f)), Dn.push(() => zn(l, "value", _)), Dn.push(() => zn(l, "points", d)), l.$on(
      "points_change",
      /*points_change_handler*/
      n[32]
    ), l.$on(
      "edit",
      /*edit_handler*/
      n[33]
    ), l.$on(
      "clear",
      /*clear_handler*/
      n[34]
    ), l.$on(
      "stream",
      /*stream_handler*/
      n[35]
    ), l.$on(
      "drag",
      /*drag_handler*/
      n[36]
    ), l.$on(
      "upload",
      /*upload_handler*/
      n[37]
    ), l.$on(
      "select",
      /*select_handler_1*/
      n[38]
    ), l.$on(
      "share",
      /*share_handler_1*/
      n[39]
    ), l.$on(
      "error",
      /*error_handler_2*/
      n[40]
    ), l.$on(
      "click",
      /*click_handler*/
      n[41]
    ), l.$on(
      "error",
      /*error_handler*/
      n[42]
    ), {
      c() {
        Fe(e.$$.fragment), t = Ui(), Fe(l.$$.fragment);
      },
      m(m, p) {
        Ae(e, m, p), $t(m, t, p), Ae(l, m, p), a = !0;
      },
      p(m, p) {
        const C = p[0] & /*gradio, loading_status*/
        524290 ? Pi(r, [
          p[0] & /*gradio*/
          524288 && {
            autoscroll: (
              /*gradio*/
              m[19].autoscroll
            )
          },
          p[0] & /*gradio*/
          524288 && { i18n: (
            /*gradio*/
            m[19].i18n
          ) },
          p[0] & /*loading_status*/
          2 && Ai(
            /*loading_status*/
            m[1]
          )
        ]) : {};
        e.$set(C);
        const b = {};
        p[0] & /*root*/
        256 && (b.root = /*root*/
        m[8]), p[0] & /*sources*/
        65536 && (b.sources = /*sources*/
        m[16]), p[0] & /*label*/
        32 && (b.label = /*label*/
        m[5]), p[0] & /*show_label*/
        64 && (b.show_label = /*show_label*/
        m[6]), p[0] & /*streaming*/
        262144 && (b.streaming = /*streaming*/
        m[18]), p[0] & /*gradio*/
        524288 && (b.i18n = /*gradio*/
        m[19].i18n), p[0] & /*gradio, sources*/
        589824 | p[1] & /*$$scope*/
        4096 && (b.$$scope = { dirty: p, ctx: m }), !i && p[0] & /*active_tool*/
        4194304 && (i = !0, b.active_tool = /*active_tool*/
        m[22], En(() => i = !1)), !o && p[0] & /*_image*/
        1048576 && (o = !0, b.value = /*_image*/
        m[20], En(() => o = !1)), !s && p[0] & /*_points*/
        8388608 && (s = !0, b.points = /*_points*/
        m[23], En(() => s = !1)), l.$set(b);
      },
      i(m) {
        a || (_e(e.$$.fragment, m), _e(l.$$.fragment, m), a = !0);
      },
      o(m) {
        de(e.$$.fragment, m), de(l.$$.fragment, m), a = !1;
      },
      d(m) {
        m && Qt(t), Oe(e, m), Oe(l, m);
      }
    }
  );
}
function wc(n) {
  let e, t, l, i;
  const o = [
    {
      autoscroll: (
        /*gradio*/
        n[19].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[19].i18n
    ) },
    /*loading_status*/
    n[1]
  ];
  let s = {};
  for (let a = 0; a < o.length; a += 1)
    s = Li(s, o[a]);
  return e = new ji({ props: s }), l = new $r({
    props: {
      value: (
        /*_image*/
        n[20]
      ),
      label: (
        /*label*/
        n[5]
      ),
      show_label: (
        /*show_label*/
        n[6]
      ),
      show_download_button: (
        /*show_download_button*/
        n[7]
      ),
      selectable: (
        /*_selectable*/
        n[11]
      ),
      show_share_button: (
        /*show_share_button*/
        n[15]
      ),
      i18n: (
        /*gradio*/
        n[19].i18n
      )
    }
  }), l.$on(
    "select",
    /*select_handler*/
    n[26]
  ), l.$on(
    "share",
    /*share_handler*/
    n[27]
  ), l.$on(
    "error",
    /*error_handler_1*/
    n[28]
  ), {
    c() {
      Fe(e.$$.fragment), t = Ui(), Fe(l.$$.fragment);
    },
    m(a, r) {
      Ae(e, a, r), $t(a, t, r), Ae(l, a, r), i = !0;
    },
    p(a, r) {
      const u = r[0] & /*gradio, loading_status*/
      524290 ? Pi(o, [
        r[0] & /*gradio*/
        524288 && {
          autoscroll: (
            /*gradio*/
            a[19].autoscroll
          )
        },
        r[0] & /*gradio*/
        524288 && { i18n: (
          /*gradio*/
          a[19].i18n
        ) },
        r[0] & /*loading_status*/
        2 && Ai(
          /*loading_status*/
          a[1]
        )
      ]) : {};
      e.$set(u);
      const f = {};
      r[0] & /*_image*/
      1048576 && (f.value = /*_image*/
      a[20]), r[0] & /*label*/
      32 && (f.label = /*label*/
      a[5]), r[0] & /*show_label*/
      64 && (f.show_label = /*show_label*/
      a[6]), r[0] & /*show_download_button*/
      128 && (f.show_download_button = /*show_download_button*/
      a[7]), r[0] & /*_selectable*/
      2048 && (f.selectable = /*_selectable*/
      a[11]), r[0] & /*show_share_button*/
      32768 && (f.show_share_button = /*show_share_button*/
      a[15]), r[0] & /*gradio*/
      524288 && (f.i18n = /*gradio*/
      a[19].i18n), l.$set(f);
    },
    i(a) {
      i || (_e(e.$$.fragment, a), _e(l.$$.fragment, a), i = !0);
    },
    o(a) {
      de(e.$$.fragment, a), de(l.$$.fragment, a), i = !1;
    },
    d(a) {
      a && Qt(t), Oe(e, a), Oe(l, a);
    }
  };
}
function vc(n) {
  let e, t, l, i;
  const o = [dc, _c], s = [];
  function a(r, u) {
    return (
      /*interactive*/
      r[17] ? 1 : 0
    );
  }
  return e = a(n), t = s[e] = o[e](n), {
    c() {
      t.c(), l = Oi();
    },
    m(r, u) {
      s[e].m(r, u), $t(r, l, u), i = !0;
    },
    p(r, u) {
      let f = e;
      e = a(r), e === f ? s[e].p(r, u) : (Ri(), de(s[f], 1, 1, () => {
        s[f] = null;
      }), Fi(), t = s[e], t ? t.p(r, u) : (t = s[e] = o[e](r), t.c()), _e(t, 1), t.m(l.parentNode, l));
    },
    i(r) {
      i || (_e(t), i = !0);
    },
    o(r) {
      de(t), i = !1;
    },
    d(r) {
      r && Qt(l), s[e].d(r);
    }
  };
}
function kc(n, e, t) {
  let l, i, o, { elem_id: s = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { value: u = null } = e, { label: f } = e, { show_label: _ } = e, { show_download_button: d } = e, { root: c } = e, { proxy_url: m } = e, { height: p } = e, { width: C } = e, { _selectable: b = !1 } = e, { container: q = !0 } = e, { scale: g = null } = e, { min_width: w = void 0 } = e, { loading_status: E } = e, { show_share_button: T = !1 } = e, { sources: L = ["upload"] } = e, { interactive: R } = e, { streaming: x } = e, { gradio: F } = e, ie, ae = null;
  const ne = ({ detail: v }) => F.dispatch("select", v), M = ({ detail: v }) => F.dispatch("share", v), O = ({ detail: v }) => F.dispatch("error", v);
  function H(v) {
    ae = v, t(22, ae);
  }
  function Z(v) {
    l = v, t(20, l), t(0, u), t(8, c), t(24, m);
  }
  function z(v) {
    i = v, t(23, i), t(0, u);
  }
  const G = ({ detail: v }) => t(0, u.points = v, u), S = () => F.dispatch("edit"), y = () => {
    t(0, u = null), F.dispatch("clear"), F.dispatch("change");
  }, k = () => F.dispatch("stream"), h = ({ detail: v }) => t(21, ie = v), D = ({ detail: v }) => {
    u == null ? t(0, u = { image: v, points: null }) : t(0, u.image = v, u), F.dispatch("upload");
  }, N = ({ detail: v }) => F.dispatch("select", v), A = ({ detail: v }) => F.dispatch("share", v), V = ({ detail: v }) => {
    t(1, E), t(1, E.status = "error", E), F.dispatch("error", v);
  }, U = () => F.dispatch("error", "bad thing happened");
  function j(v) {
    uc.call(this, n, v);
  }
  return n.$$set = (v) => {
    "elem_id" in v && t(2, s = v.elem_id), "elem_classes" in v && t(3, a = v.elem_classes), "visible" in v && t(4, r = v.visible), "value" in v && t(0, u = v.value), "label" in v && t(5, f = v.label), "show_label" in v && t(6, _ = v.show_label), "show_download_button" in v && t(7, d = v.show_download_button), "root" in v && t(8, c = v.root), "proxy_url" in v && t(24, m = v.proxy_url), "height" in v && t(9, p = v.height), "width" in v && t(10, C = v.width), "_selectable" in v && t(11, b = v._selectable), "container" in v && t(12, q = v.container), "scale" in v && t(13, g = v.scale), "min_width" in v && t(14, w = v.min_width), "loading_status" in v && t(1, E = v.loading_status), "show_share_button" in v && t(15, T = v.show_share_button), "sources" in v && t(16, L = v.sources), "interactive" in v && t(17, R = v.interactive), "streaming" in v && t(18, x = v.streaming), "gradio" in v && t(19, F = v.gradio);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*value, root, proxy_url*/
    16777473 && t(20, l = u && Te(u.image, c, m)), n.$$.dirty[0] & /*value*/
    1 && t(23, i = u && u.points), n.$$.dirty[0] & /*_image*/
    1048576 && t(25, o = l?.url), n.$$.dirty[0] & /*url, gradio*/
    34078720 && o && F.dispatch("change");
  }, [
    u,
    E,
    s,
    a,
    r,
    f,
    _,
    d,
    c,
    p,
    C,
    b,
    q,
    g,
    w,
    T,
    L,
    R,
    x,
    F,
    l,
    ie,
    ae,
    i,
    m,
    o,
    ne,
    M,
    O,
    H,
    Z,
    z,
    G,
    S,
    y,
    k,
    h,
    D,
    N,
    A,
    V,
    U,
    j
  ];
}
class Nc extends ac {
  constructor(e) {
    super(), fc(
      this,
      e,
      kc,
      vc,
      cc,
      {
        elem_id: 2,
        elem_classes: 3,
        visible: 4,
        value: 0,
        label: 5,
        show_label: 6,
        show_download_button: 7,
        root: 8,
        proxy_url: 24,
        height: 9,
        width: 10,
        _selectable: 11,
        container: 12,
        scale: 13,
        min_width: 14,
        loading_status: 1,
        show_share_button: 15,
        sources: 16,
        interactive: 17,
        streaming: 18,
        gradio: 19
      },
      null,
      [-1, -1]
    );
  }
  get elem_id() {
    return this.$$.ctx[2];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), Q();
  }
  get elem_classes() {
    return this.$$.ctx[3];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), Q();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({ visible: e }), Q();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), Q();
  }
  get label() {
    return this.$$.ctx[5];
  }
  set label(e) {
    this.$$set({ label: e }), Q();
  }
  get show_label() {
    return this.$$.ctx[6];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), Q();
  }
  get show_download_button() {
    return this.$$.ctx[7];
  }
  set show_download_button(e) {
    this.$$set({ show_download_button: e }), Q();
  }
  get root() {
    return this.$$.ctx[8];
  }
  set root(e) {
    this.$$set({ root: e }), Q();
  }
  get proxy_url() {
    return this.$$.ctx[24];
  }
  set proxy_url(e) {
    this.$$set({ proxy_url: e }), Q();
  }
  get height() {
    return this.$$.ctx[9];
  }
  set height(e) {
    this.$$set({ height: e }), Q();
  }
  get width() {
    return this.$$.ctx[10];
  }
  set width(e) {
    this.$$set({ width: e }), Q();
  }
  get _selectable() {
    return this.$$.ctx[11];
  }
  set _selectable(e) {
    this.$$set({ _selectable: e }), Q();
  }
  get container() {
    return this.$$.ctx[12];
  }
  set container(e) {
    this.$$set({ container: e }), Q();
  }
  get scale() {
    return this.$$.ctx[13];
  }
  set scale(e) {
    this.$$set({ scale: e }), Q();
  }
  get min_width() {
    return this.$$.ctx[14];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), Q();
  }
  get loading_status() {
    return this.$$.ctx[1];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), Q();
  }
  get show_share_button() {
    return this.$$.ctx[15];
  }
  set show_share_button(e) {
    this.$$set({ show_share_button: e }), Q();
  }
  get sources() {
    return this.$$.ctx[16];
  }
  set sources(e) {
    this.$$set({ sources: e }), Q();
  }
  get interactive() {
    return this.$$.ctx[17];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), Q();
  }
  get streaming() {
    return this.$$.ctx[18];
  }
  set streaming(e) {
    this.$$set({ streaming: e }), Q();
  }
  get gradio() {
    return this.$$.ctx[19];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), Q();
  }
}
export {
  Mc as BaseExample,
  Jf as BaseImage,
  Au as BaseImageUploader,
  $r as BaseStaticImage,
  ku as BoxDrawer,
  Nc as default
};
