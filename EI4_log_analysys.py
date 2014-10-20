import time, sys
import gl
from progressbar import Percentage, ProgressBar, Bar, FormatLabel
# deal with two list and delete have matched items
def usage():
    print '''Usage:''' + sys.argv[0] + ''' [-i] file [-o output] [-f leach argument] [-m match argument]
   You must input file to deal with. and you can choose -o to assign the output name. 
    The filter argument which is use -f or -m is optional. if not , the argument will be use default argument.
    The default argument is: '''  + sys.argv[0] + ''' -o result_record.txt -f |type=double_quote| |type=double_quote_ack| -m |bid_quote_id |ask_quote_id |feedcode'''

def right_swich(time):
    hour = int(time[0:2])
    minute = int(time[3:5])
    second = int(time[6:8])
    other = int(time[9:])
    result = (hour * 3600 + minute * 60 + second) * 1000000 + other
    return result
    
def abstract_list(line):
    tmp_list = []
    if gl.file_flag = 0:
        tmp = line[line.find(gl.Arg_mA):]
        tmp_list.append(line[line.find(gl.Arg_mA):tmp.find(']'))
        tmp = line[line.find(gl.Arg_mB):]
        tmp_list.append(line[line.find(gl.Arg_mB):tmp.find(']'))
        tmp = line[line.find(gl.Arg_mC):]
        tmp_list.append(line[line.find(gl.Arg_mC):tmp.find(']'))
    elif gl.file_flag = 1:
        tmp = line[line.find(gl.Arg_mA):]
        if tmp.find('|') >= 0:
            tmp_list.append(line[line.find(gl.Arg_mA):tmp.find('|')])
        else:
            tmp_list.append(line[line.find(gl.Arg_mA):tmp.find('}')])
        tmp = line[line.find(gl.Arg_mB):]
        if tmp.find('|') >= 0:
            tmp_list.append(line[line.find(gl.Arg_mB):tmp.find('|')])
        else:                                  
            tmp_list.append(line[line.find(gl.Arg_mB):tmp.find('}')])
        tmp = line[line.find(gl.Arg_mC):]
        if tmp.find('|') >= 0:
            tmp_list.append(line[line.find(gl.Arg_mC):tmp.find('|')])
        else:
            tmp_list.append(line[line.find(gl.Arg_mC):tmp.find('}')])
    return tmp_list
    

def get_time(line):
    if gl.file_flag == 0:
        tmp_line = line[line.find('AUDIT') - 16:line.find('AUDIT') - 1]
    if gl.file_flag == 1:
        tmp_line = line[line.find('time') + 5:line.find('time') + 20]
    return tmp_line
    
# deal with have chosen items 
def match_function()
    list_out_cursor = []
    list_in_cursor = []
    find_OK = False
    for i in range(len(gl.list_sed)):
        list_tmp = abstract_list(gl.list_sed[i])
        for j in range(len(gl.list_rev)):
            if list_tmp == abstract_list(gl.list_rev[j]):
                find_OK = True
                list_in_cursor.append(j)
                rev_time = get_time(gl.list_rev[j])
                break
        if find_OK:
            list_out_cursor.append(i)
            find_OK = False
            sed_time = get_time(list_sed[i],file_flag)
            list_tmp.append(rev_time)
            list_tmp.append(sed_time)
            gl.list_OK.append(list_tmp)
    for index in list_out_cursor:
        del gl.list_sed[index]
    for index in list_in_cursor:
        del gl.list_rev[index]
        
def get_value(string):
    if gl.file_flag = 0:
        return string[string.find(":")+1:]
    elif gl.file_flag = 1:
        return string[string.find("=")+1:]
    else:
        return ''
def count():
    file_end_flag = 1
    probar = 1
    print "Begin analysis the log, please waiting...\n"
    pbar.start()
    for i in range(1,101):
        while file_end_flag and probar:
            line = src_handle.readline()
            if len(line) == 0:
                file_end_flag = 0
            else:
                gl.file_size_tmp += len(line)
            if gl.file_size_tmp > (gl.file_size / 100) * i:
                probar = 0
                continue
            if line.find(gl.Arg_A) >= 0:
                gl.list_sed.append(line)
            if line.find(gl.Arg_B) >= 0:
                gl.list_rev.append(line)
            if len(gl.list_sed) > 100 and len(gl.list_rev) > 100:
                match_function()
            if file_end_flag == 0:
                match_function()
                continue
        pbar.update(i)
        probar = 1
    pbar.finish()
    
def gather_result():
    print "Begin gather the result, please waiting...\n"
    pbar.start()
    for cur_i in list_OK:
        for cur_j in range(len(cur_i) - 2):
            glb_line = glbline + get_value(cur_i[cur_j]) + '\t'
        glb_line = glb_line + str(right_swich(cur_i[4]) - right_swich(cur_i[3])) + '\t\n'
        tar_handle.write(glb_line)
        glb_line = ''
    
    
    
    
    
    
    
    
    
    
# main

src_handle = open('GDK-Native01.ommTP.audit.log', 'rU')
tar_handle = open('record.log', 'w')
file_end_flag = False
glb_line = ''

widgets = [Percentage(), ' ', Bar(marker='|',left='|',right='|'),'[', FormatLabel('%(elapsed)s'), ']']
pbar = ProgressBar(widgets=widgets, maxval=100)
try:
    count()
    
    
    
    
    
    
finally:
    tar_handle.close()
    src_handle.close()