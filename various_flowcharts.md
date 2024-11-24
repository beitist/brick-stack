# Functional flowcharts
### Creating and placing bricks
::: mermaid
graph TD;
    A[1: calc and update grid / NS or EW] --> E[2: create box: size, color, axis, up];
    E --> H[3: rotate: angle, r-axis];
    H --> K[4: move box: pos - 1/2 h/w];
:::