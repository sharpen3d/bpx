import bpy
import os.path
import bpy.props


class SpecialRenderPanel(bpy.types.Panel):
    bl_label = "Special Render"
    bl_idname = "SCENE_PT_layout_specialRender"
    
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    
    def draw(self, context):        
        scene = bpy.context.scene
        render = scene.render
        sp_tool = context.scene.sp_tool
        
        layout = self.layout 
        
        displayPath = sp_tool.render_path +"\\"+ sp_tool.render_name +"\\"+ sp_tool.render_name + "####.png" 
        layout.label(text="Output:  "+ displayPath)
        
        row = layout.row()
        row.prop(sp_tool, "render_path")
        
        row = layout.row()
        row.prop(sp_tool, "render_name")
        
        row = layout.row()
        row.operator("scene.specialrender")
        

class SpecialRender(bpy.types.Operator):
    bl_idname = "scene.specialrender"
    bl_label = "Render Animation To Folder"
    
    def execute(self, context):
        
        thisFilePath = bpy.data.filepath
        thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
        fileBaseName = thisFileName.replace(".blend", "")
        currentPath = thisFilePath.replace(thisFileName, "")
        currentPath = currentPath[:-1]
        sp_tool = context.scene.sp_tool

        scene = bpy.context.scene
        render = scene.render
        
        render.filepath = sp_tool.render_path +"//"+ sp_tool.render_name +"//"+ sp_tool.render_name
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "Render Complete!")
        
        return {"FINISHED"}

class SP_settings(bpy.types.PropertyGroup):
    render_name: bpy.props.StringProperty(
        name='Render Name',
        default="Render Name"
    )
    
    render_path: bpy.props.StringProperty(
    name='Render Path',
    default="Render Path"
    )

classes = (
    SP_settings,
    SpecialRenderPanel,
    SpecialRender,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sp_tool = bpy.props.PointerProperty(type=SP_settings)

def unregister():
    del bpy.types.Scene.tm_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()   