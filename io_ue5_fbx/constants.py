from enum import Enum


class ToolInfo(Enum):
    NAME = 'io_ue5_fbx'


class BlenderTypes:
    SKELETON = 'ARMATURE'
    MESH = 'MESH'
    ANIMATION = 'ANIMATION'


class UnrealTypes:
    SKELETAL_MESH = 'SkeletalMesh'
    STATIC_MESH = 'StaticMesh'
    ANIM_SEQUENCE = 'AnimSequence'


class BlenderUnits(Enum):
    NONE = 'NONE'
    METRIC = 'METRIC'
    IMPERIAL = 'IMPERIAL'


class AddonUnits(Enum):
    LOCAL = 'All Local (Metric, Recommended)'
    FBX = 'FBX Units Scale'


class AddonSmoothing(Enum):
    FACE = 'Face (Recommended)'
    EDGE = 'Edge'
    NORMALS = "Normals Only"