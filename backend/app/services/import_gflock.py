from app.database.database import SessionLocal

from app.models.ecommerce_product import EcommerceProduct

from app.services.product_metadata import (
    infer_product_metadata
)
from app.services.ecommerce_retrieval import (
    get_gflock_products
)

from app.services.product_classifier import (
    classify_product
)


def import_products():

    db = SessionLocal()

    collections = [
        ("men_shirts", 20),
        ("men_pants", 20),
    ]

    imported = 0
    skipped = 0

    try:

        for collection, limit in collections:

            print(
                f"\nRetrieving {collection}..."
            )

            products = get_gflock_products(
                collection,
                limit
            )

            for product in products:

                existing = db.query(
                    EcommerceProduct
                ).filter(
                    EcommerceProduct.product_url
                    == product["product_url"]
                ).first()

                if existing:

                    print(
                        f"Skipping existing: "
                        f"{product['name']}"
                    )

                    skipped += 1

                    continue

                metadata = classify_product(
                    product
                )

                ecommerce_product = EcommerceProduct(

                    name=product["name"],

                    brand=product["brand"],

                    source=product["source"],

                    product_url=product["product_url"],

                    image_url=product["image_url"],

                    price=product["price"],

                    currency=product["currency"],

                    category=metadata["category"],

                    gender=metadata["gender"],

                    color=product["color"],

                    style=metadata["style"],

                    occasion=metadata["occasion"],

                    temperature=metadata["temperature"],

                    material=metadata["material"],

                    description=product["description"],

                    sizes=product["sizes"],

                    inventory_quantity=
                        product["inventory_quantity"],

                    availability=
                        product["availability"]
                )

                db.add(ecommerce_product)

                imported += 1

                print(
                    f"Importing: {product['name']}"
                )

        db.commit()

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()

    print("\n==============================")
    print("GFLOCK IMPORT COMPLETE")
    print("==============================")
    print(f"Imported: {imported}")
    print(f"Skipped:  {skipped}")
    print("==============================")


if __name__ == "__main__":
    import_products()