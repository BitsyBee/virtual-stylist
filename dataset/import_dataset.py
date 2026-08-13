import pandas as pd
from pathlib import Path
import sys

sys.path.append("../backend")

from app.database.database import SessionLocal
from app.models.clothing_item import ClothingItem

db = SessionLocal()

csv_file = Path("clothing_dataset.csv")

df = pd.read_csv(csv_file)

count = 0

for _, row in df.iterrows():

    existing = db.query(ClothingItem).filter(
        ClothingItem.name == row["name"]
    ).first()

    if existing:
        print(f"Skipping: {row['name']}")
        continue

    clothing = ClothingItem(
        name=row["name"],
        category=row["category"],
        gender=row["gender"],
        color=row["color"],
        style=row["style"],
        occasion=row["occasion"],
        fit=row["fit"],
        season=row["season"],
        recommended_skin_tones=row["recommended_skin_tones"],
        recommended_body_types=row["recommended_body_types"],
        temperature=row["temperature"],
        material=row["material"],
        tags=row["tags"],
        image_url=row["image_url"]
    )

    db.add(clothing)
    count += 1

db.commit()

print(f"\nImported {count} clothing items successfully.")

db.close()