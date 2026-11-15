"""Картинки к главе 4 «Думай как математик»: порции информации и иллюзия компетентности."""
# Рисунки media/book-bottom-up-top-down.png (раздел «Основные способы формирования порций информации»)
# и media/book-chunk-library.png (раздел «Иллюзия компетентности и важность вспоминания»)
# взяты из книги, этот файл их не рисует.

import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import C, new, save  # noqa: E402


def box(ax, x, y, text, color, w=2.6, h=0.9, fs=14, fill=0.15, ls="-", tc=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.05,rounding_size=0.15",
                                facecolor=to_rgba(color, fill), edgecolor=color, lw=2,
                                linestyle=ls))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc or C.ink)


def arrow(ax, p, q, color=C.gray, lw=2.2, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=20,
                                 color=color, lw=lw, connectionstyle=f"arc3,rad={rad}"))


def blank(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


# ---------- порция как архив: б, о, б -> «боб» ----------

fig, ax = new(size=(6.4, 2.8))
blank(ax, (-0.5, 10.5), (-0.4, 2.6))
for i, ch in enumerate("боб"):
    box(ax, 0.6 + i * 1.5, 1.1, ch, C.gray, w=1.1, h=1.1, fs=20)
ax.text(2.1, -0.15, "отдельные фрагменты", ha="center", fontsize=12, color=C.gray)
arrow(ax, (4.2, 1.1), (6.0, 1.1), color=C.blue, lw=2.8)
box(ax, 8.2, 1.1, "боб", C.blue, w=3.0, h=1.4, fs=24, fill=0.2)
ax.text(8.2, -0.15, "одна порция", ha="center", fontsize=12, color=C.blue)
save(fig, "chunk-zip")


# ---------- порция в рабочей памяти как гиперссылка ----------

fig, ax = new(size=(7.0, 3.6))
blank(ax, (-0.3, 11.2), (-1.2, 4.4))
ax.text(2.6, 4.0, "рабочая память", ha="center", fontsize=13, color=C.ink)
box(ax, 0.8, 2.9, "порция", C.blue, w=1.4, h=1.0, fs=12, fill=0.25)
for i in range(1, 4):
    box(ax, 0.8 + i * 1.6, 2.9, "свободно", C.gray, w=1.4, h=1.0, fs=10,
        fill=0.0, ls="--", tc=C.gray)
ax.add_patch(FancyBboxPatch((6.9, -0.3), 4.0, 2.4, boxstyle="round,pad=0.05,rounding_size=0.2",
                            facecolor=to_rgba(C.blue, 0.06), edgecolor=C.blue, lw=1.5))
rng = np.random.default_rng(3)
pts = np.c_[rng.uniform(7.3, 10.5, 14), rng.uniform(0.1, 1.7, 14)]
for a in range(len(pts)):
    for b in range(a + 1, len(pts)):
        if np.hypot(*(pts[a] - pts[b])) < 1.1:
            ax.plot(*zip(pts[a], pts[b]), color=C.blue, lw=1, alpha=0.5)
ax.scatter(pts[:, 0], pts[:, 1], s=40, color=C.blue, zorder=3)
ax.text(8.9, -0.8, "детали в долговременной памяти", ha="center", fontsize=11, color=C.blue)
arrow(ax, (1.2, 2.35), (6.85, 0.9), color=C.blue, rad=0.25)
save(fig, "chunk-hyperlink")


# ---------- понимание как клей: пазл ----------

def piece(ax, x, y, s, color, alpha=1.0):
    ax.add_patch(Rectangle((x, y), s, s, facecolor=to_rgba(color, 0.75 * alpha),
                           edgecolor="white", lw=2))


fig, ax = new(size=(7.6, 3.2))
blank(ax, (-0.3, 12.3), (-1.0, 3.6))
rng = np.random.default_rng(7)
for _ in range(12):
    x, y = rng.uniform(0, 2.8), rng.uniform(0, 2.8)
    piece(ax, x, y, 0.55, C.gray)
ax.text(1.6, -0.6, "сырая информация", ha="center", fontsize=12)
piece(ax, 5.6, 1.1, 0.8, C.orange)
ax.text(6.0, -0.6, "запомнил\nбез понимания", ha="center", fontsize=12, va="center")
for i in range(4):
    for j in range(4):
        piece(ax, 8.9 + i * 0.75, 0.1 + j * 0.75, 0.75, C.blue)
ax.text(10.4, -0.6, "порция: понято\nи связано", ha="center", fontsize=12, va="center",
        color=C.blue)
save(fig, "puzzle-understanding")


# ---------- порция крепнет с практикой ----------

fig, ax = new(size=(7.4, 3.0))
blank(ax, (-0.4, 12.4), (-1.3, 2.4))
t = np.linspace(0, 2 * np.pi, 200)
labels = ["понял,\nрешил раз-два", "практика в разных\nконтекстах", "укоренилась в\nдолговременной памяти"]
for k, (lw, al, lab) in enumerate(zip([1.5, 4, 8], [0.35, 0.65, 1.0], labels)):
    cx = 2 + k * 4
    for (dx, dy) in [(-0.8, 0.5), (0.0, 1.2), (0.8, 0.5), (0.3, -0.3), (-0.5, -0.3)]:
        ax.add_patch(Circle((cx + dx, 0.6 + dy * 0.8), 0.13, color=C.gray, zorder=3))
    xs = cx + 1.0 * np.cos(t) * (1 + 0.15 * np.sin(3 * t))
    ys = 0.85 + 0.85 * np.sin(t) * (1 + 0.1 * np.cos(2 * t))
    ax.plot(xs, ys, color=C.blue, lw=lw, alpha=al)
    ax.text(cx, -0.75, lab, ha="center", va="center", fontsize=11)
save(fig, "chunk-strength")


# ---------- три шага формирования порции ----------

fig, ax = new(size=(7.6, 2.4))
blank(ax, (-0.2, 12.2), (-0.2, 1.8))
steps = [("1. внимание", C.orange), ("2. понимание\nсути", C.blue), ("3. контекст:\nпрактика", C.green)]
for i, (s, c) in enumerate(steps):
    box(ax, 1.8 + i * 4.2, 0.8, s, c, w=3.2, h=1.3, fs=13)
    if i:
        arrow(ax, (3.5 + (i - 1) * 4.2, 0.8), (4.3 + (i - 1) * 4.2, 0.8))
save(fig, "chunk-steps")


# ---------- избыточное обучение: отдача каждой следующей задачи ----------

n = np.linspace(0, 10, 300)
gain = np.where(n < 3, 1.0 - 0.05 * n, 0.85 * np.exp(-(n - 3) / 1.3))
fig, ax = new(size=(6.6, 3.8))
ax.plot(n, gain, color=C.blue)
ax.fill_between(n, 0, gain, where=n >= 3, color=C.red, alpha=0.12)
ax.axvline(3, color=C.gray, ls="--", lw=1.5)
ax.text(3.15, 1.02, "понял приём", fontsize=12, color=C.gray, va="top")
ax.text(6.2, 0.45, "избыточное\nобучение", fontsize=13, color=C.red, ha="center")
ax.set_xlabel("задачи одного типа подряд, в одном занятии")
ax.set_ylabel("польза следующей задачи")
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0, 1.1)
save(fig, "overlearning")


# ---------- подряд или вперемешку ----------

fig, ax = new(size=(7.4, 2.8))
blank(ax, (-3.2, 12.3), (-0.3, 2.9))
col = {"A": C.blue, "B": C.orange, "C": C.green}
blocked = "AAAABBBBCCCC"
mixed = "ABCBACCABCBA"
for row, (name, seq) in enumerate([("подряд", blocked), ("вперемешку", mixed)]):
    y = 1.7 - row * 1.4
    ax.text(-0.3, y + 0.4, name, ha="right", va="center", fontsize=13)
    for i, s in enumerate(seq):
        ax.add_patch(Rectangle((i * 1.0, y), 0.85, 0.8, facecolor=to_rgba(col[s], 0.8),
                               edgecolor="white"))
        ax.text(i * 1.0 + 0.425, y + 0.4, s, ha="center", va="center", color="white",
                fontsize=12, fontweight="bold")
save(fig, "blocked-vs-interleaved")
