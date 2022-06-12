import bpy

class AddReels(bpy.types.Operator):
    bl_idname = "scene.addreels"
    bl_label = "New Symbol Layout"
    
    def execute(self, context):
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        try:
            cam = bpy.context.scene.camera.data.name
            scale = bpy.data.cameras[cam].ortho_scale
            print(scale)
                    
            bpxPlane = bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            mod = bpy.ops.object.modifier_add(type='NODES')
            bpxNodes = bpy.data.node_groups["bpx_symbolGrid"]
            geo = bpy.context.object.modifiers["GeometryNodes"]
            geo.node_group = bpxNodes
            
            geo["Input_20"] = xVal
            geo["Input_21"] = yVal
            geo["Input_22"] = scale
            geo["Input_28_attribute_name"] = "UVMap"
            geo["Input_55"] = bpy.context.object
            
            bpy.ops.object.geometry_nodes_input_attribute_toggle(prop_path="[\"Input_28_use_attribute\"]", modifier_name="GeometryNodes")
            
            geo["Output_27_attribute_name"] = "UVMap"
            geo["Output_35_attribute_name"] = "frameWidth"
            geo["Output_36_attribute_name"] = "frameHeight"
            geo["Output_37_attribute_name"] = "coverWidth"
            geo["Output_38_attribute_name"] = "coverHeight"
            geo["Output_39_attribute_name"] = "BGwidth"
            geo["Output_40_attribute_name"] = "BGheight"
            geo["Output_41_attribute_name"] = "symbolWidth"
            geo["Output_42_attribute_name"] = "symbolHeight"
            geo["Output_43_attribute_name"] = "unitSpacingX"
            geo["Output_44_attribute_name"] = "unitSpacingY"
            geo["Output_45_attribute_name"] = "symbolPosition"
            geo["Output_54_attribute_name"] = "centerPosition"
            
            
            bpy.ops.scene.setdefaultmat()
        except:
            self.report({'INFO'}, "Add a camera before creating a symbol grid!")

                        
        return {"FINISHED"}
    
class SetDefaultMat(bpy.types.Operator):
    bl_idname = "scene.setdefaultmat"
    bl_label = "Set Default Material"

    def execute(self, context):
        
        #check if defaultMat exists
        for mat in bpy.data.materials:
            if mat.name == "bpx_geoMap":
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
            object = "bpx_geoMap"

            library = path + subFolder
            xfilepath = path + subFolder + object

            bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
            
        selected = bpy.context.object
        
        if (len(selected.material_slots) < 1):
            selected.data.materials.append(None)

        selected.material_slots[0].material = bpy.data.materials["bpx_defaultMat"]
        
        mat = bpy.context.object.material_slots[0].material
        newmat = mat.copy()
        
        #name new material here?
        bpy.context.object.material_slots[0].material = newmat
                
        return {"FINISHED"}

class RenderTemplates(bpy.types.Operator):
    bl_idname = "scene.rendertemplates"
    bl_label = "Render Template Images"
    
    def execute(self, context):
        
        useSymbols = bpy.context.object.modifiers["GeometryNodes"]["Input_31"]
        useCovers = bpy.context.object.modifiers["GeometryNodes"]["Input_29"]
        useBG = bpy.context.object.modifiers["GeometryNodes"]["Input_30"]
        useFrame = bpy.context.object.modifiers["GeometryNodes"]["Input_32"]
        AnimateCovers = bpy.context.object.modifiers["GeometryNodes"]["Input_46"]
        AnimateSymbols = bpy.context.object.modifiers["GeometryNodes"]["Input_47"]
        thisName = bpy.context.object.name
        bpy.context.scene.render.film_transparent = True                
                
        bpy.context.object.modifiers["GeometryNodes"]["Input_31"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_29"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_30"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_32"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_46"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_47"] = 0
        
        #render symbols
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Symbols" 
        render.filepath = "//Templates//ScreenSize//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath


        #render Covers
        bpy.context.object.modifiers["GeometryNodes"]["Input_31"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_29"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_30"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_32"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_46"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_47"] = 0
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Covers" 
        render.filepath = "//Templates//ScreenSize//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        scene.frame_start = revertStart
        scene.frame_end = revertEnd        
        
        #render Background
        bpy.context.object.modifiers["GeometryNodes"]["Input_31"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_29"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_30"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_32"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_46"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_47"] = 0
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Background" 
        render.filepath = "//Templates//ScreenSize//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        scene.frame_start = revertStart
        scene.frame_end = revertEnd   
        
        #render Frame
        bpy.context.object.modifiers["GeometryNodes"]["Input_31"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_29"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_30"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_32"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_46"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_47"] = 0
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Frame" 
        render.filepath = "//Templates//ScreenSize"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        scene.frame_start = revertStart
        scene.frame_end = revertEnd

        #prep symbol template
        mainScene = bpy.context.window.scene
        
        #get values
        symbolGridData = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        symbolWidth = bpy.context.object.modifiers["GeometryNodes"]["Input_3"]
        symbolHeight = bpy.context.object.modifiers["GeometryNodes"]["Input_4"]
        coverWidth = symbolGridData.attributes["coverWidth"].data[0].value
        coverHeight = symbolGridData.attributes["coverHeight"].data[0].value
        frameWidth = symbolGridData.attributes["frameWidth"].data[0].value
        frameHeight = symbolGridData.attributes["frameHeight"].data[0].value
        BGwidth = symbolGridData.attributes["BGwidth"].data[0].value
        BGheight = symbolGridData.attributes["BGheight"].data[0].value
        
        
        
        ##
        ##
        #new scenes
        
        if frameWidth > frameHeight:
            frameSize = frameWidth
        else:
            frameSize = frameHeight
        
        power = 0
        num = frameSize
        i=0
        while i < 20:
            pow = 2**i
            if pow > num:
                power = pow
                break;
            i += 1

        #render template symbol        
        #create new scene to render from
        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = "FrameTemplate"
        
        #set render resolution to nearest power of 2
        bpy.context.scene.render.resolution_x = power
        bpy.context.scene.render.resolution_y = power
        
        #create new camera for render
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.data.ortho_scale = 10
        scene.camera = bpy.context.view_layer.objects.active
            
        #spawn new plane at symbol size
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        cam = bpy.context.scene.camera.data.name
        scale = bpy.data.cameras[cam].ortho_scale

        bpy.ops.object.add_named(name = thisName)
        
        bpxNodes = bpy.data.node_groups["bpx_symbolGrid"]
        geo = bpy.context.object.modifiers["GeometryNodes"]
        geo.node_group = bpxNodes
        
        geo["Input_20"] = xVal
        geo["Input_21"] = yVal
        geo["Input_22"] = scale
        geo["Input_53"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_31"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_29"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_30"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_32"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_46"] = 0
        bpy.context.object.modifiers["GeometryNodes"]["Input_47"] = 0
        
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0
        
        bpy.context.scene.render.film_transparent = True
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Frame"    
        render.filepath = "//Templates//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered Template at "+ render.filepath)
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        scene.frame_start = revertStart
        scene.frame_end = revertEnd
        
        bpy.context.window.scene = mainScene
        
        
        
        
        #prep symbol template
        mainScene = bpy.context.window.scene
        
        #get values
        symbolGridData = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        symbolWidth = bpy.context.object.modifiers["GeometryNodes"]["Input_3"]
        symbolHeight = bpy.context.object.modifiers["GeometryNodes"]["Input_4"]
        coverWidth = symbolGridData.attributes["coverWidth"].data[0].value
        coverHeight = symbolGridData.attributes["coverHeight"].data[0].value
        if symbolWidth > symbolHeight:
            symbolSize = symbolWidth
        else:
            symbolSize = symbolHeight
        
        power = 0
        num = symbolSize
        i=0
        while i < 20:
            pow = 2**i
            if pow > num:
                power = pow
                break;
            i += 1

        #render template symbol        
        #create new scene to render from
        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = "SymbolTemplate"

        
        #set render resolution to nearest power of 2
        bpy.context.scene.render.resolution_x = power
        bpy.context.scene.render.resolution_y = power
        
        #create new camera for render
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.data.ortho_scale = 10
        scene.camera = bpy.context.view_layer.objects.active
            
        #spawn new plane at symbol size
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        cam = bpy.context.scene.camera.data.name
        scale = bpy.data.cameras[cam].ortho_scale
        print(scale)
                
        bpxPlane = bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        mod = bpy.ops.object.modifier_add(type='NODES')
        bpxNodes = bpy.data.node_groups["bpx_geo"]
        geo = bpy.context.object.modifiers["GeometryNodes"]
        geo.node_group = bpxNodes
        
        geo["Input_20"] = xVal
        geo["Input_21"] = yVal
        geo["Input_22"] = scale
        geo["Input_3"] = symbolWidth
        geo["Input_4"] = symbolHeight
        
        bpy.context.scene.render.film_transparent = True
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Symbol_Template"
        render.filepath = "//Templates//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered Templates at "+ render.filepath)
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        
        bpy.context.window.scene = mainScene
        
        
        #render template cover   
        
        if coverWidth > coverHeight:
            coverSize = coverWidth
        else:
            coverSize = coverHeight
        
        power = 0
        num = coverSize
        i=0
        while i < 20:
            pow = 2**i
            if pow > num:
                power = pow
                break;
            i += 1 

        #create new scene to render from
        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = "CoverTemplate"
        
        #set render resolution to nearest power of 2
        bpy.context.scene.render.resolution_x = power
        bpy.context.scene.render.resolution_y = power
        
        #create new camera for render
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.data.ortho_scale = 10
        scene.camera = bpy.context.view_layer.objects.active
            
        #spawn new plane at symbol size
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        cam = bpy.context.scene.camera.data.name
        scale = bpy.data.cameras[cam].ortho_scale
        print(scale)
                
        bpxPlane = bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        mod = bpy.ops.object.modifier_add(type='NODES')
        bpxNodes = bpy.data.node_groups["bpx_geo"]
        geo = bpy.context.object.modifiers["GeometryNodes"]
        geo.node_group = bpxNodes
        
        geo["Input_20"] = xVal
        geo["Input_21"] = yVal
        geo["Input_22"] = scale
        geo["Input_3"] = coverWidth
        geo["Input_4"] = coverHeight
        
        bpy.context.scene.render.film_transparent = True
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Cover_Template"       
        render.filepath = "//Templates//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered Templates at "+ render.filepath)
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        
        bpy.context.window.scene = mainScene
        
        
        #render template background
        if BGwidth > BGheight:
            BGsize = BGwidth
        else:
            BGsize = BGheight
        
        power = 0
        num = BGsize
        i=0
        while i < 20:
            pow = 2**i
            if pow > num:
                power = pow
                break;
            i += 1 
        #create new scene to render from
        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = "BackgroundTemplate"
        
        #set render resolution to nearest power of 2
        bpy.context.scene.render.resolution_x = power
        bpy.context.scene.render.resolution_y = power
        
        #create new camera for render
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.data.ortho_scale = 10
        scene.camera = bpy.context.view_layer.objects.active
            
        #spawn new plane at symbol size
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        cam = bpy.context.scene.camera.data.name
        scale = bpy.data.cameras[cam].ortho_scale
        print(scale)
                
        bpxPlane = bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        mod = bpy.ops.object.modifier_add(type='NODES')
        bpxNodes = bpy.data.node_groups["bpx_geo"]
        geo = bpy.context.object.modifiers["GeometryNodes"]
        geo.node_group = bpxNodes
        
        geo["Input_20"] = xVal
        geo["Input_21"] = yVal
        geo["Input_22"] = scale
        geo["Input_3"] = BGwidth
        geo["Input_4"] = BGheight
        
        bpy.context.scene.render.film_transparent = True
        
        scene = bpy.context.scene
        render = scene.render
        revert = render.resolution_percentage
        revertStart = scene.frame_start
        revertEnd = scene.frame_end                
        currentFrame = scene.frame_current        
        revertPath = render.filepath

        renderName = "Background_Template"
        render.filepath = "//Templates//"+renderName+"_"
        
        scene.frame_start = currentFrame
        scene.frame_end = currentFrame
        
        render.resolution_percentage = 100

        newX = round(render.resolution_x)
        newY = round(render.resolution_y)
        
        bpy.ops.render.render(animation=True, use_viewport=True)
        bpy.ops.render.view_show('INVOKE_DEFAULT')
                
        self.report({'INFO'}, "rendered Templates at "+ render.filepath)
        
        render.resolution_percentage = revert
        scene.frame_start = 0
        scene.frame_end = 0
        render.filepath = revertPath
        
        bpy.context.window.scene = mainScene
                        
        return {"FINISHED"}

class PrintInfo(bpy.types.Operator):
    bl_idname = "scene.printinfo"
    bl_label = "Print Layout Info To Console"
    
    def execute(self, context):
        symbolGridData = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get()).data

        frameWidth = symbolGridData.attributes["frameWidth"].data[0].value
        frameHeight = symbolGridData.attributes["frameHeight"].data[0].value
        coverWidth = symbolGridData.attributes["coverWidth"].data[0].value
        coverHeight = symbolGridData.attributes["coverHeight"].data[0].value
        BGwidth = symbolGridData.attributes["BGwidth"].data[0].value
        BGheight = symbolGridData.attributes["BGheight"].data[0].value
        symbolWidth = bpy.context.object.modifiers["GeometryNodes"]["Input_3"]
        symbolHeight = bpy.context.object.modifiers["GeometryNodes"]["Input_4"]
        unitSpacingX = symbolGridData.attributes["unitSpacingX"].data[0].value
        unitSpacingY = symbolGridData.attributes["unitSpacingY"].data[0].value
        centerPosition = symbolGridData.attributes["centerPosition"].data[0].vector

        gapSizeX = bpy.context.object.modifiers["GeometryNodes"]["Input_25"]
        gapSizeY = bpy.context.object.modifiers["GeometryNodes"]["Input_23"]

        amountX = bpy.context.object.modifiers["GeometryNodes"]["Input_26"]
        amountY = bpy.context.object.modifiers["GeometryNodes"]["Input_24"]

        print("")
        print("")
        print("Values in Pixels")
        print("Symbol Size: "+str(symbolWidth) + "px x " + str(symbolHeight) + "px")
        print("Covers Size (each): "+str(coverWidth) + "px x " + str(coverHeight) + "px")
        print("Play Area Background: "+str(BGwidth) + "px x " + str(BGheight) + "px")
        print("Full Frame Size: "+str(frameWidth) + "px x " + str(frameHeight) + "px")
        print("Symbol Gap X: "+str(gapSizeX) + "px")
        print("Symbol Gap Y: "+str(gapSizeY) + "px")

        print("")
        print("Symbol Position in Units")

        symbolTotal = amountX * amountY
        i = 0
        while i < symbolTotal:
            symbolPosition = symbolGridData.attributes["symbolPosition"].data[i].vector
            print(symbolPosition)
            i += 1
            
        print("")
        print("Grid Center in Units")  
        print(centerPosition)  

        print("")
        print("Uniform Spacing in Units")  
        print("Spacing X: "+str(unitSpacingX) + " units")
        print("Spacing Y: "+str(unitSpacingY) + " units")

                        
        return {"FINISHED"}

class SetEmpties(bpy.types.Operator):
    bl_idname = "scene.setempties"
    bl_label = "Make Layout Rig"
    
    def execute(self, context):
        selected = bpy.context.view_layer.objects.active
        symbolGridData = selected.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        centerPosition = symbolGridData.attributes["centerPosition"].data[0].vector
        amountX = bpy.context.object.modifiers["GeometryNodes"]["Input_26"]
        amountY = bpy.context.object.modifiers["GeometryNodes"]["Input_24"]
        symbolTotal = amountX * amountY
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0,0,0), scale=(1, 1, 1))
        worldCenter = bpy.context.object
        bpy.context.object.name = "Scene_Root"
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = selected
        selected.select_set(True)
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(centerPosition), scale=(1, 1, 1))
        parentObj = bpy.context.object
        bpy.context.object.name = "SymbolPositions"
        bpy.context.object.parent = worldCenter
        #bpy.context.object.matrix_parent_inverse = worldCenter.matrix_world.inverted()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = selected
        selected.select_set(True)
        
        i = 0
        while i < symbolTotal:
            selected = bpy.context.view_layer.objects.active
            symbolGridData = selected.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
            
            symbolPosition = symbolGridData.attributes["symbolPosition"].data[i].vector
            bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(symbolPosition), scale=(1, 1, 1))
            bpy.context.object.name = "Symbol_" + str(i)
            bpy.context.object.parent = parentObj
            bpy.context.object.matrix_parent_inverse = parentObj.matrix_world.inverted()
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = selected
            selected.select_set(True)
            i += 1

                        
        return {"FINISHED"}
    
class LayoutHelper(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Symbol Grids"
    bl_label = "Grid Creator"
    bl_idname = "SCENE_PT_layout_LayoutHelper"
    
    def draw(self, context):
        scene = bpy.context.scene
        render = scene.render
        
        layout = self.layout
        row = layout.row()
        self.layout.label(text="Create New")
        row = layout.row()
        row.operator("scene.addreels")
        
        row = layout.row()
        self.layout.label(text="Symbol Layout Information")
        row = layout.row()
        row.operator("scene.printinfo")
        row = layout.row()
        row.operator("scene.rendertemplates")
        row = layout.row()
        row.operator("scene.setempties")

def register():   
    bpy.utils.register_class(LayoutHelper)
    bpy.utils.register_class(PrintInfo)
    bpy.utils.register_class(RenderTemplates)
    bpy.utils.register_class(SetEmpties)
    bpy.utils.register_class(SetDefaultMat)
    bpy.utils.register_class(AddReels)
    
register()