import xml.etree.ElementTree as ET
from os import getcwd
import re

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

# classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

labels_path='labels.txt'
with open(labels_path,'rb') as f:
    label_names = f.readlines()
    classes = [c.decode('utf-8').split(':')[0] for c in label_names]

def convert_annotation(year, image_id, list_file):
    print(image_id)
    try:
        in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id),'rb').read().decode('gbk')
    except:
        in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id),'rb').read().decode('utf-8')
    match = re.match(r'([a-zA-Z0-9\_]+[\_])([0-9]+)', image_id, re.I)
    cls = match.groups()[1]
    root = ET.XML(in_file)
    # tree=ET.parse(in_file)
    # root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        # cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('/output/%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('/output/JPEGImages/%s.jpg'%(image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

