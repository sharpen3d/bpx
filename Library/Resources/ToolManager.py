import bpy
import os
from pathlib import Path
import bpy.props

prefs = bpy.context.preferences
filepaths = prefs.filepaths
asset_libraries = filepaths.asset_libraries
resources_path = ""
verified_library_path = ""
selected_tool = ""
tools_list = ["2DTools.py", "WordArtist.py", "FileManager.py", "GeoEmitters.py", "GridPacker.py", "QuickActions.py"]

class TestOpenTool(bpy.types.Operator):
    bl_idname = "scene.testopentool"
    bl_label = "Verify Correct Paths (hidden to user)"
    
    def execute(self, context):
        selected_script = bpy.data.texts["WordArtist.py"]
        print(selected_script)
        
        exec(selected_script.as_string())
              
        return {"FINISHED"}
    
class AppendNodes(bpy.types.Operator):
    bl_idname = "scene.appendnodes"
    bl_label = "append specific node group"
    
    def execute(self, context):
        path = resources_path + "\\Extensions\\Resources.blend"
        subFolder = "\\Scene\\"
        object = "Emitters"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
              
        return {"FINISHED"}

class verify_library(bpy.types.Operator):
    bl_idname = "scene.verifylibrary"
    bl_label = "Verify Correct Paths (hidden to user)"
    
    def execute(self, context):
        for asset_library in asset_libraries:
            library_name = asset_library.name
            library_path = Path(asset_library.path)
            blend_files = [fp for fp in library_path.glob("**/*.blend") if fp.is_file()]
            for blend_file in blend_files:
                with bpy.data.libraries.load(str(blend_file)) as (file_contents, _):
                    try:
                        if(file_contents.texts[0] == "MetadataVerify"):
                            verified_library_path = library_path
                            break
                    except:
                        print("an error occured, checking for other libraries...")
        
        global resources_path
        resources_path = str(verified_library_path) + "//Resources"
        resources_path = os.path.normpath(resources_path) 
        
        print(resources_path)
              
        return {"FINISHED"}

class emitter_append(bpy.types.Operator):
    bl_idname = "scene.emitterappend"
    bl_label = "append extra emitter resources"
    
    def execute(self, context):
        path = resources_path + "\\Extensions\\Resources.blend"
        subFolder = "\\Scene\\"
        object = "Emitters"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
              
        return {"FINISHED"}
    
class wordart_append(bpy.types.Operator):
    bl_idname = "scene.wordartappend"
    bl_label = "append extra word artist resources"
    
    def execute(self, context):
        path = resources_path + "\\Extensions\\Resources.blend"
        
        subFolder = "\\NodeTree\\"
        object = "wordArt_geo"
        library = path + subFolder
        xfilepath = path + subFolder + object
        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
        bpy.data.node_groups['wordArt_geo']use_fake_user = True
        
        subFolder = "\\Material\\"
        object = "wa_default_front"
        library = path + subFolder
        xfilepath = path + subFolder + object
        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)

        subFolder = "\\Material\\"
        object = "wa_default_bevel"
        library = path + subFolder
        xfilepath = path + subFolder + object
        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
        
        subFolder = "\\Material\\"
        object = "wa_default_depth"
        library = path + subFolder
        xfilepath = path + subFolder + object
        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
              
        return {"FINISHED"}
    
class packing_append(bpy.types.Operator):
    bl_idname = "scene.packingappend"
    bl_label = "append extra gridpacking resources"
    
    def execute(self, context):
        path = resources_path + "\\Extensions\\Resources.blend"
        subFolder = "\\Scene\\"
        object = "packScene"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
              
        return {"FINISHED"}

class ortho_append(bpy.types.Operator):
    bl_idname = "scene.orthoappend"
    bl_label = "append extra 2D Tools resources"
    
    def execute(self, context):
        path = resources_path + "\\Extensions\\Resources.blend"
        
        subFolder = "\\NodeTree\\"
        object = "bpx_geo"
        library = path + subFolder
        xfilepath = path + subFolder + object
        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
        bpy.data.node_groups["bpx_geo"].use_fake_user = True
              
        return {"FINISHED"}

class release_tools(bpy.types.Operator):
    bl_idname = "scene.releasetools"
    bl_label = "Release All Tools"
    
    def execute(self, context):
        for text in bpy.data.texts:
            if text.name != "ToolManager.py":
                text.use_module = False
                text.use_fake_user = False
                ctx = bpy.context.copy()
                ctx['edit_text'] = text
                bpy.ops.text.unlink(ctx)
        bpy.context.copy()
        ctx = bpy.context.copy()
        ctx['edit_text'] = bpy.data.texts["ToolManager.py"]
        bpy.ops.text.run_script(ctx)
              
        return {"FINISHED"}
    
class append_button(bpy.types.Operator):
    bl_idname = "scene.appendbutton"
    bl_label = "Append Tools"
    
    def execute(self, context):
        global selected_tool
        global resources_path
        tm_tool = context.scene.tm_tool
        
        #run verification of installation
        bpy.ops.scene.verifylibrary()
        
        index = 0
        while index < len(tools_list):
            installatindex = False
            
            # this format for each list item
            if index == 0:
                if tm_tool.DTools == True:
                    for text in bpy.data.texts:
                        if text.name == "2DTools.py":
                            print("skipping 2D Tools, already installed")
                            break
                    else:
                        installatindex = True
                        bpy.ops.scene.orthoappend()
                        
            if index == 1:
                if tm_tool.WordArtist == True:
                    for text in bpy.data.texts:
                        if text.name == "WordArtist.py":
                            print("skipping Word Artist, already installed")
                            break
                    else:
                        installatindex = True
                        bpy.ops.scene.wordartappend()
            
            if index == 2:
                if tm_tool.FileManager == True:
                    for text in bpy.data.texts:
                        if text.name == "FileManager.py":
                            print("skipping File Manager, already installed")
                            break
                    else:
                        installatindex = True
  
            if index == 3:
                if tm_tool.GeoEmitters == True:
                    for text in bpy.data.texts:
                        if text.name == "GeoEmitters.py":
                            print("skipping Geo Emitters, already installed")
                            break
                    else:
                        installatindex = True   
                        bpy.ops.scene.emitterappend()
                        
            if index == 4:
                if tm_tool.GridPacker == True:
                    for text in bpy.data.texts:
                        if text.name == "2DTools.py":
                            print("skipping 2D Tools, already installed")
                            break
                    else:
                        installatindex = True  
                        bpy.ops.scene.packingappend()
                        
            if index == 5:
                if tm_tool.QuickActions == True:
                    installatindex = True  
            
            #install                     
            if installatindex == True:
                selected_tool = tools_list[index]               
                path = resources_path + "//" + selected_tool
                path = os.path.normpath(path)
                bpy.ops.text.open(filepath=path)        
                selected_script = bpy.data.texts[selected_tool]        
                text = bpy.data.texts[selected_tool]
                ctx = bpy.context.copy()
                ctx['edit_text'] = text
                bpy.ops.text.run_script(ctx)
                text.use_module = True
            
            #iterate
            index = index+1
            
        
        #exec(selected_script.as_string())
                       
        return {"FINISHED"}

#make panel
class resources_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool Manager"
    bl_label = "Tool Manager"
    bl_idname = "SCENE_PT_layout_resources_layout"
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout     
        tm_tool = context.scene.tm_tool   
        
        self.layout.label(text="Custom Libraries")        
        row = layout.row() 
        row.operator("scene.appendbutton")
        row = layout.row() 
        row.operator("scene.releasetools")
        
        #2D Tools 
        row = layout.row()        
        label0 = "2D Tools"
        for i in bpy.data.texts:
            if i.name == tools_list[0]:
                self.layout.label(text=label0 + " (installed)", icon = 'CHECKBOX_HLT')
                break            
        else:            
            row.prop(tm_tool, "DTools", text=label0)
        
        #Word Artist  
        row = layout.row()        
        label0 = "Word Artist"
        for i in bpy.data.texts:
            if i.name == tools_list[1]:
                self.layout.label(text=label0 + " (installed)", icon = 'CHECKBOX_HLT')
                break            
        else:            
            row.prop(tm_tool, "WordArtist", text=label0)        

        #File Manager
        row = layout.row()        
        label0 = "File Manager"
        for i in bpy.data.texts:
            if i.name == tools_list[2]:
                self.layout.label(text=label0 + " (installed)", icon = 'CHECKBOX_HLT')
                break            
        else:            
            row.prop(tm_tool, "FileManager", text=label0)
            
        #Geo Emitters
        row = layout.row()        
        label0 = "Geo Emitters"
        for i in bpy.data.texts:
            if i.name == tools_list[3]:
                self.layout.label(text=label0 + " (installed)", icon = 'CHECKBOX_HLT')
                break            
        else:            
            row.prop(tm_tool, "GeoEmitters", text=label0)

        #Grid Packer
        row = layout.row()        
        label0 = "Grid Packer"
        for i in bpy.data.texts:
            if i.name == tools_list[4]:
                self.layout.label(text=label0 + " (installed)", icon = 'CHECKBOX_HLT')
                break            
        else:            
            row.prop(tm_tool, "GridPacker", text=label0)
        
        
        #Grid Packer
        row = layout.row()        
        label0 = "Quick Actions"
        for i in bpy.data.texts:
            if i.name == tools_list[5]:
                self.layout.label(text=label0 + " (installed)", icon = 'CHECKBOX_HLT')
                break            
        else:            
            row.prop(tm_tool, "QuickActions", text=label0)
        

#def register():
#    bpy.utils.register_class(resources_panel)   
#    bpy.utils.register_class(append_button)   
#    bpy.utils.register_class(verify_library)     
#    bpy.utils.register_class(TestOpenTool)  


class TM_settings(bpy.types.PropertyGroup):
    DTools: bpy.props.BoolProperty(
        name=tools_list[0],
        default=False
    )
    
    WordArtist: bpy.props.BoolProperty(
        name=tools_list[1],
        default=False
    )

    FileManager: bpy.props.BoolProperty(
        name=tools_list[2],
        default=False
    )

    GeoEmitters: bpy.props.BoolProperty(
        name=tools_list[3],
        default=False
    )

    GridPacker: bpy.props.BoolProperty(
        name=tools_list[4],
        default=False
    )

    QuickActions: bpy.props.BoolProperty(
        name=tools_list[4],
        default=False
    )
    
classes = (
    resources_panel,
    append_button,
    verify_library,
    TestOpenTool,
    TM_settings,
    emitter_append,
    ortho_append,
    packing_append,
    wordart_append,
    release_tools,
    AppendNodes,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tm_tool = bpy.props.PointerProperty(type=TM_settings)

def unregister():
    del bpy.types.Scene.tm_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()    