# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-12-15 22:22:14
"""
import arcpy
from datetime import date
import timeit

path = r"G:\projects\UtilityDistricts\eweb\DrinkingWater\EPA319_NPS_grant\ForestApplication\ODF_FACTS_DB\FERNS\FERNS_Model"
wrkspace = path + "\\FERNS_Workspace.gdb"
year = str(date.today().year)
arcpy.env.workspace = wrkspace

def FERNSforAGOstep3(Expression="YEAR <> '{0}'".format(year)):  # FERNS for AGO step 3

    arcpy.env.overwriteOutput = True

    FERNSSummary_McKenzie_Joined = path + "\\FERNS_Final_Products.gdb\\FERNSSummary_McKenzie_Joined"
    res = arcpy.GetCount_management(FERNSSummary_McKenzie_Joined)
    
    AGO_FERNSSummary_McKenzie_Joined_3_ = "https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/FERNS_for_McKenzie_Catchments/FeatureServer/0"

    AGO_FERNSSummary_McKenzie_Joined_5_, count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=AGO_FERNSSummary_McKenzie_Joined_3_, 
                                                                                        selection_type="NEW_SELECTION", 
                                                                                        where_clause=Expression, 
                                                                                        invert_where_clause="")
    arcpy.management.CopyFeatures(AGO_FERNSSummary_McKenzie_Joined_5_, f'FERNS_before_{year}')

    print(f"Before Year {year} there are {count} counts and in Year {year} there are {res[0]} counts!")

    # Process: Append (Append) (management)
    AGO_FERNSSummary_McKenzie_Joined = arcpy.management.Append(inputs=[FERNSSummary_McKenzie_Joined], 
                                                                target=f'FERNS_before_{year}', 
                                                                schema_type="NO_TEST", 
                                                                field_mapping="", 
                                                                subtype="", 
                                                                expression="")[0]

if __name__ == '__main__':
    # Global Environment settings
    start = timeit.default_timer()
    with arcpy.EnvManager(scratchWorkspace=wrkspace, workspace=wrkspace):
        FERNSforAGOstep3()
    # print("tested")
    stop = timeit.default_timer()
    total_time = stop - start
    print(f'FERNS for AGO step 3 takes {total_time}')