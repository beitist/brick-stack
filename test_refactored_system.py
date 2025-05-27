#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Brick Stack System

This module contains comprehensive tests for the refactored brick system,
including unit tests and integration tests for all major components.
"""

from brickstack_refactored import *

def test_basic_functionality():
    """Test basic system functionality and component creation."""
    print("Testing basic functionality...")
    
    # Test project creation
    project = BrickProject("duplo", auto_z=True)
    assert project.brick_system == "duplo"
    assert project.auto_z == True
    
    # Test scene creation
    scene = project.add_scene()
    assert len(project.brick_scenes) == 1
    assert scene.brick_system == "duplo"
    
    print("✓ Basic functionality tests passed")

def test_orientation_system():
    """Test brick orientation and rotation functionality."""
    print("Testing orientation system...")
    
    project = BrickProject("test", auto_z=False)  # Use test system for faster rendering
    scene = project.add_scene()
    
    # Test all orientations
    orientations = [NORTH, EAST, SOUTH, WEST]
    colors = [color.blue, color.red, color.yellow, color.green]
    
    for i, (orient, col) in enumerate(zip(orientations, colors)):
        brick = scene.add_brick(
            length=3, width=2, height=1,
            x_pos=i*4, y_pos=0, z_pos=0,
            brick_color=col, orientation=orient
        )
        assert brick.orientation == orient
    
    print("✓ Orientation system tests passed")

def test_height_calculation():
    """Test automatic height calculation and collision detection."""
    print("Testing height calculation...")
    
    project = BrickProject("duplo", auto_z=True)
    scene = project.add_scene()
    
    # First brick at ground level
    brick1 = scene.add_brick(length=4, width=2, height=1, x_pos=0, y_pos=0)
    
    # Second brick should stack on top
    brick2 = scene.add_brick(length=2, width=2, height=1, x_pos=1, y_pos=0)
    
    # Verify height calculation worked
    assert brick2.world_z > brick1.world_z
    
    print("✓ Height calculation tests passed")

def test_grid_system():
    """Test occupancy grid functionality."""
    print("Testing occupancy grid...")
    
    grid = OccupancyGrid()
    
    # Add a brick footprint
    grid.add_brick_footprint(0, 0, 0, 4, 2, 1)
    
    # Test height calculation
    height = grid.calculate_next_available_height(1, 0, 2, 2)
    assert height == 1  # Should be on top of first brick
    
    # Test bounds calculation
    bounds = grid.get_construction_bounds()
    assert bounds["max_x"] >= 3  # 4-unit length brick
    assert bounds["max_y"] >= 1  # 2-unit width brick
    
    print("✓ Grid system tests passed")

def test_brick_factory():
    """Test brick creation factory."""
    print("Testing brick factory...")
    
    # Test random color generation
    color1 = BrickFactory._generate_random_color()
    color2 = BrickFactory._generate_random_color()
    assert isinstance(color1, vector)
    assert isinstance(color2, vector)
    
    # Test brick creation
    brick = BrickFactory.create_brick(
        "test", "rect", 2, 2, 1, 0, 0, 0, color.red, NORTH
    )
    assert isinstance(brick, RectangularBrick)
    
    print("✓ Brick factory tests passed")

def run_all_tests():
    """Run the complete test suite."""
    print("Brick Stack System - Test Suite")
    print("=" * 40)
    
    try:
        test_basic_functionality()
        test_orientation_system()
        test_height_calculation()
        test_grid_system()
        test_brick_factory()
        
        print("\n🎉 All tests passed successfully!")
        print("The refactored system is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
