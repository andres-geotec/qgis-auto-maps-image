import pandas as pd
import datetime
import warnings
import seaborn as sns

fecha_base=datetime.date.today()

#BASES
jurisdicciones=pd.read_csv('data_original/jurisdicciones.csv',dtype={'cvegeomun':str,'nom_juri':str,'cvegeojuri':str})
b=pd.read_csv('data_original/'+str(fecha_base).replace('-','')[2:8]+'COVID19MEXICOTOT.csv',encoding='latin1',dtype={'CLASIFICACION_FINAL':int,'TIPO_PACIENTE':float,'INTUBADO':float,'UCI':float,'EDAD':float,'ENTIDAD_RES':str,'MUNICIPIO_RES':str},low_memory=False)
b.columns=b.columns.str.lower()

#PROCESAMIENTO
#claves para identificar cada municipio
b.insert(0,'cvegeomun',b['entidad_res']+b['municipio_res'])
#para clasificar a los pacientes en positivos (1), negativos (2), pendiente (3)
b.insert(0,'resultado',b['clasificacion_final'].replace({2:1,3:1,7:2,4:3,5:3,6:3}))
#para agregar información de las jurisdicciones sanitarias
b=b.merge(jurisdicciones,on='cvegeomun',how='outer')
#para quitar registros de pacientes sin municipio
b=b[b.cvegeomun.str.contains('999')==False]
#Se introduce fecha dummy 100 dias después del día de hoy para no tener que filtrar de la a los pacientes que tienen alguna de las fechas con las que se harán los cálculos.
fecha_dummy=fecha_base+datetime.timedelta(days=100)
b=b.replace('9999-99-99',fecha_dummy)
#para dar formato a todas las fechas correctamente
for fecha in ['fecha_sintomas','fecha_ingreso','fecha_resultado','fecha_def']:
    b.loc[:,fecha]=pd.to_datetime(b[fecha], format='%Y-%m-%d')
#creación de fecha aproximada del tiempo de estancia en el hospital
b.insert(0,'estancia_hosp',0)
#para los que reciben cuidados intensivos o respirador
b.loc[(b['tipo_paciente']==2),'estancia_hosp']=16
#los que son hospitalizados pero no necesitan cuidados extra
b.loc[((b['tipo_paciente']==2) & (b['intubado']!=1) & (b['uci']!=1)),'estancia_hosp']=10
#los hospitalizados fallecidos
b.loc[((b['tipo_paciente']==2) & (b['fecha_def']!=fecha_dummy)),'estancia_hosp']=b.loc[((b['tipo_paciente']==2) & (b['fecha_def']!=fecha_dummy)),:].apply(lambda x: min(x['estancia_hosp'],(x['fecha_def']-x['fecha_ingreso']).days),axis=1)
#para crear fecha de alta aproximada por paciente
b.insert(0,'fecha_alta',b['fecha_ingreso'])
b.loc[(b['estancia_hosp']>0),'fecha_alta']=b.loc[(b['estancia_hosp']>0),:].apply(lambda x: x['fecha_ingreso']+datetime.timedelta(days=x['estancia_hosp']),axis=1)
#PERIODO ENTRE FECHA DE SÍNTOMAS Y FECHA DE INGRESO
b.insert(0,'tiempo_ingreso_sintomas',[x.days for x in (b['fecha_ingreso']-b['fecha_sintomas'])])
#PERIODO ENTRE FECHA DE INGRESO Y FECHA DE ALTA
b.insert(0,'tiempo_alta_ingreso',[x.days for x in (b['fecha_alta']-b['fecha_ingreso'])])
#PERIODO ENTRE FECHA DE INGRESO Y FECHA DE RESULTADOS
b.insert(0,'tiempo_resultado_ingreso',[x.days for x in (b['fecha_resultado']-b['fecha_ingreso'])])
#PERIODO ENTRE FECHA DE INGRESO Y FECHA DE DEFUNCIÓN
b.insert(0,'tiempo_defuncion_ingreso',[x.days for x in (b['fecha_def']-b['fecha_ingreso'])])
#PERIODO ENTRE FECHA RESULTADOS Y FECHA DE ALTA
b.insert(0,'tiempo_alta_resultado',[x.days for x in (b['fecha_alta']-b['fecha_resultado'])])
#PERIODO ENTRE FECHA RESULTADOS Y FECHA DE DEFUNCIÓN
b.insert(0,'tiempo_defuncion_resultado',[x.days for x in (b['fecha_def']-b['fecha_resultado'])])

def contador(base,nombre):
    muni=base.groupby('cvegeomun')['resultado'].count().reset_index().rename({'resultado':nombre},axis=1)
    mun=jurisdicciones[['cvegeomun','cvegeojuri']].merge(muni,on='cvegeomun',how='outer').fillna({nombre:0})
    return mun

#SEMANAS EPIDEMIOLÓGICAS POR DÍA
nd=(fecha_base-pd.Timestamp(year=2019, month=12, day=29)).days
diasI=[pd.Timestamp(year=2019, month=12, day=29)+pd.Timedelta(days=dia) for dia in range(0,nd)]
valores=[int(dia/7)+1 for dia in range(0,nd)]
semana_epidemiologica_d=pd.DataFrame({'dia':diasI,'semana_epidemiologica':valores}).astype({'semana_epidemiologica':str}).set_index('dia')
semana_epidemiologica_d.loc[:,'semana_epidemiologica']=semana_epidemiologica_d.loc[:,'semana_epidemiologica'].replace({'1':'01','2':'02','3':'03','4':'04','5':'05','6':'06','7':'07','8':'08','9':'09'})
b=b.merge(semana_epidemiologica_d,left_on='fecha_ingreso',right_on='dia',how='outer')
#Conteo
#positivos acumuladas
pp=b[b['resultado']==1]
pMun=contador(pp,'positivos_acumulados')
#ambulatorios acumuladas
aa=pp[(pp['fecha_def']==fecha_dummy) & (pp['tipo_paciente']==1)]
aMun=contador(aa,'ambulatorios_acumulados')
#hospitalizados acumuladas
hh=pp[(pp['fecha_def']==fecha_dummy) & (pp['tipo_paciente']==2)]
hMun=contador(hh,'hospitalizados_acumulados')
#defunciones acumuladas
dd=pp[(pp['fecha_def']!=fecha_dummy)]
dMun=contador(dd,'defunciones_acumuladas')
#todo agrupado
filtros=pMun.merge(aMun,on=['cvegeomun','cvegeojuri'],how='outer').merge(hMun,on=['cvegeomun','cvegeojuri'],how='outer').merge(dMun,on=['cvegeomun','cvegeojuri'],how='outer').fillna({'positivos_acumulados':0,'ambulatorios_acumulados':0,'hospitalizados_acumulados':0,'defunciones_acumuladas':0})

#función para hacer agrupación por jurisdicción y por municipio
#tiene como argumentos un dataframe sobre el que se hacen las agrupaciones (base)
#la variable sobre la que se hacen los promedios (variable)
#la variable con la que se decide si se usa el promedio por jurisdicción o por municipio (filtro)
def agrupador(base,variable,filtro):
    j=base.groupby('cvegeojuri')[variable].mean()
    m=pd.DataFrame(base.groupby('cvegeomun')[variable].mean())
    tabla=filtros.merge(j,on='cvegeojuri',how='outer').merge(m,on='cvegeomun',how='outer',suffixes=('', '_mun'))
    tabla.loc[(tabla[filtro]>3),variable]=tabla.loc[(tabla[filtro]>3),variable+'_mun']
    return tabla.set_index('cvegeomun')[['cvegeojuri',variable]]

#para sacar promedios por jurisdicción
#'tiempo_ingreso_sintomas':TODES
agrupador(b,'tiempo_ingreso_sintomas','positivos_acumulados').to_csv('data_procesada/ingreso_sintomas_todos.csv')

#'tiempo_resultado_ingreso'
#TODES con resultado
agrupador(b[b['fecha_resultado']!=fecha_dummy],'tiempo_resultado_ingreso','positivos_acumulados').to_csv('data_procesada/resultado_ingreso_todes.csv')
#POSITIVOS AMBULATORIOS con resultado
agrupador(aa[(aa['fecha_resultado']!=fecha_dummy)],'tiempo_resultado_ingreso','ambulatorios_acumulados').to_csv('data_procesada/resultado_ingreso_ambulatorios.csv')
#POSITIVOS HOSPITALIZADOS con resultado
agrupador(hh[(hh['fecha_resultado']!=fecha_dummy)],'tiempo_resultado_ingreso','hospitalizados_acumulados').to_csv('data_procesada/resultado_ingreso_hospitalizados.csv')

#'tiempo_alta_ingreso': HOSPITALIZADOS
agrupador(hh,'tiempo_alta_ingreso','hospitalizados_acumulados').to_csv('data_procesada/alta_ingreso_hospitalizados.csv')

#'tiempo_defuncion_ingreso': FALLECIDOS
agrupador(dd,'tiempo_defuncion_ingreso','defunciones_acumuladas').to_csv('data_procesada/defuncion_ingreso_fallecidos.csv')

#'tiempo_alta_resultado':HOSPITALIZADOS con resultado
agrupador(hh[hh['fecha_resultado']!=fecha_dummy],'tiempo_alta_resultado','hospitalizados_acumulados').to_csv('data_procesada/alta_resultado_hospitalizados.csv')

#'tiempo_defuncion_resultado':FALLECIDOS con resultado
agrupador(dd[dd['fecha_resultado']!=fecha_dummy],'tiempo_defuncion_resultado','defunciones_acumuladas').to_csv('data_procesada/defuncion_resultado_fallecidos.csv')

#PARA GIFS por semana epidemiológica
#'tiempo_resultado_ingreso'
variable='tiempo_resultado_ingreso'
#POSITIVOS AMBULATORIOS con resultado
base=aa[(aa['fecha_resultado']!=fecha_dummy)]
tabla=pd.DataFrame(base.groupby(['cvegeojuri','semana_epidemiologica'])[variable].mean()).reset_index()
tPV=tabla.pivot(index='cvegeojuri',columns='semana_epidemiologica',values=variable)
tPV.to_csv('data_procesada/resultado_ingreso_ambulatorios_semanas.csv')
#POSITIVOS HOSPITALIZADOS con resultado
base=hh[(hh['fecha_resultado']!=fecha_dummy)]
tabla2=pd.DataFrame(base.groupby(['cvegeojuri','semana_epidemiologica'])[variable].mean()).reset_index()
tPV2=tabla2.pivot(index='cvegeojuri',columns='semana_epidemiologica',values=variable)
tPV2.to_csv('data_procesada/resultado_ingreso_hospitalizados_semanas.csv')