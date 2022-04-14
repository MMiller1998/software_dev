AIRPORTS: dict = {
    "width": 300,
    "height": 700,
    "cities": [
        ["SAN", [150, 100]],
        ["LAX", [75, 200]],
        ["LAS", [225, 250]],
        ["SFO, SJC", [75, 300]],
        ["PDX", [150, 400]],
        ["SEA", [150, 500]]
    ],
    "connections": {
        "SAN": {
            "LAX": {
                "white": 3
            },
            "LAS": {
                "green": 5
            }
        },
        "LAX": {
            "SFO, SJC": {
                "blue": 4,
                "green": 4,
                "red": 4
            }
        },
        "LAS": {
            "SFO, SJC": {
                "blue": 4
            }
        },
        "PDX": {
            "SFO, SJC": {
                "white": 4
            },
            "SEA": {
                "red": 3
            }
        }
    }
}

EMPTY: dict = {
    'width': 523,
    'height': 678,
    'cities': [],
    'connections': []
}
