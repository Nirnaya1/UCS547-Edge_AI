import cv2
import os
import copy


# Paths to the image and label folders
image_folder = '/home/nirnaya/Desktop/Edge AI/annotation_app/images'
label_folder = '/home/nirnaya/Desktop/Edge AI/annotation_app/labels'

font=cv2.FONT_HERSHEY_SIMPLEX
fontScale=1
color=(255,0,0)
thickness=2

# Function to draw bounding boxes and labels on an image
def draw_labels_on_image(image_path, label_path):
    # Load the image
    image = cv2.imread(image_path)

    shape=image.shape
    height=shape[0]
    width=shape[1]
    
    # Read the labels from the file
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # Draw each label
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue
        
        label = parts[0]
        xmin = int(float(parts[1])*width)
        ymin = int(float(parts[2])*height)
        xmax = int(float(parts[3])*width)
        ymax = int(float(parts[4])*height)
        
        # Calculate the bounding box coordinates

        if label=='car':
            color=(100,100,255)
        else:
            color=(150,255,150)
        
        
        # Draw the bounding box
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax),color, 2)
        
        # Put the label text above the bounding box
        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,color, 2)
    
    return image

# Process all images in the image folder
for image_filename in os.listdir(image_folder):
    if not image_filename.endswith(('.jpg', '.png', '.jpeg')):
        continue
    
    # Construct the full path for the image and label files
    image_path = os.path.join(image_folder, image_filename)
    label_path = os.path.join(label_folder, os.path.splitext(image_filename)[0] + '.txt')

    while(1):
        if os.path.exists(label_path):
            # Draw labels on the image
            annotated_image = draw_labels_on_image(image_path, label_path)

            shape=annotated_image.shape
            height=shape[0]
            width=shape[1]

            im=copy.deepcopy(annotated_image)

            org=(00,20)
            annotated_image=cv2.putText(annotated_image, "next", org,font, fontScale, color, thickness,cv2.LINE_AA)

            org=(500,20)
            annotated_image=cv2.putText(annotated_image, "add roi", org, font, fontScale, color, thickness,cv2.LINE_AA)

            r=cv2.selectROI(annotated_image)
            if r[0]<50 and r[1]<30:
                break
            if r[0]>500 and r[0]<550 and r[1]>0 and r[1]<30:
                org=(00,20)
                im=cv2.putText(im, "done", org,font, fontScale, color, thickness,cv2.LINE_AA)

                org=(500,20)
                im=cv2.putText(im, "car", org, font, fontScale, color, thickness,cv2.LINE_AA)

                org=(1000,20)
                im=cv2.putText(im, "Person", org, font, fontScale, color, thickness,cv2.LINE_AA)
                
                frame=image_filename[: -4]
                dst_txt=frame+'.txt'
                with open(os.path.join(label_folder,dst_txt),'a') as f:
                    while (1):
                        r1=cv2.selectROI('ROI selector',im)
                        if r1[0]<50 and r1[1]<30:
                            break
                        r2=cv2.selectROI(im)
                        if r2[0]>500 and r2[0]<550 and r2[1]>0 and r2[1]<30:
                            s='car'
                            clr=(100,100,255)
                        if r2[0]>1000 and r2[0]<1050 and r2[1]>0 and r2[1]<30:
                            s='person'
                            clr=(150,255,150)

                        xmin=r1[0]/width
                        ymin=r1[1]/height
                        xmax=(r1[0]+r1[2])/width
                        ymax=(r1[1]+r1[3])/height
                        cv2.rectangle(im,(r1[0],r1[1]),((r1[0]+r1[2]),(r1[1]+r1[3])),clr,2)
                        line=s + " " +str(xmin)+" "+str(ymin)+" "+str(xmax)+" "+str(ymax)+"\n"
                        f.write(line)
                f.close()

        # Optionally, save the annotated image
        # output_path = os.path.join('path_to_save_folder', image_filename)
        # cv2.imwrite(output_path, annotated_image)

cv2.destroyAllWindows()
