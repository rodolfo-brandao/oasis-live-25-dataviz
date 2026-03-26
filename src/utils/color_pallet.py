"""
Everything related to colors.
"""


from typing import List, Dict


OASIS_ALBUM_COLORS: Dict[str, str] = {
    "Definitely Maybe":                     "#E8A838",
    "Morning Glory":                        "#3A86FF",
    "Be Here Now":                          "#FF006E",
    "The Masterplan":                       "#8338EC",
    "Standing on the Shoulder of Giants":   "#06D6A0",
    "Heathen Chemistry":                    "#FB5607",
    "Don't Believe the Truth":              "#118AB2",
    "Dig Out Your Soul":                    "#EF233C",
    "Other / Unknown":                      "#ADB5BD",
}


OASIS_COLOR_PALLET: Dict[str, str] = {
    "primary":      "#222f5b",
    "secondary":    "#395e7f",
    "accent":       "#271d12",
    "neutral":      "#3d3d3d",
    "light":        "#bcb5ae",
    "background":   "#f7f6f3",
    "grid":         "#d9d4ce",
}


OASIS_COLOR_SEQUENCE: List[str] = [
    OASIS_COLOR_PALLET["primary"],
    OASIS_COLOR_PALLET["secondary"],
    OASIS_COLOR_PALLET["accent"],
    OASIS_COLOR_PALLET["neutral"],
    OASIS_COLOR_PALLET["light"],
]


CONTINENT_COLORS: Dict[str, str] = {
    "Europe":           OASIS_COLOR_PALLET["primary"],
    "North America":    OASIS_COLOR_PALLET["secondary"],
    "South America":    OASIS_COLOR_PALLET["accent"],
    "Asia":             OASIS_COLOR_PALLET["neutral"],
    "Oceania":          OASIS_COLOR_PALLET["light"],
}
