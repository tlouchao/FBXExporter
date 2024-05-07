import bpy
import os
from .. import operators, properties
from ..constants import BlenderTypes, BlenderUnits, AddonUnits


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
        '''
        Decide whether or not to show the tool based on context
        '''
        obj = context.active_object
        return (obj is not None and \
               (obj.type == BlenderTypes.MESH or \
                obj.type == BlenderTypes.ARMATURE))
    

    def draw(self, context):
        '''
        Draw the parent panel to be filled with subpanels
        '''
        pass


class VIEW3D_PT_Filepath(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Filepath"
    bl_options = {'HEADER_LAYOUT_EXPAND'}


    def draw(self, context):
        '''
        Draw the filepath subpanel
        '''
        [layout, io_props] = super(VIEW3D_PT_Filepath, self).draw(context)
        
        # filter filepath properties
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
                row = layout.row()
                row.prop(io_props, key)


class VIEW3D_PT_Objects(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Object Types"
    bl_options = {'HEADER_LAYOUT_EXPAND'}


    def draw(self, context):
        '''
        Draw the Objects subpanel
        '''
        [layout, io_props] = super(VIEW3D_PT_Objects, self).draw(context)

        # filter blender properties
        ann = io_props.__annotations__.keys()
        ob_keys = [k for k in ann if k.startswith('ob')]
        
        # UI Layout
        row = layout.row(align=True) # props on the same row
        for key in ob_keys:
            row.prop(io_props, key, toggle=1)



class VIEW3D_PT_Modify(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Modify"
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):
        '''
        Draw the Modify subpanel
        '''
        [layout, io_props] = super(VIEW3D_PT_Modify, self).draw(context)  

        # filter blender properties
        ann = io_props.__annotations__.keys()
        br_keys = [k for k in ann if k.startswith('br')]

        # UI Layout
        for key in br_keys:
            row = layout.row()
            row.prop(io_props, key)


class VIEW3D_PT_Export(Base_Panel, bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_FBXExporter"
    bl_label = "Export"
    bl_options = {'HIDE_HEADER'}


    def draw(self, context):
        '''
        Draw the Reset button and Export FBX Button
        '''
        [layout, _] = super(VIEW3D_PT_Export, self).draw(context)

        # UI Button
        row1 = layout.row()
        row1.operator(operators.OT_Reset.bl_idname)
        row2 = layout.row()
        row2.operator(operators.OT_Export.bl_idname)


ui_classes = [
    VIEW3D_PT_FBXExporter,
    VIEW3D_PT_Filepath,
    VIEW3D_PT_Objects,
    VIEW3D_PT_Modify,
    VIEW3D_PT_Export,
]


def register():
    """
    Registers the ui classes when the addon is enabled.
    """
    for ui_class in ui_classes:
        bpy.utils.register_class(ui_class)


def unregister():
    """
    Unregisters the ui classes when the addon is disabled.
    """
    for ui_class in reversed(ui_classes):
        bpy.utils.unregister_class(ui_class)
