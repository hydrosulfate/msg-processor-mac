import os
import time


def process_line(line):
    return line.split(":")


def load_msg():
    all_msgs = []
    with open('./msg_history') as msgs:
        last = ''
        for _, line in enumerate(msgs):
            processed = process_line(line)
            print (processed)
            if not filter_line(processed[1], processed[0]):
                if last != processed[0]:
                    all_msgs.append(processed)
                    last = processed[0]
                else:
                    all_msgs[-1][1] += processed[1]

    return all_msgs


def skip_msgs(msgs):
    start = -1
    end = -1
    for _, msg in enumerate(msgs):
        if msg[0] == '李金主':
            end = _
            if start == -1:
                start = _

    return msgs[start:end + 1]


def write_to_files(msgs):
    detail_file = open('./result_detail.txt', 'a+')
    brief_file = open('./result_zhuoyan.txt', 'a+')

    for _, msg in enumerate(msgs):
        detail_file.write('{}: {}'.format(msg[0], msg[1]))
        if (msg[0]) == '李金主':
            brief_file.write(msg[1])

    detail_file.close()
    brief_file.close()


def filter_line(line, name):
    if name == '李金主':
        return False
    # if '[' in line and ']' in line \
    #         or ((
    #         len(line) <= 4
    #         or '嗯' in line
    #         or '哈' in line
    #         or '谢谢' in line
    #         or '师父' in line and '辛苦' in line
    # )) \
    #         or name == '系统消息':
    #     return True
    # return False


def cleanup():
    for fname in os.listdir('.'):
        if fname.startswith("result"):
            os.remove(os.path.join('.', fname))


def run_processor():
    cleanup()
    print('开始运行。。。')
    msgs = load_msg()
    skipped_msg = skip_msgs(msgs)
    write_to_files(skipped_msg)
    print('运行结束。。。')


run_processor()
