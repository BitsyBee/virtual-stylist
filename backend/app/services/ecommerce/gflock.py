import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import EcommerceProvider


GFLOCK_BASE_URL = "https://gflock.lk"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


GFLOCK_COLLECTIONS = {

    "Top": [
        "/collections/mens-shirts",
        "/collections/mens-t-shirts",
    ],

    "Bottom": [
        "/collections/mens-trousers",
        "/collections/mens-jeans",
    ],

    "Shoes": []
}


class GflockProvider(EcommerceProvider):

    name = "GFLOCK"

    def get_soup(self, url):

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

    def detect_category(
        self,
        name,
        url=""
    ):

        text = f"{name} {url}".lower()

        shoe_words = [
            "shoe",
            "shoes",
            "sneaker",
            "sneakers",
            "loafer",
            "loafers",
            "boot",
            "boots",
            "sandal",
            "sandals",
            "slipper",
            "slippers",
            "trainer",
            "trainers"
        ]

        bottom_words = [
            "pant",
            "pants",
            "trouser",
            "trousers",
            "jean",
            "jeans",
            "shorts",
            "chino",
            "chinos",
            "cargo",
            "jogger",
            "joggers"
        ]

        top_words = [
            "shirt",
            "shirts",
            "t-shirt",
            "tshirt",
            "tee",
            "tees",
            "polo",
            "top",
            "tops",
            "sweater",
            "hoodie",
            "sweatshirt"
        ]

        outerwear_words = [
            "blazer",
            "jacket",
            "coat",
            "cardigan"
        ]

        if any(
            word in text
            for word in shoe_words
        ):
            return "Shoes"

        if any(
            word in text
            for word in bottom_words
        ):
            return "Bottom"

        if any(
            word in text
            for word in outerwear_words
        ):
            return "Outerwear"

        if any(
            word in text
            for word in top_words
        ):
            return "Top"

        return None

    def extract_product_details(
        self,
        product_url
    ):

        soup = self.get_soup(
            product_url
        )

        details = {
            "description": None,
            "price": None,
            "currency": "LKR",
            "image_url": None,
            "sizes": None,
            "color": None,
            "inventory_quantity": None,
            "availability": "Unknown"
        }

        meta = soup.find(
            "meta",
            property="og:description"
        )

        if meta:
            details["description"] = (
                meta.get("content")
            )

        image = soup.find(
            "meta",
            property="og:image"
        )

        if image:

            details["image_url"] = urljoin(
                GFLOCK_BASE_URL,
                image.get("content")
            )

        price = soup.find(
            "meta",
            property="og:price:amount"
        )

        if price:

            try:
                details["price"] = float(
                    price.get("content")
                    .replace(",", "")
                )
            except (TypeError, ValueError):
                pass

        currency = soup.find(
            "meta",
            property="og:price:currency"
        )

        if currency:
            details["currency"] = (
                currency.get("content")
            )

        variant_script = soup.find(
            "script",
            attrs={"data-all-variants": True}
        )

        if variant_script:

            try:

                variants = json.loads(
                    variant_script.string
                )

                sizes = []
                colors = []
                quantities = []

                for variant in variants:

                    if variant.get("option1"):
                        sizes.append(
                            str(variant["option1"])
                        )

                    if variant.get("option2"):
                        colors.append(
                            str(variant["option2"])
                        )

                    quantity = variant.get(
                        "inventory_quantity"
                    )

                    if quantity is not None:
                        quantities.append(
                            quantity
                        )

                if sizes:
                    details["sizes"] = ", ".join(
                        sorted(set(sizes))
                    )

                if colors:
                    details["color"] = ", ".join(
                        sorted(set(colors))
                    )

                if quantities:

                    details[
                        "inventory_quantity"
                    ] = sum(quantities)

                    details[
                        "availability"
                    ] = (
                        "In Stock"
                        if sum(quantities) > 0
                        else "Out of Stock"
                    )

            except Exception as error:

                print(
                    f"GFLOCK variant error: {error}"
                )

        return details

    def get_collection_products(
        self,
        collection_path,
        limit=20
    ):

        url = urljoin(
            GFLOCK_BASE_URL,
            collection_path
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        products = []
        seen = set()

        links = soup.select(
            'a[href*="/products/"]'
        )

        for link in links:

            href = link.get("href")

            if not href:
                continue

            product_url = urljoin(
                GFLOCK_BASE_URL,
                href
            ).split("?")[0]

            if product_url in seen:
                continue

            seen.add(product_url)

            name = link.get_text(
                " ",
                strip=True
            )

            if not name:

                slug = (
                    product_url
                    .split("/products/")[-1]
                )

                name = (
                    slug
                    .replace("-", " ")
                    .title()
                )

            category = self.detect_category(
                name,
                product_url
            )

            if not category:
                continue

            products.append({

                "name": name,
                "brand": "GFLOCK",
                "source": "GFLOCK",
                "category": category,
                "product_url": product_url
            })

            if len(products) >= limit:
                break

        return products

    def get_products(
        self,
        categories=None,
        limit=20
    ):

        if categories is None:

            categories = [
                "Top",
                "Bottom"
            ]

        results = []

        for category in categories:

            for collection in (
                GFLOCK_COLLECTIONS.get(
                    category,
                    []
                )
            ):

                try:

                    products = (
                        self.get_collection_products(
                            collection,
                            limit=limit
                        )
                    )

                    for product in products:

                        if (
                            product["category"]
                            != category
                        ):
                            continue

                        try:

                            details = (
                                self.extract_product_details(
                                    product[
                                        "product_url"
                                    ]
                                )
                            )

                            product.update(
                                details
                            )

                            results.append(
                                product
                            )

                        except Exception as error:

                            print(
                                f"GFLOCK detail error: "
                                f"{error}"
                            )

                except Exception as error:

                    print(
                        f"GFLOCK collection error: "
                        f"{error}"
                    )

        return results