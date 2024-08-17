import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import copy

imagefol="/home/nirnaya/Desktop/Edge AI/annotation_app/images"
annotationfol="/home/nirnaya/Desktop/Edge AI/annotation_app/Poly_labels"
outputfol="/home/nirnaya/Desktop/Edge AI/annotation_app/Poly_images"

font=cv2.FONT_HERSHEY_SIMPLEX
fontScale=1
color=(255,0,0)
thickness=2

imlist=os.listdir(imagefol) #imlist will have all the imagenames as a list


for i in imlist:
    poly_points=[]
    im=cv2.imread(os.path.join(imagefol,i))
    imb=np.zeros_like(im)
    cv2.rectangle(im, (0, 0), (50, 30),color, 2)
    cv2.rectangle(im, (500, 0), (560, 30),color, 2)
    cv2.rectangle(im, (1000, 0), (1100, 30),color, 2)
    org=(00,20)
    im=cv2.putText(im, "next", org,font, fontScale, color, thickness,cv2.LINE_AA)
     
    org=(500,20)
    im=cv2.putText(im, "Car", org, font, fontScale, color, thickness,cv2.LINE_AA)

    org=(1000,20)
    im=cv2.putText(im, "Person", org, font, fontScale, color, thickness,cv2.LINE_AA)

    plt.imshow(im)
    
    flag=1
    while(flag):
        pl=[]
        while(1):
            p=plt.ginput(1)
            (px,py)=p[0][0],p[0][1]
            if px>500 and py>0 and px<560 and py<30:
                type="car"
                if pl:
                    pl.insert(0,type)
                break
            if px>1000 and py>0 and px<1100 and py<30:
                type="person"
                if pl:
                    pl.insert(0,type)
                break
            if px<50 and py<30:
                plt.close()
                flag=0
                break
            pl.append((int(px),int(py)))
        if pl:
            poly_points.append(pl)
    print(poly_points)
    plt.show()
    for a in poly_points:
        pt=copy.deepcopy(a)
        ty=pt.pop(0)
        clr=(255,255,255)
        if ty=="car":
            clr=(100,100,255)
        elif ty=="person":
            clr=(150,255,150)
        cv2.fillPoly(imb,[np.array(pt)],clr)
    cv2.imshow('win',imb)
    cv2.waitKey()
    cv2.destroyAllWindows()

    frame=i[: -4]
    dst_txt=frame + '.txt'
    dst_png=frame + '.png'
    with open(os.path.join(annotationfol,dst_txt),'w') as f:
        for b in poly_points:
            f.write(str(b.pop(0))+" ")
            for a in b:
                f.write("("+str(a[0]) + "," + str(a[1])+")")
            f.write("\n")
    f.close()
    cv2.imwrite(os.path.join(outputfol,dst_png),imb)
#run for multiple images
#save the segmented image using cv2.imwrite
#try to save multiple polygons in the same image