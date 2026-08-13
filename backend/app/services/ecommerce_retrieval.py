import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


GFLOCK_BASE_URL = "https://gflock.lk"


# ---------------------------------------------------------
# GFLOCK COLLECTIONS
# ---------------------------------------------------------

GFLOCK_COLLECTIONS = {
    "men_shirts": "/collections/mens-shirts",
    "men_tshirts": "/collections/mens-t-shirts",
    "men_pants": "/collections/mens-trousers",
    "men_jeans": "/collections/mens-jeans",
}


# ---------------------------------------------------------
# GET PRODUCTS FROM GFLOCK COLLECTION
# ---------------------------------------------------------

def get_gflock_products(collection: str, limit: int = 20):

    if collection not in GFLOCK_COLLECTIONS:
        raise ValueError(
            f"Unknown GFLOCK collection: {collection}"
        )

    url = urljoin(
        GFLOCK_BASE_URL,
        GFLOCK_COLLECTIONS[collection]
    )

    response = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        },
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    products = []

    # Shopify product cards
    product_links = soup.select(
        'a[href*="/products/"]'
    )

    seen_urls = set()

    for link in product_links:

        product_url = urljoin(
            GFLOCK_BASE_URL,
            link.get("href")
        )

        if product_url in seen_urls:
            continue

        seen_urls.add(product_url)

        product_name = link.get_text(
            " ",
            strip=True
        )

        if not product_name:
            continue

        products.append({
            "name": product_name,
            "product_url": product_url,
            "source": "GFLOCK"
        })

        if len(products) >= limit:
            break

    return products