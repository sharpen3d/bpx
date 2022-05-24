import bpy
import os.path
from bpy.props import *

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
fileBaseName = thisFileName.replace(".blend", "")
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]

class AppendGridPack(bpy.types.Operator):
    bl_idname = "scene.appendgridpack"
    bl_label = "Append Grid Packing"
    
    def execute(self, context):
        path = "\\\\NCFS1\\Dev\\Art\\_ArtistShareables_\\blenderTemplates\\packToGrid.blend"
        subFolder = "\\Scene\\"
        object = "packScene"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
        
        path = "\\\\NCFS1\\Dev\\Art\\_ArtistShareables_\\blenderTemplates\\packToGrid.blend"
        subFolder = "\\WorkSpace\\"
        object = "packing"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
        
                       
        return {"FINISHED"}

class StoreImages2(bpy.types.Operator):
    bl_idname = "scene.storeimagesa"
    bl_label = "collect images in folder"
    
    def execute(self, context):
        renderpath = currentPath+"//images\\"
        bpy.context.scene.render.filepath = renderpath+"//render\\"
        bpy.ops.render.render(animation=False, write_still=True, layer='', scene='Scene')
        
        for img in bpy.data.images:
            if img.name != "Render Result":
                img.reload()
                img.filepath=renderpath+img.name+"."+img.file_format
                img.save()
                img.reload()
                
        return {"FINISHED"}
    
#class AlignX(bpy.types.Operator):
#    bl_idname = "scene.alignx"
#    bl_label = "Align X"
#    
#    def execute(self, context):
#        selected = bpy.context.selected_objects
#        active = bpy.context.object
##        currentScale = [0] * (len(selected)+1)
##        
##        i = 0
##        while i < len(selected):
##            currentScale[i] = selected[i].scale[0]
##            i=i+1
##        
##        bpy.ops.transform.resize(value=(0, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
##        
##        x = 0
##        while x < len(selected):
##            selected[x].scale[0] = currentScale[x]
##            x=x+1

#        for obj in selected:
#            if obj != bpy.context.object:
#                obj.location[0] = active.location[0]

#                
#        return {"FINISHED"}
#    
#class AlignY(bpy.types.Operator):
#    bl_idname = "scene.aligny"
#    bl_label = "Align Y"
#    
#    def execute(self, context):
#        selected = bpy.context.selected_objects
#        active = bpy.context.object
#        for obj in selected:
#            if obj != bpy.context.object:
#                obj.location[1] = active.location[1]
#                
#        return {"FINISHED"}
#    
#class AlignZ(bpy.types.Operator):
#    bl_idname = "scene.alignz"
#    bl_label = "Align Z"
#    
#    def execute(self, context):
#        selected = bpy.context.selected_objects
#        active = bpy.context.object
#        for obj in selected:
#            if obj != bpy.context.object:
#                obj.location[2] = active.location[2]
#                
#        return {"FINISHED"}
#    
class SpaceXWithCam(bpy.types.Operator):
    bl_idname = "scene.spacexwithcam"
    bl_label = "Center X Location"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object
        dist = abs(selected[0].location[0] - selected[1].location[0])
        print(dist)
        cursorx = bpy.context.scene.cursor.location[0]
        if selected[0].location[0] < selected[1].location[0]:
            selected[0].location[0] = cursorx - (dist/2)
            selected[1].location[0] = cursorx + (dist/2)
        else:
            selected[1].location[0] = cursorx - (dist/2)
            selected[0].location[0] = cursorx + (dist/2)
                
        return {"FINISHED"}

class SpaceYWithCam(bpy.types.Operator):
    bl_idname = "scene.spaceywithcam"
    bl_label = "Center Y Location"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object
        dist = abs(selected[0].location[1] - selected[1].location[1])
        print(dist)
        cursorx = bpy.context.scene.cursor.location[1]
        if selected[0].location[1] < selected[1].location[1]:
            selected[0].location[1] = cursorx - (dist/2)
            selected[1].location[1] = cursorx + (dist/2)
        else:
            selected[1].location[1] = cursorx - (dist/2)
            selected[0].location[1] = cursorx + (dist/2)
                
        return {"FINISHED"}

class SpaceZWithCam(bpy.types.Operator):
    bl_idname = "scene.spacezwithcam"
    bl_label = "Center Z Location"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object
        dist = abs(selected[0].location[2] - selected[1].location[2])
        print(dist)
        cursorx = bpy.context.scene.cursor.location[2]
        if selected[0].location[2] < selected[1].location[2]:
            selected[0].location[2] = cursorx - (dist/2)
            selected[1].location[2] = cursorx + (dist/2)
        else:
            selected[1].location[2] = cursorx - (dist/2)
            selected[0].location[2] = cursorx + (dist/2)
                
        return {"FINISHED"}


class RenderFull(bpy.types.Operator):
    bl_idname = "scene.renderfull"
    bl_label = "Render Frame"
    
    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        if (scene.use_stamp_note == ""):
            renderName = fileBaseName
        else:
            renderName = scene.use_stamp_note
        
        render.filepath = "//images//"+"FullSize//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered animation at " + str(newX) + " x " + str(newY))
        
        render.resolution_percentage = revert
        scene.frame_start = revertStart
        scene.frame_end = revertEnd
        render.filepath = revertPath
        
        return {"FINISHED"}

class AnimFull(bpy.types.Operator):
    bl_idname = "scene.animfull"
    bl_label = "Render Animation"
    
    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertPath = render.filepath
        
        if (scene.use_stamp_note == ""):
            renderName = fileBaseName
        else:
            renderName = scene.use_stamp_note
        
        render.filepath = "//images//"+"Sequences//FullSize//"+renderName+"_"

        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered animation at " + str(newX) + " x " + str(newY))
        render.resolution_percentage = revert
        render.filepath = revertPath
        return {"FINISHED"}
    
class RenderPreviewSmall(bpy.types.Operator):
    bl_idname = "scene.renderpreviewsmall"
    bl_label = "25%"
    
    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end   
        revertPath = render.filepath             
        currentFrame = scene.frame_current
        
        if (scene.use_stamp_note == ""):
            renderName = fileBaseName
        else:
            renderName = scene.use_stamp_note
            
        render.filepath = "//images//"+"QuarterSize//"+renderName+"_"
        
        render.resolution_percentage = 25

        newX = round(render.resolution_x/4)
        newY = round(render.resolution_y/4)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered animation at " + str(newX) + " x " + str(newY))
        render.resolution_percentage = revert
        scene.frame_start = revertStart
        scene.frame_end = revertEnd   
        render.filepath = revertPath     
        return {"FINISHED"}
    
class RenderPreview(bpy.types.Operator):
    bl_idname = "scene.renderpreview"
    bl_label = "50%"
    
    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end     
        revertPath = render.filepath           
        currentFrame = scene.frame_current
        
        if (scene.use_stamp_note == ""):
            renderName = fileBaseName
        else:
            renderName = scene.use_stamp_note
        
        render.filepath = "//images//"+"HalfSize//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        render.resolution_percentage = 50

        newX = round(render.resolution_x/2)
        newY = round(render.resolution_y/2)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered animation at " + str(newX) + " x " + str(newY))
        render.resolution_percentage = revert
        scene.frame_start = revertStart
        scene.frame_end = revertEnd     
        render.filepath = revertPath   
        return {"FINISHED"}
    
class AnimPreviewSmall(bpy.types.Operator):
    bl_idname = "scene.animpreviewsmall"
    bl_label = "25%"
    
    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertPath = render.filepath
        render.resolution_percentage = 25
        
        if (scene.use_stamp_note == ""):
            renderName = fileBaseName
        else:
            renderName = scene.use_stamp_note
            
        render.filepath = "//images//"+"Sequences//QuarterSize//"+renderName+"_"
        
        newX = round(render.resolution_x/4)
        newY = round(render.resolution_y/4)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered animation at " + str(newX) + " x " + str(newY))
        render.resolution_percentage = revert
        render.filepath = revertPath
        return {"FINISHED"}
    
class AnimPreview(bpy.types.Operator):
    bl_idname = "scene.animpreview"
    bl_label = "50%"
    
    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertPath = render.filepath
        render.resolution_percentage = 50
        
        if (scene.use_stamp_note == ""):
            renderName = fileBaseName
        else:
            renderName = scene.use_stamp_note
            
        render.filepath = "//images//"+"Sequences//HalfSize//"+renderName+"_"
        
        newX = round(render.resolution_x/2)
        newY = round(render.resolution_y/2)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered animation at " + str(newX) + " x " + str(newY))
        render.resolution_percentage = revert
        render.filepath = revertPath
        return {"FINISHED"}

class CreateHDRI(bpy.types.Operator):
    bl_idname = "scene.hdriworld"
    bl_label = "HDRI world setup"

    def execute(self, context):

        currentscene = bpy.context.scene
        currentworld = currentscene.world

        root = bpy.app.binary_path
        ins = root.replace("blender.exe", "")

        for i in bpy.context.preferences.studio_lights:
            if i.type=='WORLD':
                lightdir = os.path.dirname(i.path)

        path = lightdir + "//courtyard.exr"
        bpy.ops.image.open(filepath=path)

        nodesExist = False
        for i in currentworld.node_tree.nodes:
            if i.name == "custom_hdri":
                nodesExist = True
            
        if nodesExist == False:
            
            imagenode = currentworld.node_tree.nodes.new('ShaderNodeTexEnvironment')
            imagenode.image = bpy.data.images['courtyard.exr']
            imagenode.name = "custom_hdri"

            vect = currentworld.node_tree.nodes.new('ShaderNodeMapping')
            coord = currentworld.node_tree.nodes.new('ShaderNodeTexCoord')    
            world_output = currentworld.node_tree.nodes['World Output']    
            bgnode = currentworld.node_tree.nodes.new('ShaderNodeBackground')
            
            currentworld.node_tree.links.new(world_output.inputs[0], bgnode.outputs[0])
            currentworld.node_tree.links.new(bgnode.inputs[0], imagenode.outputs[0])
            currentworld.node_tree.links.new(vect.inputs[0], coord.outputs[0])
            currentworld.node_tree.links.new(imagenode.inputs[0], vect.outputs[0])

        else:
            print("world nodes already created")
        
        return {"FINISHED"}
    
class WM_OT_path_open(bpy.types.Operator):
    "Open output path in a file browser"
    bl_idname = "wm.path_open"
    bl_label = "Open Directory in Finder"

    filepath = StringProperty(name="File Path", maxlen= 1024)

    def execute(self, context):
        import sys
        import os
        import subprocess
        
        thisFilePath = bpy.data.filepath
        thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
        currentPath = thisFilePath.replace(thisFileName, "")
        
        path = bpy.context.scene.render.filepath
        filepath = currentPath+"//images//"
        filepath = os.path.normpath(filepath)
        
        if not os.path.exists(filepath):
            self.report({'ERROR'}, "File '%s' not found" % filepath)
            return {'CANCELLED'}
        
        if sys.platform == 'win32':
            subprocess.Popen(['start', filepath], shell= True)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', filepath])
        else:
            try:
                subprocess.Popen(['xdg-open', filepath])
            except OSError:
                pass

        return {'FINISHED'}

class QuickActions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Quick Actions"
    bl_label = "Quick Renders"
    bl_idname = "SCENE_PT_layout_custom"

    
    def draw(self, context):        
        scene = bpy.context.scene
        render = scene.render
        
        layout = self.layout 
        
        displayPath = os.path.normpath(currentPath + "//images//")
        layout.label(text="Render Path:  "+ displayPath)
        
        row = layout.row()
        layout.label(text="Name")
        row = layout.row()
        row.prop(scene, "use_stamp_note", text ="")

        row = layout.row()
        row.operator("wm.path_open")   
        
        layout.label(text="Render Current Frame:")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("scene.renderfull")
        row = layout.row()
        row.operator("scene.renderpreviewsmall")
        row.operator("scene.renderpreview")

        row = layout.row()
        layout.label(text="Render Animation:")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("scene.animfull")
        row = layout.row()
        row.operator("scene.animpreviewsmall") 
        row.operator("scene.animpreview")
        
class QuickActions2(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Quick Actions"
    bl_label = "Quick Actions"
    bl_idname = "SCENE_PT_layout_custom1"

    
    def draw(self, context):        
        scene = bpy.context.scene
        render = scene.render        
        layout = self.layout

        #layout.label(text="Actions")
        #row = layout.row()
        #row.operator("scene.storeimagesa")        
#        row = layout.row()
#        row.operator("scene.hdriworld")        
#        row = layout.row()
#        row.operator("scene.alignx")        
#        row = layout.row()
#        row.operator("scene.aligny")        
#        row = layout.row()
#        row.operator("scene.alignz")    
        layout.label(text="Center Objects on 3D Cursor  ")    
        row = layout.row()
        row.operator("scene.spacexwithcam")        
        row = layout.row()
        row.operator("scene.spaceywithcam")        
        row = layout.row()
        row.operator("scene.spacezwithcam")        
        row = layout.row()
        
#        gridpackadded = False
#        for i in bpy.data.scenes:
#            if i.name == "packScene":
#                gridpackadded = True
#            
#        if gridpackadded == False:
#            row.operator("scene.appendgridpack")        
#            row = layout.row()
        
bpy.utils.register_class(QuickActions)  
bpy.utils.register_class(QuickActions2) 
bpy.utils.register_class(RenderFull)  
bpy.utils.register_class(RenderPreviewSmall)  
bpy.utils.register_class(RenderPreview)
bpy.utils.register_class(AnimFull)    
bpy.utils.register_class(AnimPreviewSmall)  
bpy.utils.register_class(AnimPreview)  
bpy.utils.register_class(AppendGridPack)  
bpy.utils.register_class(CreateHDRI)  
bpy.utils.register_class(StoreImages2)
bpy.utils.register_class(WM_OT_path_open)
#bpy.utils.register_class(AlignX)
#bpy.utils.register_class(AlignY)
#bpy.utils.register_class(AlignZ)
bpy.utils.register_class(SpaceXWithCam)
bpy.utils.register_class(SpaceYWithCam)
bpy.utils.register_class(SpaceZWithCam)