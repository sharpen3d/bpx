import bpy
from bpy.types import Menu

wm = bpy.context.window_manager
km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
kmi = km.keymap_items.new("wm.call_menu_pie", type='E', ctrl=False, value ='PRESS')
kmi.properties.name = "VIEW3D_MT_PIE_alignoptions"

# spawn an edit mode selection pie (run while object is in edit mode to get a valid output)
class AlignX(bpy.types.Operator):
    bl_idname = "scene.alignx"
    bl_label = "Align X To Selected"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object

        for obj in selected:
            if obj != bpy.context.object:
                obj.location[0] = active.location[0]

                
        return {"FINISHED"}

class AlignXCursor(bpy.types.Operator):
    bl_idname = "scene.aligncursorx"
    bl_label = "Align X To 3D Cursor"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object

        for obj in selected:
            obj.location[0] = bpy.context.scene.cursor.location[0]

                
        return {"FINISHED"}
    
class AlignY(bpy.types.Operator):
    bl_idname = "scene.aligny"
    bl_label = "Align Y To Selected"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object
        for obj in selected:
            if obj != bpy.context.object:
                obj.location[1] = active.location[1]
                
        return {"FINISHED"}

class AlignYCursor(bpy.types.Operator):
    bl_idname = "scene.aligncursory"
    bl_label = "Align Y To 3D Cursor"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object

        for obj in selected:
            obj.location[1] = bpy.context.scene.cursor.location[1]

                
        return {"FINISHED"}
    
class AlignZ(bpy.types.Operator):
    bl_idname = "scene.alignz"
    bl_label = "Align Z To Selected"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object
        for obj in selected:
            if obj != bpy.context.object:
                obj.location[2] = active.location[2]
                
        return {"FINISHED"}

class AlignZCursor(bpy.types.Operator):
    bl_idname = "scene.aligncursorz"
    bl_label = "Align Z To 3D Cursor"
    
    def execute(self, context):
        selected = bpy.context.selected_objects
        active = bpy.context.object

        for obj in selected:
            obj.location[2] = bpy.context.scene.cursor.location[2]

                
        return {"FINISHED"}

class VIEW3D_MT_PIE_alignoptions(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Align Object"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        
        #left
        pie.operator("scene.aligny")
        
        #right
        pie.operator("scene.aligncursory")
        
        #up (blank)
        pie = pie.row()
        pie.label(text='')
        pie = layout.menu_pie()
        
        #down (blank)
        pie = pie.row()
        pie.label(text='')
        pie = layout.menu_pie()
        
        #left-up
        pie.operator("scene.alignz")
        
        #right-up
        pie.operator("scene.aligncursorz")
        
        #left-down
        pie.operator("scene.alignx")
        
        #right-down
        pie.operator("scene.aligncursorx")


def register():
    bpy.utils.register_class(VIEW3D_MT_PIE_alignoptions)
    bpy.utils.register_class(AlignX)
    bpy.utils.register_class(AlignY)
    bpy.utils.register_class(AlignZ)
    bpy.utils.register_class(AlignXCursor)
    bpy.utils.register_class(AlignYCursor)
    bpy.utils.register_class(AlignZCursor)


def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_PIE_alignoptions)
    bpy.utils.register_class(AlignX)
    bpy.utils.register_class(AlignY)
    bpy.utils.register_class(AlignZ)
    bpy.utils.register_class(AlignXCursor)
    bpy.utils.register_class(AlignYCursor)
    bpy.utils.register_class(AlignZCursor)


if __name__ == "__main__":
    register()
