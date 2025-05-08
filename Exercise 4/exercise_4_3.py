# exercise_4_3.py

import os
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer
)

# ——— 1. Configure your QGIS install and data folder ———
# Change these to match your machine:
QGIS_PREFIX = r"C:/Program Files/QGIS 3.40.0/apps/qgis"
MUENSTER_DIR = r"C:/Users/Aymen/Desktop/Muenster"

# ——— 2. Start QGIS in standalone mode ———
QgsApplication.setPrefixPath(QGIS_PREFIX, True)
qgs = QgsApplication([], False)
qgs.initQgis()

# ——— 3. Create a new, empty project ———
project = QgsProject.instance()

# ——— 4. Find every .shp in the folder ———
shapefiles = [
    os.path.join(MUENSTER_DIR, f)
    for f in os.listdir(MUENSTER_DIR)
    if f.lower().endswith(".shp")
]

# ——— 5. Load them into the project ———
for shp in shapefiles:
    # use the filename (no “.shp”) as the layer name
    name = os.path.splitext(os.path.basename(shp))[0]
    layer = QgsVectorLayer(shp, name, "ogr")
    if layer.isValid():
        project.addMapLayer(layer)
    else:
        print(f"⚠️ Could not load {shp}")

# ——— 6. Save as “myFirstProject.qgs” in the same folder ———
output_qgs = os.path.join(MUENSTER_DIR, "myFirstProject.qgs")
project.write(output_qgs)
print(f"Project saved to: {output_qgs}")

# ——— 7. Clean up ———
qgs.exitQgis()
