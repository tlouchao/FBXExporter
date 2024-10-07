'''
RUN THIS SCRIPT FROM BLENDER. 
Helper script to make a zipfile, then install and enable the Blender add-on.
'''
import bpy
import os
import shutil

# Change directory
bdir = bpy.path.abspath('//')
module_name = 'io_ue5_fbx'
os.chdir(bdir)

# Make the zipfile
zf = None
zf = shutil.make_archive(module_name, 'zip', bdir, module_name)
print(zf)

# Install Blender add-on
if (zf):
    
    filepath = os.path.join(bdir, module_name + '.zip')
    
    bpy.ops.preferences.addon_install(filepath=filepath)
    bpy.ops.preferences.addon_enable(module=module_name)