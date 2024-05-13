import bpy
import os

from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty

from .export import export
from .constants import BlenderTypes, BlenderUnits, AddonUnits, AddonSmoothing

class Base_Filebrowser:

    # NOT AN OPERATOR. Inherit from this class

    # show directories only
    directory: StringProperty(
        name="Directory",
        description="Get the Unreal Engine 5 project directory",
    )

    # show directories only
    filter_folder: BoolProperty(
        default=True,
        options={"HIDDEN"}
    )
    

    def invoke(self, context, event):
        # if project directory is set, then start navigating from this directory
        project_dir = context.scene.io_ue5_fbx.fp_project_dir
        if (project_dir):
            self.directory = project_dir
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
        io_props = context.scene.io_ue5_fbx
        project_dir = io_props.fp_project_dir
        commonpath = os.path.commonpath([project_dir, self.directory])

        # display relative directory
        rel_project_subdir = self.directory.replace(commonpath, '')
        context.scene.io_ue5_fbx.fp_project_subdir = rel_project_subdir
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

        # set object type. Try to select the mesh if it exists
        objs = bpy.context.view_layer.objects
        for obj in objs:
            if obj.type == BlenderTypes.MESH:
                obj.select_set(True)
                break

        # set transform units based on Blender scene units
        if (units == BlenderUnits.NONE.value):
            io_props.tr_units = AddonUnits.FBX.name
            io_props.tr_scale = 1
        elif (units == BlenderUnits.METRIC.value):
            io_props.tr_units = AddonUnits.LOCAL.name
            io_props.tr_scale = 0.01

        # set smoothing modifier to prevent error in Unreal
        io_props.tr_smoothing = AddonSmoothing.FACE.name

        # Armatures only. Prevent extra bones in Unreal skeleton asset
        io_props.ar_leaf_bones = False

        # Armatures only. Bake animation frames
        io_props.ar_bake_animation = True

        self.report({'INFO'}, f"Reset to Recommended Defaults")
        return {'FINISHED'}


class OT_Export(Operator):

    bl_idname = "op.export"
    bl_label = "Export FBX"
    bl_description = "Export selected objects to the FBX file"


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

        export.export_fbx(op=self, # access to report()
                          context=context,
                          dir_name=io_props.fp_project_dir,
                          subdir_name=io_props.fp_project_subdir,
                          file_name=io_props.fp_file_name,
                          selected_mesh = io_props.ob_mesh,
                          selected_armature = io_props.ob_armature,
                          scale=io_props.tr_scale,
                          units=io_props.tr_units,
                          smoothing=io_props.tr_smoothing,
                          add_leaf_bones = io_props.ar_leaf_bones,
                          bake_animation = io_props.ar_bake_animation,
                          )
        
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
