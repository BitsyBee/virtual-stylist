from itertools import product


# ============================================================
# FASHION KNOWLEDGE
# ============================================================

OCCASION_STYLES = {

    "casual outing": [
        "casual",
        "smart casual",
        "streetwear"
    ],

    "dinner": [
        "smart casual",
        "formal",
        "business casual"
    ],

    "interview": [
        "formal",
        "business casual"
    ],

    "office": [
        "business casual",
        "formal",
        "smart casual"
    ],

    "party": [
        "casual",
        "smart casual",
        "streetwear"
    ],

    "date": [
        "smart casual",
        "casual"
    ],

    "formal event": [
        "formal",
        "business casual"
    ]
}


COLOR_COMPATIBILITY = {

    "black": [
        "white",
        "off white",
        "grey",
        "gray",
        "beige",
        "blue",
        "black"
    ],

    "white": [
        "black",
        "blue",
        "navy",
        "grey",
        "gray",
        "beige",
        "brown"
    ],

    "blue": [
        "white",
        "black",
        "beige",
        "grey",
        "gray",
        "navy"
    ],

    "navy": [
        "white",
        "beige",
        "grey",
        "gray",
        "brown"
    ],

    "beige": [
        "white",
        "black",
        "brown",
        "navy",
        "blue"
    ],

    "brown": [
        "white",
        "beige",
        "black",
        "blue"
    ]
}


SKIN_TONE_COLORS = {

    "fair": [
        "navy",
        "blue",
        "burgundy",
        "green",
        "black",
        "grey",
        "gray"
    ],

    "medium": [
        "blue",
        "green",
        "burgundy",
        "beige",
        "white",
        "black"
    ],

    "deep": [
        "white",
        "beige",
        "blue",
        "yellow",
        "green",
        "burgundy"
    ]
}


# ============================================================
# HELPERS
# ============================================================

def normalize(value):

    if value is None:
        return ""

    return str(value).strip().lower()


def product_text(item):

    values = [
        item.name,
        item.brand,
        item.category,
        item.color,
        item.style,
        item.description,
        item.tags,
        item.material
    ]

    return " ".join(
        normalize(v)
        for v in values
        if v
    )


def get_category(item):

    text = product_text(item)

    if any(word in text for word in [
        "shirt",
        "t-shirt",
        "tshirt",
        "top",
        "blouse",
        "polo"
    ]):
        return "top"

    if any(word in text for word in [
        "trouser",
        "pants",
        "jeans",
        "shorts",
        "skirt"
    ]):
        return "bottom"

    if any(word in text for word in [
        "shoe",
        "sneaker",
        "loafer",
        "sandal",
        "boot"
    ]):
        return "shoes"

    return "other"


def get_product_color(item):

    color = normalize(item.color)

    if color:
        return color

    text = product_text(item)

    known_colors = [
        "black",
        "white",
        "off white",
        "blue",
        "navy",
        "beige",
        "brown",
        "grey",
        "gray",
        "green",
        "burgundy",
        "red",
        "pink",
        "yellow"
    ]

    for c in known_colors:

        if c in text:
            return c

    return ""


# ============================================================
# PRODUCT SCORING
# ============================================================

def score_product(
    item,
    profile,
    occasion,
    requested_style,
    temperature,
    season,
    user_request
):

    score = 0

    reasons = []

    text = product_text(item)

    category = get_category(item)

    color = get_product_color(item)

    requested_style = normalize(requested_style)
    occasion = normalize(occasion)
    temperature = normalize(temperature)
    season = normalize(season)
    user_request = normalize(user_request)

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    if category == "other":
        return None

    # --------------------------------------------------------
    # USER REQUEST MATCH
    # --------------------------------------------------------

    request_words = user_request.split()

    request_matches = 0

    for word in request_words:

        if len(word) > 3 and word in text:
            request_matches += 1

    if request_matches:

        score += min(request_matches * 5, 20)

        reasons.append(
            "Matches keywords from your outfit request."
        )

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    item_style = normalize(item.style)

    if item_style:

        if item_style == requested_style:

            score += 25

            reasons.append(
                f"Matches your preferred {requested_style} style."
            )

        elif requested_style in item_style:

            score += 15

    # --------------------------------------------------------
    # OCCASION
    # --------------------------------------------------------

    preferred_styles = OCCASION_STYLES.get(
        occasion,
        []
    )

    for style in preferred_styles:

        if style in text:

            score += 15

            reasons.append(
                f"Suitable for a {occasion} occasion."
            )

            break

    # --------------------------------------------------------
    # PROFILE STYLE
    # --------------------------------------------------------

    profile_style = normalize(
        getattr(profile, "style_preference", "")
    )

    if profile_style and profile_style in text:

        score += 15

        reasons.append(
            "Matches your saved style preference."
        )

    # --------------------------------------------------------
    # SKIN TONE
    # --------------------------------------------------------

    skin_tone = normalize(
        getattr(profile, "skin_tone", "")
    )

    recommended_colors = SKIN_TONE_COLORS.get(
        skin_tone,
        []
    )

    if color:

        if any(
            c in color
            for c in recommended_colors
        ):

            score += 15

            reasons.append(
                "The colour is compatible with your selected skin tone."
            )

    # --------------------------------------------------------
    # FAVORITE COLORS
    # --------------------------------------------------------

    favorite_colors = normalize(
        getattr(profile, "favorite_colors", "")
    )

    if favorite_colors:

        favorites = [
            c.strip()
            for c in favorite_colors.split(",")
        ]

        if any(
            fav in color
            for fav in favorites
        ):

            score += 10

            reasons.append(
                "Matches one of your favourite colours."
            )

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    if temperature:

        if temperature in text:

            score += 10

            reasons.append(
                "Suitable for the requested temperature."
            )

        elif temperature == "warm":

            if any(
                x in text
                for x in [
                    "short sleeve",
                    "short-sleeve",
                    "linen",
                    "cotton"
                ]
            ):

                score += 8

                reasons.append(
                    "The material/style is suitable for warm weather."
                )

    # --------------------------------------------------------
    # SEASON
    # --------------------------------------------------------

    if season and season in text:

        score += 8

        reasons.append(
            "Matches the requested season."
        )

    return {
        "product": item,
        "score": score,
        "reasons": reasons
    }


# ============================================================
# OUTFIT COMPATIBILITY
# ============================================================

def calculate_compatibility(
    top,
    bottom,
    shoes
):

    score = 0
    reasons = []

    top_color = get_product_color(top)
    bottom_color = get_product_color(bottom)
    shoe_color = get_product_color(shoes)

    # --------------------------------------------------------
    # TOP + BOTTOM
    # --------------------------------------------------------

    if top_color and bottom_color:

        compatible = COLOR_COMPATIBILITY.get(
            top_color,
            []
        )

        if bottom_color in compatible:

            score += 20

            reasons.append(
                f"{top_color.title()} and "
                f"{bottom_color.title()} create a compatible colour combination."
            )

    # --------------------------------------------------------
    # SHOES
    # --------------------------------------------------------

    if shoe_color:

        if shoe_color in [
            "black",
            "white",
            "brown",
            "beige"
        ]:

            score += 10

            reasons.append(
                f"{shoe_color.title()} footwear provides a versatile neutral."
            )

    return score, reasons


# ============================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================

def recommend_ecommerce_outfits(
    products,
    profile,
    occasion,
    style,
    temperature,
    season,
    user_request
):

    scored = []

    # --------------------------------------------------------
    # SCORE PRODUCTS
    # --------------------------------------------------------

    for item in products:

        result = score_product(
            item,
            profile,
            occasion,
            style,
            temperature,
            season,
            user_request
        )

        if result:

            scored.append(result)

    # --------------------------------------------------------
    # GROUP BY CATEGORY
    # --------------------------------------------------------

    tops = [
        x for x in scored
        if get_category(x["product"]) == "top"
    ]

    bottoms = [
        x for x in scored
        if get_category(x["product"]) == "bottom"
    ]

    shoes = [
        x for x in scored
        if get_category(x["product"]) == "shoes"
    ]

    tops.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    bottoms.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    shoes.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # --------------------------------------------------------
    # CREATE OUTFITS
    # --------------------------------------------------------

    outfits = []

    for top, bottom, shoe in product(
        tops[:10],
        bottoms[:10],
        shoes[:10]
    ):

        compatibility_score, compatibility_reasons = \
            calculate_compatibility(
                top["product"],
                bottom["product"],
                shoe["product"]
            )

        total_score = (
            top["score"]
            + bottom["score"]
            + shoe["score"]
            + compatibility_score
        )

        outfits.append({

            "score": total_score,

            "top": format_product(top),

            "bottom": format_product(bottom),

            "shoes": format_product(shoe),

            "reasons": (
                top["reasons"]
                + bottom["reasons"]
                + shoe["reasons"]
                + compatibility_reasons
            )
        })

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    outfits.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATE OUTFITS
    # --------------------------------------------------------

    unique = []

    seen = set()

    for outfit in outfits:

        key = (
            outfit["top"]["id"],
            outfit["bottom"]["id"],
            outfit["shoes"]["id"]
        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(outfit)

        if len(unique) >= 5:
            break

    # --------------------------------------------------------
    # RANK
    # --------------------------------------------------------

    for index, outfit in enumerate(unique):

        outfit["rank"] = index + 1

    return unique


# ============================================================
# FORMAT PRODUCT
# ============================================================

def format_product(result):

    item = result["product"]

    return {

        "id": item.id,

        "name": item.name,

        "brand": item.brand,

        "source": item.source,

        "price": item.price,

        "currency": item.currency,

        "color": item.color,

        "style": item.style,

        "category": get_category(item),

        "image_url": item.image_url,

        "buy_url": item.product_url,

        "description": item.description,

        "sizes": item.sizes,

        "score": result["score"],

        "reasons": result["reasons"]
    }