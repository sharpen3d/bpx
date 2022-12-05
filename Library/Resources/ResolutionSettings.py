import bpy
flipped = False
scene = bpy.context.scene
prevx = scene.render.resolution_x
prevy = scene.render.resolution_y

class ShowResolutionMenu(bpy.types.Operator):
    bl_idname = "object.showresmenu"
    bl_label = "X (^2 presets)"
    bl_description = "Set Resolution From Preset"
    
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name=ResolutionMenu.bl_idname)
                
        return {"FINISHED"}
    
class ResolutionMenu(bpy.types.Menu):
    bl_label = "Power of 2 (X)"
    bl_idname = "RESOLUTION_MT_resmenu"
    

    def draw(self, context):
        layout = self.layout
        
        scene = bpy.context.scene
        layout.operator("scene.resx64")
        layout.operator("scene.resx128")
        layout.operator("scene.resx256")
        layout.operator("scene.resx512")
        layout.operator("scene.resx1024")
        layout.operator("scene.resx2048")
        layout.operator("scene.resx4096")

class ShowResolutionMenuY(bpy.types.Operator):
    bl_idname = "object.showresmenuy"
    bl_label = "Y (^2 presets)"
    bl_description = "Set Resolution From Preset"
    
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name=ResolutionMenuY.bl_idname)
                
        return {"FINISHED"}
    
class ResolutionMenuY(bpy.types.Menu):
    bl_label = "Power of 2 (Y)"
    bl_idname = "RESOLUTIONY_MT_resmenu"
    

    def draw(self, context):
        layout = self.layout
        
        scene = bpy.context.scene
        layout.operator("scene.resy64")
        layout.operator("scene.resy128")
        layout.operator("scene.resy256")
        layout.operator("scene.resy512")
        layout.operator("scene.resy1024")
        layout.operator("scene.resy2048")
        layout.operator("scene.resy4096")
        

class FlipResolution(bpy.types.Operator):
    bl_idname = "scene.flipresolution"
    bl_label = "Swap X and Y"

    def execute(self, context):
        scene = bpy.context.scene
        prevx = scene.render.resolution_x
        prevy = scene.render.resolution_y
        scene.render.resolution_x = prevy
        scene.render.resolution_y = prevx
                
        return {"FINISHED"}
    
class ResX64(bpy.types.Operator):
    bl_idname = "scene.resx64"
    bl_label = "64 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 64        
                
        return {"FINISHED"}
    
class ResX128(bpy.types.Operator):
    bl_idname = "scene.resx128"
    bl_label = "128 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 128
                
        return {"FINISHED"}
    
class ResX256(bpy.types.Operator):
    bl_idname = "scene.resx256"
    bl_label = "256 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 256
                
        return {"FINISHED"}
    
class ResX512(bpy.types.Operator):
    bl_idname = "scene.resx512"
    bl_label = "512 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 512     
                
        return {"FINISHED"}
    
class ResX1024(bpy.types.Operator):
    bl_idname = "scene.resx1024"
    bl_label = "1024 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 1024
                
        return {"FINISHED"}
    
class ResX2048(bpy.types.Operator):
    bl_idname = "scene.resx2048"
    bl_label = "2048 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 2048
                
        return {"FINISHED"}
    
class ResX4096(bpy.types.Operator):
    bl_idname = "scene.resx4096"
    bl_label = "4096 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 4096
                
        return {"FINISHED"}
    
class ResY64(bpy.types.Operator):
    bl_idname = "scene.resy64"
    bl_label = "64 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 64        
                
        return {"FINISHED"}
    
class ResY128(bpy.types.Operator):
    bl_idname = "scene.resy128"
    bl_label = "128 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 128
                
        return {"FINISHED"}
    
class ResY256(bpy.types.Operator):
    bl_idname = "scene.resy256"
    bl_label = "256 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 256
                
        return {"FINISHED"}
    
class ResY512(bpy.types.Operator):
    bl_idname = "scene.resy512"
    bl_label = "512 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 512     
                
        return {"FINISHED"}
    
class ResY1024(bpy.types.Operator):
    bl_idname = "scene.resy1024"
    bl_label = "1024 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 1024
                
        return {"FINISHED"}
    
class ResY2048(bpy.types.Operator):
    bl_idname = "scene.resy2048"
    bl_label = "2048 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 2048
                
        return {"FINISHED"}
    
class ResY4096(bpy.types.Operator):
    bl_idname = "scene.resy4096"
    bl_label = "4096 px"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_y = 4096
                
        return {"FINISHED"}

class ResVertical(bpy.types.Operator):
    bl_idname = "scene.resvertical"
    bl_label = "1080 x 1920"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1920
                
        return {"FINISHED"}
    
class ResHalf(bpy.types.Operator):
    bl_idname = "scene.reshalf"
    bl_label = "Resolution / 2"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = int(scene.render.resolution_x/2)
        scene.render.resolution_y = int(scene.render.resolution_y/2)
                
        return {"FINISHED"}
    
class ResDouble(bpy.types.Operator):
    bl_idname = "scene.resdouble"
    bl_label = "Resolution * 2"

    def execute(self, context):
        scene = bpy.context.scene
        scene.render.resolution_x = scene.render.resolution_x*2
        scene.render.resolution_y = scene.render.resolution_y*2
                
        return {"FINISHED"}


class RenderResolutionPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "Quick Resolution"
    bl_label = "Quick Resolutions"
    bl_idname = "SCENE_PT_render_options"
    bl_context = "output"
    
    def draw(self, context):
        layout = self.layout 
        
        row = layout.row(align = True)
        row.operator("object.showresmenu")  
        row.operator("object.showresmenuy")  
        
        row = layout.row()
        row.operator("scene.flipresolution")  
        
        row = layout.row()
        row.operator("scene.resvertical")
        
        row = layout.row()
        row.operator("scene.reshalf")
        
        row = layout.row()
        row.operator("scene.resdouble")


classes = (
    ResolutionMenu,
    ShowResolutionMenu,
    ResolutionMenuY,
    ShowResolutionMenuY,
    FlipResolution,
    RenderResolutionPanel,
    ResX64,
    ResX128,
    ResX256,
    ResX512,
    ResX1024,
    ResX2048,
    ResX4096,
    ResY64,
    ResY128,
    ResY256,
    ResY512,
    ResY1024,
    ResY2048,
    ResY4096,
    ResVertical,
    ResHalf,
    ResDouble
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    del bpy.types.Scene.tm_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()    