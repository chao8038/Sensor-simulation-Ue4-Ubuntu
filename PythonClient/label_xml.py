import cv2
import os
import glob

input_dir = 'D:/pothole/UE4/20200824/seg'
#out_dir = '/home/wmy/darknet/VOCdevkit3/VOC2007/JPEGImages'
a = os.listdir(input_dir)
for j in a:
    img = cv2.imread(input_dir+'/'+j)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(input_dir+'/'+j)
    bbox = [ ]
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        z=(x + w)
        q=(y + h)
        cv2.rectangle(img, (x, y), (z, q), (0, 255, 0), 1)
        rect = cv2.minAreaRect(contours[i])
        
        
        bbox.append([x,y,z,q])
        
        #print(x,y,z,q)
    file_name = os.path.splitext(j)[0]
    f = open( os.path.join('D:/pothole/UE4/20200824/label/', file_name + '.xml'), 'w+', encoding='utf-8')
    print(os.path.join('D:/pothole/UE4/20200824/label/', file_name + '.xml'))
    lines = f.readlines()
    
    f.write("<annotation verified= 'yes'>"+'\n')
    f.write('\t'+"<folder>data</folder>"+'\n')
    f.write('\t'+"<filename>"+file_name+".jpg"+"</filename>"+'\n')
    f.write('\t'+"<path>"+file_name+".jpg"+"</path>"+'\n')
    f.write('\t'+"<source>"+'\n')
    f.write('\t'+'\t'+"<database>Unknown</database>"+'\n')
    f.write('\t'+"</source>"+'\n')
    f.write('\t'+"<size>"+'\n')
    f.write('\t'+'\t'+"<width>1280</width>"+'\n')
    f.write('\t'+'\t'+"<height>720</height>"+'\n')
    f.write('\t'+'\t'+"<depth>3</depth>"+'\n')
    f.write('\t'+"</size>"+'\n')
    f.write('\t'+"<segmented>0</segmented>"+'\n')
    for (x,y,z,q) in bbox:
        print(x,y,z,q)
        f.write('\t'+"<object>"+'\n')
        f.write('\t'+'\t'+"<name>pavement_barrier</name>"+'\n')
        f.write('\t'+'\t'+"<pose>Unspecified</pose>"+'\n')
        f.write('\t'+'\t'+"<truncated>0</truncated>"+'\n')
        f.write('\t'+'\t'+"<difficult>0</difficult>"+'\n')
        f.write('\t'+'\t'+"<bndbox>"+'\n')
        f.write('\t'+'\t'+'\t'+"<xmin>"+str(x)+"</xmin>"+'\n')
        f.write('\t'+'\t'+'\t'+"<ymin>"+str(y)+"</ymin>"+'\n')
        f.write('\t'+'\t'+'\t'+"<xmax>"+str(z)+"</xmax>"+'\n')
        f.write('\t'+'\t'+'\t'+"<ymax>"+str(q)+"</ymax>"+'\n')
        f.write('\t'+'\t'+"</bndbox>"+'\n')
        f.write('\t'+"</object>"+'\n')
    f.write("</annotation>")
    f.close()
    
    