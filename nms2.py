import numpy as np
import cv2
import os   
# Malisiewicz et al.  
def non_max_suppression_fast(boxes, overlapThresh):  
    # if there are no boxes, return an empty list  
    if len(boxes) == 0:  
        return []  
   
    # if the bounding boxes integers, convert them to floats --  
    # this is important since we'll be doing a bunch of divisions  
    if boxes.dtype.kind == "i":  
    	boxes = boxes.astype("float")  
   
    # initialize the list of picked indexes   
    pick = []  
   
    # grab the coordinates of the bounding boxes  
    x1 = boxes[:,0]  
    y1 = boxes[:,1]  
    x2 = boxes[:,2]  
    y2 = boxes[:,3]  

    # compute the area of the bounding boxes and sort the bounding  
    # boxes by the bottom-right y-coordinate of the bounding box  
    area = (x2 - x1 + 1) * (y2 - y1 + 1)  
    idxs = np.argsort(y2)  
   
    # keep looping while some indexes still remain in the indexes  
    # list  
    while len(idxs) > 0:  
        # grab the last index in the indexes list and add the  
        # index value to the list of picked indexes  
        last = len(idxs) - 1  
        i = idxs[last]  
        pick.append(i)  
   
        # find the largest (x, y) coordinates for the start of  
        # the bounding box and the smallest (x, y) coordinates  
        # for the end of the bounding box  
        xx1 = np.maximum(x1[i], x1[idxs[:last]])  
        yy1 = np.maximum(y1[i], y1[idxs[:last]])  
        xx2 = np.minimum(x2[i], x2[idxs[:last]])  
        yy2 = np.minimum(y2[i], y2[idxs[:last]])  
   
        # compute the width and height of the bounding box  
        w = np.maximum(0, xx2 - xx1 + 1)  
        h = np.maximum(0, yy2 - yy1 + 1)  
   
        # compute the ratio of overlap  
        overlap = (w * h) / area[idxs[:last]]  
         # delete all indexes from the index list that have  
        idxs = np.delete(idxs, np.concatenate(([last],  
        np.where(overlap > overlapThresh)[0])))  
   
    # return only the bounding boxes that were picked using the  
    # integer data type  
    return boxes[pick].astype("int")

def draw_nmsrec(txt_path,img_dir,save_dir):
    txt_open = open(txt_path,'r')
    for txt_name in txt_open:
	txt = img_dir+'/'+txt_name.strip('\n')
	f_open = open(txt,'r')
        boxes = []
        for line in f_open:
	    line = line.strip('\n')
	    line = line.strip('\r')
	    str_list = line.split(' ')
	    splite_int = [int(s) for s in str_list]
	    box = [0,0,0,0]			
            kind = splite_int[0]
            w = splite_int[3] - splite_int[1]
	    h = splite_int[4] - splite_int[2]
            if (kind == 0) and (w > 5) and (h > 5): 
               box[0] = splite_int[1]
               box[1] = splite_int[2]
               box[2] = splite_int[3]
               box[3] = splite_int[4]	
	       boxes.append(box)
        np_boxes = np.array(boxes)
        out_boxes = non_max_suppression_fast(np_boxes, 0.5)  
        #f_write = open(save_dir+'/'+txt_name.strip('\n')+'.txt','w')
        #f_imgrec = cv2.imread(img_dir+'/'+txt_name.strip('\n').replace('txt','png'))
       
	if len(out_boxes) > 0:
	   f_write = open(save_dir+'/'+txt_name.strip('\n')+'.txt','w')	 
           f_imgrec = cv2.imread(img_dir+'/'+txt_name.strip('\n').replace('txt','png'))
           for i in range(0,out_boxes.shape[0]):
 	   	f_write.writelines(str(out_boxes[i][0])+' '+str(out_boxes[i][1])+' '+str(out_boxes[i][2])+' '+str(out_boxes[i][3]))
           	cv2.rectangle(f_imgrec,(out_boxes[i][0],out_boxes[i][1]),(out_boxes[i][2],out_boxes[i][3]),(255,0,0),1)
	   cv2.imwrite(save_dir+'/'+txt_name.strip('\n').replace('txt','png'),f_imgrec)
	   f_write.close()

    
if __name__ == '__main__':
    txt_dir = '/Volumes/self_hd/deal_samples/pro_txt.txt' 
    img_dir  = '/Volumes/self_hd/medicial_sp'
    save_dir = '/Volumes/self_hd/deal_samples/save_rec'
    draw_nmsrec(txt_dir,img_dir,save_dir)
    #im_file = cv2.imread('LIDC-IDRI-0001_89.png')
    #cv2.imshow('asd',im_file)
    #cv2.namedWindow("Image")
    #cv2.imshow("Image",im_file)
    #cv2.waitKey(0)
    # if there are no boxes, return an empty list  
    print 'success'
