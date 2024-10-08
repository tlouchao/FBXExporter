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
    CollectionProperty,
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

def update_mesh_object_type(self, context):
    '''
    After toggling boolean property, select the first mesh object from scene
    '''
    ob_mesh = context.scene.io_ue5_fbx.ob_mesh
    objs = bpy.context.view_layer.objects

    for obj in objs:
        if obj.type == BlenderTypes.MESH:
            obj.select_set(ob_mesh)
            break


def update_armature_object_type(self, context):
    '''
    After toggling boolean property, select the first armature object from scene
    '''
    ob_armature = context.scene.io_ue5_fbx.ob_armature
    objs = bpy.context.view_layer.objects

    for obj in objs:
        if obj.type == BlenderTypes.ARMATURE:
            obj.select_set(ob_armature)
            break        


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

    ob_mesh: BoolProperty(
        name="Mesh",
        description="Export the selected mesh",
        default=False,
        update=update_mesh_object_type,
    )

    ob_armature: BoolProperty(
        name="Armature",
        description="Export the selected armature",
        default=False,
        update=update_armature_object_type,
    )

    tr_scale: FloatProperty(
        name="Scale",
        description="Scale Factor",
        precision=2,
        default=0.01,
        soft_min=0,
        soft_max=10,
    )

    tr_units: EnumProperty(
        name="Apply Scalings",
        description="Scene Units",
        items=[
            (AddonUnits.LOCAL.name, AddonUnits.LOCAL.value, 'Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0'),
            (AddonUnits.FBX.name, AddonUnits.FBX.value, 'Apply custom scaling to each object transformation, and units scaling to FBX scale'),
        ],
        default=AddonUnits.LOCAL.name,
    )

    tr_smoothing: EnumProperty(
        name="Smoothing",
        description="Geometry Smoothing",
        items=[
            (AddonSmoothing.FACE.name, AddonSmoothing.FACE.value, 'Write face smoothing'),
            (AddonSmoothing.EDGE.name, AddonSmoothing.EDGE.value, 'Write edge smoothing'),
            (AddonSmoothing.OFF.name, AddonSmoothing.OFF.value, 'Export only normals instead of writing edge or face smoothing data'),
        ],
        default=AddonSmoothing.FACE.name,
    )

    ar_leaf_bones: BoolProperty(
        name="Add Leaf Bones",
        description="Uncheck add leaf bones to prevent adding extra bones",
        default=False,
    )

    ar_bake_animation: BoolProperty(
        name="Bake Animation",
        description="Export at least one key of animation for all bones",
        default=True,
    )

def register():
    """
    Registers the property group class and adds it to the context
    """
    p = bpy.types.PropertyGroup.bl_rna_get_subclass_py('PG_Properties')
    if (p is None):
        bpy.utils.register_class(PG_Properties)
    
    # reference to properties at bpy.context.scene.io_ue5_fbx
    if not hasattr(bpy.types.Scene, 'io_ue5_fbx'):
        bpy.types.Scene.io_ue5_fbx = PointerProperty(type=PG_Properties)


def unregister():
    """
    Unregisters the property group class and deletes it from the context
    """
    p = bpy.types.PropertyGroup.bl_rna_get_subclass_py('PG_Properties')
    if (p is not None):
        bpy.utils.unregister_class(PG_Properties)

    # delete reference to properties
    if hasattr(bpy.types.Scene, 'io_ue5_fbx'):
        del bpy.types.Scene.io_ue5_fbx
