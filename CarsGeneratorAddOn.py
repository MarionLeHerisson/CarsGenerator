bl_info = {
    "name": "Cars Generator", 
    "category": "Object", 
    "author": "Cottet & Hurteau"
}

import bpy, os, math
import random
import mathutils
from mathutils import Vector
from math import pi
from bpy.props import FloatVectorProperty, FloatProperty

class CarsGenerator(bpy.types.Operator):
    """It generates cars !"""          # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # unique identifier for buttons and menu items to reference.
    bl_label = "CarsGenerator"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    
    longueurMin = FloatVectorProperty(  
        name="Taille minimal(m)",  
        default=(1.00, 2.00, 1.00),  
        subtype='XYZ',  
        description="move direction"  
    )
    longueurMax = FloatVectorProperty(  
        name="Taille maximal(m)",  
        default=(2.50, 9.00, 3.00),  
        subtype='XYZ',  
        description="move direction"  
    )
    
    
    my_bool = bpy.props.BoolProperty(name="Toggle Option")

    def execute(self, context):        # execute() is called by blender when running the operator.
        print('lMin: ',self.longueurMin[0])
        voiture(dimensionMax=(self.longueurMax[0],self.longueurMax[1],self.longueurMax[2]),
                dimensionMin=(self.longueurMin[0],self.longueurMin[1],self.longueurMin[2]))
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(CarsGenerator)


def unregister():
    bpy.utils.unregister_class(CarsGenerator)



def min(a,b):
    if a<b:
        return a
    else:
        return b
def max(a,b):
    if a>b:
        return a
    else:
        return b

def voiture(
        origin=(0,0,0),
        dimensionMax=(2.5,9,3),
        dimensionMin=(1,2,1)
    ):
        
    def createMeshFromOperator(verts, faces):
        bpy.ops.object.add(
            type='MESH', 
            enter_editmode=False,
            location=origin)
        ob = bpy.context.object
        #ob.name = name
        #ob.show_name = True
        me = ob.data
        #me.name = name+'Mesh'
 
        # Create mesh from given verts, faces.
        me.from_pydata(verts, [], faces)
        # Update mesh with new data
        me.update()    
        # Set object mode
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
    y=random.randrange(int(max(yMin, x)*100), int(yMax*100))/100.00 
    z=random.randrange(int(zMin*100), int(zMax*100))/100.00  
    print('dimensions:',x,' ',y,' ',z)
      
    
    zChassis=random.randrange(1, int(min(40,20*z)))/100.00
    print(zChassis)
    posz=posz+zChassis
    
    xStruct=x
    yStruct=random.randrange(int(0.25*y*100), int((0.75*(y-zChassis))*100))/100.00
    zStruct=random.randrange(int(0.25*z*100), int(0.75*z*100))/100.00
    
    
    
    xFront=random.randrange(int(50*xStruct), int(x*100))/100.00
    yFront=random.randrange(0, int((y-yStruct)*100))/100.00
    zFront=random.randrange(0, int(zStruct*100))/100.00
    
    xBack=random.randrange(int(50*xStruct), int(x*100))/100.00
    yBack=y-yStruct-yFront
    zBack=random.randrange(0, int(z*100))/100.00
    
    xRoof=random.randrange(int((xStruct/2)*100), int(xStruct*100))/100.00
    yRoof=random.randrange(50, int(yStruct*100))/100.00
    zRoof=z-zStruct-zChassis
    
    wheelSize=random.randrange(int(max(30,zChassis*1.25)), 100)/100
    wheelWidth=random.randrange(85, 400, 5)/1000
    posXWheel=(random.randrange(int(((xStruct/2)-wheelWidth/2)*100), int((xStruct/2+wheelWidth/2)*100))/100)
    print('Z')
    print(posz)
    posZWheel=(wheelSize/2)+posz-zChassis
    posYFrontWheel= (0.75*y)+posy-(y/2)
    posYBackWheel= 0.25*y+posy-y/2
    print(wheelWidth)
    
    def createStruct():
        pos=(origin[0],origin[1]+(yBack-yFront)/2,origin[2]+zStruct/2+zChassis)
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=pos)
        bpy.ops.transform.resize(value=(xStruct,yStruct,zStruct))
        #Right side
        (mx,my,mz) = (xStruct/2, yStruct, 0.965926)
        verts = (
            (pos[0]+xStruct/2, pos,-1), 
            
        )
        faces = (
            (1,2,3)
        )
        #createMeshFromOperator(verts, faces)
        
    def createWheels():
        pos=(origin[0], origin[1]+yStruct/2+yFront/2, origin[2]+zFront/2)
        #FRONT
        #Right
        bpy.ops.mesh.primitive_cylinder_add(radius=wheelSize/2, depth=wheelWidth,location=(posXWheel,posYFrontWheel,posZWheel))
        bpy.ops.transform.rotate(value=pi/2, axis=(0,1,0), constraint_axis=(False, True, False))
        #Left
        bpy.ops.mesh.primitive_cylinder_add(radius=wheelSize/2, depth=wheelWidth,location=(-posXWheel,posYFrontWheel,posZWheel))
        bpy.ops.transform.rotate(value=pi/2, axis=(0,1,0), constraint_axis=(False, True, False))
        #BACK
        #Right
        bpy.ops.mesh.primitive_cylinder_add(radius=wheelSize/2, depth=wheelWidth,location=(posXWheel,posYBackWheel,posZWheel))
        bpy.ops.transform.rotate(value=pi/2, axis=(0,1,0), constraint_axis=(False, True, False))
        #Left
        bpy.ops.mesh.primitive_cylinder_add(radius=wheelSize/2, depth=wheelWidth,location=(-posXWheel,posYBackWheel,posZWheel))
        bpy.ops.transform.rotate(value=pi/2, axis=(0,1,0), constraint_axis=(False, True, False))
        
        #bpy.ops.transform.resize(value=(xFront,yFront,zFront))
        
    def createFront():
        pos=(posx, origin[1]+yStruct/2+(yBack-yFront)/2, origin[2]+zFront/2+zChassis)
        #bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(pos[0],pos[1]+yFront/2,pos[2]))
        #bpy.ops.transform.resize(value=(xFront,yFront,zFront))
        
        (mx,my,mz) = (xStruct/2, yStruct, 0.965926)
        verts = (
            #face du bas
            (pos[0]-xStruct/2, pos[1], posz),
            (pos[0]-xFront/2,pos[1],posz),
            (pos[0]-xFront/2,pos[1]+yFront,posz),
            (pos[0]+xStruct/2, pos[1], posz),
            (pos[0]+xFront/2,pos[1],posz),
            (pos[0]+xFront/2,pos[1]+yFront,posz),
            #face haute
            (pos[0]-xStruct/2, pos[1], posz+zStruct),
            (pos[0]+xStruct/2, pos[1], posz+zStruct),
            (pos[0]+xFront/2,pos[1]+yFront,posz+zFront),
            (pos[0]-xFront/2,pos[1]+yFront,posz+zFront),
            
        )
        faces = (
            (0,1,2),#bas gauche
            (3,4,5),#bas droit
            (6,7,8,9),#haut
            (2,5,8,9),#devant
            (0,6,9,2),#gauche
            (3,7,8,5),
            
        )
        #verts = ((x,x,-1), (x,-x,-1), (-x,-x,-1), (-x,x,-1), (0,0,1))
        #faces = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
        createMeshFromOperator(verts, faces)
        
    def createBack():
        posYBack = origin[1]-((yStruct/2)+(yBack/2))+(yBack-yFront)/2
        pos=(origin[0], posYBack, origin[2]+zBack/2+zChassis)
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(pos))
        bpy.ops.transform.resize(value=(xBack,yBack,zBack))
        
    def createRoof():
        pos=(posx, posy+(yBack-yFront)/2, posz+zStruct)
        bpy.ops.mesh.primitive_cube_add(radius=0.5, location=(pos[0],pos[1],pos[2]+zRoof/2))
        bpy.ops.transform.resize(value=(xRoof,yRoof,zRoof))
        
        verts = (
            #face du pare brise
            (pos[0]+xRoof/2, pos[1]+yRoof/2, pos[2]+zRoof),
            (pos[0]-xRoof/2, pos[1]+yRoof/2, pos[2]+zRoof),
            (pos[0]-xStruct/2, pos[1]+yStruct/2,pos[2]),
            (pos[0]+xStruct/2, pos[1]+yStruct/2, pos[2]),
            (pos[0]+xFront/2,pos[1],posz),
            (pos[0]+xFront/2,pos[1]+yFront,posz),
            #face haute
            (pos[0]-xStruct/2, pos[1], posz+zStruct),
            (pos[0]+xStruct/2, pos[1], posz+zStruct),
            (pos[0]+xFront/2,pos[1]+yFront,posz+zFront),
            (pos[0]-xFront/2,pos[1]+yFront,posz+zFront),
            
        )
        faces = (
            (0,1,2,3),#pare brise
            (3,4,5),#bas droit
            
            
        )
        #verts = ((x,x,-1), (x,-x,-1), (-x,-x,-1), (-x,x,-1), (0,0,1))
        #faces = ((1,0,4), (4,2,1), (4,3,2), (4,0,3), (0,1,2,3))
        #createMeshFromOperator(verts, faces)
        
    def test():
        pos=(posx, posy+(yBack-yFront)/2, posz+zStruct)
        print('pos',yBack-yFront)
        yhaut=pos[1]+yRoof/2
        ybas=pos[1]+yStruct/2
        zhaut=pos[2]+zRoof
        zbas=pos[2]
        
        yhautroof=random.randrange(0,30)/100
        verts=[]
        faces=[]
        print('xRoof', xRoof)
        precision=10
        decalageHaut=math.exp((xRoof/2)-(int((xRoof/2)*precision)-int((xRoof/2)*precision)))/10
        decalageBas=math.exp((xStruct/2)-(int((xStruct/2)*precision)-int((xStruct/2)*precision)))/10
        
        for i in range(0, int((xRoof/2)*precision)):
            print('i',i)
            decalageYHaut=decalageHaut-math.exp((xRoof/2)-(int((xRoof/2)*precision)-i/precision*10))/10#math.exp((xRoof/2)*precision-i)/100
            decalageYBas=decalageBas-math.exp((xStruct/2)-(int((xStruct/2)*precision)-i))/10#math.exp((xRoof/2)*precision-i)/100
            
            verts.append((pos[0]+i/precision,yhaut+decalageYHaut,zhaut))
            verts.append((pos[0]+i/precision,ybas+decalageYBas,zbas))
            verts.append((pos[0]-i/precision,yhaut+decalageYHaut,zhaut))
            verts.append((pos[0]-i/precision,ybas+decalageYBas,zbas))
            lv=len(verts)
            if (i>0):
                faces.append((lv-4,lv-3,lv-7,lv-8))
                faces.append((lv-6,lv-5,lv-1,lv-2))
           
        verts.append((pos[0]+i/precision,yhaut+decalageYHaut,zhaut))
        verts.append((pos[0]+i/precision,ybas+decalageYBas,zbas))
        verts.append((pos[0]-i/precision,yhaut+decalageYHaut,zhaut))
        verts.append((pos[0]-i/precision,ybas+decalageYBas,zbas))
        
        for i in range(int((xRoof/2)*precision), int((xStruct/2)*precision)):
            print('ii',i)
            decalageYBas=decalageBas-math.exp((xStruct/2)-(int((xStruct/2)*precision)-i))/10#math.exp((xRoof/2)*precision-i)/100
            
            verts.append((pos[0]+i/precision,yhaut+decalageYHaut,zhaut))
            verts.append((pos[0]+i/precision,ybas+decalageYBas,zbas))
            verts.append((pos[0]-i/precision,yhaut+decalageYHaut,zhaut))
            verts.append((pos[0]-i/precision,ybas+decalageYBas,zbas))
            lv=len(verts)
            if (i>0):
                faces.append((lv-4,lv-3,lv-7,lv-8))
                faces.append((lv-6,lv-5,lv-1,lv-2))
        
        createMeshFromOperator(verts, faces)
    
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
    test()
    createWheels()

           
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
        icon="PLUGIN") 
            
# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()