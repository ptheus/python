import time, sys
from progressbar import Percentage, ProgressBar, Bar, FormatLabel
# deal with two list and delete have matched items

def right_swich(time):
    hour = int(time[0:2])
    minute = int(time[3:5])
    second = int(time[6:8])
    other = int(time[9:])
    result = (hour * 3600 + minute * 60 + second) * 1000000 + other
    return result
    
def abstract_list(line):
    tmp_list = []
    tmp = line[line.find(Arg_mA):]
    tmp_list.append(line[line.find(Arg_mA) - 1:tmp.find(']') + 1)
    tmp = line[line.find(Arg_mB):]
    tmp_list.append(line[line.find(Arg_mB) - 1:tmp.find(']') + 1)
    tmp = line[line.find(Arg_mC):]
    tmp_list.append(line[line.find(Arg_mC) - 1:tmp.find(']') + 1)
    return tmp_list
def get_time(line,sign):
    if sign == 0:
        tmp_line = line[line.find('AUDIT') - 16:line.find('AUDIT') - 1]
    if sign == 1:
        tmp_line = line[line.find('time') + 5:line.find('time') + 20]
    return tmp_line
# deal with have chosen items 
def match_function()
    list_out_cursor = []
    list_in_cursor = []
    find_OK = False
    for i in range(len(list_sed)):
        list_tmp = abstract_list(list_sed[i])
        for j in range(len(list_rev)):
            if list_tmp == abstract_list(list_rev[j]):
                find_OK = True
                list_in_cursor.append(j)
                rev_time = get_time(list_rev[j],file_flag)
                break
        if find_OK:
            list_out_cursor.append(i)
            find_OK = False
            sed_time = get_time(list_sed[i],file_flag)
            list_tmp.append(rev_time)
            list_tmp.append(sed_time)
            list_OK.append(list_tmp)
    for id in list_out_cursor:
        del list_sed[id]
    for id in list_in_cursor:
        del list_rev[id]
    
# main
max_time = 0
min_time = 0
average_time =0
list_sed = []
list_rev = []
list_OK = []
src_handle = open('', 'rU')
tar_handle = open('', 'w')
file_end_flag = False
glb_line = ''
file_flag = -1
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
            match_function()
            break
    for cur_i in list_OK:
        for cur_j in range(len(cur_i) - 2):
            glb_line = glbline + #添加提取函数。+ '\t'
        glb_line = glb_line + str(right_swich(cur_i[4]) - right_swich(cur_i[3])) + '\t\n'
        tar_handle.write(glb_line)
        glb_line = ''
        
            
            
finally:
    tar_handle.close()
    src_handle.close()