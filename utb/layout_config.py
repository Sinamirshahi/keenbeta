# page_res = [4134,5846]
# new = [2067,2923]

# #######


# coordinates_1 = [[(143,594),(1606,935)],[(2000,804),(788,788)],[(3112,1100),(544,288)],[(220,1648),(576,412)],
# [(840,1696),(580,428)],[(1988,1684),(542,472)],[(2560,1712),(692,424)],[(172,2160),(572,1504)],
# ]

# # coordinates_1_scale = [[(int(page_res[0]/list(c[0])[0]),int(page_res[1]/list(c[0])[1])),
# # (int(page_res[0]/list(c[1])[0]),int(page_res[1]/list(c[1])[1]))] for c in coordinates_1  ] 


# # def scaler_old(base,res,scale):
# #     new_list =[]
    
# #     for item in scale:

# #         x = int( res[0] / item[0][0]  )
# #         y = int( res[1] / item[0][1]  )
# #         w = int( res[0] / base[0] * item[1][0]  )
# #         h = int( res[1] / base[1] * item[1][1]  )

# #         new_list.append([(x,y),(w,h)])

# #     return new_list





        






# layout_1 = [[

#             {"title": "variable symbol", "key" : "symbol):", "dist": "_next_"},
#             {"title": "Constant Symbol", "key" : "symbol:", "dist": "_next_"},
#             {"title": "Dodaci List", "key" : "list:", "dist": "_next_"},
#             {"title": "Datum splatnosti", "key" : "splatnosti:", "dist": "_next_"},
#             {"title": "Forma úhrady", "key" : "úhrady:", "dist": "_next_"},
#             {"title": "Datum vystavení faktury", "key" : "faktury:", "dist": 2},
#             {"title": "Datum zdanitelného plnění", "key" : "plnění:", "dist": "_next_"},

# ],
# [
#             {"title": "Odběratel", "key" : "Odběratel:" , "dist" : "_rest_"},
 
# ],
# [
#             {"title": "IČO", "key" : "IČO:"},
#             {"title": "DIČ", "key" : "DIČ:"},
# ],

# [
#             {"title": "Dodavatel", "key" : "Dodavatel:" , "dist" : "_rest_"},


# ],

# [
#             {"title": "IČO", "key" : "IČO:"},
#             {"title": "DIČ", "key" : "DIČ:"},
#             {"title": "Bankovní spojení", "key" : "spojení:" , "dist" : "č."},
#             {"title": "č.ú.", "key" : "ú.:" , "dist" : "_rest_"},

# ],
# [
#             {"title": "Místo určení:", "key" : "určení:" , "dist" : "_rest_"},

# ],
# [
#             {"title": "Mobile", "key" : "Mob.:"},
#             {"title": "Telephone", "key" : "Tel.:"},
# ],

# [
#             {"title": "Číslo položky", "key" : "položky","dist":"Sazba"},
#             {"title": "Sazba", "key" : "Sazba", "dist":"_rest_"},
# ],


# ]

# ############

# coordinates_2 = [[(324,672),(1704,1092)],[(2172,660),(1644,1088)],
# [(296,1836),(3544,360)]]


# layout_2 = [
    
#     [

#             {"title": "DODAVATEL", "key" : "DODAVATEL", "dist": "IČ:"},
#             {"title": "IČ", "key" : "IČ:", "dist": "_next_"},
#             {"title": "DIČ", "key" : "DIČ:", "dist": "_next_"},
#             {"title": "Email", "key" : "email:", "dist": "_next_"},
#             {"title": "Telephone", "key" : "telefon:", "dist": "Peněžní"},
#             {"title": "Peněžní ústav", "key" : "ústav:", "dist": "Číslo"},
#             {"title": "účtu:", "key" : "účtu:", "dist": "_rest_"},

#     ],

#     [

#             {"title": "ODBĚRATEL", "key" : "ODBĚRATEL", "dist": "IČ:"},
#             {"title": "IČ:", "key" : "IČ:", "dist": "_next_"},
#             {"title": "DIČ:", "key" : "DIČ:", "dist": "_next_"},
#             {"title": "ADRESA DODÁNÍ", "key" : "DODÁNÍ", "dist": "_rest_"},

#     ],

#     [

#             {"title": "Objednávka č", "key" : "č.:", "dist": "_next_"},
#             {"title": "Datum vystavení", "key" : "vystavení:", "dist": "_next_"},
#             {"title": "Forma úhrady", "key" : "úhrady:", "dist": "DUZP:"},
#             {"title": "DUZP", "key" : "DUZP:", "dist": "_next_"},
#             {"title": "KS", "key" : "KS:", "dist": "_next_"},
#             {"title": "Datum splatnosti", "key" : "splatnosti:", "dist": "_next_"},
#             {"title": "VS", "key" : "VS:", "dist": "_next_"},

#     ],

# ]

# #############################################################
# coordinates_2 = [[(324,672),(1704,1092)],[(2172,660),(1644,1088)],
# [(296,1836),(3544,360)]]


################################################################
coord_1 = [[(446, 393), (1664, 464)]]

################################################################
list_of_layouts = [layout_1,layout_2]
list_of_coordinates = [coordinates_1,coordinates_2]



def segmap(layout_query):
    
    for counter, layout in enumerate(list_of_layouts):
        if layout_query == (counter+1):
            return layout
    
    return -1

def scaler(base_res,new_res,input_list):
    new_list = []
    
    x_ratio = new_res[0] / base_res[0]
    y_ratio = new_res[1] / base_res[1]

    for item in input_list:
        x = int( x_ratio * item[0][0]  )
        y = int( y_ratio * item[0][1]  )
        w = int( x_ratio * item[1][0]  )
        h = int( y_ratio * item[1][1]  )
        
        new_list.append([(x,y),(w,h)])
    
    return new_list

def coordinates(coordinate_query,shape):
    
    new_res = list(shape)[:2]
    exit(0)
    new_res[1],new_res[0] = new_res[0] , new_res [1]
    for counter, coordinate in enumerate(list_of_coordinates):
        if coordinate_query == (counter+1):
            return scaler(base_res=page_res,new_res=new_res,input_list = coordinate) # Scale it to the resulution
    
    return -1






