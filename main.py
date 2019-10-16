import  os
import datetime

def process_line(line):
    l = line.split(' ')
    date = get_date(l[0])
    if len(l)>=3 and date[0]:
        l[2] = l[2].split('(')[0]
        return True,l[2],date[1]
    return False,None,None

def get_date(date_text):
    try:
        date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True,date
    except ValueError:
        return False,None

def load_msg(date_request):
    validinput = False
    all_msgs =[]
    with open('./msg_history') as msgs:
        for _,line in enumerate(msgs):
            line = line.rstrip()
            processed = process_line(line)
            if processed[0]:
                if processed[2] == date_request:
                    validinput = True
                    all_msgs.append([processed[1]])
                    continue
            elif validinput == True:
                if filter_line(line,all_msgs[-1][0]):
                    all_msgs.pop()
                    validinput = False
                    continue
                all_msgs[-1].append(line)
                validinput = False
    return all_msgs

def merge_msgs(all_msgs):
    merged_msgs = []
    last_name =''
    last_line = ''
    for _,msg in enumerate(all_msgs):
        if msg[0]!= last_name:
            if _!=0:
                merged_msgs.append([last_name,last_line])
                last_line = ''
            last_name = msg[0]
            last_line +=msg[1]+'\n'
        else:
            last_line +=msg[1]+'\n'
    return merged_msgs

def write_to_files(msgs):
    detail_file = open('./result_detail.txt','a+')
    brief_file = open('./result_zhuoyan.txt','a+')

    for _,msg in enumerate(msgs):
        detail_file.write('{}: {}'.format(msg[0],msg[1]))
        if (msg[0])== '拙言':
            brief_file.write(msg[1])

    detail_file.close()
    brief_file.close()

def filter_line(line,name):
    if len(line) <= 3 or '[表情]' in line or (('嗯' in line or '哈' in line or '谢谢' in line)and name != '拙言') or name =='系统消息':
        return True
    return False
def cleanup():
    for fname in os.listdir('.'):
        if fname.startswith("result"):
            os.remove(os.path.join('.', fname))

def validate_date_from_user(input):
    date_input = input.split('-')
    if len(date_input) ==3:
        date = datetime.datetime(year=int(date_input[0]),month=int(date_input[1]),day=int(date_input[2]))
    elif len(date_input) ==2 :
        date = datetime.datetime(year=datetime.date.today().year, month=int(date_input[0]), day=int(date_input[1]))
    else:
        print ("格式不正确，重新输入")
        return False,None
    return True,date

def get_date_from_user():
    date = input('输入要提取的日期 - 参考格式（{}）'.format(datetime.date.today()))
    result = validate_date_from_user(date)
    if result[0]==False:
        get_date_from_user()
    else:
        return result[1]

def run_processor():
    cleanup()
    date = get_date_from_user()
    print('开始运行。。。')
    msgs = load_msg(date)
    merged_msg = merge_msgs(msgs)
    write_to_files(merged_msg)
    print ('运行结束。。。')

run_processor()
