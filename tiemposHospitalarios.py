from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtGui
from qgis.utils import iface
import os

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
    'colorRamp': 'RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': ''
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
    'colorRamp': 'RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': ''
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
    'colorRamp': 'Greens',
    'methods': 'Jenks,Quantile',
    'classes': ''
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
    'colorRamp': 'Greys',
    'methods': 'Jenks,Quantile',
    'classes': ''
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
    'colorRamp': 'Greens',
    'methods': 'Jenks,Quantile',
    'classes': ''
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
    'colorRamp': 'Greys',
    'methods': 'Jenks,Quantile',
    'classes': ''
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
    'colorRamp': 'RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': [
        {'min':-13.2, 'max':1,'color':'#1a9641','label':'-13.2 - 1'},
        {'min':1, 'max':3,'color':'#a6d96a','label':'1 - 3'},
        {'min':3, 'max':5,'color':'#ffffc0','label':'3 - 5'},
        {'min':5, 'max':8,'color':'#fdae61','label':'5 - 8'},
        {'min':8, 'max':99,'color':'#d7191c','label':'8 - 99'}
    ]
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
    'colorRamp': 'RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': [
        {'min':-0.3, 'max':1,'color':'#1a9641','label':'-0.3 - 1'},
        {'min':1, 'max':3,'color':'#a6d96a','label':'1 - 3'},
        {'min':3, 'max':5,'color':'#ffffc0','label':'3 - 5'},
        {'min':5, 'max':8,'color':'#fdae61','label':'5 - 8'},
        {'min':8, 'max':58,'color':'#d7191c','label':'8 - 57'}
    ]
}]


#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital/data'
os.chdir(path)
project = QgsProject()

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

def addJoinData(csv, targetFieldName):
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
    if (name == 'Quantile'):
        return QgsGraduatedSymbolRenderer.Quantile

def countFeaturesByQuery(query, layer):
    layer.selectByExpression(query, QgsVectorLayer.SetSelection)
    num = len(muns.selectedFeatures())
    return num

def removeStopColorRamp(colorRamp):
    newColorRamp = QgsGradientColorRamp()
    newColorRamp.setColor1(colorRamp.color1())
    newStops = []
    countFinal = len(colorRamp.stops()) - 1
    offset = 1 / countFinal
    for i, stop in enumerate(colorRamp.stops()):
        if i == countFinal:
            newColorRamp.setColor2(stop.color)
            #print('eliminar color', i, stop.offset, stop.color.name())
        else:
            stop.offset = offset * (i + 1)
            newStops.append(stop)
            #print(i, stop.offset, stop.color.name())
    newColorRamp.setStops(newStops)
    return newColorRamp

def invertColorRamp(colorRamp, colorRampName):
    invert = QgsGradientColorRamp()
    invert.setColor1(colorRamp.color2())
    invert.setColor2(colorRamp.color1())
    stops = colorRamp.stops().copy()
    newStops = []
    for i in range(len(stops)):
        #print(i, colorRamp.stops()[i].color.name(), '=>', len(stops)-i-1)
        newStops.append(colorRamp.stops()[i])
        newStops[i].color = stops[len(stops)-i-1].color
        #print(stop.offset, stop.color.name())
    invert.setStops(newStops)
    if colorRampName == 'Greens':
        #return removeStopColorRamp(removeStopColorRamp(invert))
        return removeStopColorRamp(removeStopColorRamp(colorRamp))
    if colorRampName == 'Greys':
        invert.setColor1(QColor('#333333'))
        invert.setStops([])
        invert.setColor2(QColor('#e0e0e0'))
    return invert

def defineColorRamp(colorRampName):
    if ',' in colorRampName:
        return
    return

def addClassification(targetFieldNameData, methodName, colorRampName):
    muns.setRenderer(QgsGraduatedSymbolRenderer(targetFieldNameData))
    muns.renderer().updateClasses(muns, graduatedMethod(methodName), 5)
    ramp = QgsStyle().defaultStyle().colorRamp(colorRampName)
    muns.renderer().updateColorRamp(invertColorRamp(ramp, colorRampName))
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.triggerRepaint()

def addClasificationDefined(targetFieldNameData, classes, methodName):
    rangeList = []
    # Make our first symbol and range...
    for _class in classes:
        color = QtGui.QColor(_class['color'])
        symbol = QgsSymbol.defaultSymbol(muns.geometryType())
        symbol.setColor(color)
        _range = QgsRendererRange(_class['min'], _class['max'], symbol, _class['label'])
        rangeList.append(_range)
    
    renderer = QgsGraduatedSymbolRenderer('', rangeList)
    classificationMethod = QgsApplication.classificationMethodRegistry().method(methodName)
    renderer.setClassificationMethod(classificationMethod)
    renderer.setClassAttribute(targetFieldNameData)

    muns.setRenderer(renderer)
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.triggerRepaint()

def formatLegendlabel(eval):
    def format(n):
        if '.' in n:
            return f'{float(n):.1f}'
        return n
    min = eval.split(' - ')[0]
    max = eval.split(' - ')[1]
    query = f'"{targetFieldNameData}" >= {float(min)} and "{targetFieldNameData}" < {float(max)}'
    format = f'{format(min)} - {format(max)} ({countFeaturesByQuery(query, muns):,})'
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

def buildImageMap(dataMap):
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
    map.setLayers([edos, muns])
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
    logo = layout.itemById('logo')
    logo.setPicturePath(os.path.join(base_path, 'logos', 'log_conacyt_horizontal_sin_sintagma.png'))
    return layout

def exportImageMap(image_name, layout):
    image_path = os.path.join(base_path, image_name)

    #Export Image
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())

    print('Mapa generado', image_name)


#Municipios
muns = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Municipios')

#Estados
edos = loadLayerGpkg('edos_2019.gpkg', 'edos_2019', 'Estados', createSymbolUnfilled(0.86))

#
base_path = os.path.join(QgsProject.instance().homePath())


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
for i, dataMap in enumerate(dataMaps):
    print(i+1, 'Creando mapa', dataMap['file'])

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = addJoinData(csv, dataMap['targetFieldName'])
    muns.addJoin(join)

    #Add Clasification
    targetFieldNameData = f"{dataMap['file']}_{dataMap['variant']}"
    print(targetFieldNameData)
    
    for methodName in dataMap['methods'].split(','):
        addClassification(targetFieldNameData, methodName, dataMap['colorRamp'])

        #Instance Iamage Path
        image_name = f"{i+1}_{dataMap['file']}_{methodName}.png"
        exportImageMap(image_name, buildImageMap(dataMap))
        
    if 'classes' in dataMap.keys() and dataMap['classes']:
        for methodName in dataMap['methods'].split(','):
            addClasificationDefined(targetFieldNameData, dataMap['classes'], methodName)

            #Instance Iamage Path
            image_name = f"{i+1}_{dataMap['file']}_{methodName}_classes.png"
            exportImageMap(image_name, buildImageMap(dataMap))



    muns.removeJoin(join.joinLayerId())
    
#createMap(dataMaps[0])
print('*** Proceso finalizado ***')
