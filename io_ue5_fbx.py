import bpy
import os

from bpy.props import \
(
    StringProperty, 
    BoolProperty,
    FloatProperty,
    EnumProperty,
    PointerProperty,
)

bl_info = {
    "name": "Export FBX from Blender to Unreal Engine 5 (.fbx)",
    "author": "tlouchao",
    "version": (0, 0, 1),
    "blender": (4, 1, 0),
    "location": "3D Viewport > Sidebar > FBX Exporter",
    "description": "Exports the selected mesh, armature, and animation to Unreal Engine 5",
    "category": "Import-Export",
}


def update_project_dir(self, context):
    if (not os.path.isdir(self.project_dir)):
        print(f"Invalid filepath: {self.project_dir}")
    else:
        print(f"Selected filepath: {self.project_dir}")
    
class ExportPropertyGroup(bpy.types.PropertyGroup):
    project_dir: StringProperty(
        name="Project Directory",
        description="Unreal Engine 5 project directory",
        update=update_project_dir
    )
    project_subdir: StringProperty(
        name="Project SubDirectory",
        description="Unreal Engine 5 project subdirectory",
    )
    filename: StringProperty(
        name="Filename",
        description="FBX Filename",
    )
    scale: FloatProperty(
        name="Scale",
        description="Scale Factor",
        precision=2,
        default=0.01,
        soft_min=0,
        soft_max=10,
    )
    mesh: BoolProperty(
        name="Mesh",
        description="Export the selected mesh",
        default=False,
    )
    armature: BoolProperty(
        name="Armature",
        description="Export the selected armature",
        default=False,
    )
    smoothing: EnumProperty(
        name="Smoothing",
        description="Export smoothing information",
        default='FACE',
        items=[
            ('FACE', 'Face (Recommended)', 'Write face smoothing'),
            ('EDGE', 'Edge', 'Write edge smoothing'),
            ('OFF', 'Normals Only', 'Export only normals instead of writing edge or face smoothing data'),
        ],
    )

class ExportOperator(bpy.types.Operator):
    
    '''Export the FBX'''
    bl_idname = "export_scene.custom_fbx"
    bl_label = "Run"

    def execute(self, context):
        
        io_ue5_fbx = context.scene.io_ue5_fbx
        
        if (not io_ue5_fbx.project_dir):
            self.report({'WARNING'}, "Filepath not set")
        elif (not os.path.isdir(io_ue5_fbx.project_dir)):
            self.report({'WARNING'}, "Invalid filepath")
        else:
            
            # filepath --------------------- #
            
            project_dir = io_ue5_fbx.project_dir
            project_subdir = io_ue5_fbx.project_subdir
            
            if (io_ue5_fbx.filename):
                stem = io_ue5_fbx.filename
            else:
                bpath = bpy.data.filepath
                [stem, _] = os.path.splitext(bpy.path.basename(bpath))
                
            filepath = os.path.join(project_dir, project_subdir, stem + '.fbx')
            
            # scale ------------------------ #
            
            global_scale = io_ue5_fbx.scale
            
            # scale (these are the defaults) #
            
            apply_unit_scale = True
            apply_scale_options = 'FBX_SCALE_NONE'
            
            # object types ----------------- #
            
            use_selection = True
            object_types = set()
            
            if (io_ue5_fbx.mesh):
                object_types.add('MESH')
            if (io_ue5_fbx.armature):
                object_types.add('ARMATURE')
                
            # smoothing -------------------- #
            
            mesh_smooth_type = io_ue5_fbx.smoothing
            
            # export ----------------------- #
            
            bpy.ops.export_scene.fbx(filepath=filepath,
                                 global_scale=global_scale,
                                 apply_unit_scale=apply_unit_scale,
                                 apply_scale_options=apply_scale_options,
                                 use_selection=use_selection,
                                 object_types=object_types,
                                 mesh_smooth_type=mesh_smooth_type)
            
            self.report({'INFO'}, f"Export {filepath}")
            
        return {'FINISHED'}



class ProjectPathOperator(bpy.types.Operator):
    
    '''Set the Unreal Engine 5 Project Directory'''
    bl_idname = 'export_scene.project_dir'
    bl_label = "Add"
    
    # show directories only
    directory: StringProperty()
    filter_folder: BoolProperty(default=True)
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        context.scene.io_ue5_fbx.project_dir = self.directory
        return {'FINISHED'}


class ProjectSubPathOperator(bpy.types.Operator):
    
    '''Set the Unreal Engine 5 Project SubDirectory'''
    bl_idname = 'export_scene.project_subdir'
    bl_label = "Add"
    
    # show directories only
    directory: StringProperty()
    filter_folder: BoolProperty(default=True)
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        
        io_ue5_fbx = context.scene.io_ue5_fbx
        commonpath = os.path.commonpath(
            [io_ue5_fbx.project_dir, self.directory]) + os.sep

        # display relative directory
        rel_project_subdir = self.directory.replace(commonpath, '')
        io_ue5_fbx.project_subdir = rel_project_subdir
        return {'FINISHED'}


class ResetOperator(bpy.types.Operator):

    '''Populate the above with recommended defaults'''
    bl_idname = "export_scene.custom_reset"
    bl_label = "Reset to Recommended Defaults"
    
    def execute(self, context):
        
        io_ue5_fbx = context.scene.io_ue5_fbx
        
        io_ue5_fbx.filename = ''
        io_ue5_fbx.mesh = False
        io_ue5_fbx.armature = False
        io_ue5_fbx.scale = 0.01
        io_ue5_fbx.smoothing = 'FACE'
        return {'FINISHED'}

          
class VIEW3D_PT_MainPanel(bpy.types.Panel):
    
    bl_idname = "VIEW3D_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = " Export FBX"
    bl_label = "Export FBX From Blender to Unreal Engine 5"
    
    @classmethod
    def poll(cls, context):
        '''
        Decide whether or not to show the tool based on context
        '''
        obj_types = ['MESH', 'ARMATURE']
        
        obj_sel = context.selected_objects
        found = False

        # check selected objects
        for obj in obj_sel:
            if (obj.type in obj_types):
                found = True
                break

        return found
    
    def draw(self, context):
        
        io_ue5_fbx = context.scene.io_ue5_fbx
        # call draw on subpanels


class VIEW3D_PT_SettingsPanel(bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Settings"
    
    def draw(self, context):
        
        io_ue5_fbx = context.scene.io_ue5_fbx
        
        placeholder = os.path.join('C:\\', 'Unreal Projects', 'MyProject', 'Content', '')
        
        self.layout.label(text="Project Directory (Required)")
        split = self.layout.split(factor=0.8)
        [lcol, rcol] = split.column(), split.column(align=True)
        lcol.prop(io_ue5_fbx, 'project_dir', text='', placeholder=placeholder)
        rcol.operator('export_scene.project_dir')
        
        self.layout.label(text="Project Subdirectory")
        split = self.layout.split(factor=0.8)
        [lcol, rcol] = split.column(), split.column(align=True)
        lcol.prop(io_ue5_fbx, 'project_subdir', text='')
        rcol.operator('export_scene.project_subdir')
        
        bpath = bpy.data.filepath
        [stem, ext] = os.path.splitext(bpy.path.basename(bpath))
        placeholder = stem
        
        split = self.layout.split(factor=0.25)
        [lcol, rcol] = split.column(), split.column()
        lcol.label(text='Filename')
        rcol.prop(io_ue5_fbx, 'filename', text='', placeholder=placeholder)
        
        split = self.layout.split(factor=0.25)
        [lcol, rcol] = split.column(), split.row(align=True)
        lcol.label(text='Object Types')
        rcol.prop(io_ue5_fbx, 'mesh', toggle=1)
        rcol.prop(io_ue5_fbx, 'armature', toggle=1)
        
        split = self.layout.split(factor=0.25)
        [lcol, rcol] = split.column(), split.column()
        lcol.label(text='Scale')
        rcol.prop(io_ue5_fbx, 'scale', text='')
        
        split = self.layout.split(factor=0.25)
        [lcol, rcol] = split.column(), split.column()
        lcol.label(text='Smoothing')
        rcol.prop(io_ue5_fbx, 'smoothing', text='')
         
    
class VIEW3D_PT_ExportPanel(bpy.types.Panel):

    bl_parent_id = "VIEW3D_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Export"

    def draw(self, context):
         io_ue5_fbx = context.scene.io_ue5_fbx
         
         row1 = self.layout.row()
         row1.operator('export_scene.custom_reset')
         row2 = self.layout.row()
         row2.operator('export_scene.custom_fbx')
         
         if (not io_ue5_fbx.project_dir):
             row2.enabled = False
         elif (not os.path.isdir(io_ue5_fbx.project_dir)):
             row2.enabled = False
        
def register():
    
    bpy.utils.register_class(ExportPropertyGroup)
    bpy.utils.register_class(ProjectPathOperator)
    bpy.utils.register_class(ProjectSubPathOperator)
    bpy.utils.register_class(ResetOperator)
    bpy.utils.register_class(ExportOperator)
    bpy.utils.register_class(VIEW3D_PT_MainPanel)
    bpy.utils.register_class(VIEW3D_PT_SettingsPanel)
    bpy.utils.register_class(VIEW3D_PT_ExportPanel)
    
    bpy.types.Scene.io_ue5_fbx = bpy.props.PointerProperty(type=ExportPropertyGroup)

def unregister():
    bpy.utils.unregister_class(ExportPropertyGroup)
    bpy.utils.unregister_class(ProjectPathOperator)
    bpy.utils.unregister_class(ProjectSubPathOperator)
    bpy.utils.unregister_class(ResetOperator)
    bpy.utils.unregister_class(ExportOperator)
    bpy.utils.unregister_class(VIEW3D_PT_MainPanel)
    bpy.utils.unregister_class(VIEW3D_PT_SettingsPanel)
    bpy.utils.unregister_class(VIEW3D_PT_ExportPanel)
    
    del bpy.types.Scene.io_ue5_fbx

if __name__ == '__main__':
    register()