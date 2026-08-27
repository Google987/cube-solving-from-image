import kociemba


def colors_to_faces(cube):
    """Convert a 54-character color string to Kociemba notation."""
    cube = cube.lower().replace(" ", "").replace("\n", "")

    if len(cube) != 54:
        raise ValueError(f"Cube must contain 54 colors, got {len(cube)}")

    # If using first-letter color notation:
    # y=yellow, o=orange, g=green, w=white, r=red, b=blue
    letter_to_face = {
        "y": "U",
        "o": "R",
        "g": "F",
        "w": "D",
        "r": "L",
        "b": "B",
    }

    try:
        return "".join(letter_to_face[c] for c in cube)
    except KeyError as e:
        raise ValueError(f"Invalid color character: {e.args[0]}")


if __name__ == "__main__":
    # order: URFDLB
    colors = "wyrgyorbg wbygoyorg ywrogowgy owgbwwbrw bygrrwyyb brrobbogo"

    cube = colors_to_faces(colors)

    print("Kociemba string:", cube)
    print("Solution:", kociemba.solve(cube))