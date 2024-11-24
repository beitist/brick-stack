# Creating and placing bricks
::: mermaid
graph TD;
    A[create box: size, color, axis, up] --> B[rotate: angle, r-axis];
    B --> C[move box: pos - 1/2 h/w];
    C --> D[calculate points];
    D --> E[update grid];
:::