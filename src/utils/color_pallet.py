"""
Everything related to colors.
"""


from typing import List, Dict


# OASIS_ALBUM_COLORS: Dict[str, str] = {
#     "Definitely Maybe":                     "#222f5b",
#     "Morning Glory":                        "#3d3d3d",
#     "Be Here Now":                          "#4a7a8a",
#     "The Masterplan":                       "#5c6e8a",
#     "Standing on the Shoulder of Giants":   "#6b7f8c",
#     "Heathen Chemistry":                    "#7a6a5a",
#     "Don't Believe the Truth":              "#5a4f47",
#     "Dig Out Your Soul":                    "#395e7f",
#     "Other / Unknown":                      "#bcb5ae"
# }


OASIS_ALBUM_COLORS: Dict[str, str] = {
    "Definitely Maybe":                     "#222f5b",
    "Morning Glory":                        "#3d3d3d",
    "Be Here Now":                          "#a8a49e",
    "The Masterplan":                       "#7a7670",
    "Standing on the Shoulder of Giants":   "#7a9e8a",
    "Heathen Chemistry":                    "#4f7a6a",
    "Don't Believe the Truth":              "#4a6fa5",
    "Dig Out Your Soul":                    "#2c4a7c",
    "Other / Unknown":                      "#5a5a5a"
}


_OASIS_COLOR_PALLET: Dict[str, str] = {
    "primary":      "#222f5b",
    "secondary":    "#395e7f",
    "accent":       "#271d12",
    "neutral":      "#3d3d3d",
    "light":        "#bcb5ae",
    "background":   "#f7f6f3",
    "grid":         "#d9d4ce"
}


OASIS_COLOR_PALLET: Dict[str, str] = {
    "primary":      "#222f5b",
    "secondary":    "#4a6fa5",
    "accent":       "#4f7a6a",
    "neutral":      "#7a7670",
    "light":        "#d0cdc7",
    "background":   "#e8e6e1",
    "grid":         "#a8a49e"
}


OASIS_COLOR_SEQUENCE: List[str] = [
    OASIS_COLOR_PALLET["primary"],
    OASIS_COLOR_PALLET["secondary"],
    OASIS_COLOR_PALLET["accent"],
    OASIS_COLOR_PALLET["neutral"],
    OASIS_COLOR_PALLET["light"]
]


CONTINENT_COLORS: Dict[str, str] = {
    "Europe":           OASIS_COLOR_PALLET["primary"],
    "North America":    OASIS_COLOR_PALLET["secondary"],
    "South America":    OASIS_COLOR_PALLET["accent"],
    "Asia":             OASIS_COLOR_PALLET["neutral"],
    "Oceania":          OASIS_COLOR_PALLET["light"]
}
