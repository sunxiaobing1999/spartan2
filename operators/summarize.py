# encoding: utf-8
import os
import pickle
import sys

import numpy as np
import scipy
import scipy.sparse as ssp

import sys
dir_ = os.path.dirname(os.path.dirname(__file__))
sys.path.append(dir_)
import spartan2.spartan as st
from spartan2.models.summarize.summarizer import Summarizer

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="")

    parser.add_argument('input', nargs='?', type=str, default=sys.stdin, help='edgelist 文件路径')
    parser.add_argument('--dataset', type=str, default='dataset', help='数据集名称')
    parser.add_argument('-o1', '--output1', default='./summarized.m', help='输出文件：邻接矩阵')
    parser.add_argument('-o2', '--output2', default='./nodes.dict', help='输出文件：Supernode 字典')

    args = parser.parse_args()
    input_ = args.input
    dataset = args.dataset

    t = st.loadTensor(input_, '', col_idx=None, col_types=[int, int], hasvalue=0)
    g = t.toGraph(bipartite=False, directed=False)
    sm = g.sm

    summarizer = Summarizer(sm)
    sm_s, node_dict = summarizer.summarize(dataset)

    scipy.io.savemat(args.output1, {'sm': sm_s})
    pickle.dump(node_dict, open(args.output2, 'wb'))
