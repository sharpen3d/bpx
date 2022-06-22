import bpy

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]
input = None

class SetGeoMat(bpy.types.Operator):
    bl_idname = "scene.setgeomat"
    bl_label = "Set Particle Material"

    def execute(self, context):
        
        #use this for the emitter as well
        #check if particleMat exists
        for mat in bpy.data.materials:
            if mat.name == "bpx_particleMat":
                break
        else:
            from pathlib import Path
            import os
            prefs = bpy.context.preferences
            filepaths = prefs.filepaths
            asset_libraries = filepaths.asset_libraries
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
        
            #append material
            path = resources_path + "\\Extensions\\Resources.blend"
            subFolder = "\\Material\\"
            object = "bpx_particleMat"

            library = path + subFolder
            xfilepath = path + subFolder + object

            bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
            
        selected = bpy.context.object
        
        if (len(selected.material_slots) < 1):
            selected.data.materials.append(None)

        selected.material_slots[0].material = bpy.data.materials["bpx_particleMat"]
        
        mat = bpy.context.object.material_slots[0].material
        # newmat = mat.copy()        
        # name new material here?
        # bpy.context.object.material_slots[0].material = newmat
                
        return {"FINISHED"}
    
class AddPointEmitter(bpy.types.Operator):
    bl_idname = "scene.addpointemitter"
    bl_label = "Add Point Emitter"
    
    def execute(self, context):
        try:
            cam = bpy.context.scene.camera.data
                    
            bpxPlane = bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            mod = bpy.ops.object.modifier_add(type='NODES')
            bpxNodes = bpy.data.node_groups["bpx_particleNodes"]
            geo = bpy.context.object.modifiers["GeometryNodes"]
            geo.node_group = bpxNodes
            newNodes = geo.node_group.copy()
            geo.node_group = newNodes
            
            #geo["Input_7"] = cam
            geo["Output_2_attribute_name"] = "life"
            geo["Output_3_attribute_name"] = "col"
            geo["Output_4_attribute_name"] = "alpha"
            
            bpy.ops.scene.setgeomat()
        except:
            self.report({'INFO'}, "Add a camera before creating an emitter!")
        
        return {"FINISHED"}

class UseConstant(bpy.types.Operator):
    bl_idname = "scene.useconstant"
    bl_label = "Constant"
    
    def execute(self, context):
        global input
        input.default_value = False
        
        return {"FINISHED"}

class UseRandom(bpy.types.Operator):
    bl_idname = "scene.userandom"
    bl_label = "Random In Range"
    
    def execute(self, context):
        global input
        
        print(input)
        input.default_value = True
        
        return {"FINISHED"}

class ShowInputMenu(bpy.types.Operator):
    bl_idname = "scene.showinputmenu"
    bl_label = "Input Selection"
    
    def execute(self, context):
        global input
        input = bpy.context.object.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[4]
                
        bpy.ops.wm.call_menu(name=InputSelect.bl_idname)
                
        return {"FINISHED"}

class ShowInputMenuLife(bpy.types.Operator):
    bl_idname = "scene.showinputmenulife"
    bl_label = "Input Selection"
    
    def execute(self, context):
        global input
        input = bpy.context.object.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[8]
                
        bpy.ops.wm.call_menu(name=InputSelect.bl_idname)
                
        return {"FINISHED"}

class ShowInputMenuSpeed(bpy.types.Operator):
    bl_idname = "scene.showinputmenuspeed"
    bl_label = "Input Selection"
    
    def execute(self, context):
        global input
        input = bpy.context.object.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[6]
        bpy.ops.wm.call_menu(name=InputSelect.bl_idname)
                
        return {"FINISHED"}
    
class ShowInputMenuScale(bpy.types.Operator):
    bl_idname = "scene.showinputmenuscale"
    bl_label = "Input Selection"
    
    def execute(self, context):
        global input
        input = bpy.context.object.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[8]
        bpy.ops.wm.call_menu(name=InputSelect.bl_idname)
                
        return {"FINISHED"}
    
class ShowInputMenuRotate(bpy.types.Operator):
    bl_idname = "scene.showinputmenurotate"
    bl_label = "Input Selection"
    
    def execute(self, context):
        global input
        input = bpy.context.object.modifiers["GeometryNodes"].node_group.nodes["Start Rotation"].inputs[5]
        bpy.ops.wm.call_menu(name=InputSelect.bl_idname)
                
        return {"FINISHED"}
    
class ShowInputMenuRotateOL(bpy.types.Operator):
    bl_idname = "scene.showinputmenurotateol"
    bl_label = "Input Selection"
    
    def execute(self, context):
        global input
        input = bpy.context.object.modifiers["GeometryNodes"].node_group.nodes["Group.006"].inputs[5]
        bpy.ops.wm.call_menu(name=InputSelect.bl_idname)
                
        return {"FINISHED"}
                    
class InputSelect(bpy.types.Menu):
    bl_label = "Input Type"
    bl_idname = "INPUT_MT_inputmenu"

    def draw(self, context):
        layout = self.layout

        layout.operator("scene.useconstant")
        layout.operator("scene.userandom")

class InfoPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Emitters"
    bl_idname = "SCENE_PT_layout_ParticleInfo"

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        row.operator("scene.addpointemitter", text="Add New Emitter")
        
class ParticleOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Spawn"
    bl_idname = "SCENE_PT_layout"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:
            
            #Spawn options               
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[1], 'default_value', text="Particle Count")
             
            #curve options
            row = layout.row()
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[16], 'default_value', text="Spawn From Curve", slider=True)
            row = layout.row()
            if selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[16].default_value == True:
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Custom Curve"].inputs[0], 'default_value', text="Curve Object")
                row = layout.row()
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[14], 'default_value', text="Curve Sweep Time")

            #Emitter shape
            self.layout.label(text="Emitter Rotation")
            row = layout.row()
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[2], 'default_value', text="")   
            row = layout.row()                    
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[3], 'default_value', text="Sweep Direction")
            row = layout.row()                    

class LifeOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Life"
    bl_idname = "SCENE_PT_layout_Life"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:
            #Start Frame options
            if selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[4].default_value == True:
                self.layout.label(text="Start Frame (Min/Max)")
                row = layout.row(align=True)
                row.operator("scene.showinputmenu", text="", icon='DOWNARROW_HLT') 
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[6], 'default_value', text="Min")
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[7], 'default_value', text="Max")
            else:
                row = layout.row(align=True)
                row.operator("scene.showinputmenu", text="", icon='DOWNARROW_HLT') 
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[5], 'default_value', text="Start Frame")     
            
            #Lifetime optinos
            row = layout.row()       
            if selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[8].default_value == True:
                self.layout.label(text="Lifetime (Min/Max)")
                row = layout.row(align=True)    
                row.operator("scene.showinputmenulife", text="", icon='DOWNARROW_HLT')   
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[10], 'default_value', text="Min")
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[11], 'default_value', text="Max")
            else:
                row = layout.row(align=True)    
                row.operator("scene.showinputmenulife", text="", icon='DOWNARROW_HLT')  
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[9], 'default_value', text="Lifetime")
            row = layout.row()
            
            #looping options
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[13], 'default_value', text="Looping", slider=True)
            row = layout.row()
            if selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[13].default_value == True:
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[12], 'default_value', text="Loop Duration")
                row = layout.row()
            
class SpeedOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Movement"
    bl_idname = "SCENE_PT_layout_Movement"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:
            
            #speed
            if selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[6].default_value == True:
                self.layout.label(text="Particle Speed")
                row = layout.row(align=True)    
                row.operator("scene.showinputmenuspeed", text="", icon='DOWNARROW_HLT')   
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[8], 'default_value', text="Min")
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[9], 'default_value', text="Max")
            else:
                row = layout.row(align=True)    
                row.operator("scene.showinputmenuspeed", text="", icon='DOWNARROW_HLT')  
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[7], 'default_value', text="Particle Speed")
            row = layout.row()
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[4], 'default_value', text="Graph Movement Over Lifetime")
            row = layout.row()
            if selected.modifiers["GeometryNodes"].node_group.nodes["Initial Movement"].inputs[4].default_value == True:
                curveMap = selected.modifiers["GeometryNodes"].node_group.nodes["Speed Interpolate"]
                layout.template_curve_mapping(curveMap, "mapping")
                row = layout.row()
                
            #Global Speed options    
#            row = layout.row()                 
#            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[18], 'default_value', text="Simulation Speed")     
           

class TrailOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Trails"
    bl_idname = "SCENE_PT_layout_Trails"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:
            #Trail options
            row = layout.row()  
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[2], 'default_value', text="Trail Length")   
            row = layout.row()                    
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Particle Spawner"].inputs[3], 'default_value', text="Trail Spacing")

class GravityOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Physics"
    bl_idname = "SCENE_PT_layout_Gravity"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:    
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Calculate Accelleration"].inputs[1], 'default_value', text="Gravity Strength")   
            row = layout.row()
            self.layout.label(text="Gravity Rotation")
            row = layout.row()
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Accelleration Gravity"].inputs[2], 'default_value', text="")
            

class ScaleOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Scale"
    bl_idname = "SCENE_PT_layout_Scale"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:   
            #speed
            if selected.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[8].default_value == True:
                self.layout.label(text="Particle Scale")
                row = layout.row(align=True)   
                #wrong! 
                row.operator("scene.showinputmenuscale", text="", icon='DOWNARROW_HLT')   
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[9], 'default_value', text="Min")
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[10], 'default_value', text="Max")
            else:
                row = layout.row(align=True)    
                row.operator("scene.showinputmenuscale", text="", icon='DOWNARROW_HLT')  
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[2], 'default_value', text="Particle Scale")
            row = layout.row()   
            row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[5], 'default_value', text="Graph Scale Over Lifetime")
            if selected.modifiers["GeometryNodes"].node_group.nodes["Group"].inputs[5].default_value == True:
                curveMap = selected.modifiers["GeometryNodes"].node_group.nodes["Scale Interpolate"]
                layout.template_curve_mapping(curveMap, "mapping")
                row = layout.row()

class RotateOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Rotation"
    bl_idname = "SCENE_PT_layout_Rotate"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:   
        
            if selected.modifiers["GeometryNodes"].node_group.nodes["Start Rotation"].inputs[5].default_value == True:
                self.layout.label(text="Start Rotation (Min/Max)")
                row = layout.row(align=True)   
                #wrong! 
                row.operator("scene.showinputmenurotate", text="", icon='DOWNARROW_HLT')   
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Start Rotation"].inputs[6], 'default_value', text="Min")
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Start Rotation"].inputs[7], 'default_value', text="Max")
            else:
                self.layout.label(text="Start Rotation")
                row = layout.row(align=True)    
                row.operator("scene.showinputmenurotate", text="", icon='DOWNARROW_HLT')  
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Start Rotation"].inputs[4], 'default_value', text="Revolutions")
            row = layout.row()   
            
            if selected.modifiers["GeometryNodes"].node_group.nodes["Group.006"].inputs[5].default_value == True:
                self.layout.label(text="Rotate Over Life (Min/Max)")
                row = layout.row(align=True)   
                #wrong! 
                row.operator("scene.showinputmenurotateol", text="", icon='DOWNARROW_HLT')   
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Group.006"].inputs[6], 'default_value', text="Min")
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Group.006"].inputs[7], 'default_value', text="Max")
            else:
                self.layout.label(text="Rotate Over Life (Min/Max)")
                row = layout.row(align=True)    
                row.operator("scene.showinputmenurotateol", text="", icon='DOWNARROW_HLT')  
                row.prop(selected.modifiers["GeometryNodes"].node_group.nodes["Start Rotation"].inputs[4], 'default_value', text="Revolutions")
            row = layout.row()   
            
            self.layout.label(text="Interpolate Over Life")
            curveMap = selected.modifiers["GeometryNodes"].node_group.nodes["Rotate Interpolate"]
            layout.template_curve_mapping(curveMap, "mapping")
            row = layout.row()
            
class ColorOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Particle Color"
    bl_idname = "SCENE_PT_layout_Color"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        #check if particle is selected
        isIncluded = False
        if (bpy.context.selected_objects != []):
            selected = bpy.context.object
            if (selected.type == 'MESH'):
                if(len(selected.modifiers) > 0):
                    if "bpx_particleNodes" in selected.modifiers[0].node_group.name:
                        isIncluded = True
    
        if isIncluded == True:
            self.layout.label(text="Color Over Life")
            colorMap = selected.modifiers["GeometryNodes"].node_group.nodes["Particle Color"]
            layout.template_color_ramp(colorMap, "color_ramp")
            row = layout.row()
            
            self.layout.label(text="Alpha Over Life")
            colorMap = selected.modifiers["GeometryNodes"].node_group.nodes["Particle Alpha"]
            layout.template_color_ramp(colorMap, "color_ramp")
            row = layout.row()



#curveMap = selected.modifiers["GeometryNodes"].node_group.nodes["Speed Over Life"]
#row = layout.row()
#layout.label(text="Speed Over Life")
#layout.template_curve_mapping(curveMap, "mapping")

#class InstanceParticle(bpy.types.Operator):
#    bl_idname = "scene.instanceparticle"
#    bl_label = "Make Instance Unique"
#    activeChild = bpy.context.view_layer.objects.active
#    
#    def execute(self, context):
#        geo = bpy.context.object.modifiers["GeometryNodes"].node_group
#        print(geo)
#        newgroup = geo.copy()
#        bpy.context.object.modifiers["GeometryNodes"].node_group = newgroup
#        #newgroup.name = bpy.context.scene["Name"]
#        
#        mat = bpy.context.object.material_slots[0].material
#        print(mat)
#        newmat = mat.copy()
#        bpy.context.object.material_slots[0].material = newmat
#        #newgroup.name = bpy.context.scene["Name"]
#        
#        return {"FINISHED"} 
                    
#class ParticleRendering(bpy.types.Panel):
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'UI'
#    bl_category = "Emitters"
#    bl_label = "Color Over Life"
#    bl_idname = "SCENE_PT_layout02"
#    bl_options = {'DEFAULT_CLOSED'}
#    
#    def draw(self, context):
#        scene = bpy.context.scene
#        particlesInstalled = False
#        
#        layout = self.layout
#        row = layout.row()
#        
#        selected = bpy.context.object
#        
#        fullstring = selected.name
#        substring = "emitterDirection"
#        
#        if substring in fullstring:
#            selected = selected.parent
#        
#        children = selected.children
#                      
#        for child in children:
#            fullstring = child.name
#            substring = "emitterDirection"
#            
#            if substring in fullstring:                     
#                cr_node = selected.material_slots[0].material.node_tree.nodes['Color Over Life']
#                cr_node1 = selected.material_slots[0].material.node_tree.nodes['Alpha Over Life']
#                
#                row = layout.row()
#                layout.label(text="Color Over Life:")
#                layout.template_color_ramp(cr_node, "color_ramp", expand=True)
#                
#                row = layout.row()
#                layout.label(text="Alpha Over Life:")
#                layout.template_color_ramp(cr_node1, "color_ramp", expand=True)
#                
#                tree = selected.material_slots[0].material.node_tree
#                imagenode = selected.material_slots[0].material.node_tree.nodes['MixAlpha'] 
#                image = selected.material_slots[0].material.node_tree.nodes['Alpha Stencil'] 
#                  
#                row = layout.row()
#                layout.label(text="Alpha Stencil:")

#                row = layout.row()
#                layout.template_node_view(tree, imagenode, imagenode.inputs['Color1']) 


               
#bpy.utils.register_class(InstanceParticle)
bpy.utils.register_class(AddPointEmitter)
bpy.utils.register_class(ParticleOptions)
bpy.utils.register_class(SetGeoMat)
bpy.utils.register_class(UseConstant)
bpy.utils.register_class(UseRandom)
bpy.utils.register_class(ShowInputMenu)
bpy.utils.register_class(ShowInputMenuLife)
bpy.utils.register_class(ShowInputMenuSpeed)
bpy.utils.register_class(ShowInputMenuScale)
bpy.utils.register_class(ShowInputMenuRotate)
bpy.utils.register_class(ShowInputMenuRotateOL)
bpy.utils.register_class(ColorOptions)
bpy.utils.register_class(InputSelect)
bpy.utils.register_class(InfoPanel)
bpy.utils.register_class(LifeOptions)
bpy.utils.register_class(SpeedOptions)
bpy.utils.register_class(TrailOptions)
bpy.utils.register_class(GravityOptions)
bpy.utils.register_class(ScaleOptions)
bpy.utils.register_class(RotateOptions)