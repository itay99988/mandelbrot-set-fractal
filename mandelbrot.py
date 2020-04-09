"""
Mandelbrot set fractal generator - Itay Cohen
"""

import numpy as np
import matplotlib.cm as cm
from PIL import Image

IMG_WIDTH       = 800
IMG_HEIGHT      = 600
X_MIN_BOUND     = -2.2
X_MAX_BOUND     = 0.2
Y_MIN_BOUND     = -2.1
Y_MAX_BOUND     = 1.3

ITER_NUM        = 1000
THRESHOLD       = 2
COLOR_VEC       = np.array([255, 255, 255])

def doesSeriesConverge(c):
    z = 0 + 0j
    
    for i in range(ITER_NUM):
        if np.abs(z) > THRESHOLD:
            return i
        z_next = z*z + c
        z = z_next

    return 0
    
def RGBMap(c):
    thresh_count = doesSeriesConverge(c)
    if thresh_count == 0:
        return [0,0,0]
    return np.array(cm.flag(thresh_count/ITER_NUM)[0:3]) * COLOR_VEC
    
def calcStep(img_dim, min_val, max_val):
    return (max_val - min_val) / img_dim

def composeImg(img_data, xmin, xmax, ymin, ymax, img_width, img_height):
    z = np.complex(X_MIN_BOUND,Y_MAX_BOUND)
    x_step = calcStep(IMG_HEIGHT, xmin, xmax)
    y_step = calcStep(IMG_WIDTH, ymin, ymax)
    
    for x_val in range(IMG_HEIGHT):
        for y_val in range(IMG_WIDTH):
            img_data[x_val,y_val] = RGBMap(z)
            z = np.complex(z.real + x_step, z.imag)
        z = np.complex(X_MIN_BOUND, z.imag - y_step)
        print("finished processing row num " + str(x_val))
    
'main'
img_data = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.uint8)
composeImg(img_data, X_MIN_BOUND, X_MAX_BOUND, Y_MIN_BOUND, Y_MAX_BOUND,
           IMG_WIDTH, IMG_HEIGHT)
    
img = Image.fromarray(img_data, 'RGB')
img.save('result.png')
img.show()
