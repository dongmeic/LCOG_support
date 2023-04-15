import arcpy

outpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'

aprx = arcpy.mp.ArcGISProject(path + "\\IllegalCampsMap_DC.aprx")

lyt = aprx.listLayouts("Map*")[0]

mf = lyt.listElements("mapframe_element", "*")[0]

m = aprx.listMaps("Map")[0]

lyr = m.listLayers("Campsite")[0]

ex = mf.getLayerExtent(lyr, False, True)
p = 500
mf.camera.setExtent(arcpy.Extent(ex.XMin - p, ex.YMin - p, ex.XMax + p, ex.YMax + p))

lyt.exportToJPEG(path + "\\Map.jpg")

print("Exported the map...")