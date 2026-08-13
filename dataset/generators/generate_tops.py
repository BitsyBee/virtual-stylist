import csv
from pathlib import Path

# Output CSV
output_file = Path("../tops_batch.csv")

# Dataset fields
headers = [
    "name",
    "category",
    "gender",
    "color",
    "style",
    "occasion",
    "fit",
    "season",
    "material",
    "tags",
    "image_url"
]

colors = [
    "White",
    "Black",
    "Blue",
    "Light Blue",
    "Grey",
    "Navy",
    "Olive",
    "Beige"
]

shirts = [
    {
        "type": "Oxford Shirt",
        "style": "Smart Casual",
        "occasion": "Presentation",
        "fit": "Slim Fit",
        "season": "All Season",
        "material": "Cotton",
        "skin_tones": "Fair,Medium,Dark",
        "body_types": "Athletic,Average",
        "temperature": "Warm",
        "tags": "professional,classic,cotton"
    },
    {
        "type": "Dress Shirt",
        "style": "Formal",
        "occasion": "Interview",
        "fit": "Slim Fit",
        "season": "All Season",
        "material": "Cotton",
        "tags": "formal,professional,office"
    },
    {
        "type": "Polo Shirt",
        "style": "Casual",
        "occasion": "University",
        "fit": "Regular Fit",
        "season": "Summer",
        "material": "Cotton",
        "tags": "casual,comfortable,daily"
    },
    {
        "type": "Crew Neck T-Shirt",
        "style": "Casual",
        "occasion": "Casual Outing",
        "fit": "Regular Fit",
        "season": "Summer",
        "material": "Cotton",
        "tags": "minimal,casual,everyday"
    },
    {
        "type": "Henley",
        "style": "Smart Casual",
        "occasion": "Travel",
        "fit": "Regular Fit",
        "season": "All Season",
        "material": "Cotton",
        "tags": "comfortable,travel,modern"
    },
    {
        "type": "Crew Sweater",
        "style": "Smart Casual",
        "occasion": "Office",
        "fit": "Regular Fit",
        "season": "Winter",
        "material": "Wool",
        "tags": "warm,office,winter"
    }
]

rows = []

for shirt in shirts:
    for color in colors:

        filename = (
            color.lower()
            .replace(" ", "_")
            + "_"
            + shirt["type"].lower().replace(" ", "_")
            + ".jpg"
        )

        rows.append([
            f"{color} {shirt['type']}",
            "Top",
            "Male",
            color,
            shirt["style"],
            shirt["occasion"],
            shirt["fit"],
            shirt["season"],
            shirt["material"],
            shirt["skin_tones"],
            shirt["body_types"],
            shirt["temperature"],
            shirt["tags"],
            f"images/tops/{filename}"
        ])

with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Generated {len(rows)} clothing items.")
print(f"Saved to {output_file}")