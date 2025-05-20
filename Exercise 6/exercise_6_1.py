#To open the csv file
import csv
#to increase the default filed size limit of CSV
import sys

#create a map canvas
mc =iface.mapCanvas()


#create a new layer in the memeory
newLyr = QgsVectorLayer("MultiPolygon", "temp_standard_land_value_muenster", "memory")
newLyr.setCrs(QgsCoordinateReferenceSystem(25832))

# Getting access to the layers data provider
provider = newLyr.dataProvider()

# Getting access to the layers capabilities
capabilities = provider.capabilitiesString()

# Checking if the capabilty is part of the layer
if "Add Attributes" in capabilities:
    # Create new fields
    #QVariant' has no attribute 'float' so we will use double
    field_1 = QgsField("standard_land_value", QVariant.Double, len=10, prec=2)
    field_2 = QgsField("type", QVariant.String, len = 5)
    field_3 = QgsField("district", QVariant.String, len = 50)
    
    # Use the data provider to add the fields to the layer
    provider.addAttributes([field_1, field_2, field_3])
    
    # User the method updateFields() to finally show them in the layer
    newLyr.updateFields()
#otherwise prompt a message that you do not have permissions to add attributes
else:
    parent=iface.mainWindow()
    QMessageBox.warning(parent, "Process Cancelled", "You do not have permission to _Add Attributes_")


#add features from the csv file
#file path
file_path = "D:/standard_land_value_muenster.csv"

#increase the dafault size limit for the csv field to read lone wkt geom
csv.field_size_limit(1_000_000)

# Open the file and read line by line
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  # Skip the header line
    for row in reader:
        # Creating a new feature (polygon) and set attribute values
        feature_new = QgsFeature(newLyr.fields())
        feature_new.setAttribute("standard_land_value", row[0])
        feature_new.setAttribute("type", row[1])
        feature_new.setAttribute("district", row[2])
        
        # Creating and set the feature/ polygon geometry from wkt
        polygonGeom = QgsGeometry.fromWkt(row[3])
        feature_new.setGeometry(polygonGeom)

        # Using the data provider to add the new feature to the layer
        provider.addFeatures([feature_new])
        
        #repeat

# At last add the layer to the map
QgsProject().instance().addMapLayer(newLyr)



