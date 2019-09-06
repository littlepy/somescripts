#!/usr/bin/python

import os, sys
from time import sleep
import binascii

def hex2str(hex):
    return str(int(hex, 16))

def unhex(hex):
    s = ''
    for i in hex:
        s += '{0:0>2}'.format(str(hex(i))[2:])
    return (s)

def get_date(hex):
    year = hex2str(hex[0:2]) + hex2str(hex[2:4])
    month = hex2str(hex[4:6])
    day = hex2str(hex[6:])

    return f"{year}年{month}月{day}日"

def get_time(hex):
    hour = hex2str(hex[0:2])
    minute = hex2str(hex[2:4])
    seconds = hex2str(hex[4:])

    return f"{hour}时{minute}分{seconds}秒"

def get_speed(hex):
    return hex2str(hex)

def get_train_no(hex):
    hex_list = []
    start = 0
    stop = start + 2
    while stop < len(hex):
        value = hex[start:stop]
        if value != '00':
            hex_list.append(value)
        start = stop
        stop = start + 2
    try:
        return binascii.unhexlify(''.join(hex_list)).decode()
    except UnicodeDecodeError:
        return "UnicodeDecodeError: "+hex


# def get_train_no(hex):
#     # return binascii.unhexlify(hex)
#     return hex




def get_distance(hex):
    return hex2str(hex)

def get_route(hex):
    start = hex2str(hex[0:6])
    stop = hex2str(hex[6:])

    return f"{start}-{stop}"



def get_pis_info(file):
    data = '___'
    if file.tell() != 0:
        file.seek(0)
    while data:
        if 'cmd_type = 4' in data:
            print(data)
            hex_data = data.split(':')[-1]
            hex_data = hex_data.replace(' ', '').strip()
            header = hex_data[0:10]
            date = hex_data[10:18]
            time = hex_data[18:24]
            speed = hex_data[24:28]
            train_no = hex_data[28:50]
            distance = hex_data[50:54]
            route_start = hex_data[54:60]
            route_stop = hex_data[60:66]
            route = route_start+route_stop

            print(f"日期: {get_date(date)}, 时间: {get_time(time)}, "
                  f"车次: {get_train_no(train_no)}, 速度: {get_speed(speed)}, "
                  f"里程: {get_distance(distance)}, "
                  f"区间: {get_route(route)}")
            #sleep(1)
            print(file.name)

        data = file.readline()





if __name__ == '__main__':
    log_path = sys.argv[1]
    file_list = os.listdir(log_path)
    for file in file_list:
        os.chdir(log_path)
        with open(file) as file:
            get_pis_info(file)