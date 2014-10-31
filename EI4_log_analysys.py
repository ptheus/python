import time, sys,os
import gl
from progressbar import Percentage, ProgressBar, Bar, FormatLabel
# deal with two list and delete have matched items
def usage():
    print '''Usage:''' + sys.argv[0] + ''' [-i] input file [-o output file]'''

def right_swich(time):
    if len(time) != 15:
        return 0
    else:
        hour = int(time[0:2])
        minute = int(time[3:5])
        second = int(time[6:8])
        other = int(time[9:])
        result = (hour * 3600 + minute * 60 + second) * 1000000 + other
        return result
    
def abstract_list(line):    
    tmp_list = []
    if gl.file_flag == 1:
        tmp = line[line.find(gl.Arg_mA):]
        tmp_list.append(line[line.find(gl.Arg_mA):tmp.find(']')])
        tmp = line[line.find(gl.Arg_mB):]
        tmp_list.append(line[line.find(gl.Arg_mB):tmp.find(']')])
        tmp = line[line.find(gl.Arg_mC):]
        tmp_list.append(line[line.find(gl.Arg_mC):tmp.find(']')])
    elif gl.file_flag == 0:
        Arg_mA = '|' + gl.Arg_mA + '='
        Arg_mB = '|' + gl.Arg_mB + '='
        Arg_mC = '|' + gl.Arg_mC + '='
        tmp = line[line.find(Arg_mA)+1:]
        if tmp.find('|') >= 0:
            tmp_list.append(line[line.find(Arg_mA)+1:tmp.find('|') + line.find(Arg_mA)+1])
        else:
            tmp_list.append(line[line.find(Arg_mA)+1:tmp.find('}') + line.find(Arg_mA)+1])
        tmp = line[line.find(Arg_mB)+1:]
        if tmp.find('|') >= 0:
            tmp_list.append(line[line.find(Arg_mB)+1:tmp.find('|') + line.find(Arg_mB)+1])
        else:
            tmp_list.append(line[line.find(Arg_mB)+1:tmp.find('}') + line.find(Arg_mB)+1])
        tmp = line[line.find(Arg_mC)+1:]
        if tmp.find('|') >= 0:
            tmp_list.append(line[line.find(Arg_mC)+1:tmp.find('|') + line.find(Arg_mC)+1])
        else:
            tmp_list.append(line[line.find(Arg_mC)+1:tmp.find('}') + line.find(Arg_mC)+1])
    return tmp_list
    

def get_time(line):
    if gl.file_flag == 1:
        tmp_line = line[line.find('AUDIT') - 16:line.find('AUDIT') - 1]
    elif gl.file_flag == 0:
        tmp_line = line[line.find('time') + 5:line.find('time') + 20]
    else:
        tmp_line = 0
    return tmp_line
    
# deal with have chosen items 
def match_function():
    list_sed = []
    list_rev = []
    find_OK = False
    for i in range(len(gl.list_sed)):
        list_tmp = abstract_list(gl.list_sed[i])
        for j in range(len(gl.list_rev)):
            if list_tmp == abstract_list(gl.list_rev[j]):
                find_OK = True
                rev_time = get_time(gl.list_rev[j])
                gl.list_rev[j] = 'DELD'
                break
        if find_OK:
            find_OK = False
            sed_time = get_time(gl.list_sed[i])
            gl.list_sed[i] = 'DELD'
            list_tmp.append(rev_time)
            list_tmp.append(sed_time)
            gl.list_OK.append(list_tmp)
    for i in gl.list_sed:
        if i != 'DELD':
            list_sed.append(i)
    gl.list_sed = list_sed[:]
    del list_sed
    for j in gl.list_rev:
        if j != 'DELD':
            list_rev.append(j)
    gl.list_rev = list_rev[:]
    del list_rev

def get_value(string):
    if gl.file_flag == 1:
        return string[string.find(":")+1:]
    elif gl.file_flag == 0:
        return string[string.find("=")+1:]
    else:
        return ''

def count():
    rev_num = 0
    sed_num = 0
    widgets = ['Analysising: ',Percentage(), ' ', Bar(marker='|',left='|',right='|'),'[', FormatLabel('%(elapsed)s'), ']']
    pbar = ProgressBar(widgets=widgets, maxval=100)
    file_end_flag = 1
    flag_jump = 1
    probar = 1
    print "Begin analysis the log, please waiting..."
    pbar.start()
    for i in range(1,101):
        if gl.g_time != 0:
            while flag_jump and file_end_flag and probar:
                line = src_handle.readline()
                if len(line) == 0:
                    file_end_flag = 0
                else:
                    gl.file_size_tmp += len(line)
                if right_swich(get_time(line)) == 0:
                    pass
                else:
                    if right_swich(get_time(line)) > swich_time(gl.g_time):
                        flag_jump = 0
                if gl.file_size_tmp > (gl.file_size / 100) * i:
                    probar = 0
        else:
            flag_jump = 0
        while file_end_flag and probar and not flag_jump:
            line = src_handle.readline()
            if len(line) == 0:
                file_end_flag = 0
            else:
                gl.file_size_tmp += len(line)
            if gl.file_size_tmp > (gl.file_size / 100) * i:
                probar = 0
                continue
            if line.find(gl.Arg_A) >= 0:
                sed_num += 1
                gl.list_sed.append(line)
            if line.find(gl.Arg_B) >= 0:
                rev_num += 1
                gl.list_rev.append(line)
            if sed_num > 100 and rev_num > 100:
                match_function()
                rev_num = 0
                sed_num = 0
            if file_end_flag == 0:
                match_function()
                rev_num = 0
                sed_num = 0
            if gl.g_number != -1 and len(gl.list_OK) > int(gl.g_number):
                file_end_flag = 0
        pbar.update(i)
        probar = 1
    pbar.finish()

def swich_time(string):
    tmp = string.split(':')
    if len(tmp) != 3:
        return 0
    else:
        t_hour = int(tmp[0])
        t_min = int(tmp[1])
        t_sec = int(tmp[2])
        return (t_hour * 3600 + t_min * 60 + t_sec) * 1000000
        
def gather_result():
    start_cur = 0
    end_cur = len(gl.list_OK)
    bar_length = len(gl.list_OK)
    if gl.g_time != 0:
        for index in range(len(gl.list_OK)):
            if right_swich(gl.list_OK[index][4]) > swich_time(gl.g_time):
                start_cur = index
                break
    if gl.g_number != -1:
        end_cur = start_cur + gl.g_number
        bar_length = gl.g_number
    widgets = ['Gather result: ',Percentage(), ' ', Bar(marker='|',left='|',right='|'),'[', FormatLabel('%(elapsed)s'), ']']
    pbar = ProgressBar(widgets=widgets, maxval=bar_length)
    pbar.start()
    diff_time = 0
    glb_line = ''
    for cur_i in range(start_cur,end_cur):
        for cur_j in range(len(gl.list_OK[cur_i]) - 2):
            glb_line = glb_line + get_value(gl.list_OK[cur_i][cur_j]) + '\t'
        diff_time = right_swich(gl.list_OK[cur_i][3]) - right_swich(gl.list_OK[cur_i][4])
        if gl.max_time < diff_time:
            gl.max_time = diff_time
        if gl.min_time > diff_time:
            gl.min_time = diff_time
        gl.average_time += diff_time
        glb_line = glb_line + str(diff_time) + '\t\n'
        tar_handle.write(glb_line)
        glb_line = ''
        pbar.update(cur_i)
    pbar.finish()
    gl.average_time = gl.average_time / len(gl.list_OK)
    print "--------------------------------"
    print "%15s%d\n%15s%d\n%15s%d\n%15s%f" %("Total Number:",len(gl.list_OK),"Max_time:", gl.max_time,"Min_time:", gl.min_time,"Average_time:", gl.average_time)
    print "--------------------------------"
# set receive arguments
def set_gl_arg():
    gl.Arg_A = '|type=double_quote|'
    gl.Arg_B = '|type=double_quote_ack|'
    gl.Arg_mA = 'bid_quote_id'
    gl.Arg_mB = 'ask_quote_id'
    gl.Arg_mC = 'feedcode'
def yes_time(string):
    hour = int(string[0:2])
    minute = int(string[3:5])
    second = int(string[6:8])
    if hour <= 24 and hour >= 0 and minute < 60 and minute >= 0 and second < 60 and second >= 0:
        return 0
    else:
        return -1    
    
# user input legal judgement
if len(sys.argv) < 2:
    usage()
    sys.exit(-1)
elif len(sys.argv) < 4:
    if os.path.isfile(sys.argv[1]):
        gl.file_input = sys.argv[1]
        if len(sys.argv) < 3:
            gl.file_output = 'result_record.txt'
        else:
            gl.file_output = sys.argv[2]
        gl.file_size = os.path.getsize(sys.argv[1])
    else:
        print "Input file is not effective!"
        sys.exit(-1)
else:
    if os.path.isfile(sys.argv[1]):
        gl.file_input = sys.argv[1]
        gl.file_output = 'result_record.txt'
        gl.file_size = os.path.getsize(sys.argv[1])
    else:
        print "Input file is not effective!"
        sys.exit(-1)
    rev_list = ','.join(sys.argv)
    rev_list = rev_list[rev_list.find(',')+1:]
    rev_list = rev_list[rev_list.find(',')+1:]
    rev_list = rev_list[rev_list.find(',')+1:]
    if rev_list.find('-t') >= 0:
        _t = rev_list[rev_list.find('-t') + 3:]
        if _t.find('-') >= 0:
            _t = _t[:_t.find('-')-1]
        if not yes_time(_t):
            gl.g_time = _t
    if rev_list.find('-n') >= 0:
        _n = rev_list[rev_list.find('-n') + 3:]
        if _n.find('-') >= 0:
            _n = _n[:_n.find('-')-1]
        if int(_n) < 100000:
            gl.g_number = int(_n)
    if rev_list.find('-o') >= 0:
        _o = rev_list[rev_list.find('-o') + 3:]
        if _o.find('-') >= 0:
            _o = _o[:_o.find('-')-1]
        gl.file_output = _o

# main
src_handle = open(gl.file_input, 'rU')
tar_handle = open(gl.file_output, 'w')
try:
    set_gl_arg()
    count()
    gather_result()    
finally:
    tar_handle.close()
    src_handle.close()