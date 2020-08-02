# encoding: utf-8
import spartan as st
import os
import pickle
import sys

import scipy.sparse as ssp

dir_ = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir_)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument('input', nargs='?', type=str,
                        default=sys.stdin, help='edgelist 文件路径')
    parser.add_argument('--turn', type=int, default=20, help='迭代轮数')
    parser.add_argument('-o1', '--output1',
                        default='./summarized.npz', help='输出文件：邻接矩阵')
    parser.add_argument('-o2', '--output2',
                        default='./nodes_dict.pkl', help='输出文件：Supernode 字典')

    args = parser.parse_args()

    data = st.loadTensor(args.input, col_types=[int, int])
    mapper = st.DenseIntMapper()
    tensor = data.toSTensor(hasvalue=False, mappers={0: mapper, 1: mapper})
    N = mapper._idx
    tensor.shape = (N, N)

    summarizer = st.Summarizer(tensor)
    nodes_dict, sm_s = summarizer.run(args.T)


    ssp.save_npz(args.output1, sm_s._data.tocsr())
    pickle.dump(nodes_dict, open(args.output2, 'wb'))

