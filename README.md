# brick-stack
A tiny python tool to create toy brick building plans, using VPython rendering functions.

## Usage
### Standard usage
1. Define a project and specify the type of bricks you want to use:

    my_project = BrickProject("duplo")

2. Define a scene with optional scene and camera settings:

    my_project.add_scene()  # optional: scene- and camera-settings

3. Add a 4x2x1 brick at (0,0) in red to your scene. Note: The z-coordinate is ignored as long as automatic z-calculation is turned on (standard).

    my_project.scenes[0].add_brick(
        'rect', 4, 2, 1, 0, 0, 0, color.red
    )

## Use case: learning tool
With brick-stack, you can learn simple programming techniques and see visual results instantly.

#### Understand coordinates:
- Place bricks according to (x, y) coordinates
- Optional: choose your own (z) coordinates to expand to 3d
- Understand parameters: define length, width, height and location

### Use loops to: 
- stack bricks and build towers
- build staircases by shifting along one axis

### Have fun!
Create brick models with an unlimited supply of basic building bricks.
