import bpy
import os

from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

from . import subscribe
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
    
    def execute(self, context):
        context.scene.io_ue5_fbx.fp_project_dir = self.directory
        return {'FINISHED'}


class OT_Filebrowser_Subdir(Base_Filebrowser, Operator):

    bl_idname = "op.filebrowser_subdir"
    bl_label = "Set"
    
    def execute(self, context):
        context.scene.io_ue5_fbx.fp_project_subdir = self.directory
        return {'FINISHED'}


class OT_Reset(Operator):

    bl_idname = "op.reset"
    bl_label = "Reset to Recommended Defaults"

    def execute(self, context):

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

    def execute(self, context):
        
        io_props = context.scene.io_ue5_fbx

        dir_name = io_props.fp_project_dir
        subdir_name = io_props.fp_project_subdir
        stem = io_props.fp_file_name

        if (dir_name == '' or dir is None):
            dir_name = 'C:/'

        filepath = os.path.join(dir_name, subdir_name, stem + '.fbx')
        bpy.ops.export_scene.fbx(filepath=filepath)
        
        self.report({'INFO'}, f"Exported {stem}.fbx to {dir_name}{subdir_name}")
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
