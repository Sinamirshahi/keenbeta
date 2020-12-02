import glob
mydir = "/home/non/work/01/"
file_list = glob.glob(mydir + r"*.pdf")

print(len(file_list))
    print(item)


import os
for index, file_item in enumerate(file_list):
    print("testing {0} out of {1}".format(str(index+1),str(len(file_list))))
    command = "python /home/non/kkk/keenbeta/test.py --file "+str(file_item)
    os.system(command)
    print("done")

print("finished")