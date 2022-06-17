import bpy

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]

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
                    

class ParticleOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Spawn Emitter"
    bl_idname = "SCENE_PT_layout"
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        #selected = bpy.context.object
        #mod = selected.modifiers
        
        row.operator("scene.addpointemitter", text="Add New Emitter")
        
        #check if particle is selected   
        
        #external values (un-nested)
        #row = layout.row()        
        #row.prop(selected.modifiers["GeometryNodes"], '["Input_6"]', text = "Random Seed")
        
        #inputs on nested node groups
                    

                    
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