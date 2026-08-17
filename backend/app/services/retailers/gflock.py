import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.services.retailers.base import RetailProduct


BASE_URL = "https://gflock.lk"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


COLLECTIONS = {
    "top": [
        "/collections/mens-shirts",
        "/collections/mens-t-shirts",
    ],

    "bottom": [
        "/collections/mens-trousers",
        "/collections/mens-jeans",
    ],
}


def fetch_page(url):

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def get_product_links(category):

    links = []

    for collection in COLLECTIONS.get(category, []):

        url = urljoin(
            BASE_URL,
            collection
        )

        soup = fetch_page(url)

        for link in soup.select(
            'a[href*="/products/"]'
        ):

            href = link.get("href")

            if not href:
                continue

            product_url = urljoin(
                BASE_URL,
                href
            )

            if product_url not in links:
                links.append(product_url)

    return links


def extract_product(product_url, category):

    soup = fetch_page(product_url)

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "GFLOCK Product"
    )

    title = title.replace(
        "– GFLOCK.LK",
        ""
    ).strip()

    image_url = None

    og_image = soup.find(
        "meta",
        property="og:image"
    )

    if og_image:
        image_url = og_image.get("content")

    price = None

    price_meta = soup.find(
        "meta",
        property="og:price:amount"
    )

    if price_meta:

        try:
            price = float(
                price_meta.get("content")
            )
        except (TypeError, ValueError):
            pass

    currency = "LKR"

    currency_meta = soup.find(
        "meta",
        property="og:price:currency"
    )

    if currency_meta:
        currency = currency_meta.get(
            "content"
        )

    description = None

    description_meta = soup.find(
        "meta",
        property="og:description"
    )

    if description_meta:
        description = description_meta.get(
            "content"
        )

    return RetailProduct(
        name=title,
        brand="GFLOCK",
        source="GFLOCK",
        product_url=product_url,
        image_url=image_url,
        price=price,
        currency=currency,
        category=category,
        gender="unisex",
        description=description,
        availability="available"
    )


def search_gflock(
    category,
    limit=15
):

    products = []

    links = get_product_links(category)

    for url in links[:limit]:

        try:

            product = extract_product(
                url,
                category
            )

            products.append(product)

            print(
                f"Retrieved: {product.name}"
            )

        except Exception as e:

            print(
                f"GFLOCK error: {url} -> {e}"
            )

    return products