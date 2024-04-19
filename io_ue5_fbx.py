bl_info = \
{
    "name": "Export FBX from Blender to Unreal Engine 5 (.fbx)",
    "author": "tlouchao",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar > FBX Exporter",
    "description": "Exports the selected mesh, armature, and animation to Unreal Engine 5",
    "category": "Import-Export",
}

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
    

class OP_Export(bpy.types.Operator):

    bl_idname = "op.export"
    bl_label = "Export FBX"

    def execute(self, context):
        
        dname = "C:/Users/tiffa/Documents/Elvtr/TART07"
        content_folder = "TART07/Content/TART07"
        fname = "leaf"
        filepath = dname + '/' + content_folder  + '/' + fname + ".fbx"
        
        bpy.ops.export_scene.fbx(filepath=filepath)
        
        self.report({'INFO'}, f"Exported {fname}.fbx to {dname}/{content_folder}")
        return {'FINISHED'}
    

class VIEW3D_PT_FBXExporter(bpy.types.Panel):
    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FBX Exporter"
    bl_context = "objectmode"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    bl_idname = "VIEW3D_PT_FBXExporter"
    bl_label = "Export FBX to Unreal Engine 5"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH')
    
    def draw(self, context):
        self.layout.label(text="Default Parameters")
        row = self.layout.row()
        row.operator(OP_Export.bl_idname)


def register():
    bpy.utils.register_class(OP_Export)
    bpy.utils.register_class(VIEW3D_PT_FBXExporter)
    
def unregister():
    bpy.utils.unregister_class(OP_Export)
    bpy.utils.unregister_class(VIEW3D_PT_FBXExporter)

if __name__ == "__main__":
    register()