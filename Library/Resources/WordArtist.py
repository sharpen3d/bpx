import bpy
import bpy.props

class MakeText(bpy.types.Operator):
    bl_idname = "scene.maketext"
    bl_label = "Make New Text"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.text_add()
        selected = bpy.context.object
        selected.data.body = text_tool.edit_text
        selected.data.align_x = 'CENTER'
        selected.data.align_y = 'CENTER'
        selected.data.bevel_depth = text_tool.user_bevel
        selected.data.extrude = text_tool.user_depth
        
        #add geo node style
        mod = bpy.ops.object.modifier_add(type='NODES')
        textNodes = bpy.data.node_groups["wordArt_geo"]
        geo = bpy.context.object.modifiers["GeometryNodes"]
        geo.node_group = textNodes
        geo["Output_2_attribute_name"] = "nrmMin"
        geo["Output_3_attribute_name"] = "nrmMax"
        geo["Output_4_attribute_name"] = "parts_id"
        geo["Output_15_attribute_name"] = "posMin"
        geo["Output_16_attribute_name"] = "posMax"
        
        #set up material
        if (len(selected.material_slots) < 6):
            amt = 6 - len(selected.material_slots)
            while amt > 0:
                selected.data.materials.append(None)
                amt = amt - 1
                               
        return {"FINISHED"}

class UseAdvGeo(bpy.types.Operator):
    bl_idname = "scene.useadvgeo"
    bl_label = "Use Advanced Geometry"
    bl_description = "Use Custom Geometry Nodes"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        selected = bpy.context.object
        selected.data.align_x = 'CENTER'
        selected.data.align_y = 'CENTER'
        
        #add geo node style
        mod = bpy.ops.object.modifier_add(type='NODES')
        textNodes = bpy.data.node_groups["wordArt_geo"]
        geo = bpy.context.object.modifiers["GeometryNodes"]
        geo.node_group = textNodes
        geo["Output_2_attribute_name"] = "nrmMin"
        geo["Output_3_attribute_name"] = "nrmMax"
        geo["Output_4_attribute_name"] = "parts_id"
        geo["Output_15_attribute_name"] = "posMin"
        geo["Output_16_attribute_name"] = "posMax"
        
        #set up material
        if (len(selected.material_slots) < 6):
            amt = 6 - len(selected.material_slots)
            while amt > 0:
                selected.data.materials.append(None)
                amt = amt - 1
                               
        return {"FINISHED"}

class SetText(bpy.types.Operator):
    bl_idname = "scene.settext"
    bl_label = "Edit Text"
    bl_description = "Update Current Text"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            if (txt.type == 'FONT'):
                txt.data.body = text_tool.edit_text
            
        return {"FINISHED"}    

class CycleForward(bpy.types.Operator):
    bl_idname = "scene.cycleforward"
    bl_label = "Cycle To Next Font"
    bl_description = "Next Font Loaded in File"
    
    def execute(self, context):
        text_tool = context.scene.text_tool  
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            fontIndex = 0
            x = 0
            
            target = txt.data.font
            for i in bpy.data.fonts:
                if (i == target):    
                    fontIndex = x
                else:        
                    x=x+1
            
            nextFont = fontIndex+1
            if (fontIndex == (len(bpy.data.fonts)-1)):
                nextFont = 0
                    
            txt.data.font = bpy.data.fonts[nextFont]        
                       
        return {"FINISHED"}

class CycleBackward(bpy.types.Operator):
    bl_idname = "scene.cyclebackward"
    bl_label = "Cycle To Previous Font"
    bl_description = "Previous Font Loaded in File"
    
    def execute(self, context):
        text_tool = context.scene.text_tool  
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            fontIndex = 0
            x = 0
            
            target = txt.data.font
            for i in bpy.data.fonts:
                if (i == target):    
                    fontIndex = x
                else:        
                    x=x+1
            
            prevFont = fontIndex-1
            if (fontIndex == -1):
                prevFont = (len(bpy.data.fonts)-1)
                    
            txt.data.font = bpy.data.fonts[prevFont]    
        
            
        return {"FINISHED"}

class SetBevel(bpy.types.Operator):
    bl_idname = "scene.setbevel"
    bl_label = "Apply Bevel"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            if (txt.type == 'FONT'):
                txt.data.bevel_depth = text_tool.user_bevel
            
        return {"FINISHED"} 

class SetExtrude(bpy.types.Operator):
    bl_idname = "scene.setextrude"
    bl_label = "Apply Depth"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            if (txt.type == 'FONT'):
                txt.data.extrude = text_tool.user_depth      
            
        return {"FINISHED"}

class CopyToSelected(bpy.types.Operator):
    bl_idname = "scene.copytoselected"
    bl_label = "Copy Properties (Active To Selected)"
    bl_description = "Copy the selected properties from the active object (last selected) to other selected objects"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            if (txt.type == 'FONT'):
                
                #scale?/size
                txt.data.align_x = selected.data.align_x
                txt.data.align_y = selected.data.align_y
                
                if text_tool.use_body == True:
                    txt.data.body = selected.data.body  
                if text_tool.use_font == True:
                    txt.data.font = selected.data.font
                if text_tool.use_shear == True:
                    txt.data.shear = selected.data.shear
                if text_tool.use_extrude == True:
                    txt.data.extrude = selected.data.extrude
                if text_tool.use_offset == True:
                    txt.data.offset = selected.data.offset
                if text_tool.use_resolution == True:
                    txt.data.resolution_u = selected.data.resolution_u
                if text_tool.use_bevel_mode == True:
                    txt.data.bevel_mode = selected.data.bevel_mode
                if text_tool.use_bevel_depth == True:
                    txt.data.bevel_depth = selected.data.bevel_depth
                if text_tool.use_bevel_resolution == True:
                    txt.data.bevel_resolution = selected.data.bevel_resolution
                
                if text_tool.use_geometry == True:
                    
                    #check if source has wordart nodes
                    srcNodes = False
                    if len(bpy.context.object.modifiers) > 0:
                        for modif in bpy.context.object.modifiers:
                            if modif.name == "GeometryNodes":
                                if modif.node_group == bpy.data.node_groups["wordArt_geo"]:
                                    srcNodes = True
                                    geoSrc = modif
                                    break
                    
                    if srcNodes == True:
                        
                        #check if target has geo nodes
                        tgtNodes = False
                        
                        if len(txt.modifiers) > 0:
                            for modif in txt.modifiers:
                                if modif.name == "GeometryNodes":
                                    if modif.node_group == bpy.data.node_groups["wordArt_geo"]:
                                        tgtNodes = True
                                        mod = modif
                                        break
                        
                        
                        #add nodes to target(s)                                 
                        if tgtNodes == False:
                            print(txt.name)
                            
                            #bpy.context.view_layer.objects.active = txt                            
                            #mod = bpy.ops.object.modifier_add(type='NODES')
                            txt.modifiers.new("GeometryNodes", 'NODES')
                            #txt.modifiers[0] = ["GeometryNodes"]
                            
                            textNodes = bpy.data.node_groups["wordArt_geo"]                            
                            geo = txt.modifiers["GeometryNodes"]
                            geo.node_group = textNodes                        
                            geo["Output_2_attribute_name"] = "nrmMin"
                            geo["Output_3_attribute_name"] = "nrmMax"
                            geo["Output_4_attribute_name"] = "parts_id"
                            geo["Output_15_attribute_name"] = "posMin"
                            geo["Output_16_attribute_name"] = "posMax"
                        
                        bpy.context.view_layer.objects.active = selected
                        geoTgt = txt.modifiers["GeometryNodes"]
                        
                        geoTgt["Input_5"] = geoSrc["Input_5"]
                        geoTgt["Input_6"] = geoSrc["Input_6"]
                        geoTgt["Input_7"] = geoSrc["Input_7"]
                        geoTgt["Input_12"] = geoSrc["Input_12"]
                        geoTgt["Input_14"] = geoSrc["Input_14"]
                        geoTgt["Input_17"] = geoSrc["Input_17"]
                        geoTgt["Input_19"] = geoSrc["Input_19"]

                if text_tool.use_material == True:
                    if (len(txt.material_slots) < len(selected.material_slots)):
                        amt = len(selected.material_slots) - len(txt.material_slots)
                        while amt > 0:
                            txt.data.materials.append(None)
                            amt = amt - 1
                    
                    x = 0
                    for i in selected.material_slots:
                        txt.material_slots[x].material = selected.material_slots[x].material
                        x = x + 1
            
        return {"FINISHED"}

class SetUnderline(bpy.types.Operator):
    bl_idname = "scene.setunderline"
    bl_label = "Toggle Underline"
    
    def execute(self, context):
        text_tool = context.scene.text_tool
        selected = bpy.context.object
        textGroup = bpy.context.selected_objects
        
        for txt in textGroup:
            if (txt.type == 'FONT'):
                index = 0
                for i in txt.data.body_format:
                    if(txt.data.body_format[index].use_underline == True):
                        txt.data.body_format[index].use_underline = False
                    else:
                        txt.data.body_format[index].use_underline = True
                    index=index+1
            
        return {"FINISHED"}
        
class Text_settings(bpy.types.PropertyGroup):
    new_text: bpy.props.StringProperty(
        name='New Text',
        default="New Text"
    )
    
    edit_text: bpy.props.StringProperty(
        name='New Text',
        default="New Text"
    )
    
    user_bevel: bpy.props.FloatProperty(
        name='Bevel',
        default= 0.01
    )
    
    user_depth: bpy.props.FloatProperty(
        name='Extrude',
        default= 0.25
    )

    use_font: bpy.props.BoolProperty(
        name='Font',
        default=True
    )
    
    use_bevel: bpy.props.BoolProperty(
        name='Bevel',
        default=True
    )

    use_extrude: bpy.props.BoolProperty(
        name='Extrude',
        default=True
    )

    use_offset: bpy.props.BoolProperty(
        name='Offset',
        default=True
    )

    use_bevel_mode: bpy.props.BoolProperty(
        name='Mode',
        default=True
    )

    use_bevel_depth: bpy.props.BoolProperty(
        name='Depth',
        default=True
    )

    use_bevel_resolution: bpy.props.BoolProperty(
        name='Resolution',
        default=True
    )

    use_shear: bpy.props.BoolProperty(
        name='Shear',
        default=True
    )

    use_body: bpy.props.BoolProperty(
        name='Body',
        default=True
    )
    
    use_resolution: bpy.props.BoolProperty(
        name='Resolution',
        default=True
    )
    
    use_character: bpy.props.BoolProperty(
        name='Character',
        default=True
    )

    use_word: bpy.props.BoolProperty(
        name='Word',
        default=True
    )

    use_line: bpy.props.BoolProperty(
        name='Line',
        default=True
    )

    use_geometry: bpy.props.BoolProperty(
        name='Geometry Settings',
        default=True
    )
    
    use_material: bpy.props.BoolProperty(
        name='Material Settings',
        default=True
    )

#create panel
class Text_Panel(bpy.types.Panel):
    bl_idname = "SCENE_PT_layout_wa_props"
    bl_label = "Advanced Geometry"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"    
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FONTPREVIEW")
    
    def draw(self, context):        
        scene = bpy.context.scene 
        layout = self.layout
        text_tool = context.scene.text_tool
        row = layout.row()
        
        hasNodes = False
        if len(bpy.context.object.modifiers) > 0:
            for mod in bpy.context.object.modifiers:
                if mod.name == "GeometryNodes":
                    if mod.node_group == bpy.data.node_groups["wordArt_geo"]:
                        hasNodes = True
                        break
        
        if hasNodes == True:
            geo = bpy.context.object.modifiers["GeometryNodes"]
            row.prop(geo, '["Input_19"]', text='Slide X')
            row = layout.row()
            row.prop(geo, '["Input_5"]', text='Slide Y')
            row = layout.row()       
            row.prop(geo, '["Input_7"]', text='Taper X')
            row = layout.row()     
            row.prop(geo, '["Input_6"]', text='Taper Y')
            row = layout.row()
            row.prop(geo, '["Input_12"]', text='Stroke (1) Width')
            row = layout.row()
            row.prop(geo, '["Input_14"]', text='Stroke (2) Width')
            row = layout.row()
            row.prop(geo, '["Input_17"]', text='Stroke (3) Width')
            row = layout.row()
        else:
            row.operator("scene.useadvgeo")
            row = layout.row()
                            
            

            
#            layout.label(text="Materials")
#            row = layout.row()
#            row.prop(geo, '["Input_8"]', text='Face Material')
#            row = layout.row()
#            row.prop(geo, '["Input_9"]', text='Bevel Material')
#            row = layout.row()
#            row.prop(geo, '["Input_10"]', text='Depth Material')
            
            

        
class Edit_Text_Panel(bpy.types.Panel):
    bl_idname = "SCENE_PT_layout_EditTextProp"
    bl_label = "Font Selector"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"    
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FONTPREVIEW")
    
    def draw(self, context):        
        scene = bpy.context.scene 
        layout = self.layout
        text_tool = context.scene.text_tool
        
#        layout.label(text="Text Body:")
#        row = layout.row()
#        row.prop(text_tool, "edit_text", text='')
#        row = layout.row(align=True)            
#        row.operator("scene.maketext", text='New Text Object', icon='OUTLINER_DATA_FONT')
        
        #Set Selected Text
        if (bpy.context.selected_objects != [] and bpy.context.object.type == 'FONT'):
            
            selected = bpy.context.object
        
            #button to add new          
            #row.operator("scene.settext", text='Update Selected', icon='OUTLINER_DATA_FONT')
            
            #Cycle through fonts
#            row = layout.row()
#            layout.label(text="Cycle Through Fonts")
            row = layout.row(align=True)
            row.operator("scene.cyclebackward", text='', icon='TRIA_LEFT')
            row.prop(selected.data, "font", text="")
            row.operator("scene.cycleforward", text='', icon='TRIA_RIGHT')

#            #underline
#            row = layout.row()
#            layout.label(text="Character Style:")
#            row = layout.row()
#            row.prop(selected.data, "shear", text="Shear")
#            row = layout.row()  
#            row.operator("scene.setunderline")
#            row = layout.row()
#            row.prop(selected.data, "underline_position", text="Underline Position")
#            row = layout.row()
#            row.prop(selected.data, "underline_height", text="Underline Thickness")
#            
#            #settings
#            row = layout.row()
#            layout.label(text="Geometry Settings")
#            row = layout.row()
#            row.prop(selected.data, "extrude", text="Extrude")
#            row = layout.row()
#            row.prop(selected.data, "offset", text="Offset")
#            row = layout.row()
#            row.prop(selected.data, "resolution_u", text="Resolution")
#            row = layout.row()
#            layout.label(text="Bevel")
#            row = layout.row()                        
#            row.prop(selected.data, "bevel_mode", text="")
#            row = layout.row()
#            row.prop(selected.data, "bevel_depth", text="Bevel Depth")
#            row = layout.row()            
#            layout.label(text="Spacing Settings")
#            row = layout.row()
#            row.prop(selected.data, "space_character", text="Character Spacing")
#            row = layout.row()
#            row.prop(selected.data, "space_word", text="Word Spacing")
#            row = layout.row()
#            row.prop(selected.data, "space_line", text="Line Spacing")
#            row = layout.row()
#            layout.label(text="Text Follows Curve")
#            row = layout.row()            
#            row.prop(selected.data, "follow_curve", text="")
#            row = layout.row()
            
#            row = layout.row()
#            layout.label(text="Edit Bevel Of Selected")
#            row = layout.row(align=True)
#            row.prop(text_tool, "user_bevel")
#            row.operator("scene.setbevel")
#            
#            row = layout.row()
#            layout.label(text="Edit Depth Of Selected")
#            row = layout.row(align=True)
#            row.prop(text_tool, "user_depth")
#            row.operator("scene.setextrude")

class Match_Text_Panel(bpy.types.Panel):

    bl_idname = "SCENE_PT_layout_cpyslectProp"
    bl_label = "Copy Font Data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data" 
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FONTPREVIEW")
    
    def draw(self, context):        
        scene = bpy.context.scene 
        layout = self.layout
        text_tool = context.scene.text_tool
        
        #Set Selected Text
        if (len(bpy.context.selected_objects) > 1 and bpy.context.object.type == 'FONT'):
            
            selected = bpy.context.object
            
            row = layout.row()
            row.operator("scene.copytoselected")
            row = layout.row()
                    
        #write new text
        layout.label(text="Text Data:")
        row = layout.row(align=True)
        row.prop(text_tool, "use_body")
        row.prop(text_tool, "use_font")
        row.prop(text_tool, "use_shear")
        layout.label(text="Geometry Data:")
        row = layout.row(align=True)
        row.prop(text_tool, "use_extrude")
        row.prop(text_tool, "use_offset")
        row.prop(text_tool, "use_resolution")
        layout.label(text="Bevel Data:")
        row = layout.row(align=True)
        row.prop(text_tool, "use_bevel_mode")
        row.prop(text_tool, "use_bevel_depth")
        row.prop(text_tool, "use_bevel_resolution")
        layout.label(text="Additional Data:")
        row = layout.row(align=True)
        row.prop(text_tool, "use_geometry")
        row.prop(text_tool, "use_material")
            
class Kern_Text_Panel(bpy.types.Panel):
    bl_idname = "SCENE_PT_layout_KernProp"
    bl_label = "Kern By Character"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data" 
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FONTPREVIEW")
    
    def draw(self, context):        
        scene = bpy.context.scene 
        layout = self.layout
        text_tool = context.scene.text_tool
        
        #Set Selected Text
        if (bpy.context.selected_objects != [] and bpy.context.object.type == 'FONT'):
            
            selected = bpy.context.object
            #write new text
            row = layout.row()
            
            layout.label(text="Per-Character Kerning:")
            index = 0
            for i in selected.data.body_format:
                row = layout.row()
                row.prop(selected.data.body_format[index], "kerning", text="Kern ("+selected.data.body[index]+")")
                #row.prop(selected.data.body_format[index], "material_index", text="Material Index")
                index = index+1
       
classes = (
    MakeText,
    SetText,
    CycleForward,
    CycleBackward,
    Text_settings,
    Text_Panel,
    Edit_Text_Panel,
    SetBevel,
    SetExtrude,
    Match_Text_Panel,
    SetUnderline,
    Kern_Text_Panel,
    CopyToSelected,
    UseAdvGeo,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.text_tool = bpy.props.PointerProperty(type=Text_settings)

def unregister():
    del bpy.types.Scene.text_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()    