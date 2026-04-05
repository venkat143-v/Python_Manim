"""
RAG Pipeline Animation — Manim (Fully Fixed Layout)
=====================================================
Manim default frame:  width=14.22  height=8.0  (units)
All elements are carefully positioned to stay on screen.

SETUP:
  pip install manim

RUN (choose one):
  manim -pql rag_pipeline_animation.py RAGPipeline   # fast preview
  manim -pqh rag_pipeline_animation.py RAGPipeline   # HD final

OUTPUT:
  media/videos/rag_pipeline_animation/RAGPipeline.mp4
"""

from manim import *

# ── Palette ────────────────────────────────────────────────────────────────
BG        = "#021B2E"
NAVY      = "#0D2137"
TEAL_C    = "#0D9488"
MINT_C    = "#02C39A"
BLUE_C    = "#1A8FE3"
DKBLUE    = "#065A82"
ORANGE_C  = "#E87722"
PURPLE_C  = "#8B5CF6"
GREEN_C   = "#10B981"
RED_C     = "#EF4444"
SALMON_C  = "#F87171"
GOLD_C    = "#F59E0B"
GRAY_C    = "#64748B"
LBLUE     = "#BAE6FD"
CGREEN    = "#A8D8A8"
W         = "#FFFFFF"

# ── Frame constants (Manim default 16:9) ───────────────────────────────────
# X range: -7.11 … +7.11   Y range: -4.0 … +4.0
FW = 14.22   # frame width
FH = 8.0     # frame height


# ── Tiny helpers ───────────────────────────────────────────────────────────
def lbl(text, sz=18, color=W, bold=True):
    return Text(text, font_size=sz, color=color,
                weight=BOLD if bold else NORMAL)


def sub(text, sz=13, color=LBLUE):
    return Text(text, font_size=sz, color=color)


def arr(start, end, color=TEAL_C, sw=3):
    return Arrow(start, end, buff=0.10, color=color,
                 stroke_width=sw,
                 max_tip_length_to_length_ratio=0.25)


def db2d(body_color=GOLD_C, rim_color=ORANGE_C, w=0.9, h=0.65):
    """2-D flat database cylinder."""
    body = Rectangle(width=w, height=h,
                     fill_color=body_color, fill_opacity=1,
                     stroke_color=rim_color, stroke_width=2)
    top  = Ellipse(width=w, height=w*0.28,
                   fill_color=rim_color, fill_opacity=1,
                   stroke_color=W, stroke_width=1.2)
    bot  = Ellipse(width=w, height=w*0.28,
                   fill_color=body_color, fill_opacity=1,
                   stroke_color=rim_color, stroke_width=1.2)
    top.next_to(body, UP,   buff=0)
    bot.next_to(body, DOWN, buff=0)
    return VGroup(body, top, bot)


def banner(text, w=5.5, h=0.40, color=DKBLUE):
    r = Rectangle(width=w, height=h,
                  fill_color=color, fill_opacity=1, stroke_width=0)
    t = Text(text, font_size=16, color=W, weight=BOLD)
    t.move_to(r)
    return VGroup(r, t)


def node_box(w=1.6, h=1.0, fill=NAVY, border=TEAL_C):
    return RoundedRectangle(corner_radius=0.10, width=w, height=h,
                            fill_color=fill, fill_opacity=1,
                            stroke_color=border, stroke_width=2.5)


# ═══════════════════════════════════════════════════════════════════════════
class RAGPipeline(Scene):
    """
    Scenes
    ──────
    1. Title card
    2. Data Indexing    (left half, Y ≈ 0.5 … -1.5)
    3. Retrieval+Gen    (right half, same Y band)
    4. Particle replay
    5. Closing card
    """

    def construct(self):
        self.camera.background_color = BG
        self._s1_title()
        self._s2_indexing()
        self._s3_retrieval()
        self._s4_replay()
        self._s5_closing()

    # ═══════════════════════════════════════════════════════════════════════
    # S1  TITLE
    # ═══════════════════════════════════════════════════════════════════════
    def _s1_title(self):
        # decorative blobs  (safe: circles, no stroke)
        b1 = Circle(radius=2.8, color=DKBLUE,
                    fill_opacity=0.20, stroke_width=0).shift(RIGHT*3.5+UP*1.2)
        b2 = Circle(radius=1.6, color=TEAL_C,
                    fill_opacity=0.14, stroke_width=0).shift(RIGHT*4.5+DOWN*0.8)

        title = Text("RAG Pipeline", font_size=68, color=W, weight=BOLD)
        sub1  = Text("Retrieval-Augmented Generation",
                     font_size=28, color=MINT_C)
        sub2  = Text("AI grounded in YOUR data — not just training memory",
                     font_size=18, color=LBLUE)
        sub1.next_to(title, DOWN, buff=0.35)
        sub2.next_to(sub1,  DOWN, buff=0.35)

        uline = Line(title.get_left()+DOWN*0.06,
                     title.get_right()+DOWN*0.06,
                     color=TEAL_C, stroke_width=4)

        self.play(FadeIn(b1, b2), run_time=0.4)
        self.play(Write(title), run_time=1.1)
        self.play(Create(uline), run_time=0.45)
        self.play(FadeIn(sub1, shift=UP*0.25), run_time=0.65)
        self.play(FadeIn(sub2, shift=UP*0.20), run_time=0.65)
        self.wait(1.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.7)

    # ═══════════════════════════════════════════════════════════════════════
    # S2  DATA INDEXING
    # ═══════════════════════════════════════════════════════════════════════
    def _s2_indexing(self):
        """
        Layout (all Y between  2.5 top … -2.5 bottom):

          [banner at Y=3.2]

          Y=1.4   docs   →   chunks   →   embeds   →   vector DB
          (nodes centered horizontally in X = -6.0, -3.2, -0.5, 2.1)

          Y=-0.6  labels below each node
        """

        # ── PHASE BANNER ─────────────────────────────────────────────────
        idx_banner = banner(
            "  DATA INDEXING  (Offline — One Time)",
            w=6.5, h=0.42, color=DKBLUE
        )
        idx_banner.move_to(UP*3.4 + LEFT*2.5)
        self.play(FadeIn(idx_banner, shift=DOWN*0.18), run_time=0.5)

        # ── X positions for the 4 nodes ──────────────────────────────────
        x_doc, x_ck, x_em, x_db = -5.8, -3.0, -0.4, 2.2
        node_y   = 0.9    # icon centre Y
        lbl_y    = -0.05  # label Y
        sublbl_y = -0.52  # sub-label Y

        # ── NODE 1: Documents ─────────────────────────────────────────────
        # paper stack
        def paper_stack(cx, cy):
            pps = []
            cols = ["#475569", "#64748B", W]
            for i, c in enumerate(cols):
                p = Rectangle(width=0.65, height=0.80,
                               fill_color=c, fill_opacity=0.92,
                               stroke_color=GRAY_C, stroke_width=1.2)
                p.move_to([cx - 0.10*(2-i), cy + 0.06*(2-i), 0])
                pps.append(p)
            # ruled lines on top paper
            for j in range(3):
                ln = Line(pps[-1].get_left()+RIGHT*0.08+DOWN*(0.05+j*0.2),
                          pps[-1].get_right()+LEFT*0.08+DOWN*(0.05+j*0.2),
                          color=GRAY_C, stroke_width=1.0)
                pps[-1].add(ln)
            return VGroup(*pps)

        doc_icon = paper_stack(x_doc, node_y)
        doc_lbl  = lbl("Documents", sz=16)
        doc_slbl = sub("PDFs / CSVs / Web pages", sz=12)
        doc_lbl.move_to([x_doc, lbl_y, 0])
        doc_slbl.move_to([x_doc, sublbl_y, 0])
        doc_grp  = VGroup(doc_icon, doc_lbl, doc_slbl)

        self.play(FadeIn(doc_grp, shift=RIGHT*0.35), run_time=0.7)

        # ── ARROW 1 ───────────────────────────────────────────────────────
        a1 = arr([x_doc+0.52, node_y, 0],
                 [x_ck -0.52, node_y, 0], color=ORANGE_C)
        self.play(GrowArrow(a1), run_time=0.4)

        # ── NODE 2: Chunks ────────────────────────────────────────────────
        ck_boxes = VGroup(*[
            Rectangle(width=0.46, height=0.26,
                      fill_color=BLUE_C, fill_opacity=0.88,
                      stroke_color=W, stroke_width=1.2)
            for _ in range(6)
        ]).arrange_in_grid(rows=3, cols=2, buff=0.08)
        ck_boxes.move_to([x_ck, node_y, 0])

        ck_lbl  = lbl("Chunks", sz=16)
        ck_slbl = sub("Split into small pieces", sz=12)
        ck_lbl.move_to([x_ck, lbl_y, 0])
        ck_slbl.move_to([x_ck, sublbl_y, 0])
        ck_grp  = VGroup(ck_boxes, ck_lbl, ck_slbl)

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP*0.12) for b in ck_boxes],
                        lag_ratio=0.10),
            run_time=0.75
        )
        self.play(FadeIn(ck_lbl, ck_slbl), run_time=0.3)

        # ── ARROW 2 ───────────────────────────────────────────────────────
        a2 = arr([x_ck+0.55, node_y, 0],
                 [x_em-0.65, node_y, 0], color=ORANGE_C)
        self.play(GrowArrow(a2), run_time=0.4)

        # ── NODE 3: Vector Embeddings ─────────────────────────────────────
        # flash numbers then morph to dots
        vec_txt = Text("[0.23, -0.41, 0.87 …]",
                       font_size=13, color=CGREEN)
        vec_txt.move_to([x_em, node_y, 0])
        self.play(Write(vec_txt), run_time=0.55)
        self.wait(0.25)

        e_dots = VGroup(*[
            Dot(radius=0.07, color=BLUE_C, fill_opacity=0.9)
            for _ in range(16)
        ]).arrange_in_grid(rows=4, cols=4, buff=0.14)
        e_dots.move_to([x_em, node_y, 0])

        self.play(ReplacementTransform(vec_txt, e_dots), run_time=0.55)
        self.play(e_dots.animate.set_color(MINT_C), run_time=0.2)
        self.play(e_dots.animate.set_color(BLUE_C),  run_time=0.2)

        em_lbl  = lbl("Vector Embeddings", sz=15)
        em_slbl = sub("Convert to numeric vectors", sz=12)
        em_lbl.move_to([x_em, lbl_y, 0])
        em_slbl.move_to([x_em, sublbl_y, 0])
        em_grp  = VGroup(e_dots, em_lbl, em_slbl)
        self.play(FadeIn(em_lbl, em_slbl), run_time=0.3)

        # ── ARROW 3 ───────────────────────────────────────────────────────
        a3 = arr([x_em+0.65, node_y, 0],
                 [x_db-0.60, node_y, 0], color=ORANGE_C)
        self.play(GrowArrow(a3), run_time=0.4)

        # ── NODE 4: Vector DB ─────────────────────────────────────────────
        db4 = db2d()
        db4.move_to([x_db, node_y+0.15, 0])

        db4_lbl  = lbl("Vector DB", sz=16)
        db4_slbl = sub("Pinecone / pgvector", sz=12)
        db4_lbl.move_to([x_db, lbl_y, 0])
        db4_slbl.move_to([x_db, sublbl_y, 0])
        db4_grp  = VGroup(db4, db4_lbl, db4_slbl)

        glow4 = Circle(radius=0.72, color=GOLD_C,
                       fill_opacity=0.12, stroke_width=0)
        glow4.move_to(db4.get_center())
        self.play(FadeIn(glow4), FadeIn(db4_grp, shift=DOWN*0.2),
                  run_time=0.65)

        # vectors flowing into DB animation
        for _ in range(3):
            dp = Dot(radius=0.07, color=MINT_C)
            dp.move_to([x_em+0.5, node_y, 0])
            self.play(dp.animate.move_to(db4.get_center()),
                      run_time=0.25, rate_func=rush_into)
            self.remove(dp)
        self.play(FadeOut(glow4), run_time=0.25)

        # ── BIG SEPARATOR ARROW ───────────────────────────────────────────
        # Centred on screen, pointing right
        big_a = Arrow(
            [x_db+0.8, node_y, 0],
            [x_db+2.2, node_y, 0],
            color=ORANGE_C, stroke_width=14, buff=0,
            max_tip_length_to_length_ratio=0.45
        )
        self.play(GrowArrow(big_a), run_time=0.65)

        # save for replay
        self._doc_grp  = doc_grp
        self._ck_grp   = ck_grp
        self._em_grp   = em_grp
        self._db4_grp  = db4_grp
        self._big_a    = big_a
        self._a1 = a1; self._a2 = a2; self._a3 = a3
        self._idx_ban  = idx_banner
        self._ny       = node_y      # store for retrieval phase
        self.wait(0.5)

    # ═══════════════════════════════════════════════════════════════════════
    # S3  DATA RETRIEVAL & GENERATION
    # ═══════════════════════════════════════════════════════════════════════
    def _s3_retrieval(self):
        """
        We shrink the indexing side to the left half and build the
        retrieval phase on the right half.

        After shrink, the indexing block sits ~ X=-4.5…-1.5
        Retrieval nodes:  X = 0.5, 2.4, 4.3, 6.0 (clamped to +7)
        """

        # ── Shrink + shift indexing block left ────────────────────────────
        idx_all = VGroup(
            self._doc_grp, self._ck_grp, self._em_grp,
            self._db4_grp, self._a1, self._a2, self._a3,
            self._big_a,   self._idx_ban
        )
        self.play(
            idx_all.animate.scale(0.55).move_to(LEFT * 3.5 + UP * 0.3),
            run_time=0.85
        )

        # ── RETRIEVAL PHASE BANNER ────────────────────────────────────────
        ret_ban = banner(
            "  DATA RETRIEVAL & GENERATION  ",
            w=6.4, h=0.42, color=ORANGE_C
        )
        ret_ban.move_to(UP*3.4 + RIGHT*2.8)
        self.play(FadeIn(ret_ban, shift=DOWN*0.18), run_time=0.5)

        # ── Fixed X positions (right half, all within ±7) ─────────────────
        # Frame right edge ≈ +7.11
        center_right = 2.8   # center of right half
        gap = 1.5

        x_q  = center_right - gap * 1.5
        x_qe = center_right - gap * 0.5
        x_vd = center_right + gap * 0.5
        x_tk = center_right + gap * 1.5
        # x_q  = -0.5    # User Query bubble centre
        # x_qe = 1.2   # Vector Embedding dots
        # x_vd = 2.9    # Vector DB Search
        # x_tk = 4.4    # Top-k chunks
        # node_y = 1.4  # icon Y
        # lbl_y  = 0.38 # label Y
        # sl_y   = -0.02
        node_y = 1.2
        lbl_y  = 0.3
        sl_y   = -0.1

        # ── NODE 5: User Query ────────────────────────────────────────────
        bubble = RoundedRectangle(
            corner_radius=0.14, width=1.6, height=0.65,
            fill_color="#1E3A4A", fill_opacity=1,
            stroke_color=TEAL_C, stroke_width=2.5
        )
        bubble.move_to([x_q, node_y, 0])

        q_lbl  = lbl("User Query", sz=12)
        q_slbl = sub("Question from user", sz=9)
        q_lbl.move_to([x_q, lbl_y, 0])
        q_slbl.move_to([x_q, sl_y, 0])

        self.play(FadeIn(bubble, q_lbl, q_slbl), run_time=0.5)

        # Typing effect inside bubble
        stages = [
            "Printer error…",
            "Error code 49.38.07",
            "How do I fix error 49.38.07?",
        ]
        cur = None
        for s in stages:
            t = Text(s, font_size=8, color=W)
            t.move_to(bubble.get_center())
            if cur:
                self.play(ReplacementTransform(cur, t), run_time=0.25)
            else:
                self.play(FadeIn(t), run_time=0.28)
            cur = t
        query_typed = cur
        q_grp = VGroup(bubble, query_typed, q_lbl, q_slbl)

        # ── ARROW Q1 ──────────────────────────────────────────────────────
        arrow_y = node_y - 0.35   # shift below icons

        aq1 = arr([x_q+1.2,  arrow_y, 0],
            [x_qe-0.52, arrow_y, 0], color=ORANGE_C)
        
        self.play(GrowArrow(aq1), run_time=0.38)

        # ── NODE 6: Vector Embedding ───────────────────────────────────────
        qd = VGroup(*[
            Dot(radius=0.06, color=GREEN_C, fill_opacity=1.0)
            for _ in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.16)
        qd.move_to([x_qe, node_y, 0])

        qe_lbl  = lbl("Vector Embedding", sz=12)
        qe_slbl = sub("Embed query to vector", sz=9)
        qe_lbl.move_to([x_qe, lbl_y, 0])
        qe_slbl.move_to([x_qe, sl_y, 0])
        qe_grp  = VGroup(qd, qe_lbl, qe_slbl)

        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in qd],
                        lag_ratio=0.08),
            run_time=0.55
        )
        self.play(FadeIn(qe_lbl, qe_slbl), run_time=0.3)

        # ── ARROW Q2 ──────────────────────────────────────────────────────
        aq2 = arr([x_qe+0.55, node_y, 0],
                  [x_vd-0.55, node_y, 0], color=ORANGE_C)
        self.play(GrowArrow(aq2), run_time=0.38)

        # ── NODE 7: Vector DB Search ───────────────────────────────────────
        db7 = db2d()
        db7.move_to([x_vd, node_y+0.12, 0])

        db7_lbl  = lbl("Vector DB", sz=12)
        db7_slbl = sub("Find similar chunks", sz=9)
        db7_lbl.move_to([x_vd, lbl_y, 0])
        db7_slbl.move_to([x_vd, sl_y, 0])
        db7_grp  = VGroup(db7, db7_lbl, db7_slbl)

        self.play(FadeIn(db7_grp, shift=DOWN*0.18), run_time=0.55)

        # search ring pulse
        ring = Circle(radius=0.5, color=GOLD_C,
                      stroke_width=3, fill_opacity=0)
        ring.move_to(db7.get_center())
        self.play(Create(ring), run_time=0.3)
        self.play(ring.animate.scale(1.5).set_opacity(0), run_time=0.38)
        self.remove(ring)

        # ── ARROW Q3 ──────────────────────────────────────────────────────
        aq3 = arr([x_vd+0.55, node_y, 0],
                  [x_tk-0.85, node_y, 0], color=ORANGE_C)
        self.play(GrowArrow(aq3), run_time=0.38)

        # ── TOP-K CHUNKS ──────────────────────────────────────────────────
        bars = VGroup(*[
            Rectangle(
                width=1.2, height=0.20,
                fill_color=SALMON_C,
                fill_opacity=max(0.50, 0.92 - i*0.18),
                stroke_color=W, stroke_width=1.2
            )
            for i in range(3)
        ]).arrange(DOWN, buff=0.10)
        bars.move_to([x_tk, node_y, 0])

        tk_lbl  = Text("Top-k Chunks", font_size=13,
                       color=RED_C, weight=BOLD)
        tk_lbl.next_to(bars, UP, buff=0.06)
        ret_lbl = Text("Retrieval", font_size=12,
                       color=ORANGE_C, weight=BOLD)
        ret_lbl.next_to(bars, DOWN, buff=0.06)

        for bar in bars:
            self.play(FadeIn(bar, shift=LEFT*0.2), run_time=0.22)
        self.play(FadeIn(tk_lbl, ret_lbl), run_time=0.3)

        # ── DASHED LINE: top-k  →  LLM (going DOWN) ───────────────────────
        # LLM brain will be placed below, centred between x_vd and x_tk
        # llm_x = (x_vd + x_tk) / 2   # ≈ 5.05
        # llm_y = -1.5                 # below the node row
        llm_x = center_right
        llm_y = -1.3
        
        # dash = DashedLine(
        #     [x_tk, node_y - 0.40, 0],
        #     [llm_x, llm_y + 0.72,  0],
        #     color=GREEN_C, stroke_width=2.5,
        #     dash_length=0.12, dashed_ratio=0.55
        # )
        # create 3-point path: down → left → down
        p1 = np.array([x_tk, node_y - 0.9, 0])     # BELOW text
        p2 = np.array([x_tk, llm_y + 0.8, 0])      # down
        p3 = np.array([llm_x, llm_y + 0.8, 0])     # left
        p4 = np.array([llm_x, llm_y + 0.6, 0])     # down into LLM 

        path = VMobject()
        path.set_points_as_corners([p1, p2, p3, p4])

        dash = DashedVMobject(
            path,
            num_dashes=25,
            color=GREEN_C,
            stroke_width=2.5
        )

        self.play(Create(dash), run_time=0.5)
        arrow_head = Arrow(
            p3, p4,
            buff=0,
            color=GREEN_C,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.4
        )

        self.play(GrowArrow(arrow_head), run_time=0.3)

        # ── NODE 8: LLM Brain ─────────────────────────────────────────────
        brain_c = Circle(
            radius=0.48,
            fill_color=PURPLE_C, fill_opacity=0.90,
            stroke_color=W, stroke_width=2.5
        )
        brain_c.move_to([llm_x, llm_y, 0])

        # neural net inside
        npos = [UP*0.22, DOWN*0.22, LEFT*0.28,
                RIGHT*0.28, UP*0.09+LEFT*0.15,
                DOWN*0.09+RIGHT*0.15]
        nd = VGroup(*[
            Dot(radius=0.050, color=W, fill_opacity=1.0
                ).move_to(brain_c.get_center()+p)
            for p in npos
        ])
        nl = VGroup(
            Line(nd[0].get_center(), nd[2].get_center(),
                 color=MINT_C, stroke_width=1.4),
            Line(nd[0].get_center(), nd[3].get_center(),
                 color=MINT_C, stroke_width=1.4),
            Line(nd[1].get_center(), nd[2].get_center(),
                 color=MINT_C, stroke_width=1.4),
            Line(nd[1].get_center(), nd[3].get_center(),
                 color=MINT_C, stroke_width=1.4),
            Line(nd[4].get_center(), nd[5].get_center(),
                 color=MINT_C, stroke_width=1.4),
        )
        llm_lbl  = lbl("LLM", sz=14)
        llm_slbl = sub("Generation", sz=10)
        llm_lbl.next_to(brain_c, DOWN, buff=0.08)
        llm_slbl.next_to(llm_lbl, DOWN, buff=0.05)
        brain_grp = VGroup(brain_c, nd, nl, llm_lbl, llm_slbl)

        self.play(GrowFromCenter(brain_c), run_time=0.65)
        self.play(FadeIn(nd), Create(nl),
                  FadeIn(llm_lbl, llm_slbl), run_time=0.5)

        # neural pulse × 3
        for _ in range(3):
            self.play(nl.animate.set_color(GOLD_C),  run_time=0.20)
            self.play(nl.animate.set_color(MINT_C),  run_time=0.20)

        # Curved arrow: User Query  →  LLM
        arr_q = CurvedArrow(
            q_grp.get_bottom() + DOWN*0.05,
            brain_c.get_left() + LEFT*0.05,
            color=TEAL_C, stroke_width=2.5,
            angle=-TAU/6
        )
        # Straight arrow: top-k dash  →  LLM top
        arr_ck = arr(
            [llm_x, llm_y+0.80, 0],
            [llm_x, llm_y+0.70, 0],
            color=GREEN_C, sw=2.5
        )
        self.play(Create(arr_q), run_time=0.6)
        self.play(GrowArrow(arr_ck), run_time=0.35)

        # ── NODE 9: Response ───────────────────────────────────────────────
        # Place it to the right of LLM, clamped within frame
        # resp_x = min(llm_x + 1.3, 6.2)   # safe upper bound
        # resp_y = llm_y
        
        resp_x = llm_x + 1.6
        resp_y = llm_y
        
        resp = RoundedRectangle(
            corner_radius=0.13, width=1.3, height=0.70,
            fill_color=TEAL_C, fill_opacity=0.92,
            stroke_color=MINT_C, stroke_width=3
        )
        resp.move_to([resp_x, resp_y, 0])

        chk      = Text("✓", font_size=28, color=W, weight=BOLD)
        chk.move_to(resp.get_center() + UP*0.08)
        resp_lbl = lbl("Response", sz=14)
        resp_sub = sub("Cited Answer", sz=10)
        resp_lbl.next_to(resp, DOWN, buff=0.08)
        resp_sub.next_to(resp_lbl, DOWN, buff=0.05)

        arr_br = arr(
            brain_c.get_right() + RIGHT*0.05,
            resp.get_left()      + LEFT*0.05,
            color=MINT_C, sw=4
        )
        self.play(GrowArrow(arr_br), run_time=0.42)
        self.play(FadeIn(resp, scale=0.8), run_time=0.52)
        self.play(Write(chk), run_time=0.38)
        self.play(FadeIn(resp_lbl, resp_sub), run_time=0.32)

        # glow flash
        self.play(resp.animate.set_stroke(W, 5),      run_time=0.22)
        self.play(resp.animate.set_stroke(MINT_C, 3), run_time=0.22)

        # save for replay
        self._ret_ban   = ret_ban
        self._q_grp     = q_grp
        self._qe_grp    = qe_grp
        self._db7_grp   = db7_grp
        self._bars      = bars
        self._dash      = dash
        self._brain_c   = brain_c
        self._brain_grp = brain_grp
        self._resp      = resp
        self._arr_br    = arr_br
        self._arr_q     = arr_q
        self._arr_ck    = arr_ck
        self._aq1 = aq1; self._aq2 = aq2; self._aq3 = aq3

        self.wait(0.8)

    # ═══════════════════════════════════════════════════════════════════════
    # S4  PARTICLE REPLAY
    # ═══════════════════════════════════════════════════════════════════════
    def _s4_replay(self):
        replay_lbl = Text("Full Pipeline Flow →",
                          font_size=18, color=GOLD_C, weight=BOLD)
        replay_lbl.to_edge(DOWN, buff=0.20)
        self.play(FadeIn(replay_lbl, shift=UP*0.18), run_time=0.38)

        particle = Dot(radius=0.14, color=GOLD_C, fill_opacity=1)
        glow     = Circle(radius=0.22, color=GOLD_C,
                          stroke_width=2, fill_opacity=0,
                          stroke_opacity=0.75)

        waypoints = [
            self._doc_grp.get_center(),
            self._ck_grp.get_center(),
            self._em_grp.get_center(),
            self._db4_grp.get_center(),
            self._big_a.get_center(),
            self._q_grp.get_center(),
            self._qe_grp.get_center(),
            self._db7_grp.get_center(),
            self._bars.get_center(),
            self._brain_c.get_center(),
            self._resp.get_center(),
        ]

        particle.move_to(waypoints[0])
        glow.move_to(waypoints[0])
        self.add(particle, glow)

        for wp in waypoints[1:]:
            self.play(
                particle.animate.move_to(wp),
                glow.animate.move_to(wp),
                run_time=0.40, rate_func=smooth
            )
            ripple = Circle(radius=0.22, color=GOLD_C,
                            stroke_width=2, fill_opacity=0)
            ripple.move_to(wp)
            self.add(ripple)
            self.play(
                ripple.animate.scale(2.2).set_stroke(opacity=0),
                run_time=0.20
            )
            self.remove(ripple)

        self.play(
            Flash(self._resp.get_center(),
                  color=MINT_C, num_lines=14,
                  line_length=0.40, flash_radius=0.70),
            self._resp.animate.set_stroke(W, 6),
            run_time=0.52
        )
        self.play(self._resp.animate.set_stroke(MINT_C, 3), run_time=0.22)
        self.play(FadeOut(particle, glow, replay_lbl), run_time=0.38)
        self.wait(0.5)

    # ═══════════════════════════════════════════════════════════════════════
    # S5  CLOSING CARD
    # ═══════════════════════════════════════════════════════════════════════
    def _s5_closing(self):
        # ✅ Group (not VGroup) handles all Mobject subtypes safely
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.15)

        b1 = Circle(radius=2.8, color=DKBLUE,
                    fill_opacity=0.20, stroke_width=0).shift(RIGHT*3.5+UP*1.2)
        b2 = Circle(radius=1.6, color=TEAL_C,
                    fill_opacity=0.14, stroke_width=0).shift(LEFT*3.5+DOWN*1)

        title = Text("RAG Pipeline", font_size=62, color=W, weight=BOLD)
        tag   = Text("AI grounded in YOUR data",
                     font_size=26, color=MINT_C)
        tag.next_to(title, DOWN, buff=0.38)

        uline = Line(title.get_left()+DOWN*0.06,
                     title.get_right()+DOWN*0.06,
                     color=TEAL_C, stroke_width=4)

        flow = Text(
            "Docs → Chunks → Embeddings → Vector DB → LLM → Response",
            font_size=16, color=LBLUE
        )
        flow.next_to(tag, DOWN, buff=0.52)

        bot = Rectangle(width=16, height=0.55,
                        fill_color=TEAL_C, fill_opacity=1,
                        stroke_width=0)
        bot.to_edge(DOWN, buff=0)
        bot_t = Text("Built with Manim  •  RAG Pipeline Explainer",
                     font_size=14, color=W)
        bot_t.move_to(bot.get_center())

        self.play(FadeIn(b1, b2), run_time=0.38)
        self.play(Write(title), run_time=0.95)
        self.play(Create(uline), run_time=0.42)
        self.play(FadeIn(tag,  shift=UP*0.22), run_time=0.60)
        self.play(FadeIn(flow, shift=UP*0.18), run_time=0.60)
        self.play(FadeIn(bot, bot_t), run_time=0.48)
        self.wait(2.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.75)