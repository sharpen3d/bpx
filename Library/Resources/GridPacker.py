import bpy
import math

class PackTex(bpy.types.Operator):
    bl_idname = "scene.packtexture"
    bl_label = "pack texture"    
    
    def execute(self, context):
        
        #file paths
        thisFilePath = bpy.data.filepath
        thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
        currentPath = thisFilePath.replace(thisFileName, "")
        inputName = bpy.data.scenes["packScene"]["Name"]+".png"
        
        #saved image location
        f=currentPath + "images\\packed\\" + inputName
        revert = bpy.context.scene.render.filepath
        bpy.data.scenes["packScene"].render.filepath = f
        bpy.context.scene.render.filepath = f
        canvasSize = bpy.data.scenes["packScene"]["canvasSize"]
        
        if (bpy.data.scenes["packScene"]["isLiveRender"] == 1):
            srcname = bpy.data.scenes["packScene"].node_tree.nodes['sourceScene'].scene.name
            bpy.data.scenes["packScene"]["sourceSize"] = bpy.data.scenes[srcname].render.resolution_x
                    
        #packed canvas full resolution
        bpy.data.scenes["packScene"].render.resolution_x = canvasSize
        bpy.data.scenes["packScene"].render.resolution_y = canvasSize
        
        #start and end frames (internal)
        sf = bpy.data.scenes["packScene"]["start frame"]
        ef = bpy.data.scenes["packScene"]["end frame"]
        i = sf
        
        imageCollection = bpy.data.images.keys()
        
        #prep a fresh image for packing
        if not inputName in imageCollection:
            bpy.data.scenes["packScene"].frame_current = sf
            bpy.ops.image.new(name=inputName, width=canvasSize, height=canvasSize, color=(0.0, 0.0, 0.0, 0.0))
            bpy.ops.render.render(animation=False, write_still=True, layer='', scene='packScene')
            bpy.data.images[inputName].filepath = f
            bpy.data.images[inputName].filepath_raw = f
            bpy.data.images[inputName].source = 'FILE'
            bpy.data.images[inputName].reload()
                     
        #load on to packTarget node
        target_node = bpy.data.scenes["packScene"].node_tree.nodes['packTarget']
        target_node.image = bpy.data.images[inputName]
        
        #set scene frame to start frame
        bpy.data.scenes["packScene"].frame_current = sf
        bpy.context.scene.frame_current = sf
        
        #for each frame in frame collection
        while i<=(ef):
            bpy.data.images[inputName].reload()
            
            #pack
            bpy.ops.render.render(animation=False, write_still=True, layer='', scene='packScene')
            
            currentFrame = bpy.data.scenes['packScene'].frame_current
            bpy.data.scenes['packScene'].frame_set(currentFrame + 1)
            bpy.context.scene.frame_set(currentFrame + 1)
       
            i+=1
        
        #test
        bpy.data.scenes['packScene'].frame_set(currentFrame - 1)
        bpy.data.images[inputName].reload()
        
        #display saved location
        self.report({'INFO'}, "Image Saved at " + f )
        
        bpy.context.scene.render.filepath = revert
        
        return {"FINISHED"}

class SourceSelect(bpy.types.Operator):
    bl_idname = "scene.sourceselect"
    bl_label = "use PNG sequence"
    
    def execute(self, context):
        if (bpy.data.scenes["packScene"]["isLiveRender"] == 1):
            bpy.data.scenes["packScene"]["isLiveRender"] = 0
        else:
            bpy.data.scenes["packScene"]["isLiveRender"] = 1
        
        return {"FINISHED"}

class MyOptions(bpy.types.Panel):    
    bl_idname = "SCENE_PT_layout_gp_output"
    bl_label = "Pack To Grid"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    
    def draw(self, context):
        
        bitRes = bpy.data.scenes["packScene"]["bitRes"]
        frames = str(bitRes*bitRes)
        unused = str((bitRes*bitRes)-bpy.data.scenes["packScene"]["frameLength"])
        unusedSize = str(((bitRes*bitRes)-bpy.data.scenes["packScene"]["frameLength"])*bpy.data.scenes["packScene"]["imageSize"])
        
        layout = self.layout
        row = layout.row()
        layout.prop(bpy.data.scenes["packScene"], '["Name"]', text='Output Name')
        
        row = layout.row()
        row.scale_y = 3.0
        row.operator("scene.packtexture")
            
        if (bpy.data.scenes["packScene"]["isLiveRender"] == 0):
            row = layout.row()
            sctext = "use SCENE as source instead"
            layout.label(text="Current Source is IMAGE SEQUENCE")
            
            
            #select source
            row = layout.row()
            row.operator("scene.sourceselect", text = sctext)  
            row = layout.row()
            
            #PNG nodetree
            row = layout.row()
            tree = bpy.data.scenes["packScene"].node_tree
            seq_node = bpy.data.scenes["packScene"].node_tree.nodes['packSquare']
            layout.template_node_view(tree, seq_node, seq_node.inputs['sourceSequence'])
            layout.prop(bpy.data.scenes["packScene"], '["sourceSize"]', text='Source Raw Size')
            
        else:
            sctext = "use IMAGE SEQUENCE as source instead"
            layout.label(text="Current Source is SCENE")
            
            #select source
            row = layout.row()
            row.operator("scene.sourceselect", text = sctext)
            
            #scene nodetree
            row = layout.row()
            tree = bpy.data.scenes["packScene"].node_tree
            seq_node = bpy.data.scenes["packScene"].node_tree.nodes['packSquare']
            layout.template_node_view(tree, seq_node, seq_node.inputs['sourceScene'])
        
        #Pack settings
        row = layout.row()
        layout.label(text="Pack Settings:")
        layout.prop(bpy.data.scenes["packScene"], '["canvasSize"]', text ='Packed Canvas Size')
        layout.prop(bpy.data.scenes["packScene"], '["imageSize"]', text = 'Packed Image Size')        
        row = layout.row(align=True)
        row.prop(bpy.data.scenes["packScene"], '["start frame"]')
        row.prop(bpy.data.scenes["packScene"], '["end frame"]')
        
bpy.utils.register_class(MyOptions)
bpy.utils.register_class(SourceSelect)    
bpy.utils.register_class(PackTex)