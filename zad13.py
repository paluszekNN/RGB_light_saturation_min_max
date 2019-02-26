from PIL import Image
import glob
import math


def check_color_v(color_v):
    if color_v < 0:
        return 0
    elif color_v > 255:
        return 255
    else:
        return color_v


def change_rgb(im, color, name):
    pix = im.load()
    red = []
    green = []
    blue = []
    for h in range(im.size[1]):
        red.append([])
        green.append([])
        blue.append([])
        for w in range(im.size[0]):
            red[h].append(pix[w, h][0])
            green[h].append(pix[w, h][1])
            blue[h].append(pix[w, h][2])
            if name == 'saturation':
                L = (max(red[h][w]/255, green[h][w]/255, blue[h][w]/255)+min(red[h][w]/255, green[h][w]/255, blue[h][w]/255))/2
                if L < 1.0 and L > 0:
                    S = (max(red[h][w]/255, green[h][w]/255, blue[h][w]/255) -
                         min(red[h][w]/255, green[h][w]/255, blue[h][w]/255))/(1 - math.fabs(2*L - 1))

                if L == 1 and L == 0:
                    S = 0
                red_change = check_color_v(int(red[h][w]+red[h][w]*S))
                green_change = check_color_v(int(green[h][w]+green[h][w]*S))
                blue_change = check_color_v(int(blue[h][w]+blue[h][w]*S))
            elif name == 'max':
                max_color = max(red[h][w]/255, green[h][w]/255, blue[h][w]/255)
                red_change = check_color_v(int(red[h][w] * max_color))
                green_change = check_color_v(int(green[h][w] * max_color))
                blue_change = check_color_v(int(blue[h][w] * max_color))
            elif name == 'min':
                min_color = min(red[h][w] / 255, green[h][w] / 255, blue[h][w] / 255)
                red_change = check_color_v(int(red[h][w] * min_color))
                green_change = check_color_v(int(green[h][w] * min_color))
                blue_change = check_color_v(int(blue[h][w] * min_color))
            else:
                red_change = check_color_v(int(red[h][w]*color[0]))
                green_change = check_color_v(int(green[h][w]*color[1]))
                blue_change = check_color_v(int(blue[h][w]*color[2]))

            pix[w, h] = (red_change, green_change, blue_change)
    im.save('img_'+name+'.png')

    for h in range(im.size[1]):
        for w in range(im.size[0]):
            pix[w, h] = (red[h][w], green[h][w], blue[h][w])


image_list = [Image.open(item)
              for i in [glob.glob('*.%s' % ext)
                        for ext in ["jpg", "gif", "png"]] for item in i]

for im in image_list:
    change_rgb(im, (1, 0, 0), "red")
    change_rgb(im, (0, 1, 0), 'green')
    change_rgb(im, (0, 0, 1), 'blue')
    change_rgb(im, (1.2, 1.2, 1.2), 'light')
    change_rgb(im, (1, 1, 1), 'saturation')
    change_rgb(im, (1, 1, 1), 'min')
    change_rgb(im, (1, 1, 1), 'max')
