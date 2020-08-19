#!/usr/bin/env python
# encoding: utf-8
# @author: Sunxiaobing
# @file: iat.py
# @time: 2020/8/18
# @version v1.0
# @desc:
#
#
import argparse
import sys, os
import pickle
import spartan as st

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")
    parser.add_argument("--delimeter", type=str, default='\x01',
                        help="输入文件分割符;示例1: , 示例2: \x01")
    parser.add_argument("--timeformat", type=str, default='%Y-%m-%d %H:%M:%S',
                        help="输入数据的时间格式;示例数据%Y-%m-%d %H:%M:%S")
    parser.add_argument("--timeidx", type=int, default=0,
                        help="时间列的id(id从0开始);示例数据：0 (表示第一列)")
    parser.add_argument("--groupids", nargs='*', type=list, default=[1],
                        help=")分组的id(id从0开始);示例数据：1 (表示第二列)")
    parser.add_argument("--type", type=str, default='Rectangle',
                        choices=["Rectangle","Hexagon"], help="Histogram的类型")
    parser.add_argument("--gridsize", type=int, default=100,
                        help="Histogram的网格数，示例格式:100")
    parser.add_argument("--xlabel", type=str, default='IATn',
                        help="Histogram横坐标的标签")
    parser.add_argument("--ylabel", type=str, default='IATn+1',
                        help="Histogram纵坐标的标签")
    parser.add_argument("-o1", "--outpkl", type=str, default='./source/iat_data.pkl',
                        help="输出文件名")
    parser.add_argument("-o2", "--outfig", nargs='?', type=str, default='./source/out.jpg',
                        help="图片的输出文件")
    args = parser.parse_args()

    # infile = './input/test.reid.gz'
    argsinput = args.input
    argsgridsize = args.gridsize
    argsdelimeter = args.delimeter
    argstimeformat = args.timeformat
    argstimeidx = args.timeidx
    argsgroupids = args.groupids
    argstype = args.type
    argsxlabel = args.xlabel
    argsylabel = args.ylabel
    argsoutpkl = args.outpkl
    argsoutfig = args.outfig
    # outfile='./output/test.iat'

    tensor_data = st.loadTensor(path=argsinput, sep=argsdelimeter)
    coords, data = tensor_data.do_map(hasvalue=False,
            mappers={argstimeidx:st.TimeMapper(timeformat=argstimeformat, timebin = 1, mints = 0)})
    aggts = tensor_data.to_aggts(coords, time_col=argstimeidx, group_col=argsgroupids)


    instance = st.IAT()
    instance.calaggiat(aggts)
    xs, ys = instance.getiatpairs()

    if not os.path.exists(os.path.split(argsoutpkl)[0]): # 目录不存在，则创建
        os.makedirs(os.path.split(argsoutpkl)[0])

    with open(argsoutpkl, 'wb') as outputpkl: # 保存数据到文件
        pickle.dump(instance, outputpkl)
        outputpkl.close()

    if argstype == 'Hexagon': # invoke drawHexbin function
        st.drawHexbin(xs, ys, outfig=argsoutfig, gridsize=argsgridsize, xlabel=argsxlabel, ylabel=argsylabel)
    elif argstype == 'Rectangle': # invoke drawRectbin function
        st.drawRectbin(xs, ys, outfig=argsoutfig, gridsize=argsgridsize, xlabel=argsxlabel, ylabel=argsylabel)
