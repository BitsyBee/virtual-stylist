from app.models.ecommerce_product import EcommerceProduct


def normalize(value):
    if not value:
        return ""

    return str(value).strip().lower()


def product_matches_clothing(
    product,
    clothing_item
):
    """
    Determines how closely a real e-commerce
    product matches a clothing knowledge item.
    """

    score = 0
    reasons = []

    # ------------------------------------------------
    # CATEGORY
    # ------------------------------------------------

    if normalize(product.category) == normalize(
        clothing_item.category
    ):

        score += 20

        reasons.append(
            "Matches recommended clothing category"
        )


    # ------------------------------------------------
    # COLOR
    # ------------------------------------------------

    if (
        product.color
        and clothing_item.color
        and normalize(product.color)
        == normalize(clothing_item.color)
    ):

        score += 20

        reasons.append(
            "Matches recommended color"
        )


    # ------------------------------------------------
    # STYLE
    # ------------------------------------------------

    if (
        product.style
        and clothing_item.style
        and normalize(product.style)
        == normalize(clothing_item.style)
    ):

        score += 20

        reasons.append(
            "Matches recommended style"
        )


    # ------------------------------------------------
    # OCCASION
    # ------------------------------------------------

    if (
        product.occasion
        and clothing_item.occasion
    ):

        product_occasions = {
            normalize(x)
            for x in product.occasion.split(",")
        }

        clothing_occasions = {
            normalize(x)
            for x in clothing_item.occasion.split(",")
        }

        if product_occasions.intersection(
            clothing_occasions
        ):

            score += 15

            reasons.append(
                "Matches recommended occasion"
            )


    # ------------------------------------------------
    # TEMPERATURE
    # ------------------------------------------------

    if (
        product.temperature
        and clothing_item.temperature
    ):

        if (
            normalize(product.temperature)
            == normalize(clothing_item.temperature)
            or normalize(product.temperature) == "any"
        ):

            score += 10

            reasons.append(
                "Suitable for the recommended temperature"
            )


    # ------------------------------------------------
    # SEASON
    # ------------------------------------------------

    if (
        product.season
        and clothing_item.season
    ):

        if (
            normalize(product.season)
            == normalize(clothing_item.season)
            or normalize(product.season)
            == "all season"
        ):

            score += 10

            reasons.append(
                "Suitable for the recommended season"
            )


    return score, reasons


def find_ecommerce_matches(
    db,
    clothing_item,
    limit=5
):

    products = (
        db.query(EcommerceProduct)
        .filter(
            EcommerceProduct.source == "GFLOCK"
        )
        .all()
    )


    candidates = []


    for product in products:

        score, reasons = product_matches_clothing(
            product,
            clothing_item
        )

        candidates.append(
            {
                "product": product,
                "score": score,
                "reasons": reasons
            }
        )


    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    return candidates[:limit]