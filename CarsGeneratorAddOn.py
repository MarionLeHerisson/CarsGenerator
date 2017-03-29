bl_info = {
    "name": "Cars Generator", 
    "category": "Object", 
    "author": "Cottet & Hurteau"
}

import bpy, os, math, random
import random

class ObjectMoveX(bpy.types.Operator):
    """It generates cars !"""          # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # unique identifier for buttons and menu items to reference.
    bl_label = "CarsGenerator"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        voiture()
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(ObjectMoveX)


def unregister():
    bpy.utils.unregister_class(ObjectMoveX)


def createMeshFromData(name, origin, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
 
    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    ob.select = True
 
    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()    
    return ob

def voiture(
        origin=(0,0,0),
        dimensionMax=(2,6,2),
        dimensionMin=(0.5,2,1)
    ):
        
    def createMeshFromOperator(verts, faces):
        bpy.ops.object.add(
            type='MESH', 
            enter_editmode=False,
            location=origin)
        ob = bpy.context.object
        me = ob.data
 
        me.from_pydata(verts, [], faces)
        me.update()
        bpy.ops.object.mode_set(mode='OBJECT')
        return ob
    
    posx=origin[0]
    posy=origin[1]
    posz=origin[2]
    xMax=dimensionMax[0]
    yMax=dimensionMax[1]
    zMax=dimensionMax[2]
    xMin=dimensionMin[0]
    yMin=dimensionMin[1]
    zMin=dimensionMin[2]
    
    #dimension de la voiture
    x=random.randrange(int(xMin*100), int(xMax*100))/100.00
    y=random.randrange(int(yMin), int(yMax*100))/100.00 
    z=random.randrange(int(zMin*100), int(zMax*100))/100.00    
    
    xStruct=x
    yStruct=random.randrange(int(0.25*y*100), int((0.75*y)*100))/100.00
    zStruct=random.randrange(int(0.25*z*100), int(z*100))/100.00
    
    xFront=random.randrange(0, int(x*100))/100.00
    yFront=random.randrange(0, int((y-yStruct)*100))/100.00
    zFront=random.randrange(0, int(zStruct*100))/100.00
    
    xBack=random.randrange(0, int(x*100))/100.00
    yBack=y-yStruct-yFront
    zBack=random.randrange(0, int(z*100))/100.00
    
    xRoof=random.randrange(int(xStruct/2),int(xStruct*100))/100.00
    yRoof=random.randrange(50, int(yStruct*100))/100.00
    zRoof=z-zStruct
    
    wheelSize=random.randrange(30, 100)/100
    wheelWidth=random.randrange(85, 400, 5)/1000
    posXWheel=xStruct/2#random.randrange(int(((xStruct/2))*100), int((xStruct/2)*100))/100
    posZWheel=wheelSize/2
    posYFrontWheel= (0.75*y)+posy-(x/2)
    posYBackWheel= 0.25*y+posy-x/2
    print(wheelWidth)
    
    def createStruct():
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(origin[0],origin[1],origin[2]+zStruct/2))
        bpy.ops.transform.resize(value=(xStruct,yStruct,zStruct))
        #Right side
        (mx,my,mz) = (xStruct/2, yStruct, 0.965926)
        verts = ((x,x,-1), (x,-x,-1), (-x,-x,-1), (-x,x,-1), (0,0,1))
        faces = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
        #createMeshFromOperator(verts, faces)
        
    def createWheels():
        pos=(origin[0], origin[1]+yStruct/2+yFront/2, origin[2]+zFront/2)
        bpy.ops.mesh.primitive_cylinder_add(radius=wheelSize, depth=wheelWidth,location=(posXWheel,posYFrontWheel,posZWheel))
        bpy.ops.transform.rotate(value=1.5, axis=(0,1,0), constraint_axis=(False, True, False))
        
    def createFront():
        pos=(origin[0], origin[1]+yStruct/2+yFront/2, origin[2]+zFront/2)
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(pos))
        bpy.ops.transform.resize(value=(xFront,yFront,zFront))
        
    def createBack():
        posYBack = origin[1]-((yStruct/2)+(yBack/2))
        pos=(origin[0], posYBack, origin[2]+zBack/2)
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(pos))
        bpy.ops.transform.resize(value=(xBack,yBack,zBack))
        
    def createRoof():
        pos=(origin[0], origin[1], origin[2]+zStruct+zRoof/2)
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(pos))
        bpy.ops.transform.resize(value=(xRoof,yRoof,zRoof))
        
        
    
    'lumiere'
    '''scene = bpy.context.scene
    lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
    lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
    scene.objects.link(lamp_object)
    lamp_object.location = (x+5.0, y+5.0, z+5.0)
    lamp_object.select = True
    scene.objects.active = lamp_object'''
    
    createStruct()
    createFront()
    createBack()
    createRoof()
    createWheels()
            
            
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()