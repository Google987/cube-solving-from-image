import serial
import time


PORT = "/dev/cu.SLAB_USBtoUART"
BAUDRATE = 115200


ser = serial.Serial(
    PORT,
    BAUDRATE,
    timeout=0.1
)

# Give ESP32 time to reset after opening serial
time.sleep(2)


def solve_physical_cube(solution):

    solution = solution.strip().upper()

    print()
    print("=" * 50)
    print("Sending solution:")
    print(solution)
    print("=" * 50)

    # Send solution + newline
    ser.write((solution + "\n").encode())

    # Wait for ESP32
    while True:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        # Print ESP32 message
        print(f"[ESP32] {line}")

        # ESP32 says everything is finished
        if line == "SOLUTION_DONE":
            print()
            print("Cube solution completed.")
            break


def close():
    ser.close()
    print("Serial connection closed.")


# Example
# solve_physical_cube(
#     "U2 R2 L F R' D B' R F2 B2 R L2 D' F2 B2 R2 U2 F2 D B2 L2"
# )
# close()
