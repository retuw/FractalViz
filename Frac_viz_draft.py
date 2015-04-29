'''
    Fractal Audio Visualizer by Pearce Reinsch
        Abstract: Audio visualizer which animates 3D cube objects in a 2D matrix
                The cube objects are animated along with the audio on the Z axis
                The color of the cube is determined using a fractal (Julia Set) algorithm.
'''

import bpy
import random

bpy.ops.object.select_by_type(type = 'MESH')
bpy.ops.object.delete(use_global = False)

rows = 5
columns = 5
rowCounter = 0
columnCounter = 0
red = 0
blue = 0
green = 0
bpy.ops.mesh.primitive_plane_add(radius = 25, location = (0,0,-1))

def fractalPixels(x,y):
    xLeft = -2.0
    xRight = 2.0
    yTop = -1.5
    yBottom = 1.5
    maxIt = 177
    while True:
        cx = random.random() * (xRight - xLeft) + xLeft
        cy = random.random() * (yBottom - yTop) + yTop
        c = cx + cy * 1j
        z = c
        for i in range(maxIt):
            if abs(z) > 2.0:
                break 
            z = z * z + c
        if i > 10 and i < 100:
            break


    for y in range(rows):
    # generate the RGB values from the Julia set
        zy = y * (yBottom - yTop) / (rows - 1)  + yTop
        for x in range(columns):
            zx = x * (xRight - xLeft) / (columns - 1)  + xLeft
            z = zx + zy * 1j
            for i in range(maxIt):
                if abs(z) > 2.0:
                    break 
                z = z * z + c
            red = ((i  *32) % 100) / 100
            green = ((i  * 16) % 100) / 100
            blue = ((i  * 8) % 100) / 100
            rgb = [red, green, blue]
            print(rgb)
            if y == rowCounter and x == columnCounter:
                return rgb
    return rgb

for i in range(0, rows * columns):
    if columnCounter == columns:
        rowCounter += 1
        columnCounter = 0
    #^^^If the end of the row is reached, reset column counter and itterate row counter to the next row
            
    bpy.ops.mesh.primitive_cube_add(location = ((rowCounter/1.5) * 2, (columnCounter/1.5) * 2, 1))
        #^^^places a new cube on the 3D plane and sets the starting location in the 3D space
    bpy.context.object.name = "Freq Bar"
        #^^^Names the new cube
    bpy.context.scene.cursor_location = bpy.context.active_object.location
        #^^^Moves the cursor to the newly created cube
    bpy.context.scene.cursor_location.z -= 1  
        #^^^moves cursor to bottom of object to restrict the movement to only 'up' direction
    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')
    
    rgb = fractalPixels(rowCounter, columnCounter)
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
        #^^^Assigns RGB values by calling a Fractal function based on the objects location in the object matrix
    
    bpy.ops.material.new()
        #^^^Makes a new 'material' for the bar object
    barColor = bpy.data.materials[-1]
        #^^^Saves the new material at the end of the available materials list as a variable 'barColor'
    barColor.name = "Color"
        #^^^Names the new material 'Color'
    barColor.diffuse_color = (red,green,blue)
        #***** shading emit 2
        #***** world settings : indirect lighting 2-3 passes
        #^^^Assigns the currently stored RGB values to the current material
    
    bpy.ops.object.material_slot_add()
        #^^^Adds a new material slot to the current object
    bpy.context.active_object.active_material = barColor
        #^^^Adds the newly created material to the new material slot of the current object
    bpy.context.object.active_material.diffuse_intensity = 1
        #^^^Turns the diffuse setting to the max setting for current object's material
    bpy.context.object.active_material.specular_intensity = 0.0
        #^^^Turns the specular setting to the min setting for current object's material
    bpy.context.object.active_material.emit = 2
        #^^^Sets the shadow emission of the current object
    #bpy.context.space_data.context = 'WORLD'
    #bpy.context.scene.world.light_settings.use_indirect_lighting = True
    #bpy.context.scene.world.light_settings.gather_method = 'APPROXIMATE'
    #bpy.context.scene.world.light_settings.passes = 3
    
    bpy.context.active_object.scale.x = 0.5
    bpy.context.active_object.scale.y = 0.5
    bpy.context.active_object.scale.z = 1.0
        #^^^sets the size of the new cube on all 3 axises
    bpy.ops.object.transform_apply(scale = True)
        #^^^Allows animation of the objects shape
    
    bpy.ops.anim.keyframe_insert_menu(type = 'Scaling')
        #^^^Creates a keyframe to set time when objects will start their animation
    
    bpy.context.active_object.animation_data.action.fcurves[0].lock = True
    bpy.context.active_object.animation_data.action.fcurves[1].lock = True
        #^^^Locks the X & Y axises, only allowing animation on the Z axis
    
    bpy.context.area.type = 'GRAPH_EDITOR'
        #^^^Switches area to graph editor to allow sound baking
    
    freq = 7000 / (rows * columns)
    lowEnd = (i * freq)
    highEnd = (i * freq + freq)
        #^^^Separates the maximum frequency range by the total possible amount of objects in the matrix
    file_path = "/Users/Seichan/Documents/CSITin3/Spring2015/CST-205/FinalProject/Moon.wav"
        #^^^File path of the audio file
    bpy.ops.graph.sound_bake(filepath = file_path, low = lowEnd, high = highEnd)
        #^^^Animates the object on the Z axis using the f-curves from the audio file
    
    bpy.context.active_object.animation_data.action.fcurves[2].lock = True
        #^^^Locks animation on the Z axis to prevent unintentional changes
    
    columnCounter += 1
        #^^^Moves couner to next object on the current row