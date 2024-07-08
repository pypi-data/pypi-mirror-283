# -*- coding:utf-8 -*-
# ProjectName：huojiweiguoba
# FileName：ipdf.py
# Time：2024/7/8 下午12:53
# Author：侯文杰
# IDE：PyCharm
import fitz
import os
from paddleocr import PaddleOCR, draw_ocr

def extract_pics(file_path, save_path):
    '''提取PDF中的所有图片'''
    result = []
    # 1.打开文件
    doc = fitz.open(file_path)
    # 文档页数
    page_count = len(doc)
    print("文档共有{}页".format(page_count))
    # 2.遍历并检查每页的图片
    image_count = 0
    for i in range(page_count):
        # 页面对象
        page = doc[i]
        # 获取图片列表
        images = page.get_images()
        # 遍历图片
        for image in images:
            # 返回图片引用
            xref = image[0]
            # 根据引用从pdf中释放出图片
            base_image = doc.extract_image(xref)
            # 获得图片数据
            image_data = base_image["image"]
            # 保存图片
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            cur_save_path = f'{save_path}/image_{image_count}.png'
            with open(cur_save_path, 'wb') as f:
                f.write(image_data)
                image_count = image_count + 1
            result.append(cur_save_path)
    # 3.关闭打开的pdf
    doc.close()
    return result


def extract_text(path):
    '''从图片中提取文字'''
    result_str = []
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to load model into memory
    image_path = path
    result = ocr.ocr(image_path, cls=True)
    for line in result[0]:
        result_str.append(str(line[1][0]))
    return result_str

def extract_result(file_list):
    '''从图片列表中提取需求文字'''
    av_str = None
    vate_str = None
    for x in file_list:
        print('当前文件FileName:', x)
        str_list = extract_text(x)
        if "药品再注册批件" in str_list:
            if "药品批准文号" in str_list:
                # print(str_list[str_list.index("药品批准文号") + 1])
                av_str = str_list[str_list.index("药品批准文号") + 1]
            if "药品批准文号有效期" in str_list:
                # print(str_list[str_list.index("药品批准文号有效期") + 1])
                vate_str = str_list[str_list.index("药品批准文号有效期") + 1]
            print("当前提取结果",av_str,vate_str)
            return av_str,vate_str
    return None

def i_main(pdf_file_path,save_path):
    '''
    主函数
    :return:tuple(国药准字,国药准字有效期)
    '''
    file_list = extract_pics(pdf_file_path, save_path)
    print("导出 {} 张图片".format(len(file_list)))
    result = extract_result(file_list)
    return result