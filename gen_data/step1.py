# -*- coding:utf-8 -*-
"""
我现有VOC2007数据格式，要转化后才能类似east的数据格式，然后在再通过作者提供的数据代码来训练数据
VOC2007下的Annotations(221999)JPEGImages(222037)
对xml和jpg都存在的数据进行转化221999
"""
import xml.etree.ElementTree as ET
import numpy as np
import numpy as np
import os
import shutil,glob
import cv2
import json

def gen_east_data_from_ctpn():
    save_dir = '/data/kuaidi01/dataset_detect/AdvancedEast_data'
    save_txt_dir = os.path.join(save_dir, 'txt_all')
    save_jpg_dir = os.path.join(save_dir, 'image_all')
    if os.path.exists(save_txt_dir):
        shutil.rmtree(save_txt_dir)
    os.makedirs(save_txt_dir)
    if os.path.exists(save_jpg_dir):
        shutil.rmtree(save_jpg_dir)
    os.makedirs(save_jpg_dir)


    xml_path = '/data/kuaidi01/dataset_detect/VOC2007/Annotations/*.xml'
    jpg_dir = '/data/kuaidi01/dataset_detect/VOC2007/JPEGImages'


    xmls = glob.glob(xml_path)
    num = 0
    for idx, xml_path in enumerate(xmls):
        e = ET.parse(xml_path).getroot()
        width = float(e.find('size').find('width').text)
        height = float(e.find('size').find('height').text)
        assert width > 0 and height > 0, 'xml s width or height error'
        xml_name = os.path.basename(xml_path)[:-4]
        ctpn_jpg_path = os.path.join(jpg_dir, xml_name+'.jpg')
        east_txt_path = os.path.join(save_txt_dir, xml_name+'.txt')
        east_jpg_path = os.path.join(save_jpg_dir, xml_name+'.jpg')

        # copy jpg
        if not os.path.exists(ctpn_jpg_path):
            continue
        else:
            shutil.copy(ctpn_jpg_path, east_jpg_path)

        # write txt
        with open(east_txt_path, 'w') as o:
            for bbox in e.findall('object'):
                inst_bbox = bbox.find('bndbox')
                xmin = float(inst_bbox.find('xmin').text) if float(inst_bbox.find('xmin').text) >= 0 else float(0)
                ymin = float(inst_bbox.find('ymin').text) if float(inst_bbox.find('ymin').text) >= 0 else float(0)
                xmax = float(inst_bbox.find('xmax').text) if float(inst_bbox.find('xmax').text) <= width else float(width)
                ymax = float(inst_bbox.find('ymax').text) if float(inst_bbox.find('ymax').text) <= height else float(height)


                icdar_text = '%s,%s,%s,%s,%s,%s,%s,%s,text' % (xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax)
                o.write(icdar_text+'\n')

        num+=1

        if idx%10000 == 0:
            print('finish:', idx)
    print('all finished', idx, 'transfer num:',num)

gen_east_data_from_ctpn()