from PIL import Image
import os

path = '/home/andres/Proyectos/CONACyT/201119_AtencionHospitalaria/210106COVID19MEXICOTOT/forGifs'
names = ['0_resultado_ingreso_ambulatorios','1_resultado_ingreso_hospitalizados']
images = []

def lowerImageResolution(img, percent):
    def getPercent(n, percent):
        return int(n*(percent/100))
    w, h = im.size
    return im.resize((getPercent(w, percent), getPercent(h, percent)))
for name in names:
    #image_name = '1_resultado_ingreso_hospitalizados_semanas_{}_Jenks.png'
    for i in range(10, 53):
        image_path = os.path.join(path, f'{name}_semanas_{i}_Jenks.png')
        im = Image.open(image_path)
        images.append(lowerImageResolution(im, 19))
        print('load', image_path)


    print('creando gif de', len(images), 'imagenes')
    images[0].save(os.path.join(path, f'{name}.gif'), save_all=True, append_images=images[1:], optimize=False, duration=850, loop=0)
    print(name, 'Finalizado.')
    images = []