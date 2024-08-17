import os
import cv2

#first version : taking 1 ROI from each image and saving it in txt file
#second version : we want multiple ROI from image
#third version : we want to know the type of each ROI when they are not all car or all people

imagefol="/home/nirnaya/Desktop/Edge AI/annotation_app/images"
annotationfol="/home/nirnaya/Desktop/Edge AI/annotation_app/labels"

imlist=os.listdir(imagefol) #imlist will have all the imagenames as a list

font=cv2.FONT_HERSHEY_SIMPLEX
fontScale=1
color=(255,0,0)
thickness=2

for im in imlist:
    img=cv2.imread(os.path.join(imagefol,im)) #img is a 3d array containing the RGB image
    #no of bits for the image = rows*cols*3*8

    

    shape=img.shape
    height=shape[0]
    width=shape[1]
   
    org=(00,20)
    img=cv2.putText(img, "next", org,font, fontScale, color, thickness,cv2.LINE_AA)
     
    org=(500,20)
    img=cv2.putText(img, "Car", org, font, fontScale, color, thickness,cv2.LINE_AA)

    org=(1000,20)
    img=cv2.putText(img, "Person", org, font, fontScale, color, thickness,cv2.LINE_AA)
    
    frame=im[: -4]
    dst_txt=frame + '.txt'
    with open(os.path.join(annotationfol,dst_txt),'w') as f:
        while(1):
            r=cv2.selectROI('selector',img) #returns x0 y0 width height

            if r[0]<50 and r[1]<50:
                break
            
            r1=cv2.selectROI('selector',img)
            print(r1)
            if r1[0]>500 and r1[0]<550 and r1[1]>0 and r1[1]<50: #manipulating and existing
                s="car"  #assuming your car org was(500,20)
                clr=(100,100,255)

            if r1[0]>1000 and r1[0]<1050 and r1[1]>0 and r1[1]<50: #manipulating and 
                s="person"  #assuming your person org was(1000,20)
                clr=(150,255,150)
            

            xmin=r[0]/width
            ymin=r[1]/height
            xmax=(r[0]+r[2])/width
            ymax=(r[1]+r[3])/height
            cv2.rectangle(img,(r[0],r[1]),((r[0]+r[2]),(r[1]+r[3])),clr,2)
            line=s + " " +str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax)+"\n"
            f.write(line)
    f.close()
cv2.destroyAllWindows()
                #there are various annotation format requirements 
                #xmin ymin xmax ymax
                #xmin ymin width height
                #ymin xmin ymax xmax
