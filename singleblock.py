#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vpython import *

# Scene mit  Standardwerten
scene = canvas(
    width=800,            # Fensterbreite
    height=600,           # Fensterhöhe
    center=vector(0,0,0), # Mittelpunkt der Scene
    background=color.cyan,  # Hellgrauer Hintergrund
    up=vector(0,0,1)     # Z ist "oben"
)

# Kamera mittig von oben/vorne
scene.camera.pos = vector(0,-40,30)    # Y negativ = von vorne, Z positiv = von oben
scene.camera.axis = vector(0,40,-20)   # Schaut nach hinten und leicht nach unten

# Hilfslinien zum Verstehen der Achsen
curve(pos=[vector(0,0,0), vector(10,0,0)], color=color.red)    # X-Achse
curve(pos=[vector(0,0,0), vector(0,10,0)], color=color.green)  # Y-Achse
curve(pos=[vector(0,0,0), vector(0,0,10)], color=color.blue)   # Z-Achse

class LegoBrick:
    # v0.2 / 3.11.24 / beiti
    #
    # PARAMETER:
    # ==========
    # length, width, height = int
    # x, y, z = int
    # color = VPython Farbcode
    # type = lego/duplo
    #
    # Alle Endangaben in Millimetern
    #
    # TO DO: 
    #   - Unterseite vom Stein modellieren
    #   - Farbcodes offener wählen, um Render-Engine flexibel zu halten
    #   - Scene-Standardwerte an Klasse übergeben, sofern vorhanden
    #   - Sonderformen definieren
    # mm-Faktoren für Lego und Duplo

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
        "duplo": {
            "xy_factor": 15.6,
            "z_factor": 19.2,
            "stud_diameter": 8.6,
            "stud_height": 3.6,
            "stud_xy_offset": 7.8,
            "stud_spacing": 16,
            "stud_wall_thickness": 2.2,
            "is_hollow": True           
        }
    }

    def __init__(self, length=4, width=2, height=1, x=0, y=0, z=0, color=color.red, type="lego"):
        self.type=type
        self.specs = self.BRICK_SPECS[self.type]

        self.spalten = width
        self.reihen = length

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
        legoBasis = box(
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

        brickComponents = [legoBasis]
        for i in range(int(self.reihen)):
            for j in range(int(self.spalten)):
                mitteStud = vec(
                    self.x + self.specs["stud_xy_offset"] + (i * self.specs["stud_spacing"]),
                    self.y + self.specs["stud_xy_offset"] + (j * self.specs["stud_spacing"]),
                    self.z + self.height)

                stud = self.generate_stud(
                    pos = mitteStud,
                    hollow = self.specs["is_hollow"],
                    wall_thickness = self.specs["stud_wall_thickness"]
                )

                brickComponents.append(stud)

        return compound(brickComponents)

brick1 = LegoBrick(2, 8, 1, 0, 0, 0, color.yellow, "duplo")
# brick2 = LegoBrick(2, 8, 1, 6, 0, 0, color.yellow, "duplo")
brick3 = LegoBrick(2, 4, 1, 2, 0, 0, color.red, "duplo")
brick4 = LegoBrick(4, 2, 1, 1, 0, 1, color.blue, "duplo")
brick5 = LegoBrick(4, 2, 1, 1, 2, 1, color.green, "duplo")
brick6 = LegoBrick(2, 4, 1, -2, 0, 0, color.red, "duplo")
brick7 = LegoBrick(2, 8, 1, -1, 0, 1,color.yellow, "duplo")
brick8 = LegoBrick(2, 4, 1, 0, 0, 2, color.red, "duplo")
