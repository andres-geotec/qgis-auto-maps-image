from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtGui
from qgis.utils import iface
import os

methods = ['Jenks']

dataMaps = [{
    'file': 'resultado_ingreso_ambulatorios_semanas',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas no hospitalizadas',
    'date': '22 de Noviembre de 2020',
    'note': 'Días promedio desde "FECHA_INGRESO" a "FECHA_RESULTADO", agrupado por municipio y semana epidemiológica. En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalariaGif.qpt',
    'colorRamp': 'RdYlGn'
}, {
    'file': 'resultado_ingreso_hospitalizados_semanas',
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas hospitalizadas',
    'date': '22 de Noviembre de 2020',
    'note': 'Días promedio desde "FECHA_INGRESO" a "FECHA_RESULTADO", agrupado por por municipio y semana epidemiológica. En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "201122COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalariaGif.qpt',
    'colorRamp': 'RdYlGn'
}]

semanas = ['03','05','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47']


#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital/data'
os.chdir(path)
project = QgsProject()

def createSymbol(outlineWidth, fillColor):
    return QgsFillSymbol.createSimple({
        'outline_width': str(outlineWidth),
        'outline_color': '35,35,35,255',
        'offset_unit': 'MM',
        'color': str(fillColor),
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
    if (name == 'Quantile'):
        return QgsGraduatedSymbolRenderer.Quantile

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
    
def addClasificationDefined(targetFieldNameData):
    classes = [
        {'min':0, 'max':1,'color':'#1a9641','label':'0 - 1'},
        {'min':1.1, 'max':3,'color':'#a6d96a','label':'1.1 - 3'},
        {'min':3.1, 'max':5,'color':'#ffffc0','label':'3.1 - 5'},
        {'min':5.1, 'max':8,'color':'#fdae61','label':'5.1 - 8'},
        {'min':8.1, 'max':500,'color':'#d7191c','label':'Más de 8'}
    ]
    #myTargetField = targetFieldNameData
    rangeList = []
    # Make our first symbol and range...
    for _class in classes:
        color = QtGui.QColor(_class['color'])
        symbol = QgsSymbol.defaultSymbol(muns.geometryType())
        symbol.setColor(color)
        _range = QgsRendererRange(_class['min'], _class['max'], symbol, _class['label'])
        rangeList.append(_range)
    
    renderer = QgsGraduatedSymbolRenderer('', rangeList)
    classificationMethod = QgsApplication.classificationMethodRegistry().method("Jenks")
    renderer.setClassificationMethod(classificationMethod)
    renderer.setClassAttribute(targetFieldNameData)

    muns.setRenderer(renderer)
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
munsBackground = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Fondo', QgsFillSymbol.createSimple({'outline_width': '0.05', 'color': '255,255,255,255'}))
muns = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Municipios')

#Estados
edos = loadLayerGpkg('edos_2019.gpkg', 'edos_2019', 'Estados', createSymbol(0.86, '0,0,0,255'))


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
for i, dataMap in enumerate(dataMaps[-1:]):
    print(i, 'Creando mapa', dataMap['file'])

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = createJoinData(csv, dataMap['targetFieldName'])
    muns.addJoin(join)

    #for semana in semanas:
    for semana in semanas[-1:]:
        #Add Clasification
        targetFieldNameData = f"{dataMap['file']}_{semana}"
        print(targetFieldNameData)
        
        #for methodName in methods:
        #addClasification(targetFieldNameData, methods[0], dataMap['colorRamp'])
        addClasificationDefined(targetFieldNameData)
        
        QgsProject.instance().addMapLayer(muns)

    
#createMap(dataMaps[0])
print('*** Proceso finalizado ***')
