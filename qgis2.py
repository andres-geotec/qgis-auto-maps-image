
#!/usr/local/bin/python
# coding=latin-1
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os

class MapComposer:
    """PyQGIS Composer class.  Encapsulates boiler plate QgsComposition
    code and centers the QgsComposerMap object on an 8.5x11 inch page."""
    def __init__(self, qmlr=None, qmr=None, lyr=None, **kwargs):
        self.paperWidth = 508
        self.paperHeight = 356
        self.rectScale = 1
        self.xScale = 0.9
        self.yScale = 0.9
        self.qmlr = qmlr
        self.qmr = qmr
        self.__dict__.update(kwargs)
        self.lyrs = self.qmlr.mapLayers().keys()
        self.qmr.setLayerSet(self.lyrs)
        self.rect = QgsRectangle(-117.877, 14.327, -86.097, 32.918)
        self.rect.scale(self.rectScale)
        self.qmr.setExtent(self.rect)
        self.c = QgsComposition(self.qmr)
        self.c.setPlotStyle(QgsComposition.Print)
        self.c.setPaperSize(self.paperWidth, self.paperHeight)
        self.composerMap = QgsComposerMap(self.c, 6, 44, 496, 290)
        self.composerMap.setNewExtent(self.rect)
        self.composerMap.setFrameEnabled(False)
        self.composerMap.setBackgroundColor(QColor(225, 228, 230, 255))
        self.c.addItem(self.composerMap)
        # add min map
        self.minRect = QgsRectangle(-100.629, 17.818, -97.596, 20.566)
        self.minRect.scale(self.rectScale)
        self.composerMinMap = QgsComposerMap(self.c, 10, 210, 132, 120)
        self.composerMinMap.setNewExtent(self.minRect)
        self.composerMinMap.setFrameEnabled(True)
        self.c.addItem(self.composerMinMap)

    def output(self, path, format):
        #self.dpi = self.c.printResolution()
        self.dpi = 280
        self.c.setPrintResolution(self.dpi)
        self.dpmm = self.dpi / 25.4
        self.width = int(self.dpmm * self.c.paperWidth())
        self.height = int(self.dpmm * self.c.paperHeight())
        self.image = QImage(QSize(self.width, self.height), QImage.Format_ARGB32)
        self.image.setDotsPerMeterX(self.dpmm * 1000)
        self.image.setDotsPerMeterY(self.dpmm * 1000)
        self.image.fill(0)
        self.imagePainter = QPainter(self.image)
        self.sourceArea = QRectF(0, 0, self.c.paperWidth(), self.c.paperHeight())
        self.targetArea = QRectF(0, 0, self.width, self.height)
        self.c.render(self.imagePainter, self.targetArea, self.sourceArea)
        self.imagePainter.end()
        self.image.save(path, format)



def newFont(name, size, bold):
    f = QFont()
    f.setBold(bold)
    f.setFamily(name)
    f.setPointSize(size)
    return f

def addLabel(qc, text, font, rect):
    qc.label = QgsComposerLabel(qc.c)
    qc.label.setText(text.decode('utf8'))
    qc.label.setFont(font)
    qc.label.setSceneRect(rect)
    qc.label.setFrameEnabled(False)#True para ver borde
    qc.c.addItem(qc.label)



path = 'C:\\Users\\COMIMSA\\Projects\\CONACyT\\AtencionHospitalaria\\generador-mapas-tiempos-hospitalarios\\data'
os.chdir(path)

reg = QgsMapLayerRegistry.instance()

#generamos un disenador de impresion
mr = iface.mapCanvas().mapRenderer()
qc = MapComposer(qmlr=reg, qmr=mr)

#etiquetas
titulo = 'Respuesta hospitalaria'
subtitulo = 'Tiempo promedio entre fecha de ingreso y resultado'
datetext = 'Actualización de los datos: 20 de Noviembre 2020'
notas = "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_RESULTADO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria."
fuente = 'Secretaría de Salud: "201120COVID19MEXICOTOT" de la Dirección General de Epidemiología.'

addLabel(qc, titulo, newFont('Montserrat', 34, True), QRectF(6, 6, 496, 16))
addLabel(qc, subtitulo, newFont('Montserrat', 30, False), QRectF(6, 22, 496, 12))
addLabel(qc, datetext, newFont('Montserrat', 18, False), QRectF(6, 34, 496, 10))
#mapa(290, 6, 44)
addLabel(qc, 'Notas:', newFont('Montserrat', 18, True), QRectF(6, 336, 24, 10))
addLabel(qc, notas, newFont('Montserrat', 18, False), QRectF(30, 336, 466, 10))
addLabel(qc, 'Fuente de datos:', newFont('Montserrat', 18, True), QRectF(6, 346, 56, 10))
addLabel(qc, fuente, newFont('Montserrat', 18, False), QRectF(62, 346, 434, 10))

#estilos de la leyenda del mapa
qc.legend = QgsComposerLegend(qc.c)
qc.legend.model().setLayerSet(qc.qmr.layerSet())
qc.legend.setItemPosition(364, 64)
qc.c.addItem(qc.legend)

#imagen de conacyt
qc.picture = QgsComposerPicture(qc.c)
qc.picture.setPicturePath('.\\..\\logos\\log_conacyt_horizontal_sin_sintagma.svg')
qc.picture.setSceneRect(QRectF(428, 12, 78, 20))
qc.picture.setFrameEnabled(False)
qc.c.addItem(qc.picture)

#definimos grafico de salida
qc.output("Jurisdicciones.png", "png")