"""
Everything related to Oasis' albums and songs.
"""


from typing import List, Dict


ALBUMS: Dict[str, List[str]] = {
    "Definitely Maybe": [  # 1994
        "Rock 'n' Roll Star",
        "Shakermaker",
        "Live Forever",
        "Up in the Sky",
        "Columbia",
        "Supersonic",
        "Bring It On Down",
        "Cigarettes & Alcohol",
        "Slide Away",
        "Married with Children",
        "Whatever",
    ],

    "Morning Glory": [  # 1995
        "Hello",
        "Roll With It",
        "Wonderwall",
        "Don't Look Back in Anger",
        "Hey Now!",
        "Some Might Say",
        "Cast No Shadow",
        "She's Electric",
        "Morning Glory",
        "Champagne Supernova",
        "The Masterplan",
    ],

    "Be Here Now": [  # 1997
        "D'You Know What I Mean?",
        "My Big Mouth",
        "Stand by Me",
        "I Hope, I Think, I Know",
        "The Girl in the Dirty Shirt",
        "Fade Away",
        "Don't Go Away",
        "Be Here Now",
        "Magic Pie",
        "It's Gettin' Better (Man!!)",
    ],

    "The Masterplan": [  # 1998
        "Acquiesce",
        "Half the World Away",
        "Talk Tonight",
        "Listen Up",
        "Rockin' Chair",
    ],

    "Standing on the Shoulder of Giants": [  # 2000
        "Go Let It Out",
        "Who Feels Love?",
        "Where Did It All Go Wrong?",
        "Sunday Morning Call",
    ],

    "Heathen Chemistry": [  # 2002
        "The Hindu Times",
        "Force of Nature",
        "Better Man",
        "Little by Little",
        "She Is Love",
        "Stop Crying Your Heart Out",
        "Songbird",
    ],

    "Don't Believe the Truth": [  # 2005
        "Lyla",
        "The Importance of Being Idle",
        "Let There Be Love",
        "Part of the Queue",
        "Keep the Dream Alive",
    ],

    "Dig Out Your Soul": [  # 2008
        "Bag It Up",
        "The Shock of the Lightning",
        "I'm Outta Time",
        "Falling Down",
    ],
}


# Inverted lookup: song name -> album name
SONGS: Dict[str, str] = {
    song: album
    for album, songs in ALBUMS.items()
    for song in songs
}


ALBUM_ORDER: List[str] = [
    "Definitely Maybe",
    "Morning Glory",
    "Be Here Now",
    "The Masterplan",
    "Standing on the Shoulder of Giants",
    "Heathen Chemistry",
    "Don't Believe the Truth",
    "Dig Out Your Soul",
    "Other / Unknown",
]
