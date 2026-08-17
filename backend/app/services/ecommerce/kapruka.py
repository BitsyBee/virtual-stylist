import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .base import EcommerceProvider


KAPRUKA_BASE_URL = "https://www.kapruka.com"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


KAPRUKA_CATEGORIES = {

    "Top":
        "/lk/online/clothing/price/mens_clothing/lanka/shirts",

    "Bottom":
        "/lk/online/clothing/price/mens_clothing",

    "Shoes":
        "/lk/online/shoes"
}


class KaprukaProvider(EcommerceProvider):

    name = "Kapruka"

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
        name
    ):

        text = name.lower()

        shoe_words = [
            "shoe",
            "sneaker",
            "loafer",
            "boot",
            "sandal",
            "slipper"
        ]

        bottom_words = [
            "trouser",
            "trousers",
            "pant",
            "pants",
            "jean",
            "short",
            "chino",
            "cargo",
            "jogger"
        ]

        top_words = [
            "shirt",
            "t-shirt",
            "tshirt",
            "tee",
            "polo",
            "hoodie",
            "sweater"
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
            for word in top_words
        ):
            return "Top"

        return None

    def extract_price(
        self,
        text
    ):

        if not text:
            return None

        matches = re.findall(
            r"(?:Rs\.?|LKR)\s*"
            r"([\d,]+(?:\.\d+)?)",
            text,
            re.IGNORECASE
        )

        if not matches:
            return None

        try:

            return float(
                matches[-1].replace(
                    ",",
                    ""
                )
            )

        except ValueError:
            return None

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

            path = KAPRUKA_CATEGORIES.get(
                category
            )

            if not path:
                continue

            url = urljoin(
                KAPRUKA_BASE_URL,
                path
            )

            try:

                soup = self.get_soup(
                    url
                )

            except Exception as error:

                print(
                    f"Kapruka request error: "
                    f"{error}"
                )

                continue

            seen = set()

            links = soup.select(
                'a[href*="/p/"]'
            )

            for link in links:

                href = link.get(
                    "href"
                )

                if not href:
                    continue

                product_url = urljoin(
                    KAPRUKA_BASE_URL,
                    href
                )

                if product_url in seen:
                    continue

                seen.add(
                    product_url
                )

                name = link.get_text(
                    " ",
                    strip=True
                )

                detected_category = (
                    self.detect_category(
                        name
                    )
                )

                if (
                    detected_category
                    != category
                ):
                    continue

                parent = link.parent

                card_text = (
                    parent.get_text(
                        " ",
                        strip=True
                    )
                    if parent
                    else name
                )

                image = link.find(
                    "img"
                )

                image_url = None

                if image:

                    image_url = (
                        image.get("src")
                        or image.get(
                            "data-src"
                        )
                    )

                    if image_url:

                        image_url = urljoin(
                            KAPRUKA_BASE_URL,
                            image_url
                        )

                results.append({

                    "name": name,

                    "brand":
                        "Kapruka",

                    "source":
                        "Kapruka",

                    "category":
                        category,

                    "product_url":
                        product_url,

                    "image_url":
                        image_url,

                    "price":
                        self.extract_price(
                            card_text
                        ),

                    "currency":
                        "LKR",

                    "description":
                        card_text,

                    "availability":
                        "Unknown"
                })

                if len(
                    [
                        x
                        for x in results
                        if x["category"]
                        == category
                    ]
                ) >= limit:

                    break

        return results