# -*- coding: utf-8 -*-
'''
Created on 2016-12-26 15:40
---------
@summary: 将某一文件夹下的代码由驼峰转为下划线
---------
@author: Boris
'''
import os
import fileinput
import re
import sys

def get_file_list(path, ignore = []):
    templist = path.split("*")
    path = templist[0]
    file_type = templist[1] if len(templist) >= 2 else ''

    # 递归遍历文件
    def get_file_list_(path, file_type, ignore, all_file = []):
        file_list =  os.listdir(path)

        for file_name in file_list:
            if file_name in ignore:
                continue

            file_path = os.path.join(path, file_name)
            if os.path.isdir(file_path):
                get_file_list_(file_path, file_type, ignore, all_file)
            else:
                if not file_type or file_name.endswith(file_type):
                    all_file.append(file_path)

        return all_file

    return get_file_list_(path, file_type, ignore) if os.path.isdir(path) else [path]

def get_text(content, regex, ignore = []):
    for text in ignore:
        content = content.replace(text, '')

    return re.findall(regex, str(content), re.S)

def cammel_to_underline(text, words):
    for word in words:
        word_ = ''
        is_first = True
        for character in word:
            if character == character.upper():
                character = character.lower()
                if is_first:
                    character = '_' + character
                    is_first = False
            else:
                is_first = True

            word_ += character

        text = text.replace(word, word_)

    return text


def format_code(path, ignore = []):
    files = get_file_list(path, ignore)
    for file_name in files:
        try:
            infile = open(file_name, 'r', encoding= 'utf8')
            text = infile.read()

            classes = get_text(text, 'class\s+?(.*?)\s*?\(') # 取类名
            words = get_text(text, '[a-z][A-Z]+', ignore = classes) #取aA 类型除外
            text = cammel_to_underline(text, words)

            infile.close()
            bak_file_name = file_name + '_bak'
            if os.path.isfile(bak_file_name):
                os.remove(bak_file_name)
            os.rename(file_name, bak_file_name)

            outfile = open(file_name, 'w', encoding = 'utf8')
            outfile.write(text)
        except Exception as e:
            print('''
                    格式化出错: %s
                    Exception : %s
                    '''%(file_name, str(e))
                 )
        else:
            print(file_name + " 处理完毕")
        finally:
            infile.close()
            outfile.close()

def del_file(path, ignore = []):
    files = get_file_list(path, ignore)
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
           print('''
                删除出错: %s
                Exception : %s
                '''%(file, str(e))
             )
        else:
            print(file + " 删除成功")
        finally:
            pass

def helper():
    '''
    命令格式：python format path
    例如：    python format ../spider/*.py  (可以加任意需要格式化的文件 如 *.txt) 不加为默认格式py文件
    默认：    只格式化.py文件

    '''

def main():
    ignore = ['.git', '.svn', 'config.conf', '__pycache__']
    argv = ''
    path = ''
    if len(sys.argv) > 1:
        argv = sys.argv[1]
    else:
        print(helper.__doc__)
        return

    if argv == '-h':
        print(helper.__doc__)
        return
    else:
        templist = argv.split("*")
        path = templist[0]
        file_type = "*" + templist[1] if len(templist) >= 2 else '*.py'

        format_code(path + file_type, ignore)

        is_del = input("格式化完成, 请运行代码, 若无问题, 是否删除备份? (y/n)")
        print(is_del)
        if is_del == 'y' or is_del == "Y":
            del_file(path + "*_bak", ignore)

if __name__ == '__main__':
    main()