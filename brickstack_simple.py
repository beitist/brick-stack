#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Brick Stack - Simple Working Version
Fixed rotation and height model for LEGO/Duplo visualization
"""

from vpython import *
import random
from math import ceil, pi

# =============================================================================
# CONFIGURATION
# =============================================================================

class DebugConfig:
    GLOBAL_DEBUG = False
    BRICK_DEBUG = False
    GRID_DEBUG = False

# =============================================================================
# DIRECTIONS
# =============================================================================

class DirectionalVector(vector):
    @property
    def rotation(self):
        return {
            (0,1,0): 0,        # North
            (1,0,0): 3*pi/2,   # East  
            (0,-1,0): pi,      # South
            (-1,0,0): pi/2     # West
        }[(self.x, self.y, self.z)]

NORTH = DirectionalVector(0,1,0)
EAST = DirectionalVector(1,0,0)
SOUTH = DirectionalVector(0,-1,0)
WEST = DirectionalVector(-1,0,0)

# =============================================================================
# OCCUPANCY GRID
# =============================================================================

class OccupancyGrid:
    def __init__(self):
        self.points = {}
        
    def add_brick_footprint(self, x, y, z, length, width, height):
        if DebugConfig.GLOBAL_DEBUG and DebugConfig.GRID_DEBUG:
            print(f"Adding brick footprint: ({x},{y}) size {length}x{width}")
            
        for dx in range(length):
            for dy in range(width):
                point = (x + dx, y + dy)
                if point not in self.points:
                    self.points[point] = []
                self.points[point].append((z, z + height))

    def get_next_z(self, x, y, length, width):
        max_height = 0
        for dx in range(length):
            for dy in range(width):
                point = (x + dx, y + dy)
                if point in self.points:
                    for z_start, z_end in self.points[point]:
                        max_height = max(max_height, z_end)
        return max_height
    
    def print_grid_status(self, title="Grid Status"):
        """Print current occupancy grid status to console."""
        print(f"\n=== {title} ===")
        if not self.points:
            print("Grid is empty")
            return
            
        # Find bounds
        min_x = min(point[0] for point in self.points.keys())
        max_x = max(point[0] for point in self.points.keys())
        min_y = min(point[1] for point in self.points.keys())  
        max_y = max(point[1] for point in self.points.keys())
        
        print(f"Grid bounds: X({min_x}-{max_x}), Y({min_y}-{max_y})")
        
        # Print grid map
        print("\nOccupancy Map (# = occupied, . = free):")
        print("Y\\X ", end="")
        for x in range(min_x, max_x + 1):
            print(f"{x:2}", end="")
        print()
        
        for y in range(max_y, min_y - 1, -1):  # Top to bottom
            print(f"{y:2}: ", end="")
            for x in range(min_x, max_x + 1):
                if (x, y) in self.points:
                    max_height = max(z_end for z_start, z_end in self.points[(x, y)])
                    print(f"{int(max_height):2}", end="")
                else:
                    print(" .", end="")
            print()
        print("=" * 50)
# =============================================================================
# BRICK PROJECT & SCENE
# =============================================================================

class BrickProject:
    def __init__(self, brick_system, auto_z=True):
        self.brick_scenes = []
        self.brick_system = brick_system
        self.auto_z = auto_z

    def add_scene(self):
        scene = BrickScene(self)
        self.brick_scenes.append(scene)
        return scene

class BrickScene:
    def __init__(self, project):
        self.project = project
        self.brick_system = project.brick_system
        self.auto_z = project.auto_z
        self.bricks = []
        self.grid = OccupancyGrid()
        self.scene = self._setup_scene()

    def _setup_scene(self):
        scene = canvas(
            width=1024, height=768,
            center=vector(0,0,0),
            background=color.cyan,
            up=vector(0,0,1)
        )
        
        if self.brick_system == "duplo":
            scene.camera.pos = vector(260,-60,160)
            scene.camera.axis = vector(0,60,-60)
        else:
            scene.camera.pos = vector(130,-30,80)
            scene.camera.axis = vector(0,30,-30)
        
        return scene

    def add_baseplate(self, color_spec=color.green*0.5, custom_length=None, custom_width=None):
        baseplate = Baseplate(self.brick_system, color_spec, custom_length, custom_width)
        self.bricks.append(baseplate)
        return baseplate

    def add_brick(self, brick_type="rect", length=4, width=2, height=1, 
                  x_pos=0, y_pos=0, z_pos=0, brick_color=color.red, 
                  orientation=NORTH):
        
        # Calculate Z position with correct orientation
        if self.auto_z:
            if orientation in [NORTH, SOUTH]:
                grid_length, grid_width = length, width
            else:  # EAST or WEST
                grid_length, grid_width = width, length
            
            z_pos = self.grid.get_next_z(x_pos, y_pos, grid_length, grid_width)
            
            if self.brick_system == "duplo":
                z_pos = ceil(z_pos * 2) / 2
            else:
                z_pos = ceil(z_pos * 3) / 3

        if DebugConfig.GLOBAL_DEBUG and DebugConfig.BRICK_DEBUG:
            print(f"Adding brick {length}x{width} at ({x_pos},{y_pos},{z_pos:.2f}) facing {orientation}")

        brick = RectangularBrick(
            self.brick_system, length, width, height,
            x_pos, y_pos, z_pos, brick_color, orientation
        )
        
        self.bricks.append(brick)
        
        # Update grid with correct orientation
        if orientation in [NORTH, SOUTH]:
            self.grid.add_brick_footprint(x_pos, y_pos, z_pos, length, width, height)
        else:
            self.grid.add_brick_footprint(x_pos, y_pos, z_pos, width, length, height)
        
        # Update camera to center on construction
        self._update_camera()
        
        return brick
    
    def _update_camera(self):
        """Automatically adjust camera to center on construction."""
        if not self.grid.points:
            return
            
        # Find construction bounds
        min_x = min(point[0] for point in self.grid.points.keys())
        max_x = max(point[0] for point in self.grid.points.keys())
        min_y = min(point[1] for point in self.grid.points.keys())
        max_y = max(point[1] for point in self.grid.points.keys())
        
        # Calculate center in world coordinates
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        # Get scaling factor
        if self.bricks:
            scale = self.bricks[-1].specs["xy_factor"]
        else:
            scale = 15.6 if self.brick_system == "duplo" else 7.8
            
        world_center_x = center_x * scale  
        world_center_y = center_y * scale
        
        # Update camera position to center on construction
        if self.brick_system == "duplo":
            self.scene.camera.pos = vector(world_center_x + 100, world_center_y - 60, 160)
            self.scene.camera.axis = vector(-100, 60, -60)
        else:
            self.scene.camera.pos = vector(world_center_x + 50, world_center_y - 30, 80)
            self.scene.camera.axis = vector(-50, 30, -30)
            
        if DebugConfig.GLOBAL_DEBUG:
            print(f"Camera updated: center=({world_center_x:.1f},{world_center_y:.1f})")
    
    def print_grid_status(self, title="Current Grid Status"):
        """Print occupancy grid for debugging."""
        self.grid.print_grid_status(title)
# =============================================================================
# BRICK CLASSES  
# =============================================================================

class BasicBrick:
    BRICK_SPECS = {
        "lego": {"xy_factor": 7.8, "z_factor": 9.6, "stud_diameter": 4.8, 
                "stud_height": 1.8, "stud_xy_offset": 3.9, "stud_spacing": 7.8,
                "is_hollow": False, "baseplate_height": 0.15},
        "duplo": {"xy_factor": 15.6, "z_factor": 19.2, "stud_diameter": 8.5,
                 "stud_height": 3.6, "stud_xy_offset": 7.8, "stud_spacing": 15.6,
                 "is_hollow": True, "stud_wall_thickness": 2.2, "baseplate_height": 0.15}
    }
    
    def __init__(self, brick_system):
        self.brick_system = brick_system
        self.specs = self.BRICK_SPECS[brick_system]

    def generate_stud(self, pos, hollow=False):
        if not hollow:
            return cylinder(
                pos=pos,
                radius=self.specs["stud_diameter"] / 2,
                axis=vec(0, 0, self.specs["stud_height"]),
                color=self.brick_color
            )
        else:
            circle_shape = shapes.circle(
                radius=self.specs["stud_diameter"]/2, 
                thickness=self.specs["stud_wall_thickness"]
            )
            path = [vec(pos.x, pos.y, pos.z), 
                   vec(pos.x, pos.y, pos.z + self.specs["stud_height"])]
            return extrusion(shape=circle_shape, path=path, color=self.brick_color)

class Baseplate(BasicBrick):
    def __init__(self, brick_system, baseplate_color, custom_length=None, custom_width=None):
        super().__init__(brick_system)
        self.brick_color = baseplate_color
        
        default_size = 24 if brick_system == "duplo" else 48
        self.stud_columns = custom_width or default_size
        self.stud_rows = custom_length or default_size
        
        self.width = self.stud_columns * self.specs["xy_factor"]
        self.length = self.stud_rows * self.specs["xy_factor"]
        self.height = self.specs["baseplate_height"] * self.specs["xy_factor"]
        
        self._generate()

    def _generate(self):
        components = []
        
        # Base
        base_shape = shapes.rectangle(pos=[0, 0], width=self.width, height=self.length)
        base_path = [vec(0, 0, -self.height), vec(0, 0, 0)]
        base = extrusion(shape=base_shape, path=base_path, color=self.brick_color)
        components.append(base)
        
        # Studs
        for x in range(self.stud_columns):
            for y in range(self.stud_rows):
                if not (self.brick_system == "duplo" and 
                       (x == 0 or x == self.stud_columns-1) and 
                       (y == 0 or y == self.stud_rows-1)):
                    stud_pos = vec(
                        -self.width/2 + self.specs["stud_xy_offset"] + x * self.specs["stud_spacing"],
                        -self.length/2 + self.specs["stud_xy_offset"] + y * self.specs["stud_spacing"],
                        0
                    )
                    stud = self.generate_stud(stud_pos, hollow=False)
                    components.append(stud)
        
        return compound(components)
class RectangularBrick(BasicBrick):
    def __init__(self, brick_system, length, width, height, x, y, z, brick_color, orientation):
        super().__init__(brick_system)
        
        self.brick_color = brick_color
        self.orientation = orientation
        self.stud_columns = width
        self.stud_rows = length
        
        # Physical dimensions
        self.length = length * self.specs["xy_factor"]
        self.width = width * self.specs["xy_factor"]  
        self.height = height * self.specs["z_factor"]
        
        # World position
        self.x = x * self.specs["xy_factor"]
        self.y = y * self.specs["xy_factor"]
        self.z = z * self.specs["z_factor"]
        
        self._generate()

    def _generate(self):
        components = []
        
        # 1. Create brick body at origin
        brick_body = box(
            pos=vec(0, 0, 0),
            axis=vector(0, 1, 0),  # NORTH orientation
            length=self.length,
            width=self.width,
            height=self.height,
            color=self.brick_color,
            up=vector(0, 0, 1)
        )
        components.append(brick_body)
        
        # 2. Add studs relative to center
        for x_stud in range(self.stud_columns):
            for y_stud in range(self.stud_rows):
                stud_center = vec(
                    -self.width/2 + self.specs["stud_xy_offset"] + x_stud * self.specs["stud_spacing"],
                    -self.length/2 + self.specs["stud_xy_offset"] + y_stud * self.specs["stud_spacing"],
                    self.height/2
                )
                stud = self.generate_stud(stud_center, self.specs["is_hollow"])
                components.append(stud)
        
        # 3. Create compound
        brick_compound = compound(components)
        
        # 4. Rotate if needed
        rotation_angle = self.orientation.rotation
        if rotation_angle != 0:
            brick_compound.rotate(angle=rotation_angle, axis=vector(0, 0, 1))
        
        # 5. Move to final position
        if self.orientation == NORTH:
            final_pos = vector(self.x + self.width/2, self.y + self.length/2, self.z + self.height/2)
        elif self.orientation == EAST:
            final_pos = vector(self.x + self.length/2, self.y + self.width/2, self.z + self.height/2)
        elif self.orientation == SOUTH:
            final_pos = vector(self.x + self.width/2, self.y + self.length/2, self.z + self.height/2)
        elif self.orientation == WEST:
            final_pos = vector(self.x + self.length/2, self.y + self.width/2, self.z + self.height/2)
        else:
            # Default to NORTH
            final_pos = vector(self.x + self.width/2, self.y + self.length/2, self.z + self.height/2)
        
        brick_compound.pos = final_pos
        
        return brick_compound

# =============================================================================
# TEST FUNCTION
# =============================================================================

def create_test():
    """Create a test scene to verify functionality."""
    print("Creating test scene...")
    
    project = BrickProject("lego", auto_z=True)
    scene = project.add_scene()
    
    # Add baseplate
    scene.add_baseplate(color.green * 0.5, 20, 20)
    
    # Test all orientations
    scene.add_brick(length=4, width=2, height=1, x_pos=1, y_pos=1, 
                   brick_color=color.blue, orientation=NORTH)
    scene.add_brick(length=4, width=2, height=1, x_pos=5, y_pos=1, 
                   brick_color=color.red, orientation=EAST)
    scene.add_brick(length=4, width=2, height=1, x_pos=1, y_pos=5, 
                   brick_color=color.yellow, orientation=SOUTH)
    scene.add_brick(length=4, width=2, height=1, x_pos=5, y_pos=5, 
                   brick_color=color.green, orientation=WEST)
    
    # Test stacking
    scene.add_brick(length=2, width=2, height=1, x_pos=2, y_pos=2, 
                   brick_color=color.orange, orientation=NORTH)
    scene.add_brick(length=2, width=1, height=1, x_pos=2, y_pos=2, 
                   brick_color=color.purple, orientation=EAST)
    
    print("Test completed! Check the 3D visualization.")
    return project

if __name__ == "__main__":
    try:
        test_project = create_test()
        print("✓ Success! 3D scene should be visible.")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
