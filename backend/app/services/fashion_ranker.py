# ============================================================
# FASHION RANKER
# Personalized ranking for live e-commerce products
# ============================================================

import re


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(value):
    if value is None:
        return ""

    return str(value).strip().lower()


# ============================================================
# TEXT MATCHING
# ============================================================

def contains_any(text, words):
    text = normalize(text)

    return any(
        word.lower() in text
        for word in words
    )


# ============================================================
# COLOR INFORMATION
# ============================================================

COLOR_FAMILIES = {

    "black": [
        "black"
    ],

    "white": [
        "white",
        "off white",
        "cream",
        "ivory"
    ],

    "blue": [
        "blue",
        "navy",
        "denim",
        "sky blue"
    ],

    "green": [
        "green",
        "olive",
        "forest",
        "khaki"
    ],

    "brown": [
        "brown",
        "beige",
        "tan",
        "camel"
    ],

    "grey": [
        "grey",
        "gray",
        "charcoal"
    ],

    "red": [
        "red",
        "burgundy",
        "maroon"
    ],

    "pink": [
        "pink"
    ],

    "yellow": [
        "yellow",
        "mustard"
    ],

    "orange": [
        "orange"
    ],

    "purple": [
        "purple",
        "violet"
    ]
}


def get_color_family(color):

    text = normalize(color)

    for family, keywords in COLOR_FAMILIES.items():

        if any(
            keyword in text
            for keyword in keywords
        ):
            return family

    return None


# ============================================================
# OCCASION RULES
# ============================================================

OCCASION_RULES = {

    "interview": {
        "preferred_styles": [
            "formal",
            "business",
            "business casual",
            "smart casual"
        ],

        "preferred_items": [
            "shirt",
            "trouser",
            "chino",
            "loafer",
            "blazer"
        ],

        "avoid": [
            "graphic",
            "ripped",
            "shorts",
            "oversize"
        ]
    },

    "office": {
        "preferred_styles": [
            "formal",
            "business",
            "business casual",
            "smart casual"
        ],

        "preferred_items": [
            "shirt",
            "trouser",
            "chino",
            "loafer",
            "blazer"
        ],

        "avoid": [
            "graphic",
            "ripped"
        ]
    },

    "university": {
        "preferred_styles": [
            "casual",
            "smart casual",
            "streetwear",
            "minimalist"
        ],

        "preferred_items": [
            "shirt",
            "t-shirt",
            "jeans",
            "chino",
            "sneaker"
        ],

        "avoid": [
            "very formal"
        ]
    },

    "casual outing": {
        "preferred_styles": [
            "casual",
            "smart casual",
            "streetwear"
        ],

        "preferred_items": [
            "t-shirt",
            "shirt",
            "jeans",
            "chino",
            "sneaker"
        ],

        "avoid": []
    },

    "date": {
        "preferred_styles": [
            "smart casual",
            "casual",
            "minimalist"
        ],

        "preferred_items": [
            "shirt",
            "polo",
            "chino",
            "jeans",
            "loafer",
            "sneaker"
        ],

        "avoid": [
            "ripped",
            "graphic"
        ]
    },

    "party": {
        "preferred_styles": [
            "casual",
            "streetwear",
            "smart casual"
        ],

        "preferred_items": [
            "shirt",
            "polo",
            "jeans",
            "sneaker"
        ],

        "avoid": []
    }
}


# ============================================================
# STYLE DETECTION
# ============================================================

def detect_style(product):

    text = " ".join([
        normalize(product.get("name")),
        normalize(product.get("description")),
        normalize(product.get("category")),
        normalize(product.get("style"))
    ])

    actual_style = normalize(
        product.get("style")
    )

    if actual_style:

        if "business casual" in actual_style:
            return "business casual"

        if "smart casual" in actual_style:
            return "smart casual"

        if "streetwear" in actual_style:
            return "streetwear"

        if "preppy" in actual_style:
            return "preppy"

        if "minimalist" in actual_style:
            return "minimalist"

        if "formal" in actual_style:
            return "formal"

        if "casual" in actual_style:
            return "casual"


    if contains_any(text, [
        "blazer",
        "formal",
        "dress shirt",
        "oxford"
    ]):

        return "formal"


    if contains_any(text, [
        "chino",
        "trouser",
        "polo",
        "oxford",
        "smart"
    ]):

        return "smart casual"


    if contains_any(text, [
        "oversize",
        "cargo",
        "graphic",
        "street"
    ]):

        return "streetwear"


    if contains_any(text, [
        "jean",
        "t-shirt",
        "tee",
        "short"
    ]):

        return "casual"


    return "casual"


# ============================================================
# OCCASION MATCHING
# ============================================================

def score_occasion(product, occasion):

    occasion = normalize(occasion)

    rule = OCCASION_RULES.get(
        occasion,
        None
    )

    if not rule:
        return 0, []

    text = " ".join([
        normalize(product.get("name")),
        normalize(product.get("description")),
        normalize(product.get("category"))
    ])

    score = 0
    reasons = []

    style = detect_style(product)

    if style in rule["preferred_styles"]:

        score += 20

        reasons.append(
            f"{style.title()} style suits a {occasion}."
        )

    for item in rule["preferred_items"]:

        if item in text:

            score += 8

            reasons.append(
                f"The {item} style is appropriate for this occasion."
            )

            break

    for avoid in rule["avoid"]:

        if avoid in text:

            score -= 15

            reasons.append(
                f"The item contains a {avoid} style that is less suitable."
            )

    return score, reasons


# ============================================================
# USER STYLE PREFERENCE
# ============================================================

def score_user_style(
    product,
    style_preference
):

    if not style_preference:
        return 0, []

    requested_style = normalize(
        style_preference
    )

    detected_style = detect_style(
        product
    )

    compatible_styles = {

        "casual": [
            "casual",
            "smart casual"
        ],

        "smart casual": [
            "smart casual",
            "casual",
            "formal"
        ],

        "formal": [
            "formal",
            "smart casual"
        ],

        "streetwear": [
            "streetwear",
            "casual"
        ],

        "minimalist": [
            "minimalist",
            "smart casual",
            "casual"
        ]
    }

    if detected_style in compatible_styles.get(
        requested_style,
        []
    ):

        return 20, [
            (
                f"It matches your preferred "
                f"{style_preference} style."
            )
        ]

    return 0, []


# ============================================================
# COLOR PREFERENCE
# ============================================================

def score_color_preference(
    product,
    favorite_colors=None,
    requested_colors=None
):

    score = 0
    reasons = []

    product_color = product.get(
        "color"
    )

    if not product_color:
        return 0, []

    product_family = get_color_family(
        product_color
    )

    colors = []

    if favorite_colors:

        if isinstance(
            favorite_colors,
            str
        ):

            colors.extend(
                [
                    x.strip()
                    for x in favorite_colors.split(",")
                    if x.strip()
                ]
            )

        elif isinstance(
            favorite_colors,
            list
        ):

            colors.extend(
                favorite_colors
            )

    if requested_colors:

        if isinstance(
            requested_colors,
            str
        ):

            colors.extend(
                [
                    x.strip()
                    for x in requested_colors.split(",")
                    if x.strip()
                ]
            )

        elif isinstance(
            requested_colors,
            list
        ):

            colors.extend(
                requested_colors
            )

    for color in colors:

        if product_family == get_color_family(
            color
        ):

            score += 15

            reasons.append(
                f"The {product_color} colour matches your requested/preferred colours."
            )

            break

    return score, reasons


# ============================================================
# SKIN TONE / COLOR THEORY
# ============================================================

SKIN_TONE_COLORS = {

    "warm": [
        "brown",
        "green",
        "olive",
        "beige",
        "cream",
        "navy",
        "orange",
        "mustard",
        "burgundy"
    ],

    "cool": [
        "blue",
        "navy",
        "grey",
        "purple",
        "pink",
        "white"
    ],

    "neutral": [
        "black",
        "white",
        "grey",
        "blue",
        "green",
        "beige"
    ]
}


def score_skin_tone(
    product,
    skin_tone
):

    if not skin_tone:
        return 0, []

    tone = normalize(
        skin_tone
    )

    product_color = normalize(
        product.get("color")
    )

    if not product_color:
        return 0, []

    preferred_colors = SKIN_TONE_COLORS.get(
        tone,
        []
    )

    for color in preferred_colors:

        if color in product_color:

            return 15, [
                f"The {product.get('color')} colour complements a {tone} skin tone according to colour harmony principles."
            ]

    return 0, []


# ============================================================
# BODY TYPE
# ============================================================

BODY_TYPE_RULES = {

    "athletic": {

        "preferred": [
            "slim",
            "straight",
            "regular",
            "structured"
        ],

        "avoid": []
    },

    "slim": {

        "preferred": [
            "regular",
            "straight",
            "oversize",
            "layered"
        ],

        "avoid": [
            "skinny"
        ]
    },

    "average": {

        "preferred": [
            "regular",
            "straight",
            "slim"
        ],

        "avoid": []
    },

    "plus size": {

        "preferred": [
            "regular",
            "straight",
            "relaxed"
        ],

        "avoid": [
            "skinny"
        ]
    }
}


def score_body_type(
    product,
    body_type
):

    if not body_type:
        return 0, []

    body_type = normalize(
        body_type
    )

    rules = BODY_TYPE_RULES.get(
        body_type
    )

    if not rules:
        return 0, []

    text = " ".join([
        normalize(product.get("name")),
        normalize(product.get("description"))
    ])

    for preferred in rules["preferred"]:

        if preferred in text:

            return 10, [
                f"The {preferred} silhouette can complement your {body_type} body type."
            ]

    return 0, []


# ============================================================
# TEMPERATURE
# ============================================================

def score_temperature(
    product,
    temperature
):

    if not temperature:
        return 0, []

    temperature = normalize(
        temperature
    )

    text = " ".join([
        normalize(product.get("name")),
        normalize(product.get("description"))
    ])

    score = 0
    reasons = []

    if temperature in [
        "warm",
        "hot",
        "summer"
    ]:

        if contains_any(
            text,
            [
                "linen",
                "short sleeve",
                "short-sleeve",
                "cotton",
                "t-shirt",
                "tee"
            ]
        ):

            score += 12

            reasons.append(
                "The lightweight style is suitable for warm weather."
            )

    elif temperature in [
        "cold",
        "cool",
        "winter"
    ]:

        if contains_any(
            text,
            [
                "long sleeve",
                "jacket",
                "hoodie",
                "sweater",
                "coat"
            ]
        ):

            score += 12

            reasons.append(
                "The style provides more coverage for cooler weather."
            )

    return score, reasons


def score_gender(
    product,
    user_gender
):
    """
    Filter out products that don't match the user's profile
    gender. Products tagged "Unisex" (or with no gender tag
    at all, e.g. legacy/unclassified data) are always allowed.
    Returns None as the score sentinel — callers should treat
    a None result as "exclude this product".
    """

    if not user_gender:
        return 0, []

    user_gender = normalize(user_gender)

    product_gender = normalize(product.get("gender"))

    if not product_gender or product_gender == "unisex":
        return 0, []

    if product_gender == user_gender:
        return 5, [
            "Suitable for your gender profile."
        ]

    # Product is explicitly tagged for a different gender.
    return None, []


# ============================================================
# MAIN PRODUCT SCORER
# ============================================================

def score_product(
    product,
    user_profile=None,
    request_context=None
):

    user_profile = user_profile or {}
    request_context = request_context or {}

    score = 0
    reasons = []

    # --------------------------------------------------------
    # GENDER (must be checked first — excludes the product
    # entirely if it doesn't match the user's profile)
    # --------------------------------------------------------

    value, explanation = score_gender(
        product,
        user_profile.get("gender")
    )

    if value is None:
        return None

    score += value
    reasons.extend(explanation)

    # --------------------------------------------------------
    # OCCASION
    # --------------------------------------------------------

    occasion = request_context.get(
        "occasion"
    )

    value, explanation = score_occasion(
        product,
        occasion
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # E-COMMERCE SOURCE
    # --------------------------------------------------------

    value, explanation = score_source(
        product
    )

    score += value

    reasons.extend(
        explanation
    )
    # --------------------------------------------------------
    # USER STYLE
    # --------------------------------------------------------

    value, explanation = score_user_style(
        product,
        user_profile.get(
            "style_preference"
        )
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # COLOR
    # --------------------------------------------------------

    value, explanation = score_color_preference(
        product,
        user_profile.get(
            "favorite_colors"
        ),
        request_context.get(
            "colors"
        )
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # SKIN TONE
    # --------------------------------------------------------

    value, explanation = score_skin_tone(
        product,
        user_profile.get(
            "skin_tone"
        )
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # BODY TYPE
    # --------------------------------------------------------

    value, explanation = score_body_type(
        product,
        user_profile.get(
            "body_type"
        )
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    value, explanation = score_temperature(
        product,
        request_context.get(
            "temperature"
        )
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # FALLBACK EXPLANATION
    # --------------------------------------------------------

    if not reasons:

        reasons.append(
            "This item matches the general requirements of the requested outfit."
        )

    return {
        **product,

        "score": round(
            score,
            2
        ),

        "recommendation_reasons": reasons
    }


# ============================================================
# RANK PRODUCTS
# ============================================================

def rank_products(
    products,
    user_profile=None,
    request_context=None,
    limit=10
):

    scored = []

    for product in products:

        result = score_product(
            product,
            user_profile,
            request_context
        )

        # score_product returns None when the product is
        # excluded (e.g. gender mismatch) — skip it entirely
        # instead of letting it leak into recommendations.
        if result is None:
            continue

        scored.append(result)

    scored.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored[:limit]

def score_source(
    product
):

    source = normalize(
        product.get("source")
    )

    if source:

        return 2, [
            f"Available from {product.get('source')}."
        ]

    return 0, []

