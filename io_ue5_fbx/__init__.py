import bpy
from . import operators, properties, depsgraph
from .constants import BlenderTypes, BlenderUnits, AddonUnits
from .ui import panel

bl_info = {
    "name": "Export FBX from Blender to Unreal Engine 5 (.fbx)",
    "author": "tlouchao",
    "version": (0, 0, 3),
    "blender": (4, 1, 0),
    "location": "3D Viewport > Sidebar > FBX Exporter",
    "description": "Exports the selected mesh, armature, and animation to Unreal Engine 5",
    "category": "Import-Export",
}

# for registration
modules = [
    properties,
    operators,
    panel,
]

def post_register():
    '''
    Initialize add-on values that require the scene context
    Cannot modify context in UIPanel.draw(), so modify in post_register()
    '''
    io_props = bpy.context.scene.io_ue5_fbx

    # initialize selected object types
    depsgraph.update_selected_objects()

    # initialize scale
    units = bpy.context.scene.unit_settings.system

    if (units == BlenderUnits.NONE.value):
        io_props.br_units = AddonUnits.FBX.name
        io_props.br_scale = 1
    elif (units == BlenderUnits.METRIC.value):
        io_props.br_units = AddonUnits.LOCAL.name
        io_props.br_scale = 0.01

    # add event listeners
    depsgraph.register()

    print('Post Register')


def register():
    """
    Registers the addon classes when the addon is enabled.
    """
    try:
        # register
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

        depsgraph.unregister()
        
        # unregister
        for module in reversed(modules):
            module.unregister()

    except RuntimeError as error:
        print(error)