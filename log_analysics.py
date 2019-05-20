#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import sys
import configparser


def parse_config(config_file_path):
    cfp = configparser.ConfigParser()
    cfp.read(config_file_path, encoding="utf-8")

    s = cfp.sections()
    dir_item = cfp.items(s[0])
    src_dir = dir_item[0][1]
    log_dir = dir_item[1][1]

    key_item = cfp.items(s[1])

    return src_dir, log_dir, key_item

def tar_file(targetdir):
    tarfilelist = []
    for root, dirs, files in os.walk(targetdir):
        for file in files:
            lentar = len(targetdir.split("/"))
            value = "/".join(os.path.join(root, file).split("/")[lentar:])
            tarfilelist.append(value)

    return tarfilelist


def parse_log(log_name, target_log, key_name):
    f = open(target_log, 'r')
    result = list()

    for line in open(target_log):
        line = f.readline()

        #if( "error" in line or "Warning" in line):
        if(key_name in line):
            result.append(line)
    f.close()
    if(result):
        open(log_name, 'w+').write('%s' % '\n'.join(result))

if __name__ =='__main__':
    print("Begin test!!!")

    source_dir, log_dir, key_word_list = parse_config("configuration.ini")
    key_num = len(key_word_list)

    tar_list = tar_file(source_dir)

    tar_len = len(tar_list)
    print(tar_len)

    print("*******")
    print(tar_list)
    os.chdir(source_dir)


    for tar_name in tar_list:
        os.system("tar xvf " + tar_name)

        log_file = tar_file(source_dir)
        print(log_file)

        #把列表里面的压缩包删除
        for i in range(tar_len):
            log_file.pop(0)

        for log in log_file:
            #print(log)
            len_log = len(log.split("/"))
            #print(len_log)
            log_name = log.split("/")[len_log - 1]
            result_log = log.split("/")
            #print(result_log)
            #log的命名方式为路径命名
            result_log_name = "-".join(result_log)
            print(result_log_name)

            if (log_name != "lastlog"):
                for i in range(key_num):
                    key_name = key_word_list[i][1]
                    #print(key_name)
                    parse_log(result_log_name, log, key_name)

        os.system("mv nvdata-* " + log_dir)
        os.system("rm -r nvdata")



