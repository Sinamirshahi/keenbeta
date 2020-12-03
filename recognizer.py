import cv2,numpy as np
import argparse
import json
from pathlib import Path
import os

def region_of_interest(image, starting_point = (0,0), area = (0,0)):
    crop_img = image[starting_point[1]:starting_point[1]+area[1], starting_point[0]:starting_point[0]+area[0]]
    return crop_img

def assembler(image,thresh_line = 200 ):
    # Load image, grayscale, Gaussian blur, Otsu's threshold
    # image = cv2.imread('test_data/img2.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ( int(image.shape[1]/thresh_line) ,1))
    horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

    # Detect vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,int(image.shape[0]/thresh_line)))
    vertical_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)

    # Combine masks and remove lines
    table_mask = cv2.bitwise_or(horizontal_mask, vertical_mask)
    image[np.where(table_mask==255)] = [255,255,255]


    #save the images
    structure = cv2.bitwise_not(table_mask)
    structure = cv2.cvtColor(structure,cv2.COLOR_GRAY2RGB)

    return structure

def liner(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image.shape[1]/3),1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (36,255,12), thinckness)

    return image


# now let's initialize the list of reference point
ref_point = []
ref_point_while_moving = None
bounding_box = []
my_list = []
json_list = ''
layout_output_file = ''
i = 0
thinckness = 5
crop = False




def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, bounding_box,crop,ref_point_while_moving

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        ref_point_while_moving = ref_point[0]

        bounding_box = [(x, y)]
        crop = True

        #print(bounding_box)
    elif event == cv2.EVENT_MOUSEMOVE and crop:
        ref_point_while_moving = (x, y)

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        ref_point_while_moving = (x, y)
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))


        # if ref_point[0][0] < x:
        #     ref_point[0][0] , x = x , ref_point[0][0]

        # if ref_point[0][1] < y:
        #     ref_point[0][1] , y = y , ref_point[0][1]

        width = x - ref_point[0][0]
        height = y - ref_point[0][1]

        #NEW METHOD

        ROI = image[ref_point[0][1]:ref_point[0][1]+height,ref_point[0][0]:ref_point[0][0]+width]


        # gray = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image.shape[1]/10),1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,int(image.shape[0]/10)))
        detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)


        cnts_hrz = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_vrt = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
        # detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        # cnts = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts_vrt = cnts_vrt[0] if len(cnts_vrt) == 2 else cnts_vrt[1]
    
        for c in cnts_vrt:
            # daymax = np.amax(c,axis=0)   
            # print(daymax)q
            a = c[0][0][0]
            b = c[-1][0][0]

            x = int((a+b)/2)

            print("x: ",x)
           
            cv2.drawContours(ROI, [c], -1, (0,0,255), thinckness)



        cnts_hrz = cnts_hrz[0] if len(cnts_hrz) == 2 else cnts_hrz[1]
        for c in cnts_hrz:
            a = c[0][0][1]
            b = c[-1][0][1]

            y = int((a+b)/2)

            print("y: ",y)
           


            cv2.drawContours(ROI, [c], -1, (0,0,255), thinckness)
            #x,y,w,h = cv2.boundingRect(c)
            #image[y:y+height, x:x+width] = ROI



        
        
        image[ref_point[0][1]:ref_point[0][1]+height,ref_point[0][0]:ref_point[0][0]+width] = ROI

        


        bounding_box.append((width, height))
        print (bounding_box)

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), thinckness)
        cv2.imshow("image", image)
        my_list.append(bounding_box)
        #list.append(ref_point)
        # print(list)
        json_list = json.dumps(my_list)
        # print(json_list)
        print(json_list, file=open(layout_output_file, 'w'))
        crop = False


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
    
# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
# args = vars(ap.parse_args())

input = "/home/non/kkk/keenbeta/jpg_converted/201201113919385-BAY20061506171.pdf.jpg"



filename_w_ext = os.path.basename(input)
filename, file_extension = os.path.splitext(filename_w_ext)
layout_output_file = f'layouts/layout_{filename}.json'

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(input)


height = image.shape[0]
thinckness = (int(height/300))
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)


# keep looping until the 'q' key is pressed
while True:
    image = ResizeWithAspectRatio(image, height = image.shape[0]) 


    # Resize by height, comment the above line to use the original height
    # if original height is used, a scrollbar (or another method) should be implemented
    # or... we can resize but might need to rescale the bounding_box *probably* to get everything in absolute values
    # unless the images are also resized from the pdf
    
    # display the image and wait for a keypress
    # cv2.imshow("image", image)

    if not crop:
        cv2.imshow('image', image)
    elif crop and ref_point:
        rect_cpy = image.copy()
        cv2.rectangle(rect_cpy, bounding_box[0], ref_point_while_moving, (0, 255, 0), thinckness)
        cv2.imshow('image', rect_cpy)



    key = cv2.waitKey(1) & 0xFF

    # press 'r' to reset the window
    if key == ord("r"):
        image = clone.copy()
        my_list = []
        json_list = ''

    # if the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break

# close all open windows
cv2.destroyAllWindows() 
