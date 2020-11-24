from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
import os

#methodName = 'Jenks'
#methodName = 'EqualInterval'
methods = ['Jenks', 'EqualInterval']

dataMaps = [{
    'file': "ingreso_sintomas_todos",
    'title': 'Accesibilidad hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de síntomas e ingreso',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_SINTOMAS' a 'FECHA_INGRESO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_ingreso_sintomas',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'RdYlGn'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'RdYlGn'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'Greens'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'Greys'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'Greens'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'Greys'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'RdYlGn'
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
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'RdYlGn'
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
def createSymbolUnfilled(outlineWidth):
    return QgsFillSymbol.createSimple({
        'outline_width': str(outlineWidth),
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

def graduatedMethod(name):
    if (name == 'Jenks'):
        return QgsGraduatedSymbolRenderer.Jenks
    if (name == 'EqualInterval'):
        return QgsGraduatedSymbolRenderer.EqualInterval

def invertColorRamp(colorRamp):
    invert = QgsGradientColorRamp()
    invert.setColor1(colorRamp.color2())
    invert.setColor2(colorRamp.color1())
    stops = colorRamp.stops().copy()
    newStops = []
    for i in range(len(stops)):
        #print(i, len(stops)-i-1)
        newStops.append(colorRamp.stops()[i])
        newStops[i].color = stops[len(stops)-i-1].color
        #print(stop.offset, stop.color.name())
    invert.setStops(newStops)
    return invert

def addClasification(targetFieldNameData, methodName, colorRamp):
    muns.setRenderer(QgsGraduatedSymbolRenderer(targetFieldNameData))
    muns.renderer().updateClasses(muns, graduatedMethod(methodName), 5)
    ramp = QgsStyle().defaultStyle().colorRamp(colorRamp)
    muns.renderer().updateColorRamp(invertColorRamp(ramp))
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.triggerRepaint()

def formatLegendlabel(eval):
    min = float(eval.split(' - ')[0])
    max = float(eval.split(' - ')[1])
    query = f'"{targetFieldNameData}" > {min} and "{targetFieldNameData}" < {max}'
    muns.selectByExpression(query, QgsVectorLayer.SetSelection)
    format = f'{min:.1f} - {max:.1f} ({len(muns.selectedFeatures()):,})'
    #print(format)
    return format

def settingsLegend(legend, legendName):
    muns.setName(legendName)
    legendlayer = legend.model().rootGroup().addLayer(muns)
    legend.model().refreshLayerLegend(legendlayer)
    for i in legend.model().layerLegendNodes(legendlayer):
        i.setUserLabel((formatLegendlabel(i.evaluateLabel())))

def createLayout(templeteQpt):
    #Create document
    document = loadTempleteQpt(templeteQpt)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.loadFromTemplate(document, QgsReadWriteContext())
    return layout



#Municipios
munsBackground = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Fondo', createSymbolUnfilled(0.05))
muns = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Municipios')

#Estados
edos = loadLayerGpkg('edos_2019.gpkg', 'edos_2019', 'Estados', createSymbolUnfilled(0.86))


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
for i, dataMap in enumerate(dataMaps):
    print(i, 'Creando mapa', dataMap['file'])

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = createJoinData(csv, dataMap['targetFieldName'])
    muns.addJoin(join)

    #Add Clasification
    targetFieldNameData = f"{dataMap['file']}_{dataMap['variant']}"
    print(targetFieldNameData)
    
    for methodName in methods:
        addClasification(targetFieldNameData, methodName, dataMap['colorRamp'])

        #Create layout
        layout = createLayout(dataMap['template'])

        ##Add Texts
        layout.itemById('title').setText(dataMap['title'])
        layout.itemById('subtitle').setText(dataMap['subtitle'])
        layout.itemById('date').setText(dataMap['date'])
        layout.itemById('note').setText(dataMap['note'])
        layout.itemById('source').setText(dataMap['source'])

        ##Add Map main
        map = layout.itemById('map')
        map.setLayers([edos, muns, munsBackground])

        ##Add Map miniature
        miniature = layout.itemById('miniature')
        miniature.setLayers([edos, muns])

        #Legend
        legend = layout.itemById('legend')
        #legend.setLinkedMap(map)
        #root = QgsLayerTree()
        #root.addLayer(muns)
        #legend.model().setRootGroup(root)
        settingsLegend(legend, dataMap['legend'])
        
        #Logo
        base_path = os.path.join(QgsProject.instance().homePath())
        logo = layout.itemById('logo')
        logo.setPicturePath(os.path.join(base_path, 'logos', 'log_conacyt_horizontal_sin_sintagma.png'))
        #logo.setSvgFillColor(QColor('#002663'))

        #Instance Iamage Path
        image_name = f"{i}_{dataMap['file']}_{methodName}.png"
        image_path = os.path.join(base_path, image_name)

        #Export Image
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())

        print('Mapa generado', image_name)
    muns.removeJoin(join.joinLayerId())
    
#createMap(dataMaps[0])
print('*** Proceso finalizado ***')
