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
import pickle
import spartan as st
import scipy as S
import numpy as N
import pandas as pd
import io

def coo_submatrix_pull(matr, rows, cols):
    """
    Pulls out an arbitrary i.e. non-contiguous submatrix out of
    a sparse.coo_matrix.
    The new matrix row and col ids are remapped.
    row mapper is actually rows; col mapper is actually cols. i.e. 
    rows[submatrix_row_id] = org_row_id
    cols[submatrix_col_id] = org_col_id
    """
    if type(matr) != S.sparse.coo_matrix:
        raise TypeError('Matrix must be sparse COOrdinate format')

    gr = -1 * N.ones(matr.shape[0])
    gc = -1 * N.ones(matr.shape[1])

    lr = len(rows)
    lc = len(cols)

    ar = N.arange(0, lr)
    ac = N.arange(0, lc)
    gr[rows[ar]] = ar
    gc[cols[ac]] = ac
    mrow = matr.row
    mcol = matr.col
    newelem = (gr[mrow] > -1) & (gc[mcol] > -1)
    newrows = mrow[newelem]
    newcols = mcol[newelem]
    return S.sparse.coo_matrix((matr.data[newelem], N.array([gr[newrows],
        gc[newcols]])),(lr, lc))

def tuples_coo_submatrix_pull(matr, rows, cols):
    """
    Pulls out an arbitrary i.e. non-contiguous submatrix out of
    a sparse.coo_matrix.

    Returns
    ------
    tuples of org_row_id, org_col_id, value
    """
    if type(matr) != S.sparse.coo_matrix:
        raise TypeError('Matrix must be sparse COOrdinate format')

    gr = -1 * N.ones(matr.shape[0])
    gc = -1 * N.ones(matr.shape[1])

    lr = len(rows)
    lc = len(cols)

    ar = N.arange(0, lr)
    ac = N.arange(0, lc)
    gr[rows[ar]] = ar
    gc[cols[ac]] = ac
    mrow = matr.row
    mcol = matr.col
    newelem = (gr[mrow] > -1) & (gc[mcol] > -1)
    newrows = mrow[newelem]
    newcols = mcol[newelem]
    return N.array([newrows, newcols, matr.data[newelem]]).T

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('input', nargs='?', type=str, default=sys.stdin,
                        help="输入文件名. 格式要求0，1列为user和object.")
    parser.add_argument("--delimeter", type=str, default=',',
                        help="输入文件分割符;示例1: , 示例2: \x01")
    parser.add_argument("--timeformat", type=str, default='%Y-%m-%d %H:%M:%S',
                        help="输入数据的时间格式;示例数据%Y-%m-%d %H:%M:%S. \
                        timestamp表示时间已经是时间戳")
    parser.add_argument("--timeidx", type=int, default=2,
                        help="时间列的id(id从0开始);示例数据：0 (表示第一列)")
    parser.add_argument("--hasvalue", action='store_true',
                        help="是否最后一列数据是边的频次或权重")
    parser.add_argument("-c", "--colum", nargs='+', type=str,
                        help="")
    parser.add_argument("--nblocks", type=int, default=1,
                        help="检测密度子图的数目")
    parser.add_argument("--level", choices=[0,1,2,3],type=int, default=0,
                        help="检测运用信号的情况")
    parser.add_argument("-o", "--output", nargs='?', type=argparse.FileType('w'),
            default=sys.stdout, help="输出文件名")
    parser.add_argument("-o2", "--output2", type=str, default='./output/hs_datastructure.pkl',
                        help="输出文件名. pkl文件保存holoscope输出的复杂结构")
    args = parser.parse_args()

    # infile = './inputData/test.reid.gz'
    argsinput = args.input
    argstimeformat = args.timeformat
    argstimeidx = args.timeidx
    columstr = args.colum
    sep = args.delimeter

    if columstr is not None:
        colum = list(map(int, columstr.split(',')))
    else:
        colum = None

    tensor_data = st.loadTensor(path = argsinput, sep=sep,  col_idx=colum,
            header=None)

    if argstimeformat is 'timestamp':
        mappers={argstimeidx:st.IntMapper()}
    else:
        mappers={argstimeidx:st.TimeMapper(timeformat=argstimeformat)}

    stensor = tensor_data.toSTensor(hasvalue=args.hasvalue, mappers=mappers)
    graph = st.Graph(stensor, bipartite=True, weighted=True, modet=argstimeidx)
    hs = st.HoloScope(graph)

    res = hs.run(k=args.nblocks, level=args.level, eps=1.6)

    #store ouput
    rows1, cols1 = res[0][0] #susp rows and level cols
    subtuples = tuples_coo_submatrix_pull(graph.sm.tocoo(), rows1, cols1)
    df = pd.DataFrame(subtuples)
    df.to_csv(args.output, index=False, header=False, sep=sep)

    #store output2
    hs.save(args.output2)
    #out2 = open(args.output2,'wb')
    #pickle.dump(res, out2)

    pass

