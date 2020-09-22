import os, glob,json, difflib,pytesseract,cv2,imutils
from pdf2image import convert_from_path
from pytesseract import Output
from skimage.metrics import structural_similarity as ssim
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pyzbar import pyzbar



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


def image_convert(path_in , path_out='jpg_converted', absolute_path = False , prefered_dpi = 500):
    '''
    @param path_in: folder indicating pdf files 
    @param path_out: folder indicating output image files ( this folder sits inside input file ) 
    @param absolute_path: if sets TRUE, paths out image file will return in absolute mode
    @param prefered_dpi: the prefered dpi of output image files
    
    '''
    cwd = os.getcwd() #getting curent woeking directory

    list = glob.glob(os.path.join(cwd,path_in,"*.pdf")) #getting the list of pdf files inside the input folder
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
            page.save(save_path, 'JPEG')

    return (output_list)



def data_extract(image_list, min_conf = 0 , tesserect_config="--psm 1", fuzzy_match = False , guess_list=[] , to_jason = False):
    set_environment() # set the folder where trained models for tesserect exist the default is the "models" folder
    word_list=[]
    for img in image_list:
        # load the input image, convert it from BGR to RGB channel ordering,
        # and use Tesseract to localize each area of text in the input image
        image = cv2.imread(img)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pytesseract.image_to_data(rgb,lang='eng+ces', config=tesserect_config, output_type=Output.DICT)
        results["file_name"] = str(img) #adding file name of the current image to the dict
        for i in range(0, len(results["text"])):
            
            # extract the bounding box coordinates of the text region from
                  # the current result
            # IF LATER WE NEED TO USE THE BOUNDING BOXES
            x = results["left"][i]
            y = results["top"][i]
            w = results["width"][i]
            h = results["height"][i]
                  # extract the OCR text itself along with the confidence of the
            #text localization

            #If fuzzy match is enabled, it will change the word to the closest match provided in guess_list
            if fuzzy_match==True and results["conf"][i] < 70: #fuzzy match only for uncertain words
                corrections = difflib.get_close_matches(results["text"][i], guess_list)
                if len(corrections) > 0:
                    results["text"][i] = corrections[0]

            
            text = results["text"][i]
           
            conf = int(results["conf"][i])
            # filter out weak confidence text localizations
            if conf > min_conf:
                            # display the confidence and text to our terminal
                print("Confidence: {}".format(conf))
                print("Text: {}".format(text))
                print("")
        #results is a dict form, we can send the dict or json, but in this case jason
        if to_jason == True:
            results = json.dumps(results, indent=4, ensure_ascii=False)
        #json_list.append(result_json)
        word_list.append(results)
    return(word_list)


def hot_word(list_of_words,stop_word,distance = 1): #returns the next and previous item in a list in the form of dictionay
    l = len(list_of_words)

    for index, obj in enumerate(list_of_words):
        bounding = {
            "previous" : None,
            "next" : None


        }
        if obj == stop_word:
            if index < (l - 1):
                bounding["next"] = list_of_words[index + distance]
            if index > 0:
                bounding["previous"] = list_of_words[index - distance]
                
            return bounding 


def crop_sentence(sentence_list, start , stop, sentence_mode = False ):
    '''
    crop a subsentence between start and ending poing
    returns a list of words, the starting and ending point are not included
    if sentence_mode is True, it will return a sentence in the form of string 
    rather than a list
    '''
    crop_range = []
    pick_words=False

    for item in sentence_list:
        if item == start:
            pick_words = True


        if pick_words==True:
            crop_range.append(item)

        
        if item == stop:
            if sentence_mode:
                return (' '.join(crop_range[1:-1]))
            return crop_range[1:-1]
        

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
          
    for index ,item in enumerate(list1):
        # convert the images to grayscale
        black_and_white = (cv2.cvtColor(item, cv2.COLOR_BGR2GRAY))
        # scale_percent = 25 # percent of original size
        # width = int(item.shape[1] * scale_percent / 100)
        # height = int(item.shape[0] * scale_percent / 100)
        dim = base_resolution
        # resize image
        resized.append(cv2.resize(black_and_white, dim, interpolation = cv2.INTER_AREA))
    return resized
######################

def find_layout(image_to_check, template_folder, base_resolution = (300,400), method = "SSIM"):
        images_path = glob.glob(os.path.join(os.getcwd(),template_folder,"*.jpg")) 
        images = []
        for item in images_path:
                images.append(cv2.imread(item))


        resized_images = process_image(images,base_resolution)

        case = cv2.imread(image_to_check)
        black_and_white=cv2.cvtColor(case, cv2.COLOR_BGR2GRAY)

        base = cv2.resize(black_and_white, base_resolution , interpolation = cv2.INTER_AREA)

        compared = compare_images(base,resized_images,method)

        return (images_path[compared.index(max(compared))])

def uncertain_detection(image_case, certaintity_percentage=30 , output = "checked"):
        image = cv2.imread(image_case)
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
          roi = cv2.imread(sub_image)
          raw_sub_image = roi #used in comapre below
          roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
          roi = cv2.Canny(roi, 50, 200)
          (tH, tW) = roi.shape[:2]
          #cv2.imshow("Template", template)

          # loop over the images to find the template in
                    # load the image, convert it to grayscale, and initialize the
                    # bookkeeping variable to keep track of the matched region
          image = cv2.imread(parent_image)
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

def barcode_reader(path):
    image = cv2.imread(path)
    barcodes = pyzbar.decode(image)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)

    # show the output image
    return image

def shape_extract(path,shapes=['rectangle','square']):
	# load the image and resize it to a smaller factor so that
	# the shapes can be approximated better
	image = cv2.imread(path)
	#adjusted = cv2.convertScaleAbs(image, alpha=2, beta=0)
	imagem = cv2.bitwise_not(image)
	resized = imutils.resize(imagem, width=2066)
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

def text_remover(image):
        img = cv2.imread(image)
        mask = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)[1][:,:,0]
        dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
        #crosses = mask[235:267,290:320] | mask[233:265,288:318]
        #mask[235:267,290:318] = crosses
        dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
        return dst
