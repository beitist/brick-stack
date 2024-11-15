#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vpython import *

# Hilfslinien zum Verstehen der Achsen
# curve(pos=[vector(0,0,0), vector(10,0,0)], color=color.red)    # X-Achse
# curve(pos=[vector(0,0,0), vector(0,10,0)], color=color.green)  # Y-Achse
# curve(pos=[vector(0,0,0), vector(0,0,10)], color=color.blue)   # Z-Achse

class BrickProject:
    # v0.1 / 11.11.24 / beiti
    # planned use:
    # - load project file
    # - save renders?
    #
    # so far implemented:
    # - define brick type, hold BrickScenes
    
    def __init__(self, type):
        self.brick_scenes = []
        self.type = type

    def add_scene(self, special_canvas=None, special_camera=None):
        brick_scene = BrickScene(self.type, special_canvas, special_camera)
        self.brick_scenes.append(brick_scene)

class BrickScene:
    # v0.1 / 11.11.24 / beiti
    # planned use:
    # hold individual scenes consisting of multiple bricks + optional camera / render / view setting
    # render full scene, possibly some more options
    #
    # to do:
    # - camera object
    # - camera calculation
    # - special scenes
    # 

    # Parameter description:
    # special_camera = camera object for manual positioning of camera for scene
    # special_scene = scene details (width, height, ...) -> new obect?
    def __init__(self, type, special_scene=None, special_camera=None):
        self.bricks = []
        self.type = type
        self.scene = None
        self.scene = self.set_scene(special_scene, special_camera)

    def set_scene(self, special_scene=None, special_camera=None):
        # Scene with std values
        # special scene/camera not yet implemented

        self.scene = canvas(
            width=800,            # window width
            height=600,           # window height
            center=vector(0,0,0), # Scene center
            background=color.cyan,  # bg color
            up=vector(0,0,1)     # Z is "up"
        )

        # Kamera mittig von oben/vorne
        self.scene.camera.pos = vector(0,-40,30)    # Y negativ = von vorne, Z positiv = von oben
        self.scene.camera.axis = vector(0,40,-20)   # Schaut nach hinten und leicht nach unten

    ##### HIER KÖNNTE MAN über ADDBRICK die Klasse Init starten anstatt brick separat dann
    ##### kann auch type besser übergeben werden. So wie oben bei Scene aus Project
    def add_brick(self, brick):
        brick =
        self.bricks.append(brick)

class BasicBrick:
    # v0.1 / 11.11.24 / beiti
    #
    # PARAMETER:
    # ==========
    # type = lego/duplo
    # color = VPython color code
    #
    # SPECS:
    # ======
    # generic lego/duplo for all bricks, in mm
    # calculate z

    BRICK_SPECS = {
        "lego": {
            "xy_factor": 7.8,
            "z_factor": 9.6,
            "stud_diameter": 4.8,
            "stud_height": 1.8,
            "stud_xy_offset": 3.9,
            "stud_spacing": 8,
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
            "stud_spacing": 16,
            "stud_wall_thickness": 2.2,
            "is_hollow": True           
        }
    }
        
    def __init__(self, type):
        self.type = type
        self.specs = self.BRICK_SPECS[type]

class RectangularBrick(BasicBrick):
    # v0.2 / 3.11.24 / beiti
    #
    # changes: inheritance, rename
    #
    # PARAMETER:
    # ==========
    # length, width, height = int
    # x, y, z = int
    # color = VPython Farbcode
    # type = lego/duplo
    #
    #
    # TO DO: 
    #   - Unterseite vom Stein modellieren
    #   - Farbcodes offener wählen, um Render-Engine flexibel zu halten
    #   - Scene-Standardwerte an Klasse übergeben, sofern vorhanden
    #   - Sonderformen definieren
    #   - separate brick-objects from brick-renders (?)



    def __init__(self, length=4, width=2, height=1, x=0, y=0, z=0, color=color.red):
        super().__init__(type)
        self.columns = width
        self.rows = length

        self.length = length * self.specs["xy_factor"]
        self.width = width * self.specs["xy_factor"]
        self.height = height * self.specs["z_factor"]
        self.x = x * self.specs["xy_factor"]
        self.y = y * self.specs["xy_factor"]
        self.z = z * self.specs["z_factor"]
       
        self.color=color
        self.generate()

    def generate_stud(self, pos, hollow=False, wall_thickness=0):
        if not hollow:
            return cylinder(
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

            cyl_extruded = extrusion(
                shape = cyl_base, 
                path = cyl_path, 
                color = self.color
            )

            return cyl_extruded

    def generate(self):
        brick_basis = box(
            pos = vec(
                self.x + self.length/2, 
                self.y + self.width/2, 
                self.z + self.height/2
            ),
            length = self.length,
            height = self.height,
            width = self.width,
            color = self.color,
            up = vector(0,0,1))

        brickComponents = [brick_basis]
        for i in range(int(self.rows)):
            for j in range(int(self.columns)):
                stud_center = vec(
                    self.x + self.specs["stud_xy_offset"] + (i * self.specs["stud_spacing"]),
                    self.y + self.specs["stud_xy_offset"] + (j * self.specs["stud_spacing"]),
                    self.z + self.height)

                stud = self.generate_stud(
                    pos = stud_center,
                    hollow = self.specs["is_hollow"],
                    wall_thickness = self.specs["stud_wall_thickness"]
                )

                brickComponents.append(stud)

        return compound(brickComponents)

schiff = BrickProject("duplo")

schiff.add_scene()

schiff.brick_scenes[0].add_brick(
    RectangularBrick(2, 8, 1, 0, 0, 0, color.yellow)
)

schiff.brick_scenes[0].add_brick(
    RectangularBrick(2, 8, 1, 4, 0, 0, color.yellow)
)

