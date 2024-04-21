from enum import Enum
from .constants import \
(
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

    units: EnumProperty(
        name="Units",
        description="Scene Units",
        items=[
            ('local', Scaling.LOCAL.value, '', '', 0),
            ('fbxunits', Scaling.FBXUNITS.value, '', '', 1)
        ],
        default="local",
    )

    smoothing: EnumProperty(
        name="Smoothing",
        description="Geometry Smoothing",
        items=[
            ('face', Smoothing.FACE.value, '', '', 0),
            ('edge', Smoothing.EDGE.value, '', '', 1),
            ('normals', Smoothing.NORMALS.value, '', '', 2),
        ],
        default="face",
    )

    leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Uncheck add leaf bones",
        default=False,
    )


def register():
    """
    Registers the property group class and adds it to the context
    """
    bpy.utils.register_class(PG_Properties)
    bpy.types.Scene.io_ue5_fbx = PointerProperty(type=PG_Properties)


def unregister():
    """
    Unregisters the property group class and deletes it from the context
    """
    bpy.utils.unregister_class(PG_Properties)
    if hasattr(bpy.types.Scene, 'io_ue5_fbx'):
        del bpy.types.Scene.io_ue5_fbx
