#!/usr/bin/env python

"""
printcore_motion_shapes.py: A script to demonstrate basic motion control
of a 3D printer using the printcore library. This script will guide the
printer head to draw a circle, a triangle, and a star shape.

Make sure to have the 'printrun' library installed:
pip install printrun

**WARNING**: This script will move your 3D printer's hardware.
Ensure your printer is clear of any obstructions and that the dimensions
and speeds are safe for your specific machine before running.
The user is responsible for any potential damage.
"""

import time
import math
from printrun.printcore import printcore


class ShapeDrawer:
    """
    A class to handle the connection to the printer and draw various shapes.
    """

    def __init__(self, port, baud):
        """
        Initializes the connection to the printer.
        """
        self.p = printcore()
        print(f"Connecting to printer on port {port} at {baud} baud...")
        try:
            self.p.connect(port, baud)
            while not self.p.online:
                time.sleep(0.1)
            print("Printer is online.")
        except Exception as e:
            print(f"Failed to connect to printer: {e}")
            exit()

    def disconnect(self):
        """
        Disconnects from the printer.
        """
        self.p.disconnect()
        print("Disconnected from printer.")

    def send_gcode(self, gcode):
        """
        Sends a G-code command to the printer and waits for it to be processed.
        """
        print(f"Sending: {gcode}")
        self.p.send_now(gcode)
        # A small delay to ensure the command is processed.
        # For more complex applications, you would want a more robust
        # way of checking the command queue.
        time.sleep(0.01)

    def setup_printer(self):
        """
        Initializes the printer to a known state.
        """
        print("Setting up printer...")
        self.send_gcode("G21")  # Set units to millimeters
        self.send_gcode("G90")  # Set to absolute positioning
        # self.send_gcode("G28")  # Home all axes # NOTE: do not home, because there are no limit switches
        # self.send_gcode("G1 Z5 F3000")  # Move Z axis up to avoid scratching the bed

    def draw_circle(self, center_x, center_y, radius, segments, speed):
        """
        Draws a circle.
        :param center_x: The x-coordinate of the circle's center.
        :param center_y: The y-coordinate of the circle's center.
        :param radius: The radius of the circle.
        :param segments: The number of line segments to approximate the circle.
        :param speed: The movement speed in mm/min.
        """
        print("\n--- Drawing Circle ---")
        # Move to the starting point of the circle
        start_x = center_x + radius
        start_y = center_y
        self.send_gcode(f"G1 X{start_x:.2f} Y{start_y:.2f} F{speed}")

        # Draw the circle with small line segments
        for i in range(1, segments + 1):
            angle = 2 * math.pi * i / segments
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.send_gcode(f"G1 X{x:.2f} Y{y:.2f} F{speed}")

    def draw_triangle(self, center_x, center_y, side_length, speed):
        """
        Draws an equilateral triangle.
        :param center_x: The x-coordinate of the triangle's center.
        :param center_y: The y-coordinate of the triangle's center.
        :param side_length: The length of each side of the triangle.
        :param speed: The movement speed in mm/min.
        """
        print("\n--- Drawing Triangle ---")
        height = (math.sqrt(3) / 2) * side_length

        # Calculate vertex coordinates relative to the center
        p1_x = center_x - side_length / 2
        p1_y = center_y - height / 3

        p2_x = center_x + side_length / 2
        p2_y = center_y - height / 3

        p3_x = center_x
        p3_y = center_y + (2 * height) / 3

        # Move to each vertex
        self.send_gcode(f"G1 X{p1_x:.2f} Y{p1_y:.2f} F{speed}")
        self.send_gcode(f"G1 X{p2_x:.2f} Y{p2_y:.2f} F{speed}")
        self.send_gcode(f"G1 X{p3_x:.2f} Y{p3_y:.2f} F{speed}")
        self.send_gcode(f"G1 X{p1_x:.2f} Y{p1_y:.2f} F{speed}")  # Back to start

    def draw_star(self, center_x, center_y, outer_radius, inner_radius, points, speed):
        """
        Draws a star.
        :param center_x: The x-coordinate of the star's center.
        :param center_y: The y-coordinate of the star's center.
        :param outer_radius: The radius of the outer points.
        :param inner_radius: The radius of the inner points.
        :param points: The number of points on the star.
        :param speed: The movement speed in mm/min.
        """
        print("\n--- Drawing Star ---")
        all_points = []
        angle_step = math.pi / points

        for i in range(points * 2):
            radius = outer_radius if i % 2 == 0 else inner_radius
            angle = i * angle_step
            x = center_x + radius * math.cos(angle - math.pi / 2)
            y = center_y + radius * math.sin(angle - math.pi / 2)
            all_points.append((x, y))

        # Move to the starting point
        self.send_gcode(f"G1 X{all_points[0][0]:.2f} Y{all_points[0][1]:.2f} F{speed}")

        # Draw the star by connecting the points
        for x, y in all_points[1:]:
            self.send_gcode(f"G1 X{x:.2f} Y{y:.2f} F{speed}")

        # Close the shape
        self.send_gcode(f"G1 X{all_points[0][0]:.2f} Y{all_points[0][1]:.2f} F{speed}")


def main():
    """
    Main function to run the shape drawing demonstration.
    """
    # --- CONFIGURATION ---
    # IMPORTANT: Change this to your printer's serial port.
    # On Linux, it's often /dev/ttyACM0 or /dev/ttyUSB0.
    # On Windows, it's COMx (e.g., COM3).
    # On macOS, it's /dev/cu.usbmodemXXXX.
    PORT = "/dev/tty.usbmodem1101"
    BAUD = 57600

    # Shape parameters
    CENTER_X = 100
    CENTER_Y = 100
    MOVE_SPEED = 1500  # in mm/min

    # --- SCRIPT EXECUTION ---
    drawer = ShapeDrawer(PORT, BAUD)

    try:
        drawer.setup_printer()

        # Wait for user to confirm before starting
        input("Printer setup is complete. Press Enter to start drawing shapes...")

        # Draw a circle
        drawer.draw_circle(
            center_x=CENTER_X,
            center_y=CENTER_Y,
            radius=20,
            segments=50,
            speed=MOVE_SPEED,
        )
        time.sleep(2)  # Pause between shapes

        # Draw a triangle
        drawer.draw_triangle(
            center_x=CENTER_X, center_y=CENTER_Y, side_length=40, speed=MOVE_SPEED
        )
        time.sleep(2)

        # Draw a 5-pointed star
        drawer.draw_star(
            center_x=CENTER_X,
            center_y=CENTER_Y,
            outer_radius=30,
            inner_radius=15,
            points=5,
            speed=MOVE_SPEED,
        )
        time.sleep(2)

        print("\nAll shapes drawn successfully!")

        # # Return to home position  # NOTE: do not home
        # drawer.send_gcode("G28")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        drawer.disconnect()


if __name__ == "__main__":
    main()
