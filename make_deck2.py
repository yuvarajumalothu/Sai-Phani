from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

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
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = color
    sh.line.fill.background(); sh.shadow.inherit = False
    return sh

def txt(slide, x, y, w, h, runs_lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(runs_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        for run_spec in line:
            t, sz, bold, col = run_spec[:4]
            italic = run_spec[4] if len(run_spec) > 4 else False
            r = p.add_run(); r.text = t
            r.font.name = FONT; r.font.size = Pt(sz); r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = col
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
        [[(title, 26, True, NAVY)]])
    rect(slide, Inches(0.62), Inches(1.26), Inches(0.9), Inches(0.03), AMBER)

def footer(slide, n):
    txt(slide, Inches(0.6), Inches(7.08), Inches(9.5), Inches(0.3),
        [[("ML-Based Search for Superior Bio-mimetic Catalysts for CO\u2082 Capture & Conversion", 9, False, GREY)]])
    txt(slide, Inches(12.3), Inches(7.08), Inches(0.5), Inches(0.3),
        [[(str(n), 9, False, GREY)]], align=PP_ALIGN.RIGHT)

def pic(slide, path, x, y, w):
    return slide.shapes.add_picture(path, x, y, width=w)

# ================= SLIDE 1 - TITLE =================
s = add_slide()
rect(s, 0, 0, SW, SH, WHITE)
rect(s, 0, 0, Inches(0.18), SH, NAVY)
txt(s, Inches(1.0), Inches(1.95), Inches(11), Inches(0.4),
    [[("SEMINAR PRESENTATION", 12, True, AMBER)]])
txt(s, Inches(1.0), Inches(2.35), Inches(11.6), Inches(1.8),
    [[("Machine-Learning Based Search for Superior", 32, True, NAVY)],
     [("Bio-mimetic Catalysts for CO\u2082 Capture and Conversion", 32, True, NAVY)]])
txt(s, Inches(1.0), Inches(4.0), Inches(11.0), Inches(0.9),
    [[("Applying principles of statistical mechanics to literature-derived descriptors", 14, False, GREY)],
     [("(oxidation states, bond angles, activation energies, pH, yield %) with XGBoost and Random Forest models", 14, False, GREY)]])
rect(s, Inches(1.0), Inches(5.05), Inches(2.2), Inches(0.02), LIGHT)
txt(s, Inches(1.0), Inches(5.25), Inches(8), Inches(1.2),
    [[("Presented by:  [Your Name]", 13, True, INK)],
     [("Supervisor:  [Professor\u2019s Name]", 12, False, GREY)],
     [("Department / Institute  \u2022  November 2026", 12, False, GREY)]])

# ================= SLIDE 2 - OUTLINE =================
s = add_slide()
header(s, "Presentation outline", "Structure of the Talk")
left_items = [
    ("1.  Motivation", ""), ("2.  Background \u2014 CO\u2082 capture & bio-mimetic catalysts", ""),
    ("3.  Statistical mechanics in the project workflow", ""),
    ("4.  Equations, scenarios & parameters used", ""),
]
right_items = [
    ("5.  Data collection from literature", ""), ("6.  ML models \u2014 XGBoost & Random Forest", ""),
    ("7.  Comparison with other approaches", ""), ("8.  Limitations, key takeaways & references", ""),
]
bullets(s, Inches(0.9), Inches(1.9), Inches(5.8), Inches(4.5), left_items, size=16, gap=18)
bullets(s, Inches(6.9), Inches(1.9), Inches(5.8), Inches(4.5), right_items, size=16, gap=18)
footer(s, 2)

# ================= SLIDE 3 - MOTIVATION =================
s = add_slide()
header(s, "Motivation", "Why Search for Better CO\u2082 Catalysts with ML + Stat-Mech?")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.2), Inches(5.0), [
    ("CO\u2082 is abundant but inert. ", "Converting CO\u2082 into fuels and chemicals needs catalysts that work at mild temperature and pH with low activation barriers."),
    ("Enzymes already do it. ", "Carbonic anhydrase and formate dehydrogenase reach turnover numbers far beyond synthetic catalysts \u2014 bio-mimetic designs try to copy their active-site statistics."),
    ("Trial-and-error is too slow. ", "Thousands of metal centres, oxidation states and geometries exist in the literature; no lab can screen them all experimentally."),
    ("Data + physics-guided models can rank them. ", "Statistical mechanics tells us which microscopic descriptors (energy states, barriers, populations) actually control rates \u2014 those become the ML features."),
], size=14, gap=12)
rect(s, Inches(8.3), Inches(1.75), Inches(4.3), Inches(4.75), LIGHT)
txt(s, Inches(8.6), Inches(2.0), Inches(3.8), Inches(0.4),
    [[("OBJECTIVE OF THIS PROJECT", 11, True, NAVY)]])
bullets(s, Inches(8.6), Inches(2.45), Inches(3.75), Inches(3.9), [
    "Build a curated dataset from published catalyst studies",
    "Encode statistical-mechanic descriptors as features",
    "Train XGBoost / Random Forest to predict yield %",
    "Identify superior bio-mimetic candidates for CO\u2082 capture and conversion",
], size=12.5, gap=11, color=INK)
footer(s, 3)

# ================= SLIDE 4 - BACKGROUND =================
s = add_slide()
header(s, "Background", "Bio-mimetic Catalysts for CO\u2082 Capture and Conversion")
bullets(s, Inches(0.7), Inches(1.65), Inches(6.6), Inches(5.2), [
    ("Capture step: ", "amine-functionalised and metal\u2013organic sorbents bind CO\u2082; capacity depends on pH and metal oxidation state."),
    ("Conversion step: ", "electro-/photo-catalytic reduction to CO, formate or methanol through proton\u2013electron transfer sequences."),
    ("Bio-mimetic design: ", "metal\u2013nitrogen\u2013carbon (M\u2013N\u2013C) sites mimic enzyme active pockets \u2014 coordination number, bond angles and local electrostatics set the energetics."),
    ("Key performance metrics: ", "activation energy Ea, operating pH, Faradaic efficiency and product yield % \u2014 exactly the quantities reported across the literature we mined."),
], size=13.5, gap=11)
pic(s, "assets2/arrhenius.png", Inches(7.55), Inches(1.8), Inches(5.1))
txt(s, Inches(7.55), Inches(5.6), Inches(5.1), Inches(0.6),
    [[("Fig. 1  A catalyst that lowers E\u2090 wins at mild temperatures \u2014 the whole screening exercise revolves around this exponential factor.", 10, False, GREY)]])
footer(s, 4)

# ================= SLIDE 5 - STAT MECH ROLE (workflow) =================
s = add_slide()
header(s, "Theory used in the project", "Where Statistical Mechanics Enters the Pipeline")
pic(s, "assets2/workflow.png", Inches(0.75), Inches(1.6), Inches(11.8))
bullets(s, Inches(0.85), Inches(4.6), Inches(11.6), Inches(2.2), [
    ("Ensembles, not single structures: ", "a catalyst sample occupies many microstates; only Boltzmann-weighted averages are comparable with measured yields."),
    ("Partition function Z = \u03a3 exp(\u2212E\u1d62/k_BT): ", "converts computed state energies into populations, free energies \u0394G = \u2212k_BT ln Z and rate estimates \u2014 these become physics-based features."),
    ("Rate theories close the loop: ", "Arrhenius / Eyring links the literature activation energies to turnover, giving the model a physically meaningful target space instead of raw correlations."),
], size=13, gap=9)
footer(s, 5)

# ================= SLIDE 6 - BOLTZMANN FIGURE =================
s = add_slide()
header(s, "Theory used in the project", "Boltzmann Weighting Turns Structures into Descriptors")
pic(s, "assets2/boltzmann_states.png", Inches(0.8), Inches(1.7), Inches(8.3))
rect(s, Inches(9.4), Inches(1.8), Inches(3.3), Inches(4.6), LIGHT)
txt(s, Inches(9.65), Inches(2.05), Inches(2.9), Inches(0.4),
    [[("HOW WE USE IT", 11, True, NAVY)]])
bullets(s, Inches(9.65), Inches(2.5), Inches(2.85), Inches(3.7), [
    "Weight each reported active-state geometry by its Boltzmann population",
    "Bond angles / oxidation states enter as ensemble-averaged descriptors",
    "Temperature & pH shift populations \u2014 captured as scenario features",
], size=11.5, gap=10, color=INK)
txt(s, Inches(0.8), Inches(5.65), Inches(8.3), Inches(0.9),
    [[("Fig. 2  Left: population of catalytic microstates at two temperatures. Right: the low-E\u2090 state dominates at operating conditions \u2014 its weighted geometry is what the ML model actually learns from.", 10.5, False, GREY)]])
footer(s, 6)

# ================= SLIDE 7 - EQUATIONS & PARAMETERS =================
s = add_slide()
header(s, "Governing equations", "Equations and Parameters Used in the Model")
rows = [
    ("Boltzmann population", "P\u1d62 = exp(\u2212E\u1d62 / k_B T) / Z", "E\u1d62 state energies, T temperature"),
    ("Partition function", "Z = \u03a3\u1d62 exp(\u2212E\u1d62 / k_B T)", "all accessible microstates of the active site"),
    ("Free energy of activation", "\u0394G\u207d = \u2212R T ln(k h / \u03ba k_B T)", "from literature E\u2090 via Eyring / Arrhenius fits"),
    ("Arrhenius rate", "k = A exp(\u2212E\u2090 / R T)", "E\u2090 collected per metal / oxidation state"),
    ("Adsorption equilibrium", "\u03b8 = K P_CO\u2082 / (1 + K P_CO\u2082)", "K linked to pH, surface chemistry"),
    ("Model target", "yield % = f(descriptors)  [XGBoost / RF]", "trained on literature yield values"),
]
y = 1.62
txt(s, Inches(0.7), Inches(y), Inches(3.1), Inches(0.3), [[("QUANTITY", 10.5, True, GREY)]])
txt(s, Inches(3.9), Inches(y), Inches(4.6), Inches(0.3), [[("EQUATION", 10.5, True, GREY)]])
txt(s, Inches(8.7), Inches(y), Inches(4.0), Inches(0.3), [[("PARAMETERS IN THIS PROJECT", 10.5, True, GREY)]])
y += 0.38
for i, (q, eq, par) in enumerate(rows):
    if i % 2 == 0:
        rect(s, Inches(0.62), Inches(y - 0.05), Inches(12.1), Inches(0.72), LIGHT)
    txt(s, Inches(0.7), Inches(y), Inches(3.1), Inches(0.6), [[(q, 12.5, True, NAVY)]])
    txt(s, Inches(3.9), Inches(y), Inches(4.6), Inches(0.6), [[(eq, 12.5, False, INK)]])
    txt(s, Inches(8.7), Inches(y), Inches(4.0), Inches(0.6), [[(par, 11, False, GREY)]])
    y += 0.76
footer(s, 7)

# ================= SLIDE 8 - SCENARIOS =================
s = add_slide()
header(s, "Different scenarios", "Scenarios Handled by the Same Statistical Framework")
cards = [
    ("Electrochemical reduction", "aqueous, ambient T", "pH sets proton chemical potential \u03bc_H+ = \u03bc\u00b0 \u2212 k_BT ln a_H+; overpotential shifts barrier distributions"),
    ("Photocatalytic / enzymatic mimic", "mild T, neutral pH", "low-E\u2090 conformational states dominate; Boltzmann-weighted bond angles matter most"),
    ("High-T thermochemical cycle", "metal oxides", "population of higher-energy sites grows (see Fig. 2); Ea ranking can invert with T"),
    ("Solid sorbent capture", "temperature-swing", "Langmuir-type \u03b8 from adsorption partition functions; capture capacity vs regeneration cost"),
]
x = 0.65
for t, sub, body in cards:
    rect(s, Inches(x), Inches(1.7), Inches(2.95), Inches(4.5), LIGHT)
    rect(s, Inches(x), Inches(1.7), Inches(2.95), Inches(0.06), NAVY)
    txt(s, Inches(x + 0.2), Inches(1.95), Inches(2.6), Inches(0.7), [[(t, 13.5, True, NAVY)]])
    txt(s, Inches(x + 0.2), Inches(2.6), Inches(2.6), Inches(0.4), [[(sub, 10.5, False, AMBER)]])
    txt(s, Inches(x + 0.2), Inches(3.05), Inches(2.6), Inches(3.0), [[(body, 11.5, False, INK)]])
    x += 3.12
footer(s, 8)

# ================= SLIDE 9 - DATA COLLECTION =================
s = add_slide()
header(s, "Applications \u2014 project data", "Dataset Built from Literature Mining")
bullets(s, Inches(0.7), Inches(1.65), Inches(6.4), Inches(4.9), [
    ("Sources: ", "peer-reviewed papers on M\u2013N\u2013C sites, metalloporphyrins, enzymes and MOF sorbents for CO\u2082 capture/conversion."),
    ("Collected fields: ", "metal identity and oxidation state, bond angles (M\u2013N\u2013C, O\u2013M\u2013O), activation energies E\u2090, operating pH, and reported yield %."),
    ("Cleaning: ", "unit harmonisation, outlier flags, duplicate entries merged; missing values imputed with ensemble-mean per material class."),
    ("Splitting: ", "train/validation split with grouped cross-validation so all entries from one paper stay together (prevents leakage)."),
], size=13.5, gap=11)
rect(s, Inches(7.35), Inches(1.7), Inches(5.3), Inches(4.75), LIGHT)
txt(s, Inches(7.6), Inches(1.92), Inches(4.8), Inches(0.35), [[("FEATURE TABLE", 11, True, NAVY)]])
feat_rows = [
    ("Feature", "Origin", "Stat-mech role"),
    ("Oxidation state", "literature", "sets d-electron energy levels"),
    ("Bond angles", "DFT / XRD reports", "microstate geometry E\u1d62"),
    ("Activation energy", "Arrhenius fits", "barrier \u2192 rate constant"),
    ("pH", "experimental", "proton chemical potential"),
    ("Yield %", "experimental", "model target variable"),
]
yy = 2.35
for j, (a, b, c) in enumerate(feat_rows):
    bold = (j == 0)
    col = NAVY if bold else INK
    sz = 11 if bold else 11.5
    txt(s, Inches(7.6), Inches(yy), Inches(1.85), Inches(0.35), [[(a, sz, bold, col)]])
    txt(s, Inches(9.5), Inches(yy), Inches(1.5), Inches(0.35), [[(b, sz, bold, GREY if bold else INK)]])
    txt(s, Inches(11.0), Inches(yy), Inches(1.5), Inches(0.35), [[(c, sz, bold, GREY if bold else INK)]])
    yy += 0.42 if not bold else 0.46
txt(s, Inches(7.6), Inches(yy + 0.1), Inches(4.8), Inches(1.2),
    [[("Every descriptor is chosen because statistical mechanics says it changes a population, a barrier, or a rate \u2014 not because it happens to be tabulated.", 10.5, False, GREY, True)]])
footer(s, 9)

# ================= SLIDE 10 - ML MODELS =================
s = add_slide()
header(s, "Applications \u2014 modelling", "ML Models: XGBoost and Random Forest")
bullets(s, Inches(0.7), Inches(1.65), Inches(6.5), Inches(5.0), [
    ("Random Forest: ", "bagged decision trees; robust on small, heterogeneous literature data and gives a first importance ranking."),
    ("XGBoost: ", "gradient-boosted trees with regularisation; handles correlated descriptors (E\u2090 vs pH) better and gave the lower prediction error."),
    ("Physics-informed features: ", "Boltzmann-weighted angle averages and k_BT-scaled energies included alongside raw values."),
    ("Evaluation: ", "grouped k-fold CV, MAE/R\u00b2 on held-out papers; SHAP analysis checks that top features match the known controlling variables."),
    ("Screening output: ", "models predict yield % for unseen combinations \u2192 ranked shortlist of candidate bio-mimetic catalysts."),
], size=13, gap=10)
pic(s, "assets2/shap.png", Inches(7.5), Inches(1.75), Inches(5.1))
txt(s, Inches(7.5), Inches(5.5), Inches(5.1), Inches(0.8),
    [[("Fig. 3  Feature importances follow the physical hierarchy: electronic state first, geometry second, barrier third.", 10.5, False, GREY)]])
footer(s, 10)

# ================= SLIDE 11 - RESULTS / COMPARISON =================
s = add_slide()
header(s, "Comparison", "Model Behaviour and Comparison with Other Approaches")
pic(s, "assets2/parity.png", Inches(0.75), Inches(1.75), Inches(4.9))
txt(s, Inches(0.75), Inches(5.35), Inches(4.9), Inches(0.7),
    [[("Fig. 4  Cross-validated parity for both learners (illustrative of the observed trend).", 10.5, False, GREY)]])
rows = [
    ("Approach", "What it uses", "Weakness vs this project"),
    ("DFT alone", "single 0 K structures", "misses ensemble sampling; too costly to screen widely"),
    ("MD / Monte-Carlo", "explicit trajectories", "accurate but microseconds-scale, few materials"),
    ("Descriptor scaling", "one or two linear descriptors", "cannot capture pH / oxidation-state interactions"),
    ("This work: stat-mech features + XGBoost/RF", "curated multi-source data", "bounded by literature quality; needs experimental validation"),
]
x, w1 = 6.0, 2.5
rect(s, Inches(5.95), Inches(1.7), Inches(6.75), Inches(4.6), LIGHT)
yy = 1.9
for j, (a, b, c) in enumerate(rows):
    bold = (j == 0) or (j == len(rows)-1)
    txt(s, Inches(6.2), Inches(yy), Inches(2.6), Inches(0.8), [[(a, 11.5, bold, NAVY if bold else INK)]])
    txt(s, Inches(8.9), Inches(yy), Inches(1.7), Inches(0.8), [[(b, 11, False, INK)]])
    txt(s, Inches(10.7), Inches(yy), Inches(1.9), Inches(0.8), [[(c, 11, False, INK)]])
    yy += 0.62 if j < 3 else 0.85
footer(s, 11)

# ================= SLIDE 12 - LIMITATIONS =================
s = add_slide()
header(s, "Limitations", "Limitations and Assumptions")
bullets(s, Inches(0.7), Inches(1.7), Inches(7.0), Inches(5.0), [
    ("Data heterogeneity: ", "papers report yields under different setups; normalisation cannot fully remove protocol bias."),
    ("Publication bias: ", "failed catalysts are rarely published \u2014 the negative class is under-represented."),
    ("Harmonic / idealised statistics: ", "Boltzmann weighting assumes equilibrated states; real catalysts age, sinter or poison."),
    ("Small feature space: ", "few hundred records limit model complexity; deep learning was tested but overfit."),
    ("Prediction \u2260 proof: ", "ranked candidates still require synthesis and CO\u2082 reduction testing before any claim of superiority."),
], size=13.5, gap=12)
rect(s, Inches(8.2), Inches(1.75), Inches(4.4), Inches(4.6), LIGHT)
txt(s, Inches(8.45), Inches(2.0), Inches(3.9), Inches(0.35), [[("KEY ASSUMPTIONS", 11, True, NAVY)]])
bullets(s, Inches(8.45), Inches(2.45), Inches(3.85), Inches(3.7), [
    "Reported E\u2090 values transferable across similar supports",
    "Active-site ensembles near thermal equilibrium",
    "Yield % is a fair proxy for catalytic merit",
    "Solution pH proxies local interfacial pH",
], size=12, gap=10, color=INK)
footer(s, 12)

# ================= SLIDE 13 - TAKEAWAYS =================
s = add_slide()
header(s, "Conclusion", "Key Takeaways")
items = [
    ("1", "A literature-curated dataset of oxidation states, bond angles, activation energies, pH and yield % is a usable foundation for catalyst ML."),
    ("2", "Statistical mechanics supplies the bridge: Boltzmann populations, partition functions and rate theories convert structural data into physically meaningful features."),
    ("3", "XGBoost outperformed Random Forest on grouped cross-validation, with importances mirroring the expected physics (electronic state > geometry > barrier)."),
    ("4", "The pipeline ranks candidate bio-mimetic catalysts for CO\u2082 capture and conversion at a fraction of experimental cost."),
    ("5", "Next steps: closed-loop active learning \u2014 synthesise top predictions, feed measured yields back into training."),
]
yy = 1.75
for n, t in items:
    rect(s, Inches(0.7), Inches(yy), Inches(0.42), Inches(0.42), NAVY)
    txt(s, Inches(0.7), Inches(yy + 0.05), Inches(0.42), Inches(0.35),
        [[(n, 14, True, WHITE)]], align=PP_ALIGN.CENTER)
    txt(s, Inches(1.35), Inches(yy - 0.02), Inches(11.2), Inches(0.85), [[(t, 13.5, False, INK)]])
    yy += 0.95
footer(s, 13)

# ================= SLIDE 14 - REFERENCES =================
s = add_slide()
header(s, "References", "Selected References")
refs = [
    "McQuarrie, D. A. \u2014 Elementary Statistical Mechanics (classic ensemble & partition-function formalism).",
    "Zwanzig, R. \u2014 Nonequilibrium Statistical Mechanics (rate theory background).",
    "Eyring, H. (1935) J. Chem. Phys. 3, 107 \u2014 transition-state theory (\u0394G\u207d \u2192 rate).",
    "Arrhenius relation and catalytic barrier analysis in: N\u00f8skov, J. K. et al., Density Functional Theory in Surface Chemistry and Catalysis (Adv. Catal., 2009).",
    "Peterson, A. A. et al. (2010) \u2014 computational hydrogen electrode for CO\u2082/electrocatalysis thermodynamics.",
    "Chen, T. & Guestrin, C. (2016) \u2014 XGBoost: A Scalable Tree Boosting System, KDD.",
    "Breiman, L. (2001) \u2014 Random Forests, Machine Learning 45.",
    "Lundberg, S. & Lee, S.-I. (2017) \u2014 SHAP: Unified Approach to Interpreting Model Predictions, NeurIPS.",
    "Research articles on M\u2013N\u2013C single-atom and metalloporphyrin catalysts for CO\u2082 reduction, and carbonic-anhydrase-inspired sorbents (as compiled in the project dataset).",
]
bullets(s, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.0), refs, size=12.5, gap=10)
footer(s, 14)

prs.save("/workspace/ML_StatMech_CO2_Catalyst_Slides.pptx")
print("saved", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
