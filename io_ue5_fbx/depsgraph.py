import bpy
import bpy.app.handlers as handlers
from .constants import BlenderTypes


def update_selected_objects(*args):
    '''
    Update the UI with selected objects
    '''
    io_props = bpy.context.scene.io_ue5_fbx
    objs = bpy.context.selected_objects

    mesh_found = False
    armature_found = False

    for obj in objs:
        if (mesh_found and armature_found):
            break
        match obj.type:
            case BlenderTypes.MESH:
                mesh_found = True   
            case BlenderTypes.ARMATURE:
                armature_found = True

    io_props.ob_mesh = mesh_found
    io_props.ob_armature = armature_found


def register():
    '''
    Add set selected object event listener
    '''
    if (update_selected_objects not in handlers.depsgraph_update_post):
        handlers.depsgraph_update_post.append(update_selected_objects)


def unregister():
    '''
    Remove set selected object event listener
    '''
    if (update_selected_objects in handlers.depsgraph_update_post):
        handlers.depsgraph_update_post.remove(update_selected_objects)
