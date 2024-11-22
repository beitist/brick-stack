#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# lego and duplo are trademarks of their respective owners!

from vpython import *
import random

# Debug options
# GLOBAL = Turn on/off all debug options
GLOBAL_DEBUG = True

# Turn on/off desired debug output
CALC_DEBUG = True
STUD_DEBUG = False
GRID_DEBUG = False
BRICK_DEBUG = False

##### COORDINATES #####
## x = length from left to right (standard camera view)
## y = width from front to back (standard camera view)
## z = height from bottom to top (standard camera view)
## coordinates x, y, z correspond with l, w, h values
#######################


####### TO DO ########
## 0: close scenes? update cameras?
## 1: Auto_Camera, auto_scene
## 2: render to file
## 3: read simple scene files
## 4: create booklet
## 5: encapsulation ok? CameraManager?


####### NOTES #########
## update camera better from BrickProject? ##

class BrickProject:
    """Class holding individuel scenes (= steps in constructing a brick project)
    
    Will (soon) provide functionality for file handling of simplified project files"""
    # v0.1c / 17.11.24 / beiti
    # planned use:
    # - load project file?
    # - save renders?
    #
    #
    # description
    # type = duplo/lego
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
        # Für jeden Punkt, den der Stein belegt
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
            # z_start_end = self.points[z_summary_of_coordinate]
            
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

        print(results)

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
    and provides camera and scene settings
    """
    # v0.1 / 17.11.24 / beiti
    # planned use:
    # hold individual scenes consisting of multiple bricks + optional camera / render / view setting
    # render full scene, possibly some more options
    #
    # to do:
    # - camera object
    # - camera calculation
    # - special scenes

    # Parameter description:
    # special_camera = camera object for manual positioning of camera for scene
    # special_scene = scene details (width, height, ...) -> new obect?
    # brick_scene inherits type and project
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

    def add_baseplate(self, baseplate_color = color.green, baseplate_custom_length = None, baseplate_custom_width = None, baseplate_custom_x = None, baseplate_custom_y = None):
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
       # Finde kleinstes mögliches z
        z = self.grid.get_next_z(x_pos, y_pos, length, width)
        # Runde auf nächste valide Höhe
        if self.brick_system == "duplo":
            # Runde auf Vielfaches von 0.5 (oder 3 in deinem System)
            if GLOBAL_DEBUG and (BRICK_DEBUG or GRID_DEBUG): print(f"z before rounding: {z}")
            z = ceil(z * 2) / 2
        else:  # lego
            # Runde auf Vielfaches von 1/3
            z = ceil(z * 3) / 3
        return z
    
    def calculate_xyz_range(self):
        xyz_range = self.grid.get_xyz_range(self)       

    def add_brick(self, brick_type, length, width, height, x_pos, y_pos, z_pos, brick_color):
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
                                          brick_color)
        
        self.bricks.append(brick)

        # add math model of brick to occupancy grid (for z-calculation)
        self.grid.add_brick(x_pos, y_pos, z_pos, length, width, height)

        # update camera view
        self.update_camera_position()

    def get_my_scene_index(self):
        return self.project.get_scene_index(self)

class BrickFactory:
    # v0.1 / 16.11.24 / beiti
    # generates bricks for scenes
    
    # space for many types of bricks
    # needs failover if type is not implemented
    @staticmethod
    def create_brick(brick_system, brick_type, length, width, height, x_pos, y_pos, z_pos, brick_color):
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
                                     final_brick_color)
        else:
            brick = RectangularBrick(brick_system,
                                     length, 
                                     width, 
                                     height, 
                                     x_pos,
                                     y_pos, 
                                     z_pos, 
                                     final_brick_color)

        return brick  

    @staticmethod
    def choose_random_color():
        """Randomize brick color

        Returns:
            vector: RGB-vector for use with vpython
        """
        random.seed()
        red = random.randint(0, 10) / 10
        green = random.randint(0, 10) / 10
        blue = random.randint(0, 10) / 10

        return vector(red, green, blue)

    @staticmethod
    def create_baseplate(brick_system, baseplate_color, baseplate_custom_length, baseplate_custom_width, baseplate_custom_x, baseplate_custom_y):
        # custom_x/y: center (standard: 0,0)
        specs = BasicBrick.BRICK_SPECS[brick_system]
        length = (
            specs["xy_factor"] * baseplate_custom_length
            if baseplate_custom_length is not None
            else (specs["xy_factor"] * (24 if brick_system == "duplo" else 48))
        )
        width = (
            specs["xy_factor"] * baseplate_custom_width 
            if baseplate_custom_width is not None
            else (specs["xy_factor"] * (24 if brick_system == "duplo" else 48))
        )
        custom_x = (
            specs["xy_factor"] * baseplate_custom_x
            if baseplate_custom_x is not None
            else (specs["xy_factor"] * 0)
        )
        custom_y = (
            specs["xy_factor"] * baseplate_custom_y
            if baseplate_custom_y is not None
            else (specs["xy_factor"] * 0)
        )

        if GLOBAL_DEBUG and CALC_DEBUG: print(f"Baseplate values: x: {custom_x}, y: {custom_y}, width: {width}, length: {length}")

        baseplate_linepath_z = [vec(0,0,0), 
                                vec(0, 0, -0.15 * specs["xy_factor"])
        ]

        baseplate_shape = shapes.rectangle(
            pos=[custom_x, custom_y],
            width = width,
            height = length,
        )

        baseplate_extrusion = extrusion(
            shape = baseplate_shape,
            path = baseplate_linepath_z,
            color = baseplate_color
        )

        return baseplate_extrusion


        # steps: 
        # 1. create rectangle (rt = shapes.rectangle(width, height, roundness=0.1?))
        # 2. extrusion_line_path = [ vec(0,0,0), vec(0,0,-0.1)]
        # 3. rect = extrusion( shape = rt, path = extrusion_line_path)
        # 4. put into compound
        # 5. call generate stud for all rows (except corners for duplo)
        # 6. add compound to scene

class BasicBrick:
    """Parent class for all bricks containing general information and a testing format
    """
    # v0.1 / 11.11.24 / beiti
    #
    # PARAMETER:
    # ==========
    # brick_system = lego/duplo
    # color = VPython color code
    #
    # SPECS:
    # ======
    # generic lego/duplo for all bricks, in mm

    BRICK_SPECS = {
        "lego": {
            "xy_factor": 7.8,
            "z_factor": 9.6,
            "stud_diameter": 4.8,
            "stud_height": 1.8,
            "stud_xy_offset": 3.9,
            "stud_spacing": 7.8,
            "stud_wall_thickness": 0,
            "is_hollow": False
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
            "is_hollow": True           
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

    brick_system = None
        
    def __init__(self, brick_system):
        """Parent brick class __init__

        is called as super from child bricks

        Args:
            brick_system (str): "lego", "duplo" or "test"; called as super from specific brick; handed over from BrickProject
        """
        self.brick_system = brick_system
        self.specs = self.BRICK_SPECS[brick_system]

class RectangularBrick(BasicBrick):
    # v0.2a / 17.11.24 / beiti
    #
    # PARAMETER:
    # ==========
    # length, width, height = int
    # x, y, z = int
    # color = VPython Farbcode
    # type = lego/duplo
    # x = width
    # y = length
    #
    #
    # TO DO: 
    #   - Unterseite vom Stein modellieren
    #   - Farbcodes offener wählen, um Render-Engine flexibel zu halten
    #   - Scene-Standardwerte an Klasse übergeben, sofern vorhanden
    #   - Sonderformen definieren
    #   - separate brick-objects from brick-renders (?)

    def __init__(self, brick_system, length=4, width=2, height=1, x=0, y=0, z=0, brick_color=color.red):
        """Rectangular Brick __init__

        Generates a 3d-object of a rectangular brick with specified options.

        Args:
            brick_system (str): received from super; handed over from BrickProject
            length (int, optional): Brick length (x-axis). Defaults to 4.
            width (int, optional): Brick width (y-axis). Defaults to 2.
            height (int, optional): Brick height (z-axis). Defaults to 1.
            x (int, optional): X-Position of front left corner of brick. Defaults to 0.
            y (int, optional): Y-Position of front left corner of brick. Defaults to 0.
            z (int, optional): Z-Position of front left corner of brick. Defaults to 0.
            brick_color (vector or vpython color, optional): vector(R, G, B) or color.name (from vpython std). Defaults to color.red.
        """
        super().__init__(brick_system)
        self.stud_x_counter = length
        self.stud_y_counter = width
        self.length = length * self.specs["xy_factor"]
        self.width = width * self.specs["xy_factor"]
        self.height = height * self.specs["z_factor"]
        self.x = x * self.specs["xy_factor"]
        self.y = y * self.specs["xy_factor"]
        self.z = z * self.specs["z_factor"]

        self.color=brick_color

        self.generate()

    def generate(self):
        """Generate / render brick, is called from __init__ with self (Brick-object)

        Generates a box (obj::vpython) first, then calculates stud center and calls generate_stud n times (row x column)
        to be added to the final compound

        Returns:
            compound (obj::vpython): 3d compound representing the rendered brick
        """
        if GLOBAL_DEBUG and (STUD_DEBUG or BRICK_DEBUG): 
            print(f"Generating 3d-brick:\nX: {self.x}, Y: {self.y}, Z: {self.z}")
            print(f'length: {self.length}, width: {self.width}, height: {self.height}')
            print(f"stud-x-counter: {self.stud_x_counter}, stud-y-counter: {self.stud_y_counter}")
        
        brick_basis = box(
            pos = vec(
                self.x + self.length/2, 
                self.y + self.width/2, 
                self.z + self.height/2
            ),
            axis = vector(1,0,0),
            length = self.length,
            height = self.height,
            width = self.width,
            color = self.color,
            up = vector(0,0,1)
        )

        brickComponents = [brick_basis]
        for x_stud in range(int(self.stud_x_counter)):
            for y_stud in range(0, int(self.stud_y_counter)):

                if GLOBAL_DEBUG and STUD_DEBUG:
                    brick_center_x = self.x + self.length/2
                    brick_center_y = self.y + self.width/2     
                    
                    stud_x = self.x + self.specs["stud_xy_offset"] + (x_stud * self.specs["stud_spacing"])
                    stud_y = self.y + self.specs["stud_xy_offset"] + (y_stud * self.specs["stud_spacing"])
                    
                    print("Checking stud position in generate-call (3d)")
                    print(f"Brick center: ({brick_center_x}, {brick_center_y})")
                    print(f"Stud position: ({stud_x}, {stud_y})")

                stud_center = vec(
                    self.x + self.specs["stud_xy_offset"] + (x_stud * self.specs["stud_spacing"]),
                    self.y + self.specs["stud_xy_offset"] + (y_stud * self.specs["stud_spacing"]),
                    self.z + self.height)

                stud = self.generate_stud(
                    pos = stud_center,
                    hollow = self.specs["is_hollow"],
                    wall_thickness = self.specs["stud_wall_thickness"]
                )

                brickComponents.append(stud)

        return compound(brickComponents)

    def generate_stud(self, pos, hollow=False, wall_thickness=0):
        """3d-function to generate and render individual studs for compound

        Distinguishes between brick_systems (lego, duplo) to render 

        Args:
            pos (vector): center point of stud basis
            hollow (bool, optional): Make hollow studs (or not). Defaults to False.
            wall_thickness (int, optional): Stud wall thickness; see BRICK_SPECS. Defaults to 0.

        Returns:
            cylinder or extrusion (obj::vpython): returns a cylinder or an extruded circle (hollow cylinder) representing one stud
        """
        if not hollow:
            generated_stud = cylinder(
                pos=pos,
                radius=self.specs["stud_diameter"] / 2,
                axis=vec(0.0, 0.0, self.specs["stud_height"]),
                color=self.color
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
                color = self.color
            )

        return generated_stud

schiff = BrickProject("duplo")

schiff.add_scene()

schiff.brick_scenes[0].add_baseplate()

schiff.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 0, 0, 0, color.cyan
)

schiff.brick_scenes[0].add_brick(
    "rect", 4, 2, 1, 4, 0, 0, "random"
)

## EXAMPLES ##

## Build a tower with h=5
for x in range(0,5):
    schiff.brick_scenes[0].add_brick(
        "rect", 4, 2, 1, 5, 7, 0, "random"
    )
    schiff.brick_scenes[0].add_brick(
        "rect", 4, 2, 1, 5, 9, 0, "random"
    )

## Build a stairway with h=10
for x in range(0, 10):
    schiff.brick_scenes[0].add_brick(
        "rect", 4, 2, 1, 11 + x, 4, 0, "random"
    )

# end