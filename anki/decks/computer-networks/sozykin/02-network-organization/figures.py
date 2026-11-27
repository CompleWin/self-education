"""Схемы для карточек. book-network-layers.png взят из конспекта."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, new, save


def link(ax, start, end):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops={"arrowstyle": "-|>", "color": C.blue, "linewidth": 2.2},
    )


def route_after_failure():
    fig, ax = new(size=(6.4, 2.8))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.set_axis_off()

    ax.text(0.11, 0.5, "Отправитель", ha="center", va="center")
    ax.text(0.89, 0.5, "Получатель", ha="center", va="center")
    ax.plot([0.24, 0.44], [0.55, 0.78], "--", color=C.gray)
    ax.plot([0.56, 0.76], [0.78, 0.55], "--", color=C.gray)
    ax.plot(0.5, 0.82, marker="x", color=C.red, markersize=11, markeredgewidth=2.5)
    ax.text(0.5, 0.92, "Сбой на пути", color=C.red, ha="center")

    ax.plot([0.24, 0.5], [0.45, 0.25], color=C.blue)
    link(ax, (0.5, 0.25), (0.76, 0.45))
    ax.text(0.5, 0.10, "Рабочий путь", color=C.blue, ha="center")
    save(fig, "route-after-failure")


def overload_points():
    fig, ax = new(size=(6.4, 3.0))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.set_axis_off()

    ax.text(0.5, 0.92, "Затопление", ha="center", weight="bold")
    ax.text(0.20, 0.73, "Быстрый\nотправитель", ha="center", va="center")
    ax.text(0.80, 0.73, "Медленный\nполучатель", ha="center", va="center", color=C.red)
    link(ax, (0.34, 0.73), (0.66, 0.73))

    ax.text(0.5, 0.43, "Скопление", ha="center", weight="bold")
    ax.text(0.20, 0.23, "Несколько\nотправителей", ha="center", va="center")
    ax.text(0.80, 0.23, "Перегруженный\nканал", ha="center", va="center", color=C.red)
    for start_y in (0.13, 0.23, 0.33):
        link(ax, (0.35, start_y), (0.65, 0.23))

    save(fig, "overload-points")


if __name__ == "__main__":
    route_after_failure()
    overload_points()
