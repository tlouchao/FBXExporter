'''
RUN THIS SCRIPT FROM BLENDER
'''
import os
import shutil

# Make the zipfile
module_name = 'io_ue5_fbx'
ext = '.zip'
zf = None
if os.path.exists(module_name):
    zf = shutil.make_archive(module_name, 'zip', '.', module_name)

# Install Blender add-on
import bpy
if (zf):

    zpath = module_name + ext
    filepath = os.path.join(bpy.path.abspath('//'), zpath)
    
    bpy.ops.preferences.addon_install(filepath=filepath)
    bpy.ops.preferences.addon_enable(module=module_name)