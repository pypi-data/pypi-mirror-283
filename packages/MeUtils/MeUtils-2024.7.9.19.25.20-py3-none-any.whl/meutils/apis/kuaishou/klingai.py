#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : klingai
# @Time         : 2024/7/9 13:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import jsonpath

from meutils.pipe import *
from meutils.schemas.kuaishou_types import BASE_URL, KlingaiImageRequest
from meutils.notice.feishu import send_message
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.decorators.retry import retrying

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=v8vcZY"


# $..task..[id,arguments]
async def submit_task(request: KlingaiImageRequest, cookie: str):
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.post("/api/task/submit", json=request.payload)
        if response.is_success:
            tasks = jsonpath.jsonpath(response.json(), '$..task')  # $..task..[id,arguments]
            send_message(bjson(tasks[0]))

            task_id = tasks[0].get('id')

            return task_id

        logger.exception(response.text)


async def get_task(task_id, cookie: str):
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json;charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        response = await client.get("/api/task/status", params={"taskId": task_id})
        if response.is_success:
            return response.json()
            # if "failed," in str(data): return True  # 触发重试
            #
            # logger.debug(data)
            # urls = jsonpath.jsonpath(data, '$..resource.resource')
            #
            # return [dict(zip(["url"] * len(urls), urls))]

        logger.exception(response.text)


@retrying(max_retries=5, predicate=lambda x: x is True)
async def create_image(request: KlingaiImageRequest):
    cookie = await get_next_token_for_polling(FEISHU_URL)
    task_id = await submit_task(request, cookie)

    while n := 5:
        await asyncio.sleep(max(1, n := n - 1))
        data = await get_task(task_id, cookie)

        logger.debug(data)

        if "failed," in str(data): return True  # 触发重试

        urls = jsonpath.jsonpath(data, '$..resource.resource')
        if all(urls):
            images = [{"url": url} for url in urls]
            return images


if __name__ == '__main__':
    # https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=v8vcZY
    rquest = KlingaiImageRequest(imageCount=1)  # 27638649

    # cookie = "weblogger_did=web_47164250171DB527; did=web_e022fde52721456f43cb66d90a7d6f14e462; userId=742626779; kuaishou.ai.portal_st=ChVrdWFpc2hvdS5haS5wb3J0YWwuc3QSoAGAEPOivL4BJ2Y8y48CvR-t25o44Sj_5G9LnZI8BJbV_Inkqd4qxPMJy4OqZCf0VHZnr8EcgMHOzuj_fw5-x0OF3UtrXrU2ZBe6G_bnD1umPIAL6DVtv6ERJ9uLpa7asCBgIUvMXk6K345vc5okzhoTPw69b1GsXY777qwuOwGoUrP9eyJc6Z4TeQPYDEW2wdazss7Dn2osIhObsW9izb1yGhJaTSf_z6v_i70Q1ZuLG30vAZsiIGMXZhr3i8pOgOICzAXA0T6fJZZk3hFRsxn3MDQzIeiKKAUwAQ; kuaishou.ai.portal_ph=fe74c1e2fb91142f838c4b3d435d6153ccf3"

    # pprint(arun(submit_task(rquest, cookie)))
    # pprint(arun(get_task(27708439, cookie)))

    pprint(arun(create_image(rquest)))
