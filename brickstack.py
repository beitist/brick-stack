#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# lego and duplo are trademarks of their respective owners!

from vpython import *
import random

# Debug options
# GLOBAL = Turn on/off all debug options
GLOBAL_DEBUG = True

# Turn on/off desired debug output
CALC_DEBUG = False
STUD_DEBUG = True
GRID_DEBUG = True
BRICK_DEBUG = True
STOP_DEBUG = True


# Expanding vector-class from vpython:
class DirectionalVector(vector):
    @property
    def rotation(self):
        return {
            (0,1,0): 0,      # North
            (1,0,0): 3*pi/2, # East
            (0,-1,0): pi,    # South
            (-1,0,0): pi/2   # West
        }[(self.x, self.y, self.z)]

NORTH = DirectionalVector(0,1,0)
EAST = DirectionalVector(1,0,0)
SOUTH = DirectionalVector(0,-1,0)
WEST = DirectionalVector(-1,0,0)

##### COORDINATES #####
## x = length from left to right (standard camera view)
## y = width from front to back (standard camera view)
## z = height from bottom to top (standard camera view)
## coordinates x, y, z correspond with l, w, h values
#######################

##### COORDINATES (NEW) #####
## length = typically the longer side of a brick (e.g. 4)
## width = typically the shorter side of a brick (e.g. 2)
## orientation = N, S, E, W aligning with length when placed
## x/y = corner of smallest x/y-coordinate (placing a brick always from "lower/left", no matter the orientation)
## z = either automatic or manual

####### TO DO ########
## 0: close scenes? update cameras?
## 1: Auto_Camera, auto_scene
## 2: render to file
## 3: read simple scene files
## 4: create booklet
## 5: encapsulation ok? CameraManager?
## 6: make baseplate a subclass to rectangularbrick??
## 7: try clone for stud generation (duplo!)

####### NOTES #########
## update camera better from BrickProject? ##

class BrickProject:
    """Class holding individual scenes (= steps in constructing a brick project)
    
    Will (soon) provide functionality for file handling of simplified project files"""
    # planned use:
    # - load project file
    # - save renders
    #
    # description
    # brick_system = duplo/lego
    # auto_z = True // turn off by initialising project with auto_z = False
    
    def __init__(self, brick_system, auto_z = True):
        """BrickProject init
        
        Args:
            brick_system (str): "duplo", "lego" or "test"
            auto_z (bool): True (standard), change to define own z-values

        Additional Variables:
            brick_scenes (array): empty array to store brick_scenes (int-index)
        """
        self.brick_scenes = []
        self.brick_system = brick_system
        self.auto_z = auto_z        

    # special_canvas, special_camera not yet there :)
    def add_scene(self, special_canvas=None, special_camera=None):
        """add_scene to a BrickProject

        Scenes are intended as construction steps of a larger brick project,
        so that you can reconstruct the visual design with your bricks and then switch to the
        next scene showing the next steps. Scenes can maintain an automatic
        camera and canvas object, or you can specify your own.

        Add baseplates to scenes like bricks with different arguments. Baseplates
        are centered at (1, 1) by default and are 24x24 (duplo) or 48x48 (lego). Baseplates
        are not considered when placing bricks with auto-z.
        
        Args:
            special_canvas (obj): vpython-canvas object, optional
            special_camera (obj): vpython-camera object, optional
            
        Scenes are appended to the brick_scene array."""
        brick_scene = BrickScene(self, special_canvas, special_camera)
        self.brick_scenes.append(brick_scene)

    def get_scene_index(self, brick_scene):
        return self.brick_scenes.index(brick_scene)

class OccupancyGrid:
    """Helper class to store z-values for occupied grid locations
    """
    def __init__(self):
        self.points = {}  # Dictionary using (x,y) as Key
        
    def add_brick(self, x, y, z, length, width, height):
        """Store mathematical representation of bricks for z calculation in helper grid

        Args:
            x (int): x-location of brick
            y (int): y-location of brick
            z (int): z-location of brick
            width (int): width of brick in multiples of basic unit
            length (int): see above
            height (int): see above
        """
        if GLOBAL_DEBUG and GRID_DEBUG: print(f"Function add_brick/OccupancyGrid: adding brick at ({x},{y}) with w={width}, l={length}")
        # for every point occupied by a brick
        for dx in range(length):
            for dy in range(width):
                point = (x + dx, y + dy)
                if point not in self.points:
                    self.points[point] = []
                self.points[point].append((z, z + height))

    def get_xyz_range(self):
        # define min/max values (min-z is always 0 on automatic setting)
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        min_z = 0
        max_z = 0

        # obtain max z
        for z_summary_of_coordinate in self.points:
            if GLOBAL_DEBUG and CALC_DEBUG: print(f"value {self.points[z_summary_of_coordinate]}, key: {z_summary_of_coordinate}")
            for z_minmax_value in self.points[z_summary_of_coordinate]:
                z_start, z_end = z_minmax_value
                if z_start < min_z : min_z = z_start
                if z_end > max_z : max_z = z_end

        # obtain min/max x and y:
        xy_keys = self.points.keys()
        for xy_tuple in xy_keys:
            x_value, y_value = xy_tuple
            if x_value < min_x : min_x = x_value
            if x_value > max_x : max_x = x_value
            if y_value < min_y : min_y = y_value
            if y_value > max_y : max_y = y_value

        results = {
            "min_x" : min_x,
            "max_x" : max_x,
            "min_y" : min_y,
            "max_y" : max_y,
            "min_z" : min_z,
            "max_z" : max_z
        }

        if GLOBAL_DEBUG and CALC_DEBUG: print(results)

        return results

    def get_next_z(self, x, y, width, length):
        max_height = 0

        # check all points the new brick might occupy
        for dx in range(width):
            for dy in range(length):
                point = (x + dx, y + dy)
                if point in self.points:
                    # Finde höchsten Punkt an dieser Stelle
                    for z_start, z_end in self.points[point]:
                        max_height = max(max_height, z_end)
        
        if GLOBAL_DEBUG and GRID_DEBUG: print(f"Max height: {max_height}")
        
        return max_height


class BrickScene:
    """BrickScene is a functional container for individual brick scenes
    and provides orientation, camera and scene settings
    """

    def __init__(self, project, special_scene=None, special_camera=None):
        """__init__ brick_scene

        Args:
            project (obj::BrickProject): contains copy of brick-project to access standard values
            special_scene (obj::vpython-scene, optional): individual scene settings. Defaults to None.
            special_camera (obj::vpython-camera, optional): individual camera settings. Defaults to None.
        """
        self.grid = OccupancyGrid()
        self.project = project
        self.brick_system = project.brick_system
        self.auto_z = project.auto_z
        self.bricks = []

        if special_scene == None:
            self.has_special_scene = False
        else:
            self.has_special_scene = True

        if special_camera == None:
            self.has_special_camera = False
        else:
            self.has_special_camera = True
        
        self.scene = self.set_scene(special_scene, special_camera)

    def add_baseplate(self, baseplate_color = color.green * 0.5, baseplate_custom_length = None, baseplate_custom_width = None, baseplate_custom_x = None, baseplate_custom_y = None):
        """Add a baseplate to a scene

        Careful: The position of the baseplate is given by the center, not as with bricks by the lower left corner.

        Args:
            baseplate_color (vector (rgb) or color.x, optional): Specify a different color for the baseplate. Defaults to color.green.
            baseplate_custom_length (int, optional): Individual length of baseplate; internal defaults = 24 / 48 (lego/duplo). Defaults to None.
            baseplate_custom_width (int, optional): See length. Defaults to None.
            baseplate_custom_x (int, optional): Custom center position of baseplate; internal default = 0. Defaults to None.
            baseplate_custom_y (_type_, optional): See custom_y. Defaults to None.
        """
        baseplate = BrickFactory.create_baseplate(self.brick_system, baseplate_color, baseplate_custom_length, baseplate_custom_width, baseplate_custom_x, baseplate_custom_y)
        self.bricks.append(baseplate)

    def set_scene(self, special_scene=None, special_camera=None):
        # Scene with std values
        # special scene/camera not yet implemented

        self.scene = canvas(
            width=1024,            # window width
            height=768,           # window height
            center=vector(0,0,0), # Scene center
            background=color.cyan,  # bg color
            up=vector(0,0,1)     # Z is "up"
        )

        # Kamera mittig von oben/vorne
        if self.brick_system == "lego":
            self.scene.camera.pos = vector(130,-30,80)    # Y negativ = von vorne, Z positiv = von oben
            self.scene.camera.axis = vector(0,30,-30)   # Schaut nach hinten und leicht nach unten
        else:
            self.scene.camera.pos = vector(260,-60,160)    # Y negativ = von vorne, Z positiv = von oben
            self.scene.camera.axis = vector(0,60,-60)   # Schaut nach hinten und leicht nach unten            

        # self.scene.autoscale = True

    def update_camera_position(self):
        """Update camera position after new block is placed

        Args:
            none

        Currently only calculates x-extension and moves the camera so it points to x-center of scene.
        """    
        xyz_range = self.grid.get_xyz_range()
        min_x = xyz_range["min_x"]
        max_x = xyz_range["max_x"]
        dx = max_x - min_x
        scene_index = self.get_my_scene_index()
        if GLOBAL_DEBUG and CALC_DEBUG: print(f"scene_index: {scene_index}")

        current_canvas = canvas.get_selected()
        current_canvas.camera.pos = vector((max_x - dx/2) * self.bricks[-1].specs["xy_factor"], -30, 80)

    def calculate_z_pos(self, length, width, height, x_pos, y_pos):
       # Find smallest possible z
        z = self.grid.get_next_z(x_pos, y_pos, length, width)
        # round up to next valid height
        if self.brick_system == "duplo":
            # round to multiples of 1/2
            if GLOBAL_DEBUG and (BRICK_DEBUG or GRID_DEBUG): print(f"z before rounding: {z}")
            z = ceil(z * 2) / 2
        else:  # lego
            # round to multiples of 1/3
            z = ceil(z * 3) / 3
        return z
    
    def calculate_xyz_range(self):
        xyz_range = self.grid.get_xyz_range(self)       

    def add_brick(self, brick_type : str = "rect", length : int = 4, width : int = 2, height : int = 1, x_pos : int = 0, y_pos : int = 0, z_pos : int = 0, brick_color : vector = color.red, brick_orientation : vector = NORTH):
        """Add a new brick to your project/scene

        Args:
            brick_type (str): Choose from "rect" or "rect" ;-) - more to come
            length (int): Length of the brick in number of studs (x-direction / "left to right")
            width (int): Width in number of studs
            height (int): Height in basic heights, use: .5, 1, 2 for duplo, .33, .66, 1, 2 for lego
            x_pos (int): x-position of the left bottom corner (in North-orientation)
            y_pos (int): see above
            z_pos (int): see above
            brick_color (vector): vector(r, g, b) or predefined color.x
            brick_orientation (vector): NORTH, SOUTH, EAST, WEST
        """
        # auto-z or not
        if self.project.auto_z:
            z_pos = self.calculate_z_pos(length, width, height, x_pos, y_pos)
        else:
            z_pos = z_pos
        
        if GLOBAL_DEBUG and BRICK_DEBUG:
            print(f"Call to add_brick in BrickScene:\nz-pos after get_min: {z_pos}")
            print(f"brickFactory call with: {brick_type}, l={length}, w={width}, h={height}, x={x_pos}, y={y_pos}, z={z_pos}")

        brick = BrickFactory.create_brick(self.brick_system,
                                          brick_type, 
                                          length, 
                                          width, 
                                          height, 
                                          x_pos, 
                                          y_pos, 
                                          z_pos, 
                                          brick_color,
                                          brick_orientation)
        
        self.bricks.append(brick)

        # add math model of brick to occupancy grid (for z-calculation)
        self.grid.add_brick(x_pos, y_pos, z_pos, length, width, height)

        # update camera view
        self.update_camera_position()

    def get_my_scene_index(self):
        return self.project.get_scene_index(self)


class BrickFactory:
    @staticmethod
    def create_brick(brick_system, brick_type, length, width, height, x_pos, y_pos, z_pos, brick_color, brick_orientation):
        if brick_color == "random":
            final_brick_color = BrickFactory.choose_random_color()
        else:
            final_brick_color = brick_color

        if brick_type == 'rect':
            brick = RectangularBrick(brick_system,
                                     length, 
                                     width, 
                                     height, 
                                     x_pos, 
                                     y_pos, 
                                     z_pos, 
                                     final_brick_color,
                                     brick_orientation)
        else:
            brick = RectangularBrick(brick_system,
                                     length, 
                                     width, 
                                     height, 
                                     x_pos,
                                     y_pos, 
                                     z_pos, 
                                     final_brick_color,
                                     brick_orientation)

        return brick  

    @staticmethod
    def create_baseplate(brick_system, baseplate_color, baseplate_custom_length, baseplate_custom_width, baseplate_center_x, baseplate_center_y):
        # custom_x/y: center (standard: 0,0)
        if GLOBAL_DEBUG and CALC_DEBUG: print(f"Baseplate values: x: {baseplate_center_x}, y: {baseplate_center_y}, length: {baseplate_custom_length}, width: {baseplate_custom_width}")

        baseplate = Baseplate(brick_system, baseplate_color, baseplate_custom_length, baseplate_custom_width, baseplate_center_x, baseplate_center_y)

        return baseplate

    @staticmethod
    def choose_random_color():
        """Randomize brick color

        Returns:
            vector: RGB-vector for use with vpython
        """
        random.seed()
        red = random.randint(0, 5) / 5
        green = random.randint(0, 5) / 5
        blue = random.randint(0, 5) / 5

        return vector(red, green, blue)


class BasicBrick:
    """Parent class for all bricks containing general information and a testing format
    """
    # SPECS:
    # ======
    # generic lego/duplo for all bricks, in mm
    # additional tools / info

    # class variables for mm-dimensions
    BRICK_SPECS = {
        "lego": {
            "xy_factor": 7.8,
            "z_factor": 9.6,
            "stud_diameter": 4.8,
            "stud_height": 1.8,
            "stud_xy_offset": 3.9,
            "stud_spacing": 7.8,
            "stud_wall_thickness": 0,
            "is_hollow": False,
            "baseplate_height" : 0.15,
            "baseplate_roundness" : 0.02
        },

        # due to likely render issues, stud diameter is reduced by half of wall thickness
        "duplo": {
            "xy_factor": 15.6,
            "z_factor": 19.2,
            "stud_diameter": 8.5,
            "stud_height": 3.6,
            "stud_xy_offset": 7.8,
            "stud_spacing": 15.6,
            "stud_wall_thickness": 2.2,
            "is_hollow": True,
            "baseplate_height" : 0.15,
            "baseplate_roundness" : 0.08          
        },

        "test": {
            "xy_factor": 1,
            "z_factor": 1,
            "stud_diameter": 0.5,
            "stud_height": 0.3,
            "stud_xy_offset": 0.5,
            "stud_spacing": 1,
            "stud_wall_thickness": 0.15,
            "is_hollow": False    
        }
    }
        
    def __init__(self, brick_system):
        """Parent brick class __init__

        is called as super from child bricks

        Args:
            brick_system (str): "lego", "duplo" or "test"; called as super from specific brick; handed over from BrickProject
        """
        self.brick_system = brick_system
        self.specs = self.BRICK_SPECS[brick_system]

    def generate_stud(self, pos, hollow=False, wall_thickness = None):
        """3d-function to generate and render individual studs for compound

        Distinguishes between brick_systems (lego, duplo) to render 

        Args:
            pos (vector): center point of stud basis
            hollow (bool, optional): Make hollow studs (or not). Defaults to False.
            wall_thickness (int, optional): Stud wall thickness; see BRICK_SPECS. Defaults to None.

        Returns:
            cylinder or extrusion (obj::vpython): returns a cylinder or an extruded circle (hollow cylinder) representing one stud
        """
        if GLOBAL_DEBUG and STUD_DEBUG: print(f"Generating 3d-stud at {pos}.")
        if not hollow:
            generated_stud = cylinder(
                pos=pos,
                radius=self.specs["stud_diameter"] / 2,
                axis=vec(0.0, 0.0, self.specs["stud_height"]),
                color=self.brick_color
            )
        else:
            cyl_base = shapes.circle(
                radius = self.specs["stud_diameter"]/2, 
                thickness = self.specs["stud_wall_thickness"]
            )

            cyl_path = [
                vec(pos.x, pos.y, pos.z),
                vec(pos.x, pos.y, pos.z + self.specs["stud_height"])
            ]

            generated_stud = extrusion(
                shape = cyl_base, 
                path = cyl_path, 
                color = self.brick_color
            )
 
        return generated_stud


class Baseplate(BasicBrick):
    def __init__(self, brick_system, baseplate_color, baseplate_length : int = None, baseplate_width : int = None, baseplate_center_x : int = None, baseplate_center_y : int = None):
        super().__init__(brick_system)
        self.stud_x_counter = (
            baseplate_width if baseplate_width is not None
            else (24 if brick_system == "duplo" else 48)
        )
        self.stud_y_counter = (
            baseplate_length if baseplate_length is not None
            else (24 if brick_system == "duplo" else 48)
        )
        # this is not ideal - how to organise brick/baseplate classes?
        self.brick_color = baseplate_color
        # Factorise size based on brick system
        self.baseplate_length = (
            self.specs["xy_factor"] * baseplate_length
            if baseplate_length is not None
            else (self.specs["xy_factor"] * (24 if brick_system == "duplo" else 48))
        )
        self.baseplate_width = (
            self.specs["xy_factor"] * baseplate_width 
            if baseplate_width is not None
            else (self.specs["xy_factor"] * (24 if brick_system == "duplo" else 48))
        )
        self.baseplate_center_x = (
            self.specs["xy_factor"] * baseplate_center_x
            if baseplate_center_x is not None
            else (self.specs["xy_factor"] * 0)
        )
        self.baseplate_center_y = (
            self.specs["xy_factor"] * baseplate_center_y
            if baseplate_center_y is not None
            else (self.specs["xy_factor"] * 0)
        )
        self.height = self.specs["baseplate_height"] * self.specs["xy_factor"]
        self.lower_left_x = self.baseplate_center_x - self.baseplate_width * 0.5
        self.lower_left_y = self.baseplate_center_y - self.baseplate_length * 0.5
        # Keep to make baseplate a child of rectangularbrick later
        self.lower_left_z = -0.15

        self.generate()

    def generate(self):
        # add baseplate to OccupancyGrid?
        # 1: extrude baseplate from shape
        baseplate_linepath_z = [vec(0, 0, self.lower_left_z * self.specs["xy_factor"]), 
                                vec(0, 0, 0)
        ]
        baseplate_shape = shapes.rectangle(
            pos=[self.baseplate_center_x, self.baseplate_center_y],
            width = self.baseplate_width,
            height = self.baseplate_length,
            roundness = self.specs["baseplate_roundness"]
        )
        baseplate_extrusion = extrusion(
            shape = baseplate_shape,
            path = baseplate_linepath_z,
            color = self.brick_color
        )
        baseplate_compound = [baseplate_extrusion]

        # 2: add studs
        # duplo: corner-studs do not exist on baseplate
        # duplo: baseplate studs are massive, not hollow
        for x_stud in (range(int(self.stud_x_counter))):
            for y_stud in (range(int(self.stud_y_counter))):
                if (self.brick_system == "duplo" and 
                    (x_stud == 0 or x_stud == int(self.stud_x_counter)-1) and 
                    (y_stud == 0 or y_stud == int(self.stud_y_counter)-1)):
                    pass
                else:
                    stud_center = vec(
                        self.lower_left_x + self.specs["stud_xy_offset"] + (x_stud * self.specs["stud_spacing"]),
                        self.lower_left_y + self.specs["stud_xy_offset"] + (y_stud * self.specs["stud_spacing"]),
                        self.lower_left_z + self.height)

                    stud = self.generate_stud(
                        pos = stud_center,
                        hollow = False,
                        wall_thickness = self.specs["stud_wall_thickness"]
                    )

                    baseplate_compound.append(stud)

        return compound(baseplate_compound)


class RectangularBrick(BasicBrick):
    def __init__(self, brick_system: str, length: int, width: int, height: int, 
                 x: int, y: int, z: int, 
                 brick_color: vector,
                 orientation: vector):
        """Rectangular Brick __init__

        Generates a 3d-object of a rectangular brick with specified options.
        Is usually called from scene.

        Args:
            brick_system (str): received from super; handed over from BrickProject
            length (int, optional): Brick length (x-axis). Defaults to 4.
            width (int, optional): Brick width (y-axis). Defaults to 2.
            height (int, optional): Brick height (z-axis). Defaults to 1.
            x (int, optional): X-Position of front left corner of brick. Defaults to 0.
            y (int, optional): Y-Position of front left corner of brick. Defaults to 0.
            z (int, optional): Z-Position of front left corner of brick. Defaults to 0.
            brick_color (vector or vpython color, optional): vector(R, G, B) or color.name (from vpython std). Defaults to color.red.
            orientation (vector): user input to determine the orientation of the brick, use NORTH, EAST, SOUTH, WEST
        """
        super().__init__(brick_system)
        self.stud_x_counter = width # x-axis in NORTH orientation (0,1,0)
        self.stud_y_counter = length # y-axis in NORTH orientation
        self.length = length * self.specs["xy_factor"]
        self.width = width * self.specs["xy_factor"]
        self.height = height * self.specs["z_factor"]
        self.x = x * self.specs["xy_factor"]
        self.y = y * self.specs["xy_factor"]
        self.z = z * self.specs["z_factor"]
        self.brick_color = brick_color
        self.orientation = orientation

        self.generate()

    def generate(self):
        """Generate / render brick, is called from __init__ with self (Brick-object)

        Generates a box (obj::vpython) first, then calculates stud center and calls generate_stud n times (row x column)
        to be added to the final compound

        Returns:
            compound (obj::vpython): 3d compound representing the rendered brick
        """
        if GLOBAL_DEBUG and (STUD_DEBUG or BRICK_DEBUG): 
            print(f"Generating 3d-brick:\n-------------------\nX: {self.x}, Y: {self.y}, Z: {self.z}")
            print(f'length: {self.length}, width: {self.width}, height: {self.height}')
            print(f"stud-x-counter: {self.stud_x_counter}, stud-y-counter: {self.stud_y_counter}")
        
        # 1. create box in standard orientation (North)
        #### this is important for irregular boxes where North ≠ South
        #### NOTICE: vpython compounds ALWAYS end up with:
        #### axis = (x,0,0) and up = (0,y,0) with unclear dimensions, 
        #### although they don't matter.
        #### This does affect the length, width, height info:
        #### 
        brick_basis = box(
            pos = vec(
                self.x + self.width/2, 
                self.y + self.length/2, 
                self.z + self.height/2
            ),
            axis = vector(0,1,0), # follows length
            length = self.length,
            height = self.height,
            width = self.width,
            color = self.brick_color,
            up = vector(0,0,1)
        )

        if GLOBAL_DEBUG and BRICK_DEBUG: 
            print(f"Box generated with:\n-------------------\npos: {brick_basis.pos}\nand l,w,h: {brick_basis.length}, {brick_basis.width}, {brick_basis.height}")
            print(f"Self remains with: x,y,z: {self.x}, {self.y}, {self.z}; stud-spacing: {self.specs["stud_spacing"]}, first stud x: {self.x + self.specs["stud_xy_offset"] + (0 * self.specs["stud_spacing"])}")
            if STOP_DEBUG: temp_in = input("Weiter.")

        brick_components = [brick_basis]

        if GLOBAL_DEBUG and BRICK_DEBUG:
            brick_length = curve(pos=[vec(0, self.y, 0), vec(0, self.length, 0)], color=color.yellow)
            brick_width = curve(pos=[vec(self.x, 0, 0), vec(self.width, 0, 0)], color=color.yellow)
            brick_height = curve(pos=[vec(0, 0, self.z), vec(0, 0, self.height)], color=color.yellow)
            brick_x_text = label(pos=vec(self.width/2, -5, 5), text='width', xoffset=-1, yoffset= 2, space= 2, height= 16, border=4, font='sans', background = color.white, color = color.black)
            brick_y_text = label(pos=vec(-5, self.length/2, 5), text='length', xoffset=-1, yoffset= 2, space= 2, height= 16, border=4, font='sans', background = color.white, color = color.black)
            brick_z_text = label(pos=vec(-5, 5, self.height/2), text='height', xoffset=-1, yoffset= 2, space= 2, height= 16, border=4, font='sans', background = color.white, color = color.black)
            brick_components.append(brick_length)
            brick_components.append(brick_x_text)
            brick_components.append(brick_width)
            brick_components.append(brick_y_text)
            brick_components.append(brick_height)
            brick_components.append(brick_z_text)

        for x_stud in range(int(self.stud_x_counter)):
            for y_stud in range(0, int(self.stud_y_counter)):
                stud_center = vec(
                    self.x + self.specs["stud_xy_offset"] + (x_stud * self.specs["stud_spacing"]),
                    self.y + self.specs["stud_xy_offset"] + (y_stud * self.specs["stud_spacing"]),
                    self.z + self.height
                )
                stud = self.generate_stud(
                    pos = stud_center,
                    hollow = self.specs["is_hollow"],
                    wall_thickness = self.specs["stud_wall_thickness"]
                )
                brick_components.append(stud)

        brick_compound = compound(brick_components)#, axis = NORTH, up = vector(0,0,1))

        print(brick_compound)

        if GLOBAL_DEBUG and BRICK_DEBUG: 
            print(f"Compound generated with:\n--------------------\npos: {brick_compound.pos} and l,w,h: {brick_compound.length}, {brick_compound.width}, {brick_compound.height}")
            print(f"--- axis: {brick_compound.axis}, up-vector: {brick_compound.up}")
        stops = input("Weiter?")
        # 3. Rotate box according to orientation
        if GLOBAL_DEBUG and BRICK_DEBUG: print(f"Rotating brick at center point: {brick_compound.pos}")
        brick_compound.rotate(angle = self.orientation.rotation, axis = vector(0,0,1))

        if STOP_DEBUG: stops = input("Weiter?")

        # 4. move box

        if GLOBAL_DEBUG and BRICK_DEBUG:
            print(f"Moving box with x, y, z: {self.x}, {self.y}, {self.z} and l,w,h: {brick_compound.length}, {brick_compound.width}, {brick_compound.height}")
            print(f"--- axis: {brick_compound.axis}, up-vector: {brick_compound.up}")
        if self.orientation == NORTH:
            brick_compound.pos = vector(
                self.x + brick_compound.width / 2,
                self.y + brick_compound.length / 2,
                self.z + brick_compound.height / 2
            )
        elif self.orientation == EAST:
            brick_compound.pos = vector(
                self.x + brick_compound.width / 2,
                self.y + brick_compound.length / 2,
                self.z + brick_compound.height / 2
            )
        elif self.orientation == SOUTH:
            brick_compound.pos = vector(
                self.x + brick_compound.width / 2,
                self.y + brick_compound.length / 2,
                self.z + brick_compound.height / 2
            )
        elif self.orientation == WEST:
            brick_compound.pos = vector(
                self.x + brick_compound.width / 2,
                self.y + brick_compound.length / 2,
                self.z + brick_compound.height / 2
            )

        return brick_compound

my_project = BrickProject("duplo")
my_project.add_scene()
my_project.brick_scenes[0].add_baseplate(color.green * 0.4, 16, 20)

# def hello_world():
#     my_project.brick_scenes[0].add_brick(
#         "rect", 8, 1, 1, -5, -2, 0, color.black, EAST
#     )
#     my_project.brick_scenes[0].add_brick(
#         "rect", 8, 1, 1, -2, -2, 0, color.black, EAST 
#     )
#     my_project.brick_scenes[0].add_brick(
    #     "rect", 2, 1, 1, -4, 1, 0, color.black 
    # )
    # my_project.brick_scenes[0].add_brick(
    #     "rect", 1, 8, 1, 0, -2, 0, color.black 
    # )
    # my_project.brick_scenes[0].add_brick(
    #     "rect", 1, 6, 1, 2, 0, 0, color.black 
    # )
    # my_project.brick_scenes[0].add_brick(
    #     "rect", 1, 1, 1, 2, -2, 0, color.black 
    # )
    # my_project.brick_scenes[0].add_brick(
    #     "rect", 8, 1, 1, -5, -4, 0, color.red 
    # )
    # my_project.brick_scenes[0].add_brick(
    #     "rect", 8, 1, 1, -5, -5, 0, color.yellow 
    # )
    # my_project.brick_scenes[0].add_brick(
    #     "rect", 8, 1, 1, -5, -6, 0, color.blue 
    # )

# hello_world()

# my_project.brick_scenes[0].add_brick(
#         "rect", 8, 2, 1, 0, 0, 0, color.black, NORTH
# )

my_project.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 0, 0, 0, color.blue, EAST
)

x_marker = curve(pos=[vec(-15 * 9.6, 0, 0.5), vec(15 * 9.6, 0, 0.5)], color=color.yellow)
y_marker = curve(pos=[vec(0, -15 * 9.6, 0.5), vec(0, 15 * 9.6, 0.5)], color=color.blue)
z_marker = curve(pos=[vec(0, 0, -15 * 9.6), vec(0, 0, 15 * 9.6)], color=color.red)
x_text = label(pos=vec(-8 * 9.6, 0, 0.5), text='x-axis', xoffset=-1 * 9.6, yoffset= 2 * 9.6, space= 3, height= 16, border=4, font='sans', background = color.white, color = color.black)
y_text = label(pos=vec(0, -8 * 9.6, 0.5), text='y-axis', xoffset=-1 * 9.6, yoffset= 2 * 9.6, space= 3, height= 16, border=4, font='sans', background = color.white, color = color.black)


my_project.brick_scenes[0].bricks.append(x_marker)
my_project.brick_scenes[0].bricks.append(y_marker)
