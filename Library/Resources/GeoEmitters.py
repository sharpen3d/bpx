import bpy

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]


class AppendParticles(bpy.types.Operator):
    bl_idname = "scene.appendparticles"
    bl_label = "Append Particle Editor"
    
    def execute(self, context):
        path = "\\\\NCFS1\\Dev\\Art\\_ArtistShareables_\\blenderTemplates\\GeoParticle\\emitters.blend"
        subFolder = "\\Scene\\"
        object = "Emitters"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
                       
        return {"FINISHED"}
    
class AddPointEmitter(bpy.types.Operator):
    bl_idname = "scene.addpointemitter"
    bl_label = "Add Point Emitter"
    
    def execute(self, context):
        direction = bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))
        bpy.context.object.name = "emitterDirection"
        bpy.ops.transform.resize(value=(2, 2, 2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        directionEmpty = bpy.context.object
        
        velocity = bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "emitterVelocity"
        bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        velocityEmpty = bpy.context.object
        
        bpy.ops.object.add_named(name="GP_PointEmitter", matrix=((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
        
        geo = bpy.context.object.modifiers["GeometryNodes"]
        scene = bpy.context.scene
        
        geo["Input_26"] = scene.camera
        geo["Input_23"] = directionEmpty
        geo["Input_24"] = velocityEmpty
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        
        directionEmpty.parent = bpy.context.object
        velocityEmpty.parent = bpy.context.object
        
        return {"FINISHED"}

class AddMeshEmitter(bpy.types.Operator):
    bl_idname = "scene.addmeshemitter"
    bl_label = "Add Emitter to Mesh"
    
    def execute(self, context):
        selected = bpy.context.object
        origin = bpy.context.object.location
        
        direction = bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))
        bpy.context.object.name = "emitterDirection"
        bpy.ops.transform.resize(value=(2, 2, 2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        directionEmpty = bpy.context.object
        
        velocity = bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "emitterVelocity"
        bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        velocityEmpty = bpy.context.object
        
        bpy.ops.object.add_named(name="GP_MeshEmitter", matrix=((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
        bpy.context.object.location = origin
        
        geo = bpy.context.object.modifiers["GeometryNodes"]
        scene = bpy.context.scene
        
        geo["Input_29"] = selected
        geo["Input_26"] = bpy.data.scenes["Scene"].camera
        geo["Input_23"] = directionEmpty
        geo["Input_24"] = velocityEmpty
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        
        directionEmpty.parent = bpy.context.object
        velocityEmpty.parent = bpy.context.object
                
        return {"FINISHED"}

class AddCurveEmitter(bpy.types.Operator):
    bl_idname = "scene.addcurveemitter"
    bl_label = "Add Emitter To Curve"
    
    def execute(self, context):
        selected = bpy.context.object
        origin = bpy.context.object.location
        
        direction = bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(2, 2, 2))
        bpy.context.object.name = "emitterDirection"
        bpy.ops.transform.resize(value=(2, 2, 2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        directionEmpty = bpy.context.object
        
        velocity = bpy.ops.object.empty_add(type='SINGLE_ARROW', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "emitterVelocity"
        bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        velocityEmpty = bpy.context.object
        
        bpy.ops.object.add_named(name="GP_CurveEmitter", matrix=((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
        bpy.context.object.location = origin
        
        geo = bpy.context.object.modifiers["GeometryNodes"]
        scene = bpy.context.scene
        
        geo["Input_29"] = selected
        geo["Input_26"] = bpy.data.scenes["Scene"].camera
        geo["Input_23"] = directionEmpty
        geo["Input_24"] = velocityEmpty
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        
        directionEmpty.parent = bpy.context.object
        velocityEmpty.parent = bpy.context.object
        
        return {"FINISHED"}

class SelectDirection(bpy.types.Operator):
    bl_idname = "scene.selectdirection"
    bl_label = "Select Emitter Direction"
    activeChild = bpy.context.view_layer.objects.active
    
    def execute(self, context):
        selected = bpy.context.object
        children = selected.children
        for child in children:
            fullstring = child.name
            print(fullstring)
            substring = "emitterDirection"
            if substring in fullstring:
                activeChild = child
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = activeChild
                activeChild.select_set(True)
        return {"FINISHED"}
    
class SelectVelocity(bpy.types.Operator):
    bl_idname = "scene.selectvelocity"
    bl_label = "Select Velocity Direction"
    activeChild = bpy.context.view_layer.objects.active
    
    def execute(self, context):
        selected = bpy.context.object
        children = selected.children
        for child in children:
            fullstring = child.name
            print(fullstring)
            substring = "emitterVelocity"
            if substring in fullstring:
                activeChild = child
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = activeChild
                activeChild.select_set(True)
        return {"FINISHED"}
    
class InstanceParticle(bpy.types.Operator):
    bl_idname = "scene.instanceparticle"
    bl_label = "Make Instance Unique"
    activeChild = bpy.context.view_layer.objects.active
    
    def execute(self, context):
        geo = bpy.context.object.modifiers["GeometryNodes"].node_group
        print(geo)
        newgroup = geo.copy()
        bpy.context.object.modifiers["GeometryNodes"].node_group = newgroup
        #newgroup.name = bpy.context.scene["Name"]
        
        mat = bpy.context.object.material_slots[0].material
        print(mat)
        newmat = mat.copy()
        bpy.context.object.material_slots[0].material = newmat
        #newgroup.name = bpy.context.scene["Name"]
        
        return {"FINISHED"}  
    
class SetLoop(bpy.types.Operator):
    bl_idname = "scene.setloop"
    bl_label = "Looping"
    activeChild = bpy.context.view_layer.objects.active
    
    
    def execute(self, context):
        loopmod = bpy.context.object.modifiers["GeometryNodes"]["Input_25"]
        
        if loopmod == False:
            bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = True
        else:
            bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = False
            
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {"FINISHED"}  
                   
class StartOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Add Emitters"
    bl_idname = "SCENE_PT_layout01"
    bl_order = 1
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = bpy.context.scene
        particlesInstalled = False
        
        layout = self.layout
        row = layout.row()
        
        for x in bpy.data.scenes:
            if x.name == "Emitters":
                particlesInstalled = True
        
        if particlesInstalled == False:
            row.operator("scene.appendparticles")
            row = layout.row()
        if particlesInstalled == True:
            row.operator("scene.addpointemitter")
            row = layout.row()
            if bpy.context.selected_objects != []:
                
                #if bpy.context.object.type == 'MESH':
                    #row.operator("scene.addmeshemitter")
                    #row = layout.row()
                if bpy.context.object.type == 'CURVE':
                    row.operator("scene.addcurveemitter")
                    

class ParticleOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Spawn Properties"
    bl_idname = "SCENE_PT_layout"
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}

    #display menu section
    
    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        
        particlesInstalled = False

        for x in bpy.data.scenes:
            if x.name == "Emitters":
                particlesInstalled = True

        if particlesInstalled == True:    
                    
            selected = bpy.context.object
            
            fullstring = selected.name
            substring = "emitterDirection"
            
            if substring in fullstring:
                selected = selected.parent
            
            children = selected.children
                          
            for child in children:
                fullstring = child.name
                substring = "emitterDirection"
                
                if substring in fullstring:
                    row = layout.row()
                    row.operator("scene.selectdirection")
                    row.operator("scene.selectvelocity")
                    
                    row = layout.row()
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_13"]', text = "Sweep Angle", slider=True)
                    
                    row = layout.row()
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_16"]', text = "Count")
                    row = layout.row()
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_6"]', text = "Random Seed")
                    
                    row = layout.row()
                    layout.label(text="Spawn Time (Frame):")                                                         
                    row = layout.row(align=True)  
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_4"]', text = "Min")
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_5"]', text = "Max")                    
                    
                    row = layout.row()
                    layout.label(text="Particle Lifespan (Frame):")                   
                    row = layout.row(align=True) 
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_27"]', text = "Min")
                    row.prop(selected.modifiers["GeometryNodes"], '["Input_28"]', text = "Max")
                    
                    layout.label(text="Loop Options:")
                    row = layout.row()
                    
                    loopOptions = bpy.context.object.modifiers["GeometryNodes"]["Input_25"]                    
                    looptext = "text"
                    
                    if loopOptions == False:
                        looptext = "Make Loop"
                    else:
                        looptext = "Disable Loop"
                        
                    row = layout.row()
                    row.operator("scene.setloop", text = looptext)
                    
                    if loopOptions == True:
                        row = layout.row()
                        row.prop(selected.modifiers["GeometryNodes"], '["Input_7"]', text = "Loop Frames")
                    

                    
class ParticleRendering(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Color Over Life"
    bl_idname = "SCENE_PT_layout02"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = bpy.context.scene
        particlesInstalled = False
        
        layout = self.layout
        row = layout.row()
        
        selected = bpy.context.object
        
        fullstring = selected.name
        substring = "emitterDirection"
        
        if substring in fullstring:
            selected = selected.parent
        
        children = selected.children
                      
        for child in children:
            fullstring = child.name
            substring = "emitterDirection"
            
            if substring in fullstring:                     
                cr_node = selected.material_slots[0].material.node_tree.nodes['Color Over Life']
                cr_node1 = selected.material_slots[0].material.node_tree.nodes['Alpha Over Life']
                
                row = layout.row()
                layout.label(text="Color Over Life:")
                layout.template_color_ramp(cr_node, "color_ramp", expand=True)
                
                row = layout.row()
                layout.label(text="Alpha Over Life:")
                layout.template_color_ramp(cr_node1, "color_ramp", expand=True)
                
                tree = selected.material_slots[0].material.node_tree
                imagenode = selected.material_slots[0].material.node_tree.nodes['MixAlpha'] 
                image = selected.material_slots[0].material.node_tree.nodes['Alpha Stencil'] 
                  
                row = layout.row()
                layout.label(text="Alpha Stencil:")

                row = layout.row()
                layout.template_node_view(tree, imagenode, imagenode.inputs['Color1']) 
                

class ParticleSpeed(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Movement Over Time"
    bl_idname = "SCENE_PT_layout03"
    bl_options = {'DEFAULT_CLOSED'}
    

    def draw(self, context):
        scene = bpy.context.scene    
        layout = self.layout        
        selected = bpy.context.object        
        fullstring = selected.name
        substring = "emitterDirection"
        
        if substring in fullstring:
            selected = selected.parent
        
        children = selected.children
                      
        for child in children:
            fullstring = child.name
            substring = "emitterDirection"
            
            if substring in fullstring:      
                layout.label(text="Velocity(Gravity):")                                   
                row = layout.row(align=True)
                row.prop(selected.modifiers["GeometryNodes"], '["Input_14"]', text = "Influence")
                layout.label(text="Start Speed:")                                   
                row = layout.row(align=True)
                row.prop(selected.modifiers["GeometryNodes"], '["Input_10"]', text = "Min")
                row.prop(selected.modifiers["GeometryNodes"], '["Input_11"]', text = "Max")          
                curveMap = selected.modifiers["GeometryNodes"].node_group.nodes["Speed Over Life"]
                row = layout.row()
                layout.label(text="Speed Over Life")
                layout.template_curve_mapping(curveMap, "mapping")

class ParticleScale(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Scale"
    bl_idname = "SCENE_PT_layout04"
    bl_options = {'DEFAULT_CLOSED'}

    
    def draw(self, context):
        scene = bpy.context.scene    
        layout = self.layout        
        selected = bpy.context.object        
        fullstring = selected.name
        substring = "emitterDirection"
        
        if substring in fullstring:
            selected = selected.parent
        
        children = selected.children
        isParticle = False         
        for child in children:
            fullstring = child.name
            substring = "emitterDirection"
            
    
            if substring in fullstring:
                isParticle=True
                
        if isParticle==True:                                  
            row = layout.row(align=True)
            row.prop(selected.modifiers["GeometryNodes"], '["Input_18"]', text = "Min")
            row.prop(selected.modifiers["GeometryNodes"], '["Input_19"]', text = "Max")          
            curveMap = selected.modifiers["GeometryNodes"].node_group.nodes["Speed Over Life"]
            row = layout.row()    
            
            scaleMap = selected.modifiers["GeometryNodes"].node_group.nodes["Scale Over Life"]
            row = layout.row()
            layout.label(text="Scale Over Life")
            layout.template_curve_mapping(scaleMap, "mapping")

class ParticleInstance(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Instancing"
    bl_idname = "SCENE_PT_layout05"
    bl_order = 0
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = bpy.context.scene    
        layout = self.layout        
        selected = bpy.context.object        
        fullstring = selected.name
        substring = "emitterDirection"
        
        if substring in fullstring:
            selected = selected.parent
        
        children = selected.children
        isParticle = False             
        for child in children:
            fullstring = child.name
            substring = "emitterDirection"
            
            if substring in fullstring:  
                isParticle = True
        
        if isParticle == True:                                     
            row = layout.row(align=False)
            row.operator("scene.instanceparticle")
            #row = layout.row(align=False)
            #row.prop(scene, '["Name"]', text = "Name")
            
class ParticleRotation(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Emitters"
    bl_label = "Rotation"
    bl_idname = "SCENE_PT_layout06"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = bpy.context.scene    
        layout = self.layout        
        selected = bpy.context.object        
        fullstring = selected.name
        substring = "emitterDirection"
        
        if substring in fullstring:
            selected = selected.parent
        
        children = selected.children
        isParticle = False            
        for child in children:
            fullstring = child.name
            substring = "emitterDirection"
            
            if substring in fullstring:  
                isParticle = True
        
        if isParticle == True:                                     
            row = layout.row(align=False)
            row.prop(selected.modifiers["GeometryNodes"], '["Input_8"]', text = "Randomize Start Rotation")   
            row = layout.row(align=False)
            row.prop(selected.modifiers["GeometryNodes"], '["Input_9"]', text = "Randomize Over Life ")   
            #row = layout.row(align=False)
            #row.prop(scene, '["Name"]', text = "Name")

bpy.utils.register_class(ParticleRotation)     
bpy.utils.register_class(InstanceParticle)
bpy.utils.register_class(SelectVelocity)
bpy.utils.register_class(SetLoop)
bpy.utils.register_class(ParticleInstance)
bpy.utils.register_class(ParticleScale)
bpy.utils.register_class(ParticleSpeed)
bpy.utils.register_class(ParticleRendering)
bpy.utils.register_class(StartOptions)
bpy.utils.register_class(AddPointEmitter)
bpy.utils.register_class(AddMeshEmitter)
bpy.utils.register_class(AddCurveEmitter)
bpy.utils.register_class(ParticleOptions) 
bpy.utils.register_class(AppendParticles)
bpy.utils.register_class(SelectDirection)

