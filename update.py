from PIL import Image
import webcolors
import os
import datetime
import cv2

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def get_percentage(path, color):
    im = Image.open(path)
    pix = im.load()
    (width, height) = im.size

    color_count = {'red':0, 'orange':0, 'yellow':0, 'green':0, 'blue':0, 'purple':0}

    for x in range(width):
        for y in range(height):
            name = ''
            actual_name, closest_name = get_colour_name(pix[x,y])
            if actual_name is None:
                name = closest_name
            else:
                name = actual_name
            print name
            if 'red' in name or 'maroon' in name or 'tomato' in name:
                color_count['red'] += 1

            if 'orange' in name:
                color_count['orange'] += 1

            if 'yellow' in name or 'gold' in name:
                color_count['yellow'] += 1

            if 'green' in name or 'mintcream' in name:
                color_count['green'] += 1

            if 'blue' in name or 'azure' in name or 'navy' in name or 'turquoise' in name or 'indigo' in name or 'teal' in name and 'lightslateblue' not in name and 'steelblue' not in name:
                color_count['blue'] += 1

            if 'purple' in name or 'violet' in name or 'plum' in name or 'orchid' in name or 'rose' in name or 'lavender' in name or 'thistle' in name or 'mageneta' in name or 'lightslateblue' in name or 'steelblue' in name:
                color_count['purple'] += 1

    total = 0.0

    for item in color_count:
        total += color_count[item]

    color_percentages = {}

    for item in color_count:
        color_percentages[item] = color_count[item] / total

    print color, ':', color_percentages

    print color, ':', round(color_percentages[color]*100)
    return round(color_percentages[color]*100)

##################################################################
# ONLY UNCOMMENT FOR PRODUCTION READY CODE  - DO NOT RUN LOCALLY #
#                                                                #
# This method commits results of get_percentage() to GitHub      #
# and updates the CSS for AreWeSortedYet.com. Be careful!        #
##################################################################
def push_update(percentages):
    """Takes a dictionary of percentages, color name being the key
    and rounded float as value (Ex. 'red':93.0)."""
    css = open('css/heights.css', 'w')
    new_code = '#red {height:%(red)s%%} #orange {height:%(orange)s%%} #yellow {height:%(yellow)s%%} #green {height:%(green)s%%} #blue {height:%(blue)s%%} #purple {height:%(purple)s%%}'
    new_code = new_code % percentages
    css.write(new_code)
    css.close()

    # THIS IS THE MOST DANGEROUS CODE YOU'LL EVER SEE IN YOUR LIFE DO NOT RUN
    # os.system('git add css/heights.css')
    # os.system('git commit -m "Auto-Update ' + str(datetime.datetime.now()) + '"')
    # os.system('git push origin gh-pages')

if __name__ == '__main__':
    image_paths = {'red':'red.jpg',
                   'orange':'orange.jpg',
                   'yellow':'yellow.jpg',
                   'green':'green.jpg',
                   'blue':'blue.jpg',
                   'purple':'purple.jpg'
                  }

    color_percentages = {'red':0.0, 'orange':0.0, 'yellow':0.0, 'green':0.0, 'blue':0.0, 'purple':0.0}

    #for color in image_paths:
    #    color_percentages[color] = get_percentage(image_paths[color], color)
    color_percentages[color] = get_percentage(image_paths['purple'], 'purple')
    for percent in color_percentages:
        print percent, ':', color_percentages[percent]

    push_update(color_percentages)

# Captures a single image from the camera and returns it in PIL format
def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im

def take_picture():
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 0

    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30

    # Now we can initialize the camera capture object with the cv2.VideoCapture class.
    # All it needs is the index to a camera port.
    camera = cv2.VideoCapture(camera_port)

    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    for i in xrange(ramp_frames):
        temp = get_image()
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = get_image()
    file = "./ball_pit.png"
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)

    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    del(camera)

def save_masked_images():
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    ball_pit_img = cv2.imread('./ball_pit.png')
    for color in colors:
        mask = cv2.imread('./masks/' + color + '_mask.png')
        new_img = cv2.bitwise_and(ball_pit_img, mask)
        cv2.imwrite('./' + color + '.png', new_img)
