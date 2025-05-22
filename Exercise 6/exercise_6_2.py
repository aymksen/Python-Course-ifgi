# Create a map canvas object
mc = iface.mapCanvas()

# Get swimming pools layer from the TOC
layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]

# Get districts layer from the TOC
districts = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# Getting all fields of the layer
fields = layer.fields()

# Getting access to the layers data provider
provider = layer.dataProvider()

# Getting access to the layers capabilities
capabilities = provider.capabilitiesString()

# Checking if the capabilty is part of the layer
if "Change Attribute Values" in capabilities:
    
    # If modifying is possible, get all features of the layer 
    # and loop through them.
    for feature in layer.getFeatures():
        
        # Get the id of the current feature
        feature_id = feature.id()
        
        # If the value of the current feature in the column "Type" has
        # the value "H" change it to "Hallenbad"
        if feature["Type"] == "H":
            
            # Create a dictionary with column and value to change
            attributes = {fields.indexOf("Type"):"Hallenbad"}
            
        elif feature["Type"] == "F":
            
            # Create a dictionary with column and value to change
            attributes = {fields.indexOf("Type"):"Freibad"}
        else:
            pass
        # Use the changeAttributeValues methode from the provider to 
        # process the attribute change for the specific feature id
        provider.changeAttributeValues({feature_id:attributes})
    
else:
    parent=iface.mainWindow()
    QMessageBox.warning(parent, "Process Cancelled", "Features of this layer cannot be modified")
    
if "Add Attributes" in capabilities:
    
    # Create new fields
    field_1 = QgsField("District", QVariant.String, len = 50)
    
    # Use the data provider to add the fields to the layer
    provider.addAttributes([field_1])
    
    # User the method updateFields() to finally show them in the layer
    layer.updateFields()
else:
    parent=iface.mainWindow()
    QMessageBox.warning(parent, "Process Cancelled", "New fields cannot be added")

#get the updated fields
newFields = layer.fields()
#go through the pools one by obe to check ifthey are in any of the districts
for pool in layer.getFeatures():
    # go through all the districts and check if the point is within any of the district
    # Get the id of the current feature/pool
    newFeature_id = pool.id()
    for dist in districts.getFeatures():
        #if the pool in within a particular District geometry
        if (dist.geometry().contains(pool.geometry())):
            #check capabilities
            if "Change Attribute Values" in capabilities:
                #Assign the name of the district to the pool district column
                newAttributes = {newFields.indexOf("District"):dist["Name"]}
                provider.changeAttributeValues({newFeature_id:newAttributes})
                #break the loop because one pool could only be within one district
                break
            else:
                parent=iface.mainWindow()
                QMessageBox.warning(parent, "Process Cancelled", "Features of this layer cannot be modified")
  
        else:
            continue