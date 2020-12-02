import os, glob,json, difflib,pytesseract,cv2,imutils,re
from pdf2image import convert_from_path
from pytesseract import Output,image_to_osd
from skimage.metrics import structural_similarity as ssim
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pyzbar import pyzbar
from scipy import ndimage


class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"

		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"

		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"

		# return the name of the shape
		return shape



def set_environment(tessdata_folder_path='models'):
    ###setting environment for tesserect engine to load models
    os.environ["TESSDATA_PREFIX"]=str((os.path.join(os.getcwd(),tessdata_folder_path)))
    print("TESSDATA_PREFIX has been set to: {}".format(str(os.environ.get("TESSDATA_PREFIX"))))

def margin_cut(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
    coords = cv2.findNonZero(gray) # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
    rect = image[y:y+h, x-int(5/100*w):x+w] # Crop the image - note we do this on the original image
    return rect

def rotate_tes(image):
    angle = 360 - int(re.search('(?<=Rotate: )\d+', image_to_osd(image)).group(0))
    if angle != 0:
        rotated = ndimage.rotate(image, float(angle))
    return rotated

def rotate(image,major = False):
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    image = np.asarray(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)

    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


    if major == True:
        rotated = rotate_tes(rotated)
    return rotated


def image_convert(path_in , path_out='jpg_converted', absolute_path = False , prefered_dpi = 500 , rotatation_fix = False):
    '''
    @param path_in: folder indicating pdf files 
    @param path_out: folder indicating output image files ( this folder sits inside input file ) 
    @param absolute_path: if sets TRUE, paths out image file will return in absolute mode
    @param prefered_dpi: the prefered dpi of output image files
    
    '''
    cwd = os.getcwd() #getting curent woeking directory

    list_pdf = glob.glob(os.path.join(cwd,path_in,"*.pdf")) #getting the list of pdf files inside the input folder
    list_PDF = glob.glob(os.path.join(cwd,path_in,"*.PDF")) #getting the list of pdf files inside the input folder
    list = list_pdf+list_PDF
    path_out = os.path.join(path_in,path_out) #where to save images, (a filder inside input folder)
    
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    output_list = [] # list of addreses of image files which obtained from pdfs

    for pdf_file in list:
        pages = convert_from_path(pdf_file, dpi=prefered_dpi)
        for index , page in enumerate(pages): #make a loop if a pdf file has multiple pages
            save_path =    os.path.join(path_out,os.path.basename(pdf_file))
            if len(pages) > 1: # add an index at the end of each file name if pdf has multiple pages
                save_path = save_path + "_"+str(index+1)
            save_path = save_path +".jpg"
            if absolute_path == True: #If user wanted absolute path of image output files
                save_path = os.path.join(cwd,save_path)
            
            #append to the list and save the file
            output_list.append(save_path)
            if rotatation_fix == True:
                page = Image.fromarray(rotate(page,major=False))
            page.save(save_path, 'JPEG')

    return (output_list)

def bound(image, starting_point = (0,0),v_line = 1, h_line =1):


        img = region_of_interest(image,starting_point=starting_point,area=(image.shape[1]-starting_point[0],image.shape[0]-starting_point[1]))
        x = img.shape[1]
        y = img.shape[0]


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image.shape[1]/10),1))
        detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,int(image.shape[0]/10)))
        detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)


        cnts_hrz = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_vrt = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        cnts_vrt = cnts_vrt[0] if len(cnts_vrt) == 2 else cnts_vrt[1]
        cnts_vrt = reversed(cnts_vrt)
    
        for index , c in enumerate(cnts_vrt):

            a = c[0][0][0]
            b = c[-1][0][0]

            x = int((a+b)/2)
            #cv2.drawContours(img, [c], -1, (0,0,255), 40)
            if index+1 == v_line:
                break


            


        cnts_hrz = cnts_hrz[0] if len(cnts_hrz) == 2 else cnts_hrz[1]
        cnts_hrz = reversed(cnts_hrz)

        for index,c in enumerate(cnts_hrz):

            a = c[0][0][1]
            b = c[-1][0][1]

            y = int((a+b)/2)
            #cv2.drawContours(img, [c], -1, (0,0,255), 40)
            if index+1 == h_line:
                break

            

        img = region_of_interest(img,starting_point=(0,0),area=(x,y))

        return (x,y) , img

def segmentizer(image_list,segmentaion_coordinates):

    segments = [] # list of cropped segments
    for image in image_list:

        # image = cv2.imread(image)
        for coordinates in segmentaion_coordinates:
            invert = False
            mass = coordinates[1]

            if isinstance(coordinates[0][0], str) and isinstance(coordinates[0][1], str):
                invert = True
                coordinates[0] = list(coordinates[0])
                coordinates[0][0] = int(coordinates[0][0])
                coordinates[0][1] = int(coordinates[0][1])
                coordinates[0] = tuple(coordinates[0])

            if isinstance(coordinates[1][0], str) and isinstance(coordinates[1][1], str):
                
                mass , _ = bound(image=image, starting_point=coordinates[0],v_line=int(coordinates[1][0]),
                    h_line= int(coordinates[1][1]))


            roi  = region_of_interest(image,starting_point=coordinates[0],area=mass) 

            if (invert):
                roi = cv2.bitwise_not(roi)
            
            segments.append(roi)


    return segments


################################################################
def segmentizer_beta(image_list,segmentaion_coordinates,stuff=[]):


    segments = [] # list of cropped segments
    for image in image_list:
        temp_image = image.copy()
        # image = cv2.imread(image)
        for coordinates in segmentaion_coordinates:
            x_margin_rate = -5
            y_margin_rate = -5

            image = temp_image
            remove_lines = False

            area = coordinates[1]

            if len(coordinates) == 3 and isinstance(coordinates[2],list): #find the region
                # print("Margin ",coordinates)
                x_margin_rate = coordinates[2][0]
                y_margin_rate = coordinates[2][1]
                coordinates.pop(2)

            if len(coordinates) == 3 and isinstance(coordinates[2],int): #find the region
                zone = coordinates[2]

                if zone == 1:
                    starting_point = (0,0)
                    mass = (int(image.shape[1]/2),int(image.shape[0]/2))

                elif zone == 2:
                    starting_point = (int(image.shape[1]/2),0)
                    mass = (int(image.shape[1]/2),int(image.shape[0]/2))

                elif zone == 3:
                    starting_point = (0,int(image.shape[0]/2))
                    mass = (int(image.shape[1]/2),int(image.shape[0]/2))

                if zone == 4:
                    starting_point = int(image.shape[1]/2),int(image.shape[0]/2)
                    mass = int(image.shape[1]/2),int(image.shape[0]/2)



                image = region_of_interest(image, starting_point=starting_point, area=mass)

                
                coordinates.pop(2)
                ddata = data_extract([remove_borders(image)])[0]
                seg_texts = ddata["text"]
                seg_conf = ddata["conf"]
                seg_y = ddata["top"]
                seg_x = ddata["left"]
                seg_w = ddata["width"]
                seg_h = ddata["height"]

                stuff.clear()
                stuff = [seg_texts,seg_conf,seg_x,seg_y,seg_w,seg_h]

                # print("tests ",seg_texts)
                # cv2.imshow("s",image)
                # cv2.waitKey(0)
                # exit()
            if isinstance(coordinates[0], str) and not isinstance(coordinates[0], tuple):
                x_margin = int(coordinates[1][0] * x_margin_rate/100) if not isinstance(coordinates[1][0],str) else 20
                y_margin = int(coordinates[1][1] * y_margin_rate/100) if not isinstance(coordinates[1][1],str) else 20
                # print("marg bros ",x_margin,y_margin)
                try:
                    pos = get_postition(coordinates[0],stuff[0],
                    stuff[2],stuff[3])
                    coordinates[0] = [pos[0]+x_margin, pos[1]+y_margin] # find the starting point

                except:
                    continue


            if isinstance(coordinates[0][0], str) and isinstance(coordinates[0][1], str) and isinstance(coordinates[0],tuple):
                remove_lines = True
                coordinates[0] = list(coordinates[0])
                coordinates[0][0] = int(coordinates[0][0])
                coordinates[0][1] = int(coordinates[0][1])
                coordinates[0] = tuple(coordinates[0])

            if isinstance(coordinates[1][0], str) and isinstance(coordinates[1][1], str):
                
                mass , _ = bound(image=image, starting_point=coordinates[0],v_line=int(coordinates[1][0]),
                    h_line= int(coordinates[1][1]))



            roi  = region_of_interest(image,starting_point=coordinates[0],area=area) 
            


            if (remove_lines == True):
                roi = remove_borders(roi.copy())
                #remove_lines = False

            segments.append(roi)


    return segments

################################################################
def data_extract(image_list, min_conf = 0 , tesserect_config="--psm 1", set_env=False, fuzzy_match = False , guess_list=[] , to_jason = False, rotatation_fix = False):
    if set_env:
        set_environment() # set the folder where trained models for tesserect exist the default is the "models" folder
    word_list=[]
    for img in image_list:
        # load the input image, convert it from BGR to RGB channel ordering,
        # and use Tesseract to localize each area of text in the input image
        #segmentaion_coordinates = [[(143,594),(1606,935)],[(1991,737),(1738,748)],[(236,1644),(1200,464)]]
        #image = cv2.imread(img)
        if rotatation_fix:
            img = rotate(img)
            
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_data(rgb,lang='eng+ces', config=tesserect_config, output_type=Output.DICT)
        results["file_name"] = str(img) #adding file name of the current image to the dict

        word_list.append(results)

    return word_list


    #     for i in range(0, len(results["text"])):
            
    #         # extract the bounding box coordinates of the text region from
    #               # the current result
    #         # IF LATER WE NEED TO USE THE BOUNDING BOXES
    #         x = results["left"][i]
    #         y = results["top"][i]
    #         w = results["width"][i]
    #         h = results["height"][i]
    #               # extract the OCR text itself along with the confidence of the
    #         #text localization

    #         #If fuzzy match is enabled, it will change the word to the closest match provided in guess_list
    #         if fuzzy_match==True and results["conf"][i] < 70: #fuzzy match only for uncertain words
    #             corrections = difflib.get_close_matches(results["text"][i], guess_list)
    #             if len(corrections) > 0:
    #                 results["text"][i] = corrections[0]

            
    #         text = results["text"][i]
           
    #         conf = int(results["conf"][i])
    #         # filter out weak confidence text localizations
    #         if conf > min_conf:
    #             # display the confidence and text to our terminal
    #             # print("Confidence: {}".format(conf))
    #             # print("Text: {}".format(text))
    #             # print("")
    #             #results is a dict form, we can send the dict or json, but in this case jason
    #             if to_jason == True:
    #                 results = json.dumps(results, indent=4, ensure_ascii=False)
    #             #json_list.append(result_json)
    #         word_list.append(results)
    # return (results)


def hot_word(list_of_words,stop_word,distance = 1): #returns the next and previous item in a list in the form of dictionay
    l = len(list_of_words)

    for index, obj in enumerate(list_of_words):
        bounding = {
            "previous" : None,
            "next" : None


        }
        if obj.lower() == stop_word.lower():
            if index < (l - 1):
                bounding["next"] = list_of_words[index + distance]
            if index > 0:
                bounding["previous"] = list_of_words[index - distance]
                
            return bounding 


def splitter(seq):
    for item in seq:
        a, b, c = item.partition(':')
        yield a+b
        if c != '':
          yield c

def crop_sentence(sentence_as_list, start ,distance = 1000000 , stop = None , sentence_mode = False , hot = False):
    '''
    crop a subsentence between start and ending poing
    returns a list of words, the starting and ending poitnt are not included
    if sentence_mode is True, it will return a sentence in the form of string 
    rather than a list
    '''
    sentence_list = sentence_as_list.copy()

    if distance == -1 or distance == -2: #dictionary passed
        if distance == -1:
            direction = 0
        elif distance == -2:
            direction = 1

        data = line_split(text_list=sentence_list,x_list=start[1],y_list=start[2],axis= direction )[start[0]]
        return data

    if hot:
        templist=[]
        # print("Stp ",start)
        # print("ls ",sentence_list)
        # print("DST ",distance)
        val = hot_word(list_of_words=sentence_list,stop_word=start,distance=int(distance))["next"]
        if val is not None:
            templist.append(val)
        return templist
        
    if stop == None:
      sentence_list.append('!!END!!@')  
      stop = "!!END!!@"


    crop_range = []
    pick_words=False
    counter = False
    index = 0

    for item in sentence_list:
        
        if pick_words==True:
            crop_range.append(item)

        if str(item).lower() == str(start).lower():
            pick_words = True
            counter = True

        if counter:
            index = index +1
        
        if item == stop or index == distance+2:
            
            ret = crop_range[:-1]
            ret = [ x for x in ret if x != "!!END!!@"]
            

            if sentence_mode:
                return (' '.join(ret))
            return ret
        

def mse(imageA, imageB): #used by compare_image()
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    #NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
          
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def compare_images(input_image, list_of_images,method): #used by find_layout()
# compute the mean squared error and structural similarity
# index for the images
    diff = []
    for image in list_of_images:
        if method == "SSIM":
            diff.append(ssim(input_image, image))
        elif method == "MSE":
            diff.append(mse(input_image, image))
        else:
            print("Method should be SSIM or MSE")
            return -1
    return diff

def process_image(list1,base_resolution): #used by find_layout()
    resized = []
          
    for item in list1:
        # convert the images to grayscale
        black_and_white = (cv2.cvtColor(item, cv2.COLOR_BGR2GRAY))
        # black_and_white = item
        # scale_percent = 25 # percent of original size
        # width = int(item.shape[1] * scale_percent / 100)
        # height = int(item.shape[0] * scale_percent / 100)
        dim = base_resolution
        # resize image
        
        resized.append(cv2.resize(black_and_white, dim, interpolation = cv2.INTER_AREA))

    return resized
######################

# def find_layout(image_to_check, template_folder, base_resolution = (300,400), method = "SSIM"):
#         images_path = glob.glob(os.path.join(os.getcwd(),template_folder,"*.jpg")) 
#         images = []
#         for item in images_path:
#                 img = cv2.imread(item)
#                 struct = assembler(image=img)
#                 images.append( struct )


#         resized_images = process_image(images,base_resolution)

#         # for test in resized_images:
#         #     cv2.imshow("test",test)
#         #     cv2.waitKey()

#         case = image_to_check
#         case = assembler(case)



#         black_and_white=cv2.cvtColor(case, cv2.COLOR_BGR2GRAY)
#         base = cv2.resize(black_and_white, base_resolution , interpolation = cv2.INTER_AREA)
    


#         compared = compare_images(base,resized_images,method)

#         #new method
#         what_the_fuck , base_number_of_elements = shape_counter(cv2.cvtColor(base,cv2.COLOR_GRAY2RGB))

#         cv2.imshow("test",what_the_fuck)
#         cv2.waitKey()
#         exit()

#         for i in resized_images:
#             print(i.shape)
#             i = cv2.cvtColor(i,cv2.COLOR_GRAY2RGB)
            
#             _ , shape_elements = shape_counter(i)
#             print(shape_elements)
#             if base_number_of_elements == shape_elements:
#                 print("hello")
#                 print(images_path[resized_images.index(i)])

#         exit()

#         path = images_path[compared.index(max(compared))]
#         file_name = os.path.basename(path)
#         layout = file_name.split('.')[0]
        
#         return (layout)



def find_layout(image_to_check, template_folder, base_resolution = (300,400), method = "SSIM", get_struct = False):

        images_path = glob.glob(os.path.join(os.getcwd(),template_folder,"*.jpg")) 
        images = []
        for item in images_path:
                img = cv2.imread(item)
                struct = assembler(image=img) if get_struct is True else img
                images.append( struct )



        resized_images = process_image(images,base_resolution)



        case = image_to_check.copy()

        case = assembler(case) if get_struct is True else case

        black_and_white=cv2.cvtColor(case, cv2.COLOR_BGR2GRAY)
        base = cv2.resize(black_and_white, base_resolution , interpolation = cv2.INTER_AREA)

        compared = compare_images(base,resized_images,method)

        compared_sorted = sorted(compared,reverse=True)

        path_sorted = []
        for each in compared_sorted:
                    temp = images_path[compared.index(each)]
                    path_sorted.append(temp)

        path = path_sorted[0]



        compared_mse = compare_images(base,resized_images,"MSE")
        compared_mse_sorted = sorted(compared_mse)

        path_mse = []
        for each in compared_mse_sorted:
                    temp = images_path[compared_mse.index(each)]
                    path_mse.append(temp)


        #new method
        # base_number_of_elements = layout_estimator(case)
        #cv2.imshow("s",im)
        #cv2.imwrite("vvv.jpg",im)
        # cv2.waitKey()
        # print(base_number_of_elements)
        # exit()

        # for i in resized_images:
        #     print(i.shape)
        #     i = cv2.cvtColor(i,cv2.COLOR_GRAY2RGB)
            
        #     _ , shape_elements = shape_counter(i)
        #     print(shape_elements)
        #     if base_number_of_elements == shape_elements:
        #         print("hello")
        #         print(images_path[resized_images.index(i)])

        # exit()

        # path = images_path[compared.index(max(compared))]

        file_name = os.path.basename(path)
        layout = file_name.split('.')[0]
        
        return (layout)

###################


def find_layout_beta(image_to_check, template_folder, base_resolution = (300,400), method = "SSIM", get_struct = False):

        images_path = glob.glob(os.path.join(os.getcwd(),template_folder,"**","*.jpg"),recursive=True) 
        images = []
        for item in images_path:
                img = cv2.resize(cv2.imread(item), base_resolution , interpolation = cv2.INTER_AREA)
                struct = assembler(image=img) if get_struct is True else img
                images.append( struct )


        resized_images = process_image(images,base_resolution)


        case = image_to_check.copy()

        case = assembler(case) if get_struct is True else case

        black_and_white=cv2.cvtColor(case, cv2.COLOR_BGR2GRAY)
        base = cv2.resize(black_and_white, base_resolution , interpolation = cv2.INTER_AREA)

        compared = compare_images(base,resized_images,method)

        compared_sorted = sorted(compared,reverse=True)

        path_sorted = []
        for each in compared_sorted:
                    temp = images_path[compared.index(each)]
                    path_sorted.append(temp)

        path = path_sorted[0]

        
        #for the test
        # print ("Similarity index ",path_sorted)
        # print(" similarity number : ",compared_sorted)


        # compared_mse = compare_images(base,resized_images,"MSE")
        # compared_mse_sorted = sorted(compared_mse)

        # path_mse = []
        # for each in compared_mse_sorted:
        #             temp = images_path[compared_mse.index(each)]
        #             path_mse.append(temp)


        #new method
        # base_number_of_elements = layout_estimator(case)
        #cv2.imshow("s",im)
        #cv2.imwrite("vvv.jpg",im)
        # cv2.waitKey()
        # print(base_number_of_elements)
        # exit()

        # for i in resized_images:
        #     print(i.shape)
        #     i = cv2.cvtColor(i,cv2.COLOR_GRAY2RGB)
            
        #     _ , shape_elements = shape_counter(i)
        #     print(shape_elements)
        #     if base_number_of_elements == shape_elements:
        #         print("hello")
        #         print(images_path[resized_images.index(i)])

        # exit()

        # path = images_path[compared.index(max(compared))]

        # file_name = os.path.basename(path)
        # name  =  os.path.dirname(path)
        layout = os.path.basename(os.path.dirname(path))

        
        return (layout)


#####################


def find_layout_beta2(image_to_check, template_folder, base_resolution = (300,400), method = "SSIM", get_struct = False):

        images_path = glob.glob(os.path.join(os.getcwd(),template_folder,"**","*.jpg"),recursive=True) 
        images = []
        for item in images_path:
                img = cv2.imread(item)
                struct = assembler(image=img) if get_struct is True else img
                images.append( struct )



        resized_images = process_image(images,base_resolution)



        case = image_to_check.copy()

        case = assembler(case) if get_struct is True else case

        black_and_white=cv2.cvtColor(case, cv2.COLOR_BGR2GRAY)
        base = cv2.resize(black_and_white, base_resolution , interpolation = cv2.INTER_AREA)

        compared = compare_images(base,resized_images,method)

        compared_sorted = sorted(compared,reverse=True)

        path_sorted = []
        for each in compared_sorted:
                    temp = images_path[compared.index(each)]
                    path_sorted.append(temp)

        vote_list = []
        for counter in range(5):
            vote = os.path.basename(os.path.dirname(path_sorted[counter]))
            vote_list.append(int(vote))
        print(vote_list)
        layout = max(set(vote_list), key = vote_list.count)
        
        return (layout)


####################
def uncertain_detection(image_case, certaintity_percentage=30 , output = "checked"):
        image = image_case
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_data(rgb, lang="eng+ces" ,output_type=Output.DICT)

        img = Image.open(image_case)
        draw  = ImageDraw.Draw(img)

        defect_list =[]

        uncertain_area = {
                "text" : None,
                "confidence" : None,
                "down_left" : None,
                "up_left" : None,
                "down_right" : None,
                "up_right" : None


            }

        # loop over each of the individual text localizations
        for i in range(0, len(results["text"])):
            # extract the bounding box coordinates of the text region from
            # the current result
            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]

            # extract the OCR text itself along with the confidence of the
            # text localization
            text = results["text"][i]
            conf = int(results["conf"][i])


           

            # filter out weak confidence text localizations
            if (0 < conf < certaintity_percentage) and results["text"][i] != "":
                # display the confidence and text to our terminal
                print("Confidence: {}".format(conf))
                print("Text: {}".format(text))
                print("")
                uncertain_area["text"] = text
                uncertain_area["confidence"] = conf
                uncertain_area["down_left"] = (x,y)
                uncertain_area["up_left"] = (x,y+h)
                uncertain_area["down_right"] = (x+w,y)
                uncertain_area["up_right"] = (x+w,y+h)

                defect_list.append(uncertain_area.copy())
                # using OpenCV, then draw a bounding box around the text along
                # with the text itself
                #cv2.rectangle(image, uncertain_area["down_left"], uncertain_area["up_right"], (0, 0, 255), 2)
                #cv2.putText(image, text, (x, y ), cv2.FONT_HERSHEY_SIMPLEX,1.2, (0, 255, 0), 3)

                #configuration
                # font_size=15
                # w = width
                # h = height
                # back_ground_color=(255,255,255)
                # font_size=36
                # font_color=(0,255,0)
                # unicode_text = text


                # unicode_font = ImageFont.truetype("DejaVuSans.ttf", font_size)
                # draw.text ( (x,y), unicode_text, font=unicode_font, fill=font_color )
                # draw.rectangle( [ (x, y+h),(x+w,y+(2*h))    ], fill="Black")
                draw.rectangle( [ (x, y),(x+w,y+h )   ], outline="Red")

                myFont = ImageFont.truetype('DejaVuSans.ttf', 40)
                draw.text((x, y+h), text, font=myFont, fill =(255, 0, 0))

        # show the output image
        # cv2.imshow("Image", image)
        # cv2.imwrite(str(os.path.basename(image_case)), image)
        # cv2.waitKey(0)
        # img = np.array(img_pil)
        # cv2.imwrite("text.jpg",img)
        if not os.path.exists(output):
            os.makedirs(output)
        img.save(os.path.join(output, str(os.path.basename(image_case))))
        return defect_list


def region_of_interest(image, starting_point = (0,0), area = (0,0)):
    crop_img = image[starting_point[1]:starting_point[1]+area[1], starting_point[0]:starting_point[0]+area[0]]
    return crop_img


def semantic_photo_match(sub_image,parent_image):
          roi = sub_image
          raw_sub_image = roi #used in comapre below
          roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
          roi = cv2.Canny(roi, 50, 200)
          (tH, tW) = roi.shape[:2]
          #cv2.imshow("Template", template)

          # loop over the images to find the template in
                    # load the image, convert it to grayscale, and initialize the
                    # bookkeeping variable to keep track of the matched region
          image = parent_image
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
          found = None
                    # loop over the scales of the image
          for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                              # resize the image according to the scale, and keep track
                              # of the ratio of the resizing
                              resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
                              r = gray.shape[1] / float(resized.shape[1])

                              # if the resized image is smaller than the template, then break
                              # from the loop
                              if resized.shape[0] < tH or resized.shape[1] < tW:
                                        break

                              # detect edges in the resized, grayscale image and apply template
                              # matching to find the template in the image
                              edged = cv2.Canny(resized, 50, 200)
                              result = cv2.matchTemplate(edged, roi, cv2.TM_CCOEFF)
                              (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

                              # if we have found a new maximum correlation value, then update
                              # the bookkeeping variable
                              if found is None or maxVal > found[0]:
                                        found = (maxVal, maxLoc, r)
          # unpack the bookkeeping varaible and compute the (x, y) coordinates
          # of the bounding box based on the resized ratio
          if found is None:
              print("Pattern image has invalid scale")
              return -1
          (_, maxLoc, r) = found
          (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
          (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
    # draw a bounding box around the detected result and display the image
    # cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
          cut = region_of_interest(image,starting_point=(startX,startY),area=((endX-startX),(endY-startY)))
          cut_scaled = cv2.resize(cut, (raw_sub_image.shape[1],raw_sub_image.shape[0]), interpolation = cv2.INTER_AREA) 
          cut_scaled =cv2.cvtColor(cut_scaled, cv2.COLOR_BGR2GRAY)

          #print(cut_scaled.shape)
          compared = compare_images(input_image=cv2.cvtColor(raw_sub_image, cv2.COLOR_BGR2GRAY),
          list_of_images=[cut_scaled],method="SSIM") #value cut should be send as a list item
          print(compared[0])
          if compared[0] > 0.8:
              cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
              return(image)
          else:
              return None

def barcode_reader(image):
    barcodes = pyzbar.decode(image.copy())
    # loop over the detected barcodes
    #return barcodes
    list_of_barcodes = []
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        # (x, y, w, h) = barcode.rect
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 20)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        list_of_barcodes.append([barcodeType,barcodeData])

        # draw the barcode data and barcode type on the image
        #text = "{} ({})".format(barcodeData, barcodeType)
        #cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 20)

    # show the output image
    return list_of_barcodes
    #return image

def shape_extract(image,shapes=['rectangle','square']):
	# load the image and resize it to a smaller factor so that
	# the shapes can be approximated better
	#image = cv2.imread(path)
	#adjusted = cv2.convertScaleAbs(image, alpha=2, beta=0)
	imagem = cv2.bitwise_not(image)
	resized = imutils.resize(imagem, width=int(image.shape[1]/2))
	ratio = image.shape[0] / float(resized.shape[0])
	print(ratio)
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	sd = ShapeDetector()

	# loop over the contours
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		if M["m00"] == 0:
			continue
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		shape = sd.detect(c)
		if shape not in shapes:
			continue # we only want the valid shapes
		print(shape)
		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		cv2.drawContours(image, [c], -1, (255, 0, 0), 10)
		#print(c)
		#break

		# show the output image
	return image

def shape_counter(image,shapes=['rectangle']):
	# load the image and resize it to a smaller factor so that
	# the shapes can be approximated better
	#image = cv2.imread(path)
	#adjusted = cv2.convertScaleAbs(image, alpha=2, beta=0)
	imagem = cv2.bitwise_not(image)
	resized = imutils.resize(imagem, width=2066)
	ratio = image.shape[0] / float(resized.shape[0])
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	sd = ShapeDetector()
	counter = 0
	# loop over the contours
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		M = cv2.moments(c)
		if M["m00"] == 0:
			continue
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		shape = sd.detect(c)
		if shape not in shapes:
			continue # we only want the valid shapes
		# multiply the contour (x, y)-coordinates by the resize ratio,
		# then draw the contours and the name of the shape on the image
		c = c.astype("float")
		c *= ratio
		c = c.astype("int")
		cv2.drawContours(image, [c], -1, (255, 0, 0), 2)

		counter = counter +1 

	return image , counter



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

def remove_borders(image,thresh_line = 10 ):
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

    return image

def layout_estimator(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]


            
    return len(cnts)




def layout_rate(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image.shape[1]/3),1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    counter = 0
    for c in cnts:
        counter+=1
        cv2.drawContours(image, [c], -1, (36,255,12), 2)

    return image , counter


def rectangler(image):
    # Load image, grayscale, Gaussian blur, Otsu's threshold]
    #image = cv2.bitwise_not(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(image.shape[1]/300),int(image.shape[0]/300)))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 20)

    return image


# data = cv2.imread("layouts/img1.jpg")
# img = assembler(data)
# rec = rectangler(img)
# cv2.imwrite("zzz.jpg",rec)



def image_convert_file(path_in , path_out='jpg_converted', absolute_path = False , prefered_dpi = 500 , rotatation_fix = False):
    '''
    @param path_in: folder indicating pdf files 
    @param path_out: folder indicating output image files ( this folder sits inside input file ) 
    @param absolute_path: if sets TRUE, paths out image file will return in absolute mode
    @param prefered_dpi: the prefered dpi of output image files
    
    '''
    cwd = os.getcwd() #getting curent working directory

    # list_pdf = glob.glob(os.path.join(cwd,path_in,"*.pdf")) #getting the list of pdf files inside the input folder
    # list_PDF = glob.glob(os.path.join(cwd,path_in,"*.PDF")) #getting the list of pdf files inside the input folder
    # list = list_pdf+list_PDF

    #path_out = os.path.join(path_in,path_out) #where to save images, (a filder inside input folder)
    
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    output_list = [] # list of addreses of image files which obtained from pdfs
    
    pdf_list =[]
    pdf_list.append(path_in)

    for pdf_file in pdf_list:
        pages = convert_from_path(pdf_file, dpi=prefered_dpi)
        for index , page in enumerate(pages): #make a loop if a pdf file has multiple pages
            save_path =    os.path.join(path_out,os.path.basename(pdf_file))
            if len(pages) > 1: # add an index at the end of each file name if pdf has multiple pages
                save_path = save_path + "_"+str(index+1)
            save_path = save_path +".jpg"
            if absolute_path == True: #If user wanted absolute path of image output files
                save_path = os.path.join(cwd,save_path)
            
            #append to the list and save the file
            output_list.append(save_path)
            if rotatation_fix == True:
                page = Image.fromarray(rotate(page,major=False))
            page.save(save_path, 'JPEG')
    
    if len(pages) > 1 :
        end_result = output_list
    elif len(pages) == 1:
        end_result = output_list[0]
    else:
        end_result = -1

    return (len(pages),end_result)



def watermark_remove(image):
    # Load the image
    img = image.copy()

    # Convert the image to grayscale
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Make a copy of the grayscale image
    bg = gr.copy()

    # Apply morphological transformations
    for i in range(5):
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                            (2 * i + 1, 2 * i + 1))
        bg = cv2.morphologyEx(bg, cv2.MORPH_CLOSE, kernel2)
        bg = cv2.morphologyEx(bg, cv2.MORPH_OPEN, kernel2)

    # Subtract the grayscale image from its processed copy
    dif = cv2.subtract(bg, gr)

    # Apply thresholding
    bw = cv2.threshold(dif, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    dark = cv2.threshold(bg, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Extract pixels in the dark region
    darkpix = gr[np.where(dark > 0)]

    # Threshold the dark region to get the darker pixels inside it
    darkpix = cv2.threshold(darkpix, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Paste the extracted darker pixels in the watermark region
    bw[np.where(dark > 0)] = darkpix.T

    bw = cv2.cvtColor(bw,cv2.COLOR_GRAY2RGB)
    
    return bw

def num_refine(text_list):
    text_list = [ item.replace(",",".") for item in text_list ]


    for index, item in enumerate(text_list):
        if item != "":
            
            try: 
                if isinstance(int(item), int):
                        text_list[index:index+2] = ([''.join(text_list[index:index+2])]) if isinstance(float(text_list[index+1]),float) else item
            except:
                pass
    return (list(filter(None,text_list)))

def postal_code_old(text_list):
    #text_list = [ item.replace(",",".") for item in text_list ]
    print("INSIDE POST ",text_list)


    for index, item in enumerate(text_list):

        if item != "":
            
            try: 
                if isinstance(int(item), int) and isinstance(int(text_list[index+1]),int) and len(text_list[index]) == 3 and len(text_list[index]) == 2:
                    text_list[index:index+2] = ([''.join(text_list[index:index+2])])
            except:
                pass
    return (list(filter(None,text_list)))


def image_combiner(list_of_image, axis = 0):
    
    combined = cv2.imread(list_of_image[0])

    images = list_of_image[1:]
    for image in images:
        data = cv2.imread(image)
        combined = np.concatenate(((combined),(data)), axis = axis)

    return combined

def semi_colon_refine(text_list):

    for index, item in enumerate(text_list):
        if item != "":
            
            try: 
                if text_list[index+1] == ":":
                        text_list[index:index+2] = ([''.join(text_list[index:index+2])])
            except:
                pass
    return (text_list)



def get_distance(item1,item2,text_list,x_list,y_list,w_list=[],h_list=[],consider_size = False ):

    try:
        item1_x = x_list[text_list.index(item1)]
        item1_y = y_list[text_list.index(item1)]

        item2_x = x_list[text_list.index(item2)]
        item2_y = y_list[text_list.index(item2)]


        x_diff = (item2_x - item1_x) if consider_size is False else (item2_x - (item1_x + w_list[text_list.index(item1)])  )
        y_diff = (item2_y - item1_y) if consider_size is False else (item2_y - (item1_y + h_list[text_list.index(item1)])  )
        

        print ("item 1 : ",item1_x,item1_y)
        print("item 2 : ",item2_x,item2_y)
        print("w , h",(w_list[text_list.index(item1)]),(h_list[text_list.index(item1)]))
    except:
        return -1

    return [x_diff,y_diff]

def get_postition(item,text_list,x_list,y_list):#,w_list,h_list,consider_size = False ):
    try:
        item_x = x_list[text_list.index(item)]
        item_y = y_list[text_list.index(item)]
    except:
        return -1

    return [item_x,item_y]

def line_split(text_list,x_list,y_list,thresh = 20 , axis = 0):
    line_list = []
    previous = y_list[0] if axis == 0 else x_list[0]

    temp_list = []

    for index,word in enumerate(text_list):
        pos = y_list[index] if axis == 0 else x_list[index]
    
        if (pos-previous) > thresh:
            line_list.append(temp_list.copy())
            temp_list.clear()
        temp_list.append(word)
        previous = pos
    
    if len(temp_list) > 0: #buffer exist because of last line
        line_list.append(temp_list.copy())

        
    return line_list

def postal_code(text,post_code_or_city):
    text_list = text.copy()

    for index, item in enumerate(text_list):
        if item != "":
            
            try:
                num1 = isinstance(int(item), int)
            except:
                num1 = False
            try:
                num2 = isinstance(int(text_list[index+1]),int)
            except:
                num2 = False
            try: 
                # print(num1,num2,len(text_list[index]),len(text_list[index+1]))
                if num1 and num2 and len(text_list[index]) == 3 and len(text_list[index+1]) == 2:
                    text_list[index:index+2] = ([''.join(text_list[index:index+2])])
            except:
                pass
            
            try:
                thresh = 5
                if text_list[index][0] == "0":
                    thresh=4

                postcode = int(text_list[index])
                
                if len(str(postcode)) == thresh:
                    if post_code_or_city == 0:
                        return [str(postcode)] if thresh ==5 else ["0"+str(postcode)]
                    elif post_code_or_city == 1:
                        return [text_list[index+1]]

                        
            except:
                pass
            
    return -1