import glob,os

mydir = "/home/non/work/dadada/"
file_list = glob.glob(os.path.join(mydir,"**","*.pdf"),recursive=True) 



# for item in file_list:
#     print(item)
# exit()

print(len(file_list))


import os
for index, file_item in enumerate(file_list):
    print("testing {0} out of {1}".format(str(index+1),str(len(file_list))))
    command = "python /home/non/kkk/keenbeta/test.py --file "+str(file_item)
    os.system(command)
    print("done")

print("finished")