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