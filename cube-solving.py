import kociemba

from detect_colors import run_cube_detection


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


def solve_the_cube(solution):
    from motor_control import close, solve_physical_cube
    solve_physical_cube(solution)
    close()


if __name__ == "__main__":
    colors = run_cube_detection()

    # order: URFDLB
    # colors = "wgowyywor ygbgoboyw bggwgwyry rbgrwowyg obrorroybyrbobwrbg"

    cube = colors_to_faces(colors)

    print("Kociemba string:", cube)
    solution = kociemba.solve(cube)
    print("Solution: ", solution)
    input("Place the cube properly and press Enter...")
    solve_the_cube(solution)
    print("SOLVED")
