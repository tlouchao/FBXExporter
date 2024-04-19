import bpy

class OP_Auto_Spline(bpy.types.Operator):

    bl_idname = "op.auto_spline"
    bl_label = "Generate Spline"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH')

    def execute(self, context):
        
        my_variable = "Hello World"
        print (my_variable) # Prints 'Hello World' to the Console
        self.report({'INFO'}, my_variable) # Reports 'Hello World' to the Info Area
        
        return {'FINISHED'} # Return the execution is finished
    

class OP_Export_FBX(bpy.types.Operator):

    bl_idname = "op.export_fbx"
    bl_label = "Export FBX to Unreal"

    def execute(self, context):
        
        dname = "C:/Users/tiffa/Documents/Elvtr/TART07"
        content_folder = "TART07/Content/TART07"
        fname = "LOLFBX"
        filepath = dname + '/' + content_folder  + '/' + fname + ".fbx"
        
        bpy.ops.export_scene.fbx(filepath=filepath)
        
        self.report({'INFO'}, f"Exported {fname}.fbx to {dname}/{content_folder}")
        return {'FINISHED'}
    

class VIEW3D_Auto_Spline(bpy.types.Panel):
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tiffany's Test"
    bl_context = "objectmode"
    
    bl_idname = "VIEW3D_AUTO_SPLINE"
    bl_label = "Tiffany's Auto Spline Rig Tool"
    
    def draw(self, context):
        self.layout.label(text="Testing Testing")
        row = self.layout.row()
        row.operator(OP_Auto_Spline.bl_idname)
        row.operator(OP_Export_FBX.bl_idname)
        
def register():
    bpy.utils.register_class(OP_Auto_Spline)
    bpy.utils.register_class(OP_Export_FBX)
    bpy.utils.register_class(VIEW3D_Auto_Spline)
    
def unregister():
    bpy.utils.unregister_class(OP_Auto_Spline)
    bpy.utils.unregister_class(OP_Export_FBX)
    bpy.utils.unregister_class(VIEW3D_Auto_Spline)
    
if __name__ == "__main__":
    register()