from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.recommendation import RecommendationRequest
from app.models.profile import Profile
from app.services.dependencies import get_current_user

from app.recommendation.request_analyzer import analyze_request

from app.services.fashion_ranker import rank_products
from app.services.outfit_builder import build_outfits

from app.services.ecommerce_retrieval import (
    get_live_ecommerce_products
)

from app.services.ecommerce_retrieval import (
    group_products_by_category
)

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


# ============================================================
# HELPERS
# ============================================================

def profile_to_dict(profile):
    """
    Convert the user's profile into a dictionary
    used by the ranking engine.
    """

    return {
        "gender": profile.gender,
        "body_type": profile.body_type,
        "skin_tone": profile.skin_tone,
        "style_preference": profile.style_preference,
        "favorite_colors": profile.favorite_colors,
    }


# ============================================================
# RECOMMENDATION ENDPOINT
# ============================================================

@router.post("/")
def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # ========================================================
    # 1. GET USER PROFILE
    # ========================================================

    profile = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()

    if not profile:

        raise HTTPException(
            status_code=400,
            detail="Please create your profile first."
        )


    # ========================================================
    # 2. ANALYZE NATURAL LANGUAGE REQUEST
    # ========================================================

    request_context = analyze_request(
        request.user_request
    )


    # ========================================================
    # 3. GET LIVE E-COMMERCE PRODUCTS
    # ========================================================

    live_products = get_live_ecommerce_products(
        categories=[
            "Top",
            "Bottom",
            "Shoes"
        ],
        per_provider=10
    )


    if not live_products:

        return {
            "message":
                "No live e-commerce products "
                "could be retrieved.",
            "request_context":
                request_context
        }


    # ========================================================
    # 4. PRODUCTS ARE ALREADY NORMALIZED
    #    (live_products are plain dicts returned by the
    #    e-commerce providers, not SQLAlchemy objects, so no
    #    conversion step is needed here.)
    # ========================================================

    product_dicts = live_products

    if not product_dicts:

        return {
            "message": "No products are currently available.",
            "request_context": request_context
        }


    # ========================================================
    # 5. CREATE USER PROFILE DICTIONARY
    # ========================================================

    profile_data = profile_to_dict(
        profile
    )


    # ========================================================
    # 6. GROUP RAW PRODUCTS BY CATEGORY FIRST
    #    (Grouping must happen before ranking. Ranking all
    #    products together and then truncating to a single
    #    global limit can starve out an entire category —
    #    e.g. shoes — if tops/bottoms happen to score higher
    #    or simply outnumber them in the combined pool.)
    # ========================================================

    raw_categorized = group_products_by_category(
        product_dicts
    )

    ranking_context = {
        "occasion": request_context.get(
            "occasion"
        ),

        "temperature": request_context.get(
            "temperature"
        ),

        "season": request_context.get(
            "season"
        ),

        "colors": request_context.get(
            "preferred_colors"
        ),

        "style": request_context.get(
            "style"
        )
    }


    # ========================================================
    # 7. RANK EACH CATEGORY SEPARATELY
    # ========================================================

    categorized_products = {
        category: rank_products(
            items,
            user_profile=profile_data,
            request_context=ranking_context,
            limit=10
        )
        for category, items in raw_categorized.items()
    }


    # ========================================================
    # 8. CHECK REQUIRED CATEGORIES
    # ========================================================

    if not categorized_products["Top"]:

        return {
            "message": "No suitable tops were found.",
            "request_context": request_context
        }


    if not categorized_products["Bottom"]:

        return {
            "message": "No suitable bottoms were found.",
            "request_context": request_context
        }


    if not categorized_products["Shoes"]:

        return {
            "message": "No suitable shoes were found.",
            "request_context": request_context
        }


    # ========================================================
    # 9. BUILD COMPLETE OUTFITS
    # ========================================================

    outfits = build_outfits(
        categorized_products,
        user_profile=profile_data,
        request_context=request_context,
        limit=5
    )


    # ========================================================
    # 10. CHECK OUTFIT RESULTS
    # ========================================================

    if not outfits:

        return {
            "message": (
                "I could not create a complete outfit "
                "from the available products."
            ),

            "request_context": request_context
        }


    # ========================================================
    # 11. FORMAT FINAL RESPONSE
    # ========================================================

    results = []

    for rank, outfit in enumerate(
        outfits,
        start=1
    ):

        results.append({

            "rank": rank,

            "score": outfit.get(
                "outfit_score",
                0
            ),

            "reasons": outfit.get(
                "reasons",
                []
            ),

            "top": outfit.get(
                "top"
            ),

            "bottom": outfit.get(
                "bottom"
            ),

            "shoes": outfit.get(
                "shoes"
            )
        })


    # ========================================================
    # 12. RETURN
    # ========================================================

    return {
        "user_request": request.user_request,

        "request_context": request_context,

        "profile": {
            "gender": profile.gender,
            "skin_tone": profile.skin_tone,
            "body_type": profile.body_type,
            "style_preference": profile.style_preference,
            "favorite_colors": profile.favorite_colors
        },

        "outfits": results
    }