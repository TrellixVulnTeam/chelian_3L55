#----------------------------------------------
# -*- encoding=utf-8 -*-                      #
# __author__:'焉知飞鱼'                        #
# CreateTime:                                 #
#       2019/12/4 16:55                       #
#                                             #
#               天下风云出我辈，                 #
#               一入江湖岁月催。                 #
#               皇图霸业谈笑中，                 #
#               不胜人生一场醉。                 #
#----------------------------------------------
'''
    功能：
        - 统计文件有多少行
        - 查看文件的前N行
        - 随机取N行作为测试样本
    usage: head.py [-h] [--number NUMBER] [--random] [--count] file

    查看文件的前N行或者随机N行，也可以统计文件的行数

    positional arguments:
      file                  输入文件

    optional arguments:
      -h, --help            show this help message and exit
      --number NUMBER, -n NUMBER
                            行数
      --random, -r          是否启用随机模式
      --count, -c           统计文件有多少行
'''
import argparse
from time import clock
from random import choice


def lineCounter(hfile):
    '''统计文件有多少行'''
    cnt = 0
    line = hfile.readline()
    while line:
        cnt += 1
        if cnt % 10000 == 0:
            print('当前行数: %d.' % cnt)
        line = hfile.readline()
    print('共有%d行.' % cnt)


def main():
    parser = argparse.ArgumentParser(
        description='查看文件的前N行或者随机N行，也可以统计文件的行数')
    parser.add_argument('file', help='输入文件')
    parser.add_argument('--number', '-n', help='行数', type=int, default=10)
    parser.add_argument('--random', '-r', help='是否启用随机模式',
                        action='store_true', default=False)
    parser.add_argument('--count', '-c', help='统计文件有多少行',
                        action='store_true', default=False)
    args = parser.parse_args()
    if args.count:
        clock()
        with open(args.file) as file:
            lineCounter(file)
        print('耗时%f秒.' % (clock()))
    else:
        with open(args.file) as file:
            line = file.readline()
            cnt = 0
            while line and cnt < args.number:
                if not args.random or choice([True, False]):
                    print(line.strip())
                    cnt += 1
                line = file.readline()


if __name__ == '__main__':
    main()