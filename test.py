from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
import os

#methodName = 'Jenks'
methodName = 'EqualInterval'

dataMap = {
    'file': "ingreso_sintomas_todos",
    'title': 'Accesibilidad hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de síntomas e ingreso',
    'date': '22 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_SINTOMAS' a 'FECHA_INGRESO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201119COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_ingreso_sintomas',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalaria.qpt',
    'colorRamp': 'RdYlGn'
}

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
    
def addClasification(targetFieldNameData, methodName, colorRampName, legendName):
    print(targetFieldNameData)
    muns.setRenderer(QgsGraduatedSymbolRenderer(targetFieldNameData))
    muns.renderer().updateClasses(muns, graduatedMethod(methodName), 5)
    ramp = QgsStyle().defaultStyle().colorRamp(colorRampName)
    muns.renderer().updateColorRamp(invertColorRamp(ramp))
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.setName(dataMap['legend'])
    text = muns.renderer().legendSymbolItems()[0].label
    muns.renderer().legendSymbolItems()[0].label = f'{text} ()'
    muns.triggerRepaint()
    #iface.layerTreeView().refreshLayerSymbology(muns.id())

def createLayout(templeteQpt):
    #Create document
    document = loadTempleteQpt(templeteQpt)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.loadFromTemplate(document, QgsReadWriteContext())
    return layout



#Municipios
muns = loadLayerGpkg('mun_2019.gpkg', 'mun_2019', 'Municipios')

#Estados
edos = loadLayerGpkg('edos_2019.gpkg', 'edos_2019', 'Estados', symbol_edos)


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
print('Creando mapa', dataMap['file'])

QgsProject.instance().addMapLayer(muns)

#Prepare data in layer
csv = loadCsvFile(dataMap['file'])
join = createJoinData(csv, dataMap['targetFieldName'])
muns.addJoin(join)

#Add Clasification
targetFieldNameData = f"{dataMap['file']}_{dataMap['variant']}"
addClasification(targetFieldNameData, methodName, dataMap['colorRamp'], dataMap['legend'])

iface.layerTreeView().refreshLayerSymbology(muns.id())

