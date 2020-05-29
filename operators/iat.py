#!/usr/bin/env python
# encoding: utf-8
# @author: ysl
# @file: csvadaptor.py
# @time: 2020/4/17 17:05
# @version v1.0
# @desc:
#
#
import argparse
import sys

import spartan2.basicutil as iatutil
import spartan2.drawutil as drawutil
import spartan2.ioutil as ioutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")
    parser.add_argument("--gridsize", type=int, default=100,
                        help="Histogram的网格数，示例格式:100")
    parser.add_argument("--delimeter", type=str, default='\x01',
                        help="输入文件分割符;示例1: , 示例2: \x01")
    parser.add_argument("--timeformat", type=str, default='%Y-%m-%d %H:%M:%S',
                        help="输入数据的时间格式;示例数据%Y-%m-%d %H:%M:%S")
    parser.add_argument("--timeidx", type=int, default=0,
                        help="时间列的id(id从0开始);示例数据：0 (表示第一列)")
    parser.add_argument("--groupids", nargs='*', type=list, default=[0],
                        help=")时间列的id(id从0开始);示例数据：0 (表示第一列)")
    parser.add_argument("--xlabel", type=str, default='IATn',
                        help="Histogram横坐标的标签")
    parser.add_argument("--ylabel", type=str, default='IATn+1',
                        help="Histogram纵坐标的标签")
    parser.add_argument("-o", "--output", type=str, default='/source/out.jpg',
                        help="输出文件名")
    args = parser.parse_args()

    # infile = './inputData/test.reid.gz'
    argsinput = args.input
    argsgridsize = args.gridsize
    argsdelimeter = args.delimeter
    argstimeformat = args.timeformat
    argstimeidx = args.timeidx
    argsgroupids = args.groupids
    argsxlabel = args.xlabel
    argsylabel = args.ylabel
    argsoutput = args.output
    # outfile='../output/test.iat'
    aggts = ioutil.extracttimes(argsinput, outfile=None, timeidx=argstimeidx, timeformat=argstimeformat, delimeter=argsdelimeter,
                                isbyte=True, comments='#', nodetype=str, groupids=argsgroupids)
    instance = iatutil.IAT()
    instance.calaggiat(aggts)
    xs, ys = instance.getiatpairs()
    drawutil.drawRectbin(xs, ys, gridsize=20, xlabel=argsxlabel, ylabel=argsylabel, outfig=argsoutput)
