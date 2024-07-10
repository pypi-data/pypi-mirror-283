#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kuaishou_types
# @Time         : 2024/7/9 13:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://klingai.kuaishou.com"

payload = {
    'arguments': [
        {'name': 'prompt', 'value': '清凉夏季美少女，微卷短发，运动服，林间石板路，斑驳光影，超级真实，16K'},
        {'name': 'style', 'value': '默认'},
        {'name': 'aspect_ratio', 'value': '1:1'},
        {'name': 'imageCount', 'value': '4'},
        {'name': 'biz', 'value': 'klingai'}
    ],
    'type': 'mmu_txt2img_aiweb',
    'inputs': []
}


class KlingaiImageRequest(BaseModel):
    prompt: str = '清凉夏季美少女，微卷短发，运动服，林间石板路，斑驳光影，超级真实，16K'
    style: str = "默认"
    aspect_ratio: Literal["1:1", "2:3", "3:2", "3:4", "4:3", "9:16", "16:9"] = "1:1"
    imageCount: int = 4
    biz: str = "klingai"

    payload: dict = {}

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        arguments = [
            {'name': 'prompt', 'value': self.prompt},
            {'name': 'style', 'value': self.style},
            {'name': 'aspect_ratio', 'value': self.aspect_ratio},
            {'name': 'imageCount', 'value': self.imageCount},
            {'name': 'biz', 'value': self.biz}
        ]
        self.payload = {
            'arguments': arguments,
            'type': 'mmu_txt2img_aiweb',
            'inputs': []
        }
