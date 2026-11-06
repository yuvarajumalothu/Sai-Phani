import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#5A6B7B",
    "text.color": "#22303C",
    "axes.labelcolor": "#22303C",
    "xtick.color": "#5A6B7B",
    "ytick.color": "#5A6B7B",
})

NAVY   = "#1F3A5F"
STEEL  = "#4E7CA6"
AMBER  = "#C8963E"
GREY   = "#8A99A8"

# ---------- Fig 1: Boltzmann distribution + energy ladder ----------
fig, ax = plt.subplots(figsize=(5.6, 3.6), dpi=200)
beta_vals = [0.5, 1.0, 2.0]
E = np.linspace(0, 10, 300)
for b, c, ls in zip(beta_vals, [NAVY, STEEL, AMBER], ["-", "--", ":"]):
    p = b * np.exp(-b * E)
    ax.plot(E, p, ls, color=c, lw=2, label=r"$\beta = %.1f$" % b)
ax.set_xlabel(r"Energy  $E$")
ax.set_ylabel(r"$P(E)\ \propto e^{-\beta E}$")
ax.set_title("Boltzmann factor at different temperatures", fontsize=11)
ax.legend(frameon=False, fontsize=9)
ax.set_yticks([])
fig.tight_layout()
fig.savefig("/workspace/assets/boltzmann.png", transparent=True)
plt.close(fig)

# ---------- Fig 2: Eyring / Arrhenius-type free energy profile ----------
fig, ax = plt.subplots(figsize=(5.8, 3.6), dpi=200)
x = np.linspace(0, 10, 500)
G = 1.2*np.exp(-((x-1.5)/1.0)**2)*-1 - 0.0
y = (-1.6*np.exp(-((x-1.6)/1.1)**2)            # substrate well
     + 3.4*np.exp(-((x-4.6)/0.75)**2)          # barrier (TS)
     - 1.1*np.exp(-((x-8.0)/1.2)**2))          # product well
ax.plot(x, y, color=NAVY, lw=2.2)
ax.fill_between(x, y, y.min()-0.6, color=STEEL, alpha=0.08)
ax.annotate("ES", (1.6, -1.55), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=10, color=NAVY)
ax.annotate("Transition state", (4.6, 3.35), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10, color=AMBER)
ax.annotate("EP", (8.0, -1.05), textcoords="offset points", xytext=(0, -16), ha="center", fontsize=10, color=NAVY)
ax.annotate("", xy=(4.6, 3.3), xytext=(4.6, -1.55), arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.4))
ax.text(4.85, 0.9, r"$\Delta G^{\ddagger}$", color=AMBER, fontsize=11)
ax.text(4.85, 0.25, r"$k=\frac{k_BT}{h}e^{-\Delta G^{\ddagger}/RT}$", color="#22303C", fontsize=9.5)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylabel("Free energy  G")
ax.set_title("Activation free energy in the catalytic step", fontsize=11)
fig.tight_layout()
fig.savefig("/workspace/assets/eyring.png", transparent=True)
plt.close(fig)

# ---------- Fig 3: MLE vs MM kinetics (Michaelis-Menten curve) ----------
fig, ax = plt.subplots(figsize=(5.6, 3.6), dpi=200)
S = np.linspace(0, 12, 300)
Km, Vmax = 2.2, 1.0
v = Vmax*S/(Km+S)
ax.plot(S, v, color=NAVY, lw=2.2, label="MM hyperbola")
rng = np.random.default_rng(3)
sc = S[::12][:-1] + rng.normal(0, 0.15, len(S[::12])-1)
sv = Vmax*sc/(Km+sc) + rng.normal(0, 0.045, len(sc))
ax.scatter(sc, sv, s=22, facecolor="white", edgecolor=AMBER, zorder=3, label="single-molecule events")
ax.axhline(Vmax, ls=":", color=GREY, lw=1.2)
ax.text(11.6, Vmax+0.03, r"$V_{max}$", ha="right", fontsize=10, color=GREY)
ax.plot([Km, Km], [0, Vmax/2], ls=":", color=GREY, lw=1.2)
ax.text(Km+0.15, Vmax/2-0.02, r"$K_m$", fontsize=10, color=GREY)
ax.set_xlabel("Substrate concentration  [S]")
ax.set_ylabel("Rate  v")
ax.set_title("Ensemble average vs. fluctuating single enzyme", fontsize=11)
ax.legend(frameon=False, fontsize=9, loc="lower right")
fig.tight_layout()
fig.savefig("/workspace/assets/mm.png", transparent=True)
plt.close(fig)

# ---------- Fig 4: Conformational ensemble / energy landscape minima ----------
fig, ax = plt.subplots(figsize=(5.8, 3.4), dpi=200)
x = np.linspace(0, 12, 600)
y = (1.8*np.exp(-((x-1.5)/0.9)**2) + 2.6*np.exp(-((x-4.0)/0.9)**2)
     + 1.4*np.exp(-((x-6.5)/0.9)**2) + 2.2*np.exp(-((x-9.0)/0.9)**2)
     - 1.7*np.exp(-((x-2.6)/0.8)**2) - 2.9*np.exp(-((x-5.2)/0.8)**2)
     - 1.2*np.exp(-((x-7.8)/0.8)**2) - 2.4*np.exp(-((x-10.4)/0.8)**2))
ax.plot(x, y, color=NAVY, lw=2.2)
ax.fill_between(x, y, y.min()-0.4, color=STEEL, alpha=0.08)
for xm, lab in [(2.6, r"$E_1$"), (5.2, r"$E_2$"), (7.8, r"$E_3$"), (10.4, r"$E_4$")]:
    yv = float(np.interp(xm, x, y))
    ax.scatter([xm], [yv], s=30, color=AMBER, zorder=4)
    ax.text(xm, yv-0.55, lab, ha="center", fontsize=10, color="#22303C")
ax.text(5.9, 2.9, r"substates sampled with weights $\propto e^{-\beta E_i}$", fontsize=9.5, color=GREY, style="italic")
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylabel("Free energy")
ax.set_title("Rough conformational landscape of a biocatalyst", fontsize=11)
fig.tight_layout()
fig.savefig("/workspace/assets/landscape.png", transparent=True)
plt.close(fig)

print("figures done")
