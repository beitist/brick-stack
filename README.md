# brick-stack

![hi-image displayed using bricks](/sample_img/hi-brick-stack2.png)

Brick-stack is a tiny python-library-to-be, with two main intentions:
1. function as a learning tool with realtime visual feedback to teach basic and advanced concepts of programming through brick layout
2. create building plans for (simple) brick projects.

Brick-stack uses [VPython](https://vpython.org/) for rendering.

# Participate
If you are interested in developing this together, be it as a teacher, coder, beta-tester, reach out!

## To Do
- [x] auto-z
- [x] automatic camera (x)
- [ ] automatic camera including baseplate (x)
- [ ] automatic camera (y, z)
- [x] add baseplate
- [x] add baseplate studs
- [ ] improve stud speed
- [ ] verify the documented examples
- [ ] add examples for auto-z = False
- [ ] create CameraManager
- [ ] rethink scene model
- [ ] add alternative cli for easier use
- [ ] 

## Usage
### Standard usage
1. Define a project and specify the type of bricks you want to use:

        my_project = BrickProject("duplo")

2. Define a scene with optional scene and camera settings:

        my_project.add_scene()  # optional: scene- and camera-settings

3. Add a 4x2x1 brick at (0,0) in red to your scene. Note: The z-coordinate is ignored as long as automatic z-calculation is turned on (standard).

    ```
    my_project.scenes[0].add_brick(
        'rect', 4, 2, 1, 0, 0, 0, color.red
    )
    ```

# Learning to Code with Brick-Stack: A Comprehensive Guide

## 1. Basic Structures
Learn the fundamentals of programming while building simple structures.

### 1.1 Single Bricks and Basic Placement
```python
# Initialize your project
my_project = BrickProject("lego")
my_project.add_scene()

# Add a baseplate (optional)
my_project.brick_scenes[0].add_baseplate()

# Place your first brick
my_project.brick_scenes[0].add_brick(
    "rect",      # brick type
    4,           # length (studs)
    2,           # width (studs)
    1,           # height (bricks)
    0,           # x position
    0,           # y position
    0,           # z position (optional with auto_z)
    color.red    # brick color
)
```

### 1.2 Simple Structures Using Loops
```python
# Build a tower (vertical stacking)
for height in range(5):
    my_project.brick_scenes[0].add_brick(
        "rect", 2, 2, 1, 
        0, 0, height,  # Notice how we use height for z-position
        color.blue
    )

# Build a wall (horizontal placement)
for position in range(6):
    my_project.brick_scenes[0].add_brick(
        "rect", 4, 2, 1,
        position * 4, 0, 0,  # Multiply position by length to avoid gaps
        color.green
    )
```

### 1.3 Basic Functions for Reusable Structures
```python
def build_simple_tower(scene, x, y, height, brick_color):
    """Build a simple tower at specified position"""
    for level in range(height):
        scene.add_brick("rect", 2, 2, 1, x, y, level, brick_color)

# Use the function to build multiple towers
build_simple_tower(my_project.brick_scenes[0], 0, 0, 5, color.red)
build_simple_tower(my_project.brick_scenes[0], 4, 0, 3, color.blue)
build_simple_tower(my_project.brick_scenes[0], 8, 0, 4, color.green)
```

## 2. Mathematical Concepts
Visualize mathematical principles with brick structures.

### 2.1 Symmetry
```python
def build_symmetric_pattern(scene, center_x, width):
    """Build a symmetric pattern around center_x"""
    for offset in range(width):
        # Build left side
        scene.add_brick("rect", 2, 2, 1, 
            center_x - offset*2 - 2, 0, 0, color.blue)
        # Build right side (mirror)
        scene.add_brick("rect", 2, 2, 1, 
            center_x + offset*2, 0, 0, color.blue)

# Create symmetric pattern with center at x=10
build_symmetric_pattern(my_project.brick_scenes[0], 10, 4)
```

### 2.2 Geometric Patterns
```python
def build_triangle(scene, base_x, base_y, size):
    """Build a triangle with given base position and size"""
    for row in range(size):
        bricks_in_row = size - row
        start_x = base_x + row  # Shift each row to center the triangle
        for brick in range(bricks_in_row):
            scene.add_brick("rect", 1, 1, 1,
                start_x + brick, base_y, row,
                color.yellow)

# Build a triangle with base of 5 bricks
build_triangle(my_project.brick_scenes[0], 0, 0, 5)
```

### 2.3 Simple Number Sequences
```python
def build_fibonacci(scene, start_x, max_height):
    """Visualize Fibonacci sequence with brick heights"""
    a, b = 1, 1
    x_pos = start_x
    
    while a <= max_height:
        # Build column of height 'a'
        for h in range(a):
            scene.add_brick("rect", 1, 1, 1,
                x_pos, 0, h, color.red)
        
        # Move to next position and calculate next Fibonacci number
        x_pos += 1
        a, b = b, a + b

# Build Fibonacci sequence up to height 8
build_fibonacci(my_project.brick_scenes[0], 0, 8)
```

## Practice Exercises
1. Build a staircase that spirals up (combine x, y, and z coordinates)
2. Create a symmetric castle with four towers
3. Build a pyramid where each level has one less row of bricks
4. Make a pattern that alternates between two colors

## Next Steps
- Experiment with different colors and patterns
- Try combining multiple functions to create more complex structures
- Challenge yourself to recreate real-world buildings
- Practice predicting the final structure before running your code

## 3. Creating Custom Objects
Learn to build reusable components and complex structures.

### 3.1 Basic Building Blocks
```python
def create_cube(scene, x, y, color_choice):
    """Create a 2x2x2 cube as a basic building block"""
    for z in range(2):
        scene.add_brick("rect", 2, 2, 1, x, y, z, color_choice)
    return {"x": x + 2, "y": y + 2}  # Return end position for chaining

def create_arch(scene, x, y):
    """Create a simple arch structure"""
    # Pillars
    for z in range(3):
        scene.add_brick("rect", 1, 1, 1, x, y, z, color.red)
        scene.add_brick("rect", 1, 1, 1, x + 3, y, z, color.red)
    # Top beam
    scene.add_brick("rect", 4, 1, 1, x, y, 3, color.blue)
```

### 3.2 Complex Structures (1)
```python
def create_house(scene, x, y, width, length, height):
    """Create a customizable house"""
    # Floor
    for dx in range(width):
        for dy in range(length):
            scene.add_brick("rect", 1, 1, 1, x + dx, y + dy, 0, color.green)
    
    # Walls
    for z in range(height):
        # Front and back walls
        for dx in range(width):
            scene.add_brick("rect", 1, 1, 1, x + dx, y, z + 1, color.red)
            scene.add_brick("rect", 1, 1, 1, x + dx, y + length - 1, z + 1, color.red)
        
        # Side walls (skip door in front wall)
        for dy in range(1, length - 1):
            if z < 2 and dy == length//2 and x == 0:  # Door position
                continue
            scene.add_brick("rect", 1, 1, 1, x, y + dy, z + 1, color.red)
            scene.add_brick("rect", 1, 1, 1, x + width - 1, y + dy, z + 1, color.red)

# Create a village
for house in range(3):
    create_house(my_project.brick_scenes[0], house * 8, 0, 6, 8, 3)
```

### 3.3 Building a Car
```python
def build_car(scene, x, y):
    # Base/chassis
    scene.add_brick("rect", 6, 4, 1, x, y, 0, color.blue)
    
    # Cabin
    scene.add_brick("rect", 3, 4, 1, x+1, y, 1, color.blue)
    
    # Wheels (using black bricks)
    wheel_positions = [(x+1, y), (x+1, y+3), 
                      (x+4, y), (x+4, y+3)]
    for wx, wy in wheel_positions:
        scene.add_brick("rect", 1, 1, 1, wx, wy, -1, color.black)

build_car(my_project.brick_scenes[0], 0, 0)
```

### 3.4 Another house
```python
def build_house(scene, x, y):
    # Foundation
    for dx in range(6):
        for dy in range(6):
            scene.add_brick("rect", 1, 1, 1, x+dx, y+dy, 0, color.black * 0.3)
    
    # Walls
    for z in range(4):  # Height of walls
        for dx in [0, 5]:  # Side walls
            for dy in range(6):
                scene.add_brick("rect", 1, 1, 1, x+dx, y+dy, z+1, color.red)
        for dy in [0, 5]:  # Front/back walls
            for dx in range(6):
                # Skip door space
                if z < 2 and dy == 0 and dx in [2, 3]:
                    continue
                scene.add_brick("rect", 1, 1, 1, x+dx, y+dy, z+1, color.red)

    # Roof
    for dx in range(7):
        height = abs(3 - dx)  # Create slope
        scene.add_brick("rect", 1, 6, 1, x+dx, y, 5+height, vec(0.5, 0.3, 0))

build_house(my_project.brick_scenes[0], 0, 0)
```

## 4. Understanding Object-Oriented Programming
Explore the Brick-Stack classes and create your own extensions.

### 4.1 Basic Class Structure
```python
# Understanding the existing class hierarchy
"""
BrickProject
  └── BrickScene
       └── OccupancyGrid
            └── BasicBrick
                 └── RectangularBrick
"""

# Creating a custom brick type
class LShapedBrick(BasicBrick):
    def __init__(self, brick_system, length=3, width=2, height=1, x=0, y=0, z=0, brick_color=color.red):
        super().__init__(brick_system)
        self.length = length
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.z = z
        self.color = brick_color
        
    def generate(self):
        # Create L-shape using two rectangular bricks
        brick1 = RectangularBrick(self.brick_system, 
            self.length-1, 1, self.height, 
            self.x, self.y, self.z, self.color)
        brick2 = RectangularBrick(self.brick_system,
            1, self.width, self.height,
            self.x + self.length-1, self.y, self.z, self.color)
```

### 4.2 Working with Parameters
```python
def create_customizable_tower(scene, x, y, height, style="basic"):
    """
    Create towers with different styles:
    - basic: simple stack
    - tapered: gets smaller towards top
    - complex: alternating patterns
    """
    if style == "basic":
        for z in range(height):
            scene.add_brick("rect", 2, 2, 1, x, y, z, color.blue)
    
    elif style == "tapered":
        for z in range(height):
            size = max(1, 3 - z//2)  # Decrease size with height
            scene.add_brick("rect", size, size, 1, 
                          x + (3-size), y + (3-size), z, color.red)
    
    elif style == "complex":
        for z in range(height):
            if z % 3 == 0:  # Every third layer is different
                scene.add_brick("rect", 3, 3, 1, x, y, z, color.green)
            else:
                scene.add_brick("rect", 2, 2, 1, x + 0.5, y + 0.5, z, color.blue)

# Create different tower styles
create_customizable_tower(my_project.brick_scenes[0], 0, 0, 6, "basic")
create_customizable_tower(my_project.brick_scenes[0], 6, 0, 6, "tapered")
create_customizable_tower(my_project.brick_scenes[0], 12, 0, 6, "complex")
```

## 5. Playful Mathematics
Visualize mathematical concepts through building.

### 5.1 Number Patterns
```python
def build_multiplication_table(scene, size):
    """Visualize multiplication table up to size x size"""
    for x in range(size):
        for y in range(size):
            height = (x + 1) * (y + 1)
            # Build columns with height representing the product
            for z in range(min(height, 10)):  # Limit height for visualization
                scene.add_brick("rect", 1, 1, 1, 
                    x * 2, y * 2, z,
                    color.hsv_to_rgb(height/size**2, 1, 1))  # Color based on value

# Build 5x5 multiplication table
build_multiplication_table(my_project.brick_scenes[0], 5)
```

## 6. Debugging Skills
Learn to identify and fix common problems.

### 6.1 Common Issues and Solutions
```python
# Problem 1: Overlapping Bricks
def broken_staircase():
    """This code has a positioning problem"""
    for i in range(5):
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 1, 1, i, i, i, color.red)  # Wrong! Bricks overlap

def fixed_staircase():
    """Fixed version with correct positioning"""
    for i in range(5):
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 1, 1, i*2, i*1, i, color.red)  # Correct spacing

# Problem 2: Incorrect Height Calculations
def broken_tower():
    """This code doesn't account for brick height"""
    for i in range(3):
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 2, 2, 0, 0, i, color.blue)  # Wrong z-position

def fixed_tower():
    """Fixed version accounting for brick height"""
    for i in range(3):
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 2, 2, 0, 0, i*2, color.blue)  # Correct z-position
```

### 6.2 Debugging Exercises
```python
# Debug Challenge 1: Find and fix the pattern error
def broken_pattern():
    """This pattern should be symmetric but isn't"""
    for i in range(4):
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 1, 1, i*2, 0, 0, color.red)
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 1, 1, -i*2, 0, 0, color.blue)  # What's wrong here?

# Debug Challenge 2: Fix the color pattern
def color_sequence_broken():
    """Should alternate between red and blue"""
    colors = [color.red, color.blue]
    for i in range(5):
        my_project.brick_scenes[0].add_brick(
            "rect", 2, 1, 1, i*2, 0, 0, colors[i])  # Index error!
```

## 7. Coding Challenges

### 7.1 Basic Challenges
```python
# Challenge 1: Create a spiral staircase
def spiral_staircase(radius, height):
    """
    Create a spiral staircase with given radius and height
    Hint: Use math.sin and math.cos for circular positioning
    """
    pass  # Your code here

# Challenge 2: Create a bridge with support columns
def bridge(length, height, support_spacing):
    """
    Create a bridge with:
    - Specified length
    - Height above ground
    - Regular support columns
    """
    pass  # Your code here
```

### 7.2 Advanced Challenges
```python
# Challenge 3: Create a fractal tree
def fractal_tree(scene, x, y, height, branch_factor=0.7):
    """
    Create a tree where each branch splits into two smaller branches
    Use recursion!
    """
    if height < 1:
        return
    
    # Create main trunk
    for z in range(int(height)):
        scene.add_brick("rect", 1, 1, 1, x, y, z, color.brown)
    
    # Create branches (recursively)
    if height > 2:
        new_height = int(height * branch_factor)
        fractal_tree(scene, x+1, y, new_height, branch_factor)
        fractal_tree(scene, x-1, y, new_height, branch_factor)

# Challenge 4: Create a maze generator
def generate_maze(width, length):
    """
    Generate a random maze with:
    - One entrance and one exit
    - No isolated areas
    - At least one valid path
    """
    pass  # Your code here
```

## 8. Optimization Techniques

### 8.1 Code Optimization
```python
# Before optimization
def build_wall_unoptimized(scene, length):
    """Unoptimized wall building"""
    for x in range(length):
        for y in range(3):  # height
            scene.add_brick("rect", 1, 1, 1, x, 0, y, color.red)
            scene.add_brick("rect", 1, 1, 1, x, 1, y, color.red)

# After optimization
def build_wall_optimized(scene, length):
    """Optimized wall building using larger bricks"""
    for x in range(0, length, 4):
        scene.add_brick("rect", 4, 2, 3, x, 0, 0, color.red)
```

### 8.2 Performance Tips
```python
def efficient_building_techniques():
    # 1. Use larger bricks where possible
    scene.add_brick("rect", 8, 2, 1, 0, 0, 0, color.red)  # Better than 8 1x2 bricks
    
    # 2. Build in layers
    def build_efficient_tower(x, y, height):
        # Build core structure first
        scene.add_brick("rect", 2, 2, height, x, y, 0, color.blue)
        # Add details later
        for z in range(height):
            if z % 2 == 0:
                scene.add_brick("rect", 1, 1, 1, x-1, y-1, z, color.red)
```

## 9. Documentation Practices

### 9.1 Code Documentation
```python
class CustomStructure:
    """
    A class for creating custom brick structures.
    
    Attributes:
        base_width (int): Width of the structure's base in studs
        base_length (int): Length of the structure's base in studs
        height (int): Height of the structure in bricks
        style (str): Building style ('modern', 'classic', 'abstract')
    """
    
    def build_layer(self, scene, level):
        """
        Builds a single layer of the structure.
        
        Args:
            scene (BrickScene): The scene to build in
            level (int): The vertical level to build at
            
        Returns:
            bool: True if successful, False if there was an error
            
        Example:
            >>> custom_structure = CustomStructure(4, 4, 3, 'modern')
            >>> custom_structure.build_layer(my_scene, 0)
        """
        pass
```

### 9.2 Project Documentation Template
```markdown
# Project Name: My Brick Creation

## Description
Brief description of what your structure represents

## Requirements
- Minimum base size: 10x10
- Maximum height: 20 bricks
- Colors used: red, blue, yellow

## Building Steps
1. Create the foundation
2. Build the main structure
3. Add details and decorations

## Code Structure
- `main.py`: Main building script
- `helpers.py`: Helper functions
- `constants.py`: Color and size definitions

## Screenshots
[Place for screenshots of your creation]

## Known Issues
- List any known problems or limitations

## Future Improvements
- Ideas for future enhancements
```


## Use case: learning tool
With brick-stack, you can learn several programming techniques and see visual results instantly.

### Basic programming:

#### Understand variables and parameters:
- Place bricks according to (x, y) coordinates
- Optional: choose your own (z) coordinates to expand to 3d
- Understand parameters: define length, width, height and location

#### Use loops to: 
- stack bricks and build towers
- build staircases by shifting along one axis

    ```
    ## Build a tower with h=5
    for x in range(0,5):
        my_project.brick_scenes[0].add_brick(
            "rect", 4, 2, 1, 5, 7, 0, "random"
        )
        my_project.brick_scenes[0].add_brick(
            "rect", 4, 2, 1, 5, 9, 0, "random"
        )
    ```

#### Understand functions to:
- simplify repeating patterns, e.g. a function to create the 4 walls of a house

### Coordinates and orientation

#### Understand 2d- and 3d-coordinates:
- Place bricks according to set coordinates, optionally include the z-dimension
- 

### Have fun!
Create brick models with an unlimited supply of basic building bricks.

#### Further educational ideas to be incorporated above:
- define your own colors (-> work with variables)