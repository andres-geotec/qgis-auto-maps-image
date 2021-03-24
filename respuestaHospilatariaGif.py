from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt import QtGui
from qgis.utils import iface
from datetime import datetime
from PIL import Image
import os

methods = ['Jenks']
PATHMAIN = '/home/andres/Proyectos/CONACyT/201119_AtencionHospitalaria'
now = datetime.today()
#now = datetime(2021,1,13)
path = os.path.join(PATHMAIN, '{}COVID19MEXICOTOT'.format(str(now).replace('-','')[2:8]))
print(now)

dataMaps = [{
    'file': 'resultado_ingreso_ambulatorios_semanas',
    'title': 'Respuesta hospitalaria (ambulatorios)',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas no hospitalizadas',
    'date': f"{now.day} de {now.strftime('%B').title()} de {now.year}",
    'note': 'Días promedio desde "FECHA_INGRESO" a "FECHA_RESULTADO", agrupado por municipio y semana epidemiológica. En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "{}COVID19MEXICOTOT" de la Dirección General de Epidemiología.'.format(str(now).replace('-','')[2:8]),
    'legend': 'Días Promedio',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalariaGif.qpt'
}, {
    'file': 'resultado_ingreso_hospitalizados_semanas',
    'title': 'Respuesta hospitalaria (no ambulatorios)',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado de personas hospitalizadas',
    'date': f"{now.day} de {now.strftime('%B').title()} de {now.year}",
    'note': 'Días promedio desde "FECHA_INGRESO" a "FECHA_RESULTADO", agrupado por municipio y semana epidemiológica. En los municipios con menos de 3 casos ambulatorios se utilizó el promedio por jurisdicción sanitaria.',
    'source': 'Secretaría de Salud: "{}COVID19MEXICOTOT" de la Dirección General de Epidemiología.'.format(str(now).replace('-','')[2:8]),
    'legend': 'Días Promedio',
    'targetFieldName': 'cvegeomun',
    'template': 'respuestaHospitalariaGif.qpt'
}]



#Instance path proyect application
#path = '/home/andres/Proyectos/CONACyT/201119_AtencionHospitalaria/210120COVID19MEXICOTOT/'
templeteFolder = 'templetes'
os.chdir(path)
project = QgsProject()

def checkFolder(folder):
    if os.path.isdir(folder) == False:
        os.mkdir(folder)
        print(f'Se ha creao la carpeta {folder}')

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
    templateFile = open(os.path.join(templeteFolder, file), 'rt')
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

def addClasificationDefined(targetFieldNameData, methodName):
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
    classificationMethod = QgsApplication.classificationMethodRegistry().method(methodName)
    renderer.setClassificationMethod(classificationMethod)
    renderer.setClassAttribute(targetFieldNameData)

    muns.setRenderer(renderer)
    muns.renderer().updateSymbols(QgsFillSymbol.createSimple({'outline_width': '0.05'}))
    muns.triggerRepaint()


def createLayout(templeteQpt):
    #Create document
    document = loadTempleteQpt(templeteQpt)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.loadFromTemplate(document, QgsReadWriteContext())
    return layout

#Devuelve el texto del rango de fechas por semana epidemiológica
def getTextDateRangesByWeek(weekNumber):
    def getDateOfWeek(weekNumber, nDay):
        year = 2020
        weeksInYear = 53
        if int(weekNumber) > weeksInYear:
            #Si la semana sobrepasa la capacidad del año, aumentar el año en cuestión
            weekNumber -= weeksInYear
            year += 1
        return datetime.strptime(f'{year}-W{weekNumber}-{nDay}', '%G-W%V-%u')
    ini = getDateOfWeek(int(weekNumber)-1, 7)
    fin = getDateOfWeek(weekNumber, 6)
    label = f"Del {ini.day:02d}"
    if ini.strftime('%B') != fin.strftime('%B'):
        #Si los meses de las fechas no coinciden, mostrar ambos meses
        label += f" de {ini.strftime('%B')}"
    return f"({label} al {fin.day:02d} de {fin.strftime('%B')})"

# Baja la resolución de la imagen
def lowerImageResolution(img, percent):
    def getPercent(n, percent):
        return int(n*(percent/100))
    w, h = im.size
    return im.resize((getPercent(w, percent), getPercent(h, percent)))

#Municipios
munsBackground = loadLayerGpkg(os.path.join(templeteFolder, 'mun_2019.gpkg'), 'mun_2019', 'Sin ingresos', 
    QgsFillSymbol.createSimple({'outline_width': '0.05', 'color': '255,255,255,255'}))
muns = loadLayerGpkg(os.path.join(templeteFolder, 'mun_2019.gpkg'), 'mun_2019', 'Días Promedio')

#Estados
edos = loadLayerGpkg(os.path.join(templeteFolder, 'edos_2019.gpkg'), 'edos_2019', 'Estados', createSymbol(0.86, '0,0,0,255'))


#def createMap(dataMap):
#for dataMap in dataMaps[:2]:
for i, dataMap in enumerate(dataMaps):
    #if i: continue
    print(i, 'Creando mapa', dataMap['file'])

    #Prepare data in layer
    csv = loadCsvFile(dataMap['file'])
    join = createJoinData(csv, dataMap['targetFieldName'])
    muns.addJoin(join)

    cols = [k.name() for k in csv.fields()]
    #print('columnas: ' + str(cols))
    semanas = cols[cols.index('10'):-2]#[40:47]
    print('semanas: ' + str(semanas))
    images = []

    for semana in semanas:
        #Add Clasification
        targetFieldNameData = f"{dataMap['file']}_{semana}"
        print(targetFieldNameData)
        
        for methodName in methods:
            #addClasification(targetFieldNameData, methodName, dataMap['colorRamp'])
            addClasificationDefined(targetFieldNameData, methodName)

            #Create layout
            layout = createLayout(dataMap['template'])

            ##Add Texts
            layout.itemById('title').setText(dataMap['title'])
            layout.itemById('subtitle').setText(dataMap['subtitle'])
            layout.itemById('date').setText(dataMap['date'])
            layout.itemById('note').setText(dataMap['note'])
            layout.itemById('source').setText(dataMap['source'])
            layout.itemById('semana_rango').setText(getTextDateRangesByWeek(int(semana)))
            if '54' in semanas:
                # Los reportes posteriores al 210120 se imprimen con año
                layout.itemById('semana_title').setText(
                    f'Semana Epidemiológica {f"{semana} (2020)" if int(semana)<54 else f"{int(semana)-53} (2021)"}')
            else:
                # Los reportes anteriores al 210120 no se imprimen con año
                layout.itemById('semana_title').setText(f'Semana Epidemiológica {semana}')
            

            ##Add Map main
            map = layout.itemById('map')
            map.setLayers([edos, muns, munsBackground])

            ##Add Map miniature
            miniature = layout.itemById('miniature')
            miniature.setLayers([edos, muns, munsBackground])

            #Legend
            legend = layout.itemById('legend')
            root = QgsLayerTree()
            root.addLayer(muns)
            legend.model().setRootGroup(root)
            #settingsLegend(legend, dataMap['legend'])
            legend2 = layout.itemById('legend2')
            root2 = QgsLayerTree()
            root2.addLayer(munsBackground)
            legend2.model().setRootGroup(root2)
            
            #Logo
            base_path = os.path.join(QgsProject.instance().homePath())
            logo = layout.itemById('logo')
            logo.setPicturePath(os.path.join(templeteFolder, 'log_conacyt_horizontal_sin_sintagma.png'))
            #logo.setSvgFillColor(QColor('#002663'))

            checkFolder('forGifs')

            #Instance Iamage Path
            image_name = f"{i}_{dataMap['file']}_{semana}_{methodName}.png"
            image_path = os.path.join(base_path, 'forGifs', image_name)

            #Export Image
            exporter = QgsLayoutExporter(layout)
            exporter.exportToImage(image_path, QgsLayoutExporter.ImageExportSettings())
            im = Image.open(image_path)
            images.append(lowerImageResolution(im, 19))
            print('load', image_path)

            print('Mapa generado', image_name)
    muns.removeJoin(join.joinLayerId())
    #QgsProject.instance().addMapLayer(muns)
    #QgsProject.instance().addMapLayer(csv)

    print('creando gif de', len(images), 'imagenes')
    images[0].save(os.path.join(base_path, 'forGifs', f'{i}_{dataMap["file"]}.gif'), save_all=True, 
        append_images=images[1:], optimize=False, duration=1000, loop=0)
    print(f'{i}_{dataMap["file"]}.gif', 'Finalizado.')
    
#createMap(dataMaps[0])
print('*** Proceso finalizado ***')
'''
print('*** Haciendo Gifs!!! ***')

from PIL import Image
import os

path = os.path.join(path, 'forGifs')
names = ['0_resultado_ingreso_ambulatorios']#,'1_resultado_ingreso_hospitalizados']
images = []

def lowerImageResolution(img, percent):
    def getPercent(n, percent):
        return int(n*(percent/100))
    w, h = im.size
    return im.resize((getPercent(w, percent), getPercent(h, percent)))
for name in names:
    #image_name = '1_resultado_ingreso_hospitalizados_semanas_{}_Jenks.png'
    for semana in semanas[40:50]:
        image_path = os.path.join(path, f'{name}_semanas_{semana}_Jenks.png')
        im = Image.open(image_path)
        images.append(lowerImageResolution(im, 19))
        print('load', image_path)


    print('creando gif de', len(images), 'imagenes')
    images[0].save(os.path.join(path, f'{name}.gif'), save_all=True, 
        append_images=images[1:], optimize=False, duration=1000, loop=0)
    print(name, 'Finalizado.')
    images = []

print('*** Proceso finalizado ***')
'''