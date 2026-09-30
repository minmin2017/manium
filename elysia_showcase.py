"""Elysia capability showcase — Engineering-style Manim, English VO (ElevenLabs Bill).
Render preview: manim -ql elysia_showcase.py ElysiaShowcase   Final: -qm
Facts come from the official docs (skill: elysia); benchmark numbers = Elysia 2 blog, 2.0.0-exp.60.
"""
import sys, os, json, platform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, r"C:\Users\wicha\.claude\skills\engineering-style")
from manim import *
from eng_style import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "timing.json")))
CODE = "Consolas" if platform.system() == "Windows" else "DejaVu Sans Mono"
NAVY = BG_DEEP


def chip(txt, fill=ORANGE, size=24, pad=0.28, tcol="#0B2A4F"):
    t = Text(txt, font_size=size, color=tcol, weight=BOLD)
    r = RoundedRectangle(corner_radius=0.14, width=t.width + pad * 2, height=t.height + pad * 1.1)
    eng_style(r, fill, 3.5)
    t.move_to(r)
    return VGroup(r, t)


def code_panel(lines, size=24, width=None, colors=None):
    txt = VGroup(*[Text(l, font=CODE, font_size=size, color=TEXT, t2c=colors or {}) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    w = width or txt.width + 0.7
    box = RoundedRectangle(corner_radius=0.18, width=w, height=txt.height + 0.6)
    box.set_fill(NAVY, opacity=0.96).set_stroke(STROKE, width=4)
    txt.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.35)
    return VGroup(box, txt)


KW = {"new": YELLOW, "Elysia": ORANGE, "t.": YELLOW, ".get": ORANGE, ".post": ORANGE, ".use": ORANGE,
      ".listen": ORANGE, ".guard": ORANGE, ".group": ORANGE, ".derive": ORANGE, ".state": ORANGE,
      ".decorate": ORANGE, "treaty": YELLOW, "await": YELLOW, "const": YELLOW}


class ElysiaShowcase(Scene):
    base = 0.0  # section classes shift the clock so each renders standalone on its own runner
    def at(self, t):
        dt = t - self.renderer.time
        if dt > 0.02:
            self.wait(dt)

    def reveal(self, items, t0, d, anim=None, span=0.8, gap=0.35):
        """Reveal `items` one by one, evenly across span*d seconds starting at t0."""
        n = len(items)
        for i, it in enumerate(items):
            self.at(t0 + span * d * i / max(1, n))
            self.play(anim(it) if anim else FadeIn(it, shift=UP * 0.15), run_time=0.35)

    def head(self, txt, sub=None):
        h = Text(txt, font_size=40, color=TEXT, weight=BOLD).to_edge(UP, buff=0.4)
        g = VGroup(h)
        if sub:
            g.add(Text(sub, font_size=24, color=YELLOW).next_to(h, DOWN, buff=0.12))
        return g

    def run_section(self, key, build):
        start, d = T["sec"][key] - self.base, T["vo"][key]
        self.at(start)
        g = build(start + T["lead"], d)
        self.at(start + T["lead"] + d + 0.15)
        self.play(FadeOut(g), run_time=0.45)

    def construct(self):
        blueprint(self)
        self.add(Text("ELYSIA", font_size=18, color=TEXT).to_corner(DL, buff=0.3).set_opacity(0.6))
        for key, fn in [("s01", self.s01), ("s02", self.s02), ("s03", self.s03), ("s04", self.s04), ("s05", self.s05),
                        ("s06", self.s06), ("s07", self.s07), ("s08", self.s08), ("s09", self.s09), ("s10", self.s10),
                        ("s11", self.s11), ("s12", self.s12), ("s13", self.s13)]:
            self.run_section(key, fn)
        self.at(T["total"])

    # ---- 1 title ---------------------------------------------------------
    def s01(self, t0, d):
        hexa = RegularPolygon(6, radius=1.25).rotate(PI / 6)
        eng_style(hexa, ORANGE, 6)
        e = Text("E", font_size=90, color="#0B2A4F", weight=BOLD).move_to(hexa)
        name = Text("Elysia", font_size=110, color=TEXT, weight=BOLD)
        row = VGroup(VGroup(hexa, e), name).arrange(RIGHT, buff=0.5).shift(UP * 0.7)
        sub = Text("TypeScript web framework  ·  Bun  ·  end-to-end types", font_size=30, color=YELLOW).next_to(row, DOWN, buff=0.5)
        chips = VGroup(*[chip(x, c, 26) for x, c in [("Routes", YELLOW), ("Validation", ORANGE), ("Types", AMBER), ("Docs", YELLOW)]]).arrange(RIGHT, buff=0.35).next_to(sub, DOWN, buff=0.6)
        self.play(FadeIn(row, scale=0.85), run_time=0.7)
        self.at(t0 + 2.2); self.play(FadeIn(sub, shift=UP * 0.15), run_time=0.5)
        self.reveal(list(chips), t0 + 5.0, d, span=0.5)
        return VGroup(row, sub, chips)

    # ---- 2 routes + context ---------------------------------------------
    def s02(self, t0, d):
        h = self.head("Routes and Context")
        code = code_panel(["new Elysia()", "  .get('/', () => 'hi')", "  .post('/user', ({ body }) => body)", "  .listen(3000)"], 26, colors=KW).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        names = ["body", "query", "params", "headers", "cookie", "set", "store"]
        ctx = VGroup(*[chip(n, [YELLOW, ORANGE][i % 2], 24) for i, n in enumerate(names)]).arrange_in_grid(rows=4, cols=2, buff=0.28).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)
        ctxt = Text("Context", font_size=30, color=YELLOW).next_to(ctx, UP, buff=0.3)
        js = chip("{ ... }  ->  JSON", HOT, 28, tcol="#FFFFFF").to_edge(DOWN, buff=1.0)
        self.play(FadeIn(h), FadeIn(code, shift=RIGHT * 0.2), run_time=0.7)
        self.at(t0 + 3.5); self.play(FadeIn(ctxt), run_time=0.3)
        self.reveal(list(ctx), t0 + 4.5, d * 0.55, span=1.0)
        self.at(t0 + d * 0.78); self.play(FadeIn(js, shift=UP * 0.15), run_time=0.5)
        return VGroup(h, code, ctx, ctxt, js)

    # ---- 3 validation ------------------------------------------------------
    def s03(self, t0, d):
        h = self.head("Validation with t")
        code = code_panel(["body: t.Object({", "  name: t.String(),", "  age: t.Number()", "})"], 28, colors=KW).to_edge(LEFT, buff=0.7).shift(UP * 0.6)
        ok = VGroup(Text("{ name: 'min', age: 20 }", font=CODE, font_size=22, color=TEXT), chip("200 OK", YELLOW, 24)).arrange(RIGHT, buff=0.4)
        bad = VGroup(Text("{ name: 1 }", font=CODE, font_size=22, color=TEXT), chip("422", HOT, 24, tcol="#FFFFFF")).arrange(RIGHT, buff=0.4)
        res = VGroup(ok, bad).arrange(DOWN, buff=0.6, aligned_edge=LEFT).to_edge(RIGHT, buff=0.7).shift(UP * 0.6)
        libs = VGroup(*[chip(x, c, 24) for x, c in [("Zod", YELLOW), ("Valibot", ORANGE), ("ArkType", AMBER)]]).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=1.1)
        libt = Text("Standard Schema", font_size=26, color=TEXT).next_to(libs, UP, buff=0.25)
        self.play(FadeIn(h), FadeIn(code, shift=RIGHT * 0.2), run_time=0.7)
        self.at(t0 + 3.0); self.play(FadeIn(ok, shift=LEFT * 0.2), run_time=0.5)
        self.at(t0 + 6.5); self.play(FadeIn(bad, shift=LEFT * 0.2), run_time=0.5)
        self.play(Indicate(bad[1], color=WHITE, scale_factor=1.15), run_time=0.7)
        self.at(t0 + d * 0.72); self.play(FadeIn(libt), run_time=0.3)
        self.reveal(list(libs), t0 + d * 0.74, d * 0.3, span=1.0)
        return VGroup(h, code, res, libs, libt)

    # ---- 4 lifecycle -------------------------------------------------------
    def s04(self, t0, d):
        h = self.head("The request lifecycle")
        top = ["Request", "Parse", "Transform", "Derive", "Before Handle"]
        bot = ["Handler", "After Handle", "Map Response", "After Response"]
        def box(n, i):
            return chip(n, ORANGE if n == "Handler" else YELLOW, 22, pad=0.22)
        r1 = VGroup(*[box(n, i) for i, n in enumerate(top)]).arrange(RIGHT, buff=0.42).shift(UP * 0.7)
        r2 = VGroup(*[box(n, i) for i, n in enumerate(bot)]).arrange(RIGHT, buff=0.42).shift(DOWN * 0.9)
        r2.align_to(r1, RIGHT)
        boxes = list(r1) + list(r2)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=4, color=STROKE, max_tip_length_to_length_ratio=0.35) for i in range(4)],
                        *[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=4, color=STROKE, max_tip_length_to_length_ratio=0.35) for i in range(5, 8)])
        p0 = r1[-1].get_bottom() + DOWN * 0.05
        p3 = r2[0].get_top() + UP * 0.05
        mid_y = (r1.get_bottom()[1] + r2.get_top()[1]) / 2
        q1 = np.array([p0[0], mid_y, 0]); q2 = np.array([p3[0], mid_y, 0])
        turn = VGroup(Line(p0, q1, stroke_width=4, color=STROKE), Line(q1, q2, stroke_width=4, color=STROKE),
                      Arrow(q2, p3, buff=0, stroke_width=4, color=STROKE, max_tip_length_to_length_ratio=0.5))
        err = chip("onError", HOT, 24, tcol="#FFFFFF").next_to(r2, DOWN, buff=0.8)
        errl = DashedLine(err.get_top(), r2.get_bottom() + DOWN * 0.05, color=STROKE)
        dot = Dot(radius=0.14, color=WHITE).move_to(boxes[0].get_center() + UP * 0.6)
        self.play(FadeIn(h), run_time=0.5)
        self.play(*[FadeIn(b, shift=UP * 0.1) for b in boxes], FadeIn(arrows), FadeIn(turn), run_time=0.9)
        n = len(boxes)
        for i in range(n):
            self.at(t0 + 1.2 + (d * 0.72) * i / n)
            self.play(dot.animate.move_to(boxes[i].get_top() + UP * 0.25), boxes[i][0].animate.set_fill(WHITE), run_time=0.3)
            self.play(boxes[i][0].animate.set_fill(ORANGE if i == 5 else YELLOW), run_time=0.2)
        self.at(t0 + d * 0.8); self.play(FadeIn(err), FadeIn(errl), run_time=0.5)
        return VGroup(h, r1, r2, arrows, turn, err, errl, dot)

    # ---- 5 context extension ----------------------------------------------
    def s05(self, t0, d):
        h = self.head("Extend the context")
        cards = []
        for title, line, col in [("state", ".state('n', 0)", YELLOW), ("decorate", ".decorate('db', db)", ORANGE),
                                 ("derive", ".derive(({ headers }) => ({ user }))", AMBER), ("guard / group", ".group('/api', g => ...)", YELLOW)]:
            head = Text(title, font_size=30, color=col, weight=BOLD)
            body = Text(line, font=CODE, font_size=20, color=TEXT)
            box = RoundedRectangle(corner_radius=0.16, width=5.9, height=1.7).set_fill(NAVY, 0.96).set_stroke(STROKE, 4)
            VGroup(head, body).arrange(DOWN, buff=0.22).move_to(box)
            cards.append(VGroup(box, head, body))
        grid = VGroup(*cards).arrange_in_grid(rows=2, cols=2, buff=0.45).shift(DOWN * 0.3)
        self.play(FadeIn(h), run_time=0.5)
        self.reveal(cards, t0 + 0.2, d, span=0.8)
        return VGroup(h, grid)

    # ---- 6 plugins + scope -----------------------------------------------
    def s06(self, t0, d):
        h = self.head("Plugins and scope")
        app = RoundedRectangle(corner_radius=0.25, width=6.0, height=4.4).set_fill(NAVY, 0.6).set_stroke(STROKE, 5).shift(LEFT * 3.2 + DOWN * 0.3)
        app_l = Text("app", font_size=26, color=YELLOW).next_to(app.get_corner(UL), DR, buff=0.15)
        plug = RoundedRectangle(corner_radius=0.2, width=3.2, height=2.2).set_fill(ORANGE, 0.9).set_stroke(STROKE, 5).move_to(app.get_center() + DOWN * 0.45)
        plug_l = Text("plugin", font_size=24, color="#0B2A4F", weight=BOLD).next_to(plug.get_top(), DOWN, buff=0.12)
        hook = Circle(radius=0.28).set_fill(HOT, 1).set_stroke(STROKE, 4).move_to(plug.get_center() + DOWN * 0.3)
        hook_l = Text("hook", font_size=20, color=TEXT).next_to(hook, DOWN, buff=0.1)
        sib = RoundedRectangle(corner_radius=0.2, width=2.4, height=1.6).set_fill(YELLOW, 0.9).set_stroke(STROKE, 5).shift(RIGHT * 3.6 + UP * 1.0)
        sib_l = Text("other plugin", font_size=22, color="#0B2A4F", weight=BOLD).move_to(sib)
        rows = VGroup(chip("local  (default)", YELLOW, 24), chip("as: 'scoped'  -> parent", ORANGE, 24), chip("as: 'global'  -> everything", AMBER, 24)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 3.4 + DOWN * 1.3)
        self.play(FadeIn(h), FadeIn(app), FadeIn(app_l), run_time=0.6)
        self.play(FadeIn(plug), FadeIn(plug_l), FadeIn(hook), FadeIn(hook_l), FadeIn(sib), FadeIn(sib_l), run_time=0.7)
        self.at(t0 + d * 0.32); self.play(FadeIn(rows[0], shift=LEFT * 0.2), Indicate(hook, color=WHITE), run_time=0.7)
        self.at(t0 + d * 0.62)
        c2 = hook.copy()
        self.play(FadeIn(rows[1], shift=LEFT * 0.2), c2.animate.move_to(app.get_center() + UP * 1.25 + RIGHT * 1.6), run_time=0.9)
        self.at(t0 + d * 0.82)
        c3 = hook.copy()
        self.play(FadeIn(rows[2], shift=LEFT * 0.2), c3.animate.move_to(sib.get_corner(UR) + LEFT * 0.35 + DOWN * 0.35), run_time=1.0)
        return VGroup(h, app, app_l, plug, plug_l, hook, hook_l, sib, sib_l, rows, c2, c3)

    # ---- 7 eden ---------------------------------------------------------
    def s07(self, t0, d):
        h = self.head("Eden Treaty", "typed client, no code generation")
        srv = code_panel(["export type App =", "  typeof app"], 22, colors=KW).move_to(np.array([-4.6, 0.55, 0]))
        srv_l = Text("server", font_size=24, color=YELLOW).next_to(srv, UP, buff=0.2)
        cli = code_panel(["const api = treaty<App>(url)", "const { data, error } =", "  await api.user.post({ name: 'min' })"], 21, colors=KW).move_to(np.array([2.6, 0.55, 0]))
        cli_l = Text("client", font_size=24, color=YELLOW).next_to(cli, UP, buff=0.2)
        arr = Arrow(srv.get_right(), cli.get_left(), buff=0.15, stroke_width=6, color=STROKE)
        arr_l = Text("types", font_size=22, color=ORANGE).next_to(arr, UP, buff=0.05)
        hint = VGroup(chip("data: { name: string }", YELLOW, 24), chip("autocomplete", ORANGE, 24)).arrange(RIGHT, buff=0.4).shift(DOWN * 1.2)
        bad = VGroup(Text("api.user.post({ age: 'x' })", font=CODE, font_size=22, color=TEXT), chip("type error at compile time", HOT, 24, tcol="#FFFFFF")).arrange(RIGHT, buff=0.4).shift(DOWN * 2.5)
        self.play(FadeIn(h), FadeIn(srv), FadeIn(srv_l), run_time=0.7)
        self.at(t0 + 3.0); self.play(FadeIn(cli), FadeIn(cli_l), GrowArrow(arr), FadeIn(arr_l), run_time=0.8)
        self.at(t0 + d * 0.5); self.play(FadeIn(hint, shift=UP * 0.15), run_time=0.5)
        self.at(t0 + d * 0.68); self.play(FadeIn(bad, shift=UP * 0.15), run_time=0.5)
        return VGroup(h, srv, srv_l, cli, cli_l, arr, arr_l, hint, bad)

    # ---- 8 plugins gallery -------------------------------------------------
    def s08(self, t0, d):
        h = self.head("Official plugins")
        names = ["OpenAPI", "CORS", "JWT", "Bearer", "Cron", "HTML / JSX", "Static", "Server Timing", "OpenTelemetry", "GraphQL"]
        cs = [chip(n, [YELLOW, ORANGE, AMBER][i % 3], 28) for i, n in enumerate(names)]
        grid = VGroup(*cs).arrange_in_grid(rows=4, cols=3, buff=(0.4, 0.4)).shift(DOWN * 0.4)
        self.play(FadeIn(h), run_time=0.5)
        self.reveal(cs, t0 + 0.4, d, span=0.85)
        return VGroup(h, grid)

    # ---- 9 realtime -------------------------------------------------------
    def s09(self, t0, d):
        h = self.head("Realtime and streaming")
        lanes, dots = VGroup(), []
        for i, (lab, col) in enumerate([("WebSocket", YELLOW), ("Server-sent events", ORANGE), ("Streaming response", AMBER)]):
            y = 1.2 - i * 1.5
            a = chip("client", col, 22).move_to(LEFT * 4.6 + UP * y)
            b = chip("server", col, 22).move_to(RIGHT * 2.2 + UP * y)
            ln = Line(a.get_right(), b.get_left(), color=STROKE, stroke_width=4)
            t = Text(lab, font_size=26, color=col).next_to(b, RIGHT, buff=0.4)
            lanes.add(VGroup(a, b, ln, t)); dots.append((a, b, col, i))
        chips = VGroup(chip("signed cookies", YELLOW, 24), chip("file uploads", ORANGE, 24)).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(h), FadeIn(lanes), run_time=0.7)
        for a, b, col, i in dots:
            self.at(t0 + 0.4 + d * 0.22 * i)
            fwd = Dot(radius=0.13, color=WHITE).move_to(a.get_right())
            self.add(fwd)
            anims = [fwd.animate.move_to(b.get_left())]
            if i == 0:
                back = Dot(radius=0.13, color=WHITE).move_to(b.get_left()); self.add(back)
                anims.append(back.animate.move_to(a.get_right()))
            self.play(*anims, run_time=1.2, rate_func=linear)
            self.remove(fwd)
            if i == 0: self.remove(back)
        self.at(t0 + d * 0.72); self.play(FadeIn(chips, shift=UP * 0.15), run_time=0.5)
        return VGroup(h, lanes, chips)

    # ---- 10 runs anywhere -----------------------------------------------
    def s10(self, t0, d):
        h = self.head("Runs anywhere")
        rows = [("Runtimes", ["Bun", "Node", "Deno"], YELLOW), ("Edge / cloud", ["Cloudflare Workers", "Vercel", "Netlify"], ORANGE),
                ("Mount inside", ["Next.js", "Astro", "Nuxt", "SvelteKit", "Expo", "TanStack Start"], AMBER)]
        groups, allc = VGroup(), []
        for title, items, col in rows:
            cs = [chip(x, col, 24) for x in items]
            r = VGroup(*cs).arrange(RIGHT, buff=0.25)
            if r.width > 12.4:
                r = VGroup(*cs).arrange_in_grid(rows=2, cols=3, buff=0.25)
            t = Text(title, font_size=26, color=TEXT)
            groups.add(VGroup(t, r).arrange(DOWN, buff=0.22)); allc += cs
        groups.arrange(DOWN, buff=0.45).shift(DOWN * 0.45)
        self.play(FadeIn(h), run_time=0.5)
        self.reveal(allc, t0 + 0.3, d, span=0.88)
        return VGroup(h, groups)

    # ---- 11 performance ---------------------------------------------------
    def s11(self, t0, d):
        h = self.head("Performance", "Elysia 2.0.0-exp.60 · benchmark from the Elysia 2 blog")
        def bars(title, data, unit, x0, maxv, fmt):
            t = Text(title, font_size=26, color=TEXT, weight=BOLD)
            rows = VGroup()
            for name, val, col in data:
                lab = Text(name, font_size=20, color=TEXT)
                w = 3.6 * val / maxv
                bar = Rectangle(width=max(w, 0.05), height=0.36); eng_style(bar, col, 3)
                num = Text(fmt(val) + unit, font_size=18, color=TEXT)
                rows.add(VGroup(lab, bar, num))
            for r in rows:
                r[0].set_x(0)
            g = VGroup(t, rows)
            for r in rows:
                r[1].next_to(r[0], RIGHT, buff=0.2, aligned_edge=LEFT); r[1].set_x(r[0].get_right()[0] + 0.2 + r[1].width / 2)
                r[2].next_to(r[1], RIGHT, buff=0.15)
            rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            g.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(np.array([x0, -0.3, 0]))
            return g, rows
        g1, r1 = bars("Requests / second", [("Elysia (Bun)", 210411, YELLOW), ("Hono (Bun)", 168275, AMBER), ("Fastify (Node)", 101360, AMBER), ("Express (Node)", 42974, AMBER)], "", -3.5, 210411, lambda v: f"{v:,}")
        g2, r2 = bars("Hello world bundle (KB)", [("Hono", 21, AMBER), ("h3", 103, AMBER), ("Elysia", 141, YELLOW), ("Express", 603, AMBER), ("Fastify", 729, AMBER)], " KB", 3.9, 729, lambda v: f"{v:,}")
        self.play(FadeIn(h), run_time=0.5)
        self.at(t0 + 0.6); self.play(FadeIn(g1[0]), run_time=0.3)
        self.play(*[FadeIn(r, shift=RIGHT * 0.2) for r in r1], run_time=1.0)
        self.at(t0 + d * 0.5); self.play(FadeIn(g2[0]), run_time=0.3)
        self.play(*[FadeIn(r, shift=RIGHT * 0.2) for r in r2], run_time=1.0)
        return VGroup(h, g1, g2)

    # ---- 12 deploy --------------------------------------------------------
    def s12(self, t0, d):
        h = self.head("Ship it")
        cs = [chip(x, [YELLOW, ORANGE, AMBER][i % 3], 30) for i, x in enumerate(["bun build --compile", "Docker", "Cluster mode", "AOT compilation", "OpenTelemetry tracing"])]
        grid = VGroup(*cs).arrange_in_grid(rows=3, cols=2, buff=0.5).shift(DOWN * 0.4)
        self.play(FadeIn(h), run_time=0.5)
        self.reveal(cs, t0 + 0.4, d, span=0.8)
        return VGroup(h, grid)

    # ---- 13 outro ---------------------------------------------------------
    def s13(self, t0, d):
        code = code_panel(["new Elysia()", "  .use(openapi())", "  .get('/user/:id', handler, { params })", "  .listen(3000)"], 28, colors=KW).shift(UP * 1.4)
        res = VGroup(*[chip(x, c, 28) for x, c in [("Routes", YELLOW), ("Validation", ORANGE), ("Types", AMBER), ("Docs", YELLOW)]]).arrange(RIGHT, buff=0.4).next_to(code, DOWN, buff=0.7)
        end = Text("Elysia  —  ergonomics, with speed.", font_size=44, color=TEXT, weight=BOLD).next_to(res, DOWN, buff=0.8)
        self.play(FadeIn(code, shift=UP * 0.2), run_time=0.7)
        self.reveal(list(res), t0 + 2.0, d * 0.5, span=1.0)
        self.at(t0 + d * 0.62); self.play(FadeIn(end, scale=0.92), run_time=0.7)
        return VGroup(code, res, end)


def _make_section(key):
    def construct(self):
        blueprint(self)
        self.add(Text("ELYSIA", font_size=18, color=TEXT).to_corner(DL, buff=0.3).set_opacity(0.6))
        self.base = T["sec"][key]
        self.run_section(key, getattr(self, key))
        self.at(T["lead"] + T["vo"][key] + T["tail"])
    return type("Sec" + key[1:], (ElysiaShowcase,), {"construct": construct, "__module__": __name__})


for _k in ["s%02d" % i for i in range(1, 14)]:
    globals()["Sec" + _k[1:]] = _make_section(_k)
