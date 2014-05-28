#!/usr/bin/env python
from gimpfu import *
import random

# create an output function that redirects to gimp's Error Console
def gprint(text):
   pdb.gimp_message(text)
   return 


# our script
def origami_fill(image, drawable, text_value, int_value) :
    image.undo_group_start()
    
    # Determine colors from image
    layerColorPick = image.layers[0]    
    colorBase = generate_color_base(image, layerColorPick, int_value)
        
    image.resize(1000, 1000, 0, 0)
    layerPaperWhite = gimp.Layer(image, "paper white", 1000, 1000, RGB_IMAGE, 100, NORMAL_MODE)
    image.add_layer(layerPaperWhite)
    layerPaperWhite.fill(WHITE_FILL)
    
    layerPaperBase = gimp.Layer(image, "paper base", 1000, 1000, RGB_IMAGE, 85, NORMAL_MODE)
    image.add_layer(layerPaperBase)
    gimp.set_foreground(generate_color_noise(colorBase[2]))
    layerPaperBase.fill(FOREGROUND_FILL)

    layerBase = gimp.Layer(image, "base", 1000, 1000, RGB_IMAGE, 100, NORMAL_MODE)
    layerBase.add_alpha() 
    image.add_layer(layerBase)
    layerBase.fill(TRANSPARENT_FILL)
    
    if (text_value == "crane"):
        create_crane(image, layerBase, colorBase)
    elif (text_value == "butterfly"):
        create_butterfly(image, layerBase, colorBase)
    elif (text_value == "iris"):
        create_iris(image, layerBase, colorBase)
    else:
        create_crane(image, layerBase, colorBase)
    
    # Merge all layers down
    pdb.gimp_selection_none(image)
    layerBase = image.merge_down(layerBase, 0)
    layerBase = image.merge_down(layerBase, 0)
    layerBase.name = "Origami Fill"
    
    image.undo_group_end()
    return


"""Returns list of 3 color bases from the layer based on provided int seed."""
def generate_color_base(image, layerColorPick, int_value):
    colorBase = [(50,50,50), (100,100,100), (150,150,150)]
    
    if (int_value % 4 == 0):
        colorBase[0] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/4, layerColorPick.height*1/4, False, True, 10)
        colorBase[1] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/2, layerColorPick.height*1/2, False, True, 10)
        colorBase[2] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*3/4, layerColorPick.height*3/4, False, True, 10)
    elif (int_value % 4 == 1):
        colorBase[0] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*3/4, layerColorPick.height*3/4, False, True, 10)
        colorBase[1] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/2, layerColorPick.height*1/2, False, True, 10)
        colorBase[2] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/4, layerColorPick.height*1/4, False, True, 10)    
    elif (int_value % 4 == 2):
        colorBase[0] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/3, layerColorPick.height*1/3, False, True, 10)
        colorBase[1] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*2/3, layerColorPick.height*1/3, False, True, 10)
        colorBase[2] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/2, layerColorPick.height*2/3, False, True, 10)
    elif (int_value % 4 == 3):
        colorBase[0] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/3, layerColorPick.height*2/3, False, True, 10)
        colorBase[1] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*2/3, layerColorPick.height*2/3, False, True, 10)
        colorBase[2] = pdb.gimp_image_pick_color(image, layerColorPick, layerColorPick.width*1/2, layerColorPick.height*1/3, False, True, 10)
    
    return colorBase
    
    
"""Returns a color tuple with a random delta noise applied to the provided color tuple"""
def generate_color_noise(color):
    sign = random.randint(0,1)
    sign = -1 if (sign == 0) else 1
    delta = random.randint(25,50)
    newR = max(min(255, color[0] + sign*delta), 0)
    newG = max(min(255, color[1] + sign*random.randint(delta-10, delta+10)), 0)
    newB = max(min(255, color[2] + sign*random.randint(delta-10, delta+10)), 0)
    return (newR, newG, newB)


"""Creates a crane on the base layer"""
def create_crane(image, layerBase, colorBase):
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 10, [0,0 , 750,250 , 1000,1000 , 250,750 , 0,0])
    gimp.set_foreground(generate_color_noise(colorBase[0]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL) 
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 10, [0,0 , 325,225 , 300,300 , 225,325 , 0,0])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 10, [1000,1000 , 1000-325,1000-225 , 1000-300,1000-300 , 1000-225,1000-325 , 1000,1000])
    gimp.set_foreground(colorBase[0])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [0,1000 , 200,500 , 500,800 , 0,1000])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 6, [1000,0 , 800,500 , 500,200 , 1000,0])
    gimp.set_foreground(colorBase[1])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)  

    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [1000,1000 , 800,1000 , 850,850 , 1000,800])
    gimp.set_foreground(colorBase[2])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL) 


"""Creates a crane on the base layer"""
def create_butterfly(image, layerBase, colorBase):
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [0,1000 , 300,1000 , 300,900 , 0,900])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 8, [1000,1000 , 1000-300,1000 , 1000-300,900 , 1000,900])
    gimp.set_foreground(generate_color_noise(colorBase[1]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
       
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 10, [0,0 , 160,240, 160,410, 0,500, 0,0])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 10, [1000,0 , 1000,500, 840,410, 840,240, 1000,0])
    gimp.set_foreground(colorBase[0])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [0,500 , 200,700 , 0,1000])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 6, [1000,500 , 800,700 , 1000,1000])
    gimp.set_foreground(colorBase[1])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [1000,0 , 840,240, 650,0, 1000,0])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 8, [0,0 , 350,0, 160,240, 0,0])
    gimp.set_foreground(colorBase[2])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [350,350 , 650,350 , 650,650 , 350,650])
    gimp.set_foreground(generate_color_noise(colorBase[0]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [160,240 , 160,410 , 500,500])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 6, [1000-160,240 , 1000-160,410 , 500,500])
    gimp.set_foreground(generate_color_noise(colorBase[2]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [350,650 , 650,650 , 650,850 , 350,850])
    gimp.set_foreground(generate_color_noise(colorBase[1]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    

"""Creates an iris flower on the base layer"""
def create_iris(image, layerBase, colorBase):
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [0,0  , 500,500 , 500,0])
    gimp.set_foreground(generate_color_noise(colorBase[2]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [1000,0  , 500,500 , 500,0])
    gimp.set_foreground(generate_color_noise(colorBase[2]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [500,1000  , 500,500 , 0,1000])
    gimp.set_foreground(generate_color_noise(colorBase[2]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 6, [500,1000  , 500,500 , 1000,1000])
    gimp.set_foreground(generate_color_noise(colorBase[2]))
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [0,500  , 500,0 , 1000,500 , 500,1000])
    gimp.set_foreground(colorBase[0])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE, 8, [0,0  , 350,150 , 500,500 , 150,350])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 8, [1000,0  , 1000-350,150 , 500,500 , 1000-150,350])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 8, [0,1000  , 350,1000-150 , 500,500 , 150,1000-350])
    pdb.gimp_image_select_polygon(image, CHANNEL_OP_ADD, 8, [1000,1000  , 1000-350,1000-150 , 500,500 , 1000-150,1000-350])
    gimp.set_foreground(colorBase[1])
    pdb.gimp_edit_fill(layerBase, FOREGROUND_FILL)
    

# This is the plugin registration function
register(
    "origami_fill",    
    "Origami Fill",   
    "Low-Poly Origami Fill",
    "Arpit Sheth & Justin Selig", 
    "Computing in the Arts @ Cornell University", 
    "May 2014",
    "<Image>/MyScripts/Origami Fill", 
    "*", 
    [
      (PF_STRING, 'origami_obj', 'Origami Object', 'crane'),
      (PF_INT, 'img_analysis_procedure', 'Random Integer (Image Analysis)', 2014)
    ], 
    [],
    origami_fill,
    )

main()