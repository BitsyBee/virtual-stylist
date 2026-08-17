from app.services.ecommerce_retrieval import (
    get_live_ecommerce_products
)


products = get_live_ecommerce_products(
    categories=[
        "Top",
        "Bottom",
        "Shoes"
    ],
    per_provider=5
)


print("\n")
print("=" * 60)
print("RESULT")
print("=" * 60)


for product in products:

    print(
        product.get("source"),
        "|",
        product.get("category"),
        "|",
        product.get("name"),
        "|",
        product.get("price"),
        "|",
        product.get("product_url")
    )


print("=" * 60)

print(
    "TOTAL:",
    len(products)
)