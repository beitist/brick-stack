#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test file to demonstrate fixed rotation functionality

from brickstack import *

# Create a project
test_project = BrickProject("duplo")
test_project.add_scene()

# Add baseplate
test_project.brick_scenes[0].add_baseplate(color.green * 0.4, 16, 16)

# Test different orientations with the same brick size
# This should clearly show the rotation working

print("Adding brick facing NORTH (blue)")
test_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 2, 2, 0, color.blue, NORTH
)

print("Adding brick facing EAST (red)")  
test_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 6, 2, 0, color.red, EAST
)

print("Adding brick facing SOUTH (yellow)")
test_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 2, 6, 0, color.yellow, SOUTH
)

print("Adding brick facing WEST (green)")
test_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 6, 6, 0, color.green, WEST
)

# Add some coordinate markers for reference
x_marker = curve(pos=[vec(-50, 0, 1), vec(50, 0, 1)], color=color.white)
y_marker = curve(pos=[vec(0, -50, 1), vec(0, 50, 1)], color=color.white)

print("Test completed! All four orientations should now be visible.")
print("Blue=NORTH, Red=EAST, Yellow=SOUTH, Green=WEST")
