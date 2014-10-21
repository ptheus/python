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
    widgets = ['Analysising: ',Percentage(), ' ', Bar(marker='|',left='|',right='|'),'[', FormatLabel('%(elapsed)s'), ']']
    pbar = ProgressBar(widgets=widgets, maxval=100)
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
    widgets = ['Gather result: ',Percentage(), ' ', Bar(marker='|',left='|',right='|'),'[', FormatLabel('%(elapsed)s'), ']']
    pbar = ProgressBar(widgets=widgets, maxval=len(gl.list_OK))
    pbar.start()
    diff_time = 0
    glb_line = ''
    for cur_i in range(len(gl.list_OK)):
        for cur_j in range(len(gl.list_OK[cur_i]) - 2):
            glb_line = glbline + get_value(gl.list_OK[cur_i][cur_j]) + '\t'
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
    
    
    
# user input legal judgement
if len(sys.argv) < 3:
    usage()
    sys.exit(-1)
elif len(sys.argv) == 3:
    if sys.argv[1]
    if sys.argv[1] != "-m" and sys.argv[1] != "-f"and sys.argv[1] != "-i" and sys.argv[1] != "-o":
        if os.path.isfile(sys.argv[1]):
            input_file = sys.argv[1]
            input_file_flag = 1
        else:
            print "Input file is not effective!"
            sys.exit(-1)
    else:
        usage()
        sys.exit(-1)
else:
    if sys.argv[1] == "-m" or sys.argv[1] == "-f"or sys.argv[1] == "-i" or sys.argv[1] == "-o":
        rev_list = " ".join(sys.argv)
        rev_list = rev_list[rev_list.find(" ") + 1:]
        if rev_list.find("-i") < 0:
            print "No Input File, Please Check..."
            sys.exit(-1)
    else:
        if os.path.isfile(sys.argv[1]):
            rev_list = " ".join(sys.argv)
            input_tmp = rev_list[rev_list.find(" ") + 1:rev_list.find("-")-1]
            if rev_list != sys.argv[1]:
                print "Your input is more than one file name. please check..."
                sys.exit(-1)
            rev_list = rev_list[rev_list.find(" ") + 1:]
            rev_list = rev_list[rev_list.find(" ") + 1:]
            input_file = sys.argv[1]
            input_file_flag = 1
        else:
            print "Your input file name is not exist. please check..."
            sys.exit(-1)
    if input_file_flag == 1 and rev_list.find("-i") >= 0:
        print "Two input file. please check..."
        sys.exit(-1)


    if rev_list.find("-i") >= 0:
        _i = rev_list[rev_list.find("-i") + 3:]
        if _i.find("-") >= 0:
            _i = _i[:_i.find("-") - 1]
        if len(_i.split(' ')) == 1:
            if os.path.isfile(_i):
                input_file = _i
            else:
                print "File is not exist!"
                sys.exit(-1)
        else:
            print "Error: -i follow wrong argument.\nYour input is more than one file name. please check..."
            sys.exit(-1)
    if rev_list.find("-o") >= 0:
        _o = rev_list[rev_list.find("-o") + 3:]
        if _o.find("-") >= 0:
            _o = _o[:_o.find("-") - 1]
        if len(_o.split(' ')) == 1:
                output_file = _o
        else:
            print "Error: -o follow wrong argument.\nYour output is more than one file name. please check..."
            sys.exit(-1)
    if rev_list.find("-f") >= 0:
        _f = rev_list[rev_list.find("-f") + 3:]
        if _f.find("-") >= 0:
            _f = _f[:_f.find("-") - 1]
        if len(_f.split(' ')) == 2:
            _f_tmp = _f.split(' ')
            lch_arg_A = _f_tmp[0]
            lch_arg_B = _f_tmp[1]
        else:
            print "Error: -f follow wrong argument.\n You must have two argument if you use -f. please check..."
            sys.exit(-1)
    if rev_list.find("-m") >= 0:
        _m = rev_list[rev_list.find("-m") + 3:]
        if _m.find("-") >= 0:
            _m = _m[:_m.find("-") - 1]
        if len(_m.split(' ')) == 3:
            _m_tmp = _m.split(' ')
            mch_arg_A = _m_tmp[0]
            mch_arg_B = _m_tmp[1]
            mch_arg_C = _m_tmp[2]
        else:
            print "Error: -m follow wrong argument.\n You must have three argument if you use -m. please check..."
            sys.exit(-1)
    
    
    
    
# main
src_handle = open(gl.file_input, 'rU')
tar_handle = open(gl.file_output, 'w')
try:
    count()
    gather_result()    
finally:
    tar_handle.close()
    src_handle.close()