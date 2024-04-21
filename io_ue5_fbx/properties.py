from enum import Enum
from .constants import \
(
    PanelTypes,
    BlenderTypes,
    UnrealTypes,
    Smoothing, 
    Scaling,
)

import bpy
from bpy.props import \
(
    StringProperty, 
    BoolProperty, 
    IntProperty, 
    FloatProperty, 
    EnumProperty, 
    PointerProperty,
)
    

class PG_Properties(bpy.types.PropertyGroup):

    fp_project_dir: StringProperty(
        name="Project Directory",
        description="Unreal Engine 5 Project Directory",
        default="C:\\Users\\tiffa\\Documents\\Unreal Projects\\MyProject",
    )

    fp_project_subdir: StringProperty(
        name="Content Subdirectory (Optional)",
        description="Content Subdirectory (Optional)",
        default="Content",
    )

    fp_file_name: StringProperty(
        name="FBX File Name",
        description="FBX File Name",
        default="square",
    )

    bl_units: EnumProperty(
        name="Units",
        description="Scene Units",
        items=[
            ('local', Scaling.LOCAL.value, '', '', 0),
            ('fbxunits', Scaling.FBXUNITS.value, '', '', 1)
        ],
        default="local",
    )

    bl_smoothing: EnumProperty(
        name="Smoothing",
        description="Geometry Smoothing",
        items=[
            ('face', Smoothing.FACE.value, '', '', 0),
            ('edge', Smoothing.EDGE.value, '', '', 1),
            ('normals', Smoothing.NORMALS.value, '', '', 2),
        ],
        default="face",
    )

    bl_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Uncheck add leaf bones",
        default=False,
    )

    @classmethod
    def get_props(cls, prop_type):
        prefix = ""
        match prop_type:
            case PanelTypes.FILEPATH:
                prefix = "fp"
            case PanelTypes.BLENDER:
                prefix = "bl"
        props = cls.__annotations__
        props = {k: props[k] for k in props if k.startswith(prefix)}
        return props


def register():
    """
    Registers the property group class and adds it to the context
    """
    if not bpy.types.PropertyGroup.bl_rna_get_subclass_py('PG_Properties'):
        bpy.utils.register_class(PG_Properties)
        bpy.types.Scene.io_ue5_fbx = PointerProperty(type=PG_Properties)


def unregister():
    """
    Unregisters the property group class and deletes it from the context
    """
    if bpy.types.PropertyGroup.bl_rna_get_subclass_py('PG_Properties'):
        bpy.utils.unregister_class(PG_Properties)
    if hasattr(bpy.types.Scene, 'io_ue5_fbx'):
        del bpy.types.Scene.io_ue5_fbx
