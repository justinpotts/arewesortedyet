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

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def get_percentage(path, color):
    im = cv2.imread(path)

    color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    color_count = {'red':0, 'orange':0, 'yellow':0, 'green':0, 'blue':0, 'purple':0}
    color_hues = {'red': 15, 'orange': 45, 'yellow': 70, 'green': 190, 'blue': 260, 'purple': 300}
    min_sat = 0.2

    for col in im:
        for pix in col:
            hsv_pix = rgb2hsv(pix[2], pix[1], pix[0])
            hue = hsv_pix[0]
            sat = hsv_pix[1]

            if sat > min_sat:
                pix_placed = False
                for curr_color in color_list:
                    if not pix_placed and color_hues[curr_color] > hue:
                        pix_placed = True
                        color_count[curr_color] += 1

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
    os.system('git add css/heights.css')
    os.system('git commit -m "Auto-Update ' + str(datetime.datetime.now()) + '"')
    os.system('git push origin gh-pages')

def cleanup():
    os.system('rm *.png')

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
        retval, im = camera.read()
        temp = im
    print("Taking image...")
    # Take the actual image we want to keep
    retval, im = camera.read()
    camera_capture = im
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

if __name__ == '__main__':
    take_picture()
    save_masked_images()

    image_paths = {'red':'red.png',
                   'orange':'orange.png',
                   'yellow':'yellow.png',
                   'green':'green.png',
                   'blue':'blue.png',
                   'purple':'purple.png'
                  }

    color_percentages = {'red':0.0, 'orange':0.0, 'yellow':0.0, 'green':0.0, 'blue':0.0, 'purple':0.0}

    for color in image_paths:
        color_percentages[color] = get_percentage(image_paths[color], color)

    for percent in color_percentages:
        print percent, ':', color_percentages[percent]

    push_update(color_percentages)
    cleanup()
