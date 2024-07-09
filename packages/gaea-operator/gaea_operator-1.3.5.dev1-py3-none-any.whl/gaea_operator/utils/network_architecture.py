#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/7/8
# @Author  : yanxiaodong
# @File    : network_architecture.py
"""
from .model_template import ModelTemplate

NETWORK_ARCHITECTURE = {
    ModelTemplate.PPYOLOE_PLUS_NAME: {
        "检测模型-极速版": "ppyoloe_s",
        "检测模型-标准版": "ppyoloe_m",
        "检测模型-专业版": "ppyoloe_l",
        "检测模型-高精版": "ppyoloe_x",
    },
    ModelTemplate.CHANGE_PPYOLOE_PLUS_NAME: {
        "变化检测-极速版": "change-ppyoloe_s",
        "变化检测-标准版": "change-ppyoloe_m",
        "变化检测-专业版": "change-ppyoloe_l",
        "变化检测-高精版": "change-ppyoloe_x",
    },
    ModelTemplate.RESNET_NAME: {"图像分类-标准版": "resnet"},
    ModelTemplate.OCRNET_NAME: {"语义分割-标准版": "ocrnet"},
    ModelTemplate.CHANGE_OCRNET_NAME: {"变化分割-标准版": "change-ocrnet"},
    ModelTemplate.CODETR_NAME: {"目标检测大模型": "codetr"}
}
