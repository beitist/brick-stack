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
        print(f"Orientation: {self.orientation}")
    
    # 1. Calculate final position based on orientation FIRST
    # This determines where the brick will be placed
    if self.orientation == NORTH:
        final_pos = vector(
            self.x + self.width/2, 
            self.y + self.length/2, 
            self.z + self.height/2
        )
        box_length = self.length
        box_width = self.width
        stud_x_range = int(self.stud_x_counter)
        stud_y_range = int(self.stud_y_counter)
        stud_offset_x = self.x + self.specs["stud_xy_offset"]
        stud_offset_y = self.y + self.specs["stud_xy_offset"]
        
    elif self.orientation == EAST:
        final_pos = vector(
            self.x + self.length/2,  # Note: length and width swapped
            self.y + self.width/2, 
            self.z + self.height/2
        )
        box_length = self.width  # Swapped for rotation
        box_width = self.length
        stud_x_range = int(self.stud_y_counter)  # Swapped
        stud_y_range = int(self.stud_x_counter)
        stud_offset_x = self.x + self.specs["stud_xy_offset"]
        stud_offset_y = self.y + self.specs["stud_xy_offset"]
        
    elif self.orientation == SOUTH:
        final_pos = vector(
            self.x + self.width/2, 
            self.y + self.length/2, 
            self.z + self.height/2
        )
        box_length = self.length
        box_width = self.width
        stud_x_range = int(self.stud_x_counter)
        stud_y_range = int(self.stud_y_counter)
        stud_offset_x = self.x + self.specs["stud_xy_offset"]
        stud_offset_y = self.y + self.specs["stud_xy_offset"]
        
    elif self.orientation == WEST:
        final_pos = vector(
            self.x + self.length/2,  # Note: length and width swapped
            self.y + self.width/2, 
            self.z + self.height/2
        )
        box_length = self.width  # Swapped for rotation
        box_width = self.length
        stud_x_range = int(self.stud_y_counter)  # Swapped
        stud_y_range = int(self.stud_x_counter)
        stud_offset_x = self.x + self.specs["stud_xy_offset"]
        stud_offset_y = self.y + self.specs["stud_xy_offset"]

    # 2. Create box in NORTH orientation at origin first
    brick_basis = box(
        pos = vec(0, 0, 0),  # Create at origin
        axis = vector(0,1,0), # North orientation
        length = self.length,  # Always use original dimensions
        height = self.height,
        width = self.width,
        color = self.brick_color,
        up = vector(0,0,1)
    )

    brick_components = [brick_basis]

    # 3. Add studs at correct positions relative to origin
    for x_stud in range(int(self.stud_x_counter)):
        for y_stud in range(int(self.stud_y_counter)):
            # Calculate stud position relative to brick base
            stud_center = vec(
                -self.width/2 + self.specs["stud_xy_offset"] + (x_stud * self.specs["stud_spacing"]),
                -self.length/2 + self.specs["stud_xy_offset"] + (y_stud * self.specs["stud_spacing"]),
                self.height/2
            )
            stud = self.generate_stud(
                pos = stud_center,
                hollow = self.specs["is_hollow"],
                wall_thickness = self.specs["stud_wall_thickness"]
            )
            brick_components.append(stud)

    # 4. Create compound at origin
    brick_compound = compound(brick_components)

    # 5. Rotate if needed
    rotation_angle = self.orientation.rotation
    if rotation_angle != 0:
        brick_compound.rotate(angle=rotation_angle, axis=vector(0,0,1))

    # 6. Move to final position
    brick_compound.pos = final_pos

    if GLOBAL_DEBUG and BRICK_DEBUG: 
        print(f"Final compound pos: {brick_compound.pos}")
        print(f"Final compound axis: {brick_compound.axis}, up-vector: {brick_compound.up}")

    return brick_compound
