import bpy
import os
import re
from ..constants import BlenderTypes, AddonUnits, AddonSmoothing


def export_fbx(op,
               context,
               dir_name = '',
               subdir_name = '',
               file_name = '',
               selected_mesh = True,
               selected_armature = False,
               scale = 1,
               units = AddonUnits.LOCAL.name,
               smoothing = AddonSmoothing.FACE.name,
               add_leaf_bones = False,
               bake_animation = True,
               ):
    """
    Given the incoming UI properties, export the FBX File

    Keyword arguments:

    op:      Operator. Passed in to get access to the report function
    context: Context dependent on the area of Blender currently being accessed
    
    Optional keyword arguments:

    dir_name:          Destination project directory
    subdir_name:       Destination project subdirectory
    file_name:         File name
    selected_mesh:     Is a mesh selected?
    selected_armature: Is an armature selected?
    scale:             Scale factor
    units:             Scale units ("All Local" is recommended)
    smoothing:         Geometry smoothing ("Face" is recommended)
    add_leaf_bones:    Is the option to add leaf bones unchecked?
    bake_animation:    Is the option to bake animation checked?
    """

    # -------------------------- Filepath ------------------------ #

    default_dir = 'C:\\'

    # 1.) validate directory
    if os.path.isdir(dir_name):
        pass # do nothing, leave the directory name be
    else:
        if not dir_name:
            if op: op.report({'WARNING'}, f"Empty project directory. " + \
                f"Defaulting to {default_dir}")
        else:
            if op: op.report({'WARNING'}, f"{dir_name} does not exist. " + \
                f"Defaulting to {default_dir}")
        dir_name = default_dir

    dir_concat = dir_name.strip('\\') + '\\' + subdir_name.strip('\\') + '\\'
    if op: op.report({'DEBUG'}, f"Concat: {dir_concat}")

    # 2.) validate subdirectory
    if os.path.isdir(dir_concat):
        pass # do nothing, leave the subdirectory name be
    else:
        if (subdir_name == '' or subdir_name is None):
            if op: op.report({'WARNING'}, f"Empty project subdirectory. " + \
                f"Defaulting to {dir_name}")
        else:
            if op: op.report({'WARNING'}, f"{dir_concat} does not exist. " + \
                f"Defaulting to {dir_name}")
        dir_concat = dir_name
    
    # 3.) validate filename. Default is the Blender filename
    basename = os.path.basename(bpy.context.blend_data.filepath)
    [stem, ext] = os.path.splitext(basename)
    is_valid_file_name = True

    if not file_name:
        is_valid_file_name = False
        if op: op.report({'WARNING'}, f"{file_name} is empty." + \
            f"Defaulting to {basename}")
    
    # if not null, accept only alphanumeric names which may include '_', '-'
    elif (re.match(r'[^[A-Za-z0-9_-]', file_name) is not None):
        is_valid_file_name = False
        if op: op.report({'WARNING'}, f"{file_name} contains invalid " + \
            f"characters. Defaulting to {basename}")

    if (not is_valid_file_name):
        file_name = stem

    # 4.) finally, set the filepath
    filepath = os.path.join(dir_concat, file_name + '.fbx')

    # -------------------------- Blender ------------------------ #
    
    # set object type
    object_types = set()
    if (selected_mesh):
        object_types.add(BlenderTypes.MESH)
    if (selected_armature):
        object_types.add(BlenderTypes.ARMATURE)

    # set scale
    global_scale = scale if scale else 1
    
    # set units
    apply_scale_options = 'FBX_SCALE_NONE'
    match units:
        case AddonUnits.LOCAL.name:
            apply_scale_options = 'FBX_SCALE_NONE'
        case AddonUnits.FBX.name:
            apply_scale_options = 'FBX_SCALE_UNITS'

    # set smoothing
    mesh_smooth_type = smoothing

    # auto select active object, if nothing is selected
    if (not context.selected_objects):
        ao = context.active_object
        ao.select_set(True)
        if op: op.report({'WARNING'}, f"Object(s) not selected. " + \
            f"Defaulting to active object \"{ao.name}\"")

    if op: op.report({'DEBUG'}, 
        f"Prepare to export {file_name}.fbx to {dir_concat}")

    # execute Blender operation
    bpy.ops.export_scene.fbx(filepath=filepath,
                            use_selection=True,
                            global_scale=global_scale,
                            apply_unit_scale=True, 
                            apply_scale_options=apply_scale_options,
                            object_types=object_types,
                            mesh_smooth_type=mesh_smooth_type,
                            add_leaf_bones=add_leaf_bones,
                            bake_anim = bake_animation,
                            )

    # TODO: handle backslash and forward slash 
    dir_concat = dir_concat.replace('/', '\\')
    if op: op.report({'INFO'},
            f"Exported {file_name}.fbx to {dir_concat}")
