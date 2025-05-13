from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView


#select the layers
layers = QgsProject.instance().mapLayersByName("Muenster_City_Districts")
districts = layers[0]

layers = QgsProject.instance().mapLayersByName("Schools")
schools = layers[0]


parent=iface.mainWindow()

#from lecture slide-13
#first create an orderby clause
nameClause=QgsFeatureRequest.OrderByClause("Name", ascending=True)
#then create an orderby object using one or more orderby clauses
orderby=QgsFeatureRequest.OrderBy([nameClause])
#pass the orderby object to FeatureRequest
request=QgsFeatureRequest().setOrderBy(orderby)

#to create the districts_name list, we will create an empty list and add names into that
districts_names=[]
for feature in districts.getFeatures(request):
    districts_names.append(feature["Name"])
#print(districts_names)

sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ",districts_names)
if not bOk:
    QMessageBox.warning(parent, "Process Cancelled", "The user has cancelled the process")
else:
    #get the geometry o fteh selected district
    for dist in districts.getFeatures():
        if(dist["Name"]== sDistrict):
            dGeo = dist.geometry()
        else:
            continue
    #get all the schools init
    sInDist=[]
    for school in schools.getFeatures():
        if dGeo.contains(school.geometry()):
            sInDist.append(str(school["Name"])+ ", " + str(school["SchoolType"]) )
            
    sInDist.sort()
    #print(sInDist)
    
    #infor box shows only strings so convert the list to string
    sch = ""
    for s in sInDist:
        sch += str(s) + '\n\n'

    if len(sch.strip()) == 0:
        sch = "No schools in the selected district"
        
    QMessageBox.information(parent, f'Schools in {sDistrict}', sch)
