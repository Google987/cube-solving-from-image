import cv2
import numpy as np


# ---------------------------------------------------------
# Color classification
# ---------------------------------------------------------

def classify_color(bgr):

    b, g, r = [int(x) for x in bgr]

    # Convert BGR -> HSV
    pixel = np.uint8([[[b, g, r]]])
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0][0]

    h, s, v = [int(x) for x in hsv]

    # -----------------------------------------------------
    # WHITE
    # -----------------------------------------------------
    if s < 70 and v > 150:
        return "w"

    # -----------------------------------------------------
    # DARK / UNCERTAIN
    # -----------------------------------------------------
    if v < 60:
        return "?"

    # -----------------------------------------------------
    # ORANGE
    # -----------------------------------------------------
    # Your webcam saturates orange's red channel to ~255.
    # Orange also has G > B.
    if r > 230 and g > b:
        return "o"

    # -----------------------------------------------------
    # RED
    # -----------------------------------------------------
    if h < 7 or h >= 172:
        return "r"

    # -----------------------------------------------------
    # YELLOW
    # -----------------------------------------------------
    if 22 <= h < 45:
        return "y"

    # -----------------------------------------------------
    # GREEN
    # -----------------------------------------------------
    if 45 <= h < 90:
        return "g"

    # -----------------------------------------------------
    # BLUE
    # -----------------------------------------------------
    if 90 <= h < 140:
        return "b"

    return "?"


# ---------------------------------------------------------
# Detect the 9 stickers
# ---------------------------------------------------------

def detect_face(frame, x, y, size, face_color):
    """
    Divide a square region into 3x3 cells and
    sample the center of each cell.
    """

    colors = []

    cell_size = size // 3

    for row in range(3):
        row_colors = []

        for col in range(3):

            # Cell boundaries
            x1 = x + col * cell_size
            y1 = y + row * cell_size

            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Sample a smaller patch around the center
            margin = cell_size // 4

            cx1 = x1 + margin
            cy1 = y1 + margin
            cx2 = x2 - margin
            cy2 = y2 - margin

            patch = frame[cy1:cy2, cx1:cx2]

            avg_bgr = np.median(patch.reshape(-1, 3), axis=0).astype(np.uint8)

            if row == 1 and col == 1:
                color = face_color
            else: 
                color = classify_color(avg_bgr)

            row_colors.append(color)

            # Draw cell
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                2
            )

            # Draw detected color
            cv2.putText(
                frame,
                color,
                (x1 + 20, y1 + 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                3
            )

        colors.append(row_colors)

    return colors


def run_cube_detection():

    # ---------------------------------------------------------
    # Webcam
    # ---------------------------------------------------------

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    SIZE = 300
    WINDOW_NAME = "Rubik's Cube Color Detection"

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 640, 360)
    cv2.moveWindow(WINDOW_NAME, 100, 100)

    # ---------------------------------------------------------
    # Cube face order: U R F D L B
    # ---------------------------------------------------------

    faces = [
        ("Upper", "yellow", "U", "y"),
        ("Right", "orange", "R", "o"),
        ("Front", "green", "F", "g"),
        ("Down", "white", "D", "w"),
        ("Left", "red", "L", "r"),
        ("Back", "blue", "B", "b"),
    ]

    captured_faces = []

    current_face = 0

    print("\n========================================")
    print("       RUBIK'S CUBE SCANNER")
    print("========================================")
    print("\nScan order: U R F D L B")
    print("\nShow Upper (yellow) layer")
    print("Align the cube and press SPACE")
    print("Press Q to quit")
    print("========================================\n")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        x = (width - SIZE) // 2
        y = (height - SIZE) // 2

        # -----------------------------------------------------
        # Detect current face
        # -----------------------------------------------------

        colors = detect_face(frame, x, y, SIZE, faces[current_face][3])

        # -----------------------------------------------------
        # Outer detection box
        # -----------------------------------------------------

        cv2.rectangle(
            frame,
            (x, y),
            (x + SIZE, y + SIZE),
            (0, 255, 255),
            3
        )

        # -----------------------------------------------------
        # Instruction text
        # -----------------------------------------------------

        if current_face < len(faces):

            face_name, face_color, face_letter, face_color_short = faces[current_face]

            instruction = f"Show {face_name} ({face_color})"

            cv2.putText(
                frame,
                instruction,
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 100, 255),
                2
            )

            cv2.putText(
                frame,
                "Press SPACE to capture",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

        # -----------------------------------------------------
        # Display
        # -----------------------------------------------------

        display_frame = cv2.resize(frame, (640, 360))

        cv2.imshow(WINDOW_NAME, display_frame)

        # -----------------------------------------------------
        # Keyboard
        # -----------------------------------------------------

        key = cv2.waitKey(1) & 0xFF

        # Quit
        if key == ord("q"):
            break

        # Capture current face
        if key == 32:  # SPACE

            if current_face < len(faces):

                face_name, face_color, face_letter, face_color_short = faces[current_face]

                # Flatten 3x3 matrix
                face_string = "".join(
                    "".join(row[::-1]) for row in colors
                )

                captured_faces.append(face_string)

                print()
                print("----------------------------------------")
                print(f"Captured {face_name} ({face_letter})")
                print(face_string)
                print("----------------------------------------")

                current_face += 1

                # -------------------------------------------------
                # Next face
                # -------------------------------------------------

                if current_face < len(faces):

                    next_name, next_color, next_letter, next_color_short = faces[current_face]

                    print()
                    print(f"Show {next_name} ({next_color}) layer")
                    print("Align the cube and press SPACE")

                else:

                    # -------------------------------------------------
                    # ALL SIX FACES CAPTURED
                    # -------------------------------------------------

                    print()
                    print("========================================")
                    print("        ALL FACES CAPTURED")
                    print("========================================")

                    # Combine U R F D L B
                    whole_cube = "".join(captured_faces)

                    print()
                    print("Cube string:")
                    print(whole_cube)

                    print()
                    print("Length:", len(whole_cube))

                    print()
                    print("Face strings:")

                    for i, face in enumerate(faces):
                        name, color, letter, color_short = face
                        print(f"{letter}: {captured_faces[i]}")

                    print()
                    print("========================================")
                    print("Press Q to exit")
                    print("========================================")

                    cap.release()
                    cv2.destroyAllWindows()
                    return whole_cube


# ---------------------------------------------------------
# Start detection
# ---------------------------------------------------------
# run_cube_detection()