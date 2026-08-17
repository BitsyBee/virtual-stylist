from sqlalchemy.orm import Session

from app.models.ecommerce_product import EcommerceProduct


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize(value):

    if value is None:
        return ""

    return str(value).strip().lower()


# =========================================================
# PRODUCT SCORING
# =========================================================

def score_ecommerce_product(
    product,
    profile,
    occasion,
    style,
    temperature,
    season
):

    score = 0
    reasons = []

    requested_occasion = normalize(occasion)
    requested_style = normalize(style)
    requested_temperature = normalize(temperature)
    requested_season = normalize(season)

    product_style = normalize(product.style)
    product_occasion = normalize(product.occasion)
    product_temperature = normalize(product.temperature)
    product_season = normalize(product.season)

    # -----------------------------------------------------
    # STYLE MATCH
    # -----------------------------------------------------

    if requested_style and product_style:

        if requested_style == product_style:

            score += 25

            reasons.append(
                "Matches your preferred style."
            )

        elif requested_style in product_style:

            score += 15

            reasons.append(
                "Closely matches your preferred style."
            )

    # -----------------------------------------------------
    # OCCASION MATCH
    # -----------------------------------------------------

    if requested_occasion and product_occasion:

        if requested_occasion == product_occasion:

            score += 25

            reasons.append(
                "Suitable for the selected occasion."
            )

        elif requested_occasion in product_occasion:

            score += 15

            reasons.append(
                "Compatible with the selected occasion."
            )

    # -----------------------------------------------------
    # TEMPERATURE
    # -----------------------------------------------------

    if requested_temperature and product_temperature:

        if requested_temperature == product_temperature:

            score += 15

            reasons.append(
                "Suitable for the selected temperature."
            )

    # -----------------------------------------------------
    # SEASON
    # -----------------------------------------------------

    if requested_season and product_season:

        if requested_season == product_season:

            score += 10

            reasons.append(
                "Suitable for the selected season."
            )

    # -----------------------------------------------------
    # SKIN TONE
    # -----------------------------------------------------

    skin_tone = normalize(
        getattr(profile, "skin_tone", None)
    )

    recommended_skin_tones = normalize(
        product.recommended_skin_tones
    )

    if skin_tone and recommended_skin_tones:

        if skin_tone in recommended_skin_tones:

            score += 15

            reasons.append(
                "Colour is recommended for your skin tone."
            )

    # -----------------------------------------------------
    # BODY TYPE
    # -----------------------------------------------------

    body_type = normalize(
        getattr(profile, "body_type", None)
    )

    recommended_body_types = normalize(
        product.recommended_body_types
    )

    if body_type and recommended_body_types:

        if body_type in recommended_body_types:

            score += 10

            reasons.append(
                "Fit is suitable for your body type."
            )

    # -----------------------------------------------------
    # AVAILABLE PRODUCT
    # -----------------------------------------------------

    availability = normalize(
        product.availability
    )

    if availability in ["available", "in stock", "true"]:

        score += 5

        reasons.append(
            "Product is currently available."
        )

    return score, reasons


# =========================================================
# RECOMMEND E-COMMERCE PRODUCTS
# =========================================================

def recommend_ecommerce_products(
    db: Session,
    profile,
    occasion,
    style,
    temperature,
    season,
    limit=12
):

    products = (
        db.query(EcommerceProduct)
        .filter(
            EcommerceProduct.source == "GFLOCK"
        )
        .all()
    )

    scored_products = []

    for product in products:

        score, reasons = score_ecommerce_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        scored_products.append(
            {
                "product": product,
                "score": score,
                "reasons": reasons
            }
        )

    # Highest score first

    scored_products.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    recommendations = []

    for rank, item in enumerate(
        scored_products[:limit],
        start=1
    ):

        product = item["product"]

        recommendations.append(
            {
                "rank": rank,

                "score": item["score"],

                "reasons": item["reasons"],

                "id": product.id,

                "name": product.name,

                "brand": product.brand,

                "source": product.source,

                "category": product.category,

                "color": product.color,

                "style": product.style,

                "price": product.price,

                "currency": product.currency,

                "image_url": product.image_url,

                "product_url": product.product_url,

                "availability": product.availability,

                "sizes": product.sizes
            }
        )

    return recommendations