import bpy
import os
from enum import Enum

from bpy.props import \
(
    StringProperty, 
    BoolProperty, 
    IntProperty, 
    FloatProperty, 
    EnumProperty, 
    PointerProperty,
)

from .constants import \
(
    BlenderTypes,
    UnrealTypes,
    BlenderUnits,
    AddonUnits,
    AddonSmoothing, 
)


class PG_Properties(bpy.types.PropertyGroup):

    fp_project_dir: StringProperty(
        name="Project Directory",
        description="Unreal Engine 5 project directory",
    )

    fp_project_subdir: StringProperty( 
        name="Subdirectory (Optional)",
        description="Subdirectory (optional) relative to the project directory",
    )

    fp_file_name: StringProperty(
        name="File Name",
        description="FBX File Name",
    )

    br_scale: FloatProperty(
        name="Scale",
        description="Scale Factor",
        precision=2,
        default=1,
    )

    br_units: EnumProperty(
        name="Apply Scalings",
        description="Scene Units",
        items=[
            ('local', AddonUnits.LOCAL.value, '', '', 0),
            ('fbx', AddonUnits.FBX.value, '', '', 1)
        ],
        default="local",
    )

    br_smoothing: EnumProperty(
        name="Smoothing",
        description="Geometry Smoothing",
        items=[
            ('face', AddonSmoothing.FACE.value, '', '', 0),
            ('edge', AddonSmoothing.EDGE.value, '', '', 1),
            ('normals', AddonSmoothing.NORMALS.value, '', '', 2),
        ],
        default="face",
    )

    # TODO: Handle armatures
    br_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Uncheck add leaf bones",
        default=False,
    )


def register():
    """
    Registers the property group class and adds it to the context
    """
    p = bpy.types.PropertyGroup.bl_rna_get_subclass_py('PG_Properties')
    if (p is None):
        bpy.utils.register_class(PG_Properties)

    # actual property is stored at bpy.context.scene.io_ue5_fbx
    if not hasattr(bpy.types.Scene, 'io_ue5_fbx'):
        bpy.types.Scene.io_ue5_fbx = PointerProperty(type=PG_Properties)


def unregister():
    """
    Unregisters the property group class and deletes it from the context
    """
    p = bpy.types.PropertyGroup.bl_rna_get_subclass_py('PG_Properties')
    if (p is not None):
        bpy.utils.unregister_class(PG_Properties)

    # actual property is stored at bpy.context.scene.io_ue5_fbx
    if hasattr(bpy.types.Scene, 'io_ue5_fbx'):
        del bpy.types.Scene.io_ue5_fbx
