'''
RUN THIS SCRIPT FROM BLENDER. 
Helper script to make a zipfile, then install and enable the Blender add-on.
'''
import bpy
import os
import shutil

# Make the zipfile
current_dir = bpy.path.abspath('//')
up_dir = current_dir + '..'
module_name = 'io_ue5_fbx'

zf = None

if os.path.exists(os.path.join(up_dir, module_name)):
    zf = shutil.make_archive(module_name, 'zip', up_dir, module_name)

# Install Blender add-on
if (zf):

    filepath = os.path.join(up_dir, module_name + '.zip')
    
    bpy.ops.preferences.addon_install(filepath=filepath)
    bpy.ops.preferences.addon_enable(module=module_name)