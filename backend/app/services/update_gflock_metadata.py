from app.database.database import SessionLocal

from app.models.ecommerce_product import EcommerceProduct

from app.services.product_metadata import (
    infer_product_metadata
)


db = SessionLocal()

try:

    products = (
        db.query(EcommerceProduct)
        .filter(
            EcommerceProduct.source == "GFLOCK"
        )
        .all()
    )

    for product in products:

        metadata = infer_product_metadata(
            {
                "name": product.name,
                "description": product.description,
                "color": product.color
            }
        )

        product.category = (
            metadata["category"]
        )

        product.style = (
            metadata["style"]
        )

        product.occasion = (
            metadata["occasion"]
        )

        product.temperature = (
            metadata["temperature"]
        )

        product.season = (
            metadata["season"]
        )

        product.recommended_skin_tones = (
            metadata[
                "recommended_skin_tones"
            ]
        )

        product.recommended_body_types = (
            metadata[
                "recommended_body_types"
            ]
        )

    db.commit()

    print(
        f"Updated {len(products)} GFLOCK products."
    )

finally:

    db.close()