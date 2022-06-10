import bpy

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]

class PivotMenu(bpy.types.Menu):
    bl_label = "Set Pivot"
    bl_idname = "PIVOT_MT_pivotmenu"

    def draw(self, context):
        layout = self.layout

        layout.operator("scene.pivotcenter")
        layout.operator("scene.pivotbottomleft")
        layout.operator("scene.pivotbottomright")
        layout.operator("scene.pivottopleft")
        layout.operator("scene.pivottopright")
        layout.operator("scene.pivotleftcenter")
        layout.operator("scene.pivottopcenter")
        layout.operator("scene.pivotrightcenter")
        layout.operator("scene.pivotbottomcenter")
        
class MatMenu(bpy.types.Panel):
    bl_label = "Set Pivot"
    bl_idname = "MAT_PT_matmenu"
    bl_options = {'INSTANCED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    is_popover = True

    def draw(self, context):
        layout = self.layout
        row = layout.row
        column = layout.column

        selected = bpy.context.object
        if (len(selected.material_slots) > 0):
            for node in selected.material_slots[0].material.node_tree.nodes:
                if node.name == "bpy_TransparentImage":                                        
                    tree = selected.material_slots[0].material.node_tree
                    imagenode = selected.material_slots[0].material.node_tree.nodes['bpy_TransparentImage'] 
                    
                    row = layout.row()
                    layout.label(text="Image Texture:")
                    layout.template_node_view(tree, imagenode, imagenode.inputs["ImageColor"])
                    row = layout.row()
                    
                    break 

class ShowPivotMenu(bpy.types.Operator):
    bl_idname = "scene.showpivotmenu"
    bl_label = "PivotMenu"
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name=PivotMenu.bl_idname)
                
        return {"FINISHED"}
    
class ShowMatMenu(bpy.types.Operator):
    bl_idname = "scene.showmatmenu"
    bl_label = "PivotMenu"
    
    def execute(self, context):
        bpy.ops.wm.call_panel(name=MatMenu.bl_idname)
                
        return {"FINISHED"}
    
class PivotCenter(bpy.types.Operator):
    bl_idname = "scene.pivotcenter"
    bl_label = "Centered"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 0
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}

class PivotBottomLeft(bpy.types.Operator):
    bl_idname = "scene.pivotbottomleft"
    bl_label = "Bottom-Left"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 1
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()  
        return {"FINISHED"}
    
class PivotBottomRight(bpy.types.Operator):
    bl_idname = "scene.pivotbottomright"
    bl_label = "Bottom-Right"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 2
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}
    
class PivotTopLeft(bpy.types.Operator):
    bl_idname = "scene.pivottopleft"
    bl_label = "Top-Left"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 3
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}
    
class PivotTopRight(bpy.types.Operator):
    bl_idname = "scene.pivottopright"
    bl_label = "Top-Right"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 4
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}

class PivotLeftCenter(bpy.types.Operator):
    bl_idname = "scene.pivotleftcenter"
    bl_label = "Left-Center"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 5
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}

class PivotTopCenter(bpy.types.Operator):
    bl_idname = "scene.pivottopcenter"
    bl_label = "Top-Center"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 6
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}

class PivotRightCenter(bpy.types.Operator):
    bl_idname = "scene.pivotrightcenter"
    bl_label = "Right-Center"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 7
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}
    
class PivotBottomCenter(bpy.types.Operator):
    bl_idname = "scene.pivotbottomcenter"
    bl_label = "Bottom-Center"
    
    def execute(self, context):
        bpy.context.object.modifiers["GeometryNodes"]["Input_25"] = 8
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()                
        return {"FINISHED"}

#turned off
class StoreImages(bpy.types.Operator):
    bl_idname = "scene.storeimages"
    bl_label = "isolateCollection"
    
    def execute(self, context):
        collect = bpy.context.view_layer.active_layer_collection

        
        for x in bpy.data.collections:
            if x.name != collect.name:
                bpy.data.collections[x.name].hide_viewport = True
                bpy.data.collections[x.name].hide_render = True
            else:
                bpy.data.collections[x.name].hide_viewport = False
                bpy.data.collections[x.name].hide_render = False

                
        return {"FINISHED"}
    
class MatchTexSize(bpy.types.Operator):
    bl_idname = "scene.matchtexsize"
    bl_label = "Match Texture Size"
    bl_description = "Make this plane size match the given texture size above"
    
    def execute(self, context):
        selected = bpy.context.object
        geo = bpy.context.object.modifiers["GeometryNodes"]
        
        texWidth = selected.material_slots[0].material.node_tree.nodes["Image Texture"].image.size[0]
        texHeight = selected.material_slots[0].material.node_tree.nodes["Image Texture"].image.size[1]
        selected.modifiers["GeometryNodes"]["Input_3"] = texWidth
        selected.modifiers["GeometryNodes"]["Input_4"] = texHeight
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
                
        return {"FINISHED"}

class FixPix(bpy.types.Operator):
    bl_idname = "scene.fixpix"
    bl_label = "Fix Pixel Size"
    bl_description = "Update this plane size to match current render and camera conditions"
    
    def execute(self, context):
        selected = bpy.context.object
        geo = bpy.context.object.modifiers["GeometryNodes"]
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        cam = bpy.context.scene.camera.data.name
        scale = bpy.data.cameras[cam].ortho_scale
        
        #fixX
        geo["Input_20"] = xVal
        
        #fixY
        geo["Input_21"] = yVal
        
        #fixSize
        geo["Input_22"] = scale
        
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
                
        return {"FINISHED"}
    
class Button2(bpy.types.Operator):
    bl_idname = "scene.button2"
    bl_label = "add layer"
    bl_description = "Add a new 2D plane in current scene"

    def execute(self, context):
        
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        try:
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
            geo["Input_26"] = bpy.context.object
            geo["Output_23_attribute_name"] = "pointPosition"
            geo["Output_27_attribute_name"] = "pointCenter"
            
            bpy.ops.scene.setmat()
        except:
            self.report({'INFO'}, "Add a camera before creating a 2D Layer!")
        
        
        #solidName = bpy.context.scene["bpxName"]
        #bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name= solidName)
                
        return {"FINISHED"}
    
class ScreenLayout(bpy.types.Operator):
    bl_idname = "scene.screenlayout"
    bl_label = "Rig Screen Layout"
    bl_description = "Add Empties defining screen size in Units"

    def execute(self, context):
        scene = bpy.ops.scene
        scene.button2()
        print(bpy.context.object.name)
        bpy.context.object.modifiers["GeometryNodes"]["Input_24"] = 1
        bpy.context.object.modifiers["GeometryNodes"]["Input_2"] = 1
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        scene.layoutrig()
        bpy.ops.object.delete(use_global=True)
        
        return {"FINISHED"}
    
class LayoutRig(bpy.types.Operator):
    bl_idname = "scene.layoutrig"
    bl_label = "Make Layout Rig"
    bl_description = "add empties to each point of the selected solid"

    def execute(self, context):
        selected = bpy.context.view_layer.objects.active
        symbolGridData = selected.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
        
        centerPos = symbolGridData.attributes["pointCenter"].data[0].vector
                
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(centerPos), scale=(1, 1, 1))
        worldCenter = bpy.context.object
        bpy.context.object.name = "LayoutRig_Root"
        #bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name= "EmptyRig")
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = selected
        selected.select_set(True)

        i = 0
        while i < len(symbolGridData.attributes["pointPosition"].data):
            selected = bpy.context.view_layer.objects.active
            symbolGridData = selected.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
            
            try:
                pointPosition = symbolGridData.attributes["pointPosition"].data[i].vector
                bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(pointPosition), scale=(1, 1, 1))
                
                pointName = "LayoutPoint"
                
                if i == 0:
                    pointName = "BottomLeft"
                elif i == 1:
                    pointName = "BottomRight"
                elif i == 2:
                    pointName = "TopLeft"
                elif i == 3:
                    pointName = "TopRight"
                elif i == 4:
                    pointName = "LeftCenter"
                elif i == 5:
                    pointName = "BottomCenter"
                elif i == 6:
                    pointName = "RightCenter"
                elif i == 7:
                    pointName = "TopCenter"
                elif i == 8:
                    pointName = "Center"
            
            except:
                print("no more data points")
                break;
                
            
            bpy.context.object.name = pointName
            #bpy.types.CollectionObjects.link()
            #bpy.ops.object.move_to_collection(collection_index=0)
            
            bpy.context.object.parent = worldCenter
            bpy.context.object.matrix_parent_inverse = worldCenter.matrix_world.inverted()
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = selected
            selected.select_set(True)
            i += 1
        return {"FINISHED"}
    
class SelectCam(bpy.types.Operator):
    bl_idname = "scene.selectcam"
    bl_label = "Select Camera"
    bl_description = "Select the scene's active camera"

    def execute(self, context):
        bpy.ops.object.select_camera()
                
        return {"FINISHED"}
    
class SetMat(bpy.types.Operator):
    bl_idname = "scene.setmat"
    bl_label = "Set Default Material"

    def execute(self, context):
        
        #check if defaultMat exists
        for mat in bpy.data.materials:
            if mat.name == "bpx_defaultMat":
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
            object = "bpx_defaultMat"

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

class ResetCam(bpy.types.Operator):
    bl_idname = "scene.resetcam"
    bl_label = "Make 2D Camera"
    bl_description = "Reset camera rotations, set to orthographic size 10, place at 0,0,10 OR add new camera if no camera exists"

    def execute(self, context):
        
        scene = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        
        for i in bpy.data.scenes[scene.name].objects:
            if i.type == 'CAMERA':
                bpy.context.view_layer.objects.active = i
                i.select_set(True)
                bpy.ops.object.rotation_clear(clear_delta=False)
                bpy.ops.object.location_clear(clear_delta=False)
                bpy.ops.transform.translate(value=(0, 0, 10), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                bpy.context.object.data.type = 'ORTHO'
                bpy.context.object.data.ortho_scale = 10
                scene.camera = bpy.context.view_layer.objects.active
                break
        else:
            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 10), rotation=(0, 0, 0), scale=(1, 1, 1))
            bpy.context.object.data.type = 'ORTHO'
            bpy.context.object.data.ortho_scale = 10
            scene.camera = bpy.context.view_layer.objects.active
                
        return {"FINISHED"}

class AppendTools(bpy.types.Operator):
    bl_idname = "scene.appendtools"
    bl_label = "Append 2D Tools"

    def execute(self, context):
        path = "\\\\NCFS1\\Dev\\Art\\_ArtistShareables_\\blenderTemplates\\2DTemplate\\geoNodes.blend"
        subFolder = "\\NodeTree\\"
        object = "bpx_geo"

        library = path + subFolder
        xfilepath = path + subFolder + object

        bpy.ops.wm.append(filename = object, filepath = xfilepath, directory = library)
                
        return {"FINISHED"}

class Selected(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "2D Tools"
    bl_label = "Solids"
    bl_idname = "SCENE_PT_layout_2D"
    
    @classmethod
    def poll(self,context):     
        isIncluded = False   
        for text in bpy.data.texts:
            if text.name == "2DTools.py":
                isIncluded = True
                break
        return isIncluded == True
    
    def draw(self, context):
        layout = self.layout 
        
        row = layout.row()
        row.operator("scene.resetcam")  
            
        row = layout.row()
        row.operator("scene.button2", text= "Add Layer")    
            
        row = layout.row() 
        obj = bpy.context.object
        
        if (bpy.context.selected_objects != []):
            if (bpy.context.object.type == 'MESH'):
                if(len(obj.modifiers) > 0):
                    if(obj.modifiers[0].node_group.name == "bpx_geo"):
                        for modifier in obj.modifiers:
                            if modifier.type == "NODES":
                                geo = bpy.context.object.modifiers["GeometryNodes"]
                                scene = bpy.context.scene
                                
                                xVal = bpy.context.scene.render.resolution_x
                                yVal = bpy.context.scene.render.resolution_y
                                cam = bpy.context.scene.camera.data.name
                                scale = bpy.data.cameras[cam].ortho_scale
                                
                                if (geo["Input_20"] != xVal) or (geo["Input_21"] != yVal) or (geo["Input_22"] != scale):
                                    layout = self.layout
                                    self.layout.label(text= "Pixel Size Not Accutate")
                                    #fix current
                                    row = layout.row()
                                    row.operator("scene.fixpix")  
                        
                                height = 1024
                                width = 1024
                                sizeVal = width
                                
                                #scene["solidWidth"] = geo["Input_3"]
                                #scene["solidHeight"] = geo["Input_4"]
                                            
                                if (height > width):
                                    sizeVal = height
                                    
                                scaling = sizeVal/scale
                                locX = bpy.context.object.location[0]
                                locY = bpy.context.object.location[1]
                                
                                locXu = locX * scaling
                                locYu = locY * scaling
                                
                                pixLocX = locXu-(width/-2)
                                pixLocY = locYu-(height/-2)
                                zLayer = bpy.context.object.location[2]
                                
                                layout = self.layout
                                row = layout.row()
                                #layout.prop(scene, '["bpxName"]')
                                #self.layout.label(text= "position= " + str(pixLocX)+", "+ str(pixLocY))
                                self.layout.label(text= "Selected:")
                                #self.layout.label(text = "size= "+str(geo["Input_3"]) + "x" + str(geo["Input_4"]))
                                
                                #maybe useful?
                                #self.layout.label(text= "Z Index= " + str(zLayer))
                                
                                row = layout.row()
                                row.prop(geo, '["Input_3"]', text = "width")
                                row = layout.row()
                                row.prop(geo, '["Input_4"]', text = "height")
                                
                                #should be toggle checkbox
                                row = layout.row()
                                row.prop(geo, '["Input_2"]', text = "match cam size")
                                
                                if geo["Input_25"] == 0:
                                    currentPivot = "Centered"
                                elif geo["Input_25"] == 1:
                                    currentPivot = "Bottom-Left"
                                elif geo["Input_25"] == 2:
                                    currentPivot = "Bottom-Right"
                                elif geo["Input_25"] == 3:
                                    currentPivot = "Top-Left"
                                elif geo["Input_25"] == 4:
                                    currentPivot = "Top-Right"
                                elif geo["Input_25"] == 5:
                                    currentPivot = "Left-Center"
                                elif geo["Input_25"] == 6:
                                    currentPivot = "Top-Center"
                                elif geo["Input_25"] == 7:
                                    currentPivot = "Right-Center"
                                else:
                                    currentPivot = "Bottom-Center"
                                
                                row = layout.row()
                                self.layout.label(text= "Pivot:")
                                row = layout.row()
                                row.operator("scene.showpivotmenu", text=currentPivot) 
                                
                                row = layout.row()
                                self.layout.label(text= "Texture:")
                                row = layout.row()
                                row.operator("scene.showmatmenu", text="Set Texture") 
                                
                                row = layout.row()
                                self.layout.label(text= "Rigging:")
                                row = layout.row()
                                row.operator("scene.layoutrig")
                                                
                                #row = layout.row()
                                #row.operator("scene.editselected")
                                #row = layout.row()
                                #row.operator("scene.canvassize")
                                #row = layout.row()
                                
#                                selected = bpy.context.object
#                                if (len(selected.material_slots) > 0):
#                                    for node in selected.material_slots[0].material.node_tree.nodes:
#                                        if node.name == "bpy_TransparentImage":                                        
#                                            tree = selected.material_slots[0].material.node_tree
#                                            imagenode = selected.material_slots[0].material.node_tree.nodes['bpy_TransparentImage'] 
#                                            
#                                            row = layout.row()
#                                            layout.label(text="Image Texture:")

#                                            row = layout.row()
#                                            layout.template_node_view(tree, imagenode, imagenode.inputs["ImageColor"])
#                                            
#                                            row = layout.row()
#                                            row.operator("scene.matchtexsize") 
#                                            
#                                            break 
                                    
                    
class MyOptions(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "2D Tools"
    bl_label = "Composition"
    bl_idname = "SCENE_PT_layout_2D_2"

    @classmethod
    def poll(self,context):     
        isIncluded = False   
        for text in bpy.data.texts:
            if text.name == "2DTools.py":
                isIncluded = True
                break
        return isIncluded == True
    
    def draw(self, context):
        scene = bpy.context.scene
        render = scene.render
        
        layout = self.layout
        row = layout.row()
        self.layout.label(text="Camera Size")
        
        layout.prop(render,'resolution_x', text='width') 
        layout.prop(render,'resolution_y', text='height') 
        #bpy.context.scene.render.resolution_x
        
        row = layout.row()
        self.layout.label(text="Composition")
        
        #row = layout.row()
        #row.operator("scene.button1")
        row = layout.row()
        row.operator("scene.selectcam")
        
        row = layout.row()
        row.operator("scene.screenlayout")
        #row = layout.row()     
        #row.operator("scene.storeimages")
        #row = layout.row()     
        #row.operator("scene.packview")

def register():  
    #bpy.utils.register_class(StoreImages)     
    bpy.utils.register_class(Selected)
    bpy.utils.register_class(SelectCam)
    bpy.utils.register_class(Button2)
    bpy.utils.register_class(MyOptions)
    bpy.utils.register_class(ResetCam)
    bpy.utils.register_class(SetMat)
    bpy.utils.register_class(MatchTexSize)
    bpy.utils.register_class(FixPix)
    bpy.utils.register_class(LayoutRig)
    bpy.utils.register_class(ScreenLayout)
    bpy.utils.register_class(PivotMenu)
    bpy.utils.register_class(ShowPivotMenu)
    bpy.utils.register_class(MatMenu)
    bpy.utils.register_class(ShowMatMenu)
    
    #Pivot Menu
    bpy.utils.register_class(PivotCenter)
    bpy.utils.register_class(PivotBottomLeft)
    bpy.utils.register_class(PivotBottomRight)
    bpy.utils.register_class(PivotTopLeft)
    bpy.utils.register_class(PivotTopRight)
    bpy.utils.register_class(PivotLeftCenter)
    bpy.utils.register_class(PivotTopCenter)
    bpy.utils.register_class(PivotRightCenter)
    bpy.utils.register_class(PivotBottomCenter)
    
register()