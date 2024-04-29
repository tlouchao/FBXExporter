import bpy
import os

from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from .export import export
from .constants import BlenderUnits, AddonUnits, AddonSmoothing

class Base_Filebrowser:

    # NOT AN OPERATOR. Inherit from this class

    # show directories only
    directory: StringProperty(
        name="Directory",
        description="Get the Unreal Engine 5 project directory",
    )

    filter_folder: BoolProperty(
        default=True,
        options={"HIDDEN"}
    )
    

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class OT_Filebrowser_Dir(Base_Filebrowser, Operator):

    bl_idname = "op.filebrowser_dir"
    bl_label = "Set"
    bl_description = "Set an Unreal Engine 5 project directory"
    

    @classmethod
    def description(cls, context, properties):
        '''
        Show the tooltip
        '''
        return cls.bl_description


    def execute(self, context):
        '''
        Executes when this button is clicked. Opens a file browser.
        '''
        context.scene.io_ue5_fbx.fp_project_dir = self.directory
        return {'FINISHED'}


class OT_Filebrowser_Subdir(Base_Filebrowser, Operator):

    bl_idname = "op.filebrowser_subdir"
    bl_label = "Set"
    bl_description = "Set a subdirectory relative to the parent directory."


    @classmethod
    def description(cls, context, properties):
        '''
        Show the tooltip
        '''
        return cls.bl_description
    

    def execute(self, context):
        '''
        Executes when this button is clicked. Opens a file browser.
        '''
        context.scene.io_ue5_fbx.fp_project_subdir = self.directory
        return {'FINISHED'}


class OT_Reset(Operator):

    bl_idname = "op.reset"
    bl_label = "Reset to Recommended Defaults"
    bl_description = "Populate the above with recommended file name and " + \
        "transform defaults"


    @classmethod
    def description(cls, context, properties):
        '''
        Show the tooltip
        '''
        return cls.bl_description


    def execute(self, context):
        '''
        Executes when this button is clicked. 
        Reset settings to recommended defaults.
        '''
        # get context
        units = context.scene.unit_settings.system
        io_props = context.scene.io_ue5_fbx

        # set filename 
        basename = os.path.basename(context.blend_data.filepath)
        [stem, ext] = os.path.splitext(basename)
        bpy.context.scene.io_ue5_fbx.fp_file_name = stem

        # set units based on Blender scene units
        if (units == BlenderUnits.NONE.value):
            io_props.br_units = AddonUnits.FBX.name.lower()
            io_props.br_scale = 1
        elif (units == BlenderUnits.METRIC.value):
            io_props.br_units = AddonUnits.LOCAL.name.lower()
            io_props.br_scale = 0.01

        # set smoothing modifier to prevent error in Unreal
        io_props.br_smoothing = AddonSmoothing.FACE.name.lower()

        # Armatures only. Prevent extra bones in Unreal skeleton asset
        io_props.br_leaf_bones = False

        self.report({'INFO'}, f"Reset to Recommended Defaults")
        return {'FINISHED'}


class OT_Export(Operator):

    bl_idname = "op.export"
    bl_label = "Export FBX"
    bl_description = "Export the FBX file"


    @classmethod
    def description(cls, context, properties):
        '''
        Show the tooltip
        '''
        return cls.bl_description


    def execute(self, context):
        '''
        Executes when this button is clicked. 
        Exports the FBX file.
        '''
        io_props = context.scene.io_ue5_fbx

        export.export_fbx(dir_name=io_props.fp_project_dir,
                          subdir_name=io_props.fp_project_subdir,
                          file_name=io_props.fp_file_name,
                          scale=io_props.br_scale,
                          units=io_props.br_units,
                          smoothing=io_props.br_smoothing,
                          add_leaf_bones = io_props.br_leaf_bones,
                          )
        
        file_name = io_props.fp_file_name
        dir_name = io_props.fp_project_dir
        subdir_name = io_props.fp_project_subdir

        self.report({'INFO'}, 
            f"Exported {file_name}.fbx to {dir_name}{subdir_name}")
        return {'FINISHED'}


op_classes = [
    OT_Filebrowser_Dir,
    OT_Filebrowser_Subdir,
    OT_Reset,
    OT_Export,
]


def register():
    """
    Registers the operator classes
    """
    for op_class in op_classes:
        bpy.utils.register_class(op_class)


def unregister():
    """
    Unegisters the operator classes
    """
    for op_class in reversed(op_classes):
        bpy.utils.unregister_class(op_class)
