import bpy
import os.path
import bpy.props

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
fileBaseName = thisFileName.replace(".blend", "")
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]

contrast = 0
parentBoneName = ""
savedBoneName = ""
acitve = None
armatureName = None


class UIMP_settings(bpy.types.PropertyGroup):
    exportpath: bpy.props.StringProperty(
        name="Asset Path",
        default="[i.e. D://Unity//MyProject//Assets]"
    )
    
    subfolder: bpy.props.StringProperty(
        name="Sub-Folder",
        default="[i.e. Art//Scene//Background//Idle]"
    )

    exportname: bpy.props.StringProperty(
        name="Name",
        default="[i.e. BackgroundLoop]"
    )

class UnityLinkFbx(bpy.types.Operator):
    bl_idname = "scene.unitylinkfbx"
    bl_label = "Export selected as FBX"
    bl_description = "Export FBX to Unity Project Asset Folder"
    
    def execute(self, context):
        thisFilePath = bpy.data.filepath
        thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
        fileBaseName = thisFileName.replace(".blend", "")
        currentPath = thisFilePath.replace(thisFileName, "")
        currentPath = currentPath[:-1]
        
        directory = "FBX"
        parent_dir = currentPath
        parent_dir = os.path.normpath(parent_dir)
        path = os.path.join(parent_dir, directory)
        
        isdir = os.path.isdir(path)
        if (isdir == False):
            os.mkdir(path)
        
        objectName  = bpy.context.object.name
        f = os.path.normpath(currentPath + "//FBX//" + objectName + ".fbx")
        
        bpy.ops.export_scene.fbx(filepath=f, check_existing = False, use_selection = True, apply_scale_options = 'FBX_SCALE_ALL', use_space_transform = False, bake_space_transform = False, bake_anim = True, bake_anim_use_nla_strips = True, bake_anim_use_all_actions = False, axis_forward = '-Z', axis_up = 'Y')

        return {"FINISHED"}


class UnityLinkRender(bpy.types.Operator):
    bl_idname = "scene.unitylinkrender"
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

class UnityLinkAnim(bpy.types.Operator):
    bl_idname = "scene.unitylinkanim"
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

class UnityLinkPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Exports"
    bl_label = "Unity Exports"
    bl_idname = "SCENE_PT_layout_UIMP"

    
    def draw(self, context):        
        scene = bpy.context.scene
        render = scene.render
        uimp_tool = context.scene.uimp_tool
        
        layout = self.layout 
        row = layout.row()
        layout.label(text="Unity Project Link")
        row = layout.row()
        row.prop(uimp_tool, "exportpath")
        row = layout.row()
        row.prop(uimp_tool, "subfolder")
        row = layout.row()
        row.prop(uimp_tool, "exportname")
        

classes = (
    UnityLinkFbx,
    UnityLinkRender,
    UnityLinkAnim,
    UnityLinkPanel,
    UIMP_settings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.uimp_tool = bpy.props.PointerProperty(type=UIMP_settings)

def unregister():
    del bpy.types.Scene.uimp_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()    
