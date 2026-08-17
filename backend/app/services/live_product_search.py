from app.services.retailer_manager import search_retailers


def retrieve_outfit_candidates():

    candidates = {

        "Top": search_retailers(
            "top",
            limit_per_retailer=10
        ),

        "Bottom": search_retailers(
            "bottom",
            limit_per_retailer=10
        ),

        "Shoes": []

    }

    return candidates