from qgis.PyQt.QtXml import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *

import os

def saveAsTemplate(composition):
    doc = QDomDocument()
    composerElem = doc.createElement(  "Composer"  )
    doc.appendChild( composerElem )
    composition.writeXML( composerElem, doc )
    composition.atlasComposition().writeXML( composerElem, doc )
    return doc

def duplicateComposition(composition):
    currentDoc = saveAsTemplate(composition)
    compositionElem = currentDoc.documentElement().firstChildElement( "Composition" )
    if compositionElem.isNull():
        print( "selected composer could not be stored as temporary template" )
        return None

    newComposition = QgsComposition(composition.mapSettings())

    if not newComposition.loadFromTemplate(currentDoc):
        print( " Cannot load template ")
        del newComposition
        return None

    return newComposition


myComposition = iface.activeComposers()[0].composition()
newComposition = duplicateComposition(myComposition)

atlas = newComposition.atlasComposition()
atlasLayer = iface.activeLayer()
atlas.setCoverageLayer(atlasLayer)
atlas.setPageNameExpression(atlasLayer.name())
atlas.setEnabled( True )
ret = newComposition.setAtlasMode( QgsComposition.ExportAtlas )
if ret is False:
    print "Error"


outputDir = "C:/temp/export_atlas"
atlas.beginRender()
print("atlas")
num = atlas.numFeatures()
for i in range(0, num):
    ret = atlas.prepareForFeature( i )
    if ret is False:
        print "prepareForFeatureror"
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    ret = newComposition.exportAsPDF(os.path.join(outputDir, str(i)+".pdf"))
    if ret is False:
        print "exportAsPDF"

atlas.endRender()