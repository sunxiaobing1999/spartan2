# -*- coding:utf-8 -*-
import argparse
import sys
sys.path.append('/Users/baby/Documents/GitHub/spartan2/')

import spartan2.basicutil as iatutil
import spartan2.drawutil as drawutil
import spartan2.ioutil as ioutil
import pandas as pd

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
    parser.add_argument("--x", type=float, default=0,
                        help="Histogram查询点的横坐标")
    parser.add_argument("--y", type=float, default=0,
                        help="Histogram查询点的纵坐标")
    parser.add_argument("--radius", type=float, default=1,
                        help="Histogram的查询半径")
    parser.add_argument('-o1', "--outfig", nargs='?', type=str, default='/source/out.jpg',
                    help="图片的输出文件")
    parser.add_argument('-o2', "--outfile", type=str, default='/source/user.csv',
                    help="用户的输出文件")

    args = parser.parse_args()

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
    argsoutfig = args.outfig
    argsoutfile = args.outfile

    aggts = ioutil.extracttimes(argsinput, outfile=None, timeidx=argstimeidx, timeformat=argstimeformat, delimeter=argsdelimeter,
                                isbyte=True, comments='#', nodetype=str, groupids=argsgroupids)
    instance = iatutil.IAT()
    instance.calaggiat(aggts)
    xs, ys = instance.getiatpairs()

    # rect: instance of class RectHistogram
    rect = drawutil.RectHistogram()
    fig, H, xedges, yedges = rect.draw(xs, ys, outfig=argsoutfig, xlabel=argsxlabel, ylabel=argsylabel)
    iatpairs = rect.find_peak_rect(xs, ys, H, xedges, yedges, x=argsx, y=argsy, radius=argsradius)
    usrlist = instance.find_iatpair_user(iatpairs)
    df = pd.DataFrame({'user':usrlist})
    df.to_csv(argsoutfile, index=False)
