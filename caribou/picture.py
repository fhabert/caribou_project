from PIL import Image
import numpy as np
import random

white = [255, 255, 255]
green = [0, 0, 0]
red = [255, 255, 255]
black = [0, 255, 0]
factor_defo = 0.12
line_black = [green for _ in range(750)]
all_black = [line_black for _ in range(250)]
number_diff = int(factor_defo * 60 * 250)
first_dif = int(number_diff / 2)
array = np.array(all_black)

counter = 0
for i in range(first_dif):
    rand_c = random.randint(65, 115)
    rand_r = random.randint(0, 249)
    array[rand_r][rand_c] = np.array(red)
    counter += 1
    if counter < 250:
        array[counter][60] = black
        array[counter][61] = black
        array[counter][62] = black

counter = 0
for i in range(number_diff):
    rand_c = random.randint(125, 185)
    rand_r = random.randint(0, 249)
    array[rand_r][rand_c] = np.array(red)
    counter += 1
    if counter < 250:
        array[counter][120] = black
        array[counter][121] = black
        array[counter][122] = black

img = Image.fromarray(array, "RGB")
img.save('./images/pov.png')
img.show()
