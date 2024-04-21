import bpy
import inspect
from .. import constants, operators, properties
from ..properties import PG_Properties
from ..constants import PanelTypes


class VIEW3D_PT_BLInfo:

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FBX Exporter"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        io_scene_props = scene.io_ue5_fbx
        return [layout, io_scene_props]
    

class VIEW3D_PT_FBXExporter(VIEW3D_PT_BLInfo, bpy.types.Panel):
      
    bl_idname = "VIEW3D_PT_FBXExporter"
    bl_label = "Export FBX to Unreal Engine 5"  
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH')
    
    def draw(self, context):
        pass


class VIEW3D_PT_Filepath(VIEW3D_PT_BLInfo, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Filepath"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):

        [layout, io_scene_props] = super(VIEW3D_PT_Filepath, self).draw(context)

        io_props = PG_Properties.get_props(PanelTypes.FILEPATH)
        for k, v in io_props.items():
            label = v.keywords.get('name')
            layout.label(text=label)
            row = layout.row()
            row.prop(io_scene_props, k, text='')


class VIEW3D_PT_Blender(VIEW3D_PT_BLInfo, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Blender"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        [layout, io_scene_props] = super(VIEW3D_PT_Blender, self).draw(context)

        io_props = PG_Properties.get_props(PanelTypes.BLENDER)
        for k in io_props:
            row = layout.row()
            row.prop(io_scene_props, k)


class VIEW3D_PT_Button(VIEW3D_PT_BLInfo, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Export"
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        
        [layout, io_scene_props] = super(VIEW3D_PT_Button, self).draw(context)

        row_ex = layout.row()
        row_ex.operator(operators.OP_OT_Export.bl_idname)

panel_classes = [
    VIEW3D_PT_FBXExporter,
    VIEW3D_PT_Filepath,
    VIEW3D_PT_Blender,
    VIEW3D_PT_Button,
]

def register():
    """
    Registers the ui classes when the addon is enabled.
    """
    for panel_class in panel_classes:
        bpy.utils.register_class(panel_class)


def unregister():
    """
    Unregisters the ui classes when the addon is disabled.
    """
    for panel_class in reversed(panel_classes):
        bpy.utils.unregister_class(panel_class)
