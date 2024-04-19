# Run this script from Blender

import bpy
import os

current_dir = bpy.path.abspath("//")
basename = "io_ue5_fbx"; ext = ".py"
fname = basename + ext

if os.path.exists(fname):
    bpy.ops.preferences.addon_install(filepath=current_dir + fname)
    bpy.ops.preferences.addon_enable(module=basename)
    