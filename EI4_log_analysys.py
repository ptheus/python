import time, sys
from progressbar import Percentage, ProgressBar, Bar, FormatLabel
# deal with two list and delete have matched items
def abstract_list(line):
    tmp_list = []
    tmp = line[line.find(Arg_mA):]
    tmp_list.append(line[line.find(Arg_mA) - 1:tmp.find(']') + 1)
    tmp = line[line.find(Arg_mB):]
    tmp_list.append(line[line.find(Arg_mB) - 1:tmp.find(']') + 1)
    tmp = line[line.find(Arg_mC):]
    tmp_list.append(line[line.find(Arg_mC) - 1:tmp.find(']') + 1)
    return tmp_list
    
def match_function()
    list_cursor = []
    find_OK = False
    for i in range(len(list_sed)):
        list_tmp = abstract_list(list_sed[i])
        for j in range(len(list_rev)):
            if list_tmp == abstract_list(list_rev[j]):
                

        
# main
max_time = 0
min_time = 0
average_time =0
list_sed = []
list_rev = []
src_handle = open('', 'rU')
tar_handle = open('', 'w')
file_end_flag = False
try:
    for line in src_handle:
        if len(line) == 0:
            file_end_flag = True
        if line.find(Arg_A) >= 0:
            list_sed.append(line)
        if line.find(Arg_B) >= 0:
            list_rev.append(line)
        if len(list_sed) > 1000 and len(list_rev) > 1000:
            match_function()
        if file_end_flag:
            break
finally:
    tar_handle.close()
    src_handle.close()