import bpy
from .constants import BlenderTypes


def handle_active_object(*args):
    '''
    Active object event listener callback
    Update the UI with active object
    '''
    io_props = bpy.context.scene.io_ue5_fbx
    obj = bpy.context.active_object

    # if the active object is the mesh
    if (obj.type == BlenderTypes.MESH):
        
        io_props.ob_mesh = True
        
        # check for multiple selection
        io_props.ob_armature = False
        for sel_obj in bpy.context.selected_objects:
            if sel_obj.type == BlenderTypes.ARMATURE:
                io_props.ob_armature = True

    # if the active object is an armature
    elif (obj.type == BlenderTypes.ARMATURE):

        io_props.ob_armature = True

        # check for multiple selection
        io_props.ob_mesh = False
        for sel_obj in bpy.context.selected_objects:
            if sel_obj.type == BlenderTypes.MESH:
                io_props.ob_mesh = True

    print(f"Object type changed to {obj.type}")


def subscribe(owner):
    '''
    Add set active object event listener
    '''
    subscribe_to = (bpy.types.LayerObjects, 'active')
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=owner,
        args=(owner,),
        notify=handle_active_object,
    )

def unsubscribe(owner):
    '''
    Remove set active object event listener
    '''
    try:
        bpy.msgbus.clear_by_owner(owner)
    except RuntimeError as error:
        print(error)
