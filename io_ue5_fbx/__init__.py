import bpy
from . import constants, operators, properties
from .constants import BlenderUnits, AddonUnits
from .ui import panel

bl_info = {
    "name": "Export FBX from Blender to Unreal Engine 5 (.fbx)",
    "author": "tlouchao",
    "version": (0, 0, 1),
    "blender": (4, 1, 0),
    "location": "3D Viewport > Sidebar > FBX Exporter",
    "description": "Exports the selected mesh, armature, and animation to Unreal Engine 5",
    "category": "Import-Export",
}

modules = [
    properties,
    operators,
    panel,
]


def post_register():

    units = bpy.context.scene.unit_settings.system
    io_props = bpy.context.scene.io_ue5_fbx

    if (units == BlenderUnits.NONE.value):
        io_props.br_units = AddonUnits.FBX.name.lower()
        io_props.br_scale = 1
    elif (units == BlenderUnits.METRIC.value):
        io_props.br_units = AddonUnits.LOCAL.name.lower()
        io_props.br_scale = 0.01
    print('Post Register')


def register():
    """
    Registers the addon classes when the addon is enabled.
    """
    try:
        for module in modules:
            module.register()

        # wait for Blender to ready the scene
        bpy.app.timers.register(post_register, first_interval=0.1)
        
        
    except RuntimeError as error:
        print(error)


def unregister():
    """
    Unregisters the addon classes when the addon is disabled.
    """
    try:
        for module in reversed(modules):
            module.unregister()

    except RuntimeError as error:
        print(error)