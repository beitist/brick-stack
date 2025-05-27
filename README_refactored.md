, 16, 16)

# Steine in verschiedenen Orientierungen
scene.add_brick(length=4, width=2, height=1, x_pos=0, y_pos=0, 
                brick_color=color.blue, orientation=NORTH)
scene.add_brick(length=4, width=2, height=1, x_pos=4, y_pos=0, 
                brick_color=color.red, orientation=EAST)
scene.add_brick(length=4, width=2, height=1, x_pos=0, y_pos=4, 
                brick_color=color.yellow, orientation=SOUTH)
scene.add_brick(length=4, width=2, height=1, x_pos=4, y_pos=4, 
                brick_color=color.green, orientation=WEST)

# Automatisches Stapeln
scene.add_brick(length=2, width=2, height=1, x_pos=1, y_pos=1, 
                brick_color=color.orange, orientation=NORTH)
```

## 📚 API-Referenz

### Hauptklassen

#### `BrickProject(brick_system, auto_z=True)`
- **brick_system**: `"lego"`, `"duplo"`, oder `"test"`
- **auto_z**: Automatische Höhenberechnung aktivieren

#### `BrickScene`
- **add_baseplate()**: Baseplate zur Szene hinzufügen
- **add_brick()**: Stein zur Szene hinzufügen

#### `add_brick()` Parameter
```python
scene.add_brick(
    brick_type="rect",      # Steintyp
    length=4,               # Länge in Noppen
    width=2,                # Breite in Noppen  
    height=1,               # Höhe in Steineinheiten
    x_pos=0,                # X-Position
    y_pos=0,                # Y-Position
    z_pos=0,                # Z-Position (bei auto_z ignoriert)
    brick_color=color.red,  # Farbe
    orientation=NORTH       # Orientierung
)
```

### Orientierungen
- `NORTH`: Länge entlang positiver Y-Achse
- `EAST`: Länge entlang positiver X-Achse  
- `SOUTH`: Länge entlang negativer Y-Achse
- `WEST`: Länge entlang negativer X-Achse

## 🔧 Debug-Konfiguration

```python
# Debug-Ausgaben aktivieren
DebugConfig.GLOBAL_DEBUG = True
DebugConfig.BRICK_DEBUG = True
DebugConfig.GRID_DEBUG = True
DebugConfig.STUD_DEBUG = True
```

## 🧪 Tests ausführen

```bash
cd /Users/beiti/Documents/Python/Lego/brick-stack
python test_refactored_system.py
```

## 📐 Koordinatensystem

```
Y (Länge)
↑
|
|
└─────→ X (Breite)
 ↙
Z (Höhe)

NORTH (0,1,0): Länge entlang Y-Achse
EAST  (1,0,0): Länge entlang X-Achse
SOUTH (0,-1,0): Länge entlang -Y-Achse  
WEST  (-1,0,0): Länge entlang -X-Achse
```

## 🎯 Verbesserungen im Detail

### 1. Rotationssystem
**Vorher:** Rotation und Positionierung führten zu Verwirrung
```python
# Alte Methode - problematisch
brick_compound.rotate(angle, axis)
brick_compound.pos = calculate_position()  # Falsche Dimensionen!
```

**Nachher:** Saubere Reihenfolge
```python
# Neue Methode - korrekt
compound = create_at_origin()
compound.rotate(angle, axis) 
compound.pos = calculate_final_position()  # Berücksichtigt Rotation
```

### 2. Höhenmodell mit Rotation
**Problem:** Grid verwendete ursprüngliche Dimensionen statt rotierte
```python
# Vorher - Bug
self.grid.add_brick(x, y, z, length, width, height)  # Immer gleich

# Nachher - Korrekt  
if orientation in [NORTH, SOUTH]:
    grid_length, grid_width = length, width
else: # EAST, WEST
    grid_length, grid_width = width, length  # Vertauscht!
self.grid.add_brick(x, y, z, grid_length, grid_width, height)
```

### 3. Verbesserte Code-Struktur
- **Typ-Hints**: Bessere IDE-Unterstützung
- **Docstrings**: Umfassende Dokumentation
- **Error-Handling**: Validierung und aussagekräftige Fehlermeldungen
- **Modularität**: Klare Trennung der Verantwortlichkeiten

## 🔍 Debugging-Tipps

1. **Debug-Modus aktivieren:**
```python
DebugConfig.GLOBAL_DEBUG = True
DebugConfig.BRICK_DEBUG = True
```

2. **Einzelne Komponenten testen:**
```python
# Nur Grid testen
DebugConfig.GRID_DEBUG = True
DebugConfig.CALCULATION_DEBUG = True
```

3. **Kamera-Probleme debuggen:**
```python
DebugConfig.CAMERA_DEBUG = True
```

## 🚧 Bekannte Limitationen

- Nur rechteckige Steine implementiert
- Keine Speicher-/Lade-Funktionalität
- Begrenzte Stein-Typen (geplant für v3.0)

## 🎉 Fazit

Das refactored System löst alle ursprünglichen Rotationsprobleme und bietet:
- ✅ Korrekte Compound-Rotation  
- ✅ Funktionierendes Höhenmodell mit Orientierung
- ✅ Saubere, dokumentierte Code-Struktur
- ✅ Umfassende Tests
- ✅ Einfache Erweiterbarkeit

Die neue Version ist production-ready und kann als Basis für weitere Entwicklungen dienen!
