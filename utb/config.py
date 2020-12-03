#page_res = [4134,5846]

# ####### (1918, 1050)


coordinates_1 = [[(0, 0), (1851, 429)],[(78, 35), (1957, 2381)],[(131, 1549), (1702, 341)],[(3017, 0), (1106, 315)],[(2017, 271), (1921, 525)],
[(2035, 1444), (1868, 438)],[(2044, 1803), (1903, 665)],['Rekapitulace', (2307, 858)],['Celkem', (1614, 674),4],
[(1087, 3750), (772, 1532)],[(5, 2692), (2295, 2791)]]

#Rekapitulace (816, 1269)  jame kharid ('2412', '3668')
layout_1 = [
    [
            {"title": "CrNo", "key" : "-", "dist": {"LINE":0},"postprocessor":"_dobropis_"},

    ],
    [
            
        #   {"title": "Chera", "key" : "Dodavatel:", "dist": "_break_"},
            {"title": "NaSup", "key" : "Dodavatel:", "dist": (1,"_line_")},
            {"title": "StSup", "key" : "Dodavatel:", "dist": (2,"_line_")},
            {"title": "PoSup", "key" : "Dodavatel:", "dist": (3,"_line_"),"postprocessor":"_postcode_"},
            {"title": "CiSup", "key" : "Dodavatel:", "dist": (3,"_line_"),"postprocessor":"_cityname_"},
            {"title": "CoSup", "key" : "Dodavatel:", "dist": (4,"_line_")},
            {"title": "INSup", "key" : "IČ:", "dist": "_next_"},
            {"title": "TIDSup", "key" : "DIČ:", "dist": "_next_"},
            {"title": "IBNSup","key" : "IBAN:", "dist": "_line_"},
            {"title": "BICSup", "key" : "BIC:", "dist": "_line_"},
            {"title": "VaSym","key" : "Var.", "dist": "2","postprocessor":"check_num"},
            {"title": "KoSy","key" : "Konst.", "dist":"2","postprocessor":"check_num"},
            {"title": "SpSym","key" : "Spec.", "dist":"2","postprocessor":"check_num"},
            {"title": "PayRef", "key" : "úhrady:", "dist": "_line_"},


            ],

            [
            {"title": "BaAcSup", "key" : "účet:", "dist": "1"},
            {"title": "BaCoSup", "key" : "účet:", "dist": "3"},

            ],

            [
            {"title": "InNum", "key" : "-", "dist": {"LINE":0}},

            ],


            [
            {"title": "NaCus", "key" : "sídlo:", "dist": "_line_"},
            {"title": "StCus", "key" : "sídlo:", "dist": (1,"_line_")},
            {"title": "PoCus", "key" : "sídlo:", "dist": (2,"_line_"),"postprocessor":"_postcode_"},
            {"title": "CiCus", "key" : "sídlo:", "dist": (2,"_line_"),"postprocessor":"_cityname_"},
            {"title": "CoCus", "key" : "sídlo:", "dist": (3,"_line_")},
            {"title": "INCus", "key" : "DIČ:", "dist": "-1"},
            {"title": "TIDCus", "key" : "DIČ:", "dist": "1"},

            ],

            [
            {"title": "AdDel", "key" : "určení:", "dist": "_rest_"},

                #[(2000, 1435), (1930, 753)]
            ],

            [
            {"title": "OrdNum", "key" : "Objednávka:", "dist": "_line_"},#
            {"title": "IssDay", "key" : "Vystaveno:", "dist": "_line_"},#
            {"title": "PayDay", "key" : "splatnosti:", "dist": "_line_"},#
            {"title": "VATDay", "key" : "plnění:", "dist": "_line_"},#
            ],

            #the part for the VAT and accounting related sections
            [

            {"title": "VATRat0", "key" : 0, "dist": "_rest_","postprocessor":"VATRat0"},
            {"title": "VATRat10", "key" : 0, "dist": "_rest_","postprocessor":"VATRat10"},
            {"title": "VATRat15", "key" : 0, "dist": "_rest_","postprocessor":"VATRat15"},
            {"title": "VATRat21", "key" : 0, "dist": "_rest_","postprocessor":"VATRat21"},

            ],

            [
            {"title": "ToInv", "key" : 'úhradě', "dist": "Zálohy"},
            {"title": "AdPay", "key" : 'Zálohy', "dist": "Zbývá"},
            {"title": "ToPay", "key" : 'uhradit', "dist": [2,"_rest_"]},
            {"title": "InCur", "key" : 'uhradit', "dist": "_next_"},

            ],

            [
            {"title": "ExVat0", "key" : '-', "dist": {"LINE":0},"postprocessor":"ExVat0"},
            {"title": "ExVat10", "key" : '-', "dist": {"LINE":1},"postprocessor":"ExVat10"},
            {"title": "ExVat15", "key" : '-', "dist": {"LINE":2},"postprocessor":"ExVat15"},
            {"title": "ExVat21", "key" : '-', "dist": {"LINE":3},"postprocessor":"ExVat21"},

        

            ],
            [
            {"title": "TrVAT", "key" : 0, "dist": "_rest_","postprocessor":"TrVAT_check"},

            ],

            ]
#             {"title": "Fax", "key" : "Fax:", "dist": "_next_"},
#             {"title": "EmAdr", "key" : "E-mail:", "dist": 1},


# ],
# [
#             {"title": "IssDay", "key" : "vystavení:", "dist": "_next_"},
#             {"title": "PayDay", "key" : "splatnosti:", "dist": "_next_"},
#             {"title": "VATDay", "key" : "plnění:", "dist": "_next_"},
# ],
# [
#             {"title": "InNum", "key" : "DOKLAD" , "dist" : '2' },
#             {"title": "VaSym", "key" : "Variabilní" , "dist" : '2' },
#             {"title": "KoSy", "key" : "Konstantní" , "dist" : '2' },
#             {"title": "INUseTy", "key" : "IČ:" , "dist" : '_next_' },
#             {"title": "TIDUseTy", "key" : "DIČ:" , "dist" : '_next_' },
#             {"title": "NaUseTy", "key" : "DIČ:" , "dist" : [2,'_line_'] },
#             {"title": "AddUseTy", "key" : "DIČ:" , "dist" : [2,'_rest_'] },
 
# ],
# [           
#             {"title": "ToInv", "key" : '-' , "dist" : {"LINE":-1}},
            
# ],

#]



############
coordinates_2 = [[(2112, 27), (1985, 532)],[(27, 27), (1742, 1308)],
[('192', '1216'), (1962, 779)],[(2084, 96), (1918, 814)],
[(2688, 586), (1349, 359)],[(2215, 800), (1402, 464)],
[(3419, 1860), (508, 1673)],['Sazba',(236, 428)],
['Základ', (400, 429),[-25,-5]],
['Celkem', (605, 700),4],
[(5, 2692), (2295, 2791)]
]

#Rekapitulace (816, 1269)  jame kharid ('2412', '3668')
layout_2 = [
    [
            {"title": "CrNo", "key" : "-", "dist": {"LINE":0},"postprocessor":"_dobropis_"},
            {"title": "InNum", "key" : "č.", "dist":"_next_"},


    ],
    [
            
            {"title": "NaSup", "key" : "Dodavatel:", "dist": (1,"_line_")},
            {"title": "StSup", "key" : "Dodavatel:", "dist": (2,"_line_")},
            {"title": "PoSup", "key" : "Dodavatel:", "dist": (3,"_line_"),"postprocessor":"_postcode_"},
            {"title": "CiSup", "key" : "Dodavatel:", "dist": (3,"_line_"),"postprocessor":"_cityname_"},
            {"title": "INSup", "key" : "IČ:", "dist": "_next_"},
            {"title": "TIDSup", "key" : "DIČ:", "dist": "_next_"},
            # {"title": "IBNSup","key" : "IBAN:", "dist": "_line_"},
            # {"title": "BICSup", "key" : "BIC:", "dist": "_line_"},
            # {"title": "VaSym","key" : "Var.", "dist": "2","postprocessor":"check_num"},
            # {"title": "KoSy","key" : "Konst.", "dist":"2","postprocessor":"check_num"},
            # {"title": "SpSym","key" : "Spec.", "dist":"2","postprocessor":"check_num"},
            # {"title": "PayRef", "key" : "úhrady:", "dist": "_line_"},


            ],

            [
            {"title": "BaAcSup", "key" : "účtu:", "dist": "1"},
            {"title": "BaCoSup", "key" : "účtu:", "dist": "2"},
            {"title": "IssDay", "key" : "vystavení:", "dist": "_line_"},#
            {"title": "PayDay", "key" : "splatnosti:", "dist": "_line_"},#
            {"title": "VATDay", "key" : "plnění:", "dist": "_line_"},#

            ],

            [

            {"title": "VaSym","key" : "Variabilní", "dist": "2","postprocessor":"check_num"},
            {"title": "KoSy","key" : "Konstantní", "dist":"2","postprocessor":"check_num"},

            ],

            [
            {"title": "INCus", "key" : "IČ:", "dist": "_line_"},
            {"title": "TIDCus", "key" : "DIČ:", "dist": "_line_"},
            ],

            [
            {"title": "NaCus", "key" : "-", "dist":{"LINE":0}},
            {"title": "StCus", "key" : "-", "dist": {"LINE":1}},
            {"title": "PoCus", "key" : "-", "dist": {"LINE":2},"postprocessor":"_postcode_"},
            {"title": "CiCus", "key" : "-", "dist": {"LINE":2},"postprocessor":"_cityname_"},

            ],
            [
            {"title": "ToInv", "key" : '-', "dist": {"LINE":-2}},
            {"title": "ToPay", "key" : '-', "dist": {"LINE":-1}},

            ],

            [

            {"title": "VATRat0", "key" : 0, "dist": "_rest_","postprocessor":"existVAT_0"},
            {"title": "VATRat10", "key" : 0, "dist": "_rest_","postprocessor":"existVAT_10"},
            {"title": "VATRat15", "key" : 0, "dist": "_rest_","postprocessor":"existVAT_15"},
            {"title": "VATRat21", "key" : 0, "dist": "_rest_","postprocessor":"existVAT_21"},

            ],

    #         [
    #         {"title": "NaCus", "key" : "sídlo:", "dist": "_line_"},
    #         {"title": "StCus", "key" : "sídlo:", "dist": (1,"_line_")},
    #         {"title": "PoCus", "key" : "sídlo:", "dist": (2,"_line_"),"postprocessor":"_postcode_"},
    #         {"title": "CiCus", "key" : "sídlo:", "dist": (2,"_line_"),"postprocessor":"_cityname_"},
    #         {"title": "CoCus", "key" : "sídlo:", "dist": (3,"_line_")},

    #         ],

    #         [
    #         {"title": "AdDel", "key" : "určení:", "dist": "_rest_"},

    #             #[(2000, 1435), (1930, 753)]
    #         ],

    #         [
    #         {"title": "OrdNum", "key" : "Objednávka:", "dist": "_line_"},#
    #         {"title": "IssDay", "key" : "Vystaveno:", "dist": "_line_"},#
    #         {"title": "PayDay", "key" : "splatnosti:", "dist": "_line_"},#
    #         {"title": "VATDay", "key" : "plnění:", "dist": "_line_"},#
    #         ],

    #         #the part for the VAT and accounting related sections


    #         [
    #         {"title": "ToInv", "key" : 'úhradě', "dist": "Zálohy"},
    #         {"title": "AddPay", "key" : 'Zálohy', "dist": "Zbývá"},
    #         {"title": "ToPay", "key" : 'uhradit', "dist": [2,"_rest_"]},
    #         {"title": "InCur", "key" : 'uhradit', "dist": "_next_"},

    #         ],

            [
            {"title": "ExVat0", "key" : '-', "dist": {"LINE":1}},
            {"title": "ExVat10", "key" : '-', "dist": {"LINE":2}},
            {"title": "ExVat15", "key" : '-', "dist": {"LINE":3}},
            {"title": "ExVat21", "key" : '-', "dist": {"LINE":4}},


            ],

            [
            {"title": "ToInv10", "key" : '-', "dist": {"LINE":1}},
            {"title": "ToInv15", "key" : '-', "dist": {"LINE":2}},
            {"title": "ToInv21", "key" : '-', "dist": {"LINE":3}},


            ],

            [
            {"title": "TrVAT", "key" : 0, "dist": "_rest_","postprocessor":"TrVAT_check"},

            ],
            ]
##############################################################

coordinates_3 = [
    [(100, 150), (1979, 727)],
    [('2977', '52'), (981, 726)],
    [(157, 43), (1296, 482)],
    [(1234, 52), (885, 543)],


    [(315, 1732), (1191, 324)],
    [(1550, 1732), (508, 324)],

    [(1068, 1216), (928, 630)],
    [(262, 1338), (824, 482)],
    [(2145, 656), (1770, 866)],
    [(2163, 1610), (1156, 429)],

    ['CELKEM', (2*319, 400),[-50,-85]],


    ['úhradě:', (650, 120),[50,-10]],

    ['uhradit:', (650, 120),[50,-10]],
    [(5, 2692), (2295, 2791)]

    #uhradit:
]

layout_3 = [
    [
            {"title": "CrNo", "key" : 'Faktura', "dist": "_line_","postprocessor":"_dobropis_"},

    ],
    [
            {"title": "InNum", "key" : '-', "dist":{"LINE":0}},

    ],

    [
            
        #   {"title": "Chera", "key" : "Dodavatel:", "dist": "_break_"},
            {"title": "NaSup", "key" : "-", "dist": {"LINE":0}},
            {"title": "StSup", "key" : "-", "dist": {"LINE":1}},
            {"title": "PoSup", "key" : "-", "dist": {"LINE":2},"postprocessor":"_postcode_"},
            {"title": "CiSup", "key" : "-", "dist": {"LINE":2},"postprocessor":"_cityname_"},
            {"title": "CoSup", "key" : "-", "dist": {"LINE":3}},
            # {"title": "CoSup", "key" : "Dodavatel:", "dist": (4,"_line_")},
            # {"title": "INSup", "key" : "IČ:", "dist": "_next_"},
            # {"title": "TIDSup", "key" : "DIČ:", "dist": "_next_"},
            # {"title": "IBNSup","key" : "IBAN:", "dist": "_line_"},
            # {"title": "BICSup", "key" : "BIC:", "dist": "_line_"},
            # {"title": "VaSym","key" : "Var.", "dist": "2","postprocessor":"check_num"},
            # {"title": "KoSy","key" : "Konst.", "dist":"2","postprocessor":"check_num"},
            # {"title": "SpSym","key" : "Spec.", "dist":"2","postprocessor":"check_num"},
            # {"title": "PayRef", "key" : "úhrady:", "dist": "_line_"},


            ],

            [

            {"title": "INSup", "key" : "DIČ:", "dist": "-1"},
            {"title": "TIDSup", "key" : "DIČ:", "dist": "1"},
            ],

            [
            {"title": "BaAcSup", "key" : '-', "dist": {"LINE":-1}},
            ],

            [
            {"title": "BaCoSup", "key" : '-', "dist": {"LINE":-1}},
            ],

            [
            {"title": "KoSy","key" : "konstantní:", "dist": "1","postprocessor":"check_num"},
            {"title": "VaSym","key" : "variabilní:", "dist":"1","postprocessor":"check_num"},
            {"title": "SpSym","key" : "specifický:", "dist":"1","postprocessor":"check_num"},
            ],

            [
            {"title": "IssDay", "key" : "vystavení:", "dist": "_line_"},#
            {"title": "PayDay", "key" : "splatnosti:", "dist": "_line_"},#
            {"title": "VATDay", "key" : "plnění:", "dist": "_line_"},#
    
            ],

            [
            {"title": "INCus", "key" : "DIČ:", "dist": "-1"},
            {"title": "TIDCus", "key" : "DIČ:", "dist": "1"},
            {"title": "NaCus", "key" : "Odběratel", "dist": (1,"_line_")},
            {"title": "StCus", "key" : "Odběratel", "dist": (2,"_line_")},
            {"title": "PoCus", "key" : "Odběratel", "dist": (3,"_line_"),"postprocessor":"_postcode_"},
            {"title": "CiCus", "key" : "Odběratel", "dist": (3,"_line_"),"postprocessor":"_cityname_"},
            {"title": "CoCus", "key" : "Odběratel", "dist": (4,"_line_")},

            ],

            [
            # {"title": "BaAcSup", "key" : "účet:", "dist": "1"},
            # {"title": "BaCoSup", "key" : "účet:", "dist": "3"},
            {"title": "AdDel", "key" : 0, "dist": "_rest_"},

            ],

            [

            {"title": "VATRat0", "key" : 0, "dist": "_rest_","preprocessor":"fix_percentage",  "postprocessor":"existVAT_0"},
            {"title": "VATRat10", "key" : 0, "dist": "_rest_","preprocessor":"fix_percentage", "postprocessor":"existVAT_10"},
            {"title": "VATRat15", "key" : 0, "dist": "_rest_","preprocessor":"fix_percentage", "postprocessor":"existVAT_15"},
            {"title": "VATRat21", "key" : 0, "dist": "_rest_","preprocessor":"fix_percentage", "postprocessor":"existVAT_21"},

            ],

            [
            {"title": "ToInv", "key" : 0, "dist": "_rest_"},
            ],

            [
            {"title": "ToPay", "key" : '-', "dist": {"LINE":0}},

            ],

            [
            {"title": "TrVAT", "key" : 0, "dist": "_rest_","postprocessor":"TrVAT_check"},

            ],


]
#############################################################
coordinates_4 = [
    [(2154, 148), (1620, 403)],
    [(297, 192), (1787, 1610)],
    [(2019, 615), (1635, 889)],
    [(2096, 658), (1396, 606)],
    [(2023, 1452), (2040, 464)],
    [(2102, 1549), (1988, 2546)],
    [(5, 2692), (2295, 2791)],
    ['Rozpis', (700, 500)],

    ]


layout_4 = [
    [
            {"title": "CrNo", "key" : "-", "dist": {"LINE":0},"postprocessor":"_dobropis_"},
            {"title": "InNum", "key" : "číslo:", "dist":"_next_"},
            {"title": "InNum", "key" : "č.", "dist":"_next_"},


    ],
    [
            {"title": "NaSup", "key" : "-", "dist":{"LINE":1}},
            {"title": "StSup", "key" : "-", "dist":{"LINE":2}},
            {"title": "PoSup", "key" : "-", "dist":{"LINE":3},"postprocessor":"_postcode_"},
            {"title": "CiSup", "key" : "-", "dist":{"LINE":3},"postprocessor":"_cityname_"},
            {"title": "INSup", "key" : "DIČ:", "dist": "-1"},
            {"title": "TIDSup", "key" : "DIČ:", "dist": "1"},

            {"title": "IBNSup","key" : "(BIC):", "dist": "_next_"} ,
            {"title": "IBNSup","key" : "IBAN/SWIFT:", "dist": "1"} ,

            {"title": "BICSup", "key" : "Číslo", "dist": "-1","postprocessor":"_validbic_"},
            {"title": "BICSup", "key" : "IBAN/SWIFT:", "dist": "3","postprocessor":"_validbic_"},

            {"title": "BaAcSup", "key" : 'účtu:', "dist": "1"},
            {"title": "BaCoSup", "key" : "účtu:", "dist": "2"},
            {"title": "PayRef", "key" : "úhrady:", "dist": "_line_"},

    ],

    [
            {"title": "VaSym","key" : "Variabilní", "dist": "2","postprocessor":"check_num"},
            {"title": "KoSy","key" : "Konstantní", "dist":"2","postprocessor":"check_num"},
            # {"title": "SpSym","key" : "Spec.", "dist":"2","postprocessor":"check_num"},
            {"title": "INCus", "key" : "IČ:", "dist": "1"},
            {"title": "TIDCus", "key" : "DIČ:", "dist": "1"},
            
            ],

            [
            {"title": "NaCus", "key" : "-", "dist":{"LINE":1}},
            {"title": "StCus", "key" : "-", "dist":{"LINE":2}},
            {"title": "PoCus", "key" : "-", "dist":{"LINE":3},"postprocessor":"_postcode_"},
            {"title": "CiCus", "key" : "-", "dist":{"LINE":3},"postprocessor":"_cityname_"},
            ],

            [
            {"title": "IssDay", "key" : "vystavení:", "dist": "_line_"},#
            {"title": "PayDay", "key" : "splatnosti:", "dist": "_line_"},#
            {"title": "VATDay", "key" : "platby:", "dist": "_line_"},#
            ],


            [
            {"title": "ToInv", "key" : 'úhradě', "dist": [2,"_line_"]},
            {"title": "InCur", "key" : 'úhradě', "dist": "_next_"},



            ],

            [
            {"title": "TrVAT", "key" : 0, "dist": "_rest_","postprocessor":"TrVAT_check"},

            ],

            [

            {"title": "VATRat0", "key" : 0, "dist": "_rest_","postprocessor":"existVAT0"},
            {"title": "VATRat10", "key" : 0, "dist": "_rest_","postprocessor":"existVAT10"},
            {"title": "VATRat15", "key" : 0, "dist": "_rest_","postprocessor":"existVAT15"},
            {"title": "VATRat21", "key" : 0, "dist": "_rest_","postprocessor":"existVAT21"},

            ],


            ]
#         

############


# ############

coordinates_5 = [
[(78, 35), (1209, 516)],
[(2951, 183), (1130, 228)],
[(140, 808), (858, 464)],
[(1296, 262), (1182, 1041)],
[(87, 1172), (990, 2*438)],
[(78, 1557), (1542, 823)],
[(1497, 1575), (1016, 560)],
[(2601, 1487), (1261, 867)],
["čiastka", (1673, 150),[30,-5]],
["uhradiť", (1600, 150),[30,-5]],
[(5, 2692), (2295, 2791)]

]

layout_5 = [
        [
            {"title": "CrNo", "key" : 0, "dist": "_line_","postprocessor":"_dobropis_"},

    ],
    [
            {"title": "InNum", "key" : 0, "dist": "_rest_","postprocessor":"_denoise_"},

    ],

    [
            {"title": "NaSup", "key" : "-", "dist": {"LINE":0}},
            {"title": "StSup", "key" : "-", "dist": {"LINE":1}},
            {"title": "PoSup", "key" : "-", "dist": {"LINE":2}  ,"postprocessor":"_postcode_"},
            {"title": "CiSup", "key" : "-", "dist": {"LINE":2}  ,"postprocessor":"_cityname_"},
    ],

    [
                    
            {"title": "INSup", "key" : "IČO:", "dist": "1"},
            {"title": "TIDSup", "key" : "DPH:", "dist": "1"},
    ],
    [
                    
            {"title": "KoSy","key" : "Konštantný", "dist": '1',"postprocessor":"check_num"},
            {"title": "VaSym","key" : "Variabilný", "dist":'1',"postprocessor":"check_num"},
            {"title": "SpSym","key" : "Špecifický", "dist":'1',"postprocessor":"check_num"},
            

    ],
    [
            {"title": "BaAcSup", "key" : "faktůry", "dist": "1"},
            {"title": "BaCoSup", "key" : "IBAN", "dist": "-1"},
            {"title": "IBNSup","key" : "IBAN", "dist": "1"},
            {"title": "BICSup", "key" : "SWIFT", "dist": "1"},
    ],

    [
            {"title": "IssDay", "key" : "Vystavenia", "dist": "_line_"},#
            {"title": "PayDay", "key" : "Splatnosti", "dist": "_line_"},#
            {"title": "VATDay", "key" : "plnenia", "dist": "_line_"},#
    ],
    [
            {"title": "INCus", "key" : "IČO:", "dist": "1","postprocessor":"check_num"},
            {"title": "TIDCus", "key" : "DIČ:", "dist": "1","postprocessor":"check_num"},
            {"title": "NaCus", "key" : "-", "dist": {"LINE":1}},
            {"title": "StCus", "key" : "-", "dist": {"LINE":2}},
            {"title": "PoCus", "key" :  "-", "dist": {"LINE":3},"postprocessor":"_postcode_"},
            {"title": "CiCus", "key" : "-", "dist": {"LINE":3},"postprocessor":"_cityname_"},
    ],
            [
            {"title": "ToInv", "key" : 0, "dist": "1"},
            ],

            [
            {"title": "ToPay", "key" : '-', "dist": {"LINE":0}},

            ],

            [
            {"title": "TrVAT", "key" : 0, "dist": "_rest_","postprocessor":"TrVAT_check"},

            ],


]
################################################################
list_of_layouts = [layout_1,layout_2,layout_3,layout_4,layout_5]
list_of_coordinates = [coordinates_1,coordinates_2,coordinates_3,coordinates_4,coordinates_5]
page_res = [[4134,5846],[4134,5846],[4134,5846],[4134,5846],[4132,5846]]


def segmap(layout_query):
    
    for counter, layout in enumerate(list_of_layouts):
        if layout_query == (counter+1):
            return layout
    
    return -1

def scaler(base_res,new_res,input_list):
    new_list = []
    
    x_ratio = new_res[0] / base_res[0]
    y_ratio = new_res[1] / base_res[1]

    ##

    for item in input_list:
        remove_lines = False
        if isinstance(item[0][1], str) and isinstance(item[0][0], str) and isinstance(item[0],tuple):
            remove_lines = True

        x = int( x_ratio * int(item[0][0])  ) if isinstance(item[0],tuple) else item[0]
        y = int( y_ratio * int(item[0][1])  ) if isinstance(item[0],tuple) else None

        # precenage_coffecies_w = 1 if not isinstance(item[1],list) else item[1][0]
        # precenage_coffecies_h = 1 if not isinstance(item[1],list) else item[1][1]

        if isinstance(item[1],list): # height and width was besed on percentage
            item[1][0] = int(item[1][0] * new_res[0] / 100)
            item[1][1] = int(item[1][1] * new_res[1] / 100)


        w = int( x_ratio * item[1][0]  ) if isinstance(item[1][0], int) else item[1][0]# do not scale if it is until line
        h = int( y_ratio * item[1][1]  ) if isinstance(item[1][0], int) else item[1][1]
        
        if (remove_lines == True):
            x = str(x)
            y = str(y)
            


        final_scaled = [(x,y),(w,h)] if y is not None else [x,(w,h)]

        if len(item)==3:
            zone = item[2]
            final_scaled.append(zone)

        new_list.append(final_scaled)
    return new_list

def coordinates(coordinate_query,shape):
    
    new_res = list(shape)[:2]
    new_res[1],new_res[0] = new_res[0] , new_res [1]
    for counter, coordinate in enumerate(list_of_coordinates):
        if coordinate_query == (counter+1):
            # print(coordinate)
            image_data = scaler(base_res=page_res[coordinate_query-1],new_res=new_res,input_list = coordinate) # Scale it to the resulution
            # print(image_data)
            # exit()
            return image_data
    #print("err")
    return -1



