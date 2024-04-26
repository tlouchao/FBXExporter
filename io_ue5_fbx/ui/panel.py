import bpy
import os
import inspect
from .. import constants, operators, properties
from ..constants import BlenderUnits, AddonUnits


class Base_Panel:

    # NOT A PANEL. Inherit from this class

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FBX Exporter"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        io_props = context.scene.io_ue5_fbx
        return [layout, io_props]


class VIEW3D_PT_FBXExporter(Base_Panel, bpy.types.Panel):
      
    bl_idname = "VIEW3D_PT_FBXExporter"
    bl_label = "Export FBX to Unreal Engine 5"  
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj is not None and obj.type == 'MESH')
    
    def draw(self, context):
        pass


class VIEW3D_PT_Filepath(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Filepath"
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):

        [layout, io_props] = super(VIEW3D_PT_Filepath, self).draw(context)
        
        # filter filepath properties, reverse order
        ann = io_props.__annotations__.keys()
        fp_keys = [k for k in ann if k.startswith('fp')]
    
        # UI Layout
        for key in fp_keys:
            if key == 'fp_project_dir' or key == 'fp_project_subdir':
                
                # label
                label = io_props.bl_rna.properties.get(key).name
                row = layout.row()
                row.label(text=label)
                
                # edit field
                split = layout.split(factor=0.8)
                [lcol, rcol] = split.column(), split.column(align=True)

                # get placeholder text (cannot set in StringProperty())
                match key:
                    case 'fp_project_dir':
                        ph = 'C:\\Unreal Projects\\'
                        lcol.prop(io_props, key, text='', placeholder=ph)
                        rcol.operator(operators.OT_Filebrowser_Dir.bl_idname)
                    case 'fp_project_subdir':
                        ph = 'Content\\'
                        lcol.prop(io_props, key, text='', placeholder=ph)
                        rcol.operator(operators.OT_Filebrowser_Subdir.bl_idname)
                    case _:
                        pass

            elif key == 'fp_file_name':

                '''
                # label and edit field on same row
                layout.row().separator()
                split = layout.split(factor=0.6)
                [lcol, rcol] = split.column(), split.column(align=True)
                lsplit = lcol.split(factor=0.4)
                [llcol, lrcol] = lsplit.column(), lsplit.column()

                label = io_props.bl_rna.properties.get(key).name
                llcol.label(text=label)
                lrcol.prop(io_props, key, text='')
                rcol.operator(operators.OT_Filename.bl_idname)
                '''
                row = layout.row()
                row.prop(io_props, key)


class VIEW3D_PT_Blender(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Blender"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        [layout, io_props] = super(VIEW3D_PT_Blender, self).draw(context)  

        # filter blender properties, reverse order
        ann = io_props.__annotations__.keys()
        br_keys = [k for k in ann if k.startswith('br')]

        # UI Layout
        for key in br_keys:
            row = layout.row()
            row.prop(io_props, key)
            if (key == 'br_scale' and \
                io_props.br_units == AddonUnits.FBX.name.lower()):
                row.enabled = False


class VIEW3D_PT_Button(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Export"
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        
        [layout, _] = super(VIEW3D_PT_Button, self).draw(context)

        # UI Button
        row1 = layout.row()
        row1.operator(operators.OT_Reset.bl_idname)
        row2 = layout.row()
        row2.operator(operators.OT_Export.bl_idname)

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
