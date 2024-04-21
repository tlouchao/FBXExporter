import bpy
from . import constants, operators, properties
from .ui import panel

bl_info = {
    "name": "Export FBX from Blender to Unreal Engine 5 (.fbx)",
    "author": "tlouchao",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar > FBX Exporter",
    "description": "Exports the selected mesh, armature, and animation to Unreal Engine 5",
    "category": "Import-Export",
}

modules = [
    properties,
    operators,
    panel,
]

def register():
    """
    Registers the addon classes when the addon is enabled.
    """
    try:
        for module in modules:
            module.register()
        
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