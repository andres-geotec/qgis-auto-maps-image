from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
import os

dataMaps = [{
    "file": "ingreso_sintomas_todos.csv",
    'title': 'Respuesta hospitalaria',
    'subtitle': 'Tiempo promedio entre fecha de ingreso y resultado',
    'date': '19 de Noviembre de 2020',
    'note': "Promedio municipal de días desde 'FECHA_INGRESO' a 'FECHA_RESULTADO'. Para los municipios con menos de 3 casos positivos se utilizó el promedio por jurisdicción sanitaria.",
    'source': 'Secretaría de Salud: "201119COVID19MEXICOTOT" de la Dirección General de Epidemiología',
    'legend': 'Días Promedio',
    'variant': 'tiempo_resultado_ingreso',
    'targetFieldName': 'cvegeomun'
}]

#Instance path proyect application
path = '/home/andres/Proyectos/CONACyT/AtencionHospitalaria/auto-map-tiempo-hospital/data'
os.chdir(path)
project = QgsProject()

#Municipios
path_muns_gpkg = "mun_2019.gpkg"
gpkg_muns_layer = path_muns_gpkg + "|layername=mun_2019"
muns = QgsVectorLayer(gpkg_muns_layer, "Municipios", "ogr")



uri = f"file://{os.getcwd()}/resultado_ingreso_todes.csv?delimiter=,"
infoLyr = QgsVectorLayer(uri, 'resultado_ingreso_todes', 'delimitedtext')
infoLyr.isValid()
QgsProject.instance().addMapLayer(muns)
QgsProject.instance().addMapLayer(infoLyr)

join = QgsVectorLayerJoinInfo()
join.setJoinFieldName('cvegeomun')
join.setTargetFieldName('cvegeomun')
join.setJoinLayer(infoLyr)
join.setUsingMemoryCache(True)
#join.setPrefix('_')
muns.addJoin(join)


muns.removeJoin(join.joinLayerId())
