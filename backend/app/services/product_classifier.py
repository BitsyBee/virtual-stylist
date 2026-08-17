def classify_product(product):
    """
    Assign recommendation metadata to an e-commerce product.

    These classifications are part of the Virtual Stylist
    recommendation framework rather than retailer metadata.
    """

    name = (
        product.get("name") or ""
    ).lower()

    description = (
        product.get("description") or ""
    ).lower()

    text = f"{name} {description}"

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "shirt",
            "t-shirt",
            "tshirt",
            "polo",
            "top"
        ]
    ):
        category = "Top"

    elif any(
        word in text
        for word in [
            "trouser",
            "pants",
            "jeans",
            "shorts"
        ]
    ):
        category = "Bottom"

    elif any(
        word in text
        for word in [
            "shoe",
            "sneaker",
            "loafer",
            "sandal"
        ]
    ):
        category = "Shoes"

    elif any(
        word in text
        for word in [
            "blazer",
            "jacket",
            "coat"
        ]
    ):
        category = "Outerwear"

    else:
        category = "Top"

    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------
    # NOTE: This used to be hardcoded to "Male" for every
    # product, regardless of what the item actually was.
    # That caused menswear to be recommended to everyone,
    # including users with a Female profile. We now infer
    # gender from the product's own name/description text,
    # and fall back to "Unisex" (rather than "Male") when we
    # can't tell, so ambiguous items don't get excluded from
    # anyone's recommendations by mistake.

    female_keywords = [
        "women", "woman", "womens", "women's",
        "ladies", "lady", "female",
        "dress", "skirt", "blouse", "gown",
        "leggings", "heels", "maternity"
    ]

    male_keywords = [
        "men", "man", "mens", "men's",
        "gents", "gentleman", "male",
        "necktie", "boxer"
    ]

    is_female = any(word in text for word in female_keywords)
    is_male = any(word in text for word in male_keywords)

    if is_female and not is_male:
        gender = "Female"
    elif is_male and not is_female:
        gender = "Male"
    else:
        # Either no gender signal was found, or the text
        # mentions both (e.g. "unisex", "men's & women's") —
        # treat it as Unisex so it's shown to everyone instead
        # of being defaulted/skewed to one gender.
        gender = "Unisex"

    # -----------------------------------------------------
    # STYLE
    # -----------------------------------------------------

    if any(
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
    # OCCASION
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "formal",
            "blazer",
            "dress shirt"
        ]
    ):
        occasion = "Formal"

    elif any(
        word in text
        for word in [
            "office",
            "business"
        ]
    ):
        occasion = "Business Casual"

    else:
        occasion = "Casual"

    # -----------------------------------------------------
    # TEMPERATURE
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "linen",
            "short sleeve",
            "short-sleeve"
        ]
    ):
        temperature = "Hot"

    elif any(
        word in text
        for word in [
            "long sleeve",
            "jacket",
            "coat"
        ]
    ):
        temperature = "Cool"

    else:
        temperature = "Moderate"

    # -----------------------------------------------------
    # MATERIAL
    # -----------------------------------------------------

    material = None

    for possible_material in [
        "linen",
        "cotton",
        "viscose",
        "rayon",
        "polyester",
        "nylon"
    ]:

        if possible_material in text:

            material = possible_material.title()

            break

    return {
        "category": category,
        "gender": gender,
        "style": style,
        "occasion": occasion,
        "temperature": temperature,
        "material": material
    }

