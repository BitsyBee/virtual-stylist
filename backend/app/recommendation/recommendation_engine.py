from app.models.clothing_item import ClothingItem


def calculate_outfit_compatibility(
    top,
    bottom,
    shoes,
    occasion
):
    score = 0
    reasons = []

    requested_occasion = occasion.strip().lower()

    # ------------------------------------------------
    # PREFERRED STYLES FOR EACH OCCASION
    # ------------------------------------------------

    preferred_styles = {
        "interview": ["formal"],
        "office": ["formal", "smart casual"],
        "presentation": ["formal", "smart casual"],
        "party": ["casual", "smart casual"],
        "university": ["casual", "smart casual"],
        "sports": ["sport"],
        "casual outing": ["casual", "smart casual"]
    }

    preferred = preferred_styles.get(
        requested_occasion,
        []
    )

    # ------------------------------------------------
    # CHECK TOP + BOTTOM + SHOES
    # ------------------------------------------------

    items = [top, bottom, shoes]

    matching_items = 0

    for item in items:

        item_style = item["style"].strip().lower()

        if item_style in preferred:
            matching_items += 1

    # ------------------------------------------------
    # COMPATIBILITY SCORE
    # ------------------------------------------------

    if matching_items == 3:

        score += 30

        reasons.append(
            "All items match the preferred style for this occasion"
        )

    elif matching_items == 2:

        score += 15

        reasons.append(
            "Most items match the preferred style for this occasion"
        )

    elif matching_items == 1:

        score += 5

        reasons.append(
            "Some items match the preferred style for this occasion"
        )

    else:

        score -= 10

        reasons.append(
            "Items have limited style compatibility"
        )

    return score, reasons

def score_item(
    item,
    profile,
    occasion,
    style,
    temperature,
    season
):
    score = 0
    reasons = []

    # ------------------------------------------------
    # USER PROFILE
    # ------------------------------------------------

    user_skin_tone = (
        profile.skin_tone.strip().lower()
        if profile.skin_tone
        else None
    )

    user_body_type = (
        profile.body_type.strip().lower()
        if profile.body_type
        else None
    )

    user_gender = (
        profile.gender.strip().lower()
        if profile.gender
        else None
    )

    favorite_colors = []

    if profile.favorite_colors:
        favorite_colors = [
            color.strip().lower()
            for color in profile.favorite_colors.split(",")
        ]

    # ------------------------------------------------
    # 1. OCCASION - 35 POINTS
    # ------------------------------------------------

    if item.occasion:

        item_occasions = [
            value.strip().lower()
            for value in item.occasion.split(",")
        ]

        requested_occasion = occasion.strip().lower()

        if requested_occasion in item_occasions:

            score += 35

            reasons.append(
                "Matches requested occasion"
        )

        else:
            score -= 10
            reasons.append("Different from requested occasion")

    # ------------------------------------------------
    # 2. STYLE - 25 POINTS
    # ------------------------------------------------

    
    if item.style:

        if item.style.lower() == style.lower():
            score += 25
            reasons.append("Matches requested style")

        else:
            score -= 5
            reasons.append("Different from requested style")

    # ------------------------------------------------
    # 3. SKIN TONE - 15 POINTS
    # ------------------------------------------------

    if (
        user_skin_tone
        and item.recommended_skin_tones
    ):
        recommended_skin_tones = [
            tone.strip().lower()
            for tone in item.recommended_skin_tones.split(",")
        ]

        if user_skin_tone in recommended_skin_tones:
            score += 15
            reasons.append("Suitable for your skin tone")

    # ------------------------------------------------
    # 4. BODY TYPE - 10 POINTS
    # ------------------------------------------------

    if (
        user_body_type
        and item.recommended_body_types
    ):
        recommended_body_types = [
            body.strip().lower()
            for body in item.recommended_body_types.split(",")
        ]

        if user_body_type in recommended_body_types:
            score += 10
            reasons.append("Suitable for your body type")

    # ------------------------------------------------
    # 5. FAVORITE COLOR - 10 POINTS
    # ------------------------------------------------

    if (
        item.color
        and item.color.lower() in favorite_colors
    ):
        score += 10
        reasons.append("Matches your favorite color")

    # ------------------------------------------------
    # 6. GENDER COMPATIBILITY - 5 POINTS
    # ------------------------------------------------

    if item.gender:

        item_gender = item.gender.strip().lower()

        if (
            item_gender != "unisex"
            and item_gender != user_gender
        ):
            return None

        if item_gender == user_gender:
            score += 5
            reasons.append("Suitable for your gender")

        elif item_gender == "unisex":
            score += 5
            reasons.append("Suitable for all genders")

    # ------------------------------------------------
    # 7. TEMPERATURE - 5 POINTS
    # ------------------------------------------------


    if item.temperature:

        item_temperature = item.temperature.strip().lower()
        requested_temperature = temperature.strip().lower()

        if item_temperature == requested_temperature:

            score += 5

            reasons.append(
                "Suitable for the requested temperature"
            )

        elif item_temperature == "any":

            reasons.append(
                "Suitable for different temperatures"
            )

        else:

            score -= 15

            reasons.append(
                "Not suitable for the requested temperature"
            )

    # ------------------------------------------------
    # 8. SEASON - 5 POINTS
    # ------------------------------------------------

    if item.season:

        item_season = item.season.strip().lower()
        requested_season = season.strip().lower()

        if item_season == requested_season:

            score += 5

            reasons.append(
                "Suitable for the requested season"
            )

        elif item_season == "all season":

            score += 3

            reasons.append(
                "Suitable for all seasons"
            )

        else:

            score -= 5

            reasons.append(
                "Not suitable for the requested season"
            )

    return {
        "score": score,
        "name": item.name,
        "category": item.category,
        "gender": item.gender,
        "color": item.color,
        "style": item.style,
        "occasion": item.occasion,
        "fit": item.fit,
        "material": item.material,
        "season": item.season,
        "temperature": item.temperature,
        "image_url": item.image_url,
        "buy_url": item.buy_url or "#",
        "brand": item.brand or "E-Commerce Partner",
        "reasons": reasons
    }


def recommend_outfits(
    profile,
    clothing_items,
    occasion,
    style,
    temperature,
    season
):

    tops = []
    bottoms = []
    shoes = []

    # ------------------------------------------------
    # SCORE ALL CLOTHING ITEMS
    # ------------------------------------------------

    for item in clothing_items:

        scored_item = score_item(
            item,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        # Skip incompatible gender items
        if scored_item is None:
            continue

        if item.category == "Top":
            tops.append(scored_item)

        elif item.category == "Bottom":
            bottoms.append(scored_item)

        elif item.category == "Shoes":
            shoes.append(scored_item)

    # ------------------------------------------------
    # SORT EACH CATEGORY
    # ------------------------------------------------

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

    # ------------------------------------------------
    # CREATE OUTFITS
    # ------------------------------------------------

    outfits = []

    for top in tops[:5]:

        for bottom in bottoms[:5]:

            for shoe in shoes[:5]:


                # ------------------------------------------------
                # OUTFIT COMPATIBILITY
                # ------------------------------------------------

                compatibility_score, compatibility_reasons = calculate_outfit_compatibility(
                    top,
                    bottom,
                    shoe,
                    occasion
                )

                outfit_score = (
                    top["score"]
                    + bottom["score"]
                    + shoe["score"]
                    + compatibility_score
                )

                outfit_reasons = (
                    compatibility_reasons
                )
                outfits.append(
                    {
                        "score": outfit_score,
                        "top": top,
                        "bottom": bottom,
                        "shoes": shoe,

                        "compatibility_reasons": outfit_reasons
                    }
                )

    # ------------------------------------------------
    # SORT OUTFITS
    # ------------------------------------------------

    outfits.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # ------------------------------------------------
    # RETURN TOP 5 OUTFITS
    # ------------------------------------------------

    top_outfits = outfits[:5]

    for index, outfit in enumerate(top_outfits):
        outfit["rank"] = index + 1

    return top_outfits

def score_live_product(
    product,
    profile,
    occasion,
    style,
    temperature,
    season
):

    score = 0
    reasons = []

    def text(value):
        return (
            str(value).strip().lower()
            if value
            else ""
        )

    product_text = " ".join([
        text(product.name),
        text(product.description),
        text(product.color),
        text(product.style),
        text(product.category),
        text(product.tags)
    ])

    # ==========================================
    # GENDER
    # ==========================================

    product_gender = text(product.gender)
    user_gender = text(profile.gender)

    if (
        product_gender
        and user_gender
        and product_gender not in [
            "unisex",
            user_gender
        ]
    ):
        return None

    score += 10

    reasons.append(
        "Compatible with your profile."
    )

    # ==========================================
    # OCCASION
    # ==========================================

    occasion_text = text(occasion)

    if occasion_text in product_text:

        score += 25

        reasons.append(
            f"Suitable for a {occasion}."
        )

    # ==========================================
    # STYLE
    # ==========================================

    requested_style = text(style)

    if requested_style in product_text:

        score += 20

        reasons.append(
            f"Matches your {style} style preference."
        )

    # ==========================================
    # FAVOURITE COLOURS
    # ==========================================

    favorite_colors = text(
        profile.favorite_colors
    )

    product_color = text(
        product.color
    )

    if favorite_colors and product_color:

        for color in favorite_colors.split(","):

            color = color.strip()

            if color and color in product_color:

                score += 10

                reasons.append(
                    f"Matches your preferred {color} colour."
                )

                break

    # ==========================================
    # SKIN TONE
    # ==========================================

    skin_tone = text(
        profile.skin_tone
    )

    skin_rules = {

        "warm": [
            "olive",
            "brown",
            "beige",
            "cream",
            "orange",
            "rust",
            "mustard",
            "green",
            "navy"
        ],

        "cool": [
            "blue",
            "navy",
            "grey",
            "gray",
            "white",
            "purple",
            "pink"
        ],

        "neutral": [
            "black",
            "white",
            "navy",
            "grey",
            "gray",
            "beige",
            "olive"
        ]
    }

    for tone_key, colours in skin_rules.items():

        if tone_key in skin_tone:

            if any(
                colour in product_text
                for colour in colours
            ):

                score += 15

                reasons.append(
                    "The colour is compatible with your skin tone."
                )

            break

    # ==========================================
    # TEMPERATURE
    # ==========================================

    if (
        text(temperature)
        and text(temperature) in product_text
    ):

        score += 10

        reasons.append(
            "Suitable for the requested temperature."
        )

    return {
        "product": product,
        "score": score,
        "reasons": reasons
    }

def calculate_ecommerce_compatibility(
    top,
    bottom,
    shoes,
    occasion
):

    score = 0
    reasons = []

    top_color = (
        top["product"].color or ""
    ).lower()

    bottom_color = (
        bottom["product"].color or ""
    ).lower()

    shoe_color = (
        shoes["product"].color or ""
    ).lower()

    neutrals = [
        "black",
        "white",
        "navy",
        "grey",
        "gray",
        "beige",
        "brown",
        "cream"
    ]

    if (
        any(
            n in top_color
            for n in neutrals
        )
        or
        any(
            n in bottom_color
            for n in neutrals
        )
    ):

        score += 10

        reasons.append(
            "The outfit uses a balanced colour combination."
        )

    if any(
        n in shoe_color
        for n in neutrals
    ):

        score += 10

        reasons.append(
            "The footwear provides a versatile neutral finish."
        )

    return score, reasons

def serialize_product(item):

    product = item["product"]

    return {
        "id": product.product_url,
        "name": product.name,
        "brand": product.brand,
        "source": product.source,
        "category": product.category,
        "color": product.color,
        "style": product.style,
        "price": product.price,
        "currency": product.currency,
        "image_url": product.image_url,
        "buy_url": product.product_url,
        "availability": product.availability,
        "score": round(
            item["score"],
            2
        ),
        "reasons": item["reasons"]
    }

def recommend_ecommerce_outfits(
    candidates,
    profile,
    occasion,
    style,
    temperature,
    season
):

    tops = []
    bottoms = []
    shoes = []

    # ==========================================
    # SCORE TOPS
    # ==========================================

    for product in candidates.get("Top", []):

        scored = score_live_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        if scored:
            tops.append(scored)

    # ==========================================
    # SCORE BOTTOMS
    # ==========================================

    for product in candidates.get("Bottom", []):

        scored = score_live_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        if scored:
            bottoms.append(scored)

    # ==========================================
    # SCORE SHOES
    # ==========================================

    for product in candidates.get("Shoes", []):

        scored = score_live_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        if scored:
            shoes.append(scored)

    # ==========================================
    # CHECK REQUIRED CATEGORIES
    # ==========================================

    if not tops:
        return {
            "message": "No suitable tops were found."
        }

    if not bottoms:
        return {
            "message": "No suitable bottoms were found."
        }

    if not shoes:
        return {
            "message": "No suitable shoes were found."
        }

    # ==========================================
    # SORT PRODUCTS
    # ==========================================

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

    # ==========================================
    # BUILD OUTFITS
    # ==========================================

    outfits = []

    for top in tops[:8]:

        for bottom in bottoms[:8]:

            for shoe in shoes[:8]:

                compatibility_score, compatibility_reasons = (
                    calculate_ecommerce_compatibility(
                        top,
                        bottom,
                        shoe,
                        occasion
                    )
                )

                total_score = (
                    top["score"]
                    + bottom["score"]
                    + shoe["score"]
                    + compatibility_score
                )

                reasons = []

                reasons.extend(
                    top["reasons"]
                )

                reasons.extend(
                    bottom["reasons"]
                )

                reasons.extend(
                    shoe["reasons"]
                )

                reasons.extend(
                    compatibility_reasons
                )

                outfits.append({
                    "score": total_score,
                    "top": top,
                    "bottom": bottom,
                    "shoes": shoe,
                    "reasons": list(
                        dict.fromkeys(reasons)
                    )
                })

    # ==========================================
    # SORT COMPLETE OUTFITS
    # ==========================================

    outfits.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # ==========================================
    # DIVERSITY
    # ==========================================

    selected = []

    used_products = set()

    for outfit in outfits:

        product_urls = {
            outfit["top"]["product"].product_url,
            outfit["bottom"]["product"].product_url,
            outfit["shoes"]["product"].product_url
        }

        if product_urls & used_products:
            continue

        selected.append(outfit)

        used_products.update(
            product_urls
        )

        if len(selected) == 5:
            break

    # ==========================================
    # FINAL RESPONSE
    # ==========================================

    results = []

    for rank, outfit in enumerate(
        selected,
        start=1
    ):

        results.append({
            "rank": rank,
            "score": round(
                outfit["score"],
                2
            ),
            "reasons": outfit["reasons"],

            "top": serialize_product(
                outfit["top"]
            ),

            "bottom": serialize_product(
                outfit["bottom"]
            ),

            "shoes": serialize_product(
                outfit["shoes"]
            )
        })

    return results

# =========================================================
# E-COMMERCE PRODUCT RECOMMENDATION
# =========================================================


def _text(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def _matches(value, requested):
    """
    Supports comma-separated metadata.
    """

    if not value or not requested:
        return False

    requested = _text(requested)

    values = [
        _text(v)
        for v in str(value).split(",")
    ]

    return requested in values


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

    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    product_gender = _text(
        product.gender
    )

    profile_gender = _text(
        profile.gender
    )

    if (
        product_gender
        and profile_gender
        and product_gender != "unisex"
        and product_gender != profile_gender
    ):

        return None

    score += 10

    reasons.append(
        "Suitable for the user's gender profile."
    )

    # -----------------------------------------------------
    # OCCASION
    # -----------------------------------------------------

    if _matches(
        product.occasion,
        occasion
    ):

        score += 20

        reasons.append(
            f"Suitable for the {occasion} occasion."
        )

    elif _text(product.occasion) == "casual":

        score += 5

    # -----------------------------------------------------
    # STYLE
    # -----------------------------------------------------

    if _text(product.style) == _text(style):

        score += 20

        reasons.append(
            f"Matches the requested {style} style."
        )

    # -----------------------------------------------------
    # TEMPERATURE
    # -----------------------------------------------------

    if _text(
        product.temperature
    ) == _text(temperature):

        score += 15

        reasons.append(
            f"Suitable for {temperature} conditions."
        )

    # -----------------------------------------------------
    # SKIN TONE
    # -----------------------------------------------------

    if _matches(
        product.recommended_skin_tones,
        profile.skin_tone
    ):

        score += 15

        reasons.append(
            "Colour is suitable for the user's skin tone."
        )

    # -----------------------------------------------------
    # BODY TYPE
    # -----------------------------------------------------

    if _matches(
        product.recommended_body_types,
        profile.body_type
    ):

        score += 10

        reasons.append(
            "Suitable for the user's body type."
        )

    # -----------------------------------------------------
    # FAVORITE COLORS
    # -----------------------------------------------------

    favorite_colors = _text(
        profile.favorite_colors
    )

    product_color = _text(
        product.color
    )

    if (
        favorite_colors
        and product_color
    ):

        for color in favorite_colors.split(","):

            if _text(color) in product_color:

                score += 5

                reasons.append(
                    "Matches one of the user's preferred colors."
                )

                break

    # -----------------------------------------------------
    # AVAILABILITY
    # -----------------------------------------------------

    if (
        product.availability
        == "available"
    ):

        score += 5

        reasons.append(
            "Currently available from the retailer."
        )

    return {
        "score": score,
        "reasons": reasons,
        "product": product
    }

def recommend_ecommerce_outfits(
    candidates,
    profile,
    occasion,
    style,
    temperature,
    season
):

    tops = []
    bottoms = []
    shoes = []

    # ==========================================
    # SCORE PRODUCTS
    # ==========================================

    for product in candidates.get("Top", []):

        scored = score_live_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        if scored:
            tops.append(scored)


    for product in candidates.get("Bottom", []):

        scored = score_live_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        if scored:
            bottoms.append(scored)


    for product in candidates.get("Shoes", []):

        scored = score_live_product(
            product,
            profile,
            occasion,
            style,
            temperature,
            season
        )

        if scored:
            shoes.append(scored)


    # ==========================================
    # SORT
    # ==========================================

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


    # ==========================================
    # SAFETY CHECK
    # ==========================================

    if not tops:
        return {
            "message":
            "No suitable tops were found."
        }

    if not bottoms:
        return {
            "message":
            "No suitable bottoms were found."
        }

    if not shoes:
        return {
            "message":
            "No suitable shoes were found."
        }


    # ==========================================
    # BUILD OUTFITS
    # ==========================================

    outfits = []

    for top in tops[:8]:

        for bottom in bottoms[:8]:

            for shoe in shoes[:8]:

                compatibility_score, compatibility_reasons = (
                    calculate_ecommerce_compatibility(
                        top,
                        bottom,
                        shoe,
                        occasion
                    )
                )

                score = (
                    top["score"]
                    + bottom["score"]
                    + shoe["score"]
                    + compatibility_score
                )

                reasons = []

                reasons.extend(
                    top["reasons"]
                )

                reasons.extend(
                    bottom["reasons"]
                )

                reasons.extend(
                    shoe["reasons"]
                )

                reasons.extend(
                    compatibility_reasons
                )

                outfits.append({
                    "score": score,
                    "top": top,
                    "bottom": bottom,
                    "shoes": shoe,
                    "reasons": list(
                        dict.fromkeys(reasons)
                    )
                })


    # ==========================================
    # SORT COMPLETE OUTFITS
    # ==========================================

    outfits.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # ==========================================
    # DIVERSITY
    # ==========================================

    selected = []

    used_products = set()

    for outfit in outfits:

        product_ids = {
            outfit["top"]["product"].product_url,
            outfit["bottom"]["product"].product_url,
            outfit["shoes"]["product"].product_url
        }

        # Avoid repeating the same pieces
        if product_ids & used_products:
            continue

        selected.append(outfit)

        used_products.update(
            product_ids
        )

        if len(selected) == 5:
            break


    # ==========================================
    # FORMAT OUTPUT
    # ==========================================

    results = []

    for rank, outfit in enumerate(
        selected,
        start=1
    ):

        results.append({

            "rank": rank,

            "score": round(
                outfit["score"],
                2
            ),

            "reasons": outfit["reasons"],

            "top": serialize_product(
                outfit["top"]
            ),

            "bottom": serialize_product(
                outfit["bottom"]
            ),

            "shoes": serialize_product(
                outfit["shoes"]
            )

        })

    return results

def serialize_product(scored_product):

    product = scored_product["product"]

    return {

        "id": product.id,

        "name": product.name,

        "brand": product.brand,

        "source": product.source,

        "category": product.category,

        "color": product.color,

        "style": product.style,

        "occasion": product.occasion,

        "temperature": product.temperature,

        "material": product.material,

        "price": product.price,

        "currency": product.currency,

        "image_url": product.image_url,

        "product_url": product.product_url,

        "availability":
            product.availability,

        "sizes":
            product.sizes,

        "score":
            scored_product["score"],

        "reasons":
            scored_product["reasons"]
    }