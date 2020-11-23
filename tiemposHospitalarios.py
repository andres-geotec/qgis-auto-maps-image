from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
import os

dataMaps = [{
    'file': "ingreso_sintomas_todos",
    'title': 'Accesibilidad hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de síntomas  e ingreso',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_SINTOMAS' a 'FECHA_INGRESO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201119COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_ingreso_sintomas',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'resultado_ingreso_todes',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_RESULTADO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'alta_ingreso_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y alta',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_ALTA' (estimada). Para los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_alta_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'defuncion_ingreso_fallecidos',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y defunción',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_DEF' (estimada). Para los municipios con menos de 3 defunciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_defuncion_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'alta_resultado_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de resultado y alta',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_RESULTADO' a 'FECHA_ALTA' (estimada). Para los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_alta_resultado',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'defuncion_resultado_fallecidos',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de resultado y defunción',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_RESULTADO' a 'FECHA_DEF' (estimada). Para los municipios con menos de 3 defunciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_defuncion_resultado',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'resultado_ingreso_ambulatorios',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas no hospitalizadas',
    'date': '22 de Noviembre de 2020',
    'note': 'Promedio municipal de días desde "FECHA_INGRESO" a "FECHA_RESULTADO". En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}, {
    'file': 'resultado_ingreso_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas hospitalizadas',
    'date': '22 de Noviembre de 2020',
    'note': 'Promedio municipal de días desde "FECHA_INGRESO" a "FECHA_RESULTADO". En los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt'
}]


#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital/data'
os.chdir(path)
project = QgsProject()

symbol_edos = QgsFillSymbol.createSimple({
    'outline_width': '0.86',
    'outline_color': '35,35,35,255',
    'offset_unit': 'MM',
    'color': '0,0,0,255',
    'outline_style': 'solid',
    'style': 'no',
    'joinstyle': 'bevel',
    'outline_width_unit': 'MM'
})


def loadLayerGpkg(file, layername, name, symbol=None):
    gpkg_layer = file + "|layername=" + layername
    vectorlayer = QgsVectorLayer(gpkg_layer, name, "ogr")
    if symbol:
        vectorlayer.renderer().setSymbol(symbol)
    return vectorlayer

def loadCsvFile(file):
    uri = f"file://{os.getcwd()}/{file}.csv?type=csv&delimiter=,&detectTypes=no"
    csv = QgsVectorLayer(uri, file, 'delimitedtext')
    #csv.isValid() s.replace('a', '')
    #QgsProject.instance().addMapLayer(muns)
    #QgsProject.instance().addMapLayer(csv)
    return csv

def createJoinData(csv, targetFieldName):
    join = QgsVectorLayerJoinInfo()
    join.setJoinFieldName(targetFieldName)
    join.setTargetFieldName(targetFieldName)
    join.setJoinLayer(csv)
    join.setUsingMemoryCache(True)
    #join.setPrefix('_')
    return join

def loadTempleteQpt(file):
    #Read qpt file
    templateFile = open(file, 'rt')
    templateContent = templateFile.read()
    templateFile.close()

    #Create document
    document = QDomDocument()
    document.setContent(templateContent)
    return document


#for dataMap in dataMaps:
def createMap(dataMap):
    print('Creando mapa', dataMap['file'])

    #Municipios
    muns = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Municipios')

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = createJoinData(csv, dataMap['targetFieldName'])
    muns.addJoin(join)

    #Add Clasification
    targetFieldNameData = f"{dataMap['file']}_{dataMap['variant']}"
    print(targetFieldNameData)
    muns.setRenderer(QgsGraduatedSymbolRenderer(targetFieldNameData))
    #muns.renderer().updateClasses(muns, QgsGraduatedSymbolRenderer.Jenks, 5)
    muns.renderer().updateClasses(muns, QgsGraduatedSymbolRenderer.EqualInterval, 5)
    ramp = QgsStyle().defaultStyle().colorRamp('RdYlGn')
    muns.renderer().updateColorRamp(QgsGradientColorRamp(ramp))
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.setName(dataMap['legend'])

    #Estados
    edos = loadLayerGpkg('edos_2019.gpkg', 'edos_2019', 'Estados', symbol_edos)

    #Create document
    document = loadTempleteQpt(dataMap['template'])

    #Create layout
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.loadFromTemplate(document, QgsReadWriteContext())

    ##Add Texts
    layout.itemById('title').setText(dataMap['title'])
    layout.itemById('subtitle').setText(dataMap['subtitle'])
    layout.itemById('date').setText(dataMap['date'])
    layout.itemById('note').setText(dataMap['note'])
    layout.itemById('source').setText(dataMap['source'])

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
    image_path = os.path.join(base_path, f"{dataMap['file']}.png")

    #Export Image
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())

    muns.removeJoin(join.joinLayerId())
    print('Mapa generado', dataMap['file'])
    
createMap(dataMaps[0])
