import arcpy

outpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'

aprx = arcpy.mp.ArcGISProject(path + "\\IllegalCampsMap.aprx")

lyt = aprx.listLayouts("Map*")[0]

mf = lyt.listElements("mapframe_element", "*")[0]

m = aprx.listMaps("Map")[0]

lyr = m.listLayers("Campsite")[0]

mf.camera.setExtent(mf.getLayerExtent(lyr, False, True))

lyt.exportToJPEG(path + "\\Map.jpg")

print("Exported the map...")