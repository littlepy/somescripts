import os
import sys
import csv
from gooey import Gooey, GooeyParser
from configparser import ConfigParser
import time
import logging

# only python3 is supported
# auto create playlist


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.removeHandler(logger.handlers)
logger.addHandler(logging.FileHandler('./run.log', delay=True))
log_fmt = '%(levelname)s,%(asctime)s,line:%(lineno)s,%(message)s'
formatter = logging.Formatter(log_fmt)
logger.handlers[0].setFormatter(formatter)



def crh_playlist(csv_file, destdir, listname):
    ininame = os.path.splitext(os.path.basename(csv_file))[0].strip()+'.ini'
    destfile = os.path.join(destdir, "E27.ini")
    with open(csv_file, 'r') as csv_file:  
        with open(destfile, 'w') as play_list:
            csv_file.seek(0)
            r = csv.reader(csv_file)
            r = filter(lambda x:True if x[0] else False, r)
            r = filter(lambda x:True if x[1] else False, r)
            cf = ConfigParser()
            cf.add_section('LIST-0')
            cf.set('LIST-0', 'list_name', listname)
            for row in r:
                cf.set('LIST-0', 'video-{}'.format(row[0]), '{}.mpg'.format(row[1]))
            cf.write(play_list)
    try:
        f = open(destfile, 'r')
        lines = f.read().strip()
    except IOError as e:
        logger.error(e[-1])
    finally:
        f.close()
    logger.info(lines)
    with open(destfile, 'w') as inifile:
        inifile.write(lines)


def hqbd_playlist(csv_file, destdir):
    ininame = os.path.splitext(os.path.basename(csv_file))[0].strip()+'.ini'
    destfile = os.path.join(destdir, "华启标动.ini")
    with open(csv_file, 'r') as csv_file:  
        with open(destfile, 'w') as play_list:
            csv_file.seek(0)
            r = csv.reader(csv_file)
            r = filter(lambda x:True if x[0] else False, r)
            r = filter(lambda x:True if x[1] else False, r)
            cf = ConfigParser()
            cf.add_section('content')
            for row in r:
                cf.set('content', 'list{}'.format(int(row[0])+1), '{}.ts'.format(row[1]))
            cf.write(play_list)
    try:
        f = open(destfile, 'r')
        lines = f.read().strip()
    except IOError as e:
        logger.error(e[-1])
    finally:
        f.close()
    logger.info(lines)
    with open(destfile, 'w') as inifile:
        inifile.write(lines)


def sfsbd_playlist(csv_file, destdir):
    destfile = os.path.join(destdir, '四方所标动.ini')
    with open(csv_file, 'r') as csv_file:  
        with open(destfile, 'w') as play_list:
            csv_file.seek(0)
            r = csv.reader(csv_file)
            r = filter(lambda x:True if x[0] else False, r)
            r = filter(lambda x:True if x[1] else False, r)
            for row in r:
                play_list.write('{}.mpg\n'.format(row[1]))
    try:
        f = open(destfile, 'r')
        lines = f.read().strip()
    except IOError as e:
        logger.error(e[-1])
    finally:
        f.close()
    logger.info(lines)
    with open(destfile, 'w') as txtfile:
        txtfile.write(lines)

        
def crh_feiying(csv_file, destdir):
    destfile = os.path.join(destdir, '公共频道列表.txt')
    with open(csv_file, 'r') as csv_file:  
        with open(destfile, 'w') as play_list:
            csv_file.seek(0)
            r = csv.reader(csv_file)
            r = filter(lambda x:True if x[0] else False, r)
            r = filter(lambda x:True if x[1] else False, r)
            for row in r:
                play_list.write('{}.mpg\n'.format(row[1]))
    try:
        f = open(destfile, 'r')
        lines = f.read().strip()
    except IOError as e:
        logger.error(e[-1])
    finally:
        f.close()
    logger.info(lines)
    with open(destfile, 'w') as txtfile:
        txtfile.write(lines)
            

def sfs380_playlist(csv_file, destdir):
    destfile = os.path.join(destdir, '四方所380.ini')
    with open(csv_file, 'r') as csv_file:  
        with open(destfile, 'w') as play_list:
            csv_file.seek(0)
            r = csv.reader(csv_file)
            r = filter(lambda x:True if x[0] else False, r)
            r = filter(lambda x:True if x[1] else False, r)
            for row in r:
                play_list.write('公共频道\{}\n'.format(row[1]))
    try:
        f = open(destfile, 'r')
        lines = f.read().strip()
    except IOError as e:
        logger.error(e[-1])
    finally:
        f.close()
    logger.info(lines)
    with open(destfile, 'w') as inifile:
        inifile.write(lines)


def crh_five(csv_file, destdir):
    destfile = os.path.join(destdir, '五型车video.ini')
    with open(csv_file, 'r') as csv_file:  
        with open(destfile, 'w') as play_list:
            csv_file.seek(0)
            r = csv.reader(csv_file)
            r = filter(lambda x:True if x[0] else False, r)
            r = filter(lambda x:True if x[1] else False, r)
            for row in r:
                play_list.write('{};\n'.format(row[1]))
    try:
        f = open(destfile, 'r')
        lines = f.read().strip()
    except IOError as e:
        logger.error(e[-1])
    finally:
        f.close()
    logger.info(lines)
    with open(destfile, 'w') as inifile:
        inifile.write(lines)


@Gooey(language='chinese', program_name="华启智能播放列表生成器V0.5", 
       default_size=(700, 650))
def main():
    desc = "2020.5.21"
    parser = GooeyParser(description=desc)
    parser.add_argument('playlist', metavar="铁总播出单(改好后的csv文件):", widget="FileChooser")
    parser.add_argument('pldir', metavar="播放列表目录:", widget="DirChooser")
    parser.add_argument("plname", metavar='节目单名称(默认为当前日期):', type=str, default=time.strftime("%Y%m%d", time.localtime()))
    parser.add_argument('-a', metavar=" ", action="store_true", help="E27/28播放列表")
    parser.add_argument('-b', metavar="  ", action="store_true", help="380Al(飞鹰、九华)播放列表")
    parser.add_argument('-c', metavar="  ", action="store_true", help="5型车播放列表")
    parser.add_argument('-d', metavar="  ", action="store_true", help="华启标动播放列表")
    parser.add_argument('-e', metavar="  ", action="store_true", help="四方所标动播放列表")
    parser.add_argument('-f', metavar="  ", action="store_true", help="四方所380播放列表")
    args = parser.parse_args(sys.argv[1:])
    
    logger.info(f"影视中心播出单: {args.playlist}")
    logger.info(f"存放播放列表目录: {args.pldir}")
    if not any([args.a, args.b, args.c, args.d]):
        logger.warning("请至少选择一个播放列表类型！")

    if not os.path.exists(args.pldir):
        logger.warning("目录不存在: {}".format(args.pldir))
        logger.warning("开始创建目录：{}".format(args.pldir))
        os.mkdir(args.pldir)
        logger.info("创建目录成功!")

    if args.a:
        logger.info("开始生成：E27/28 播放列表：")
        crh_playlist(args.playlist, args.pldir, args.plname)
    if args.b:
        logger.info("开始生成 飞鹰 播放列表：")
        crh_feiying(args.playlist, args.pldir)
    if args.c:
        logger.info("开始生成 五型车 播放列表：")
        crh_five(args.playlist, args.pldir)
    if args.d:
        logger.info("开始生成 华启标动 播放列表：")
        hqbd_playlist(args.playlist, args.pldir)
    if args.e:
        logger.info("开始生成 四方所标动 播放列表：")
        sfsbd_playlist(args.playlist, args.pldir)
    if args.f:
        logger.info("开始生成 四方所380 播放列表：")
        sfs380_playlist(args.playlist, args.pldir)
    logger.info("所有播放列表生成完毕!")
    

if __name__ == "__main__":
    logger.info("程序启动.")
    sys.exit(main())
