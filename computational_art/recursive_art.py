"""Author/Artist: Lisa Joelle Hachmann
Artist Statement: My goal was to create 1960's style wall art and iPhone backgrounds.
By adding in tan and arctan, my repository for possible 'trippy' pieces of art exploded.
"""
from __future__ import division
import random
import time
from PIL import Image
from random import choice
import math
from math import pi
def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

    options = ["prod", "sin_pi", "cos_pi" , "avg", 'neg', 'sqrt2']
    singleinput = ['sin_pi', 'cos_pi', 'tan_pi', 'arctan', 'neg', 'sqrt2']
    doubleinput = ['prod', 'avg']
    numoptions = [len(options)]
    xoy = ["x", 'y']
    alloptions = options + xoy

    if max_depth ==0:
        ranfunc = choice(xoy) 
    elif min_depth == 0:
        ranfunc= choice(alloptions)
    else:
        ranfunc = choice(options)
    newmin = min_depth -1
    newmax = max_depth - 1
    if ranfunc in xoy:
        return [ranfunc]
    elif ranfunc in singleinput:
        return [ranfunc, build_random_function(newmin, newmax)]
    elif ranfunc in doubleinput:
        return[ranfunc, build_random_function(newmin, newmax), build_random_function(newmin, newmax)]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    
    #RECURSIVE VERSION
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'cos_pi':
        return math.cos(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'sin_pi':
        return math.sin(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'tan_pi':
        return math.sin(evaluate_random_function(f[1], x, y))/math.cos(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'arctan':
        return 1/(math.tan(evaluate_random_function(f[1], x, y)))
    elif f[0] == 'neg':
        return (-1) * evaluate_random_function(f[1], x,y)
    elif f[0] == 'sqrt2':
        return (1/(math.sqrt(2))*evaluate_random_function(f[1], x, y))
    elif f[0] == 'prod':
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif f[0] == 'avg':
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x,y))

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    if input_interval_start < 0:
        new_in_start = input_interval_start + abs(input_interval_start)
        new_in_end = input_interval_end + abs(input_interval_start)
        new_val = val + abs(input_interval_start)
        portion = float(output_interval_end - output_interval_start) / (new_in_end - new_in_start)
        mapping = float(portion * new_val)
        return mapping
    if input_interval_start >= 0:
        portion = float(output_interval_end - output_interval_start) / (input_interval_end - input_interval_start)
        mapping = float(portion * (input_interval_end - val)) + output_interval_start
        return mapping

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=750, y_size=1334):
    """ Generate computational art and save as an image file.
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(2,4)
    green_function = build_random_function(9,11)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art(str(time.time())+'.png')

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
   #test_image("noise.png")
