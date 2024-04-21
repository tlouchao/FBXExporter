from enum import Enum


class ToolInfo(Enum):
    NAME = 'io_ue5_fbx'
    APP = 'blender'
    LABEL = 'Send to Unreal'


class BlenderTypes:
    SKELETON = 'ARMATURE'
    MESH = 'MESH'
    ANIMATION = 'ANIMATION'


class UnrealTypes:
    SKELETAL_MESH = 'SkeletalMesh'
    STATIC_MESH = 'StaticMesh'
    ANIM_SEQUENCE = 'AnimSequence'


class Smoothing(Enum):
    EDGE = 'Edge'
    FACE = 'Face'
    NORMALS = "Normals Only"


class Scaling(Enum):
    LOCAL = "All Local"
    FBXUNITS = "FBX Units Scale"