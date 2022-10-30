import global_var
import item_init
import source_init
import recognition
import log
import ast

# Change this flag to disable logger
flag_disable_log = False
global_var.append('_flag_disable_log', flag_disable_log)

flag_history = False
flag_target_set = False


def yes_or_no(prompt):
    yn = input(prompt)
    while (True):
        if (not (yn == 'Y' or yn == 'y' or yn == 'N' or yn == 'n')):
            yn = input('输入有误，请重试：\t')
        else:
            break
    if (yn == 'Y' or yn == 'y'):
        return True
    else:
        return False


def main():
    print('Welcome to ArkDrop by lcebot!\n', end='')

    global flag_history, flag_target_set

    counter = {}
    targets = {}
    try:
        with open('history.sav', 'r+') as f:
            counter, targets = ast.literal_eval(f.read())
            flag_history = True
        if (not yes_or_no('已找到历史记录，是否继承数据？(Y/N)\t')):
            flag_history = False
            counter = {}
            targets = {}
    except:
        pass

    if (yes_or_no('是否需要' + ('额外' if flag_history else '') + '设置刷图目标？(Y/N)\t')):
        flag_target_set = True
        with open('./res/id_dict.txt', 'r') as f:
            id_name = ast.literal_eval(f.read())

        tar = input('请输入材料名，输入#结束：\t')
        while (True):
            if tar in id_name:
                tar_n = int(eval(input('请输入目标数量：\t')))
                while (tar_n < 0):
                    tar_n = input('输入有误，请重试：\t')
                targets[id_name[tar]] = tar_n
                tar = input('已确认。\n\n请输入材料名，输入#结束：\t')
            else:
                if (tar == '#'):
                    break
                else:
                    tar = input('输入有误，请重试：\t')

    print('请将截图放到input文件夹，按回车继续。\n', end='')
    input()
    print('识别开始，请耐心等候...\n', end='')
    item_init.init()
    source_init.init()

    icon_keypoints = global_var.read('_icon_keypoints')
    icon_descriptors = global_var.read('_icon_descriptors')
    inputs = global_var.read('_inputs')

    log.begin_log()

    log.write_log('Recognition begin')
    screenshot_cnt = 0
    for screenshot in inputs:
        screenshot_cnt += 1
        for item_id, kp in icon_keypoints.items():
            get_res = recognition.recognizer(kp, icon_descriptors[item_id], screenshot, item_id, screenshot_cnt)
            if get_res >= 1:
                if item_id in counter:
                    counter[item_id] += get_res
                else:
                    counter[item_id] = get_res
    log.write_log('Recognition complete')

    with open('history.sav', 'w') as f:
        f.write(str(counter) + ',' + str(targets))
    print('识别完成，本次识别结果和目标已保存到history.sav。\n', end='')

    if (flag_target_set):
        print('\n刷图总结：\n', end='')
        for item_id, quantity in targets.items():
            print('\t' + global_var.read('_item_name')[item_id] + '：目标', quantity, '个，已刷',
                  0 if item_id not in counter else counter[item_id], '个')

    print('\n感谢使用！按任意键退出。\n', end='')
    input()


if __name__ == '__main__':
    main()
