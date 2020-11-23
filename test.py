path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital/data'
os.chdir(path)

project = QgsProject()
layout = QgsPrintLayout(project)
layout.initializeDefaults()

#Municipios
path_muns_gpkg = "mun_2019.gpkg"
gpkg_muns_layer = path_muns_gpkg + "|layername=mun_2019"
muns = QgsVectorLayer(gpkg_muns_layer, "Municipios", "ogr")

map = QgsLayoutItemMap(layout)
map.setLayers([muns])
map.setRect(QRectF(0, 0, 200, 200))
map.setFrameEnabled(True)
layout.addItem(map)

legend = QgsLayoutItemLegend(layout)
legend.setRect(QRectF(0, 0, 30, 30))
legend.setFrameEnabled(True)
legend.setLinkedMap(map) # map is an instance of QgsLayoutItemMap
layout.addItem(legend)



#Instance Iamage Path
base_path = os.path.join(QgsProject.instance().homePath())
image_path = os.path.join(base_path, "test.png")

#Export Image
exporter = QgsLayoutExporter(layout)
exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())