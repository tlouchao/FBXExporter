import bpy
import os
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
        io_props = scene.io_ue5_fbx
        return [layout, io_props]
    

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

        [layout, io_props] = super(VIEW3D_PT_Filepath, self).draw(context)
        fp_props = PG_Properties.get_props(PanelTypes.FILEPATH)

        k2 = io_props.keys()
        for k in k2:
            j = k
        
        for key in fp_props:
            if key == 'fp_project_dir' or key == 'fp_project_subdir':
                
                # label
                label = PG_Properties.get_prop_name(key)
                row = layout.row()
                row.label(text=label)
                
                # edit field
                split = layout.split(factor=0.8)
                [lcol, rcol] = split.column(), split.column(align=True)

                ph = PG_Properties.get_placeholder(key)
                lcol.prop(io_props, key, text='', placeholder=ph)
                rcol.operator(operators.OP_OT_Filename.bl_idname)

            elif key == 'fp_file_name':

                # label and edit field on same row
                layout.row().separator()
                split = layout.split(factor=0.8)
                [lcol, rcol] = split.column(), split.column(align=True)
                lsplit = lcol.split(factor=0.3)
                [llcol, lrcol] = lsplit.column(), lsplit.column()

                label = PG_Properties.get_prop_name(key)
                llcol.label(text=label)
                lrcol.prop(io_props, key, text='')
                rcol.operator(operators.OP_OT_Filename.bl_idname)


class VIEW3D_PT_Blender(VIEW3D_PT_BLInfo, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Blender"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        [layout, io_props] = super(VIEW3D_PT_Blender, self).draw(context)
        bl_props = PG_Properties.get_props(PanelTypes.BLENDER)

        for key in bl_props:
            row = layout.row()
            row.prop(io_props, key)


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
