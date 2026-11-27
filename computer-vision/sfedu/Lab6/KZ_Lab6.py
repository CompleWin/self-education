import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    1–2. Загрузить кадры и расположить их по порядку съёмки
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import cv2
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Rectangle

    return Rectangle, cv2, mo, np, plt


@app.cell
def _(cv2, plt):
    def show_row(images, titles, width=4):
        fig, axes = plt.subplots(
            1, len(images), figsize=(width * len(images), 3.5),
            squeeze=False, layout="constrained",
        )
        for ax, image, title in zip(axes[0], images, titles):
            ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            ax.set_title(title)
            ax.axis("off")
        plt.close(fig)
        return fig

    return (show_row,)


@app.cell
def _(cv2, np, show_row):
    names = sorted(["photo_1.jpg", "photo_2.jpg", "photo_3.jpg"])

    frames = []
    for _name in names:
        _data = np.fromfile(_name, dtype=np.uint8)
        _frame = cv2.imdecode(_data, cv2.IMREAD_COLOR)
        _h, _w = _frame.shape[:2]
        _scale = 1200 / max(_h, _w)
        if _scale < 1:
            _size = (max(1, round(_w * _scale)), max(1, round(_h * _scale)))
            _frame = cv2.resize(_frame, _size, interpolation=cv2.INTER_AREA)
        frames.append(_frame)

    show_row(frames, names)
    return frames, names


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    3. Найти ключевые точки и дескрипторы SIFT
    """)
    return


@app.cell
def _(cv2, frames, names, show_row):
    sift = cv2.SIFT_create(nfeatures=3000)
    features = [
        sift.detectAndCompute(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), None)
        for frame in frames
    ]

    keypoint_views = [
        cv2.drawKeypoints(
            frame, sorted(points, key=lambda point: point.response, reverse=True)[:200],
            None, color=(0, 210, 255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
        )
        for frame, (points, _) in zip(frames, features)
    ]
    show_row(
        keypoint_views,
        [f"{name}\nТочек: {len(points)}" for name, (points, _) in zip(names, features)],
    )
    return (features,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4. Сопоставить точки соседних кадров по критерию Лоу и найти гомографии через RANSAC
    """)
    return


@app.cell
def _(cv2, features, frames, mo, names, np, show_row):
    cv2.setRNGSeed(0)
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    pair_homographies = []
    _views = []
    for _i in range(1, len(frames)):
        _title = f"{names[_i]} → {names[_i - 1]}"
        _prev_points, _prev_desc = features[_i - 1]
        _curr_points, _curr_desc = features[_i]
        _neighbors = matcher.knnMatch(_curr_desc, _prev_desc, k=2)
        _good = [
            pair[0] for pair in _neighbors
            if len(pair) == 2 and pair[0].distance < 0.75 * pair[1].distance
        ]
        if len(_good) < 4:
            raise ValueError(f"{_title}: для гомографии нужно хотя бы четыре совпадения")

        _src = np.float32([_curr_points[m.queryIdx].pt for m in _good])
        _dst = np.float32([_prev_points[m.trainIdx].pt for m in _good])
        _H, _mask = cv2.findHomography(_src, _dst, cv2.RANSAC, 3.0)
        if _H is None or not np.isfinite(_H).all() or _mask.sum() < 4:
            raise ValueError(f"{_title}: RANSAC не нашёл гомографию")
        pair_homographies.append(_H)

        _inliers = _mask.ravel().astype(bool)
        _projected = cv2.perspectiveTransform(_src[_inliers, None, :], _H)[:, 0, :]
        _error = np.median(np.linalg.norm(_projected - _dst[_inliers], axis=1))
        _matches = [m for m, keep in zip(_good, _inliers) if keep]
        print(
            f"{_title} | Лоу: {len(_good)} | RANSAC: {len(_matches)}"
            f" | медианная ошибка: {_error:.2f} px"
        )
        print(_H)
        _sample = _matches[::max(1, len(_matches) // 35)][:35]
        _view = cv2.drawMatches(
            frames[_i], _curr_points, frames[_i - 1], _prev_points, _sample,
            None, matchColor=(0, 210, 255), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        )
        _views.append(show_row([_view], [_title], width=9))
    mo.vstack(_views)
    return (pair_homographies,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    5. Перенести углы кадров в координаты первого кадра и рассчитать размер холста
    """)
    return


@app.cell
def _(cv2, frames, np, pair_homographies):
    transforms = [np.eye(3)]
    for _H in pair_homographies:
        transforms.append(transforms[-1] @ _H)

    _outlines = []
    for _frame, _H in zip(frames, transforms):
        _h, _w = _frame.shape[:2]
        _corners = np.float64([[0, 0], [_w - 1, 0], [_w - 1, _h - 1], [0, _h - 1]])
        _denominator = _corners @ _H[2, :2] + _H[2, 2]
        if (
            _denominator.min() <= 0 <= _denominator.max()
            or np.any(np.abs(_denominator) < 1e-8)
        ):
            raise ValueError("Один из кадров выходит за горизонт проекции первого кадра")
        _outlines.append(cv2.perspectiveTransform(_corners[None], _H)[0])

    _corners = np.concatenate(_outlines)
    _lo = np.floor(_corners.min(axis=0))
    _hi = np.ceil(_corners.max(axis=0))
    _size = _hi - _lo + 1
    if not np.isfinite(_size).all() or _size.prod() > 16_000_000:
        raise ValueError("Холст слишком велик. Проверь порядок и перекрытие кадров")

    shift = np.array([[1, 0, -_lo[0]], [0, 1, -_lo[1]], [0, 0, 1]])
    canvas_size = tuple(map(int, _size))
    canvas_transforms = [shift @ H for H in transforms]
    outlines = [outline - _lo for outline in _outlines]
    print(f"Размер холста: {canvas_size[0]} × {canvas_size[1]} пикселей")
    return canvas_size, canvas_transforms, outlines


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    6. Перенести кадры на холст и смешать перекрытия
    """)
    return


@app.cell
def _(canvas_size, canvas_transforms, cv2, frames, np):
    _width, _height = canvas_size
    _color_sum = np.zeros((_height, _width, 3), dtype=np.float32)
    _weight_sum = np.zeros((_height, _width), dtype=np.float32)
    for _frame, _H in zip(frames, canvas_transforms):
        _warped = cv2.warpPerspective(_frame, _H, canvas_size, borderMode=cv2.BORDER_REPLICATE)
        _mask = np.ones(_frame.shape[:2], dtype=np.uint8)
        _mask = cv2.warpPerspective(_mask, _H, canvas_size, flags=cv2.INTER_NEAREST)
        _weights = cv2.distanceTransform(np.pad(_mask, 1), cv2.DIST_L2, 3)[1:-1, 1:-1]
        _color_sum += _warped * _weights[:, :, None]
        _weight_sum += _weights

    covered = _weight_sum > 0
    np.divide(_color_sum, _weight_sum[:, :, None], out=_color_sum, where=covered[:, :, None])
    canvas = np.clip(np.rint(_color_sum), 0, 255).astype(np.uint8)
    return canvas, covered


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7. Обрезать панораму по маске покрытия
    """)
    return


@app.cell
def _(np):
    def largest_covered_rectangle(covered):
        heights = np.zeros(covered.shape[1], dtype=int)
        best_area = 0
        best = None
        for y, row in enumerate(covered):
            heights = np.where(row, heights + 1, 0)
            stack = []
            for x, height in enumerate(heights.tolist() + [0]):
                left = x
                while stack and stack[-1][1] > height:
                    left, previous_height = stack.pop()
                    area = (x - left) * previous_height
                    if area > best_area:
                        best_area = area
                        best = (left, y + 1 - previous_height, x, y + 1)
                if height and (not stack or stack[-1][1] < height):
                    stack.append((left, height))
        if best is None:
            raise ValueError("После преобразования холст пуст")
        return best

    return (largest_covered_rectangle,)


@app.cell
def _(
    Rectangle,
    canvas,
    covered,
    largest_covered_rectangle,
    mo,
    outlines,
    show_row,
):
    crop = largest_covered_rectangle(covered)
    x0, y0, x1, y1 = crop
    panorama = canvas[y0:y1, x0:x1].copy()

    canvas_fig = show_row([canvas], ["Холст и окно обрезки"], width=10)
    _ax = canvas_fig.axes[0]
    for _i, _outline in enumerate(outlines):
        _loop = _outline[[0, 1, 2, 3, 0]]
        _ax.plot(_loop[:, 0], _loop[:, 1], color=f"C{_i}", linewidth=1.5)
    _ax.add_patch(Rectangle(
        (x0 - 0.5, y0 - 0.5), x1 - x0, y1 - y0,
        edgecolor="white", facecolor="none", linewidth=1.5, linestyle="--",
    ))
    print(f"Размер панорамы: {x1 - x0} × {y1 - y0} пикселей")
    print(f"Доля покрытых пикселей: {covered[y0:y1, x0:x1].mean():.1%}")
    mo.vstack([canvas_fig, show_row([panorama], ["Панорама"], width=10)])
    return (panorama,)


@app.cell(hide_code=True)
def _(cv2, mo, panorama):
    mo.download(
        data=lambda: cv2.imencode(".png", panorama)[1].tobytes(),
        filename="panorama.png",
        label="Скачать панораму",
    )
    return


if __name__ == "__main__":
    app.run()
