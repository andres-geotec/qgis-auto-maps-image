from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
import os


path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital'
os.chdir(path)

def quick_export():
    alayer=iface.activeLayer()

    myFile = 'nacional.qpt'
    myTemplateFile = open(myFile, 'rt')
    myTemplateContent = myTemplateFile.read()
    myTemplateFile.close()

    myDocument = QDomDocument()
    myDocument.setContent(myTemplateContent)

    project = QgsProject()
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.loadFromTemplate(myDocument, QgsReadWriteContext())

    base_path = os.path.join(QgsProject.instance().homePath())
    image_path = os.path.join(QgsProject.instance().homePath(), "index.png")

    exporter = QgsLayoutExporter(layout)

    ''''''

    # Add all layers in map canvas to render
    myMapRenderer = iface.mapCanvas().mapRenderer()

    # Load template from file
    myComposition = QgsComposition(myMapRenderer)
    myComposition.loadFromTemplate(myDocument)
    #myComposition.loadFromTemplate(myDocument)


    # Get map composition and define scale
    myAtlasMap = myComposition.getComposerMapById(0)
    myAtlasMap.setAtlasDriven(True)

    # Setup Atlas.
    myAtlas = myComposition.atlasComposition()
    myAtlas.setCoverageLayer(alayer) 
    myAtlas.setComposerMap(myAtlasMap)
    myAtlas.setEnabled(True)
    myAtlas.setHideCoverage(False)
    myAtlasMap.setAtlasScalingMode( QgsComposerMap.Auto )
    # Generate atlas
    myAtlas.beginRender()
    myComposition.setAtlasMode(QgsComposition.ExportAtlas)
    for i in range(0, myAtlas.numFeatures()):
        myAtlas.prepareForFeature( i )
        jobs = r"C:\\Users\\fran\\Desktop\\test\\"
        output_jpeg = jobs + str(i)+ "_BMS_plan.jpg"
        myImage = myComposition.printPageAsRaster(0)
        myImage.save(output_jpeg)
        myComposition.refreshItems()
    myAtlas.endRender()

quick_export()