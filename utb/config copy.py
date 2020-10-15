#page_res = [4134,5846]

# ####### (1918, 1050)


coordinates_1 = [[(229, 264), (1938, 1059)],[(465, 1470), (1743, 550)],[(2172, 11), (1844, 1212)],[(3503, 1852), (477, 1259)],[(2312, 822), (1568, 341)]]
coordinates_1 = [['Dodavatel:', [4,5]],[(465, 1470), (1743, 550)],[(2172, 11), (1844, 1212)],[(3503, 1852), (477, 1259)]]



layout_1 = [[

            {"title": "NaSupRe", "key" : "Dodavatel:", "dist": "IČ:"},
            {"title": "INSuRe", "key" : "IČ:", "dist": "_next_"},
            {"title": "'TIDSupRe", "key" : "'DIČ:", "dist": "_next_"},
            {"title": "Telefon", "key" : "Telefon:", "dist": "Mobil:"},
            {"title": "Mobil", "key" : "Mobil:", "dist": "Fax:"},
            {"title": "Fax", "key" : "Fax:", "dist": "_next_"},
            {"title": "EmAdr", "key" : "E-mail:", "dist": 1},


],
[
            {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
            {"title": "PayDay", "key" : "splatnosti:", "dist": "_next_"},
            {"title": "VATDay", "key" : "plnění:", "dist": "_next_"},
],
[
            {"title": "InNum", "key" : "DOKLAD" , "dist" : '2' },
            {"title": "VaSym", "key" : "Variabilní" , "dist" : '2' },
            {"title": "KoSy", "key" : "Konstantní" , "dist" : '2' },
            {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
            {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
            {"title": "NaUseTy", "key" : "DIČ:" , "dist" : [2,'_line_'] },
            {"title": "AddUseTy", "key" : "DIČ:" , "dist" : [2,'_rest_'] },
 
],
[           
            {"title": "ToInv", "key" : '-' , "dist" : {"LINE":-1}},
            
],

]



############

coordinates_2 = [[(341, 175), (1866, 1650)],[(2172, 183), (1830, 1584)]]


layout_2 = [
    
    [

       
            {"title": "NaSupRe", "key" : "Dodavatel:", "dist": [5,"_line_"]},
            {"title": "INSuRe", "key" : "IČ:", "dist": "_next_"},
            {"title": "TIDSupRe", "key" : "IČ:", "dist": "3"},
            {"title": "AddUseTy", "key" : "IČ:" , "dist" : [4,'Bankovní'] },
            {"title": "BaAcSupRe", "key" : "Banka:", "dist": "IBAN/SWIFT:" },
            {"title": "IBNSupAc", "key" : "IBAN/SWIFT:", "dist": "_next_"},
            {"title": "BICSupAc", "key" : "IBAN/SWIFT:", "dist": "3"},


    ],

[
            {"title": "InNum", "key" : "DOKLAD" , "dist" : '2' },
            {"title": "VaSym", "key" : "Variabilní" , "dist" : '2' },
            {"title": "KoSy", "key" : "Konstantní" , "dist" : '2' },
            {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
            {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
            {"title": "NaUseTy", "key" : "IČ:" , "dist" : [2,'_line_'] },
            {"title": "AddUseTy", "key" : "IČ:" , "dist" : [2,'Tel.:'] },
            {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
            {"title": "PayDay", "key" : "splatnosti:", "dist": "_next_"},
            {"title": "VATDay", "key" : "platby:", "dist": "_next_"},
 
],

]

#############################################################
coordinates_3 = [[(200, 17), (1095, 403)],[(1471, 140), (595, 306)],[(1996, 131), (1305, 262)],[(3056, 393), (815, 394),],
[(2000, 402), (1857, 1619)],[(1716, 2677), (464, 884)]]


layout_3 = [
    
    [

       
            {"title": "NaSupRe", "key" : 0 , "dist": [1,"_line_"]},
            {"title": "AddUseTy", "key" : 0 , "dist" : [1,"_rest_"] },

            # {"title": "TIDSupRe", "key" : "IČ:", "dist": "3"},
            # {"title": "BaAcSupRe", "key" : "Banka:", "dist": "IBAN/SWIFT:" },
            # {"title": "IBNSupAc", "key" : "IBAN/SWIFT:", "dist": "_next_"},
            # {"title": "BICSupAc", "key" : "IBAN/SWIFT:", "dist": "3"},
            # {"title": "VATDay", "key" : "plnění:", "dist": "_next_"},


    ],

    [           
            {"title": "INSuRe", "key" : "IČ:", "dist": "_next_"},
            {"title": "TIDSupRe", "key" : "DIČ:", "dist": "_next_"},
            # {"title": "InNum", "key" : "DOKLAD" , "dist" : '2' },
            # {"title": "VaSym", "key" : "Variabilní" , "dist" : '2' },
            # {"title": "KoSy", "key" : "Konstantní" , "dist" : '2' },
            # {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
            # {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
            # {"title": "NaUseTy", "key" : "IČ:" , "dist" : [2,'_line_'] },
            # {"title": "AddUseTy", "key" : "IČ:" , "dist" : [2,'Tel.:'] },
            # {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
            # {"title": "PayDay", "key" : "splatnosti:", "dist": "_next_"},
            # {"title": "VATDay", "key" : "platby:", "dist": "_next_"},
 
    ],

    [
            {"title": "Telefon", "key" : "tel.:", "dist": "_next_"},
            {"title": "Mobil", "key" : "mobil:", "dist": "_next_"},
            {"title": "Fax", "key" : "fax:", "dist": "_next_"},
            {"title": "EmAdr", "key" : "email:", "dist": "_next_"},
    ],

    [
            {"title": "InNum", "key" : 0 , "dist": [1,"_next_"]}
    ],

    [
           {"title": "NaCusTy", "key" : "Odběratel" , "dist" : '_line_' },
           {"title": "AdCus", "key" : "Odběratel" , "dist" :  "IČ:"},
           {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
           {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },

    ],
    
    [
            {"title": "ToInv", "key" : '-' , "dist" : {"LINE":-1}},
    ]

]

############

coordinates_4 = [[(2758, 8), (1314, 1532)],[(1278, 673), (1542, 849)],[(324, 113), (989, 1427)],[(2732, 4559), (1279, 753)],
            [(2732, 4559), (1279, 753)]]


layout_4 = [
    
    [

       
            {"title": "NaSupRe", "key" : "Dodavatel:", "dist": [1,"_line_"]},
            {"title": "AddUseTy", "key" : "Dodavatel:" , "dist" : [1,'IČO:'] },
            {"title": "INSuRe", "key" : "IČO:", "dist": "_next_"},
            {"title": "TIDSupRe", "key" : "DIČ:", "dist": "_next_"},
            {"title": "BaAcSupRe", "key" : "účet", "dist": "2" },
            {"title": "VATDay", "key" : "plnění:", "dist": "_next_"},
            {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
            {"title": "Telefon", "key" : "Telefony:", "dist": "_rest_"},




    ],

[
              {"title": "PayDay", "key" : "SPLATNOSTI:", "dist": "_next_"},
              {"title": "ToInv", "key" : "ÚHRADĚ:" , "dist" : "DATUM" },
              {"title": "InNum", "key" : "DOKLAD" , "dist" : '2' },
#             {"title": "VaSym", "key" : "Variabilní" , "dist" : '2' },
#             {"title": "KoSy", "key" : "Konstantní" , "dist" : '2' },
#             {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
#             {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
#             {"title": "NaUseTy", "key" : "IČ:" , "dist" : [2,'_line_'] },
#             {"title": "AddUseTy", "key" : "IČ:" , "dist" : [2,'Tel.:'] },
#             {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
#             {"title": "VATDay", "key" : "platby:", "dist": "_next_"},
 
],
    [
              {"title": "NaCusTy", "key" : "Odběratel" , "dist" : [2,'_line_'] },
              {"title": "AdCus", "key" : "Odběratel" , "dist" :  [2,'IČO:']},
              {"title": "INUseTy", "key" : "IČO:" , "dist" : '_next_' },
              {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' }, 
              {"title": "BaAcSupAc", "key" : "Bankovní" , "dist" : '2' },
    ],

    [
            {"title": "ToInv", "key" : "úhradě" , "dist" : "_rest_", "preprocessor" : "_num_", "postprocessor" : "_test_"},

    ]
]
############

coordinates_5 = [[(0, 26), (1973, 1129)],[(5, 1794), (1990, 1171)],[(1965, 223), (2066, 2777)],[(2413, 8130), (1495, 765)]]


layout_5 = [
    
    [

       
            {"title": "NaSupRe", "key" : "Dodává:", "dist": "_line_"},
            {"title": "AddUseTy", "key" : "Dodává:" , "dist" : "Tel/Fax:" },
            {"title": "INSuRe", "key" : "IČO:", "dist": "_next_"},
            {"title": "TIDSupRe", "key" : "DIČ:", "dist": "_next_"},
            # {"title": "BaAcSupRe", "key" : "účet", "dist": "2" },
            # {"title": "VATDay", "key" : "plnění:", "dist": "_next_"},
            # {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
            # {"title": "Telefon", "key" : "Telefony:", "dist": "_rest_"},




    ],

    [
           {"title": "AddUseTy", "key" : "zboží/služby:" , "dist" : "GLN:" },

#             {"title": "PayDay", "key" : "SPLATNOSTI:", "dist": "_next_"},
#             {"title": "ToInv", "key" : "ÚHRADĚ:" , "dist" : "DATUM" },
#             {"title": "VaSym", "key" : "Variabilní" , "dist" : '2' },
#             {"title": "KoSy", "key" : "Konstantní" , "dist" : '2' },
#             {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
#             {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
#             {"title": "NaUseTy", "key" : "IČ:" , "dist" : [2,'_line_'] },
#             {"title": "AddUseTy", "key" : "IČ:" , "dist" : [2,'Tel.:'] },
#             {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
#             {"title": "VATDay", "key" : "platby:", "dist": "_next_"},
            # {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},

 
    ],
    [
            {"title": "InNum", "key" : "FAKTURY/VARIABILNÍ" , "dist" : '2' },
            {"title": "BaAcSupAc", "key" : "Banka:" , "dist" : 'Konstantní' },
            {"title": "VaSym", "key" : "FAKTURY/VARIABILNÍ" , "dist" : '2' },
            {"title": "KoSy", "key" : "Konstantní" , "dist" : '_next_' },
            {"title": "NaCusTy", "key" : "dokladu:" , "dist" : "Splatnost" },
            #   {"title": "AdCus", "key" : "Odběratel" , "dist" :  [2,'IČO:']},
            #   {"title": "INUseTy", "key" : "IČO:" , "dist" : '_next_' },
            #   {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
            {"title": "PayDay", "key" : "Splatnost", "dist": "2"},
            {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
            {"title": "VATDay", "key" : "plnění:", "dist": "_next_"},
  
    ],

    [
            {"title": "ToInv", "key" : "ÚHRADĚ" , "dist" : "_rest_"},
    ]

     
]

################################################################
list_of_layouts = [layout_1,layout_2,layout_3,layout_4,layout_5]
list_of_coordinates = [coordinates_1,coordinates_2,coordinates_3,coordinates_4,coordinates_5]
page_res = [[4134,5846],[4134,5846],[4134,5846],[4134,5846],[4132,11696]]


def segmap(layout_query):
    
    for counter, layout in enumerate(list_of_layouts):
        if layout_query == (counter+1):
            return layout
    
    return -1

def scaler(base_res,new_res,input_list):
    new_list = []
    
    x_ratio = new_res[0] / base_res[0]
    y_ratio = new_res[1] / base_res[1]

    invert = False

    for item in input_list:
        if isinstance(item[0][1], str) and isinstance(item[0][0], str) and isinstance(item[0],tuple):
            invert = True

        x = int( x_ratio * int(item[0][0])  ) if isinstance(item[0],tuple) else item[0]
        y = int( y_ratio * int(item[0][1])  ) if isinstance(item[0],tuple) else None

        # precenage_coffecies_w = 1 if not isinstance(item[1],list) else item[1][0]
        # precenage_coffecies_h = 1 if not isinstance(item[1],list) else item[1][1]

        if isinstance(item[1],list): # height and width was besed on percentage
            item[1][0] = int(item[1][0] * new_res[0] / 100)
            item[1][1] = int(item[1][1] * new_res[1] / 100)


        w = int( x_ratio * item[1][0]  ) if isinstance(item[1][0], int) else item[1][0]# do not scale if it is until line
        h = int( y_ratio * item[1][1]  ) if isinstance(item[1][0], int) else item[1][1]
        
        if (invert):
            x = str(x)
            y = str(y)

        final_scaled = [(x,y),(w,h)] if y is not None else [x,(w,h)]
        new_list.append(final_scaled)
    return new_list

def coordinates(coordinate_query,shape):
    
    new_res = list(shape)[:2]
    new_res[1],new_res[0] = new_res[0] , new_res [1]
    for counter, coordinate in enumerate(list_of_coordinates):
        if coordinate_query == (counter+1):
            return scaler(base_res=page_res[coordinate_query-1],new_res=new_res,input_list = coordinate) # Scale it to the resulution
    
    #print("err")
    return -1



