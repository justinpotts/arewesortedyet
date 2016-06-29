'''
RGB Default Colors from Photo Sample

Red             228 50 26
Orange          251 121 35
Yellow          254 223 18
Green           78 180 78
Blue            2 68 176
Purple          168 105 201
'''

from PIL import Image
from webcolors import rgb_to_name

imagePath = raw_input('Image Path: ')
im = Image.open(imagePath)
pix = im.load()
(width, height) = im.size

color_count = {'red':0, 'orange':0, 'yellow':0, 'green':0, 'blue':0, 'purple':0}

for x in range(width):
    for y in range(height):
        rgb = str(pix[x,y]).strip('(').strip(')').split(', ')

        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])


        #print r, g, b

        if r in range(208, 248) and g in range(30, 70) and b in range(6, 46):
            color_count['red'] += 1

        if r in range(231, 271) and g in range(101, 141) and b in range(15, 55):
            color_count['orange'] += 1

        if r in range(234, 274) and g in range(203, 243) and b in range(0, 38):
            color_count['yellow'] += 1

        if r in range(58, 98) and g in range(160, 200) and b in range(48, 98):
            color_count['green'] += 1

        if r in range(0, 22) and g in range(48, 88) and b in range(156, 196):
            color_count['blue'] += 1

        if r in range(148, 188) and g in range(85, 125) and b in range(181, 221):
            color_count['purple'] += 1

total = 0.0

for color in color_count:
    total += color_count[color]

color_percentages = {}

for color in color_count:
    color_percentages[color] = color_count[color] / total

for color in color_percentages:
    print color, str(round(color_percentages[color]*100)).split('.')[0] + '%'
