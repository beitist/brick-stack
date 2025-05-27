#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Haus im römischen Verbund - Testcase
Baut ein 10x10 Haus aus 4x2 Steinen in 6 Reihen mit versetztem Mauermuster
"""

from brickstack_simple import *

def build_roman_bond_house():
    """
    Baut ein Haus im römischen Verbund mit 4x2 Steinen.
    
    Layout:
    - 10x10 Grundfläche
    - 6 Reihen hoch
    - Römischer Verbund (jede 2. Reihe um 2 Einheiten versetzt)
    - 4x2 Steine in NSEW Orientierung
    """
    print("Building Roman Bond House...")
    print("=" * 40)
    
    # Projekt erstellen
    project = BrickProject("duplo", auto_z=True)
    scene = project.add_scene()
    
    # Baseplate (etwas größer für Stabilität)
    print("Adding baseplate...")
    scene.add_baseplate(color.green * 0.4, 14, 14)
    
    # Haus-Parameter
    house_width = 10    # Einheiten breit
    house_depth = 10    # Einheiten tief  
    house_height = 6    # Reihen hoch
    brick_length = 4    # 4x2 Steine
    brick_width = 2
    
    # Verschiedene Farben für bessere Sichtbarkeit
    colors = [color.red, color.blue, color.yellow, color.orange, color.purple, color.cyan]
    
    print(f"Building {house_width}x{house_depth} house, {house_height} rows high")
    
    # Für jede Reihe
    for row in range(house_height):
        current_color = colors[row % len(colors)]
        print(f"\nBuilding row {row + 1}/6 with color {current_color}...")
        
        # Bestimme Versatz für römischen Verbund
        if row % 2 == 0:
            # Ungerade Reihen (1,3,5): Kein Versatz
            offset_x = 0
            offset_y = 0
            print(f"  Row {row + 1}: Standard layout (no offset)")
        else:
            # Gerade Reihen (2,4,6): Kleinerer Versatz (nur 1 Einheit für echten Verbund)
            offset_x = 1
            offset_y = 1  
            print(f"  Row {row + 1}: Offset layout (+1,+1)")
        
        # Baue die 4 Wände des Hauses
        build_house_walls(scene, row, offset_x, offset_y, current_color, 
                         house_width, house_depth, brick_length, brick_width)
        
        # Zeige Grid-Status nach jeder Reihe
        scene.print_grid_status(f"After Row {row + 1}/6")
    
    # Koordinatenreferenz hinzufügen
    add_coordinate_markers(scene)
    
    print(f"\n🏠 Roman Bond House completed!")
    print(f"   - {house_width}x{house_depth} foundation")
    print(f"   - {house_height} rows high") 
    print(f"   - Roman bond pattern for stability")
    print(f"   - Built with {brick_length}x{brick_width} bricks")
    
    return project

def build_house_walls(scene, row, offset_x, offset_y, brick_color, 
                     house_width, house_depth, brick_length, brick_width):
    """
    Baut die 4 Wände des Hauses für eine Reihe.
    
    Args:
        scene: BrickScene Objekt
        row: Aktuelle Reihe (0-basiert)
        offset_x, offset_y: Versatz für römischen Verbund
        brick_color: Farbe der Steine
        house_width, house_depth: Haus-Dimensionen
        brick_length, brick_width: Stein-Dimensionen
    """
    
    # NORDWAND (oben, Y=house_depth-brick_width)
    print(f"    Building North wall...")
    y_north = (house_depth - brick_width) + offset_y
    for x in range(0, house_width - brick_length + 1, brick_length):
        x_pos = x + offset_x
        if x_pos + brick_length <= house_width:  # Prüfe Grenzen
            scene.add_brick(
                length=brick_length, width=brick_width, height=1,
                x_pos=x_pos, y_pos=y_north, 
                brick_color=brick_color, orientation=NORTH
            )
    
    # SÜDWAND (unten, Y=0)  
    print(f"    Building South wall...")
    y_south = 0 + offset_y
    for x in range(0, house_width - brick_length + 1, brick_length):
        x_pos = x + offset_x
        if x_pos + brick_length <= house_width:  # Prüfe Grenzen
            scene.add_brick(
                length=brick_length, width=brick_width, height=1,
                x_pos=x_pos, y_pos=y_south,
                brick_color=brick_color, orientation=NORTH
            )
    
    # OSTWAND (rechts, X=house_width-brick_width)
    print(f"    Building East wall...")
    x_east = (house_width - brick_width) + offset_x  
    for y in range(brick_width, house_depth - brick_width - brick_length + 1, brick_length):
        y_pos = y + offset_y
        if y_pos + brick_length <= house_depth - brick_width:  # Prüfe Grenzen, vermeide Überlappung
            scene.add_brick(
                length=brick_length, width=brick_width, height=1,
                x_pos=x_east, y_pos=y_pos,
                brick_color=brick_color, orientation=EAST
            )
    
    # WESTWAND (links, X=0)
    print(f"    Building West wall...")
    x_west = 0 + offset_x
    for y in range(brick_width, house_depth - brick_width - brick_length + 1, brick_length):
        y_pos = y + offset_y  
        if y_pos + brick_length <= house_depth - brick_width:  # Prüfe Grenzen, vermeide Überlappung
            scene.add_brick(
                length=brick_length, width=brick_width, height=1,
                x_pos=x_west, y_pos=y_pos,
                brick_color=brick_color, orientation=WEST
            )

def add_coordinate_markers(scene):
    """Fügt Koordinatenreferenz-Linien hinzu."""
    print("Adding coordinate reference markers...")
    
    # X-Achse (rot)
    x_line = curve(pos=[vec(-20, 0, 1), vec(200, 0, 1)], color=color.red)
    
    # Y-Achse (grün)  
    y_line = curve(pos=[vec(0, -20, 1), vec(0, 200, 1)], color=color.green)
    
    # Labels
    x_label = label(pos=vec(180, -10, 5), text='X-axis', color=color.red, 
                   height=16, border=4, background=color.white)
    y_label = label(pos=vec(-10, 180, 5), text='Y-axis', color=color.green,
                   height=16, border=4, background=color.white)

if __name__ == "__main__":
    try:
        # Debug aktivieren für Details
        DebugConfig.GLOBAL_DEBUG = True
        DebugConfig.BRICK_DEBUG = True
        DebugConfig.GRID_DEBUG = True
        
        house_project = build_roman_bond_house()
        
        print("\n✅ Success! Your Roman Bond House is ready!")
        print("\nControls:")
        print("- Left drag: Rotate view")
        print("- Right drag: Pan")  
        print("- Mouse wheel: Zoom")
        
    except Exception as e:
        print(f"\n❌ Error building house: {e}")
        import traceback
        traceback.print_exc()
