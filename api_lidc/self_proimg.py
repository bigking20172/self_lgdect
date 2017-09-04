import os
import argparse
import dicom
import numpy as np
import struct
import scipy.misc
from self_annotation import find_all_files
from self_annotation import parse_original_xmls
import cv2
import pickle
import shutil


company_ge = 'E:/medical_pro/lidc_nodule_detection-master/api_lidc/self_company_ge.txt'
OUT_PATH = 'F:/medicial_sp/LIDC-IDRI'
dst_2class = 'F:/medicial_sp'


def process_onefold(srcpath,dstpath,name):
    image_list = {}
    instance_list = {}
    for f_dcm in find_all_files(srcpath, suffix='.dcm'):
        dcm = dicom.read_file(f_dcm)
        z = dcm[0x0020, 0x0013].value  # instance number
        ##imge =  np.array(dcm.pixel_array)

        h = dcm[0x0028, 0x0010].value
        w = dcm[0x0028, 0x0011].value
        sop_uid = dcm[0x08, 0x18].value
        instance_list[z] = sop_uid
        image_list[z] = np.array(dcm.pixel_array)

        # sort by z position
    images = []
    for i in sorted(image_list.keys(), reverse=True):
        # for i in sorted(image_list.keys()):
        images.append(image_list[i])

    instances = []
    for i in sorted(instance_list.keys(), reverse=True):
        instances.append(instance_list[i])

    map_uid = {}
    for i in range(len(instances)):
        map_uid[instances[i]] = i

    for i in range(len(images)):
        print '{}/{}_{}.png'.format(dstpath, name, i)
        scipy.misc.imsave('{}/{}_{}.png'.format(dstpath, name, i),images[i])

    return map_uid

def draw_rectangle(dst_path):
    files = os.listdir(dst_path)
    for file in files:
        if file.find('.txt') != -1:
            img_name = file.split('.')[0] + '.png'
            img_path = os.path.join(dst_path, img_name)
            txt_path = os.path.join(dst_path,file)
            dst_txt = os.path.join(dst_2class,file)
            dst_img1 = os.path.join(dst_2class,img_name)
            img_rec = '{}/{}_rect.png'.format(dst_path,file.split('.')[0])
            dst_rect = '{}/{}_rect.png'.format(dst_2class,file.split('.')[0])
            f = open(txt_path,'r')
            img = cv2.imread(img_path)
            flag = 0
            for line in f:
                line = line.replace('\n','')
                str_list = line.split(' ')
                cls = int(str_list[0])
                if cls == 0:
                    cv2.rectangle(img,(int(str_list[1]), int(str_list[2])),(int(str_list[3]), int(str_list[4])),(255, 0, 0),1)
                    flag = 1
                elif cls == 1:
                    cv2.rectangle(img, (int(str_list[1]), int(str_list[2])), (int(str_list[3]), int(str_list[4])), (0, 255, 0), 1)
                else:
                    cv2.rectangle(img, (int(str_list[1]), int(str_list[2])), (int(str_list[3]), int(str_list[4])), (0, 0, 255), 1)

            cv2.imwrite(img_rec,img)
            if flag == 1:
                shutil.copy(img_path, dst_img1)
                shutil.copy(txt_path, dst_txt)
                shutil.copy(img_rec, dst_rect)

def main():
    file_ge = open(company_ge,'r')
    count = 0
    for line in file_ge:
        if count >= 166:

            src_path = line.split('\n')[0]
            assert os.path.exists(src_path)
            name = line.split('/')[3]
            print src_path
            dst_path = os.path.join(OUT_PATH, name)
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            map_uid = process_onefold(src_path,dst_path,name)
            parse_original_xmls(name,src_path,dst_path,map_uid)
            draw_rectangle(dst_path)
        count = count + 1

if __name__ == '__main__':
    main()