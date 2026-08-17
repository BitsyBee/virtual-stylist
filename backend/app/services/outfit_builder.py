# ============================================================
# OUTFIT BUILDER
# Combines ranked e-commerce products into complete outfits
# ============================================================

from itertools import product


# ============================================================
# COLOR COMPATIBILITY
# ============================================================

COLOR_COMPATIBILITY = {

    "black": [
        "white",
        "black",
        "grey",
        "blue",
        "beige",
        "brown",
        "green"
    ],

    "white": [
        "black",
        "white",
        "blue",
        "grey",
        "beige",
        "brown",
        "green"
    ],

    "blue": [
        "white",
        "black",
        "beige",
        "brown",
        "grey",
        "blue"
    ],

    "green": [
        "white",
        "black",
        "beige",
        "brown",
        "navy",
        "green"
    ],

    "brown": [
        "white",
        "beige",
        "black",
        "blue",
        "green"
    ],

    "beige": [
        "white",
        "black",
        "blue",
        "brown",
        "green"
    ],

    "grey": [
        "black",
        "white",
        "blue",
        "green",
        "burgundy"
    ],

    "red": [
        "black",
        "white",
        "grey",
        "navy"
    ],

    "pink": [
        "black",
        "white",
        "grey",
        "navy"
    ],

    "yellow": [
        "black",
        "white",
        "navy",
        "brown"
    ],

    "orange": [
        "black",
        "white",
        "navy",
        "brown"
    ]
}


# ============================================================
# COLOR FAMILY
# ============================================================

def get_color_family(color):

    if not color:
        return None

    text = str(color).lower()

    mapping = {

        "black": "black",
        "white": "white",
        "off white": "white",
        "cream": "white",

        "blue": "blue",
        "navy": "blue",
        "denim": "blue",

        "green": "green",
        "olive": "green",
        "forest": "green",

        "brown": "brown",
        "beige": "beige",
        "tan": "brown",

        "grey": "grey",
        "gray": "grey",
        "charcoal": "grey",

        "red": "red",
        "burgundy": "red",
        "maroon": "red",

        "pink": "pink",

        "yellow": "yellow",
        "mustard": "yellow",

        "orange": "orange"
    }

    for keyword, family in mapping.items():

        if keyword in text:
            return family

    return None


# ============================================================
# COLOR COMPATIBILITY
# ============================================================

def score_color_pair(
    product_a,
    product_b
):

    color_a = get_color_family(
        product_a.get("color")
    )

    color_b = get_color_family(
        product_b.get("color")
    )

    if not color_a or not color_b:

        return 0, []

    if color_b in COLOR_COMPATIBILITY.get(
        color_a,
        []
    ):

        return 15, [
            f"The {product_a.get('color')} and {product_b.get('color')} colours create a compatible colour combination."
        ]

    return -5, [
        f"The {product_a.get('color')} and {product_b.get('color')} colours have weaker colour harmony."
    ]


# ============================================================
# STYLE COMPATIBILITY
# ============================================================

def get_style(product):

    text = " ".join([
        str(product.get("name", "")).lower(),
        str(product.get("description", "")).lower()
    ])

    if any(
        x in text
        for x in [
            "blazer",
            "formal",
            "dress shirt",
            "oxford"
        ]
    ):

        return "formal"

    if any(
        x in text
        for x in [
            "chino",
            "trouser",
            "polo"
        ]
    ):

        return "smart casual"

    if any(
        x in text
        for x in [
            "oversize",
            "cargo",
            "graphic"
        ]
    ):

        return "streetwear"

    return "casual"


def score_style_pair(
    product_a,
    product_b
):

    style_a = get_style(
        product_a
    )

    style_b = get_style(
        product_b
    )

    if style_a == style_b:

        return 15, [
            f"The {style_a} styles work well together."
        ]

    compatible = {

        "formal": [
            "smart casual"
        ],

        "smart casual": [
            "formal",
            "casual"
        ],

        "casual": [
            "smart casual",
            "streetwear"
        ],

        "streetwear": [
            "casual"
        ]
    }

    if style_b in compatible.get(
        style_a,
        []
    ):

        return 8, [
            f"The {style_a} and {style_b} styles are compatible."
        ]

    return 0, []


# ============================================================
# OUTFIT SCORE
# ============================================================

def score_outfit(
    top,
    bottom,
    shoes,
    user_profile=None,
    request_context=None
):

    user_profile = user_profile or {}
    request_context = request_context or {}

    score = 0
    reasons = []

    # --------------------------------------------------------
    # INDIVIDUAL PRODUCT SCORES
    # --------------------------------------------------------

    score += top.get(
        "score",
        0
    )

    score += bottom.get(
        "score",
        0
    )

    score += shoes.get(
        "score",
        0
    )

    # --------------------------------------------------------
    # TOP + BOTTOM COLOUR
    # --------------------------------------------------------

    value, explanation = score_color_pair(
        top,
        bottom
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # TOP + SHOES COLOUR
    # --------------------------------------------------------

    value, explanation = score_color_pair(
        top,
        shoes
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # BOTTOM + SHOES COLOUR
    # --------------------------------------------------------

    value, explanation = score_color_pair(
        bottom,
        shoes
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # STYLE COMPATIBILITY
    # --------------------------------------------------------

    value, explanation = score_style_pair(
        top,
        bottom
    )

    score += value
    reasons.extend(
        explanation
    )

    value, explanation = score_style_pair(
        bottom,
        shoes
    )

    score += value
    reasons.extend(
        explanation
    )

    # --------------------------------------------------------
    # FINAL EXPLANATION
    # --------------------------------------------------------

    if request_context.get(
        "occasion"
    ):

        reasons.append(
            f"The outfit is ranked for the requested {request_context['occasion']} occasion."
        )

    if user_profile.get(
        "style_preference"
    ):

        reasons.append(
            f"It considers your {user_profile['style_preference']} style preference."
        )

    return {
        "top": top,
        "bottom": bottom,
        "shoes": shoes,

        "outfit_score": round(
            score,
            2
        ),

        "reasons": reasons
    }


# ============================================================
# BUILD OUTFITS
# ============================================================

def build_outfits(
    products,
    user_profile=None,
    request_context=None,
    limit=5
):

    tops = products.get(
        "Top",
        []
    )

    bottoms = products.get(
        "Bottom",
        []
    )

    shoes = products.get(
        "Shoes",
        []
    )

    # --------------------------------------------------------
    # IMPORTANT
    # --------------------------------------------------------

    if not tops or not bottoms or not shoes:

        return []

    outfits = []

    # --------------------------------------------------------
    # CREATE COMBINATIONS
    # --------------------------------------------------------

    for top, bottom, shoe in product(
        tops,
        bottoms,
        shoes
    ):

        outfit = score_outfit(
            top,
            bottom,
            shoe,
            user_profile,
            request_context
        )

        outfits.append(
            outfit
        )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    outfits.sort(
        key=lambda x: x["outfit_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # DIVERSITY
    # --------------------------------------------------------

    selected = []

    used_tops = set()
    used_bottoms = set()

    for outfit in outfits:

        top_url = outfit["top"].get(
            "product_url"
        )

        bottom_url = outfit["bottom"].get(
            "product_url"
        )

        # Don't show the same combination repeatedly.

        if (
            top_url in used_tops
            and bottom_url in used_bottoms
        ):

            continue

        selected.append(
            outfit
        )

        used_tops.add(
            top_url
        )

        used_bottoms.add(
            bottom_url
        )

        if len(selected) >= limit:

            break

    return selected