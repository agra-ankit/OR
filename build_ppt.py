"""
Builds the final presentation: Highway Risk Assessment using Monte Carlo Simulation
Operations Research Project - Topic 10
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

PLOTS = "plots"

# ── Colour palette ──────────────────────────────────────────────────────────
C_DARK    = RGBColor(0x0F, 0x17, 0x2A)   # near-black navy
C_WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
C_ACCENT  = RGBColor(0x38, 0xBD, 0xF8)   # sky blue  (headings)
C_RED     = RGBColor(0xDC, 0x26, 0x26)
C_GREEN   = RGBColor(0x10, 0xB9, 0x81)
C_YELLOW  = RGBColor(0xF5, 0x9E, 0x0B)
C_GRAY    = RGBColor(0x94, 0xA3, 0xB8)
C_LIGHT   = RGBColor(0xF1, 0xF5, 0xF9)   # slide background (light slides)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)


# ── Helpers ──────────────────────────────────────────────────────────────────

def new_prs():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank_slide(prs):
    blank_layout = prs.slide_layouts[6]          # truly blank
    return prs.slides.add_slide(blank_layout)


def bg(slide, color: RGBColor):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, l, t, w, h, fill_color=None, line_color=None, line_width=Pt(0)):
    shape = slide.shapes.add_shape(1, l, t, w, h)   # MSO_SHAPE_TYPE.RECTANGLE = 1
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = line_width
    else:
        shape.line.fill.background()
    return shape


def txb(slide, text, l, t, w, h,
        size=Pt(18), bold=False, color=C_WHITE,
        align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    p  = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size  = size
    run.font.bold  = bold
    run.font.color.rgb = color
    return tb


def bullet_box(slide, items, l, t, w, h,
               size=Pt(15), color=C_WHITE, head_color=C_ACCENT,
               title=None, title_size=Pt(17)):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True

    if title:
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = title
        r.font.size  = title_size
        r.font.bold  = True
        r.font.color.rgb = head_color

    for item in items:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.level = 0
        r = p.add_run()
        r.text = "  " + item
        r.font.size  = size
        r.font.bold  = False
        r.font.color.rgb = color
    return tb


def img(slide, path, l, t, w, h=None):
    if h:
        slide.shapes.add_picture(path, l, t, w, h)
    else:
        slide.shapes.add_picture(path, l, t, w)


def divider(slide, t, color=C_ACCENT, thickness=Pt(2)):
    ln = slide.shapes.add_connector(1, Inches(0.5), t, SLIDE_W - Inches(0.5), t)
    ln.line.color.rgb = color
    ln.line.width = thickness


# ── Slide builders ───────────────────────────────────────────────────────────

def slide_title(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)

    # left accent bar
    add_rect(s, Inches(0), Inches(0), Inches(0.08), SLIDE_H, fill_color=C_ACCENT)

    # top thin accent line
    add_rect(s, Inches(0.08), Inches(0), SLIDE_W, Inches(0.06), fill_color=C_ACCENT)

    txb(s, "OPERATIONS RESEARCH PROJECT",
        Inches(0.5), Inches(0.9), Inches(12), Inches(0.5),
        size=Pt(13), color=C_ACCENT, bold=True)

    txb(s, "Identification of High-Risk Zones\nin a National Highway Project",
        Inches(0.5), Inches(1.5), Inches(10), Inches(2.2),
        size=Pt(40), bold=True, color=C_WHITE)

    divider(s, Inches(3.9), C_ACCENT)

    txb(s, "Methodology:  Monte Carlo Simulation of Weather & Terrain Data\n"
           "Optimization: 0-1 Knapsack Mixed Integer Linear Programming (MILP)",
        Inches(0.5), Inches(4.1), Inches(11), Inches(1.2),
        size=Pt(16), color=C_GRAY)

    # bottom tag row
    for i, (label, val) in enumerate([
        ("CASE STUDY", "200 km Mountain Highway Corridor"),
        ("SIMULATIONS", "10,000 Monte Carlo Trials"),
        ("COURSE", "Operations Research  |  CSN13402(L)"),
    ]):
        lx = Inches(0.5 + i * 4.3)
        add_rect(s, lx, Inches(5.9), Inches(4.0), Inches(1.3),
                 fill_color=RGBColor(0x1E, 0x29, 0x3B))
        txb(s, label, lx + Inches(0.15), Inches(5.95), Inches(3.7), Inches(0.4),
            size=Pt(10), color=C_ACCENT, bold=True)
        txb(s, val,   lx + Inches(0.15), Inches(6.3),  Inches(3.7), Inches(0.6),
            size=Pt(13), color=C_WHITE)


def slide_problem(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "01  |  Problem Statement", Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    # left column
    bullet_box(s, [
        "A 200 km national highway cuts through steep mountain terrain",
        "Every monsoon season: landslides, rockfalls, and flash floods",
        "Roads blocked for 3–7 days → freight halted, lives at risk",
        "Annual repair & disruption cost: Crores of rupees",
    ], Inches(0.4), Inches(1.3), Inches(6.2), Inches(2.8),
       title="The Real-World Crisis", size=Pt(15))

    bullet_box(s, [
        "Reinforcing 1 km costs Rs. 15–25 Crores",
        "Total annual budget: only Rs. 60 Crores",
        "Cannot protect all 200 km — must prioritise",
        "Traditional methods use averages → miss extreme events",
    ], Inches(0.4), Inches(4.1), Inches(6.2), Inches(2.8),
       title="The Engineering Constraint", size=Pt(15))

    # right panel
    add_rect(s, Inches(6.9), Inches(1.3), Inches(6.0), Inches(5.8),
             fill_color=RGBColor(0x1E,0x29,0x3B))

    txb(s, "The Core Question", Inches(7.1), Inches(1.5), Inches(5.6), Inches(0.5),
        size=Pt(15), bold=True, color=C_ACCENT)
    txb(s, '"Given a limited budget of Rs. 60 Cr,\nwhich specific highway segments\nare most likely to collapse,\nand where should we invest first?"',
        Inches(7.1), Inches(2.0), Inches(5.6), Inches(2.2),
        size=Pt(17), color=C_WHITE, bold=True)

    divider(s, Inches(4.4), C_YELLOW, Pt(1))

    txb(s, "OR Solution", Inches(7.1), Inches(4.5), Inches(5.6), Inches(0.4),
        size=Pt(14), bold=True, color=C_YELLOW)
    txb(s, "Monte Carlo Simulation quantifies failure\nprobabilities for each segment.\n\n0-1 Knapsack MILP allocates the budget\nto maximise total risk reduction.",
        Inches(7.1), Inches(4.9), Inches(5.6), Inches(1.8),
        size=Pt(14), color=C_GRAY)


def slide_why_or(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "02  |  Why Operations Research?", Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    cols = [
        ("Deterministic Approach\n(Traditional)", C_RED, [
            "Uses average rainfall, slope, soil strength",
            "Gives one fixed risk estimate",
            "Ignores rare catastrophic 1-in-50 year storms",
            "Misses how multiple bad factors combine",
            "Cannot quantify probability or uncertainty",
        ]),
        ("Probabilistic OR Approach\n(Our Model)", C_GREEN, [
            "Models full range of rainfall, slope, soil",
            "Runs 10,000 simulated storm seasons",
            "Captures extreme tail-event cloudbursts",
            "Evaluates all 4 factors simultaneously",
            "Outputs failure probability & Value-at-Risk",
        ]),
    ]

    for i, (title, color, points) in enumerate(cols):
        lx = Inches(0.4 + i * 6.5)
        add_rect(s, lx, Inches(1.3), Inches(6.1), Inches(5.8),
                 fill_color=RGBColor(0x1E,0x29,0x3B))
        add_rect(s, lx, Inches(1.3), Inches(6.1), Inches(0.65), fill_color=color)
        txb(s, title, lx + Inches(0.15), Inches(1.35), Inches(5.8), Inches(0.6),
            size=Pt(15), bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
        bullet_box(s, points, lx + Inches(0.15), Inches(2.1),
                   Inches(5.8), Inches(4.5), size=Pt(14), color=C_GRAY)

    txb(s, "Central Limit: Disasters happen during extreme tails, not on average days.",
        Inches(0.4), Inches(7.1), Inches(12.5), Inches(0.35),
        size=Pt(13), color=C_YELLOW, bold=True, align=PP_ALIGN.CENTER)


def slide_factors(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "03  |  The 4 Hazard Factors & Their Distributions",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    factors = [
        ("Rainfall Intensity", "R", "Log-Normal (μ, σ)", C_ACCENT,
         "Cannot be negative. Extreme cloudbursts create a heavy right tail. High-altitude zones receive orographic rainfall."),
        ("Cut-Slope Angle", "θ", "Triangular (min, mode, max)", C_RED,
         "Survey gives min/most-likely/max degrees. Bounded by physical terrain limits. Steeper = higher gravitational shear force."),
        ("Soil & Rock Quality", "G", "Beta (α, β)  →  [0, 1]", C_YELLOW,
         "Naturally bounded between 0 (loose mud) and 1 (solid granite). Fractured shale zones have α < 2, β > 5 — peak near 0.2."),
        ("Drainage Deficit", "D", "Uniform (0, 0.4) choke rate", C_GREEN,
         "Culverts randomly choked by storm debris. Effective drainage = base capacity minus random blockage. Deficit = 1 − effective."),
    ]

    for i, (name, sym, dist, color, desc) in enumerate(factors):
        row = i // 2
        col = i % 2
        lx = Inches(0.4 + col * 6.45)
        ty = Inches(1.25 + row * 2.9)

        add_rect(s, lx, ty, Inches(6.1), Inches(2.65), fill_color=RGBColor(0x1E,0x29,0x3B))
        add_rect(s, lx, ty, Inches(0.55), Inches(2.65), fill_color=color)

        txb(s, sym, lx + Inches(0.08), ty + Inches(0.6), Inches(0.4), Inches(0.9),
            size=Pt(26), bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

        txb(s, name, lx + Inches(0.65), ty + Inches(0.08), Inches(5.3), Inches(0.45),
            size=Pt(16), bold=True, color=color)
        txb(s, "Distribution: " + dist,
            lx + Inches(0.65), ty + Inches(0.52), Inches(5.3), Inches(0.4),
            size=Pt(12), color=C_YELLOW, bold=False)
        txb(s, desc, lx + Inches(0.65), ty + Inches(0.95), Inches(5.3), Inches(1.6),
            size=Pt(12.5), color=C_GRAY)


def slide_slope(prs):
    s = blank_slide(prs)
    bg(s, C_LIGHT)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=C_DARK)
    txb(s, "04  |  What Is 'Slope'? Cut-Slope vs Road Gradient",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    img(s, os.path.join(PLOTS, "fig5_slope_cross_section.png"),
        Inches(0.3), Inches(1.2), Inches(7.5), Inches(5.9))

    bullet_box(s, [
        "Road gradient: 3°–5° — engineered flat so trucks can climb",
        "Cut-slope: 45°–65° — the mountain cliff carved beside the road",
        "Road gradient is controlled. Cut-slope is natural and cannot be flattened",
        "Rainfall saturates the cut-slope → pore-water pressure rises → shear strength drops → COLLAPSE",
        "In our model, 'slope' always refers to the cut-slope angle (θ)",
    ], Inches(8.1), Inches(1.4), Inches(4.9), Inches(5.5),
       title="Key Distinction", size=Pt(13.5), color=C_DARK, head_color=C_RED)


def slide_methodology(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "04  |  Monte Carlo Simulation Methodology",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    # Flow boxes
    steps = [
        ("1", "Define Corridor", "20 segments × 10 km each\nTerrain & weather parameters"),
        ("2", "AHP Weights", "Pairwise comparison matrix\nEigenvector → w_R, w_S, w_G, w_D"),
        ("3", "Draw Random Values", "Sample Rain, Slope,\nSoil, Drainage from distributions"),
        ("4", "Compute CRI", "CRI = Σ wᵢ × normalised factor\nRange: 0 (safe) to 1 (extreme)"),
        ("5", "Check Threshold", "If CRI > 0.65 → Failure\nRecord closure days & loss"),
        ("6", "Repeat × 10,000", "Tally: P(Failure), VaR-95\nExpected Annual Loss"),
    ]

    for i, (num, title, body) in enumerate(steps):
        col = i % 3
        row = i // 3
        lx = Inches(0.35 + col * 4.3)
        ty = Inches(1.25 + row * 2.8)

        add_rect(s, lx, ty, Inches(4.0), Inches(2.5), fill_color=RGBColor(0x1E,0x29,0x3B))
        add_rect(s, lx, ty, Inches(0.55), Inches(2.5), fill_color=C_ACCENT)
        txb(s, num, lx + Inches(0.05), ty + Inches(0.7), Inches(0.45), Inches(0.8),
            size=Pt(24), bold=True, color=C_DARK, align=PP_ALIGN.CENTER)
        txb(s, title, lx + Inches(0.65), ty + Inches(0.12), Inches(3.2), Inches(0.5),
            size=Pt(15), bold=True, color=C_ACCENT)
        txb(s, body,  lx + Inches(0.65), ty + Inches(0.65), Inches(3.2), Inches(1.7),
            size=Pt(13), color=C_GRAY)

    # Formula bar at bottom
    add_rect(s, Inches(0.35), Inches(6.9), Inches(12.63), Inches(0.5),
             fill_color=RGBColor(0x0C,0x4A,0x6E))
    txb(s, "CRI = 0.394·R̃  +  0.285·θ̃  +  0.205·(1−G̃)  +  0.116·(1−D̃)        Failure when CRI > 0.65",
        Inches(0.5), Inches(6.92), Inches(12.3), Inches(0.45),
        size=Pt(14), bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)


def slide_ahp(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "05  |  AHP Multi-Criteria Weighting",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    # Pairwise matrix table header
    txb(s, "Pairwise Comparison Matrix (Saaty 1–9 Scale):",
        Inches(0.4), Inches(1.2), Inches(7), Inches(0.4),
        size=Pt(14), bold=True, color=C_YELLOW)

    headers = ["Criterion", "Rainfall", "Slope", "Soil", "Drainage", "Weight"]
    rows_data = [
        ["Rainfall",  "1.0",    "1.5",    "2.0",    "3.0",    "39.4%"],
        ["Slope",     "0.67",   "1.0",    "1.5",    "2.5",    "28.5%"],
        ["Soil",      "0.50",   "0.67",   "1.0",    "2.0",    "20.5%"],
        ["Drainage",  "0.33",   "0.40",   "0.50",   "1.0",    "11.6%"],
    ]

    col_w = [Inches(1.6), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]
    col_x = [Inches(0.4)]
    for w in col_w[:-1]:
        col_x.append(col_x[-1] + w)

    # Header row
    for j, (h, cx, cw) in enumerate(zip(headers, col_x, col_w)):
        add_rect(s, cx, Inches(1.65), cw, Inches(0.42), fill_color=C_ACCENT)
        txb(s, h, cx + Inches(0.05), Inches(1.67), cw, Inches(0.38),
            size=Pt(12), bold=True, color=C_DARK, align=PP_ALIGN.CENTER)

    # Data rows
    row_colors = [RGBColor(0x1E,0x29,0x3B), RGBColor(0x0F,0x17,0x2A)]
    for ri, row in enumerate(rows_data):
        ty = Inches(2.07 + ri * 0.44)
        for j, (cell, cx, cw) in enumerate(zip(row, col_x, col_w)):
            fill = row_colors[ri % 2]
            if j == len(row) - 1:
                fill = RGBColor(0x06,0x4E,0x3B)  # green tint for weight col
            add_rect(s, cx, ty, cw, Inches(0.42), fill_color=fill)
            color = C_GREEN if j == len(row) - 1 else C_GRAY
            txb(s, cell, cx + Inches(0.05), ty + Inches(0.04), cw, Inches(0.35),
                size=Pt(12.5), color=color, align=PP_ALIGN.CENTER, bold=(j==len(row)-1))

    # Weight bars on right
    txb(s, "Derived Criteria Weights:", Inches(7.5), Inches(1.2), Inches(5.4), Inches(0.4),
        size=Pt(14), bold=True, color=C_YELLOW)

    weight_data = [
        ("Rainfall", 39.4, C_ACCENT),
        ("Slope",    28.5, C_RED),
        ("Soil",     20.5, C_YELLOW),
        ("Drainage", 11.6, C_GREEN),
    ]
    for i, (name, pct, color) in enumerate(weight_data):
        ty = Inches(1.75 + i * 0.72)
        txb(s, name, Inches(7.5), ty, Inches(1.4), Inches(0.4),
            size=Pt(13), color=C_GRAY)
        bar_w = Inches(pct / 100 * 4.5)
        add_rect(s, Inches(9.0), ty + Inches(0.06), bar_w, Inches(0.32), fill_color=color)
        txb(s, f"{pct}%", Inches(9.0) + bar_w + Inches(0.08), ty, Inches(0.6), Inches(0.4),
            size=Pt(13), bold=True, color=color)

    # Note
    txb(s, "Weights computed using the principal eigenvector of the pairwise matrix.\n"
           "Consistency verified via Saaty's Consistency Ratio (CR < 0.10).",
        Inches(0.4), Inches(4.0), Inches(12.5), Inches(0.7),
        size=Pt(13), color=C_GRAY)

    # Sensitivity figure
    img(s, os.path.join(PLOTS, "fig3_sensitivity_analysis.png"),
        Inches(0.4), Inches(4.8), Inches(12.5), Inches(2.4))


def slide_results(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "06  |  Simulation Results — Corridor Risk Profile",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    img(s, os.path.join(PLOTS, "fig1_corridor_risk_profile.png"),
        Inches(0.3), Inches(1.15), Inches(9.4), Inches(6.1))

    # Stats panel
    stats = [
        ("3",  "High-Risk Segments",  C_RED),
        ("4",  "Medium-Risk Segments", C_YELLOW),
        ("13", "Low-Risk Segments",    C_GREEN),
    ]
    for i, (num, label, color) in enumerate(stats):
        ty = Inches(1.3 + i * 1.4)
        add_rect(s, Inches(9.9), ty, Inches(3.1), Inches(1.1),
                 fill_color=RGBColor(0x1E,0x29,0x3B))
        add_rect(s, Inches(9.9), ty, Inches(0.08), Inches(1.1), fill_color=color)
        txb(s, num,   Inches(10.1), ty + Inches(0.05), Inches(1.0), Inches(0.55),
            size=Pt(32), bold=True, color=color)
        txb(s, label, Inches(10.1), ty + Inches(0.6), Inches(2.9), Inches(0.42),
            size=Pt(13), color=C_GRAY)

    add_rect(s, Inches(9.9), Inches(5.5), Inches(3.1), Inches(1.65),
             fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "Critical Segments",
        Inches(10.0), Inches(5.55), Inches(3.0), Inches(0.35),
        size=Pt(13), bold=True, color=C_ACCENT)
    crit = [
        ("Seg 12 — Cloudburst Canyon",  "P = 31.0%", C_RED),
        ("Seg 7  — Fractured Fault Zone","P = 28.1%", C_RED),
        ("Seg 6  — Mountain Pass Summit","P = 16.6%", C_RED),
    ]
    for j, (name, pf, col) in enumerate(crit):
        ty = Inches(5.9 + j * 0.42)
        txb(s, f"• {name}  ({pf})",
            Inches(10.0), ty, Inches(3.0), Inches(0.4),
            size=Pt(11.5), color=col)


def slide_monte_carlo(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "07  |  Monte Carlo Distributions & Value-at-Risk",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    img(s, os.path.join(PLOTS, "fig2_monte_carlo_distributions.png"),
        Inches(0.3), Inches(1.15), Inches(9.4), Inches(5.5))

    bullet_box(s, [
        "PDF: Segment 1 (green) safely below threshold",
        "Segment 7 (red) has a fat tail beyond τ = 0.65",
        "VaR-95 = 0.82 for Seg 7: worst 5% of storms cause catastrophic damage",
        "CDF shaded region = 28.1% failure probability",
        "10,000 trials capture rare 1-in-50-yr cloudburst events",
    ], Inches(9.9), Inches(1.3), Inches(3.1), Inches(5.3),
       title="Key Insights", size=Pt(12.5), color=C_GRAY, head_color=C_YELLOW)


def slide_optimization(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "08  |  0-1 Knapsack MILP — Budget Optimization",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    img(s, os.path.join(PLOTS, "fig4_budget_optimization.png"),
        Inches(0.3), Inches(1.15), Inches(9.4), Inches(5.9))

    bullet_box(s, [
        "Maximize total risk reduction subject to Rs. 60 Cr budget constraint",
        "xᵢ ∈ {0,1}: binary — either fully fund a segment or skip it",
        "Solver: SciPy MILP (Branch-and-Bound)",
        "Funded: Seg 12 (Rs. 21 Cr) + Seg 7 (Rs. 22 Cr) + Seg 11 (Rs. 16.5 Cr)",
        "Total spent: Rs. 59.5 Cr  |  Risk reduced by 55.5%",
        "Mitigation efficiency: 85% failure risk eliminated per funded segment",
    ], Inches(9.9), Inches(1.3), Inches(3.1), Inches(5.5),
       title="Optimization Details", size=Pt(12), color=C_GRAY, head_color=C_YELLOW)


def slide_implications(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "09  |  Managerial Implications",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    panels = [
        ("High-Risk Zones (Red)", C_RED, [
            "Segments 6, 7, 12",
            "Immediate structural intervention",
            "Anchored retaining walls, rock-shed galleries",
            "Geo-mesh netting on exposed cut-slopes",
            "Deep reinforced culvert reconstruction",
        ]),
        ("Medium-Risk Zones (Yellow)", C_YELLOW, [
            "Segments 5, 8, 10, 11",
            "IoT slope displacement sensors",
            "Prepositioned earthmoving machinery",
            "Pre-monsoon culvert clearing drives",
            "Variable message signs for traffic alerts",
        ]),
        ("Low-Risk Zones (Green)", C_GREEN, [
            "Segments 1–4, 9, 13–20",
            "Standard periodic maintenance",
            "Annual drainage inspection",
            "No major capital intervention needed",
            "Redirect savings to High/Medium zones",
        ]),
    ]

    for i, (title, color, points) in enumerate(panels):
        lx = Inches(0.35 + i * 4.3)
        add_rect(s, lx, Inches(1.25), Inches(4.1), Inches(5.9),
                 fill_color=RGBColor(0x1E,0x29,0x3B))
        add_rect(s, lx, Inches(1.25), Inches(4.1), Inches(0.55), fill_color=color)
        txb(s, title, lx + Inches(0.1), Inches(1.3), Inches(3.9), Inches(0.45),
            size=Pt(14), bold=True, color=C_WHITE)
        bullet_box(s, points, lx + Inches(0.1), Inches(1.9),
                   Inches(3.9), Inches(5.0), size=Pt(13.5), color=C_GRAY)


def slide_conclusion(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(1.1), fill_color=RGBColor(0x1E,0x29,0x3B))
    txb(s, "10  |  Conclusion & Future Scope",
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.7),
        size=Pt(26), bold=True, color=C_ACCENT)

    bullet_box(s, [
        "Monte Carlo simulation with 10,000 trials successfully identified 3 critical high-risk zones",
        "AHP-derived weights provided scientifically defensible multi-criteria prioritisation",
        "0-1 Knapsack MILP optimally allocated Rs. 59.5 Cr achieving 55.5% system risk reduction",
        "Value-at-Risk (VaR-95) planning metric identified catastrophic storm thresholds per segment",
        "Model is extensible: pre-construction route comparison or post-construction maintenance planning",
    ], Inches(0.4), Inches(1.3), Inches(12.5), Inches(2.8),
       title="Summary of Contributions", size=Pt(14.5), color=C_GRAY)

    divider(s, Inches(4.4), C_ACCENT, Pt(1))

    bullet_box(s, [
        "Real-time IoT sensor data feed (slope displacement, soil moisture, rainfall radar)",
        "Dynamic vehicle rerouting optimization across alternate arterial networks",
        "Multi-hazard model extension: earthquakes, snowmelt, and traffic load cycles",
        "Machine learning integration for real-time CRI updating during active storm events",
    ], Inches(0.4), Inches(4.6), Inches(12.5), Inches(2.4),
       title="Future Scope", size=Pt(14.5), color=C_GRAY, head_color=C_YELLOW)


def slide_thankyou(prs):
    s = blank_slide(prs)
    bg(s, C_DARK)
    add_rect(s, Inches(0), Inches(0), Inches(0.08), SLIDE_H, fill_color=C_ACCENT)
    add_rect(s, Inches(0.08), Inches(0), SLIDE_W, Inches(0.06), fill_color=C_ACCENT)

    txb(s, "Thank You",
        Inches(0.5), Inches(1.8), Inches(12), Inches(1.8),
        size=Pt(64), bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)

    divider(s, Inches(3.8), C_ACCENT)

    txb(s, "Operations Research Project  |  Topic 10\n"
           "Monte Carlo Simulation for Highway High-Risk Zone Identification",
        Inches(0.5), Inches(4.0), Inches(12.3), Inches(0.9),
        size=Pt(16), color=C_GRAY, align=PP_ALIGN.CENTER)

    txb(s, "Open for Questions",
        Inches(0.5), Inches(5.1), Inches(12.3), Inches(0.6),
        size=Pt(20), bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)

    # small key results reminder
    kpis = [
        ("3 Segments", "High-Risk (Red Zone)", C_RED),
        ("28,050 / 100,000", "Failure Trials (Seg 7+12)", C_YELLOW),
        ("55.5% Reduction", "System Risk Post-Mitigation", C_GREEN),
        ("Rs. 59.5 Cr", "Optimal Budget Allocation", C_ACCENT),
    ]
    for i, (val, label, color) in enumerate(kpis):
        lx = Inches(0.5 + i * 3.2)
        add_rect(s, lx, Inches(5.9), Inches(3.0), Inches(1.3),
                 fill_color=RGBColor(0x1E,0x29,0x3B))
        txb(s, val,   lx + Inches(0.1), Inches(5.95), Inches(2.8), Inches(0.5),
            size=Pt(16), bold=True, color=color)
        txb(s, label, lx + Inches(0.1), Inches(6.42), Inches(2.8), Inches(0.4),
            size=Pt(11), color=C_GRAY)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    prs = new_prs()

    print("Building slides...")
    slide_title(prs);        print("  [1/12] Title slide")
    slide_problem(prs);      print("  [2/12] Problem statement")
    slide_why_or(prs);       print("  [3/12] Why OR?")
    slide_factors(prs);      print("  [4/12] 4 Hazard factors")
    slide_methodology(prs);  print("  [5/12] Methodology flow")
    slide_ahp(prs);          print("  [6/12] AHP weights")
    slide_results(prs);      print("  [7/12] Corridor risk profile")
    slide_monte_carlo(prs);  print("  [8/12] Monte Carlo distributions")
    slide_optimization(prs); print("  [9/12] Budget optimization")
    slide_implications(prs); print(" [10/12] Managerial implications")
    slide_conclusion(prs);   print(" [11/12] Conclusion")
    slide_thankyou(prs);     print(" [12/12] Thank You")

    out = "Highway_Risk_Assessment_OR_Project_v2.pptx"
    prs.save(out)
    print(f"\nPresentation saved: {out}")
    print(f"Slides: {len(prs.slides)}  |  Open in PowerPoint or upload to Google Slides.")


if __name__ == "__main__":
    main()
