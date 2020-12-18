from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtGui
from qgis.utils import iface
import os


#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/201119_AtencionHospitalaria/201216COVID19MEXICOTOT/'
outputFolder = 'image-maps'
templeteFolder = 'templetes'
os.chdir(path)
project = QgsProject()

dataMaps = [{
    'group': 1,
    'file': 'ingreso_sintomas_todos',
    'title': 'Accesibilidad hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de síntomas e ingreso',
    'date': '16 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_SINTOMAS' a 'FECHA_INGRESO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_ingreso_sintomas',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'group': 2,
    'file': 'resultado_ingreso_todes',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado',
    'date': '16 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_RESULTADO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'group': 3,
    'file': 'alta_ingreso_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y alta',
    'date': '16 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_ALTA' (estimada). Para los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_alta_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'Greens-|2',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'group': 4,
    'file': 'defuncion_ingreso_fallecidos',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y defunción',
    'date': '16 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_DEF' (estimada). Para los municipios con menos de 3 defunciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_defuncion_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '#333333,#e0e0e0',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'group': 5,
    'file': 'alta_resultado_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de resultado y alta',
    'date': '16 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_RESULTADO' a 'FECHA_ALTA' (estimada). Para los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_alta_resultado',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-Greens-2',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'group': 6,
    'file': 'defuncion_resultado_fallecidos',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de resultado y defunción',
    'date': '16 de Diciembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_RESULTADO' a 'FECHA_DEF' (estimada). Para los municipios con menos de 3 defunciones se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_defuncion_resultado',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '#333333,#e0e0e0',
    'methods': 'Jenks,Quantile',
    'classes': ''
}, {
    'group': 7,
    'file': 'resultado_ingreso_ambulatorios',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas no hospitalizadas',
    'date': '16 de Diciembre de 2020',
    'note': 'Promedio municipal de días desde "FECHA_INGRESO" a "FECHA_RESULTADO". En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks',
    'classes': [
        {'min':-13.2, 'max':1,'color':'#1a9641','label':'13.2 - 1'},
        {'min':1, 'max':3,'color':'#a6d96a','label':'1 - 3'},
        {'min':3, 'max':5,'color':'#ffffc0','label':'3 - 5'},
        {'min':5, 'max':8,'color':'#fdae61','label':'5 - 8'},
        {'min':8, 'max':99,'color':'#d7191c','label':'8 - 99'}
    ]
}, {
    'group': 8,
    'file': 'resultado_ingreso_hospitalizados',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas hospitalizadas',
    'date': '16 de Diciembre de 2020',
    'note': 'Promedio municipal de días desde "FECHA_INGRESO" a "FECHA_RESULTADO". En los municipios con menos de 3 hospitalizaciones se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201216COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variants': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': '-RdYlGn',
    'methods': 'Jenks',
    'classes': [
        {'min':-0.3, 'max':1,'color':'#1a9641','label':'-0.3 - 1'},
        {'min':1, 'max':3,'color':'#a6d96a','label':'1 - 3'},
        {'min':3, 'max':5,'color':'#ffffc0','label':'3 - 5'},
        {'min':5, 'max':8,'color':'#fdae61','label':'5 - 8'},
        {'min':8, 'max':58,'color':'#d7191c','label':'8 - 10'}
    ]
}]

#-------------------- ESTILOS DE CAPAS --------------------
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

#Crea una lista de colores intermedios para una paleta de colores
def defineIntermediateColorsRamp(colors):
    #offset determina la pocisión de los colores intermedios o `stops`
    offset = round(1 / (len(colors) + 1), 2)
    return [QgsGradientStop(offset*(i+1), QColor(color)) for i, color in enumerate(colors)]

#Devuelve la lista de colores intermedios en hexadecimal
def getIntermediateHexaColorsRamp(colorRamp):
    return [stop.color.name() for stop in colorRamp.stops()].copy()

#Crea una paleta a partir de una lista de colores en hexadecimal
def createRampByColors(colors):
    colorRamp = QgsGradientColorRamp()
    colorRamp.setColor1(QColor(colors[0]))
    colorRamp.setColor2(QColor(colors[-1]))
    colorRamp.setStops(defineIntermediateColorsRamp(colors[1:-1]))
    return colorRamp

#Invierte una paleta de colores
def invertColorRamp(colorRamp):
    invert = QgsGradientColorRamp()
    invert.setColor1(colorRamp.color2())
    invert.setColor2(colorRamp.color1())
    intermediateColors = getIntermediateHexaColorsRamp(colorRamp)
    intermediateColors.reverse()
    invert.setStops(defineIntermediateColorsRamp(intermediateColors))
    return invert

#Elimina colores intermedios de una paleta de colores
def removeIntermediateColorRamp(colorRamp, remove, start=False):
    newColorRamp = QgsGradientColorRamp()
    if remove > len(colorRamp.stops()): remove = len(colorRamp.stops())
    intermediateColors = getIntermediateHexaColorsRamp(colorRamp)
    if start:
        newColorRamp.setColor1(QColor(intermediateColors[remove-1]))
        newColorRamp.setStops(defineIntermediateColorsRamp(intermediateColors[remove:]))
        newColorRamp.setColor2(colorRamp.color2())
    else:
        newColorRamp.setColor1(colorRamp.color1())
        newColorRamp.setStops(defineIntermediateColorsRamp(intermediateColors[:-remove]))
        newColorRamp.setColor2(QColor(intermediateColors[-remove]))
    return newColorRamp

#Define el tipo de paleta seun el parámetro
# 1 '#,#,#'     -> lista de colores en hexadecimal
# 2 'RdYlGn'    -> nombre de paleta establecida
# 3 '-RdYlGn'   -> paleta establecida invertida
# 4 'RdYlGn-1'  -> paleta establecida menos un color al final
# 5 'RdYlGn-|1' -> paleta establecida menos un color al inicio
def defineRampColor(colorRampName):
    if ',' in colorRampName:
        #Si es una lista de colores separada por comas
        return createRampByColors(colorRampName.split(','))
    invert = False
    if colorRampName.startswith('-'):
        #Si es necesario invertirla
        invert = True
        colorRampName = colorRampName[1:]
    remove = ''
    if '-' in colorRampName:
        #Si es necesario remover colores
        separe = colorRampName.split('-')
        colorRampName = separe[0]
        remove = separe[1]
    if colorRampName in QgsStyle().defaultStyle().colorRampNames():
        #Si la paleta establecida existe
        colorRamp = QgsStyle().defaultStyle().colorRamp(colorRampName)
        if invert: colorRamp = invertColorRamp(colorRamp)
        if bool(remove):
            removeStart = False
            if remove.startswith('|'):
                #Si hay que remover colores al inicio
                removeStart = True
            remove = [int(i) for i in remove.split('|') if i.isdigit()][0]
            colorRamp = removeIntermediateColorRamp(colorRamp, remove, removeStart)
        return colorRamp
    else:
        print('La rampa de colores no existe')
        return QgsGradientColorRamp()
#-------------------- ESTILOS DE CAPAS --------------------

#-------------------- CARGA DE ARCHIVOS --------------------
#Carga un layer de un geopakage asignandole nombre y simbolo
def loadLayerGpkg(file, layerName, name, symbol=None):
    gpkg_layer = file + "|layername=" + layerName
    vectorlayer = QgsVectorLayer(gpkg_layer, name, "ogr")
    if symbol: vectorlayer.renderer().setSymbol(symbol)
    return vectorlayer

#Cargar un csv como layer en el proyecto
def loadCsvFile(file, delimiter=','):
    uri = f"file://{os.getcwd()}/{file}.csv?type=csv&delimiter={delimiter}&detectTypes=no"
    return QgsVectorLayer(uri, file, 'delimitedtext')

#Crea una hoja de impresión a partir de un archivo qpt
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
#-------------------- CARGA DE ARCHIVOS --------------------

#-------------------- TRATAMIENTO DE DATOS --------------------
#Establece los parametros de union etre layers
def defineJoinData(joinLayer, targetFieldName):
    join = QgsVectorLayerJoinInfo()
    join.setJoinFieldName(targetFieldName)
    join.setTargetFieldName(targetFieldName)
    join.setJoinLayer(joinLayer)
    join.setUsingMemoryCache(True)
    #join.setPrefix('_')
    return join

#Lista de atributos por columna
def getAttributesByField(layer, field):
    idxField = layer.fields().names().index(field)
    return [feature.attributes()[idxField] for feature in layer.dataProvider().getFeatures()]

#Valores minimos y maximos por columna    
def getMinMaxValuesByField(layer, field):
    values = getAttributesByField(layer, field)
    values.sort()
    return values[0], values[-1]

def countFeaturesByQuery(query, layer):
    layer.selectByExpression(query, QgsVectorLayer.SetSelection)
    num = len(layer.selectedFeatures())
    layer.removeSelection()
    return num
#-------------------- TRATAMIENTO DE DATOS --------------------

#-------------------- CLASIFICACIÓN --------------------
def graduatedMethod(name):
    if (name == 'Jenks'):
        return QgsGraduatedSymbolRenderer.Jenks
    if (name == 'EqualInterval'):
        return QgsGraduatedSymbolRenderer.EqualInterval
    if (name == 'Quantile'):
        return QgsGraduatedSymbolRenderer.Quantile

def classificationMethod(methodName):
    return QgsApplication.classificationMethodRegistry().method(methodName)

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
        #_range = QgsRendererRange(_class['min'], _class['max'], symbol, _class['label'])
        _range = QgsRendererRange(_class['min'], _class['max'], symbol, _class['label'])
        rangeList.append(_range)
    
    renderer = QgsGraduatedSymbolRenderer('', rangeList)
    classificationMethod = QgsApplication.classificationMethodRegistry().method(methodName)
    renderer.setClassificationMethod(classificationMethod)
    renderer.setClassAttribute(targetFieldNameData)

    muns.setRenderer(renderer)
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.triggerRepaint()
#-------------------- CLASIFICACIÓN --------------------

#-------------------- IMPRESIÓN --------------------
def formatLegendlabel(eval, i, ant):
    def format(n):
        if '.' in n: return f'{float(n):.1f}'
        return n
    min = eval.split(' - ')[0]
    max = eval.split(' - ')[1]
    #query = f'"{targetFieldNameData}" >= {float(min)} and "{targetFieldNameData}" < {float(max)}'
    query = f'"{targetFieldNameData}" <= {float(max)}'
    label = ''
    count = countFeaturesByQuery(query, muns)-ant
    if i == 0:
        if min == max: label = f'{format(min)} ({count:,})'
        else: label = f'{format(min)} - {format(max)} ({count:,})'
    else: label = f'{format(str(float(min)+0.1))} - {format(max)} ({count:,})'
    ant += count
    return label, ant

def settingsLegend(legend, legendName):
    muns.setName(legendName)
    legendlayer = legend.model().rootGroup().addLayer(muns)
    legend.model().refreshLayerLegend(legendlayer)
    ant = 0
    for i, node in enumerate(legend.model().layerLegendNodes(legendlayer)):
        label, ant = formatLegendlabel(node.evaluateLabel(), i, ant)
        node.setUserLabel(label)

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

#valida que una carpeta exista
def checkFolder(folder):
    if os.path.isdir(folder) == False:
        os.mkdir(folder)
        print(f'Se ha creao la carpeta {folder}')

#Guarda el layout como imagen
def exportImageMap(image_name, layout):
    checkFolder(outputFolder)
    image_path = os.path.join(outputFolder, image_name)
    #Export Image
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())
    print('Mapa generado', image_name)
#-------------------- IMPRESIÓN --------------------



#Municipios
muns = loadLayerGpkg(os.path.join(templeteFolder, 'mun_2019.gpkg'), 'mun_2019', 'Municipios')
#Estados
edos = loadLayerGpkg(os.path.join(templeteFolder, 'edos_2019.gpkg'), 'edos_2019', 'Estados', createSymbolUnfilled(0.86))
#QgsProject.instance().addMapLayer(muns)


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
for dataMap in dataMaps:
    ant = 0
    print(dataMap['group'], 'Creando mapa', dataMap['file'])

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = defineJoinData(csv, dataMap['targetFieldName'])
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
            image_name = f"{dataMap['group']}_{dataMap['file']}_{methodName}.png"
            exportImageMap(image_name, buildImageMap(dataMap))
            
        if 'classes' in dataMap.keys() and dataMap['classes']:
            for methodName in dataMap['methods'].split(','):
                addClassificationDefined(targetFieldNameData, dataMap['classes'], methodName)

                #Instance Iamage Path
                image_name = f"{dataMap['group']}_{dataMap['file']}_{methodName}_classes.png"
                exportImageMap(image_name, buildImageMap(dataMap))

    muns.removeJoin(join.joinLayerId())
    
#createMap(dataMaps[0])
print('*** Proceso finalizado ***')
