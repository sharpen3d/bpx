import bpy
import os.path
import bpy.props

#locate files
thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
fileBaseName = thisFileName.replace(".blend", "")
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]
truncatedPath = "C:\\"

#gets the parent of the blend file's directory
x = 0
for i in currentPath:
    sub = currentPath[x]
    if (sub == "\\"):    
        truncatedPath = currentPath[:x]            
    x=x+1

#opens system browser at a location
class OpenPath(bpy.types.Operator):
    bl_idname = "scene.openpath"
    bl_label = "Open"
    
    def execute(self, context):
        import sys
        import os
        import subprocess
        
        thisFilePath = bpy.data.filepath
        thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
        fileBaseName = thisFileName.replace(".blend", "")
        currentPath = thisFilePath.replace(thisFileName, "")
        currentPath = currentPath[:-1]
        
        my_tool = context.scene.my_tool
        
        if(my_tool.save_as_new == True):
            currentPath = my_tool.save_path
        else:
            currentPath = currentPath
        
        filepath = currentPath+"//ProjectFiles//"
        
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
                       
        return {"FINISHED"}

#master class, runs multiple operators
class ConsolidateAdvanced(bpy.types.Operator):
    bl_idname = "scene.consolidateadvanced"
    bl_label = "Collect Files"
    
    def execute(self, context):
        
        bpy.ops.wm.save_mainfile()        
        my_tool = context.scene.my_tool
        thisFilePath = bpy.data.filepath
        thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
        
        #bpy.ops.wm.save_as_mainfile('INVOKE_DEFAULT')
        if(my_tool.save_as_new == True):
            currentPath = my_tool.save_path        
            
            bpy.ops.wm.save_as_mainfile(filepath=currentPath + thisFileName)
        
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
        bpy.ops.scene.consolidateimages()
        bpy.ops.scene.consolidatefonts()        
        bpy.ops.wm.save_mainfile()
        
        if(my_tool.show_finished == True):
            bpy.ops.scene.openpath()
                       
        return {"FINISHED"}

#collects all fonts
class ConsolidateFonts(bpy.types.Operator):
    bl_idname = "scene.consolidatefonts"
    bl_label = "Collect Fonts"
    
    def execute(self, context):
        
        if(fileBaseName == "untitled" or fileBaseName == "untitled" or fileBaseName == ""):
            self.report({'INFO'}, "Please save this .blend file before using this operator")
        else:            
            import shutil
            import os
            
            my_tool = context.scene.my_tool
            
            if(my_tool.save_as_new == True):
                currentPath = my_tool.save_path
            else:
                thisFilePath = bpy.data.filepath
                thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
                currentPath = thisFilePath.replace(thisFileName, "")
                currentPath = currentPath[:-1]        
            
            bpy.ops.file.make_paths_absolute('INVOKE_DEFAULT')

            for font in bpy.data.fonts:
                
                fullstring = font.name
                substring = "Bfont"

                if substring in fullstring:
                    print("Found!")
                else:
              
                    directory = "ProjectFiles"
                    parent_dir = currentPath
                    parent_dir = os.path.normpath(parent_dir)
                    path = os.path.join(parent_dir, directory)
                    
                    isdir = os.path.isdir(path)
                    if (isdir == False):
                        os.mkdir(path)
                    
                    directory = "Fonts"
                    parent_dir = currentPath+"//ProjectFiles//"
                    parent_dir = os.path.normpath(parent_dir)
                    path = os.path.join(parent_dir, directory)
                    
                    isdir = os.path.isdir(path)
                    if (isdir == False):
                        os.mkdir(path)
                    
                    fontName = bpy.path.basename(font.filepath)                    
                    o = font.filepath
                    t = currentPath+"//ProjectFiles//Fonts"
                    check = currentPath+"//ProjectFiles//Fonts//"+fontName
                    
                    orig = os.path.normpath(o)
                    tar = os.path.normpath(t)          
                    chk = os.path.normpath(check)  
                    
                    if (orig != chk):
                        shutil.copy(orig,tar)                
                        newPath = currentPath+"//ProjectFiles//Fonts//"+fontName
                        font.filepath = os.path.normpath(newPath)
            
                    bpy.ops.file.make_paths_relative()
                    dispPath = currentPath+"//ProjectFiles//Fonts//"
                    dispPath = os.path.normpath(dispPath)
                    
                    self.report({'INFO'}, "Fonts Saved in " + dispPath)
            
        return {"FINISHED"}
    
#Collects all images used in .blend
class ConsolidateImages(bpy.types.Operator):
    bl_idname = "scene.consolidateimages"
    bl_label = "Collect Images"
    
    def execute(self, context):
        
        if(fileBaseName == "untitled" or fileBaseName == "untitled" or fileBaseName == ""):
            self.report({'INFO'}, "Please save this .blend file before using this operator")
        else:            
            import shutil
            import os
            
            my_tool = context.scene.my_tool
            
            if(my_tool.save_as_new == True):
                currentPath = my_tool.save_path
            else:
                thisFilePath = bpy.data.filepath
                thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
                currentPath = thisFilePath.replace(thisFileName, "")
                currentPath = currentPath[:-1]
            
            bpy.ops.file.make_paths_absolute('INVOKE_DEFAULT')

            for img in bpy.data.images:
                
                img.reload()
                
                #sequences not allowed
                if ((img.type == 'IMAGE' or img.type == 'MULTILAYER') and not (img.source == 'GENERATED')):
                    
                    directory = "ProjectFiles"
                    parent_dir = currentPath
                    parent_dir = os.path.normpath(parent_dir)
                    path = os.path.join(parent_dir, directory)
                    
                    isdir = os.path.isdir(path)
                    if (isdir == False):
                        os.mkdir(path)
                    
                    directory = "Images"
                    parent_dir = currentPath+"//ProjectFiles//"
                    parent_dir = os.path.normpath(parent_dir)
                    path = os.path.join(parent_dir, directory)
                    
                    isdir = os.path.isdir(path)
                    if (isdir == False):
                        os.mkdir(path)
                    
                    imageBaseName = bpy.path.basename(img.filepath)
                    o = img.filepath
                    t = currentPath+"//ProjectFiles//Images"
                    check = currentPath+"//ProjectFiles//Images//"+imageBaseName
                    
                    orig = os.path.normpath(o)
                    tar = os.path.normpath(t)          
                    chk = os.path.normpath(check)  
                    
                    if (orig != chk):
                        try:
                            shutil.copy(orig,tar)   
                            newPath = currentPath+"//ProjectFiles//Images//"+imageBaseName
                            img.filepath = os.path.normpath(newPath)
                            img.reload()   
                        except:          
                            print("Image " + img.name + " could not be saved")

            
            bpy.ops.file.make_paths_relative()
            dispPath = currentPath+"//ProjectFiles//Images//"
            dispPath = os.path.normpath(dispPath)
            
            self.report({'INFO'}, "Images Saved in " + dispPath)
            
        return {"FINISHED"}         
        
#custom variables for menu panel
class My_settings(bpy.types.PropertyGroup):
    save_path: bpy.props.StringProperty(
        name='Filepath',
        default=truncatedPath
    )

    include_fonts: bpy.props.BoolProperty(
        name='Fonts',
        default=True
    )
    
    include_images: bpy.props.BoolProperty(
        name='Images',
        default=True
    )
    
    save_as_new: bpy.props.BoolProperty(
        name='Save Into New Directory',
        description="Copy this .blend file and save to new location \n1% the new .blend will become the active file \n1% Use this method when preparing to share this file",
        default=False
    )
    
    show_finished: bpy.props.BoolProperty(
        name='Show In System Browser When Finished',
        default=True
    )
    
#create panel
class CollectFiles(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "File Manager"
    bl_label = "Collect Files"
    bl_icon = 'FILE_BACKUP'
    bl_idname = "SCENE_PT_layout_collect"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FILE_BACKUP")
    
    def draw(self, context):        
        scene = bpy.context.scene
        render = scene.render        
        layout = self.layout
        my_tool = context.scene.my_tool

        row = layout.row(align=True)
        if (my_tool.include_fonts == True and my_tool.include_images == True):
            row.operator("scene.consolidateadvanced")
        elif (my_tool.include_images == True):
            row.operator("scene.consolidateimages")
        elif (my_tool.include_fonts == True):
            row.operator("scene.consolidatefonts")
        else:
            layout.label(text="Select File Types To Include")
            
        row.operator("scene.openpath", text='', icon='FILEBROWSER')
        
        layout.label(text="File Types To Include", icon='LINKED')
        row = layout.row()
        row.prop(my_tool, "include_images")
        row = layout.row()
        row.prop(my_tool, "include_fonts")  

#create second panel
class OutputSettings_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "File Manager"
    bl_label = "Filepaths"
    bl_idname = "SCENE_PT_layout_output"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FILE_CACHE")
    
    def draw(self, context):        
        scene = bpy.context.scene
        render = scene.render        
        layout = self.layout
        my_tool = context.scene.my_tool
        
        #paths        
        row = layout.row()
        row.prop(my_tool, "save_as_new")     
        if (my_tool.save_as_new == True):
            row = layout.row()
            row.prop(my_tool, "save_path", text="")
        
        row = layout.row()
        row.prop(my_tool, "show_finished")   

       
#prep classes to register
classes = (
    My_settings,
    CollectFiles,
    OutputSettings_Panel,
    OpenPath,
    ConsolidateImages,
    ConsolidateFonts,
    ConsolidateAdvanced,  
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=My_settings)

def unregister():
    del bpy.types.Scene.my_tool
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()    