import os
import numpy as np
from PIL import Image 
import glob
import xml.etree.ElementTree as ET


path = "path"  #xml 경로 설정
file_list = os.listdir(path)
file_list_py = [file for file in file_list if file.endswith(".xml")]
print ("file_list_xml: {}".format(file_list_py))
#len(file_list_py)




path2='jpg2'#jpg 경로설정
file_list = os.listdir(path2)
file_list_jpg = [file for file in file_list if file.endswith(".jpg")]  
#print ("file_list_jpg: {}".format(file_list_jpg))

save_path_xml="path"
save_path_img="path"

labels=['bicycle',  #label 
'bus',
'car',
'carrier',
'cat',
'dog',
'motorcycle',
'movable_signage',
'person',
'scooter',
'stroller',
'truck',
'wheelchair',
'barricade',
'bench',
'bollard',
'chair',
'fire_hydrant',
'kiosk',
'parking_meter',
'pole',
'potted_plant',
'power_controller',
'stop',
'table',
'traffic_light',
'traffic_light_controller',
'traffic_sign',
'tree_trunk'
]

def obj_tv():
    for label in labels:
        trainval = open('ImageSets/Main/'+label+'_trainval.txt', 'w')
        val = open('ImageSets/Main/'+label+'_val.txt', 'w')
        train = open('ImageSets/Main/'+label+'_train.txt', 'w')
        train.close()
        val.close()        
        trainval.close() 
        
    for label in labels:
        trainval = open('ImageSets/Main/'+label+'_trainval.txt', 'a')
        val = open('ImageSets/Main/'+label+'_val.txt', 'a')
        train = open('ImageSets/Main/'+label+'_train.txt', 'a')
        i=0
        for lis in file_list_py:
            tree = ET.parse(path+lis)
            root = tree.getroot()
            a=[]
            for obj in root.findall('object') :
                objs=obj.find('name')
                txt = objs.text
                a.append(txt)
            b=set(a)
            if label in b:
                trainval.write(lis[:-4]+'  1\n')
                if(i<len(file_list_py)*0.2):
                   val.write(lis[:-4]+'  1\n')
                else:
                   train.write(lis[:-4]+'  1\n')
            else:
                trainval.write(lis[:-4]+' -1\n')
                if(i<len(file_list_py)*0.2):
                   val.write(lis[:-4]+' -1\n')
                else:
                   train.write(lis[:-4]+' -1\n')
            i=i+1
        train.close()
        val.close()        
        trainval.close()  
    print("Finish")
    
    
def create_tv():
    trainval = open('ImageSets/Main/trainval.txt', 'w')
    val = open('ImageSets/Main/val.txt', 'w')
    train = open('ImageSets/Main/train.txt', 'w') 
    train.close()
    val.close()        
    trainval.close() 

    trainval = open('ImageSets/Main/trainval.txt', 'a')
    val = open('ImageSets/Main/val.txt', 'a')
    train = open('ImageSets/Main/train.txt', 'a')
    i=0
    for lis in file_list_py:  
        trainval.write(lis[:-4]+'\n')
        if(i<len(file_list_py)*0.2):
            val.write(lis[:-4]+'\n')
        else:
            train.write(lis[:-4]+'\n')
        i=i+1 
    train.close()
    val.close()        
    trainval.close() 
    print('Finish')
    
    
    
    
def check_object():
    for lis in file_list_py:  
        tree = ET.parse(path+lis)
        root=tree.getroot()
        i=0
        for elem in root.findall("object"):
            i=i+1
        if i==0:
            print(lis+' has no object\n')
    print("Finish!")
    
def check_channel():
    for img in file_list_jpg:
        img=np.array(Image.open(path2+img))
        if img.shape[-1]!=3:
            print(img+'has no 3 channel') # 채널검사
    
    print("Finish!")


def img_resize(width,height):
    for img in file_list_jpg:
        image=Image.open(path2+img)
        resize_image=image.resize((width,height))
        resize_image.save(save_path_img+img)
    print('finish!')
    
    
def resize_xml(wdt=500,hgt=300):
    for lis in file_list_py:
        tree=ET.parse(save_path_xml+lis)
 
        size=tree.find('size')  

        width=size.find('width')    
        original_width=int(width.text)
        width.text=str(wdt)

        height=size.find('height')
        original_height=int(height.text)
        height.text=str(hgt)
        
        for obj in tree.findall('object'):
            bdbox=obj.find('bndbox')    
    
            xmin=bdbox.find('xmin')
            resize_xmin=float(xmin.text)
            resize_xmin=str(round(resize_xmin*(wdt/original_width)))
            xmin.text=resize_xmin
    
            ymin=bdbox.find('ymin')
            resize_ymin=float(ymin.text)
            resize_ymin=str(round(resize_ymin*(hgt/original_height)))
            ymin.text=resize_ymin
    
            xmax=bdbox.find('xmax')
            resize_xmax=float(xmax.text)
            resize_xmax=str(round(resize_xmax*(wdt/original_width)))
            xmax.text=resize_xmax
    
            ymax=bdbox.find('ymax')
            resize_ymax=float(ymax.text)
            resize_ymax=str(round(resize_ymax*(hgt/original_height)))
            ymax.text=resize_ymax
            
            
        tree.write(save_path_xml+lis)
        
        
        
        
obj_tv()
create_tv()  # create train, trainval, val
img_resize(300,300)  # image resize
resize_xml()    # resize xmin, xmax ymin ymax
