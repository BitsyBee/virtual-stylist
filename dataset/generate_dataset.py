import csv
import random

OUTPUT_FILE = "clothing_dataset.csv"

# -----------------------------
# Clothing types
# -----------------------------

clothing_types = {
    "Top": [
        "Oxford Shirt",
        "Polo Shirt",
        "T-Shirt",
        "Linen Shirt",
        "Hoodie",
        "Sweater",
        "Casual Shirt",
        "Formal Shirt"
    ],

    "Bottom": [
        "Jeans",
        "Chinos",
        "Cargo Pants",
        "Formal Trousers",
        "Shorts",
        "Joggers"
    ],

    "Shoes": [
        "Sneakers",
        "Loafers",
        "Formal Shoes",
        "Running Shoes",
        "Boots",
        "Canvas Shoes"
    ]
}

colors = [
    "Black",
    "White",
    "Blue",
    "Navy",
    "Grey",
    "Brown",
    "Beige",
    "Olive",
    "Red",
    "Green"
]

styles = [
    "Casual",
    "Formal",
    "Smart Casual",
    "Sport"
]

occasions = [
    "University",
    "Interview",
    "Presentation",
    "Office",
    "Casual Outing",
    "Party",
    "Sports"
]

fits = [
    "Slim Fit",
    "Regular Fit",
    "Oversized"
]

materials = [
    "Cotton",
    "Linen",
    "Denim",
    "Leather",
    "Polyester",
    "Wool"
]

seasons = [
    "Summer",
    "Winter",
    "All Season"
]

skin_tones = [
    "Fair",
    "Medium",
    "Dark"
]

body_types = [
    "Slim",
    "Average",
    "Athletic"
]

temperatures = [
    "Hot",
    "Warm",
    "Cold",
    "Any"
]

genders = [
    "Male",
    "Female",
    "Unisex"
]


# -----------------------------
# Generate one clothing item
# -----------------------------

def generate_item(category, item_type, number):

    color = random.choice(colors)

    name = f"{color} {item_type}"

    selected_skin_tones = random.sample(
        skin_tones,
        random.randint(1, 3)
    )

    selected_body_types = random.sample(
        body_types,
        random.randint(1, 3)
    )

    style = random.choice(styles)
    occasion = random.choice(occasions)
    fit = random.choice(fits)
    season = random.choice(seasons)
    material = random.choice(materials)
    temperature = random.choice(temperatures)
    gender = random.choice(genders)

    tags = []

    if style == "Formal":
        tags.append("Professional")

    if style == "Casual":
        tags.append("Comfortable")

    if occasion == "University":
        tags.append("Daily Wear")

    if occasion == "Sports":
        tags.append("Active")

    if not tags:
        tags.append("Modern")

    image_name = name.lower().replace(" ", "_")

    if category == "Top":
        image_url = f"images/tops/{image_name}.jpg"

    elif category == "Bottom":
        image_url = f"images/bottoms/{image_name}.jpg"

    else:
        image_url = f"images/shoes/{image_name}.jpg"

    return {
        "name": name,
        "category": category,
        "gender": gender,
        "color": color,
        "style": style,
        "occasion": occasion,
        "fit": fit,
        "season": season,
        "recommended_skin_tones": ",".join(selected_skin_tones),
        "recommended_body_types": ",".join(selected_body_types),
        "temperature": temperature,
        "material": material,
        "tags": ",".join(tags),
        "image_url": image_url
    }


# -----------------------------
# Generate dataset
# -----------------------------

rows = []

items_per_category = {
    "Top": 120,
    "Bottom": 100,
    "Shoes": 80
}

counter = 1

for category, amount in items_per_category.items():

    for _ in range(amount):

        item_type = random.choice(
            clothing_types[category]
        )

        item = generate_item(
            category,
            item_type,
            counter
        )

        rows.append(item)

        counter += 1


# -----------------------------
# Save CSV
# -----------------------------

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
    "image_url"
]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(rows)


print(f"Generated {len(rows)} clothing items.")
print(f"Dataset saved to {OUTPUT_FILE}")