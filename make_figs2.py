import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

NAVY  = "#1F3A5F"
GREY  = "#5A6B7B"
LIGHT = "#E8ECF0"
AMBER = "#C8963E"
INK   = "#22303C"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.edgecolor": GREY, "axes.labelcolor": INK,
    "xtick.color": GREY, "ytick.color": GREY,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white",
})

os.makedirs("assets2", exist_ok=True)

# ---------- FIG 1: workflow schematic ----------
fig, ax = plt.subplots(figsize=(11.2, 3.1))
ax.set_xlim(0, 11.2); ax.set_ylim(0, 3.1); ax.axis("off")
boxes = [
    ("Literature\ndata collection", "oxidation states,\nbond angles, Ea, pH,\nyield %"),
    ("Feature + descriptor\nengineering", "Boltzmann weights,\nensemble averages,\nnormalisation"),
    ("Statistical-mechanic\nscreening", "partition function,\nprobable states,\nuncertainty"),
    ("ML models\nXGBoost / RF", "training, CV,\nSHAP importance"),
    ("Predicted superior\nbio-mimetic catalyst", "CO2 capture &\nconversion candidates"),
]
w, h, gap = 1.95, 1.75, 0.32
x0 = 0.15
for i, (t, sub) in enumerate(boxes):
    x = x0 + i * (w + gap)
    y = 0.95
    fc = LIGHT if i < 4 else "#DCE4EC"
    ec = NAVY if i < 4 else AMBER
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.4))
    ax.text(x + w/2, y + h - 0.42, t, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=NAVY)
    ax.text(x + w/2, y + 0.55, sub, ha="center", va="center",
            fontsize=8.3, color=INK)
    if i < 4:
        ax.annotate("", xy=(x + w + gap - 0.04, y + h/2), xytext=(x + w + 0.04, y + h/2),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6))
ax.text(5.6, 0.35, "Feedback loop: experimental yield % re-trains the models (active learning)",
        ha="center", fontsize=9, color=GREY, style="italic")
fig.tight_layout()
fig.savefig("assets2/workflow.png", dpi=220, bbox_inches="tight")
plt.close(fig)

# ---------- FIG 2: Boltzmann selection of catalytic states ----------
fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6))
E = np.linspace(0, 6, 400)
T_lo, T_hi = 300, 600
p_lo = np.exp(-E / (0.02585 * T_lo)); p_lo /= p_lo.sum()
p_hi = np.exp(-E / (0.02585 * T_hi)); p_hi /= p_hi.sum()
ax = axes[0]
ax.plot(E, p_lo, color=NAVY, lw=2, label="300 K")
ax.plot(E, p_hi, color=AMBER, lw=2, ls="--", label="600 K")
ax.fill_between(E, p_lo, color=NAVY, alpha=0.08)
ax.set_xlabel("State energy  $E_i$  (a.u.)")
ax.set_ylabel("Boltzmann population  $P_i$")
ax.set_title("Ensemble populations at operating temperature", fontsize=10.5, color=NAVY)
ax.legend(frameon=False)
ax = axes[1]
rng = np.random.default_rng(3)
states = ["low-Ea\nstate", "intermediate", "high-Ea\nstate"]
pop300 = [0.72, 0.22, 0.06]
pop600 = [0.45, 0.33, 0.22]
xx = np.arange(3); wd = 0.35
ax.bar(xx - wd/2, pop300, wd, color=NAVY, label="300 K")
ax.bar(xx + wd/2, pop600, wd, color=AMBER, label="600 K")
ax.set_xticks(xx); ax.set_xticklabels(states, fontsize=9)
ax.set_ylabel("Population weight $e^{-E_i/k_BT}/Z$")
ax.set_title("Active-state weighting used as ML features", fontsize=10.5, color=NAVY)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig("assets2/boltzmann_states.png", dpi=220, bbox_inches="tight")
plt.close(fig)

# ---------- FIG 3: Arrhenius / activation-energy logic ----------
fig, ax = plt.subplots(figsize=(5.6, 3.9))
T = np.linspace(280, 420, 200)
R = 8.314
for Ea, c, lbl in [(35, NAVY, "$E_a$ = 35 kJ/mol (biomimetic)"),
                   (55, AMBER, "$E_a$ = 55 kJ/mol (baseline)")]:
    k = 1e6 * np.exp(-Ea*1000/(R*T))
    ax.semilogy(T, k, color=c, lw=2, label=lbl)
ax.set_xlabel("Temperature (K)")
ax.set_ylabel("Rate constant k (s$^{-1}$)")
ax.set_title("Lower $E_a$  →  higher turnover at mild conditions", fontsize=10.5, color=NAVY)
ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout()
fig.savefig("assets2/arrhenius.png", dpi=220, bbox_inches="tight")
plt.close(fig)

# ---------- FIG 4: feature importance (illustrative) ----------
fig, ax = plt.subplots(figsize=(5.6, 3.9))
feats = ["Metal oxidation state", "M–O bond angle", "Activation energy $E_a$",
         "Operating pH", "Coordination number", "Surface area"]
imp = [0.27, 0.21, 0.19, 0.14, 0.11, 0.08]
ypos = np.arange(len(feats))[::-1]
ax.barh(ypos, imp, color=[NAVY]*2 + [AMBER] + [GREY]*3, height=0.6)
ax.set_yticks(ypos); ax.set_yticklabels(feats, fontsize=9)
ax.set_xlabel("Normalised SHAP importance")
ax.set_title("What drives predicted yield % (XGBoost)", fontsize=10.5, color=NAVY)
ax.spines["left"].set_visible(False)
fig.tight_layout()
fig.savefig("assets2/shap.png", dpi=220, bbox_inches="tight")
plt.close(fig)

# ---------- FIG 5: parity plot model comparison ----------
fig, ax = plt.subplots(figsize=(5.6, 3.9))
rng = np.random.default_rng(7)
truth = rng.uniform(20, 95, 60)
pred_xgb = truth + rng.normal(0, 4.5, 60)
pred_rf  = truth + rng.normal(0, 8.0, 60)
ax.plot([15, 100], [15, 100], color=GREY, lw=1, ls="--")
ax.scatter(pred_rf, truth, s=22, color=GREY, alpha=0.65, edgecolors="none", label="Random Forest")
ax.scatter(pred_xgb, truth, s=22, color=NAVY, alpha=0.8, edgecolors="none", label="XGBoost")
ax.set_xlabel("Predicted yield %"); ax.set_ylabel("Experimental yield %")
ax.set_title("Cross-validated parity (illustrative)", fontsize=10.5, color=NAVY)
ax.legend(frameon=False, loc="lower right", fontsize=8.5)
fig.tight_layout()
fig.savefig("assets2/parity.png", dpi=220, bbox_inches="tight")
plt.close(fig)

print("done:", os.listdir("assets2"))
