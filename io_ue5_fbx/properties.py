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
    PanelTypes,
    BlenderTypes,
    UnrealTypes,
    Smoothing, 
    Scaling,
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

    br_units: EnumProperty(
        name="Units",
        description="Scene Units",
        items=[
            ('local', Scaling.LOCAL.value, '', '', 0),
            ('fbxunits', Scaling.FBXUNITS.value, '', '', 1)
        ],
        default="local",
    )

    br_smoothing: EnumProperty(
        name="Smoothing",
        description="Geometry Smoothing",
        items=[
            ('face', Smoothing.FACE.value, '', '', 0),
            ('edge', Smoothing.EDGE.value, '', '', 1),
            ('normals', Smoothing.NORMALS.value, '', '', 2),
        ],
        default="face",
    )

    br_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Uncheck add leaf bones",
        default=False,
    )

    @classmethod
    def get_props(cls, prop_type):
        '''
        Helper function to get custom properties
        '''
        prefix = ""
        match prop_type:
            case PanelTypes.FILEPATH:
                prefix = "fp"
            case PanelTypes.BLENDER:
                prefix = "br"
            case _:
                pass
        ann = cls.__annotations__
        props = {k: ann[k] for k in ann if k.startswith(prefix)}
        return props

    @classmethod
    def get_prop_name(cls, prop_name):
        '''
        Helper function to get the name attribute of custom property
        '''
        ann = cls.__annotations__
        prop = ann[prop_name]
        return prop.keywords.get('name') if prop else None

    @classmethod
    def get_placeholder(cls, prop_name):
        '''
        StringProperty() does not have a placeholder attribute.
        This helper function returns a placeholder string
        independent of the given custom property.
        '''
        ann = cls.__annotations__
        prop = ann[prop_name]
        if prop:
           match prop_name:
            case 'fp_project_dir':
                return 'C:/Unreal Projects/'
            case 'fp_project_subdir':
                return 'Content/'
            case _:
                return ''


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
