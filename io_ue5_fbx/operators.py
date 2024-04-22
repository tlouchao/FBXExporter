import bpy
import os


class OP_OT_Export(bpy.types.Operator):

    bl_idname = "op.export"
    bl_label = "Export FBX"

    def execute(self, context):
        
        dname = "C:/Users/tiffa/Documents/Elvtr/TART07"
        content_folder = "TART07/Content/TART07"
        fname = "leaf"
        filepath = os.path.join(dname, content_folder, fname + ".fbx")
        
        bpy.ops.export_scene.fbx(filepath=filepath)
        
        self.report({'INFO'}, f"Exported {fname}.fbx to {dname}/{content_folder}")
        return {'FINISHED'}

class OP_OT_Filename(bpy.types.Operator):

    bl_idname = "op.filename"
    bl_label = "Auto"

    def execute(self, context):
        basename = os.path.basename(context.blend_data.filepath)
        [stem, ext] = os.path.splitext(basename)
        bpy.context.scene.io_ue5_fbx.fp_file_name = stem + '.fbx'
        return {'FINISHED'}

op_classes = [
    OP_OT_Export,
    OP_OT_Filename,
]


def register():
    """
    Registers the operator classes
    """
    for op_class in op_classes:
        bpy.utils.register_class(op_class)


def unregister():
    """
    Unegisters the operator classes
    """
    for op_class in reversed(op_classes):
        bpy.utils.unregister_class(op_class)
