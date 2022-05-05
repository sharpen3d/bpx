import bpy

thisFilePath = bpy.data.filepath
thisFileName = bpy.path.basename(bpy.context.blend_data.filepath)
currentPath = thisFilePath.replace(thisFileName, "")
currentPath = currentPath[:-1]


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
    
class Button2(bpy.types.Operator):
    bl_idname = "scene.button2"
    bl_label = "add layer"

    def execute(self, context):
        
        xVal = bpy.context.scene.render.resolution_x
        yVal = bpy.context.scene.render.resolution_y
        cam = bpy.context.scene.camera.name
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
        
        
        #solidName = bpy.context.scene["bpxName"]
        #bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name= solidName)
                
        return {"FINISHED"}
    
class SelectCam(bpy.types.Operator):
    bl_idname = "scene.selectcam"
    bl_label = "Select Camera"

    def execute(self, context):
        bpy.ops.object.select_camera()
                
        return {"FINISHED"}

class ResetCam(bpy.types.Operator):
    bl_idname = "scene.resetcam"
    bl_label = "Make Camera 2D"

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
        row.operator("scene.button2", text= "Add Layer")    
        
        row = layout.row()
        row.operator("scene.resetcam")  
            
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
                                cam = bpy.context.scene.camera.name
                                scale = bpy.data.cameras[cam].ortho_scale
                        
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
                                self.layout.label(text = "size= "+str(geo["Input_3"]) + "x" + str(geo["Input_4"]))
                                self.layout.label(text= "Z Index= " + str(zLayer))
                                
                                row = layout.row()
                                row.prop(geo, '["Input_3"]', text = "width")
                                row = layout.row()
                                row.prop(geo, '["Input_4"]', text = "height")
                                row = layout.row()
                                row.prop(geo, '["Input_2"]', text = "match cam size")
                                                
                                #row = layout.row()
                                #row.operator("scene.editselected")
                                #row = layout.row()
                                #row.operator("scene.canvassize")
                                #row = layout.row()
                    
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
        row.operator("scene.storeimages")
        #row = layout.row()     
        #row.operator("scene.packview")

def register():  
    bpy.utils.register_class(StoreImages)     
    bpy.utils.register_class(Selected)
    bpy.utils.register_class(SelectCam)
    bpy.utils.register_class(Button2)
    bpy.utils.register_class(MyOptions)
    bpy.utils.register_class(ResetCam)
    
register()