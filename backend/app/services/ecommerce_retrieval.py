from app.services.ecommerce.gflock import (
    GflockProvider
)

from app.services.ecommerce.kapruka import (
    KaprukaProvider
)

from app.services.ecommerce.neverbe import (
    get_live_neverbe_products
)


# ============================================================
# PROVIDERS
# ============================================================
# Note: Neverbe is not included here because it uses a
# function-based interface (get_live_neverbe_products) rather
# than the class-based EcommerceProvider interface used by
# Gflock and Kapruka. It is called separately below, since it
# is currently the only provider that supplies shoe products.

PROVIDERS = [

    GflockProvider(),

    KaprukaProvider()

]


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_product(product):

    return {

        "name":
            product.get("name"),

        "brand":
            product.get("brand"),

        "source":
            product.get("source"),

        "category":
            product.get("category"),

        "gender": product.get(
            "gender",
            "Unisex"
        ),    

        "color":
            product.get("color"),

        "style":
            product.get("style"),

        "price":
            product.get("price"),

        "currency":
            product.get(
                "currency",
                "LKR"
            ),

        "image_url":
            product.get("image_url"),

        "product_url":
            product.get("product_url"),

        "description":
            product.get("description"),

        "sizes":
            product.get("sizes"),

        "availability":
            product.get(
                "availability",
                "Unknown"
            ),

        "inventory_quantity":
            product.get(
                "inventory_quantity"
            )
    }


# ============================================================
# LIVE MULTI-STORE RETRIEVAL
# ============================================================

def get_live_ecommerce_products(
    categories=None,
    per_provider=10
):

    if categories is None:

        categories = [
            "Top",
            "Bottom",
            "Shoes"
        ]

    all_products = []

    print(
        "\n===================================="
    )

    print(
        "LIVE MULTI-STORE RETRIEVAL"
    )

    print(
        "===================================="
    )

    for provider in PROVIDERS:

        print(
            f"\nProvider: {provider.name}"
        )

        try:

            products = provider.get_products(
                categories=categories,
                limit=per_provider
            )

            for product in products:

                normalized = (
                    normalize_product(
                        product
                    )
                )

                all_products.append(
                    normalized
                )

                print(
                    f"  ✓ "
                    f"{normalized['name']} "
                    f"[{normalized['category']}] "
                    f"({normalized['source']})"
                )

        except Exception as error:

            print(
                f"  ✗ "
                f"{provider.name} failed: "
                f"{error}"
            )

    # --------------------------------------------------------
    # Neverbe (shoe-specific, function-based provider)
    # --------------------------------------------------------

    if "Shoes" in categories:

        print(
            "\nProvider: Neverbe"
        )

        try:

            neverbe_results = get_live_neverbe_products(
                per_category=per_provider
            )

            for product in neverbe_results.get("Shoes", []):

                product.setdefault("source", "Neverbe")
                product.setdefault("brand", "Neverbe")
                product.setdefault("category", "Shoes")

                normalized = normalize_product(product)

                all_products.append(normalized)

                print(
                    f"  ✓ "
                    f"{normalized['name']} "
                    f"[Shoes] "
                    f"(Neverbe)"
                )

        except Exception as error:

            print(
                f"  ✗ Neverbe failed: {error}"
            )

    print(
        "\n===================================="
    )

    print(
        f"TOTAL PRODUCTS: "
        f"{len(all_products)}"
    )

    print(
        "===================================="
    )

    return all_products


# ============================================================
# GROUP BY CATEGORY
# ============================================================

def group_products_by_category(
    products
):

    grouped = {

        "Top": [],

        "Bottom": [],

        "Shoes": []
    }

    for product in products:

        category = product.get(
            "category"
        )

        if category in grouped:

            grouped[
                category
            ].append(
                product
            )

    return grouped