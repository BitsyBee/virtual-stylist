"""
Fashion Theory Knowledge Base - V2

This knowledge base is used to generate a controlled synthetic
fashion dataset.

The dataset is based on:
- Basic color theory
- Skin-tone color compatibility
- Occasion/formality
- Style compatibility
- Body-type considerations
- Fit
- Material
- Seasonal/temperature suitability
- Pattern coordination
"""

# ============================================================
# COLORS
# ============================================================

COLORS = {
    "Black": {
        "temperature": "Neutral",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "White", "Grey", "Beige", "Navy",
            "Burgundy", "Olive", "Red"
        ],
    },

    "White": {
        "temperature": "Neutral",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "Black", "Navy", "Grey", "Beige",
            "Brown", "Olive", "Burgundy",
            "Light Blue", "Pink"
        ],
    },

    "Navy": {
        "temperature": "Cool",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "White", "Beige", "Grey", "Brown",
            "Khaki", "Light Blue", "Burgundy",
            "Olive"
        ],
    },

    "Light Blue": {
        "temperature": "Cool",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "White", "Navy", "Grey", "Beige",
            "Brown", "Khaki"
        ],
    },

    "Grey": {
        "temperature": "Neutral",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "Black", "White", "Navy", "Burgundy",
            "Light Blue", "Pink", "Olive"
        ],
    },

    "Beige": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "Navy", "White", "Brown", "Black",
            "Olive", "Burgundy", "Light Blue"
        ],
    },

    "Cream": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "Navy", "Brown", "Olive", "Burgundy",
            "Black", "Beige"
        ],
    },

    "Brown": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "White", "Cream", "Beige", "Navy",
            "Olive", "Light Blue", "Burgundy"
        ],
    },

    "Olive": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "White", "Cream", "Beige", "Black",
            "Brown", "Navy", "Burgundy", "Khaki"
        ],
    },

    "Burgundy": {
        "temperature": "Warm",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "White", "Cream", "Beige", "Grey",
            "Black", "Navy", "Brown", "Khaki"
        ],
    },

    "Red": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "Black", "White", "Grey", "Navy", "Beige"
        ],
    },

    "Pink": {
        "temperature": "Cool",
        "skin_tones": ["Fair", "Medium"],
        "good_with": [
            "White", "Grey", "Navy", "Beige", "Brown"
        ],
    },

    "Mustard": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "Navy", "Black", "White", "Brown", "Olive"
        ],
    },

    "Forest Green": {
        "temperature": "Cool",
        "skin_tones": ["Fair", "Medium", "Deep"],
        "good_with": [
            "White", "Cream", "Beige", "Brown",
            "Black", "Navy"
        ],
    },

    "Lavender": {
        "temperature": "Cool",
        "skin_tones": ["Fair", "Medium"],
        "good_with": [
            "White", "Grey", "Navy", "Beige"
        ],
    },

    "Khaki": {
        "temperature": "Warm",
        "skin_tones": ["Medium", "Deep"],
        "good_with": [
            "White", "Navy", "Black", "Brown",
            "Burgundy", "Olive"
        ],
    },
}


# ============================================================
# OCCASIONS
# ============================================================

OCCASIONS = {
    "Interview": {
        "formality": 5,
        "styles": ["Formal", "Business Casual"],
    },

    "Business Meeting": {
        "formality": 5,
        "styles": ["Formal", "Business Casual"],
    },

    "Office": {
        "formality": 4,
        "styles": ["Business Casual", "Smart Casual"],
    },

    "Wedding": {
        "formality": 5,
        "styles": ["Formal", "Preppy"],
    },

    "Presentation": {
        "formality": 4,
        "styles": ["Formal", "Business Casual", "Smart Casual"],
    },

    "Date": {
        "formality": 3,
        "styles": ["Smart Casual", "Casual"],
    },

    "Party": {
        "formality": 3,
        "styles": ["Smart Casual", "Casual", "Streetwear"],
    },

    "University": {
        "formality": 2,
        "styles": ["Casual", "Smart Casual", "Streetwear"],
    },

    "Casual Outing": {
        "formality": 2,
        "styles": ["Casual", "Smart Casual"],
    },

    "Travel": {
        "formality": 2,
        "styles": ["Casual", "Smart Casual"],
    },

    "Beach": {
        "formality": 1,
        "styles": ["Casual"],
    },
}


# ============================================================
# BODY TYPES
# ============================================================

BODY_TYPES = [
    "Slim",
    "Average",
    "Athletic",
    "Broad",
    "Plus Size",
]


# ============================================================
# CLOTHING DEFINITIONS
# ============================================================

CLOTHING = {

    # --------------------------------------------------------
    # TOPS
    # --------------------------------------------------------

    "T-Shirt": {
        "category": "Top",
        "styles": ["Casual", "Streetwear", "Minimalist"],
        "formality": 1,
        "fits": ["Regular Fit", "Relaxed Fit", "Oversized"],
        "materials": ["Cotton"],
        "seasons": ["Spring/Summer", "All Season"],
        "temperatures": ["Hot", "Warm"],
        "patterns": ["Solid", "Graphic", "Striped"],
    },

    "Polo Shirt": {
        "category": "Top",
        "styles": ["Smart Casual", "Casual", "Preppy"],
        "formality": 3,
        "fits": ["Slim Fit", "Regular Fit"],
        "materials": ["Cotton", "Pique"],
        "seasons": ["Spring/Summer", "All Season"],
        "temperatures": ["Hot", "Warm", "Any"],
        "patterns": ["Solid", "Striped"],
    },

    "Oxford Shirt": {
        "category": "Top",
        "styles": ["Business Casual", "Smart Casual", "Preppy"],
        "formality": 4,
        "fits": ["Slim Fit", "Regular Fit"],
        "materials": ["Cotton"],
        "seasons": ["All Season"],
        "temperatures": ["Any", "Warm"],
        "patterns": ["Solid", "Striped", "Check"],
    },

    "Dress Shirt": {
        "category": "Top",
        "styles": ["Formal", "Business Casual"],
        "formality": 5,
        "fits": ["Slim Fit", "Regular Fit"],
        "materials": ["Cotton"],
        "seasons": ["All Season"],
        "temperatures": ["Any", "Warm"],
        "patterns": ["Solid", "Striped"],
    },

    "Linen Shirt": {
        "category": "Top",
        "styles": ["Casual", "Smart Casual"],
        "formality": 3,
        "fits": ["Regular Fit", "Relaxed Fit"],
        "materials": ["Linen"],
        "seasons": ["Spring/Summer"],
        "temperatures": ["Hot", "Warm"],
        "patterns": ["Solid", "Striped"],
    },

    "Henley": {
        "category": "Top",
        "styles": ["Casual", "Smart Casual"],
        "formality": 2,
        "fits": ["Slim Fit", "Regular Fit"],
        "materials": ["Cotton"],
        "seasons": ["All Season"],
        "temperatures": ["Warm", "Mild"],
        "patterns": ["Solid"],
    },

    "Hoodie": {
        "category": "Top",
        "styles": ["Casual", "Streetwear"],
        "formality": 1,
        "fits": ["Relaxed Fit", "Oversized"],
        "materials": ["Cotton", "Fleece"],
        "seasons": ["Autumn/Winter", "All Season"],
        "temperatures": ["Cool", "Mild"],
        "patterns": ["Solid", "Graphic"],
    },

    "Knit Sweater": {
        "category": "Top",
        "styles": ["Smart Casual", "Preppy", "Minimalist"],
        "formality": 3,
        "fits": ["Regular Fit", "Relaxed Fit"],
        "materials": ["Wool", "Cotton"],
        "seasons": ["Autumn/Winter"],
        "temperatures": ["Cool", "Mild"],
        "patterns": ["Solid"],
    },


    # --------------------------------------------------------
    # BOTTOMS
    # --------------------------------------------------------

    "Jeans": {
        "category": "Bottom",
        "styles": ["Casual", "Smart Casual", "Streetwear"],
        "formality": 2,
        "fits": ["Slim Fit", "Regular Fit", "Straight Fit"],
        "materials": ["Denim"],
        "seasons": ["All Season"],
        "temperatures": ["Any"],
        "patterns": ["Solid"],
    },

    "Chinos": {
        "category": "Bottom",
        "styles": ["Business Casual", "Smart Casual", "Preppy"],
        "formality": 3,
        "fits": ["Slim Fit", "Regular Fit", "Straight Fit"],
        "materials": ["Cotton"],
        "seasons": ["All Season"],
        "temperatures": ["Any", "Warm"],
        "patterns": ["Solid"],
    },

    "Dress Trousers": {
        "category": "Bottom",
        "styles": ["Formal", "Business Casual"],
        "formality": 5,
        "fits": ["Slim Fit", "Regular Fit", "Straight Fit"],
        "materials": ["Wool", "Polyester"],
        "seasons": ["All Season"],
        "temperatures": ["Any", "Mild"],
        "patterns": ["Solid", "Pinstripe"],
    },

    "Cargo Pants": {
        "category": "Bottom",
        "styles": ["Casual", "Streetwear"],
        "formality": 2,
        "fits": ["Regular Fit", "Relaxed Fit"],
        "materials": ["Cotton"],
        "seasons": ["All Season"],
        "temperatures": ["Any"],
        "patterns": ["Solid"],
    },

    "Shorts": {
        "category": "Bottom",
        "styles": ["Casual"],
        "formality": 1,
        "fits": ["Regular Fit", "Relaxed Fit"],
        "materials": ["Cotton", "Linen"],
        "seasons": ["Spring/Summer"],
        "temperatures": ["Hot"],
        "patterns": ["Solid", "Striped"],
    },


    # --------------------------------------------------------
    # SHOES
    # --------------------------------------------------------

    "Sneakers": {
        "category": "Shoes",
        "styles": ["Casual", "Streetwear", "Minimalist"],
        "formality": 2,
        "fits": ["Regular Fit"],
        "materials": ["Leather", "Canvas"],
        "seasons": ["All Season"],
        "temperatures": ["Any"],
        "patterns": ["Solid"],
    },

    "Loafers": {
        "category": "Shoes",
        "styles": ["Smart Casual", "Business Casual", "Preppy"],
        "formality": 4,
        "fits": ["Regular Fit"],
        "materials": ["Leather", "Suede"],
        "seasons": ["All Season"],
        "temperatures": ["Any"],
        "patterns": ["Solid"],
    },

    "Oxford Shoes": {
        "category": "Shoes",
        "styles": ["Formal", "Business Casual"],
        "formality": 5,
        "fits": ["Regular Fit"],
        "materials": ["Leather"],
        "seasons": ["All Season"],
        "temperatures": ["Any"],
        "patterns": ["Solid"],
    },

    "Boots": {
        "category": "Shoes",
        "styles": ["Casual", "Smart Casual", "Streetwear"],
        "formality": 3,
        "fits": ["Regular Fit"],
        "materials": ["Leather", "Suede"],
        "seasons": ["Autumn/Winter", "All Season"],
        "temperatures": ["Cool", "Mild", "Any"],
        "patterns": ["Solid"],
    },

    "Sandals": {
        "category": "Shoes",
        "styles": ["Casual"],
        "formality": 1,
        "fits": ["Regular Fit"],
        "materials": ["Leather", "Rubber"],
        "seasons": ["Spring/Summer"],
        "temperatures": ["Hot"],
        "patterns": ["Solid"],
    },


    # --------------------------------------------------------
    # OUTERWEAR
    # --------------------------------------------------------

    "Blazer": {
        "category": "Outerwear",
        "styles": ["Formal", "Business Casual", "Smart Casual"],
        "formality": 5,
        "fits": ["Slim Fit", "Regular Fit"],
        "materials": ["Wool", "Cotton"],
        "seasons": ["All Season"],
        "temperatures": ["Cool", "Mild", "Any"],
        "patterns": ["Solid", "Check"],
    },

    "Denim Jacket": {
        "category": "Outerwear",
        "styles": ["Casual", "Streetwear"],
        "formality": 2,
        "fits": ["Regular Fit", "Relaxed Fit"],
        "materials": ["Denim"],
        "seasons": ["Autumn/Winter", "All Season"],
        "temperatures": ["Cool", "Mild"],
        "patterns": ["Solid"],
    },

    "Bomber Jacket": {
        "category": "Outerwear",
        "styles": ["Casual", "Streetwear"],
        "formality": 2,
        "fits": ["Regular Fit", "Oversized"],
        "materials": ["Nylon", "Cotton"],
        "seasons": ["Autumn/Winter", "All Season"],
        "temperatures": ["Cool", "Mild"],
        "patterns": ["Solid"],
    },
}


# ============================================================
# BODY TYPE → FIT THEORY
# ============================================================

BODY_TYPE_FITS = {
    "Slim": [
        "Slim Fit",
        "Regular Fit",
        "Relaxed Fit",
    ],

    "Average": [
        "Regular Fit",
        "Slim Fit",
        "Straight Fit",
    ],

    "Athletic": [
        "Regular Fit",
        "Slim Fit",
    ],

    "Broad": [
        "Regular Fit",
        "Relaxed Fit",
        "Straight Fit",
    ],

    "Plus Size": [
        "Regular Fit",
        "Relaxed Fit",
        "Straight Fit",
    ],
}
# ============================================================
# ITEM-SPECIFIC OCCASION RULES
# ============================================================

ITEM_OCCASIONS = {

    "T-Shirt": [
        "University",
        "Casual Outing",
        "Travel",
        "Party",
        "Date",
    ],

    "Polo Shirt": [
        "Office",
        "University",
        "Casual Outing",
        "Date",
        "Travel",
        "Party",
    ],

    "Oxford Shirt": [
        "Interview",
        "Business Meeting",
        "Office",
        "Presentation",
        "Date",
        "Wedding",
    ],

    "Dress Shirt": [
        "Interview",
        "Business Meeting",
        "Office",
        "Presentation",
        "Wedding",
    ],

    "Linen Shirt": [
        "Beach",
        "Travel",
        "Casual Outing",
        "Date",
        "Party",
    ],

    "Henley": [
        "Casual Outing",
        "University",
        "Travel",
        "Date",
    ],

    "Hoodie": [
        "University",
        "Casual Outing",
        "Travel",
        "Party",
    ],

    "Knit Sweater": [
        "Office",
        "University",
        "Casual Outing",
        "Date",
        "Travel",
    ],

    "Jeans": [
        "University",
        "Casual Outing",
        "Travel",
        "Date",
        "Party",
    ],

    "Chinos": [
        "Office",
        "Business Meeting",
        "Presentation",
        "Date",
        "University",
        "Casual Outing",
    ],

    "Dress Trousers": [
        "Interview",
        "Business Meeting",
        "Office",
        "Presentation",
        "Wedding",
    ],

    "Cargo Pants": [
        "University",
        "Casual Outing",
        "Travel",
        "Party",
    ],

    "Shorts": [
        "Beach",
        "Travel",
        "Casual Outing",
    ],

    "Sneakers": [
        "University",
        "Casual Outing",
        "Travel",
        "Date",
        "Party",
    ],

    "Loafers": [
        "Office",
        "Business Meeting",
        "Date",
        "Wedding",
        "Presentation",
        "Party",
    ],

    "Oxford Shoes": [
        "Interview",
        "Business Meeting",
        "Office",
        "Presentation",
        "Wedding",
    ],

    "Boots": [
        "Travel",
        "Casual Outing",
        "University",
        "Date",
        "Party",
    ],

    "Sandals": [
        "Beach",
        "Travel",
        "Casual Outing",
    ],

    "Blazer": [
        "Interview",
        "Business Meeting",
        "Office",
        "Presentation",
        "Wedding",
        "Date",
    ],

    "Denim Jacket": [
        "University",
        "Casual Outing",
        "Travel",
        "Party",
        "Date",
    ],

    "Bomber Jacket": [
        "University",
        "Casual Outing",
        "Travel",
        "Party",
        "Date",
    ],
}


# ============================================================
# BODY TYPE COMPATIBILITY
# ============================================================

BODY_TYPE_COMPATIBILITY = {

    "Slim": [
        "Slim Fit",
        "Regular Fit",
        "Relaxed Fit",
        "Oversized",
        "Straight Fit",
    ],

    "Average": [
        "Slim Fit",
        "Regular Fit",
        "Relaxed Fit",
        "Oversized",
        "Straight Fit",
    ],

    "Athletic": [
        "Slim Fit",
        "Regular Fit",
        "Relaxed Fit",
    ],

    "Broad": [
        "Regular Fit",
        "Relaxed Fit",
        "Oversized",
        "Straight Fit",
    ],

    "Plus Size": [
        "Regular Fit",
        "Relaxed Fit",
        "Oversized",
        "Straight Fit",
    ],
}