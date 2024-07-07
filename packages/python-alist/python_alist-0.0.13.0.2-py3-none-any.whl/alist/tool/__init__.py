#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__all__ = ["alist_update_115_cookie"]

from collections.abc import Iterable
from json import dumps, loads

from alist import AlistClient
from httpx import TimeoutException


def alist_update_115_cookies(
    client: AlistClient, 
    cookie: str, 
    only_not_work: bool = False, 
):
    """更新 alist 中有关 115 的存储的 cookies
    """
    storages = client.admin_storage_list()["data"]["content"]
    for storage in storages:
        if storage["driver"] in ("115 Cloud", "115 Share"):
            if only_not_work and storage["status"] == "work":
                continue
            addition = loads(storage["addition"])
            addition["cookie"] = cookie
            storage["addition"] = dumps(addition)
            client.admin_storage_update(storage)


def alist_batch_add_115_share_links(
    alist_client: AlistClient, 
    share_links: str | Iterable[str], 
    cookies: str, 
    mount_root: str = "/", 
):
    """批量添加 115 分享到 alist

    :param alist_client: alist 客户端对象，例如 AlistClient(origin="http://localhost:5244", username="admin", password="123456")
    :param share_links: 一堆分享链接
    :param cookies: 115 的 cookies，格式为 'UID=...; CID=...; SEID=...'
    :param mount_root: 挂载到的根路径，默认为 "/"
    """
    try:
        from p115 import P115ShareFileSystem
        from retrytools import retry
    except ImportError:
        from sys import executable
        from subprocess import run
        run([executable, "-m", "pip", "install", "-U", "python-115", "python-retrytools"], check=True)
        from p115 import P115ShareFileSystem
        from retrytools import retry
    if isinstance(share_links, str):
        share_links = (share_links,)
    mount_root = mount_root.strip("/")
    if mount_root:
        mount_root = "/" + mount_root
    for link in share_links:
        fs = P115ShareFileSystem("", link)
        get_files = retry(fs.fs_files, retry_times=5, suppress_exceptions=TimeoutError)
        try:
            files: dict = get_files({"limit": 1}) # type: ignore
        except Exception as e:
            print(f"获取链接信息失败：{link!r}，错误原因：{type(e).__qualname__}: {e}")
            continue
        sharedata = files["data"]
        shareinfo = sharedata["shareinfo"]
        if shareinfo["forbid_reason"]:
            print(f"跳过失效链接：{shareinfo}")
            continue
        if sharedata["count"] >= 2:
            name = shareinfo["share_title"]
            root_id = ""
        else:
            item = sharedata["list"][0]
            name = item["n"]
            root_id = str(item["cid"])
        payload = {
            "mount_path": f"{mount_root}/{name}", 
            "order": 0, 
            "remark": "", 
            "cache_expiration": 30, 
            "web_proxy": False, 
            "webdav_policy": "302_redirect", 
            "down_proxy_url": "", 
            "extract_folder": "", 
            "enable_sign": False, 
            "driver": "115 Share", 
            "addition": dumps({
                'cookie': cookies,
                'qrcode_token': "", 
                'qrcode_source': "web", 
                'page_size': 20, 
                'limit_rate': None, 
                'share_code': fs.share_code, 
                'receive_code': fs.receive_code, 
                'root_folder_id': root_id, 
            })
        }
        print("-" * 40)
        print(alist_client.admin_storage_create(payload))
        print(payload)

