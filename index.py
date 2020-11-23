from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
import os

texts = {
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado',
    'date': '19 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_RESULTADO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201119COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio'
}

#Methods


#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital/data'
os.chdir(path)
project = QgsProject()

#Municipios
path_muns_gpkg = "mun_2019.gpkg"
gpkg_muns_layer = path_muns_gpkg + "|layername=mun_2019"
muns = QgsVectorLayer(gpkg_muns_layer, "Municipios", "ogr")

#Add Clasification
muns.setRenderer(QgsGraduatedSymbolRenderer('x'))
muns.renderer().updateClasses(muns, QgsGraduatedSymbolRenderer.Jenks, 5)
ramp = QgsStyle().defaultStyle().colorRamp('RdYlGn')
muns.renderer().updateColorRamp(QgsGradientColorRamp(ramp))
muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
muns.setName(texts['legend'])

#Estados
path_edos_gpkg = "edos_2019.gpkg"
gpkg_edos_layer = path_edos_gpkg + "|layername=edos_2019"
edos = QgsVectorLayer(gpkg_edos_layer, "Estados", "ogr")
edos.renderer().setSymbol(QgsFillSymbol.createSimple({
    'outline_width': '0.86',
    'outline_color': '35,35,35,255',
    'offset_unit': 'MM',
    'color': '0,0,0,255',
    'outline_style': 'solid',
    'style': 'no',
    'joinstyle': 'bevel',
    'outline_width_unit': 'MM'
}))

#Read qpt file
myFile = 'respuestaHospitalaria.qpt'
myTemplateFile = open(myFile, 'rt')
myTemplateContent = myTemplateFile.read()
myTemplateFile.close()

#Create document
myDocument = QDomDocument()
myDocument.setContent(myTemplateContent)

#Create layout
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.loadFromTemplate(myDocument, QgsReadWriteContext())

##Add Texts
layout.itemById('title').setText(texts['title'])
layout.itemById('subtitle').setText(texts['subtitle'])
layout.itemById('date').setText(texts['date'])
layout.itemById('note').setText(texts['note'])
layout.itemById('source').setText(texts['source'])

##Add Map main
map = layout.itemById('map')
map.setLayers([edos, muns])

##Add Map miniature
miniature = layout.itemById('miniature')
miniature.setLayers([edos, muns])

#Legend
legend = layout.itemById('legend')
#legend.setLinkedMap(map)
root = QgsLayerTree()
root.addLayer(muns)
legend.model().setRootGroup(root)

#Instance Iamage Path
base_path = os.path.join(QgsProject.instance().homePath())
image_path = os.path.join(base_path, "index.png")

#Export Image
exporter = QgsLayoutExporter(layout)
exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())