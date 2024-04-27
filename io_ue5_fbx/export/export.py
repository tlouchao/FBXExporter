import bpy
import os
from ..constants import AddonUnits, AddonSmoothing

def export_fbx(dir_name,
               subdir_name,
               file_name,
               scale,
               units,
               smoothing,
               add_leaf_bones,
               ):

    # set filepath
    if (dir_name == '' or dir is None):
        dir_name = 'C:/'
    filepath = os.path.join(dir_name, subdir_name, file_name + '.fbx')

    # set scale
    if (units == AddonUnits.FBX.name.lower()):
        scale = None
    global_scale = scale if scale else 1
    
    # set units
    apply_scale_options = 'FBX_SCALE_NONE'
    match units:
        case AddonUnits.LOCAL.name:
            apply_scale_options = 'FBX_SCALE_NONE'
        case AddonUnits.FBX.name:
            apply_scale_options = 'FBX_SCALE_UNITS'

    # set smoothing
    mesh_smooth_type = 'OFF'
    match smoothing:
        case AddonSmoothing.FACE.name:
            mesh_smooth_type = 'FACE'
        case AddonSmoothing.EDGE.name:
            mesh_smooth_type = 'EDGE'
        case AddonSmoothing.NORMALS.name:
            mesh_smooth_type = 'OFF'

    # execute Blender operation
    bpy.ops.export_scene.fbx(filepath=filepath,
                                use_selection=True,
                                global_scale=global_scale,
                                apply_unit_scale=True, 
                                apply_scale_options=apply_scale_options,
                                object_types={"MESH"},
                                use_mesh_modifiers=True,
                                mesh_smooth_type=mesh_smooth_type,
                                add_leaf_bones=add_leaf_bones)