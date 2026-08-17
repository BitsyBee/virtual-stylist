import json
import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


# =========================================================
# CONFIGURATION
# =========================================================

NEVERBE_BASE_URL = "https://neverbe.lk"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# =========================================================
# VERIFIED NEVERBE COLLECTIONS
# =========================================================

# =========================================================
# VERIFIED NEVERBE COLLECTIONS
#
# Each collection is paired with the style label that best
# describes footwear found there. Tagging style by collection
# is far more reliable than trying to infer it from scraped
# product names/descriptions, which Neverbe's page structure
# doesn't always expose cleanly.
# =========================================================

NEVERBE_COLLECTIONS = [
    ("/collections/products?category=casual%20shoes", "Casual"),
    ("/collections/products?category=formal%20shoes", "Formal"),
    ("/collections/products?category=chunky%20shoes", "Streetwear"),
    ("/collections/sneakers", "Casual"),
    ("/collections/running-shoes", "Casual"),
    ("/collections/boots", "Smart Casual"),
    ("/collections/slides-sandals", "Casual"),
]


# =========================================================
# HTTP
# =========================================================

def get_soup(url):

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


# =========================================================
# CATEGORY DETECTION
# =========================================================

def detect_category(name, url=""):

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
        "slide",
        "slides",
        "trainer",
        "trainers",
    ]

    if any(
        word in text
        for word in shoe_words
    ):
        return "Shoes"

    return None

def decode_neverbe_text(value):
    """
    Decode escaped strings embedded in Neverbe HTML.
    """

    if not value:
        return ""

    try:

        # Convert JSON-style escaped content
        return json.loads(
            '"' + value + '"'
        )

    except Exception:

        return (
            value
            .replace('\\"', '"')
            .replace("\\/", "/")
            .replace("\\u0026", "&")
            .replace("\\u0027", "'")
            .replace("\\n", " ")
            .strip()
        )

# =========================================================
# EXTRACT PRODUCT URLS
# =========================================================

def extract_product_urls(html, limit=20):
    """
    Extract Neverbe footwear products from embedded page data.

    Neverbe uses URLs such as:

        /collections/products/p-ETebZVtG

    instead of the normal:

        /products/product-name
    """

    products = []
    seen_urls = set()

    # =========================================================
    # 1. Find Neverbe product URLs
    # =========================================================

    # Do NOT require:
    #     "url":"https://neverbe.lk/...
    #
    # because the HTML may contain escaped/serialized JSON.

    url_pattern = re.compile(
        r'(?:https?:\\?/\\?/neverbe\.lk|https://neverbe\.lk)'
        r'[/\\]+collections[/\\]+products[/\\]+'
        r'([A-Za-z0-9_-]+)',
        re.IGNORECASE
    )

    url_matches = list(
        url_pattern.finditer(html)
    )

    print(
        f"Neverbe product URL candidates: "
        f"{len(url_matches)}"
    )

    # =========================================================
    # 2. Process candidates
    # =========================================================

    for match in url_matches:

        if len(products) >= limit:
            break

        product_id = match.group(1)

        product_url = (
            f"https://neverbe.lk/collections/products/"
            f"{product_id}"
        )

        if product_url in seen_urls:
            continue

        seen_urls.add(product_url)

        # =====================================================
        # 3. Get a nearby section of HTML
        # =====================================================

        start = max(
            0,
            match.start() - 5000
        )

        end = min(
            len(html),
            match.end() + 3000
        )

        section = html[start:end]

        # =====================================================
        # 4. Find product name
        # =====================================================

        name = None

        # Look backwards first because the product name normally
        # appears before the URL.

        before_url = html[
            start:match.start()
        ]

        name_matches = re.findall(
            r'"name"\s*:\s*"([^"]+)"',
            before_url,
            re.IGNORECASE
        )

        if name_matches:
            name = name_matches[-1]

        # =====================================================
        # 5. Find image
        # =====================================================

        image_url = None

        image_matches = re.findall(
            r'"image"\s*:\s*"([^"]+)"',
            section,
            re.IGNORECASE
        )

        if image_matches:
            image_url = image_matches[0]

        # =====================================================
        # 6. Find description
        # =====================================================

        description = None

        description_matches = re.findall(
            r'"description"\s*:\s*"([^"]*)"',
            section,
            re.IGNORECASE
        )

        if description_matches:
            description = description_matches[0]

        # =====================================================
        # 7. Clean escaped values
        # =====================================================

        def clean(value):

            if not value:
                return value

            return (
                value
                .replace("\\/", "/")
                .replace("\\\\/", "/")
                .replace('\\"', '"')
                .replace("\\u0026", "&")
                .replace("\\u0027", "'")
                .replace("\\u003c", "<")
                .replace("\\u003e", ">")
            )

        name = clean(name)
        image_url = clean(image_url)
        description = clean(description)

        # =====================================================
        # 8. Fallback name
        # =====================================================

        if not name:

            name = product_id.replace(
                "-",
                " "
            ).title()

        # =====================================================
        # 9. Exclude accessories
        #    Every collection scanned here is already a
        #    footwear-specific collection (casual shoes,
        #    formal shoes, sneakers, boots, slides/sandals,
        #    etc.), so we no longer require the scraped name or
        #    description to literally contain a shoe keyword
        #    before accepting a product. That check was
        #    rejecting every single candidate: Neverbe's current
        #    page structure doesn't expose a "name" field where
        #    this scraper expected one, so every product fell
        #    back to an ID-based placeholder name (e.g. from
        #    "p-ETebZVtG") with no shoe keywords in it at all,
        #    and otherwise-valid products were being discarded.
        #    We keep a light exclusion filter for obvious
        #    non-footwear accessories, applied only when there
        #    is real text to check against.
        # =====================================================

        text = (
            f"{name} "
            f"{description or ''}"
        ).lower()

        excluded_keywords = [
            "sock",
            "socks",
            "cleaner",
            "polish",
            "brush",
            "insole",
            "lace",
            "laces",
        ]

        if any(
            keyword in text
            for keyword in excluded_keywords
        ):
            continue

        # =====================================================
        # 11. Create normalized product
        # =====================================================

        product = {
            "name": name.strip(),
            "brand": "Neverbe",
            "source": "Neverbe",
            "category": "Shoes",
            "product_url": product_url,
            "image_url": image_url,
            "description": description,
            "price": None,
            "currency": "LKR",
            "color": None,
            "sizes": None,
            "availability": "Unknown",
            "inventory_quantity": None,
        }

        products.append(product)

    print(
        f"Valid Neverbe products extracted: "
        f"{len(products)}"
    )

    return products

def extract_neverbe_product_details(product):
    """
    Retrieve additional information from an individual
    Neverbe product page.
    """

    import re
    import requests
    from bs4 import BeautifulSoup

    url = product["product_url"]

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        html = response.text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

    except Exception as error:

        print(
            f"Could not retrieve Neverbe product "
            f"{url}: {error}"
        )

        return product

    # =========================================================
    # IMAGE
    # =========================================================

    og_image = soup.find(
        "meta",
        property="og:image"
    )

    if og_image:

        image_url = og_image.get("content")

        if image_url:
            product["image_url"] = image_url

    # =========================================================
    # DESCRIPTION
    # =========================================================

    og_description = soup.find(
        "meta",
        property="og:description"
    )

    if og_description:

        description = og_description.get(
            "content"
        )

        if description:
            product["description"] = (
                description.strip()
            )

    # =========================================================
    # TITLE
    # =========================================================

    og_title = soup.find(
        "meta",
        property="og:title"
    )

    if og_title:

        title = og_title.get("content")

        if title:
            product["name"] = title.strip()

    # =========================================================
    # PRICE
    # =========================================================

    price_patterns = [

        # JSON price fields
        r'"price"\s*:\s*"?([\d,]+(?:\.\d+)?)',

        r'"amount"\s*:\s*"?([\d,]+(?:\.\d+)?)',

        r'"priceValue"\s*:\s*"?([\d,]+(?:\.\d+)?)',

    ]

    for pattern in price_patterns:

        match = re.search(
            pattern,
            html,
            re.IGNORECASE
        )

        if match:

            try:

                price = float(
                    match.group(1).replace(
                        ",",
                        ""
                    )
                )

                # Avoid accidentally capturing
                # unrealistic values.
                if price > 0:

                    product["price"] = price

                    break

            except ValueError:
                pass

    # =========================================================
    # CURRENCY
    # =========================================================

    product["currency"] = "LKR"

    currency_match = re.search(
        r'"priceCurrency"\s*:\s*"([^"]+)"',
        html,
        re.IGNORECASE
    )

    if currency_match:

        product["currency"] = (
            currency_match.group(1)
        )

    # =========================================================
    # COLOR
    # =========================================================

    color_patterns = [

        r'"color"\s*:\s*"([^"]+)"',

        r'"colour"\s*:\s*"([^"]+)"',

    ]

    for pattern in color_patterns:

        match = re.search(
            pattern,
            html,
            re.IGNORECASE
        )

        if match:

            color = match.group(1).strip()

            if color:

                product["color"] = color

                break

    # =========================================================
    # AVAILABILITY
    # =========================================================

    availability_match = re.search(
        r'"availability"\s*:\s*"([^"]+)"',
        html,
        re.IGNORECASE
    )

    if availability_match:

        availability = (
            availability_match
            .group(1)
            .lower()
        )

        if "instock" in availability:

            product["availability"] = (
                "In Stock"
            )

        elif "outofstock" in availability:

            product["availability"] = (
                "Out of Stock"
            )

    # =========================================================
    # FALLBACK AVAILABILITY
    # =========================================================

    if product["availability"] == "Unknown":

        lowered_html = html.lower()

        if (
            "out of stock" in lowered_html
            or "out-of-stock" in lowered_html
        ):

            product["availability"] = (
                "Out of Stock"
            )

        else:

            product["availability"] = (
                "In Stock"
            )

    return product


# =========================================================
# PRODUCT NAME FROM URL
# =========================================================

def product_name_from_url(product_url):

    slug = product_url.rstrip("/").split("/")[-1]

    slug = slug.replace("-", " ")

    return slug.title()


# =========================================================
# PRODUCT DETAILS
# =========================================================

def extract_product_details(
    product_url
):

    soup = get_soup(
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
        "availability": "Unknown",
    }

    # =====================================================
    # PRODUCT NAME
    # =====================================================

    title = soup.find(
        "meta",
        property="og:title"
    )

    if title:

        details["name"] = (
            title.get("content")
        )

    elif soup.title:

        details["name"] = (
            soup.title.get_text(
                " ",
                strip=True
            )
        )

    # =====================================================
    # DESCRIPTION
    # =====================================================

    meta_description = soup.find(
        "meta",
        property="og:description"
    )

    if meta_description:

        details["description"] = (
            meta_description.get(
                "content"
            )
        )

    # =====================================================
    # IMAGE
    # =====================================================

    og_image = soup.find(
        "meta",
        property="og:image"
    )

    if og_image:

        image = og_image.get(
            "content"
        )

        if image:

            details["image_url"] = urljoin(
                NEVERBE_BASE_URL,
                image
            )

    # =====================================================
    # PRICE
    # =====================================================

    price_meta = soup.find(
        "meta",
        property="og:price:amount"
    )

    if price_meta:

        try:

            details["price"] = float(
                price_meta.get(
                    "content"
                ).replace(
                    ",",
                    ""
                )
            )

        except Exception:
            pass

    # =====================================================
    # CURRENCY
    # =====================================================

    currency_meta = soup.find(
        "meta",
        property="og:price:currency"
    )

    if currency_meta:

        details["currency"] = (
            currency_meta.get(
                "content"
            )
        )

    # =====================================================
    # SHOPIFY PRODUCT JSON
    # =====================================================

    product_json = soup.find(
        "script",
        type="application/ld+json"
    )

    if product_json:

        try:

            data = json.loads(
                product_json.string
            )

            if isinstance(
                data,
                dict
            ):

                if not details.get(
                    "name"
                ):

                    details["name"] = (
                        data.get("name")
                    )

                if not details.get(
                    "description"
                ):

                    details["description"] = (
                        data.get(
                            "description"
                        )
                    )

                if not details.get(
                    "image_url"
                ):

                    image = data.get(
                        "image"
                    )

                    if isinstance(
                        image,
                        list
                    ) and image:

                        details[
                            "image_url"
                        ] = image[0]

                    elif isinstance(
                        image,
                        str
                    ):

                        details[
                            "image_url"
                        ] = image

                offers = data.get(
                    "offers"
                )

                if isinstance(
                    offers,
                    dict
                ):

                    if not details.get(
                        "price"
                    ):

                        try:

                            details[
                                "price"
                            ] = float(
                                offers.get(
                                    "price"
                                )
                            )

                        except Exception:
                            pass

                    availability = (
                        offers.get(
                            "availability",
                            ""
                        )
                    ).lower()

                    if "instock" in availability:

                        details[
                            "availability"
                        ] = "In Stock"

                    elif "outofstock" in availability:

                        details[
                            "availability"
                        ] = "Out of Stock"

        except Exception as error:

            print(
                f"JSON-LD parsing failed: {error}"
            )

    # =====================================================
    # AVAILABILITY FROM PAGE TEXT
    # =====================================================

    page_text = soup.get_text(
        " ",
        strip=True
    ).lower()

    if (
        "out of stock" in page_text
        or "sold out" in page_text
    ):

        details[
            "availability"
        ] = "Out of Stock"

    elif (
        "add to cart" in page_text
        or "buy now" in page_text
    ):

        details[
            "availability"
        ] = "In Stock"

    # =====================================================
    # COLOR DETECTION
    # =====================================================

    color_words = [
        "black",
        "white",
        "grey",
        "gray",
        "blue",
        "navy",
        "brown",
        "beige",
        "tan",
        "green",
        "olive",
        "red",
        "burgundy",
        "pink",
        "yellow",
        "orange",
    ]

    detected_colors = []

    for color in color_words:

        if re.search(
            rf"\b{re.escape(color)}\b",
            page_text,
            re.IGNORECASE
        ):

            detected_colors.append(
                color.title()
            )

    if detected_colors:

        details["color"] = ", ".join(
            sorted(
                set(
                    detected_colors
                )
            )
        )

    # =====================================================
    # SIZE DETECTION
    # =====================================================

    sizes = []

    for size in [
        "XS",
        "S",
        "M",
        "L",
        "XL",
        "XXL",
        "XXXL",
    ]:

        if re.search(
            rf"\b{size}\b",
            page_text,
            re.IGNORECASE
        ):

            sizes.append(size)

    if sizes:

        details["sizes"] = ", ".join(
            sizes
        )

    return details


# =========================================================
# GET PRODUCTS FROM COLLECTION
# =========================================================

def get_neverbe_collection_products(
    collection_path,
    limit=20
):

    url = urljoin(
        NEVERBE_BASE_URL,
        collection_path
    )

    print(
        f"\nScanning Neverbe collection: {url}"
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    print(
        f"HTTP status: {response.status_code}"
    )

    print(
        f"HTML length: {len(response.text)}"
    )

    products = extract_product_urls(
        response.text,
        limit=limit
    )

    print(
        f"Product URLs found: {len(products)}"
    )

    for product in products:

        print(
            f"  ✓ "
            f"{product['name']} "
            f"[Shoes] "
            f"(Neverbe)"
        )

    print(
        f"Collection result: {len(products)} products"
    )

    return products


# =========================================================
# LIVE NEVERBE RETRIEVAL
# =========================================================

def get_live_neverbe_products(
    per_category=8
):
    """
    Retrieve live shoe products from Neverbe.

    Neverbe uses a custom product structure, so the
    collection page is scanned directly and embedded
    product objects are extracted.
    """

    print("\n======================================")
    print("LIVE NEVERBE PRODUCT RETRIEVAL")
    print("======================================")

    results = {
        "Shoes": []
    }

    for collection_url, style_label in NEVERBE_COLLECTIONS:

        if len(results["Shoes"]) >= per_category:
            break

        print(
            f"\nScanning Neverbe collection: "
            f"{collection_url} "
            f"(style: {style_label})"
        )

        try:

            full_url = urljoin(
                NEVERBE_BASE_URL,
                collection_url
            )

            response = requests.get(
                full_url,
                headers=HEADERS,
                timeout=20
            )

            response.raise_for_status()

            print(
                f"HTTP status: {response.status_code}"
            )

            print(
                f"HTML length: {len(response.text)}"
            )

            products = extract_product_urls(
                response.text,
                limit=per_category * 3
            )

            # -------------------------------------------------
            # Add products
            # -------------------------------------------------

            for product in products:

                if len(results["Shoes"]) >= per_category:
                    break

                product_url = product.get(
                    "product_url"
                )

                if not product_url:
                    continue

                # Prevent duplicates between collections
                if any(
                    existing.get("product_url")
                    == product_url
                    for existing in results["Shoes"]
                ):
                    continue

                # Tag style from the collection it was found
                # in — more reliable than scraped text.
                product["style"] = style_label

                # Fetch the real product page so we get an
                # accurate image, name, description, and price.
                # The embedded JSON scraped from the collection
                # page doesn't reliably expose these fields on
                # Neverbe's current site.
                product = extract_neverbe_product_details(
                    product
                )

                results["Shoes"].append(product)

                print(
                    f"  ✓ "
                    f"{product['name']} "
                    f"[Shoes/{style_label}] "
                    f"(Neverbe)"
                )

        except Exception as error:

            print(
                f"Could not retrieve "
                f"{collection_url}: {error}"
            )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print("\n======================================")
    print("NEVERBE RETRIEVAL SUMMARY")
    print("======================================")

    print(
        "SHOES:",
        len(results["Shoes"])
    )

    print("======================================")

    return results

def is_shoe_product(product):
    """
    Determine whether a Neverbe product is footwear.
    """

    text = " ".join([
        str(product.get("name", "")),
        str(product.get("description", ""))
    ]).lower()

    shoe_keywords = [
        "shoe",
        "shoes",
        "sneaker",
        "sneakers",
        "trainer",
        "trainers",
        "loafer",
        "loafers",
        "boot",
        "boots",
        "sandal",
        "sandals",
        "slide",
        "slides",
        "slipper",
        "slippers",
        "running shoe",
        "casual shoe",
        "formal shoe",
        "chunky shoe",
        "jordan",
        "nike",
        "adidas",
        "puma",
        "new balance",
        "reebok",
        "vans",
        "converse"
    ]

    return any(
        keyword in text
        for keyword in shoe_keywords
    )