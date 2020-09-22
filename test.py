from utb.beta import data_extract,find_layout,assembler,shape_extract,shape_counter,hot_word,image_convert_file
from utb.beta import segmentizer,crop_sentence,splitter,barcode_reader,watermark_remove,num_refine,image_combiner
from utb.beta import semi_colon_refine,set_environment
from utb.config import segmap,coordinates
import cv2,numpy as np


def confidence_calculator(list_of_words,list_of_conf,sentence,threshold = 50):

        counter = 0
        sum_con = 0
        for word in sentence:
                con = list_of_conf[list_of_words.index(word)]
                sum_con = sum_con + con
                counter = counter + 1
        if counter == 0 :
                print("CHECK THE PAGE!")
                return None
                
        confident_number = int(sum_con/counter) if counter != 0 else counter

        if confident_number >= threshold:
                tag = 1
        else:
                tag = 0
        

        return tag,confident_number

def same_line(key,list_of_words,list_of_positions):
        distance = 0
        index = list_of_words.index(key)

        cut_word_list = list_of_words[index:]
        cut_position_list = list_of_positions[index:]

        
        prev_pos = cut_position_list[0]
        
        for pos in (cut_position_list):

                if abs( pos - prev_pos) < 50:
                        distance = distance + 1
                else:
                        break
        return distance 

def preprocessor_handler(trigger,list_in):
        
        if trigger == "_num_":
                list_in = num_refine(list_in)
        elif trigger == "_reverse_":
                list_in = list_in.reverse()
        return list_in

def postprocessor_handler(trigger,list_in):
        if trigger == "_test_":
                print("post processes activated")
        return list_in

safe = True
set_environment()


input_file = "pdf/1.pdf"              
        
number_of_pages,path = image_convert_file(path_in=input_file,absolute_path=True,rotatation_fix=False)


if number_of_pages > 1:
        img = image_combiner([path[0],path[-1]])
        cat = "lay_templates_multiple"
else:
        img = cv2.imread(path)
        cat = "lay_templates"

#img = watermark_remove(img)




layout_number = int(find_layout(img,template_folder=cat))
print("the detected layout: ", layout_number)

# cv2.imshow("L",img)
# cv2.waitKey(0)
# exit()




segs = segmentizer([img],coordinates(layout_number,img.shape ))

# for image in segs:
#         image = cv2.bitwise_not(image)
# parts=[]
# for part in segs:
#       parts.append(assembler_beta(part)
#       )  

seg_data = data_extract(segs)


# #FOR TESTING
# test_array = -1
# seg_texts = seg_data[test_array]["text"]
# #seg_top = seg_data[-1]["top"]
# segment_texts = semi_colon_refine(seg_texts)
# segment_texts = list(filter(None,seg_texts))
# segment_texts = [item for item in segment_texts if item !=' ' and item !='|' and item != "'" and item != "-"]
# print(list(splitter(segment_texts)))
# #print("top ",seg_top)
# cv2.imshow("test",segs[test_array])
# cv2.imwrite("luis_test.jpg",segs[test_array])
# cv2.waitKey()
# exit()



seg_keys = segmap(layout_number)

for index,seg in enumerate(seg_keys):

    seg_texts = seg_data[index]["text"]
    seg_conf = seg_data[index]["conf"]
    seg_y = seg_data[index]["top"]
    


    for index, item in enumerate(seg_texts):#refinements for separate alone semicolons like ":"
        if item != "":
            
            try: 
                if seg_texts[index+1] == ":":
                        seg_texts[index:index+2] = ([''.join(seg_texts[index:index+2])])
                        seg_conf[index:index+2] = (seg_conf[index+1])
                        seg_y[index:index+2] = (seg_conf[index+1])
            except:
                pass
#     print("Unit")
#     print(seg_texts)
#     print(len(seg_texts),len(seg_y),len(seg_conf))
#     exit()

    # refinement section
    refined_list = []
    for conf , word , y_pos in zip(seg_conf ,seg_texts , seg_y):
            if word !='' and word !=' ' and word !="|" and word !="'": 
                
                a, b, c = word.partition(':')
                word = a+b

                temp_combination = [word,conf,y_pos]
                refined_list.append(temp_combination)

                if c != '':
                    word = c
                    temp_combination = [word,conf,y_pos]
                    refined_list.append(temp_combination)
   
    seg_texts_refined = []
    seg_conf_refined = []
    seg_pos_refined = []



    for item in refined_list:
            seg_texts_refined.append(item[0])
            seg_conf_refined.append(item[1])
            seg_pos_refined.append(item[2])





#     seg_texts_refined = list(splitter(segment_texts))

#     print(seg_texts_refined)
#     continue
    
    key_lock = False
    for counter,line in enumerate(seg):
        stop = None
        blank = False
        if key_lock == True:

                seg_pos_refined.pop(seg_texts_refined.index("!!START!!@"))
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

                    line["key"] = "!!START!!@"
                    key_lock = True
                #     print(seg_texts_refined)
                #     exit()


                


        if "dist" in line:

            if isinstance((line["dist"]), list):
                    temp = line["dist"]
                    #if key_lock != True or True :
                    line["key"] = hot_word(seg_texts_refined,line["key"],distance=(temp[0]-1))["next"]
                    #print("nnnn ",line["key"])
                    line["dist"] = temp[1]


            try:
                 hot_val = isinstance(int(line["dist"]), int)
            except:
                 hot_val = False

            if isinstance(line["dist"], str) and hot_val == True:
                    distance = line["dist"]

            elif line["dist"]=="_next_":
                    distance = 1

            elif isinstance(line["dist"], int):
                    distance = line["dist"]
                    #hot_val = False

            elif line["dist"]=="_rest_":
                    distance = 1000000

            elif line["dist"]=="_line_":
                    starting_word = hot_word(seg_texts_refined,line["key"])["next"]

                    distance = same_line(starting_word,seg_texts_refined,seg_pos_refined)     
                    
            else:
                    distance = 100000
                    stop = line["dist"]
                    

        
        else:
            distance = 1
        var = crop_sentence(sentence_as_list=seg_texts_refined,start=line["key"],stop=stop,distance=distance,hot=hot_val)
        # print("var is here ",var)

        if var == None and safe == True:
                continue

        #if str(var[0]).lower() not in  str(segs[index+1]["title"][0]).lower(): #means expected value was empty (make both lower case)
        #print("next ", crop_sentence(sentence_list=seg_texts_refined,start=seg[counter+1]["key"],distance=1))
        try:    
                #print("var = ",var)
                if ":" in str(var):
                        blank =True
                if  (' '.join(var).lower().rstrip().replace(":","")) in seg[counter+1]["key"].lower()  :
                        #print("Blank")
                        blank = True
        except:
                pass

        if key_lock == True:

                seg_pos_refined.pop(seg_texts_refined.index("!!START!!@"))
                seg_texts_refined.pop(seg_texts_refined.index("!!START!!@"))
                key_lock = False


        ##################
        if not blank:

                _, confidence  =  confidence_calculator(seg_texts_refined,seg_conf_refined,var)
                        #New post processor !!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT CALCULATING THE CONFIDENCE MIGHT BE EFFECTED , POST PROCESS MIGHT BE MOVED AFTER CALCULATION OF CONF
                try:
                        if "postprocessor" in line:
                                var = postprocessor_handler(line["postprocessor"],var)
                except:
                        pass

                print("{0} : {1} : conf {2}".format(line["title"],' '.join(var),confidence   ))


#additional data
qr = True
if qr == True:

        barcodes = barcode_reader(img)
        if ( len(barcodes) > 0 ):
                print("QrCod : ",barcodes)   

print("PgCou : ",number_of_pages)
