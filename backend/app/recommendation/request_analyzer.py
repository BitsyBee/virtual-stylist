import re


def _contains_any(text: str, values: list[str]) -> bool:
    return any(value in text for value in values)


def analyze_request(user_request: str) -> dict:
    text = user_request.lower().strip()

    result = {
        "occasion": None,
        "style": None,
        "temperature": None,
        "season": None,
        "preferred_colors": [],
        "categories": ["Top", "Bottom", "Shoes"],
        "gender": None,
        "keywords": []
    }

    # =========================================================
    # OCCASION
    # =========================================================

    occasion_rules = {
        "interview": [
            "interview",
            "job interview",
            "career interview"
        ],
        "university": [
            "university",
            "campus",
            "lecture",
            "presentation",
            "presentation day"
        ],
        "work": [
            "office",
            "work",
            "business",
            "meeting"
        ],
        "wedding": [
            "wedding",
            "wedding guest",
            "reception"
        ],
        "party": [
            "party",
            "club",
            "night out",
            "nightlife"
        ],
        "date": [
            "date",
            "dinner date"
        ],
        "casual": [
            "casual",
            "outing",
            "hangout",
            "everyday"
        ],
        "formal": [
            "formal",
            "ceremony",
            "gala"
        ],
        "sports": [
            "gym",
            "sport",
            "sports",
            "workout"
        ]
    }

    for occasion, keywords in occasion_rules.items():
        if _contains_any(text, keywords):
            result["occasion"] = occasion
            result["keywords"].append(occasion)
            break

    # =========================================================
    # STYLE
    # =========================================================

    style_rules = {
        "Formal": [
            "formal",
            "professional",
            "business formal"
        ],
        "Business Casual": [
            "business casual",
            "office casual"
        ],
        "Smart Casual": [
            "smart casual",
            "smart",
            "polished"
        ],
        "Casual": [
            "casual",
            "everyday",
            "relaxed"
        ],
        "Streetwear": [
            "streetwear",
            "street style",
            "urban"
        ],
        "Preppy": [
            "preppy",
            "preppy style"
        ],
        "Minimalist": [
            "minimal",
            "minimalist",
            "simple"
        ]
    }

    for style, keywords in style_rules.items():
        if _contains_any(text, keywords):
            result["style"] = style
            break

    # =========================================================
    # TEMPERATURE
    # =========================================================

    if _contains_any(
        text,
        [
            "hot",
            "hot weather",
            "warm",
            "warm weather",
            "humid",
            "tropical"
        ]
    ):
        result["temperature"] = "Warm"

    elif _contains_any(
        text,
        [
            "cold",
            "cold weather",
            "cool weather",
            "winter",
            "chilly"
        ]
    ):
        result["temperature"] = "Cold"

    elif _contains_any(
        text,
        [
            "cool",
            "mild"
        ]
    ):
        result["temperature"] = "Cool"

    # =========================================================
    # SEASON
    # =========================================================

    season_rules = {
        "Summer": ["summer"],
        "Winter": ["winter"],
        "Spring": ["spring"],
        "Autumn": ["autumn", "fall"],
        "Rainy": ["rainy", "rain", "monsoon"]
    }

    for season, keywords in season_rules.items():
        if _contains_any(text, keywords):
            result["season"] = season
            break

    # =========================================================
    # COLOURS
    # =========================================================

    colours = [
        "black",
        "white",
        "blue",
        "navy",
        "red",
        "green",
        "olive",
        "forest green",
        "brown",
        "beige",
        "cream",
        "grey",
        "gray",
        "pink",
        "purple",
        "burgundy",
        "maroon",
        "yellow",
        "orange"
    ]

    for colour in colours:
        if colour in text:
            result["preferred_colors"].append(colour)

    # =========================================================
    # GENDER
    # =========================================================

    if _contains_any(
        text,
        [
            "men",
            "man",
            "male",
            "mens"
        ]
    ):
        result["gender"] = "Male"

    elif _contains_any(
        text,
        [
            "women",
            "woman",
            "female",
            "womens"
        ]
    ):
        result["gender"] = "Female"

    # =========================================================
    # CATEGORY REQUIREMENTS
    # =========================================================

    category_text = []

    if _contains_any(
        text,
        [
            "shirt",
            "t-shirt",
            "tshirt",
            "top",
            "blouse",
            "polo"
        ]
    ):
        category_text.append("Top")

    if _contains_any(
        text,
        [
            "pants",
            "trousers",
            "jeans",
            "shorts",
            "skirt",
            "bottom"
        ]
    ):
        category_text.append("Bottom")

    if _contains_any(
        text,
        [
            "shoes",
            "shoe",
            "sneakers",
            "boots",
            "loafers",
            "heels"
        ]
    ):
        category_text.append("Shoes")

    # If the user asks for a complete outfit,
    # always search all three major categories.
    if _contains_any(
        text,
        [
            "outfit",
            "look",
            "dress me",
            "full outfit",
            "complete outfit"
        ]
    ):
        result["categories"] = [
            "Top",
            "Bottom",
            "Shoes"
        ]

    elif category_text:
        result["categories"] = list(dict.fromkeys(category_text))

    return result