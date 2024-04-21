import bpy
from .. import constants, operators, properties


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

        layout = self.layout
        scene = context.scene
        io_props = scene.io_ue5_fbx

        # is there another way to get keys?
        io_keys = properties.PG_Properties.__annotations__
        for key in io_keys:
            row = layout.row()
            row.prop(io_props, key)
        
        row_ex = layout.row()
        row_ex.operator(operators.OP_OT_Export.bl_idname)


def register():
    """
    Registers the ui classes when the addon is enabled.
    """
    bpy.utils.register_class(VIEW3D_PT_FBXExporter)


def unregister():
    """
    Unregisters the ui classes when the addon is disabled.
    """
    bpy.utils.unregister_class(VIEW3D_PT_FBXExporter)
