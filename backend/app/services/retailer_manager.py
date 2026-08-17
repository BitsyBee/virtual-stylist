from app.services.retailers.gflock import search_gflock


def search_retailers(
    category,
    limit_per_retailer=10
):

    products = []

    # ==========================================
    # GFLOCK
    # ==========================================

    try:

        products.extend(
            search_gflock(
                category,
                limit_per_retailer
            )
        )

    except Exception as e:

        print(
            f"GFLOCK retrieval failed: {e}"
        )

    # ==========================================
    # OTHER RETAILERS WILL BE ADDED HERE
    # ==========================================

    return products