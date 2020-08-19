#!/usr/bin/env python
# encoding: utf-8
# @author: Sunxiaobing
# @file: iat_detect.py
# @time: 2020/8/18
# @version v1.0
# @desc:
#

import argparse
import sys, os
import pickle
import spartan as st
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名")
    parser.add_argument("--gridsize", type=int, default=100,
                        help="Histogram的网格数，示例格式:100")
    parser.add_argument("--xlabel", type=str, default='IATn',
                        help="Histogram横坐标的标签")
    parser.add_argument("--ylabel", type=str, default='IATn+1',
                        help="Histogram纵坐标的标签")
    parser.add_argument("--x", type=float, default=0,
                        help="Histogram查询点的横坐标")
    parser.add_argument("--y", type=float, default=0,
                        help="Histogram查询点的纵坐标")
    parser.add_argument("--radius", type=float, default=1,
                        help="Histogram的查询半径")
    parser.add_argument("--k", type=int, default=10,
                        help="前k个可疑用户")
    parser.add_argument('-o1', "--outfig", nargs='?', type=str, default='./source/out.jpg',
                    help="Histogram图的输出文件")
    parser.add_argument('-o2', "--outfile", type=str, default='./source/user.csv',
                    help="用户的输出文件")
    parser.add_argument('-o3', "--outpdf", type=str, default='./source/pdf.jpg',
                    help="top-k用户的iat分布图的输出文件")

    args = parser.parse_args()

    argsinput = args.input
    argsgridsize = args.gridsize
    argsxlabel = args.xlabel
    argsylabel = args.ylabel
 
    argsx = args.x
    argsy = args.y
    argsradius = args.radius
    argsk = args.k
    argsoutfig = args.outfig
    argsoutfile = args.outfile
    argsoutpdf = args.outpdf

    with open(argsinput, 'rb') as picklefile:
        instance = pickle.load(picklefile)
        picklefile.close()

    xs, ys = instance.getiatpairs()

    # rect: instance of class RectHistogram
    rect = st.RectHistogram(xscale='log', yscale='log', gridsize=argsgridsize)
    fig = rect.draw(xs, ys, outfig=argsoutfig, xlabel=argsxlabel, ylabel=argsylabel)

    xrange, yrange = rect.find_peak_range(x=argsx, y=argsy, radius=argsradius)
    iatpairs = rect.find_peak_rect(xrange, yrange)
    usrlist = instance.find_iatpair_user_ordered(iatpairs, k=argsk)
    df = pd.DataFrame({'user':usrlist})
    df.to_csv(argsoutfile, index=False)

    instance.drawIatPdf(usrlist, outfig=argsoutpdf)