from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


SOURCE_DIR = Path("assets")
OUTPUT_DIR = SOURCE_DIR / "web"

OUTPUT_DIR.mkdir(exist_ok=True)

# Размеры в физических пикселях.
# В приложении мы покажем их примерно вдвое меньше.
TARGET_WIDTHS = {
    "anxiety_monster.png": 440,
    "procrastination_monster.png": 520,
    "fear_monster.png": 440,
    "negativity_monster.png": 440,
}


def prepare_image(filename: str, target_width: int) -> None:
    source_path = SOURCE_DIR / filename
    output_path = OUTPUT_DIR / filename

    image = Image.open(source_path).convert("RGBA")

    # Обрезаем прозрачный или почти однотонный воздух вокруг героя.
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()

    if bbox:
        image = image.crop(bbox)

    target_height = round(
        image.height * target_width / image.width
    )

    image = image.resize(
        (target_width, target_height),
        Image.Resampling.LANCZOS,
    )

    # Лёгкая резкость без жёстких ореолов.
    image = image.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=135,
            threshold=3,
        )
    )

    # Совсем немного усиливаем контраст.
    image = ImageEnhance.Contrast(image).enhance(1.04)

    image.save(
        output_path,
        format="PNG",
        optimize=True,
    )

    print(f"Saved: {output_path}")


for filename, width in TARGET_WIDTHS.items():
    prepare_image(filename, width)