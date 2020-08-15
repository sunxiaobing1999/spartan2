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

import spartan as st

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
    parser.add_argument("--groupids", nargs='*', type=list, default=[1],
                        help=")分组的id(id从0开始);示例数据：1 (表示第二列)")
    parser.add_argument("--xlabel", type=str, default='IATn',
                        help="Histogram横坐标的标签")
    parser.add_argument("--ylabel", type=str, default='IATn+1',
                        help="Histogram纵坐标的标签")
    parser.add_argument("--x", type=int, default=100,
                        help="定位的中心点x轴坐标")
    parser.add_argument("--y", type=int, default=100,
                        help="定位的中心点y轴坐标")
    parser.add_argument("--radius", type=int, default=100,
                        help="以中心点为圆心的搜索半径")
    parser.add_argument("--k", type=int, default=10,
                        help="前k个可疑用户")
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
    argsx = args.x
    argsy = args.y
    argsradius = args.radius
    argsk = args.argsk
    argsoutput = args.output
    # outfile='../output/test.iat'
    
    tensor_data = st.loadTensor(path=argsinput, sep=argsdelimeter)
    coords, data = tensor_data.do_map(hasvalue=False, mappers={timeidx:st.TimeMapper(timeformat=argstimeformat, timebin = 1, mints = 0)})
    aggts = tensor_data.to_aggts(coords, time_col=argstimeidx, group_col=argsgroupids)

    
    instance = st.IAT()
    instance.calaggiat(aggts)
    xs, ys = instance.getiatpairs()
    
    # invoke drawHexbin function
    st.drawHexbin(xs, ys, gridsize=argsgridsize, xlabel=argsxlabel, ylabel=argsylabel)
    # invoke drawRectbin function
    st.drawRectbin(xs, ys, gridsize=argsgridsize, xlabel=argsxlabel, ylabel=argsylabel)
    
    recthistogram = st.RectHistogram(xscale='log', yscale='log', gridsize=argsgridsize)
    fig, H, xedges, yedges = recthistogram.draw(xs, ys, xlabel=argsxlabel, ylabel=argsylabel)
    recthistogram.find_peak_rect(xs, ys, H, xedges, yedges, x=argsx, y=argsy, radius=argsradius)
    
    usrlist = instance.find_iatpair_user_ordered(coordpairs, k=argsk)
    instance.drawIatPdf(usrlist)
    
    

