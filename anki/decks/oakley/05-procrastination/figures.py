"""Картинки к главе 5 «Думай как математик»: как не поддаться прокрастинации."""
# Рисунок media/book-procrastination-cycle.png взят из книги (раздел «Как прокрастинирует мозг»),
# media/book-brick-wall.png тоже из книги (глава 3, скопирован из колоды 03-modes-memory-sleep).
# Этот файл их не рисует.

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from figstyle import C, new, save  # noqa: E402


# ---------- больно только до начала работы ----------

t = np.linspace(0, 10, 400)
start = 4.0
pain = np.where(t < start, 0.25 + 0.6 * (t / start) ** 2, 0.77 * np.exp(-(t - start) / 0.5) + 0.08)
fig, ax = new(size=(6.6, 3.8))
ax.plot(t, pain, color=C.red)
ax.fill_between(t, 0, pain, where=t <= start, color=C.red, alpha=0.12)
ax.axvline(start, color=C.gray, ls="--", lw=1.5)
ax.text(start + 0.15, 1.02, "сел за задачи", fontsize=12, color=C.gray, va="top")
ax.text(1.9, 0.2, "предчувствие", fontsize=13, color=C.red, ha="center")
ax.text(7.3, 0.28, "работа идёт", fontsize=13, color=C.green, ha="center")
ax.set_xlabel("время")
ax.set_ylabel("дискомфорт")
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0, 1.1)
save(fig, "anticipation-pain")


# ---------- чем дольше откладываешь, тем страшнее начать ----------

days = np.arange(1, 9)
fear = 0.18 * 1.33 ** days
fig, ax = new(size=(6.6, 3.8))
ax.bar(days, fear, color=[C.orange] * 6 + [C.red] * 2, width=0.65)
ax.text(8, fear[-1] + 0.12, "экзамен", ha="center", fontsize=12, color=C.red)
ax.set_xlabel("сколько раз занятие отложено")
ax.set_ylabel("страх приступить")
ax.set_xticks(days)
ax.set_yticks([])
ax.set_ylim(0, fear[-1] + 0.5)
ax.grid(False)
save(fig, "fear-grows")


# ---------- яд малыми дозами: каждый раз мелочь, в сумме вред ----------

days = np.arange(1, 21)
dose = np.full(days.shape, 0.2)
fig, ax = new(size=(6.8, 3.8))
ax.bar(days, dose, color=C.gray, width=0.6, label="каждый отдельный случай")
ax.plot(days, np.cumsum(dose), color=C.red, marker="o", ms=4, label="накопленный вред")
ax.text(20.3, np.cumsum(dose)[-1], "накопленный\nвред", color=C.red, fontsize=12, va="center")
ax.text(14, 0.45, "каждый раз «ничего страшного»", color=C.gray, fontsize=12, ha="center")
ax.set_xlabel("отложенные дела")
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(0, 24)
ax.grid(False)
save(fig, "poison-doses")
