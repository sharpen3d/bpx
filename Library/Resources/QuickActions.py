import bpy
import os.path
from bpy.props import *

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
fileBaseName = thisFileName.replace(".blend", "")
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]

contrast = 0
parentBoneName = ""
savedBoneName = ""
acitve = None

class RecursiveArmature(bpy.types.Operator):
    bl_idname = "scene.recursivearmature"
    bl_label = "Make Armature Structure"
    bl_description = ""
    
    def execute(self, context):
        #TODO
        #name bones
        #transfer animation
        #make Unity Panel
        
        scene = bpy.context.scene
        global active
        global parentBoneName
        
        rootName = active.name
        print(active.name)

        i=0
        while i < len(active.children):
            
            #set location to child
            loc = active.children[i].matrix_world.translation
            
            #set cursor to childLoc
            bpy.context.scene.cursor.location = loc
            
            #add bone at cursor
            newBone = bpy.ops.armature.bone_primitive_add()
            
            #select new bone
            bpy.ops.armature.select_more()
            
            #get selected bone name
            boneName = bpy.context.selected_bones[0].name
            
            #set new bone parent
            bpy.context.object.data.edit_bones[boneName].parent = bpy.context.object.data.edit_bones[parentBoneName]
            
            #check if child has children
            if len(active.children[i].children) > 0:
                active = active.children[i]
                parentBoneName = boneName
                print(i)
                bpy.ops.scene.recursivearmature()
                active = active.parent
                parentBoneName = bpy.context.object.data.edit_bones[boneName].parent.name
                
            i += 1
                
        return {"FINISHED"}

class EmptyToArmature(bpy.types.Operator):
    bl_idname = "scene.emptytoarmature"
    bl_label = "Make Armature Structure"
    bl_description = "Make Armature structure on parented objects"
    
    def execute(self, context):
        scene = bpy.context.scene
        global active
        global parentBoneName
        
        active = bpy.context.object
        rootName = active.name
        loc = active.location
        
        #add root armature bone
        bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(loc), scale=(1, 1, 1))
        bpy.ops.armature.select_more()
        parentBoneName = bpy.context.selected_bones[0].name
        
        bpy.ops.scene.recursivearmature()        
        bpy.ops.object.editmode_toggle()
                
        return {"FINISHED"}
     
class SpaceXWithCam(bpy.types.Operator):
    bl_idname = "scene.spacexwithcam"
    bl_label = "Center X Location"
    bl_description = "Selection to cursor X (keep offset)"
    
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
    bl_description = "Selection to cursor Y (keep offset)"
    
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
    bl_description = "Selection to cursor Z (keep offset)"
    
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
    bl_description = "Render frame at 100% render size"
    
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
    bl_description = "Render animation at 100% render size"
    
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
    bl_description = "Render frame at 25% render size"
    
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
    bl_description = "Render frame at 50% render size"
    
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
    bl_description = "Render animation at 25% render size"
    
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
    bl_description = "Render animation at 50% render size"
    
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
    bl_description = "Set up HDRI map nodes in World Shader Nodes"

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

class DisableCM(bpy.types.Operator):
    bl_idname = "scene.disablecm"
    bl_label = "Disable Color Management"
    bl_description = "Set color management display device to NONE"

    def execute(self, context):
        bpy.context.scene.display_settings.display_device = 'sRGB'
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1
        bpy.context.scene.view_settings.use_curve_mapping = False
        
        return {"FINISHED"}

class ResetCM(bpy.types.Operator):
    bl_idname = "scene.resetcm"
    bl_label = "Reset Color Management"
    bl_description = "Set color management display device to sRGB"

    def execute(self, context):
        bpy.context.scene.display_settings.display_device = 'sRGB'
        bpy.context.scene.view_settings.view_transform = 'Filmic'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1
        bpy.context.scene.view_settings.use_curve_mapping = False
        
        return {"FINISHED"}
    
class BoostContrast(bpy.types.Operator):
    bl_idname = "scene.boostcontrast"
    bl_label = "Boost Contrast"
    bl_description = "Toggle through color management contrast options"

    def execute(self, context):
        global contrast
        
        if contrast == 0:
            bpy.context.scene.view_settings.look = 'Medium High Contrast'
        elif contrast == 1:
            bpy.context.scene.view_settings.look = 'High Contrast'
        elif contrast == 2:
            bpy.context.scene.view_settings.look = 'Very High Contrast'
        elif contrast == 3:
            bpy.context.scene.view_settings.look = 'None'
        elif contrast == 4:
            bpy.context.scene.view_settings.look = 'Medium High Contrast'
    
        contrast = contrast+1
        if contrast > 4:
            contrast = 0
        
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
        global contrast
        setContrast = "Contrast is Standard"
        buttonContrast = "Boost Contrast"
        
        if contrast == 0:
            setContrast = "Contrast is Standard"
            buttonContrast = "Boost Contrast"
        elif contrast == 1:
            setContrast = "Contrast is Medium High"
            buttonContrast = "Boost Contrast"
        elif contrast == 2:
            setContrast = "High Contrast"
            buttonContrast = "Boost Contrast"
        elif contrast == 3:
            setContrast = "Very High Contrast"
            buttonContrast = "Reset Contrast"
        
        scene = bpy.context.scene
        render = scene.render        
        layout = self.layout
        
        layout.label(text="Scene Rig")
        row = layout.row()       
        row.operator("scene.emptytoarmature")   

        layout.label(text="Scene Color")
        row = layout.row()       
        row.operator("scene.hdriworld")   
        
        layout.label(text="Color Management")  
        row = layout.row()       
        row.operator("scene.disablecm")  
        row = layout.row()       
        row.operator("scene.resetcm")  
        row = layout.row()      
        layout.label(text= setContrast)
        row = layout.row() 
        row.operator("scene.boostcontrast", text= buttonContrast)          
    
        layout.label(text="Center Objects on 3D Cursor  ")    
        row = layout.row()
        row.operator("scene.spacexwithcam")        
        row = layout.row()
        row.operator("scene.spaceywithcam")        
        row = layout.row()
        row.operator("scene.spacezwithcam")        
        row = layout.row()
        
        
bpy.utils.register_class(QuickActions)  
bpy.utils.register_class(EmptyToArmature)  
bpy.utils.register_class(RecursiveArmature)  
bpy.utils.register_class(QuickActions2) 
bpy.utils.register_class(RenderFull)  
bpy.utils.register_class(RenderPreviewSmall)  
bpy.utils.register_class(RenderPreview)
bpy.utils.register_class(AnimFull)    
bpy.utils.register_class(AnimPreviewSmall)  
bpy.utils.register_class(AnimPreview)  
bpy.utils.register_class(CreateHDRI)  
bpy.utils.register_class(WM_OT_path_open)
bpy.utils.register_class(SpaceXWithCam)
bpy.utils.register_class(SpaceYWithCam)
bpy.utils.register_class(SpaceZWithCam)
bpy.utils.register_class(DisableCM)
bpy.utils.register_class(ResetCM)
bpy.utils.register_class(BoostContrast)