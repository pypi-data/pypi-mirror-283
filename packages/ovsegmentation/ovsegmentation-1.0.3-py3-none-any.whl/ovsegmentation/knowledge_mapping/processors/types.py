from enum import Enum


class SAM_TYPE(Enum):
    EfficientVit = "efficientvit"
    TinySAM = "tinysam"
    MobileSAM = "mobilesam"


class VLM_TYPE(Enum):
    CLIP = "clip"
    MobileVLM = "mobilevlm"
    TinyGPTV = "tinygptv"


class DETECTOR_TYPE(Enum):
    GrouningDINO = "grounding_dino"
    YOLOWorld = "yoloworld"
