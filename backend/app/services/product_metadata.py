def infer_product_metadata(product):

    name = (
        product.get("name") or ""
    ).lower()

    description = (
        product.get("description") or ""
    ).lower()

    color = (
        product.get("color") or ""
    ).lower()

    text = (
        name + " " +
        description + " " +
        color
    )

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "shirt",
            "t-shirt",
            "tee",
            "polo"
        ]
    ):

        category = "Top"

    elif any(
        word in text
        for word in [
            "pant",
            "trouser",
            "jean"
        ]
    ):

        category = "Bottom"

    else:

        category = "Other"

    # -----------------------------------------------------
    # STYLE
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "formal",
            "dress shirt",
            "blazer"
        ]
    ):

        style = "Formal"

    elif any(
        word in text
        for word in [
            "polo",
            "collar",
            "linen"
        ]
    ):

        style = "Smart Casual"

    elif any(
        word in text
        for word in [
            "oversize",
            "oversized"
        ]
    ):

        style = "Streetwear"

    else:

        style = "Casual"

    # -----------------------------------------------------
    # TEMPERATURE
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "linen",
            "viscose",
            "short sleeve",
            "short-sleeve"
        ]
    ):

        temperature = "Hot"

    elif any(
        word in text
        for word in [
            "long sleeve",
            "long-sleeve"
        ]
    ):

        temperature = "Warm"

    else:

        temperature = "Moderate"

    # -----------------------------------------------------
    # SEASON
    # -----------------------------------------------------

    if temperature == "Hot":

        season = "Summer"

    else:

        season = "All"

    # -----------------------------------------------------
    # OCCASION
    # -----------------------------------------------------

    if style == "Formal":

        occasion = "Interview, Formal, Business"

    elif style == "Smart Casual":

        occasion = "Casual, Smart Casual, Business Casual"

    else:

        occasion = "Casual"

    # -----------------------------------------------------
    # SKIN TONE
    # -----------------------------------------------------

    recommended_skin_tones = (
        "Fair, Medium, Deep"
    )

    # -----------------------------------------------------
    # BODY TYPE
    # -----------------------------------------------------

    recommended_body_types = (
        "Athletic, Rectangle, Oval, "
        "Triangle, Inverted Triangle"
    )

    return {

        "category":
            category,

        "style":
            style,

        "temperature":
            temperature,

        "season":
            season,

        "occasion":
            occasion,

        "recommended_skin_tones":
            recommended_skin_tones,

        "recommended_body_types":
            recommended_body_types
    }