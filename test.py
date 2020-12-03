from utb.beta import data_extract,find_layout,assembler,shape_extract,shape_counter,hot_word,image_convert_file
from utb.beta import segmentizer,crop_sentence,splitter,barcode_reader,watermark_remove,num_refine,image_combiner
from utb.beta import semi_colon_refine,set_environment,postal_code,remove_borders
from utb.config import segmap,coordinates
import cv2,numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=False,
	help="path to pdf file")

args = vars(ap.parse_args())

def confidence_calculator(list_of_words,list_of_conf,sentence,threshold = 50):
        counter = 0
        sum_con = 0
        for word in sentence:
                con = list_of_conf[list_of_words.index(word)]
                sum_con = sum_con + con
                counter = counter + 1
        if counter == 0 :
                print("CHECK THE PAGE!")
                
        confident_number = int(sum_con/counter) if counter != 0 else None

        if confident_number >= threshold:
                tag = 1
        else:
                tag = 0
        
        return tag,confident_number

def check_dobropis(list_in):
        list_in = [x.lower() for x in list_in]
        if "opravný" in list_in:
                return ["1"]
        else:
                return ["0"]


def same_line(key,list_of_words,list_of_positions):
        distance = 0
        index = list_of_words.index(key)

        cut_word_list = list_of_words[index:]
        cut_position_list = list_of_positions[index:]

        
        prev_pos = cut_position_list[0]
        
        for pos in (cut_position_list):

                if abs( pos - prev_pos) < int(img.shape[0]/116):
                        # print("GOLDEN ",int(img.shape[0]/116))
                        distance = distance + 1
                else:
                        break
                
                prev_pos = pos

        return distance 

def multi_line(key,list_of_words,list_of_positions,which_line=0):
        index = list_of_words.index(key)

        cut_word_list = list_of_words[index:]
        cut_position_list = list_of_positions[index:]

        
        prev_pos = cut_position_list[0]
        distance = 0
        counter = 0
        start_key = key
        for word, pos in  zip(cut_word_list,cut_position_list):

                if abs( pos - prev_pos) > int(img.shape[0]/116): #line break
                        counter = counter +1 
                        start_key = word
                        distance = same_line(word,cut_word_list,cut_position_list) 
                else:
                        start_key = word
                if counter == which_line:
                        break
                prev_pos = pos

        start_key = cut_word_list[cut_word_list.index(word)-1]
        return start_key,distance

def find_break(key,list_of_words,list_of_positions,jump=2):
        index = list_of_words.index(key)

        cut_word_list = list_of_words[index:]
        cut_position_list = list_of_positions[index:]

        prev_pos = cut_position_list[0]
        distance = 0
        diff = [0]
        for counter,pos in  enumerate(cut_position_list):
                delta_y = abs(pos - prev_pos)

                distance = distance + 1
                if len(diff)>0:
                        if delta_y > 2 * (sum(diff)/len(diff)):
                                break
                if delta_y > 50: #line break
                        diff.append(delta_y)   

                prev_pos = pos
                        
                # if counter+1 == len(cut_position_list):
                #         return len(cut_position_list)
        return distance

def find_split(key,text_list,y_list,x_list,thresh = 20):

    index = text_list.index(key) 
    print(key," key ")
    cut_word_list = text_list[index+1:]
    cut_position_list = y_list[index+1:]
    cut_x_list = x_list[index+1:]


    #print(cut_word_list," cut word list ")
    previous = cut_position_list[0]
    x_shift = cut_x_list[0]

    distance = 0
    
    gap = False
    temp_list = []
    line_list = []
    pos_thresh = []
    x_thresh = []
    for x,pos,word in zip(cut_x_list,cut_position_list,cut_word_list):
    
        if (pos-previous) > thresh:
            line_list.append(temp_list.copy())
            temp_list.clear()
            pos_thresh.append(pos-previous)
            thresh = sum(pos_thresh)/len(pos_thresh)
            x_thresh.append(x)
            x_shift = sum(x_thresh)/len(x_thresh)
        #     print("new thresh ",thresh)
        #     print("on word ",word)

        # print("thesh ",thresh)
        # print("dif ",pos-previous)
        if (pos-previous) > (1.4*thresh) :#or ":" in word:#x < x_shift:
                print("--------- ",word)
                gap = True
                break
        
        temp_list.append(word)

        previous = pos


    if len(temp_list) > 0 and not gap: #buffer exist because of last line
        line_list.append(temp_list.copy())
    
    print(line_list," inam line")
    for item in line_list:
            for word in item:
                    distance = distance + 1

    return distance





        #         if abs( pos - prev_pos) > 50: #line break
        #                 counter = counter +1 
        #                 start_key = word
        #                 distance = same_line(word,cut_word_list,cut_position_list) 
        #         else:
        #                 start_key = word
        #         if counter == which_line:
        #                 break
        #         prev_pos = pos

        # start_key = cut_word_list[cut_word_list.index(word)-1]
        # return start_key,distance

def check_num(string):
        string = ''.join(string)
        try:
                if isinstance(int(string),int):
                        return [string]

        except:
                return None

def remove_noise(list_in,threshold = 1):
        denoised = [item for item in list_in if len(item)>threshold]
        return denoised

def vatrate_num(lst,num):
    num = str(num)
    for index, rate in enumerate(lst):
        if "%" in rate and lst[index-1] == "DPH":
            if num in rate:
                return [num]
    return None

def vatrate_num_plain(lst,num):
#     print(" I AM RUNNING ",lst,num)
    num = str(num)
    for rate in (lst):
        if num+"%" == rate:
                return [num]
    return None

def fix_percentage(thelist):
    for index,item in enumerate(thelist):
        if item == "%":
            thelist[index-1]=thelist[index-1]+thelist[index]
            thelist.pop(index)
    return thelist

def exVat(word_list,num):
    try:
        for index,item in enumerate(word_list):
            if item == "DPH":
                if word_list[index+1]== str(num)+"%":
                    return word_list[:index]
        return None
    except:
        return None

def TrVAT_check(list_in):
        for index,item in enumerate(list_in):
                if item == "odvede" and ("zákazník" in list_in[index+1]):
                        return ["1"]
        return ["0"]



def preprocessor_handler(triggers,list_in):
        list_of_actions = []

        if isinstance(triggers, str):
            list_of_actions.append(triggers)
        elif isinstance(triggers, list):
            list_of_actions = triggers
            if isinstance(triggers[0], int) and isinstance(triggers[1], str) and len(triggers) == 2 :
                temp_list = []
                for item in range(triggers[0]):
                    temp_list.append(triggers[1])
                list_of_actions.clear()
                list_of_actions = temp_list
                


        for trigger in list_of_actions:
                if trigger == "_num_":
                        list_in = num_refine(list_in)
                elif trigger == "_reverse_":
                        list_in = list_in.reverse()
                elif trigger == "check_num":
                        list_in = check_num(list_in)
                elif trigger == "fix_percentage":
                        list_in = fix_percentage(list_in)
                elif "_denoise_" == trigger:
                        list_in = remove_noise(list_in)


        return list_in

def postprocessor_handler(triggers,list_in):

        list_of_actions = []

        if isinstance(triggers, str):
            list_of_actions.append(triggers)

        elif isinstance(triggers, list):
            list_of_actions = triggers

            if isinstance(triggers[0], int) and isinstance(triggers[1], str) and len(triggers) == 2 :
                temp_list = []
                for item in range(triggers[0]):
                    temp_list.append(triggers[1])
                list_of_actions.clear()
                list_of_actions = temp_list
                


        for trigger in list_of_actions:
                if trigger == "_postcode_":
                        
                        list_in = postal_code(list_in,0)
                if trigger == "_cityname_":
                        list_in = postal_code(list_in,1)
                elif trigger == "check_num":
                        list_in = check_num(list_in)
                elif trigger == "_dobropis_":
                        list_in = check_dobropis(list_in)
                elif "VATRat" in trigger:
                        try:
                                rate = int(trigger[-2:])
                        except:
                                rate = int(trigger[-1:])
                        
                        #print("RATE ",rate)
                        #print("LIST IN ",list_in)
                        list_in = vatrate_num(list_in,rate)

                elif  "existVAT" in trigger:
                        try:
                                rate = int(trigger[-2:])
                        except:
                                rate = int(trigger[-1:])
                        
                        #print("RATE ",rate)
                        #print("LIST IN ",list_in)
                        list_in = vatrate_num_plain(list_in,rate)

                elif "ExVat" in trigger:
                        try:
                                rate = int(trigger[-2:])
                        except:
                                rate = int(trigger[-1:])
                        
                        #print("RATE ",rate)
                        #print("LIST IN ",list_in)
                        list_in = exVat(list_in,rate)

                elif "TrVAT_check" in trigger:
                        list_in = TrVAT_check(list_in)

                elif trigger == "_denoise_":
                        list_in = remove_noise(list_in)

        return list_in


safe = True
save_logs_into_file = True
set_environment()

#ABRA
#input_file = "/home/non/KeenData/New Layouts/Faktury k testování/ABRA/Kombinace přenesená DPH + ne/VF1_0015_2020.pdf"              
# input_file = "/home/non/KeenData/New Layouts/Faktury k testování/ABRA/Kombinace přenesená DPH + ne/3_20.pdf"   
# Phoda           
# input_file = "/home/non/KeenData/zip/Pohoda/Kombinace přenesená DPH + ne/BAY20100417030.pdf"
#MRP
#input_file = "/home/non/KeenData/zip/Obdobné layouty MONEY S4, S5/Trénovací/BAY20101109360.pdf"
#input_file = "/home/non/KeenData/zip/Money S3/Kombinace přenesená DPH + ne/BAY20100713080.pdf"
#input_file = "/home/non/KeenData/zip/MRP/Kombinace DPH +ne DPH/BAY20101019220.pdf"
#input_file = "/home/non/KeenData/New Layouts/Faktury k testování/ABRA/Nedaňový doklad (neplátce)/AF Hla 83.pdf"


# #TEST SAMPLES OF POWER BI
#input_file = "/home/non/201125131132392-22320062918022.pdf"
#input_file = "/home/non/KeenData/zip/MRP/Daňový doklad/22320062918022.pdf"

# import glob
# mydir = "/home/non/work/proSinu/layout5/sada-a-mix/"
# file_list = glob.glob(mydir + r"*.pdf")


# print(len(file_list)," PDF files has been found")
# correct_list = []
# wrong_list = []
# for item in file_list:
#         number_of_pages,path = image_convert_file(path_in=item,absolute_path=True,rotatation_fix=True)
#         cat = "MasterPool" #KEEDDAT for new style of
#         if number_of_pages > 1:
#                 img = image_combiner([path[0],path[-1]])
#         else:
#                 img = cv2.imread(path)


#         from utb.beta import find_layout_beta
#         layout_number = int(find_layout_beta(img,template_folder=cat,get_struct=False))

#         #FOR THE SAKE OF SPEED CORRECT IT LATER
#         # layout_number = int(find_layout(img,template_folder=cat,get_struct=False))
#         # layout_number = 5

#         print("File name: ",item)
#         print("the detected layout: ", layout_number)
#         if (layout_number == 4 ):
#                 correct_list.append(item)
#         else:
#                 temp_dict = {"name": item , "layout" : layout_number}
#                 wrong_list.append(temp_dict)





# print("the accuracy: ",(len(correct_list)/len(file_list)) * 100 )
# print("wrong classification files ",wrong_list)


# exit()


# input_file = "/home/non/work/proSinu/layout1/sada-a-mix/VF_0007_2020.pdf"


input_file = args["file"]

# input_file = "/home/non/KeenData/zip/ABRA/Nedaňový doklad (neplátce)/22320093012500.pdf"
#input_file = "/home/non/work/01/201201114011408-BAY20061506550.pdf"
#input_file = "/home/non/work/proSinu/layout1/sada-a-mix/2020_060.pdf"

if save_logs_into_file:
        myfile = open(input_file+".txt",'w+') 



number_of_pages,path = image_convert_file(path_in=input_file,absolute_path=True,rotatation_fix=True,prefered_dpi=500)
cat = "MasterPool" #KEEDDAT for new style of
if number_of_pages > 1:
        img = image_combiner([path[0],path[-1]])
else:
        img = cv2.imread(path)

####
#print(img.shape)
from utb.beta import find_layout_beta
layout_number = int(find_layout_beta(img,template_folder=cat,get_struct=False))

#FOR THE SAKE OF SPEED CORRECT IT LATER
# layout_number = int(find_layout(img,template_folder=cat,get_struct=False))
# layout_number = 5
print("the detected layout: ", layout_number)
if save_logs_into_file:
        myfile.write("DETECTED LAYOUT : "+str(layout_number)+"\n")


coordinate_based_on_word = False

for item in coordinates(layout_number,img.shape):
        if (isinstance(item[0],str)):
                coordinate_based_on_word = True
                break

# if isinstance(item[0],str):
#EXPERIMENTAL PART FOR THE KEYWORD BASED SEGMENTATION
stuff=[]
if coordinate_based_on_word or True:
        ddata = data_extract([img])[0]
        seg_texts = ddata["text"]
        seg_conf = ddata["conf"]
        seg_y = ddata["top"]
        seg_x = ddata["left"]
        seg_w = ddata["width"]
        seg_h = ddata["height"]

        stuff = [seg_texts,seg_conf,seg_x,seg_y,seg_w,seg_h]

# print(seg_texts)
# exit()
# cv2.imshow("L",img)
# cv2.waitKey(0)


    

# segs = segmentizer([img],coordinates(layout_number,img.shape ))



from utb.beta import segmentizer_beta
segs = segmentizer_beta([img],coordinates(layout_number,img.shape ),stuff = stuff)

# for part in segs:
#         cv2.imshow("d",part)
#         cv2.waitKey(0)
# exit()
# # #TEST 
# print(len(segs))
# cv2.imshow("S",img)
# cv2.waitKey(0)
# exit()

seg_data = data_extract(segs)

# print(seg_data[0]["text"])
# exit()


# #FOR TESTING
# test_array = -1
# seg_texts = seg_data[test_array]["text"]
# #seg_top = seg_data[-1]["top"]
# #segment_texts = [x for x in seg_texts if len(x)>1]
# segment_texts = seg_texts
# segment_texts = semi_colon_refine(segment_texts)
# segment_texts = list(filter(None,segment_texts))
# segment_texts = [item for item in segment_texts if item !=' ' and item !='|' and item != "'" and item != "-"]
# print(list(splitter(segment_texts)))
# #print("top ",seg_top)
# cv2.imshow("test",segs[test_array])
# cv2.imwrite("luis_test.jpg",segs[test_array])
# cv2.waitKey()
# exit()





# Test segment
# cv2.imshow("!",segs[-1])
# cv2.waitKey()
# exit()





seg_keys = segmap(layout_number)

for index,seg in enumerate(seg_keys):
        
 try:
    seg_texts = seg_data[index]["text"]
    seg_conf = seg_data[index]["conf"]
    seg_y = seg_data[index]["top"]
    seg_x = seg_data[index]["left"]
    seg_w = seg_data[index]["width"]
    seg_h = seg_data[index]["height"]
    


    for index, item in enumerate(seg_texts):#refinements for separate alone semicolons like ":"
        if item != "":
            
            try: 
                if seg_texts[index+1] == ":":
                        seg_texts[index:index+2] = ([''.join(seg_texts[index:index+2])])
                        seg_conf[index:index+2] = (seg_conf[index+1])
                        seg_y[index:index+2] = (seg_conf[index+1])
                        seg_x[index:index+2] = (seg_conf[index+1])
                        seg_w[index:index+2] = (seg_conf[index+1])
                        seg_h[index:index+2] = (seg_conf[index+1])
            except:
                pass


    # refinement section
    refined_list = []

    for conf , word , y_pos, x_pos, w_pos, h_pos in zip(seg_conf ,seg_texts , seg_y,seg_x,seg_w,seg_h):
            if word !='' and word !=' ' and word !="|" and word !="'" and word != '-':# and len(word)>1: 
             while True:
                a, b, c = word.partition(':')
                word = a+b

                temp_combination = [word,conf,y_pos,x_pos,w_pos,h_pos]
                refined_list.append(temp_combination)

                if c != '' and ":" not in c:
                    word = c
                    temp_combination = [word,conf,y_pos,x_pos,w_pos,h_pos]
                    refined_list.append(temp_combination)
                
                word = c
                if ":" not in c:
                        break
                


    seg_texts_refined = []
    seg_conf_refined = []
    seg_pos_refined = []
    seg_x_refined = []
    seg_w_refined = []
    seg_h_refined = []



    for item in refined_list:
            seg_texts_refined.append(item[0])
            seg_conf_refined.append(item[1])
            seg_pos_refined.append(item[2])
            seg_x_refined.append(item[3])
            seg_w_refined.append(item[4])
            seg_h_refined.append(item[5])
       #test 
#     print(seg_texts_refined)
#     continue

#     print(  seg_texts_refined,
#             seg_conf_refined,
#             seg_pos_refined,
#             seg_x_refined,
#             seg_w_refined,
#             seg_h_refined)
#     exit()
#     from distance import get_distance

#     x = get_distance("RODEPA","s.r.o.",text_list=seg_texts_refined,x_list = seg_x_refined,
#     y_list = seg_pos_refined,w_list=seg_w_refined,h_list = seg_h_refined,consider_size=True)

#     print(x)
#     exit()

#     seg_texts_refined = list(splitter(segment_texts))

#     print(seg_texts_refined)
#     continue
    
    key_lock = False
    for counter,line in enumerate(seg):
        stop = None
        blank = False
        if key_lock == True:

                seg_pos_refined.pop(seg_texts_refined.index("!!START!!@"))
                seg_x_refined.pop(seg_texts_refined.index("!!START!!@"))

                seg_w_refined.pop(seg_texts_refined.index("!!START!!@"))
                seg_h_refined.pop(seg_texts_refined.index("!!START!!@"))

                seg_texts_refined.pop(seg_texts_refined.index("!!START!!@"))
                key_lock = False

        try:

                if "preprocessor" in line:
                        seg_texts_refined = preprocessor_handler(line["preprocessor"],seg_texts_refined)           
        except:
                pass
        
        if isinstance(line["key"], int):
                    
                    seg_texts_refined.insert(line["key"],"!!START!!@")
                    seg_pos_refined.insert(line["key"],seg_pos_refined[line["key"]+1])

                    seg_x_refined.insert(line["key"],seg_x_refined[line["key"]+1])
                    seg_w_refined.insert(line["key"],seg_w_refined[line["key"]+1])
                    seg_h_refined.insert(line["key"],seg_h_refined[line["key"]+1])

                    line["key"] = "!!START!!@"
                    key_lock = True
                #     print(seg_texts_refined)
                #     exit()
        # if isinstance(line["key"], list):




                


        if "dist" in line:

            if isinstance((line["dist"]), list):
                    temp = line["dist"]
                    #if key_lock != True or True :
                    line["key"] = hot_word(seg_texts_refined,line["key"],distance=(temp[0]-1))["next"]
                    #print("nnnn ",line["key"])
                    line["dist"] = temp[1]




            #
            try:
                 hot_val = isinstance(int(line["dist"]), int)
            except:
                 hot_val = False

            if isinstance(line["dist"], str) and hot_val == True:
                    distance = line["dist"]

            elif isinstance((line["dist"]), dict):
                    if (line["key"]=='-'):
                        distance = -1
                    if (line["key"]=='|'):
                        distance = -2
                    line["key"] = [line["dist"]["LINE"],seg_x_refined,seg_pos_refined]

                    #sending needed parms through the key

            elif line["dist"]=="_next_":
                    distance = 1

            elif isinstance(line["dist"], int):
                    distance = line["dist"]
                    #hot_val = False

            elif line["dist"]=="_rest_":
                    distance = 1000000
            elif line["dist"]=="_break_":
                    distance = find_split(line["key"],seg_texts_refined,seg_pos_refined,seg_x_refined)

            elif line["dist"]=="_line_":
                    starting_word = hot_word(seg_texts_refined,line["key"])["next"]

                    distance = same_line(starting_word,seg_texts_refined,seg_pos_refined)   
            elif isinstance(line["dist"], tuple):
                    line["key"],distance = multi_line(line["key"],seg_texts_refined,seg_pos_refined,line["dist"][0])
              
            else:
                    distance = 100000
                    stop = line["dist"]
                    

        
        else:
            distance = 1
        
        # print("test section")
        # print(seg_texts_refined)
        # print(line["key"])
        # print(distance)
        try:
                # print("key is ",line["key"])
                # print("test is ",seg_texts_refined)
                var = crop_sentence(sentence_as_list=seg_texts_refined,start=line["key"],stop=stop,distance=distance,hot=hot_val)
        except:
                # print(line["key"], " triggered")
                var = None
        if (var == [None] or var==None or len(var)==0)  and safe == True:
                continue

        #if str(var[0]).lower() not in  str(segs[index+1]["title"][0]).lower(): #means expected value was empty (make both lower case)
        #print("next ", crop_sentence(sentence_list=seg_texts_refined,start=seg[counter+1]["key"],distance=1))
        try:    
                #print("var = ",var)
                if ":" in str(var) and len(var)==1:
                        blank =True
                if  (' '.join(var).lower().rstrip().replace(":","")) in seg[counter+1]["key"].lower() :
                        #print("Blank")
                        blank = True
        except:
                pass

        if key_lock == True:

                seg_pos_refined.pop(seg_texts_refined.index("!!START!!@"))
                seg_x_refined.pop(seg_texts_refined.index("!!START!!@"))
                seg_w_refined.pop(seg_texts_refined.index("!!START!!@"))
                seg_h_refined.pop(seg_texts_refined.index("!!START!!@"))



                seg_texts_refined.pop(seg_texts_refined.index("!!START!!@"))
                key_lock = False


        ##################
        if not blank:
                try:
                        _, confidence  =  confidence_calculator(seg_texts_refined,seg_conf_refined,var)
                except:
                        continue
                        #New post processor !!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT CALCULATING THE CONFIDENCE MIGHT BE EFFECTED , POST PROCESS MIGHT BE MOVED AFTER CALCULATION OF CONF
                try:
                        if "postprocessor" in line:
                                # print("post ",line["postprocessor"])
                                var = postprocessor_handler(line["postprocessor"],var)
                        if var is None:
                                #print(line["key"]," was None ")
                                continue
                except:
                        pass

                print("{0} : {1} : conf {2}".format(str(line["title"]),str(' '.join(var)),confidence   ))
                if save_logs_into_file:
                        data_for_file = "{0} : {1} : conf {2}".format(str(line["title"]),str(' '.join(var)),confidence   )
                        myfile.write(data_for_file+"\n")


 except:
         continue
#additional data
qr = True
if qr == True:

        barcodes = barcode_reader(img)
        if ( len(barcodes) > 0 ):
                print("QrCod : ",barcodes)
                if save_logs_into_file:
                        myfile.write("QrCod : "+str(barcodes)+"\n")
                        
print("PgCou : ",number_of_pages)
if save_logs_into_file:
        myfile.write("PgCou : "+str(number_of_pages)+"\n")
        print("file saved ",input_file+".txt")
        myfile.close()
