'''
RUN THIS SCRIPT FROM BLENDER
'''
import bpy
import os
import shutil

# Make the zipfile
current_dir = bpy.path.abspath('//')
module_name = 'io_ue5_fbx'

zf = None

if os.path.exists(os.path.join(current_dir, module_name)):
    zf = shutil.make_archive(module_name, 'zip', current_dir, module_name)

# Install Blender add-on
if (zf):

    filepath = os.path.join(current_dir, module_name + '.zip')
    
    bpy.ops.preferences.addon_install(filepath=filepath)
    bpy.ops.preferences.addon_enable(module=module_name)