from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView


#select the layer
layers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
districts = layers[0]

parent=iface.mainWindow()

#get the input coordinates
sCoords, bOk = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text = "51.96066,7.62476")

if not bOk:
    QMessageBox.warning(parent, "Process Cancelled", "The user has cancelled the process")
else:
    sCoords = sCoords.split(",")
    #from basics of GIS; Lat, Lng = Y, X
    sY = float(sCoords[0])
    sX = float(sCoords[1])
    #make a point from the provided coordinates (from lecture slide 28)
    sPoint = QgsPointXY(sX, sY)


# Source coordinate system
crsS = QgsCoordinateReferenceSystem(4326)

# Target coordinate system EPSG:25832 - ETRS89 / UTM zone 32N
#i.e. EPSG:25832 Projected coordinate system for Europe between 6°E and 12°E: Austria; Denmark, Germany 
crsT = QgsCoordinateReferenceSystem("EPSG:25832")

#Initializing the transformation and convert the coordinates
transformation = QgsCoordinateTransform(crsS, crsT, QgsProject.instance())
tPoint = transformation.transform(sPoint)

#create the geometry from a QGSPointXY 
#source: https://qgis.org/pyqgis/3.40/core/QgsGeometry.html#module-QgsGeometry
tGeom = QgsGeometry.fromPointXY(tPoint)
inMuenster = False
# go through all the districts and check if the point is within any of the district
for dist in districts.getFeatures():
    if (dist.geometry().contains(tGeom)):
        indistrict = dist["Name"]
        inMuenster = True
    else:
        continue


if (inMuenster):
    QMessageBox.information(parent, "Point is in Münster", f' The point falls in the District:" {indistrict}"')
else:
    QMessageBox.information(parent, "Point is not in Münster", "The points does not fall in the Münster")
