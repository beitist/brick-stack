#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test file to demonstrate height model with rotation

from brickstack import *

# Create a project with auto-z enabled
test_project = BrickProject("duplo", auto_z=True)
test_project.add_scene()

# Add baseplate
test_project.brick_scenes[0].add_baseplate(color.green * 0.4, 12, 12)

print("Testing height model with different orientations...")

# Layer 1: Base layer with different orientations
print("Layer 1: Base bricks in different orientations")
test_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 0, 0, 0, color.blue, NORTH
)

test_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 4, 0, 0, color.red, EAST  # Should be rotated 90°
)

# Layer 2: Stacking on top - should automatically find correct height
print("Layer 2: Stacking bricks on top")
test_project.brick_scenes[0].add_brick(
    "rect", 2, 2, 1, 1, 0, 0, color.yellow, NORTH  # Should stack on blue brick
)

test_project.brick_scenes[0].add_brick(
    "rect", 2, 2, 1, 4, 1, 0, color.green, SOUTH  # Should stack on red brick
)

# Layer 3: More complex stacking
print("Layer 3: More complex stacking")
test_project.brick_scenes[0].add_brick(
    "rect", 2, 1, 1, 1, 1, 0, color.orange, WEST  # Should stack even higher
)

print("Test completed!")
print("If height model works correctly:")
print("- Blue and red bricks should be at ground level")
print("- Yellow and green bricks should be stacked on top") 
print("- Orange brick should be at the highest level")

# Add coordinate markers
x_marker = curve(pos=[vec(-50, 0, 1), vec(50, 0, 1)], color=color.white)
y_marker = curve(pos=[vec(0, -50, 1), vec(0, 50, 1)], color=color.white)
