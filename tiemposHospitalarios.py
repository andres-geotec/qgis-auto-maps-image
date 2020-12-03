from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtGui
from qgis.utils import iface
import os


#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/201119_AtencionHospitalaria/201202COVID19MEXICOTOT/'
outputFolder = 'image-maps'
templeteFolder = 'templetes'
os.chdir(path)
project = QgsProject()

dataMaps = [{
    'file': "ingreso_sintomas_todos",
    'title': 'Accesibilidad hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de síntomas e ingreso',
    'date': '02 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_SINTOMAS' a 'FECHA_INGRESO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_ingreso_sintomas',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'file': 'resultado_ingreso_todes',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado',
    'date': '02 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_RESULTADO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'file': 'alta_ingreso_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y alta',
    'date': '02 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_ALTA' (estimada). Para los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_alta_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'Greens-|2',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'file': 'defuncion_ingreso_fallecidos',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y defunción',
    'date': '02 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_DEF' (estimada). Para los municipios con menos de 3 defunciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_defuncion_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '#333333,#e0e0e0',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'file': 'alta_resultado_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de resultado y alta',
    'date': '02 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_RESULTADO' a 'FECHA_ALTA' (estimada). Para los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_alta_resultado',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-Greens-2',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'file': 'defuncion_resultado_fallecidos',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de resultado y defunción',
    'date': '02 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_RESULTADO' a 'FECHA_DEF' (estimada). Para los municipios con menos de 3 defunciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_defuncion_resultado',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '#333333,#e0e0e0',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'file': 'resultado_ingreso_ambulatorios',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas no hospitalizadas',
    'date': '02 de Diciembre de 2020',
    'note': 'Promedio municipal de días desde "FECHA_INGRESO" a "FECHA_RESULTADO". En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks',
    'classes': [
        {'min':-13.2, 'max':1,'color':'#1a9641','label':'-13.2 - 1'},
        {'min':1, 'max':3,'color':'#a6d96a','label':'1.1 - 3'},
        {'min':3, 'max':5,'color':'#ffffc0','label':'3.1 - 5'},
        {'min':5, 'max':8,'color':'#fdae61','label':'5.1 - 8'},
        {'min':8, 'max':99,'color':'#d7191c','label':'8.1 - 99'}
    ]
}, {
    'file': 'resultado_ingreso_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas hospitalizadas',
    'date': '02 de Diciembre de 2020',
    'note': 'Promedio municipal de días desde "FECHA_INGRESO" a "FECHA_RESULTADO". En los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201202COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks',
    'classes': [
        {'min':-0.3, 'max':1,'color':'#1a9641','label':'-0.3 - 1'},
        {'min':1, 'max':3,'color':'#a6d96a','label':'1.1 - 3'},
        {'min':3, 'max':5,'color':'#ffffc0','label':'3.1 - 5'},
        {'min':5, 'max':8,'color':'#fdae61','label':'5.1 - 8'},
        {'min':8, 'max':58,'color':'#d7191c','label':'8.1 - 57'}
    ]
}]

#Devuelve un estilo para poligonos sin color de relleno
def createSymbolUnfilled(outlineWidth='0.26'):
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

#Carga un layer de un geopakage asignandole nombre y simbolo
def loadLayerGpkg(file, layerName, name, symbol=None):
    gpkg_layer = file + "|layername=" + layerName
    vectorlayer = QgsVectorLayer(gpkg_layer, name, "ogr")
    if symbol: vectorlayer.renderer().setSymbol(symbol)
    return vectorlayer

#Cargar un csv
def loadCsvFile(file):
    uri = f"file://{os.getcwd()}/{file}.csv?type=csv&delimiter=,&detectTypes=no"
    return QgsVectorLayer(uri, file, 'delimitedtext')

#Crea union de datos entre layer y csv
def createJoinData(csv, targetFieldName):
    join = QgsVectorLayerJoinInfo()
    join.setJoinFieldName(targetFieldName)
    join.setTargetFieldName(targetFieldName)
    join.setJoinLayer(csv)
    join.setUsingMemoryCache(True)
    #join.setPrefix('_')
    return join

def graduatedMethod(name):
    if (name == 'Jenks'):
        return QgsGraduatedSymbolRenderer.Jenks
    if (name == 'EqualInterval'):
        return QgsGraduatedSymbolRenderer.EqualInterval
    if (name == 'Quantile'):
        return QgsGraduatedSymbolRenderer.Quantile

def classificationMethod(methodName):
    return QgsApplication.classificationMethodRegistry().method(methodName)

def countFeaturesByQuery(query, layer):
    layer.selectByExpression(query, QgsVectorLayer.SetSelection)
    num = len(layer.selectedFeatures())
    layer.removeSelection()
    return num

def createRampByColors(colors):
    colorRamp = QgsGradientColorRamp()
    colorRamp.setColor1(QColor(colors[0]))
    colorRamp.setColor2(QColor(colors[-1]))
    offset = 1 / len(colors[1:])
    stops = []
    for i, color in enumerate(colors[1:-1]):
        stops.append(QgsGradientStop(offset * (i + 1), QColor(color)))
    colorRamp.setStops(stops)
    return colorRamp

def invertColorRamp(colorRamp):
    invert = QgsGradientColorRamp()
    invert.setColor1(colorRamp.color2())
    invert.setColor2(colorRamp.color1())
    stops = colorRamp.stops().copy()
    newStops = []
    for i, stop in enumerate(stops):
        newStops.append(QgsGradientStop(stop.offset, stops[len(stops)-i-1].color))
        #print(f'{i} ({stop.offset}:{stop.color.name()}) => ({newStops[i].offset}:{newStops[i].color.name()})')
    invert.setStops(newStops)
    return invert

def removeStopColorRamp(colorRamp, remove, start=False):
    newColorRamp = QgsGradientColorRamp()
    nStops = len(colorRamp.stops()) - remove
    if nStops < 0: nStops = 0
    offset = round(1 / (nStops + 1), 2)
    newStops = []
    
    if start:
        for i in range(nStops):
            #print(f'{i} ({offset * (i + 1)}:{colorRamp.stops()[i + remove].color.getRgb()})')
            newStops.append(QgsGradientStop(offset * (i + 1), colorRamp.stops()[i + remove].color))
        newColorRamp.setColor1(colorRamp.stops()[-nStops-1].color)
        newColorRamp.setColor2(colorRamp.color2())
    else:
        for i in range(nStops):
            #print(f'{i} ({offset * (i + 1)}:{colorRamp.stops()[i].color.getRgb()})')
            newStops.append(QgsGradientStop(offset * (i + 1), colorRamp.stops()[i].color))
        newColorRamp.setColor1(colorRamp.color1())
        newColorRamp.setColor2(colorRamp.stops()[nStops].color)
    
    newColorRamp.setStops(newStops)
    return newColorRamp

def defineRampColor(colorRampName):
    availableRamps = QgsStyle().defaultStyle().colorRampNames()
    if ',' in colorRampName:
        return createRampByColors(colorRampName.split(','))
    invert = False
    if colorRampName.startswith('-'):
        invert = True
        colorRampName = colorRampName[1:]
    remove = ''
    if '-' in colorRampName:
        separe = colorRampName.split('-')
        colorRampName = separe[0]
        remove = separe[1]
    if colorRampName in availableRamps:
        colorRamp = QgsStyle().defaultStyle().colorRamp(colorRampName)
        if invert:
            colorRamp = invertColorRamp(colorRamp)
        if bool(remove):
            removeStart = False
            if remove.startswith('|'): removeStart = True
            remove = [int(i) for i in remove.split('|') if i.isdigit()][0]
            colorRamp = removeStopColorRamp(colorRamp, remove, removeStart)
        return colorRamp
    else:
        print('La rampa de colores no existe')
        return QgsGradientColorRamp()

def addClassification(targetFieldNameData, methodName, colorRampName):
    muns.setRenderer(QgsGraduatedSymbolRenderer(targetFieldNameData))
    muns.renderer().updateClasses(muns, graduatedMethod(methodName), 5)
    #ramp = QgsStyle().defaultStyle().colorRamp(colorRampName)
    muns.renderer().updateColorRamp(defineRampColor(colorRampName))
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.triggerRepaint()

def addClassificationDefined(targetFieldNameData, classes, methodName):
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
        if '.' in n: return f'{float(n):.1f}'
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

def createLayoutFromTemplate(file):
    #Read qpt file
    templateFile = open(os.path.join(templeteFolder, file), 'rt')
    templateContent = templateFile.read()
    templateFile.close()
    #Create document
    document = QDomDocument()
    document.setContent(templateContent)
    #Create layout
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.loadFromTemplate(document, QgsReadWriteContext())
    return layout

def buildImageMap(dataMap):
    #Create layout
    layout = createLayoutFromTemplate(dataMap['template'])
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
    logo.setPicturePath(os.path.join(templeteFolder, 'log_conacyt_horizontal_sin_sintagma.png'))
    return layout

def checkFolder(folder):
    if os.path.isdir(folder) == False:
        os.mkdir(folder)
        print(f'Se ha creao la carpeta {folder}')

def exportImageMap(image_name, layout):
    checkFolder(outputFolder)
    image_path = os.path.join(outputFolder, image_name)

    #Export Image
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())

    print('Mapa generado', image_name)


#Municipios
muns = loadLayerGpkg(os.path.join(templeteFolder, 'mun_2019.gpkg'), 'mun_2019', 'Municipios')
#Estados
edos = loadLayerGpkg(os.path.join(templeteFolder, 'edos_2019.gpkg'), 'edos_2019', 'Estados', createSymbolUnfilled(0.86))
#QgsProject.instance().addMapLayer(muns)


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
for i, dataMap in enumerate(dataMaps):
    print(i+1, 'Creando mapa', dataMap['file'])

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = createJoinData(csv, dataMap['targetFieldName'])
    muns.addJoin(join)

    #Add variants
    for variant in dataMap['variants'].split(','):
        targetFieldNameData = f"{dataMap['file']}_{variant}"
        #targetFieldNameData = f"{dataMap['file']}_{dataMap['variant']}"
        print(targetFieldNameData)
        
        for methodName in dataMap['methods'].split(','):
            #Add Clasification
            addClassification(targetFieldNameData, methodName, dataMap['colorRamp'])

            #Instance Iamage Path
            image_name = f"{i+1}_{dataMap['file']}_{methodName}.png"
            exportImageMap(image_name, buildImageMap(dataMap))
            
        if 'classes' in dataMap.keys() and dataMap['classes']:
            for methodName in dataMap['methods'].split(','):
                addClassificationDefined(targetFieldNameData, dataMap['classes'], methodName)

                #Instance Iamage Path
                image_name = f"{i+1}_{dataMap['file']}_{methodName}_classes.png"
                exportImageMap(image_name, buildImageMap(dataMap))

    muns.removeJoin(join.joinLayerId())
    
#createMap(dataMaps[0])
print('*** Proceso finalizado ***')
