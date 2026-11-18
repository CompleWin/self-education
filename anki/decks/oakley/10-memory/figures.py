"""Три рисунка с префиксом book- взяты из EPUB. Скрипт сохраняет их в PNG."""

import argparse
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path)
    args = parser.parse_args()
    media = Path(__file__).resolve().parent / "media"
    media.mkdir(exist_ok=True)
    figures = {
        "OPS/images/_38.jpg": "book-flying-mule.png",
        "OPS/images/_39.jpg": "book-knuckles.png",
        "OPS/images/_40.jpg": "book-palace-route.png",
    }
    with ZipFile(args.epub) as book:
        for source, filename in figures.items():
            with Image.open(BytesIO(book.read(source))) as image:
                image.save(media / filename)


if __name__ == "__main__":
    main()
