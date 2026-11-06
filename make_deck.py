from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ---------- palette (minimal corporate) ----------
NAVY   = RGBColor(0x1F, 0x3A, 0x5F)
INK    = RGBColor(0x22, 0x30, 0x3C)
GREY   = RGBColor(0x5A, 0x6B, 0x7B)
LIGHT  = RGBColor(0xE8, 0xEC, 0xF0)
AMBER  = RGBColor(0xC8, 0x96, 0x3E)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Calibri"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height

def add_slide():
    return prs.slides.add_slide(BLANK)

def rect(slide, x, y, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def txt(slide, x, y, w, h, runs_lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(runs_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        for t, sz, bold, col, *rest in line:
            r = p.add_run(); r.text = t
            r.font.name = FONT; r.font.size = Pt(sz); r.font.bold = bold
            r.font.color.rgb = col
            if rest and rest[0]:
                r.font.italic = True
    return tb

def bullets(slide, x, y, w, h, items, size=14, gap=8, color=INK, lead_color=NAVY):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r0 = p.add_run(); r0.text = "\u2013  "
        r0.font.name = FONT; r0.font.size = Pt(size); r0.font.color.rgb = lead_color; r0.font.bold = True
        if isinstance(it, tuple):
            lead, rest = it
            r1 = p.add_run(); r1.text = lead
            r1.font.name = FONT; r1.font.size = Pt(size); r1.font.bold = True; r1.font.color.rgb = NAVY
            r2 = p.add_run(); r2.text = rest
            r2.font.name = FONT; r2.font.size = Pt(size); r2.font.color.rgb = color
        else:
            r1 = p.add_run(); r1.text = it
            r1.font.name = FONT; r1.font.size = Pt(size); r1.font.color.rgb = color
    return tb

def header(slide, kicker, title):
    rect(slide, 0, 0, SW, Inches(0.06), NAVY)
    txt(slide, Inches(0.6), Inches(0.32), Inches(11.5), Inches(0.3),
        [[(kicker.upper(), 11, True, GREY)]])
    txt(slide, Inches(0.6), Inches(0.58), Inches(12.1), Inches(0.7),
        [[(title, 27, True, NAVY)]])
    rect(slide, Inches(0.62), Inches(1.28), Inches(0.9), Inches(0.03), AMBER)

def footer(slide, n):
    txt(slide, Inches(0.6), Inches(7.08), Inches(9), Inches(0.3),
        [[("Principles of Statistical Mechanics in Modelling Biocatalysts", 9, False, GREY)]])
    txt(slide, Inches(12.3), Inches(7.08), Inches(0.5), Inches(0.3),
        [[(str(n), 9, False, GREY)]], align=PP_ALIGN.RIGHT)

def pic(slide, path, x, y, w):
    return slide.shapes.add_picture(path, x, y, width=w)

# ================= SLIDE 1 - TITLE =================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
rect(s, 0, 0, Inches(0.18), SH, NAVY)
txt(s, Inches(1.0), Inches(2.15), Inches(11), Inches(0.4),
    [[("SEMINAR PRESENTATION", 12, True, AMBER)]])
txt(s, Inches(1.0), Inches(2.55), Inches(11.4), Inches(1.6),
    [[("Principles of Statistical Mechanics in", 34, True, NAVY)],
     [("Modelling Biocatalysts", 34, True, NAVY)]])
txt(s, Inches(1.0), Inches(4.05), Inches(10.5), Inches(0.8),
    [[("From molecular ensembles to catalytic rates \u2014 connecting equilibrium and", 14, False, GREY)],
     [("non-equilibrium statistical mechanics with enzyme kinetics and simulation.", 14, False, GREY)]])
rect(s, Inches(1.0), Inches(5.0), Inches(2.2), Inches(0.02), LIGHT)
txt(s, Inches(1.0), Inches(5.2), Inches(8), Inches(1.2),
    [[("Presented by:  [Your Name]", 13, True, INK)],
     [("Supervisor:  [Professor\u2019s Name]", 12, False, GREY)],
     [("Department / Institute  \u2022  November 2026", 12, False, GREY)]])

# ================= SLIDE 2 - OUTLINE =================
s = add_slide()
header(s, "Presentation outline", "Structure of the Talk")
left_items = [
    ("1.  Motivation", ""), ("2.  Background", ""), ("3.  Core concepts of the theory", ""),
    ("4.  Governing equations & key parameters", ""), ("5.  Model scenarios", ""),
]
right_items = [
    ("6.  Applications to biocatalysis", ""), ("7.  Comparison with other subject areas", ""),
    ("8.  Limitations", ""), ("9.  Key takeaways & references", ""),
]
bullets(s, Inches(0.9), Inches(1.9), Inches(5.6), Inches(4.5), left_items, size=16, gap=16)
bullets(s, Inches(6.9), Inches(1.9), Inches(5.6), Inches(4.5), right_items, size=16, gap=16)
footer(s, 2)

# ================= SLIDE 3 - MOTIVATION =================
s = add_slide()
header(s, "Motivation", "Why Statistical Mechanics for Biocatalysis?")
bullets(s, Inches(0.7), Inches(1.75), Inches(7.1), Inches(4.9), [
    ("Enzymes are not static machines. ", "A biocatalyst samples many conformations; its function is an ensemble property, not a single-structure property."),
    ("Rates emerge from molecular statistics. ", "Catalytic turnover k_cat is set by free-energy differences and barrier crossings \u2014 quantities defined by Boltzmann statistics."),
    ("Bulk kinetics hides fluctuations. ", "Michaelis\u2013Menten kinetics averages over ~10^17 molecules; single-enzyme experiments show memory and dynamic disorder that only stochastic theory captures."),
    ("Design needs predictive thermodynamics. ", "Protein engineering and artificial enzymes require linking sequence \u2192 ensemble \u2192 \u0394G\u207d\u2071 \u2192 rate, which is exactly the domain of statistical mechanics."),
], size=14.5, gap=12)
rect(s, Inches(8.2), Inches(1.8), Inches(4.4), Inches(4.7), LIGHT)
txt(s, Inches(8.5), Inches(2.05), Inches(3.9), Inches(0.4),
    [[("THE GAP WE ADDRESS", 11, True, NAVY)]])
bullets(s, Inches(8.5), Inches(2.5), Inches(3.85), Inches(3.8), [
    "Deterministic ODEs ignore thermal noise",
    "Static structures ignore conformational ensembles",
    "Fixed barriers ignore protein dynamics & tunnelling",
    "Continuum treatments lose solvent entropy effects",
], size=12.5, gap=10, color=INK)
footer(s, 3)

# ================= SLIDE 4 - BACKGROUND =================
s = add_slide()
header(s, "Background", "Biocatalysts as Statistical Systems")
bullets(s, Inches(0.7), Inches(1.7), Inches(6.9), Inches(5.0), [
    ("Biocatalysts: ", "enzymes, ribozymes, engineered proteins and nanozymes that accelerate reactions under mild conditions."),
    ("Hierarchy of scales: ", "\u00c5 (bond making/breaking) \u2192 nm (domain motions) \u2192 \u00b5s\u2013ms (conformational gating) \u2192 s (turnover)."),
    ("Energy landscape picture: ", "the protein has a rough, many-minima free-energy surface; catalysis is a rare transition between basins."),
    ("Thermodynamic anchors: ", "binding affinity K_d, \u0394G of ES/EP complexes, transition-state stabilisation \u2014 all ensemble averages."),
], size=14, gap=12)
pic(s, "/workspace/assets/landscape.png", Inches(7.7), Inches(1.95), Inches(5.1))
txt(s, Inches(7.7), Inches(5.15), Inches(5.1), Inches(0.9),
    [[("Fig. 1 \u2014 A biocatalyst populates substates E_i with Boltzmann weights; inter-basin hopping gates the catalytic step.", 11, False, GREY)]])
footer(s, 4)

# ================= SLIDE 5 - CORE CONCEPTS =================
s = add_slide()
header(s, "Core concepts", "Statistical-Mechanical Toolkit Used in the Models")
rows = [
    ("Ensembles (micro / canonical / grand)", "Fixes what is conserved; enzyme in solution \u2192 canonical ensemble at fixed T, V, \u03bc of bath species."),
    ("Partition function Z and free energy", "All observables derive from Z;  F = \u2212k_BT ln Z  connects microscopic states to measurable affinities."),
    ("Boltzmann weighting", "P(E_i) \u221d exp(\u2212\u03b2E_i) determines population of catalytically competent vs. inactive conformers."),
    ("Fluctuation\u2013dissipation & equipartition", "Thermal noise drives barrier crossings; relates friction (\u03b3) to diffusion (D = k_BT/\u03b3) in Kramers theory."),
    ("Entropy\u2013enthalpy compensation", "Binding and catalysis trade-off; conformational entropy loss offsets enthalpic gains on substrate capture."),
]
y = Inches(1.7)
for name, desc in rows:
    rect(s, Inches(0.7), y, Inches(0.05), Inches(0.86), AMBER)
    txt(s, Inches(0.95), y + Inches(0.02), Inches(4.6), Inches(0.9),
        [[(name, 13.5, True, NAVY)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(5.7), y + Inches(0.02), Inches(7.0), Inches(0.9),
        [[(desc, 12, False, INK)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.0)
footer(s, 5)

# ================= SLIDE 6 - THEORY I =================
s = add_slide()
header(s, "Theory used to model the system  (i)", "Equilibrium Statistics: Ensembles & Partition Functions")
bullets(s, Inches(0.7), Inches(1.7), Inches(6.6), Inches(4.9), [
    ("Canonical distribution ", "governs the enzyme + solvent bath at temperature T; \u03b2 = 1/k_BT."),
    ("Binding equilibria ", "follow from ratio of partition functions of complex vs. separated partners \u2014 e.g. quasi-chemical treatment of ligand binding."),
    ("Constrained / reaction-coordinate Z ", "isolates the chemistry step: integrate out all degrees of freedom except the progress coordinate \u03be."),
    ("Free-energy profiles ", "G(\u03be) = \u2212k_BT ln P(\u03be) + const \u2014 histograms from MD become potentials of mean force directly comparable to experiment."),
], size=14, gap=12)
pic(s, "/workspace/assets/boltzmann.png", Inches(7.6), Inches(1.9), Inches(5.1))
txt(s, Inches(7.6), Inches(5.35), Inches(5.1), Inches(0.8),
    [[("Fig. 2 \u2014 Higher temperature (smaller \u03b2) broadens state populations; catalysis depends on the tail that reaches the transition state.", 11, False, GREY)]])
footer(s, 6)

# ================= SLIDE 7 - THEORY II =================
s = add_slide()
header(s, "Theory used to model the system  (ii)", "Non-Equilibrium Statistics: Rate Theories")
bullets(s, Inches(0.7), Inches(1.7), Inches(6.6), Inches(4.9), [
    ("Eyring / Transition-State Theory: ", "assumes quasi-equilibrium between ES and the transition state; every crossing leads to product."),
    ("Kramers\u2019 extension: ", "in viscous (solvent-loaded) environments the barrier is recrossed; the rate acquires a transmission coefficient \u03ba < 1 set by friction \u03b3."),
    ("Dynamic prefactor idea: ", "protein motion along the reaction coordinate acts like an additional medium \u2014 enzymes interpolate between energy-diffusion and spatial-diffusion limits."),
    ("Master equations: ", "discrete kinetic networks (E \u2194 ES \u2194 EP \u2194 E) written as a Markov chain give full distributions, not just mean rates."),
], size=14, gap=12)
pic(s, "/workspace/assets/eyring.png", Inches(7.6), Inches(1.9), Inches(5.1))
txt(s, Inches(7.6), Inches(5.35), Inches(5.1), Inches(0.8),
    [[("Fig. 3 \u2014 Catalytic step as barrier crossing on a free-energy profile; TST counts crossings, Kramers corrects them.", 11, False, GREY)]])
footer(s, 7)

# ================= SLIDE 8 - EQUATIONS =================
s = add_slide()
header(s, "Governing equations", "Key Relations and Their Parameters")
eqs = [
    ("Boltzmann population", "P_i = exp(\u2212\u03b2E_i) / Z ,    Z = \u03a3_i exp(\u2212\u03b2E_i)",
     "\u03b2 = 1/k_BT sets resolution of states; Z encodes every thermodynamic observable."),
    ("Eyring TST rate", "k = \u03ba \u00b7 (k_BT/h) \u00b7 exp(\u2212\u0394G\u207d\u2071/RT)",
     "\u0394G\u207d\u2071: activation free energy; \u03ba: transmission coefficient (=1 in ideal TST)."),
    ("Kramers (high friction)", "k \u2248 (\u03c9_0\u03c9_TS / 2\u03c0\u03b3) \u00b7 exp(\u2212\u0394G\u207d\u2071/k_BT)",
     "\u03b3: friction from solvent/protein; \u03c9: curvatures of well and barrier \u2014 rate falls when motion slows."),
    ("Michaelis\u2013Menten (ensemble limit)", "v = V_max[S] / (K_m + [S])",
     "Emerges as the mean-field average of the master equation when fluctuations are neglected."),
]
y = Inches(1.62)
for name, eq, note in eqs:
    rect(s, Inches(0.7), y, Inches(11.95), Inches(1.18), LIGHT)
    txt(s, Inches(0.95), y + Inches(0.08), Inches(3.4), Inches(1.0),
        [[(name, 12.5, True, NAVY)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(4.35), y + Inches(0.08), Inches(4.6), Inches(1.0),
        [[(eq, 13, False, INK)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(8.95), y + Inches(0.08), Inches(3.5), Inches(1.0),
        [[(note, 10.5, False, GREY)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.32)
footer(s, 8)

# ================= SLIDE 9 - SCENARIOS =================
s = add_slide()
header(s, "Model scenarios", "Same Framework, Different Physical Regimes")
cols = [
    ("Dilute solution, fast equilibration", [
        "Standard TST + MM kinetics valid",
        "Rate controlled by \u0394G\u207d\u2071 alone",
        "Ensemble average \u2248 single molecule"
    ]),
    ("Crowded cellular milieu", [
        "Anomalous diffusion, \u03b3 effectively rises",
        "Substrate search becomes fractal-time",
        "Fractional master equations needed"
    ]),
    ("Single-enzyme observation", [
        "Kinetic memory / dynamic disorder",
        "Non-exponential waiting times",
        "Single-molecule kinetics \u2260 MM prediction"
    ]),
    ("Immobilised / surface enzymes", [
        "2-D diffusion + local pH gradients",
        "Ensemble heterogeneity in site energies",
        "Grand-canonical treatment of protons"
    ]),
]
x = Inches(0.7)
for title, items in cols:
    rect(s, x, Inches(1.75), Inches(2.85), Inches(0.5), NAVY)
    txt(s, x + Inches(0.12), Inches(1.75), Inches(2.6), Inches(0.5),
        [[(title, 12, True, WHITE)]], anchor=MSO_ANCHOR.MIDDLE)
    rect(s, x, Inches(2.32), Inches(2.85), Inches(3.6), LIGHT)
    bullets(s, x + Inches(0.15), Inches(2.5), Inches(2.6), Inches(3.3), items, size=11.5, gap=10, color=INK)
    x += Inches(3.13)
txt(s, Inches(0.7), Inches(6.2), Inches(11.9), Inches(0.6),
    [[("Each scenario changes which statistical-mechanical ingredient dominates \u2014 the barrier, the friction, or the ensemble spread itself.", 12.5, False, GREY, True)]])
footer(s, 9)

# ================= SLIDE 10 - APPLICATIONS =================
s = add_slide()
header(s, "Applications", "Where the Theory Is Actually Used")
bullets(s, Inches(0.7), Inches(1.7), Inches(6.9), Inches(4.9), [
    ("Enzyme engineering: ", "\u0394\u0394G\u207d\u2071 decomposition guides mutations; free-energy perturbation (FEP) predicts mutant activities before synthesis."),
    ("Drug design: ", "binding free energies (MM-PBSA, TI) rank inhibitors against the same ensemble machinery."),
    ("Artificial enzymes & nanozymes: ", "landscape design principles borrowed from natural catalysts set selectivity targets."),
    ("Biocatalysis in industry: ", "immobilised-lipase and cellulase process models use Kramers-type temperature dependence for reactor scale-up."),
    ("Simulations powering this: ", "MD + enhanced sampling (metadynamics, replica exchange) numerically evaluate the partition functions behind every number above."),
], size=13.5, gap=11)
pic(s, "/workspace/assets/mm.png", Inches(7.9), Inches(1.95), Inches(4.8))
txt(s, Inches(7.9), Inches(5.2), Inches(4.8), Inches(0.9),
    [[("Fig. 4 \u2014 The smooth MM hyperbola is the ensemble mean; single-molecule events fluctuate around it \u2014 captured only by stochastic models.", 11, False, GREY)]])
footer(s, 10)

# ================= SLIDE 11 - COMPARISONS =================
s = add_slide()
header(s, "Comparisons", "With Adjacent Subject Areas")
tbl_data = [
    ("Aspect", "Biocatalysis (this talk)", "Heterogeneous catalysis", "Soft-matter / polymer kinetics"),
    ("Energy source", "Protein fold landscape + solvent", "Surface electronic structure", "Chain entropy + confinement"),
    ("Rate theory", "Kramers / TST with dynamic \u03ba", "Arrhenius + microkinetic ODEs", "Rouse/Zimm + reptation models"),
    ("Ensemble role", "Conformational substates gate rate", "Site distribution on facets", "Relaxation-time spectrum"),
    ("Key parameter", "\u0394G\u207d\u2071, \u03b3 (friction)", "Adsorption energies", "Entanglement time \u03c4_e"),
]
widths = [Inches(1.9), Inches(3.5), Inches(3.2), Inches(3.35)]
x0, y0 = Inches(0.7), Inches(1.8)
row_h = Inches(0.78)
table = s.shapes.add_table(len(tbl_data), 4, x0, y0, Inches(11.95), row_h*len(tbl_data)).table
for j, w in enumerate(widths):
    table.columns[j].width = w
for i, row in enumerate(tbl_data):
    table.rows[i].height = row_h
    for j, val in enumerate(row):
        cell = table.cell(i, j)
        cell.margin_left = Inches(0.1); cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.04); cell.margin_bottom = Inches(0.04)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; r = p.add_run(); r.text = val
        r.font.name = FONT
        if i == 0:
            r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = WHITE
            cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        else:
            r.font.size = Pt(11.5); r.font.bold = (j == 0)
            r.font.color.rgb = NAVY if j == 0 else INK
            cell.fill.solid(); cell.fill.fore_color.rgb = WHITE if i % 2 else LIGHT
txt(s, Inches(0.7), Inches(6.05), Inches(11.9), Inches(0.7),
    [[("Shared mathematics, different physics: all three fields cross barriers on landscapes \u2014 but the origin of the barrier and of the friction differs.", 12, False, GREY, True)]])
footer(s, 11)

# ================= SLIDE 12 - LIMITATIONS =================
s = add_slide()
header(s, "Limitations", "Where the Current Models Break Down")
bullets(s, Inches(0.7), Inches(1.7), Inches(5.9), Inches(5.0), [
    ("Timescale gap: ", "chemically relevant events (ms\u2013s) exceed routine MD by orders of magnitude; sampling of the true ensemble is incomplete."),
    ("Force-field error: ", "\u0394G\u207d\u2071 from simulations carries 1\u20132 kcal/mol uncertainty \u2014 enough to shift predicted rates 10\u2013100\u00d7."),
    ("TST assumptions fail locally: ", "tunnelling (H-transfer), recrossing and quantum nuclear effects violate the classical barrier-crossing picture."),
    ("Coarse-graining loses detail: ", "Markov state models assume memoryless hops; kinetic memory contradicts this."),
], size=13.5, gap=12)
rect(s, Inches(6.9), Inches(1.75), Inches(5.75), Inches(4.6), LIGHT)
txt(s, Inches(7.15), Inches(1.95), Inches(5.3), Inches(0.4),
    [[("COMMONLY MADE ASSUMPTIONS", 11, True, NAVY)]])
bullets(s, Inches(7.15), Inches(2.4), Inches(5.3), Inches(3.8), [
    "Quasi-equilibrium along the reaction coordinate",
    "Linear response near equilibrium (fluctuation\u2013dissipation)",
    "Separation of fast solvent / slow protein timescales",
    "Harmonic wells around each basin",
    "Dilute-solution ideal behaviour of substrates",
], size=12.5, gap=10, color=INK)
footer(s, 12)

# ================= SLIDE 13 - KEY TAKEAWAYS =================
s = add_slide()
header(s, "Key takeaways", "Five Points to Remember")
takeaways = [
    "A biocatalyst is a statistical object: its rate is an ensemble property, governed by Boltzmann weights over conformational substates.",
    "The partition function is the bridge: everything measurable \u2014 affinity, specificity, k_cat \u2014 derives from ratios of state sums.",
    "Barrier crossing is the core event: Eyring TST gives the skeleton, Kramers friction and dynamic \u03ba give the flesh.",
    "Classical kinetics is the averaged limit: Michaelis\u2013Menten emerges only when fluctuations and memory are negligible.",
    "The framework transfers: the same landscape logic spans drug design, industrial biocatalysis and abiotic catalysis \u2014 within stated limitations.",
]
y = Inches(1.75)
for i, t in enumerate(takeaways, 1):
    rect(s, Inches(0.7), y, Inches(0.55), Inches(0.55), NAVY)
    txt(s, Inches(0.7), y, Inches(0.55), Inches(0.55),
        [[(str(i), 16, True, WHITE)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.5), y - Inches(0.03), Inches(11.1), Inches(0.85),
        [[(t, 13.5, False, INK)]], anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.98)
footer(s, 13)

# ================= SLIDE 14 - REFERENCES =================
s = add_slide()
header(s, "References", "Selected Sources")
refs = [
    "McQuarrie, J. D. (2000). Statistical Mechanics. University Science Books.",
    "Hill, T. L. (1987). Free Energy Transduction and Biochemical Cycle Kinetics. Dover Publications.",
    "Zwanzig, R. (2001). Nonequilibrium Statistical Mechanics. Oxford University Press.",
    "Kramers, H. A. (1940). Brownian motion in a field of force and the diffusion model of chemical reactions. Physica, 7(4), 284\u2013304.",
    "Eigen, M. (1996). Neurobiology and the central role of non-equilibrium thermodynamics. In: Foundations of Sensory Science.",
    "Min, W., Xie, X. S. (2004). Single-molecule enzyme kinetics and fluctuating enzymes. J. Phys. Chem. B, 108, 15742\u201315750.",
    "Warshel, A. et al. (2006). Empirical valence-bond methods as a general approach to enzymatic catalysis. Acc. Chem. Res., 39, 182\u2013191.",
    "English, B. P. et al. (2006). Ever-fluctuating single enzyme molecules. Proc. Natl. Acad. Sci., 103, 13093\u201313098.",
]
bullets(s, Inches(0.7), Inches(1.75), Inches(11.9), Inches(4.8), refs, size=12.5, gap=9, color=INK, lead_color=AMBER)
txt(s, Inches(0.7), Inches(6.35), Inches(11.9), Inches(0.5),
    [[("Thank you  \u2014  questions and discussion are welcome.", 14, True, NAVY)]])
footer(s, 14)

prs.save("/workspace/StatMech_Biocatalysis_Slides.pptx")
print("saved", len(prs.slides._sldIdLst), "slides")
