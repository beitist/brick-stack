# brick-stack
A tiny python tool to create toy brick building plans, using VPython rendering functions.

brick-stack is intended to serve as a learning tool as well as a toy for modelling simple brick models based on textfile input or cli.

## To Do
- [x] auto-z
- [x] automatic camera (x)
- [ ] automatic camera (y, z)
- [ ] add baseplate
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

1. Grundlagen der Programmierung
a) Variablen und Parameter
Lernziel: Die Bedeutung von Parametern und wie sie die Funktion von Methoden oder Konstruktoren beeinflussen.
Ansatz: Schüler können Bricks mit verschiedenen Längen, Breiten, Höhen und Farben erstellen und dabei sehen, wie sich die Szene verändert.
Beispiel: Was passiert, wenn man die Parameter von add_brick verändert?
python
Code kopieren
schiff.brick_scenes[0].add_brick("rect", 4, 2, 1, 0, 0, 0, color.red)
b) Schleifen
Lernziel: Die Wiederholung von Aufgaben mithilfe von Schleifen.
Ansatz: Schüler können Türme, Treppen oder Muster bauen, indem sie Schleifen verwenden, anstatt jede Anweisung einzeln zu schreiben.
Beispiel:
python
Code kopieren
for x in range(10):
    schiff.brick_scenes[0].add_brick("rect", 4, 2, 1, x * 4, 0, 0, "random")
c) Funktionen
Lernziel: Den Nutzen von Funktionen erkennen und wie sie Wiederholungen vermeiden.
Ansatz: Schüler können Funktionen erstellen, um komplexere Konstruktionen wie Häuser, Brücken oder Fahrzeuge zu abstrahieren.
Beispiel: Eine Funktion für ein Auto:
python
Code kopieren
def build_car(scene):
    # Basis
    scene.add_brick("rect", 6, 4, 1, 0, 0, 0, color.blue)
    # Räder
    for x in [0, 5]:
        for y in [0, 3]:
            scene.add_brick("rect", 1, 1, 1, x, y, -1, color.black)
2. Koordinatensystem und Raumvorstellung
a) 3D-Koordinaten verstehen
Lernziel: Wie x, y und z in einem 3D-Raum zusammenhängen.
Ansatz: Schüler können experimentieren, um zu verstehen, wie sich Bricks in der Szene platzieren lassen:
x: Länge (links/rechts).
y: Breite (vorne/hinten).
z: Höhe (unten/oben).
Übung: Eine Treppe oder Pyramide bauen.
python
Code kopieren
for x in range(5):
    schiff.brick_scenes[0].add_brick("rect", 4, 2, 1, x * 4, 0, x, "random")
b) Relativpositionen
Lernziel: Verständnis für relative Positionierung entwickeln.
Ansatz: Bausteine können relativ zu bereits existierenden Steinen positioniert werden, z. B. für Brücken oder Türme.
3. Debugging und Problemlösung
a) Visuelles Debugging
Lernziel: Fehler erkennen und beheben.
Ansatz: Wenn ein Brick falsch positioniert oder die Z-Koordinate nicht korrekt berechnet wird, können Schüler durch die visuelle Darstellung sehen, was falsch gelaufen ist.
b) Logisches Denken
Lernziel: Strukturiertes Vorgehen bei der Problemlösung.
Ansatz: Schüler lernen, ihre Konstruktionen Schritt für Schritt zu planen und systematisch zu implementieren.
4. Einführung in objektorientierte Programmierung (OOP)
a) Klassen und Objekte
Lernziel: Wie Klassen und Objekte verwendet werden.
Ansatz: Schüler können lernen, wie BrickProject, BrickScene und BrickFactory zusammenarbeiten.
Übung: Ein eigenes BrickProject erstellen und erweitern:
python
Code kopieren
projekt = BrickProject("lego")
projekt.add_scene()
b) Vererbung und Polymorphismus
Lernziel: Wie Vererbung funktioniert.
Ansatz: Erweiterungen der Brick-Klassen (z. B. neue Brick-Formen oder Spezialsteine) als Übung für OOP-Konzepte.
5. Kreativität und eigenständiges Arbeiten
a) Eigene Projekte umsetzen
Schüler können eigenständig Designs erstellen, die ihren Interessen entsprechen (z. B. Häuser, Tiere, Fahrzeuge).
Beispiel:
Haus: Ein Rechteck als Basis, kleinere Rechtecke als Wände und ein Dach als umgekehrtes Dreieck.
b) Wettbewerbe und Gruppenprojekte
Teams könnten in Wettbewerben antreten, um die kreativsten oder funktionalsten Designs zu erstellen, was die Teamarbeit fördert.
6. Erweiterung durch externe Technologien
a) Schnittstellen zu Dateien
Lernziel: Mit externen Daten arbeiten.
Ansatz: Schüler können ihre Designs in Dateien speichern oder laden, z. B.:
python
Code kopieren
projekt.save_to_file("projekt.json")
projekt.load_from_file("projekt.json")
b) Erweiterung durch physikalische Modelle
Die Konstruktionen könnten in 3D-gedruckte Modelle oder reale Baupläne umgewandelt werden.
c) Verbindung mit anderen Sprachen
Schüler könnten überlegen, wie sie andere Programmiersprachen (z. B. JavaScript für Web-Renderings) verwenden könnten, um ihre Designs zu erweitern.
