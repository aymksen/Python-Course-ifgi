import arcpy
import os

# Part 1
#set the working environment
gdb = arcpy.env.workspace = r"C:\exercise_arcpy_1.gdb"
# We can filter the featureClasses reference: https://pro.arcgis.com/en/pro-app/3.3/arcpy/functions/listfeatureclasses.htm
point_fcs = arcpy.ListFeatureClasses(feature_type='Point')
output_fc = os.path.join(gdb, "active_assets")

# Out output featureclass has only three fields so
fields = ['SHAPE@', 'status', 'type']

# loop through all feature classes
for fc in point_fcs:

    # The search and insert cursors
    s_cursor = arcpy.da.SearchCursor(fc, fields)
    i_cursor = arcpy.da.InsertCursor(output_fc, fields)

    # Now loop through evey line of the every point fc in the db
    for row in s_cursor:
        if str(row[1]).lower() == 'active':
            i_cursor.insertRow(row)
# Delete the cursors to free the workspace
del s_cursor
del i_cursor

# Part 2
# Add a new filed
arcpy.AddField_management(output_fc, 'buffer', "SHORT")

# Fields involved
fields = ['type', 'buffer']
u_cursor = arcpy.da.UpdateCursor(output_fc, fields)
for row in u_cursor:
    type_val = str(row[0]).lower()
    if type_val == 'mast':
        row[1] = 300
    elif type_val == 'mobile_antenna':
        row[1] = 50
    elif type_val == 'building_antenna':
        row[1] = 100
    else:
        continue

    u_cursor.updateRow(row)
del u_cursor

# Part 3
input_fc  = os.path.join(gdb, "active_assets")
output_fc = os.path.join(gdb, "active_assets_projected")
final_fc = os.path.join(gdb, "coverage")

# For testing, I might have to delete output again and again
if arcpy.Exists(output_fc):
    arcpy.Delete_management(output_fc)

# Now to get the distance accurate in meters for the buffer we have to project the featureclass
out_cord = arcpy.SpatialReference(32632)
arcpy.management.Project(in_dataset= input_fc , out_dataset = output_fc, out_coor_system = out_cord)

# Buffer ref: https://pro.arcgis.com/en/pro-app/latest/tool-reference/analysis/buffer.htm
arcpy.analysis.Buffer(in_features = output_fc, out_feature_class = final_fc, buffer_distance_or_field ='buffer')

