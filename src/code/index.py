# -*- coding: utf-8 -*-

import json
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import base64
import requests  # 新增：用于下载图片
import uuid
import oss2
import os
import logging

# OSS 配置
OSS_SECURITY_TOKEN = os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")
OSS_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
OSS_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
OSS_BUCKET = os.getenv("OSS_BUCKET")

def upload_to_oss(img_blob, img_type):

    # 创建 Bucket 实例
    auth = oss2.StsAuth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_SECURITY_TOKEN)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

    # 生成唯一的文件名
    file_name = f"{uuid.uuid4()}.{img_type}"
    print("filename: " + file_name)
    
    # 上传文件
    try:
        result = bucket.put_object(file_name, img_blob)
        logging.info(f"File uploaded successfully, status code: {result.status}")
    except oss2.exceptions.OssError as e:
        logging.error(f"Failed to upload file: {e}")

    # 生成公开访问的 URL
    return f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{file_name}"


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download image from {url}")
    
def make_error_response(ex):
    return {
        "statusCode": 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": str(ex)})
    }

def make_response(context, query, img_blob, img_type):
    
    print("image blob length:", len(img_blob))
    
    # 上传到 OSS 并获取 URL
    oss_url = upload_to_oss(img_blob, img_type)
    
    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "imageUrl": oss_url,
            "imageType": img_type
        })
    }
    return response

def pinjie(query, context):
    try:
        image1_url = query.get("left")
        image2_url = query.get("right")
        assert image1_url and image2_url
        fmt = query.get("fmt", "jpg")
        print("pinjie images: ", image1_url, image2_url)
        with Image(blob=download_image(image1_url)) as f1:
            with Image(blob=download_image(image2_url)) as f2:
                with Image(
                    width=f1.width + f2.width + 10, height=max(f1.height, f2.height)
                ) as img:
                    img.format = fmt
                    img.composite(f1, left=0, top=0)
                    img.composite(f2, left=f1.width + 10, top=0)
                    return make_response(context, query, img.make_blob(), fmt)
    except Exception as ex:
        return make_error_response(ex)

def watermark(query, context):
    try:
        image_url = query.get("img")
        text = query.get("text")
        assert image_url and text
        fmt = query.get("fmt", "jpg")
        print("watermark image: {}, text: {}".format(image_url, text))
        with Drawing() as draw:
            draw.font = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
            draw.fill_color = Color("red")
            draw.font_size = 24
            with Image(width=200, height=50, background=Color("transparent")) as pic:
                draw.text(10, int(pic.height / 2), text)
                draw(pic)
                pic.alpha = True
                pic.format = "png"
                pic.save(filename="/tmp/water.png")

        with Image(blob=download_image(image_url)) as img:
            with Image(filename="/tmp/water.png") as water:
                with img.clone() as base:
                    base.format = fmt
                    base.watermark(water, 0.3, 0, int(img.height - 30))
                    return make_response(context, query, base.make_blob(), fmt)
    except Exception as ex:
        return make_error_response(ex)

def format(query, context):
    try:
        image_url = query.get("img")
        fmt = query.get("fmt")
        assert image_url and fmt
        print("format image: {}, fmt: {}".format(image_url, fmt))
        with Image(blob=download_image(image_url)) as img:
            img.format = fmt
            return make_response(context, query, img.make_blob(), fmt)
    except Exception as ex:
        return make_error_response(ex)

def gray(query, context):
    try:
        img_url = query.get("img")
        img_type = img_url.split(".")[-1].lower()
        if img_type not in ["jpg", "jpeg", "webp", "png"]:
            img_type = "jpeg"

        with Image(blob=download_image(img_url)) as img:
            img.format = img_type
            img.transform_colorspace("gray")
            return make_response(context, query, img.make_blob(), img_type)
    except Exception as ex:
        return make_error_response(ex)
            
def handler(event, context):
    evt = json.loads(event)
    print(evt)
    print(context)
    path = evt["requestContext"]["http"]["path"]
    method = evt["requestContext"]["http"]["method"]
    query = evt.get("queryParameters", {})
    
    if method != "GET":
        return make_error_response("Only GET method is supported")

    try:
        if path == "/gray":
            return gray(query, context)
        elif path == "/format":
            return format(query, context)
        elif path == "/watermark":
            return watermark(query, context)
        elif path == "/pinjie":
            return pinjie(query, context)
        else:
            return make_error_response("Invalid path")
    except Exception as ex:
        return make_error_response(ex)