import csv
import random
from pathlib import Path

from fashion_knowledge import (
    COLORS,
    CLOTHING,
    BODY_TYPES,
    ITEM_OCCASIONS,
    BODY_TYPE_COMPATIBILITY,
)


# ============================================================
# SETTINGS
# ============================================================

NUMBER_OF_ITEMS = 400

OUTPUT_FILE = (
    Path(__file__).parent /
    "clothing_dataset_v2.csv"
)

random.seed(42)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def choose_style(item):
    return random.choice(
        CLOTHING[item]["styles"]
    )


def choose_color():
    return random.choice(
        list(COLORS.keys())
    )


def choose_fit(item):
    return random.choice(
        CLOTHING[item]["fits"]
    )


def choose_material(item):
    return random.choice(
        CLOTHING[item]["materials"]
    )


def choose_pattern(item):
    return random.choice(
        CLOTHING[item]["patterns"]
    )


def choose_season(item):
    return random.choice(
        CLOTHING[item]["seasons"]
    )


def choose_temperature(item):
    return random.choice(
        CLOTHING[item]["temperatures"]
    )


def get_skin_tones(color):
    return ", ".join(
        COLORS[color]["skin_tones"]
    )


def get_body_types(fit):
    """
    Determine body types for which this fit
    is generally appropriate.
    """

    compatible = []

    for body_type, fits in BODY_TYPE_COMPATIBILITY.items():

        if fit in fits:
            compatible.append(body_type)

    return ", ".join(compatible)

def get_compatible_occasions(item):
    """
    Return fashion-theory-based occasions
    for the specific clothing item.
    """

    return ITEM_OCCASIONS.get(
        item,
        ["Casual Outing"]
    )


def generate_tags(
    item,
    color,
    style,
    pattern,
):
    tags = [
        color,
        style.lower(),
        pattern.lower(),
    ]

    # Add useful semantic tags.
    if style in [
        "Formal",
        "Business Casual"
    ]:
        tags.append("professional")

    if style == "Smart Casual":
        tags.append("versatile")

    if style == "Streetwear":
        tags.append("urban")

    if pattern == "Solid":
        tags.append("minimal")

    return ", ".join(tags)


def generate_name(
    color,
    item,
    index,
):
    return (
        f"{color} {item} "
        f"{index}"
    )


# ============================================================
# GENERATE ONE ITEM
# ============================================================

def generate_item(
    item,
    index,
):

    data = CLOTHING[item]

    color = choose_color()

    style = choose_style(item)

    fit = choose_fit(item)

    material = choose_material(item)

    season = choose_season(item)

    temperature = choose_temperature(item)

    pattern = choose_pattern(item)

    occasions = get_compatible_occasions(item)

    # If no occasion matched, use a safe fallback.
    if not occasions:
        occasions = ["Casual Outing"]

    # Select a limited number of realistic occasions.
    occasions = random.sample(
        occasions,
        min(
            len(occasions),
            random.randint(1, 3)
        )
    )

    skin_tones = get_skin_tones(color)

    body_types = get_body_types(fit)

    tags = generate_tags(
        item,
        color,
        style,
        pattern,
    )

    return {
        "name": generate_name(
            color,
            item,
            index
        ),

        "category": data["category"],

        "gender": "Unisex",

        "color": color,

        "style": style,

        "occasion": ", ".join(
            occasions
        ),

        "fit": fit,

        "season": season,

        "recommended_skin_tones": skin_tones,

        "recommended_body_types": body_types,

        "temperature": temperature,

        "material": material,

        "tags": tags,

        # V2 uses placeholder image paths.
        # We can connect these to your existing
        # image folders later.
        "image_url": (
            f"images/"
            f"{data['category'].lower()}/"
            f"{color.lower().replace(' ', '_')}_"
            f"{item.lower().replace(' ', '_')}.jpg"
        ),
    }


# ============================================================
# DATASET GENERATION
# ============================================================

def generate_dataset():

    rows = []

    items = list(CLOTHING.keys())

    for index in range(
        1,
        NUMBER_OF_ITEMS + 1
    ):

        item = random.choice(items)

        row = generate_item(
            item,
            index
        )

        rows.append(row)

    fieldnames = [
        "name",
        "category",
        "gender",
        "color",
        "style",
        "occasion",
        "fit",
        "season",
        "recommended_skin_tones",
        "recommended_body_types",
        "temperature",
        "material",
        "tags",
        "image_url",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(rows)

    print()
    print("=" * 60)
    print("V2 FASHION DATASET GENERATED")
    print("=" * 60)
    print(f"Items : {len(rows)}")
    print(f"File  : {OUTPUT_FILE}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    generate_dataset()